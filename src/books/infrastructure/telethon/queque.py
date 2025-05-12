import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import cast

from telethon import TelegramClient
from telethon.types import Message


@dataclass(frozen=True)
class InTelegramQueque:
    tg: TelegramClient
    item_message_chat_id: int
    offset_message_chat_id: int
    offset_message_id: int
    seconds_to_wait_after_sync: int | float

    async def push(self, text: str, /) -> None:
        await self.tg.send_message(self.item_message_chat_id, text)

    async def __aiter__(self) -> AsyncIterator[str]:
        offset_message = cast(Message, await self.tg.get_messages(
            self.offset_message_chat_id, ids=self.offset_message_id
        ))

        try:
            offset = int(offset_message.message)
        except ValueError:
            offset = 0

        item_messages_after_offset = self.tg.iter_messages(
            self.item_message_chat_id, reverse=True, min_id=offset
        )

        while True:
            async for item_messgae in item_messages_after_offset:
                yield item_messgae.message

                offset = item_messgae.id
                await self.tg.edit_message(offset_message, str(offset))

            await asyncio.sleep(self.seconds_to_wait_after_sync)
