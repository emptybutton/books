from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from books.application.ports.users import Users
from books.entities.core.user import User
from books.infrastructure.in_memory_storage import (
    TransactionalInMemoryStorage,
)
from books.infrastructure.sqlalchemy import orm  # noqa: F401


@dataclass(kw_only=True, slots=True)
class InMemoryUsers(Users, TransactionalInMemoryStorage[User]):
    async def user_with_id(self, id: UUID) -> User | None:
        return self.select_one(lambda user: user.id == id)


@dataclass(kw_only=True, frozen=True, slots=True)
class InPostgresUsers(Users):
    session: AsyncSession

    async def user_with_id(self, id: UUID) -> User | None:
        return await self.session.get(User, id)
