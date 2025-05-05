from abc import ABC, abstractmethod

from books.entities.core.book.book import Book


class Books(ABC):
    @abstractmethod
    async def book_with_name(self, name: str, /) -> Book | None: ...
