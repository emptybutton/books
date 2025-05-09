from dataclasses import dataclass

from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.books import Books
from books.application.ports.clock import Clock
from books.application.ports.map import Map
from books.application.ports.transaction import Transaction
from books.entities.core.book.book import deleted_book


@dataclass(frozen=True)
class DeleteBook[SignedAccessTokenT]:
    access_token_signing: AccessTokenSigning[SignedAccessTokenT]
    map: Map
    transaction: Transaction
    clock: Clock
    books: Books

    async def __call__(
        self,
        signed_access_token: SignedAccessTokenT | None,
        book_name: str,
    ) -> None:
        """
        :raises books.entities.auth.access_token.AuthenticationError:
        :raises books.entities.core.book.book.NoBookError:
        :raises books.entities.core.book.book.NotAuthorError:
        """

        current_time = await self.clock.get_current_time()
        acess_token = await self.access_token_signing.access_token(
            signed_access_token
        )

        async with self.transaction:
            book = await self.books.book_with_name(book_name)

            deleted_book_ = deleted_book(book, acess_token, current_time)

            await self.map(deleted_book_)
