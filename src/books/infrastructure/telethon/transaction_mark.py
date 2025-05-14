from enum import StrEnum
from uuid import UUID

from books.infrastructure.telethon.row import RowSchema


transaction_uniqueness_mark_schema = RowSchema(
    "__transaction_uniqueness__", UUID, (str, UUID)
)


class TransactionState(StrEnum):
    started = "started"
    committed = "committed"
    rollbacked = "rollbacked"


transaction_state_mark_schema = RowSchema(
    "__transaction_result__",
    UUID,
    (TransactionState, ),
)
