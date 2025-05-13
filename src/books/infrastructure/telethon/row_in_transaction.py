from enum import StrEnum
from typing import cast
from uuid import UUID

from effect import (
    Effect,
    IdentifiedValueSet,
    LifeCycle,
)

from books.infrastructure.telethon.row import Row, RowSchema


class State(StrEnum):
    created = "created"
    translated = "translated"
    mutated = "mutated"
    deleted = "deleted"


def schema_of_row_in_transaction(
    schema: RowSchema
) -> RowSchema:
    return RowSchema(
        schema.name,
        schema.id_type,
        (*schema.body_types, State, UUID),
    )


def schema_of_row_not_in_transaction(
    schema: RowSchema
) -> RowSchema:
    return RowSchema(
        schema.name,
        schema.id_type,
        schema.body_types[:-2],
    )


def rows_in_transaction(
    effect: LifeCycle[Row],
    transaction_id: UUID,
) -> tuple[Row, ...]:
    rows_by_state = {
        State.created: effect.new_values,
        State.translated: effect.translated_values,
        State.mutated: effect.mutated_values,
        State.deleted: effect.dead_values,
    }

    return tuple(
        Row(
            row.id,
            (*Row.body, state, transaction_id),
            schema_of_row_in_transaction(row.schema)
        )
        for state, rows in rows_by_state.items()
        for row in rows
    )


def row_not_in_transaction(row_in_transaction: Row) -> Row:
    return Row(
        row_in_transaction.id,
        row_in_transaction.body[:-2],
        schema_of_row_not_in_transaction(
            row_in_transaction.schema
        ),
    )


def effect_from_rows_in_transaction(
    rows_in_transaction: tuple[Row, ...],
) -> LifeCycle[Row]:
    new_values = list[Row]()
    translated_values = list[Row]()
    mutated_values = list[Row]()
    dead_values = list[Row]()

    for row in rows_in_transaction:
        row_not_in_transaction_ = row_not_in_transaction(row)

        match cast(State, row[-2]):
            case State.created:
                new_values.append(row_not_in_transaction_)
            case State.translated:
                translated_values.append(row_not_in_transaction_)
            case State.mutated:
                mutated_values.append(row_not_in_transaction_)
            case State.deleted:
                dead_values.append(row_not_in_transaction_)

    return Effect(
        None,
        new_values=IdentifiedValueSet(new_values),
        translated_values=IdentifiedValueSet(translated_values),
        mutated_values=IdentifiedValueSet(mutated_values),
        dead_values=IdentifiedValueSet(dead_values),
    )
