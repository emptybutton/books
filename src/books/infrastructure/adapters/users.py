from dataclasses import dataclass
from uuid import UUID

from in_memory_db import InMemoryDb

from books.application.ports.users import Users
from books.entities.core.user import User


@dataclass(kw_only=True, slots=True)
class InMemoryUsers(Users, InMemoryDb[User]):
    async def user_with_id(self, id: UUID) -> User | None:
        return self.select_one(lambda user: user.id == id)
