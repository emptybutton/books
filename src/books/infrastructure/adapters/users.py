from dataclasses import dataclass

from in_memory_db import InMemoryDb

from books.application.ports.users import Users
from books.entities.auth.user import User


@dataclass(frozen=True)
class InMemoryUsers(Users):
    db: InMemoryDb

    async def user_with_name(self, name: str) -> User | None:
        return self.db.subset(User).select_one(lambda user: user.name == name)
