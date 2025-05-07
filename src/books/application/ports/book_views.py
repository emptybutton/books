from abc import ABC, abstractmethod

from books.entities.core.book.book import Book
from books.entities.core.book.chapter_number import ChapterNumber


class BookViews[BookViewT, BookChapterViewT](ABC):
    @abstractmethod
    async def book_view(self, book_name: str, /) -> BookViewT: ...

    @abstractmethod
    async def book_chapter_view(
        self,
        book: Book,
        book_chapter_number: ChapterNumber,
        /
    ) -> BookChapterViewT: ...
