from enum import StrEnum
from uuid import UUID

from books.infrastructure.telethon.row import RowSchema


class TransactionResult(StrEnum):
    committed = "committed"
    rollbacked = "rollbacked"


transaction_result_row_schema = RowSchema(
    "__transaction_result__",
    UUID,
    (TransactionResult, ),
)
