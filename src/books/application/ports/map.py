from abc import ABC, abstractmethod

from effect import LifeCycle

from books.entities.auth.user import UserIdentifiedEntity
from books.entities.core.book.book import BookIdentifiedEntity


type MappableEntityLifeCycle = LifeCycle[
    BookIdentifiedEntity | UserIdentifiedEntity
]


class NotUniqueUserNameError(Exception): ...


class NotUniqueBookNameError(Exception): ...


class Map(ABC):
    @abstractmethod
    async def __call__(
        self,
        effect: MappableEntityLifeCycle,
        /,
    ) -> None:
        """
        :raises books.application.ports.map.NotUniqueUserNameError:
        :raises books.application.ports.map.NotUniqueBookNameError:
        """
