from dataclasses import dataclass
from uuid import UUID

from in_memory_db import InMemoryDb

from books.application.ports.user_views import UserViews
from books.entities.auth.user import User
from books.entities.core.book.book import Book
from books.presentation.fastapi.schemas.output import (
    SimpleBookSchema,
    UserSchema,
)


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
        books = self.db.subset(Book).select_many(
            lambda it: it.author_id == user.id
        )
        book_names = tuple(SimpleBookSchema(name=book.name) for book in books)

        return UserSchema(name=user.name, writtenBooks=book_names)
