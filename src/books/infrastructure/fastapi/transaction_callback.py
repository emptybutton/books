from asyncio import gather
from contextlib import suppress
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from books.infrastructure.telethon.transaction import AsyncTransactionResults


transaction_result_callback_router = APIRouter()


@transaction_result_callback_router.websocket(
    "/transaction-results/{transaction_id}"
)
@inject
async def view_transaction_results(
    websocket: WebSocket,
    async_transaction_results: FromDishka[AsyncTransactionResults],
    transaction_id: UUID,
) -> None:
    _, transaction_result = gather(
        websocket.accept(),
        async_transaction_results[transaction_id]
    )

    encoded_transaction_result = transaction_result.model_dump_json(
        by_alias=True
    )

    with suppress(WebSocketDisconnect):
        await websocket.send_text(encoded_transaction_result)
