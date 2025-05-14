from dataclasses import dataclass

from books.infrastructure.telethon.in_telegram.value import InTelegramValue
from books.infrastructure.telethon.row import (
    Row,
    RowSchema,
    decoded_row,
    encoded_row,
)


@dataclass(frozen=True)
class InTelegramRow(InTelegramValue[Row]):
    schema: RowSchema

    def _encoded(self, row: Row) -> str:
        if row.schema != self.schema:
            raise ValueError

        return encoded_row(row)

    def _decoded(self, encoded_row: str) -> Row:
        return decoded_row(self.schema, encoded_row)
