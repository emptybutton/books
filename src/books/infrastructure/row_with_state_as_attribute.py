from enum import StrEnum
from typing import cast

from effect import (
    Effect,
    IdentifiedValueSet,
    LifeCycle,
)

from books.infrastructure.row import Row, RowAttribute, RowSchema


class State(StrEnum):
    created = "created"
    translated = "translated"
    mutated = "mutated"
    deleted = "deleted"


def schema_of_row_with_state[IdT: RowAttribute](
    schema: RowSchema[IdT]
) -> RowSchema[IdT]:
    return RowSchema(
        f"__{schema.name}WithState__",
        schema.id_type,
        (*schema.body_types, State),
    )


def schema_of_row_without_state[IdT: RowAttribute](
    schema: RowSchema[IdT]
) -> RowSchema[IdT]:
    return RowSchema(
        schema.name[len("__"):-len("WithState__")],
        schema.id_type,
        schema.body_types[:-1],
    )


def rows_with_state_as_attribute(
    effect: LifeCycle[Row]
) -> tuple[Row, ...]:
    rows_by_state = {
        State.created: effect.new_values,
        State.translated: effect.translated_values,
        State.mutated: effect.mutated_values,
        State.deleted: effect.dead_values,
    }

    return tuple(
        Row(row.id, (*Row.body, state), schema_of_row_with_state(row.schema))
        for state, rows in rows_by_state.items()
        for row in rows
    )


def row_without_state_as_attribute[IdT: RowAttribute](
    row: Row[IdT]
) -> Row[IdT]:
    return Row(
        row.id,
        row.body,
        schema_of_row_without_state(row.schema),
    )


def effect_from_rows_with_state_as_attribute(
    rows_with_state_as_attribute: tuple[Row, ...],
) -> LifeCycle[Row]:
    new_values = list[Row]()
    translated_values = list[Row]()
    mutated_values = list[Row]()
    dead_values = list[Row]()

    for row in rows_with_state_as_attribute:
        match cast(State, row[-1]):
            case State.created:
                new_values.append(row_without_state_as_attribute(row))
            case State.translated:
                translated_values.append(row_without_state_as_attribute(row))
            case State.mutated:
                mutated_values.append(row_without_state_as_attribute(row))
            case State.deleted:
                dead_values.append(row_without_state_as_attribute(row))

    return Effect(
        None,
        new_values=IdentifiedValueSet(new_values),
        translated_values=IdentifiedValueSet(translated_values),
        mutated_values=IdentifiedValueSet(mutated_values),
        dead_values=IdentifiedValueSet(dead_values),
    )
