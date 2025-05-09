from dataclasses import dataclass

from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.books import Books
from books.application.ports.clock import Clock
from books.application.ports.map import Map
from books.application.ports.transaction import Transaction
from books.entities.core.book.book import book_with_edited_chapter
from books.entities.core.book.chapter_number import ChapterNumber


@dataclass(frozen=True)
class EditChapter[SignedAccessTokenT]:
    access_token_signing: AccessTokenSigning[SignedAccessTokenT]
    map: Map
    transaction: Transaction
    clock: Clock
    books: Books

    async def __call__(
        self,
        signed_access_token: SignedAccessTokenT | None,
        book_name: str,
        chapter_number_int: int,
        new_chapter_text: str,
    ) -> None:
        """
        :raises books.entities.core.book.chapter_number.NegativeOrZeroChapterNumberError:
        :raises books.entities.auth.access_token.AuthenticationError:
        :raises books.entities.core.book.book.NoBookError:
        :raises books.entities.core.book.book.NotAuthorError:
        :raises books.entities.core.book.chapter.NoChapterError:
        """  # noqa: E501

        current_time = await self.clock.get_current_time()
        acess_token = await self.access_token_signing.access_token(
            signed_access_token
        )
        chapter_number = ChapterNumber(chapter_number_int)

        async with self.transaction:
            book = await self.books.book_with_name(book_name)

            book_with_edited_chapter_ = book_with_edited_chapter(
                book,
                acess_token,
                chapter_number,
                new_chapter_text,
                current_time,
            )

            await self.map(book_with_edited_chapter_)
