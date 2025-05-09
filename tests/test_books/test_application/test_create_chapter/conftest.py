from datetime import UTC, datetime

from in_memory_db import InMemoryDb
from in_memory_db.db import InMemoryDbAsyncTransactionOrchestrator
from pytest import fixture

from books.application.create_chapter import CreateChapter
from books.entities.auth.access_token import AccessToken
from books.entities.time.time import Time
from books.infrastructure.adapters.access_token_signing import (
    AccessTokenSigningAsIdentification,
)
from books.infrastructure.adapters.books import InMemoryDbBooks
from books.infrastructure.adapters.clock import StoppedClock
from books.infrastructure.adapters.map import MapToInMemoryDb


@fixture()
def db() -> InMemoryDb:
    return InMemoryDb()


@fixture(scope="session")
def current_time() -> Time:
    return Time(datetime(2006, 1, 1, tzinfo=UTC))


@fixture()
def operation(
    db: InMemoryDb, current_time: Time
) -> CreateChapter[AccessToken | None]:
    orchestrator = InMemoryDbAsyncTransactionOrchestrator(db)

    return CreateChapter(
        access_token_signing=AccessTokenSigningAsIdentification(),
        map=MapToInMemoryDb(db),
        transaction=orchestrator.transaction(),
        clock=StoppedClock(current_time),
        books=InMemoryDbBooks(db),
    )
