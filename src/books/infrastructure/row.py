from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, cast, overload
from urllib import parse
from uuid import UUID

from effect import IdentifiedValue, LifeCycle


type RowAttribute = bool | int | str | datetime | UUID | StrEnum


@dataclass(frozen=True)
class RowSchema[IdT: RowAttribute = RowAttribute](Sequence[type[RowAttribute]]):
    name: str
    id_type: type[IdT]
    body_types: tuple[type[RowAttribute], ...]

    def __iter__(self) -> Iterator[type[RowAttribute]]:
        yield self.id_type  # type: ignore[misc]
        yield from self.body_types

    @overload
    def __getitem__(self, index: int, /) -> type[RowAttribute]: ...

    @overload
    def __getitem__(
        self, slice_: "slice[Any, Any, Any]", /
    ) -> Sequence[type[RowAttribute]]: ...

    def __getitem__(
        self, value: "int | slice[Any, Any, Any]", /
    ) -> Sequence[type[RowAttribute]] | type[RowAttribute]:
        return tuple(self)[value]

    def __len__(self) -> int:
        return len(self.body_types) + 1


class RowSchemaError[IdT: RowAttribute](Exception):
    def __init__(self, schema: RowSchema[IdT]) -> None:
        self.schema = schema
        super().__init__()


@dataclass(frozen=True)
class Row[IdT: RowAttribute = RowAttribute](
    IdentifiedValue[IdT], Sequence[RowAttribute]
):
    body: tuple[RowAttribute, ...]
    schema: RowSchema[IdT]

    def __post_init__(self) -> None:
        for attribute_and_type in zip(self, self.schema, strict=False):
            if len(attribute_and_type) != 2:  # noqa: PLR2004
                raise RowSchemaError(self.schema)

            attribute, type = attribute_and_type

            if not isinstance(attribute, type):
                raise RowSchemaError(self.schema)

    def __iter__(self) -> Iterator[RowAttribute]:
        yield self.id
        yield from self.body

    @overload
    def __getitem__(self, index: int, /) -> RowAttribute: ...

    @overload
    def __getitem__(
        self, slice_: "slice[Any, Any, Any]", /
    ) -> Sequence[RowAttribute]: ...

    def __getitem__(
        self, value: "int | slice[Any, Any, Any]", /
    ) -> Sequence[RowAttribute] | RowAttribute:
        return tuple(self)[value]

    def __len__(self) -> int:
        return len(self.body) + 1


def row_from_attributes[IdT: RowAttribute](
    attrs: tuple[RowAttribute, ...],
    schema: RowSchema[IdT],
) -> Row[IdT]:
    if not attrs:
        raise RowSchemaError(schema)

    id, *body = attrs

    return Row(cast(IdT, id), tuple(body), schema)


def encoded_attribute_value(value: RowAttribute) -> str:
    if isinstance(value, bool):
        return str(int(value))

    if isinstance(value, int):
        return str(value)

    if isinstance(value, str):
        return parse.quote(value)

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, StrEnum):
        return parse.quote(value.value)

    return str(value)


def decoded_bool_attribute(encoded_value: str, _: object) -> bool | None:
    match encoded_value:
        case "1":
            return True
        case "0":
            return False
        case _:
            return None


def decoded_int_attribute(
    encoded_value: str,
    _: object,
) -> int | None:
    try:
        return int(encoded_value)
    except ValueError:
        return None


def decoded_str_attribute(
    encoded_value: str,
    _: object,
) -> str:
    return parse.unquote(encoded_value)


def decoded_datetime_attribute(
    encoded_value: str,
    _: object,
) -> datetime | None:
    try:
        return datetime.fromisoformat(encoded_value)
    except ValueError:
        return None


def decoded_uuid_attribute(
    encoded_value: str,
    _: object,
) -> UUID | None:
    try:
        return UUID(hex=encoded_value)
    except ValueError:
        return None


def decoded_str_enum_attribute(
    encoded_value: str,
    enum_type: type[StrEnum]
) -> StrEnum | None:
    try:
        return enum_type(parse.unquote(encoded_value))
    except ValueError:
        return None


decoded_attribute_func_by_attribute_type = {
    bool: decoded_bool_attribute,
    int: decoded_int_attribute,
    str: decoded_str_attribute,
    datetime: decoded_datetime_attribute,
    UUID: decoded_uuid_attribute,
    StrEnum: decoded_str_enum_attribute
}


attribute_separator = " "
attrubute_header_end = "="
max_encoded_row_size = 4000


class TooLargeEncodedRowError(Exception): ...


def encoded_row(row: Row) -> str:
    encoded_attributes = (
        encoded_attribute(row.schema, attribute_number, attribute)
        for attribute_number, attribute in enumerate(row)
    )
    encoded_row_ = attribute_separator.join(encoded_attributes)

    if len(encoded_row_) > max_encoded_row_size:
        raise TooLargeEncodedRowError

    return encoded_row_


def encoded_attribute(
    schema: RowSchema,
    attribute_number: int,
    attribute: RowAttribute,
) -> str:
    header = encoded_attribute_header(attribute_number, schema)
    body = encoded_attribute_value(attribute)

    return f"{header}{body}"


def encoded_attribute_header(
    attribute_number: int,
    schema: RowSchema,
) -> str:
    return (
        f"{schema.name}{attribute_number}{attrubute_header_end}"
    )


def decoded_attribute(
    schema: RowSchema,
    attribute_number: int,
    encoded_attribute: str,
) -> RowAttribute | None:
    header_end_index = encoded_attribute.find(attrubute_header_end)

    if header_end_index == -1:
        return None

    header = encoded_attribute[:header_end_index + 1]
    body = encoded_attribute[header_end_index + 1:]

    excepted_header = encoded_attribute_header(attribute_number, schema)

    if header != excepted_header:
        return None

    raw_attribute = parse.unquote(body)
    attribute_type = schema[attribute_number]

    decoded_attribute_func = decoded_attribute_func_by_attribute_type[
        attribute_type
    ]

    return decoded_attribute_func(raw_attribute, attribute_type)  # type: ignore[arg-type]


def decoded_row[IdT: RowAttribute](
    schema: RowSchema[IdT], encoded_row: str
) -> Row[IdT]:
    encoded_attributes = encoded_row.split(attribute_separator)

    attributes = tuple(
        decoded_attribute(
            schema,  # type: ignore[arg-type]
            attribute_number,
            encoded_attribute,
        )
        for attribute_number, encoded_attribute in enumerate(encoded_attributes)
    )

    if any(attribute is None for attribute in attributes):
        raise RowSchemaError(schema)

    return row_from_attributes(
        cast(tuple[RowAttribute, ...], attributes),
        schema,
    )


def processed_encoded_row[IdT: RowAttribute](
    processed_row: Callable[[Row[IdT]], LifeCycle[Row[IdT]]],
    encoded_row_: str,
    encoded_row_schema: RowSchema[IdT]
) -> LifeCycle[Row[IdT]]:

    return processed_row(decoded_row(encoded_row_schema, encoded_row_))


def map_encoded_row[IdT: RowAttribute](
    next_row: Callable[[Row[IdT]], Row[IdT]],
    encoded_row_: str,
    encoded_row_schema: RowSchema[IdT]
) -> str:
    next_row_ = next_row(decoded_row(encoded_row_schema, encoded_row_))

    return encoded_row(next_row_)  # type: ignore[arg-type]


def select_query(
    schema: RowSchema, attribute_number: int, attribute: RowAttribute | None
) -> str:
    if attribute is None:
        return encoded_attribute_header(attribute_number, schema)

    return encoded_attribute(schema, attribute_number, attribute)
