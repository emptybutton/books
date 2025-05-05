from collections import Counter
from dataclasses import dataclass

from effect import IdentifiedValue
from in_memory_db import InMemoryDb

from books.application.ports.map import (
    Map,
    MappableEntityLifeCycle,
    NotUniqueBookNameError,
    NotUniqueUserNameError,
)
from books.entities.auth.user import User
from books.entities.core.book.book import Book


@dataclass(frozen=True)
class MapToInMemoryDb(Map):
    in_memory_db: InMemoryDb

    async def __call__(
        self,
        effect: MappableEntityLifeCycle,
    ) -> None:
        """
        :raises books.application.ports.map.NotUniqueUserNameError:
        :raises books.application.ports.map.NotUniqueBookNameError:
        """

        self.in_memory_db.extend(effect.new_values)
        self.in_memory_db.extend(effect.translated_values)

        self.in_memory_db.subset(IdentifiedValue).remove_selected(
            lambda it: it.is_in(effect.mutated_values)
        )
        self.in_memory_db.extend(effect.mutated_values)

        self.in_memory_db.subset(IdentifiedValue).remove_selected(
            lambda it: it.is_in(effect.dead_values)
        )

        self._validate_uniqueness()

    def _validate_uniqueness(self) -> None:
        self._validate_user_name_uniqueness()
        self._validate_book_name_uniqueness()

    def _validate_user_name_uniqueness(self) -> None:
        user_name_counter = Counter(
            user.name for user in self.in_memory_db.subset(User)
        )

        if max(user_name_counter.values()) > 1:
            raise NotUniqueUserNameError

    def _validate_book_name_uniqueness(self) -> None:
        book_name_counter = Counter(
            book.name for book in self.in_memory_db.subset(Book)
        )

        if max(book_name_counter.values()) > 1:
            raise NotUniqueBookNameError
