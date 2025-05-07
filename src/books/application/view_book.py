from dataclasses import dataclass

from books.application.ports.book_views import BookViews
from books.application.ports.transaction import Transaction


@dataclass(frozen=True)
class ViewBook[BookViewT, BookChapterViewT]:
    book_views: BookViews[BookViewT, BookChapterViewT]
    transaction: Transaction

    async def __call__(self, book_name: str) -> BookViewT:
        async with self.transaction:
            return await self.book_views.book_view(book_name)
