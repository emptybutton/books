from abc import ABC, abstractmethod

from books.entities.auth.user import User


class Users(ABC):
    @abstractmethod
    async def user_with_name(self, name: str, /) -> User | None: ...
