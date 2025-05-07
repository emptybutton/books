from dataclasses import dataclass

from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.books import Books
from books.application.ports.clock import Clock
from books.application.ports.map import Map
from books.application.ports.transaction import Transaction
from books.entities.core.book.book import book_without_deleted_chapter
from books.entities.core.book.chapter_number import ChapterNumber


@dataclass(frozen=True)
class DeleteChapter[SignedAccessTokenT]:
    access_token_signing: AccessTokenSigning[SignedAccessTokenT]
    map: Map
    transaction: Transaction
    clock: Clock
    books: Books

    async def __call__(
        self,
        signed_access_token: SignedAccessTokenT,
        book_name: str,
        chapter_number_int: int,
    ) -> None:
        """
        :raises books.entities.core.book.chapter_number.NegativeOrZeroChapterNumberError:
        :raises books.entities.auth.access_token.AuthenticationError:
        :raises books.entities.core.book.book.NoBookError:
        :raises books.entities.core.book.book.NotAuthorError:
        :raises books.application.ports.map.NotUniqueBookNameError:
        """  # noqa: E501

        current_time = await self.clock.get_current_time()
        chapter_number = ChapterNumber(chapter_number_int)

        access_token = await self.access_token_signing.access_token(
            signed_access_token
        )

        async with self.transaction:
            book = await self.books.book_with_name(book_name)

            book_without_deleted_chapter_ = book_without_deleted_chapter(
                book, access_token, chapter_number, current_time
            )

            await self.map(book_without_deleted_chapter_)
