from asyncio import gather
from collections import defaultdict
from collections.abc import AsyncIterator, Sequence
from dataclasses import dataclass, field
from typing import NoReturn, cast
from uuid import UUID

from effect import LifeCycle
from telethon import TelegramClient
from telethon.types import Message

from books.infrastructure.telethon.client_pool import TelegramClientPool
from books.infrastructure.telethon.message_queque import InTelegramMessageQueque
from books.infrastructure.telethon.pointer import InTelegramPointer
from books.infrastructure.telethon.row import (
    Row,
    RowSchema,
    decoded_row,
    schema_name_of_encoded_row,
)
from books.infrastructure.telethon.row_in_transaction import (
    effect_from_rows_in_transaction,
    schema_of_row_in_transaction,
)
from books.infrastructure.telethon.transaction_result_row import (
    TransactionResult,
    transaction_result_row_schema,
)


# effect_from_rows_in_transaction


async def executed_telegram_log(
    log: InTelegramMessageQueque,
    replication_slot_pointers: Sequence[InTelegramPointer[int]],
    schema_by_schema_name: dict[str, RowSchema],
) -> NoReturn:
    schema_in_transaction_by_schema_name = {
        _: schema_of_row_in_transaction(schema)
        for _, schema in schema_by_schema_name.items()
    }
    schema_in_transaction_by_schema_name[transaction_result_row_schema.name] = (
        transaction_result_row_schema
    )

    rows_in_transaction_and_messages_by_transaction_id = defaultdict[
        UUID, list[tuple[Row, Message]]
    ](list)

    async for message in log:
        if message.message is None:
            continue

        schema_name = schema_name_of_encoded_row(message.message)

        if schema_name is None:
            raise ValueError

        schema = schema_in_transaction_by_schema_name[schema_name]
        row = decoded_row(schema, message.message)

        if schema != transaction_result_row_schema:
            transaction_id = cast(UUID, row[-2])
            transaction_result = cast(TransactionResult, row[-1])

            if transaction_result is TransactionResult.rollbacked:
                replication_slots = await gather(*replication_slot_pointers)
                replication_slot = min(replication_slots, default=0)

                rows_in_transaction_and_messages = (
                    rows_in_transaction_and_messages_by_transaction_id[
                        transaction_id
                    ]
                )

                message_to_delete = [
                    message
                    for _, message in rows_in_transaction_and_messages
                ]
                message_to_delete.append(message)

                messages_to_delete = [
                    message for message in message_to_delete
                    if message.id <= replication_slot
                ]

                self.


        else:
            transaction_id = cast(UUID, row[-1])

            rows_in_transaction_by_transaction_id[transaction_id].append(
                row_in_transaction
            )


async def _executed_rollback(
    log: InTelegramMessageQueque,
    replication_slot_pointers: Sequence[InTelegramPointer[int]],
    rows_in_transaction_and_messages
) -> None:
    replication_slots = await gather(*replication_slot_pointers)
    replication_slot = min(replication_slots, default=0)


