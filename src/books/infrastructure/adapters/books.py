from dataclasses import dataclass

from in_memory_db import InMemoryDb

from books.application.ports.books import Books
from books.entities.core.book.book import Book
from books.infrastructure.book_loading import loaded_book_from_in_memory_db


@dataclass(frozen=True)
class InMemoryDbBooks(Books):
    db: InMemoryDb

    async def book_with_name(self, name: str, /) -> Book | None:
        book = self.db.subset(Book).select_one(lambda it: it.name == name)

        return None if book is None else loaded_book_from_in_memory_db(
            self.db, book
        )
