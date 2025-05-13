import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass

from telethon.types import Message

from books.infrastructure.telethon.client_pool import TelegramClientPool
from books.infrastructure.telethon.pointer import InTelegramPointer


@dataclass(frozen=True)
class InTelegramMessageQueque:
    pool_to_push: TelegramClientPool
    pool_to_pull: TelegramClientPool
    offset_pointer: InTelegramPointer[int]

    heap_id: int
    offset_message_chat_id: int
    offset_message_id: int
    seconds_to_wait_after_sync: int | float

    async def push(self, text: str, /) -> None:
        await self.pool_to_push().send_message(self.heap_id, text)

    async def __aiter__(self) -> AsyncIterator[Message]:
        offset = await self.offset_pointer

        while True:
            heap_messages_after_offset = self.pool_to_pull().iter_messages(
                self.heap_id, reverse=True, min_id=offset
            )

            async for heap_message in heap_messages_after_offset:
                yield heap_message

                offset = heap_message.id
                await self.offset_pointer.set(offset)

            await asyncio.sleep(self.seconds_to_wait_after_sync)
