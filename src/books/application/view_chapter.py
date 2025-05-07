from dataclasses import dataclass

from effect import just

from books.application.ports.book_views import BookViews
from books.application.ports.books import Books
from books.application.ports.map import Map
from books.application.ports.transaction import Transaction
from books.entities.core.book.book import book_with_viewed_chapter
from books.entities.core.book.chapter_number import ChapterNumber


@dataclass(frozen=True)
class ViewChapter[BookViewT, BookChapterViewT]:
    transaction: Transaction
    books: Books
    book_views: BookViews[BookViewT, BookChapterViewT]
    map: Map

    async def __call__(
        self, book_name: str, chapter_number_int: int
    ) -> BookChapterViewT:
        """
        :raises books.entities.core.book.chapter_number.NegativeOrZeroChapterNumberError:
        :raises books.entities.core.book.book.NoBookError:
        :raises books.entities.core.book.chapter.NoChapterError:
        """  # noqa: E501

        chapter_number = ChapterNumber(chapter_number_int)

        async with self.transaction:
            book = await self.books.book_with_name(book_name)

            book_with_viewed_chapter_ = (
                book_with_viewed_chapter(book, chapter_number)
            )

            await self.map(book_with_viewed_chapter_)

            return await self.book_views.book_chapter_view(
                just(book_with_viewed_chapter_), chapter_number
            )
