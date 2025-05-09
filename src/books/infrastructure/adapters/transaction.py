from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from typing import Any

from in_memory_db import InMemoryDb


@asynccontextmanager
async def in_memory_db_transaction(
    dbs: Sequence[InMemoryDb[Any]],
) -> AsyncIterator[None]:
    for db in dbs:
        db.begin()

    try:
        yield
    except Exception as error:
        for db in dbs:
            db.rollback()
        raise error from error
    else:
        for db in dbs:
            db.commit()
