from dataclasses import dataclass
from uuid import UUID

from in_memory_db import InMemoryDb

from books.application.ports.user_views import UserViews
from books.entities.auth.user import User
from books.presentation.fastapi.schemas.output import UserSchema


@dataclass(frozen=True)
class UsersFromInMemoryDbAsUserViews(UserViews[User | None]):
    db: InMemoryDb

    async def view_of_user_with_id(self, id: UUID | None) -> User | None:
        return self.db.subset(User).select_one(lambda it: it.id == id)

    async def view_of_user_with_name(self, name: str) -> User | None:
        return self.db.subset(User).select_one(lambda it: it.name == name)


@dataclass(frozen=True)
class UserSchemasFromInMemoryDbAsUserViews(UserViews[UserSchema | None]):
    db: InMemoryDb

    async def view_of_user_with_id(self, id: UUID | None) -> UserSchema | None:
        user = self.db.subset(User).select_one(lambda it: it.id == id)

        if user is None:
            return None

        return self._user_schema(user)

    async def view_of_user_with_name(self, name: str) -> UserSchema | None:
        user = self.db.subset(User).select_one(lambda it: it.name == name)

        if user is None:
            return None

        return self._user_schema(user)

    def _user_schema(self, user: User) -> UserSchema:
        return UserSchema(name=user.name)
