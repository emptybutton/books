from collections.abc import Generator
from dataclasses import dataclass

from telethon.types import Message

from books.infrastructure.telethon.client_pool import TelegramClientPool
from books.infrastructure.telethon.primitive import (
    Primitive,
    decoded_primitive,
    encoded_primitive,
)


@dataclass(frozen=True)
class InTelegramPointer[PrimitiveT: Primitive]:
    pool_to_insert: TelegramClientPool
    pool_to_select: TelegramClientPool
    pool_to_delete: TelegramClientPool
    pointer_chat_id: int
    primitive_type: type[PrimitiveT]

    async def set(self, primitive: PrimitiveT) -> None:
        await self.pool_to_insert().send_message(
            self.pointer_chat_id,
            encoded_primitive(primitive),
        )

    def __await__(self) -> Generator[None, None, PrimitiveT]:
        return self.get().__await__()

    async def get(self) -> PrimitiveT:
        pointer_message = await self._pointer_message()

        return decoded_primitive(pointer_message.message, self.primitive_type)

    async def refresh(self) -> None:
        pointer_message = await self._pointer_message()
        ids_to_delete = list(range(pointer_message.id))
        client = self.pool_to_delete()

        await client.delete_message(self.pointer_chat_id, ids_to_delete)

    async def _pointer_message(self) -> Message:
        pointer_messages = await self.pool_to_select().get_messages(
            self.pointer_chat_id, limit=1
        )

        return pointer_messages[0]
