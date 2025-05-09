from dataclasses import dataclass

from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.clock import Clock
from books.application.ports.map import Map
from books.application.ports.transaction import Transaction
from books.entities.core.book.book import new_book


@dataclass(frozen=True)
class CreateBook[SignedAccessTokenT]:
    access_token_signing: AccessTokenSigning[SignedAccessTokenT]
    map: Map
    transaction: Transaction
    clock: Clock

    async def __call__(
        self,
        signed_access_token: SignedAccessTokenT | None,
        book_name: str,
    ) -> None:
        """
        :raises books.entities.auth.access_token.AuthenticationError:
        :raises books.application.ports.map.NotUniqueBookNameError:
        """

        new_book_ = new_book(
            await self.access_token_signing.access_token(signed_access_token),
            book_name,
            await self.clock.get_current_time()
        )

        async with self.transaction:
            await self.map(new_book_)
