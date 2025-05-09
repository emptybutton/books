from fastapi import FastAPI
from httpx import AsyncClient
from httpx_ws.transport import ASGIWebSocketTransport
from pytest import fixture

from books.main.fastapi.di import container
from books.presentation.fastapi.app import app_from


@fixture
async def app() -> FastAPI:
    return await app_from(container)


@fixture
def client(app: FastAPI) -> AsyncClient:
    transport = ASGIWebSocketTransport(app=app)

    return AsyncClient(transport=transport, base_url="http://localhost")
