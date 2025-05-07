from dataclasses import dataclass

from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.clock import Clock
from books.application.ports.transaction import Transaction
from books.application.ports.user_views import UserViews
from books.entities.auth.access_token import authenticating_access_token


@dataclass(frozen=True)
class ViewCurrentUser[SignedAccessTokenT, UserViewT]:
    clock: Clock
    access_token_signing: AccessTokenSigning[SignedAccessTokenT]
    user_views: UserViews[UserViewT]
    transaction: Transaction

    async def __call__(
        self, signed_access_token: SignedAccessTokenT | None
    ) -> UserViewT:
        """
        :raises books.entities.auth.access_token.AuthenticationError:
        """

        current_time = await self.clock.get_current_time()

        if signed_access_token is None:
            user_id = None
        else:
            access_token = await self.access_token_signing.access_token(
                signed_access_token
            )
            access_token = authenticating_access_token(
                access_token, current_time
            )
            user_id = access_token.user_id

        async with self.transaction:
            return await self.user_views.view_of_user_with_id(user_id)
