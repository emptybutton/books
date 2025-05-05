from abc import ABC, abstractmethod

from books.entities.core.book.chapter_number import ChapterNumber


class BookViews[BookSimpleViewT, BookChapterViewT](ABC):
    @abstractmethod
    async def book_simple_view(self, book_name: str, /) -> BookSimpleViewT: ...

    @abstractmethod
    async def book_detailed_view(self, book_name: str, /) -> BookSimpleViewT:
        ...

    @abstractmethod
    async def book_chapter_view(
        self,
        book_name: str,
        book_chapter_number: ChapterNumber,
        book_chapter_text_version_number: int,
        /
    ) -> BookChapterViewT: ...
