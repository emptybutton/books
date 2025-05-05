from dataclasses import dataclass
from uuid import UUID

from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.clock import Clock
from books.application.ports.transaction import Transaction
from books.application.ports.user_views import UserViews
from books.entities.auth.access_token import valid_access_token
from books.entities.time.time import Time


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
        :raises books.entities.auth.access_token.ExpiredAccessTokenError:
        """

        current_time = await self.clock.get_current_time()
        user_id = await self._user_id(signed_access_token, current_time)

        async with self.transaction:
            return await self.user_views.view_of_user_with_id(user_id)

    async def _user_id(
        self,
        signed_access_token: SignedAccessTokenT | None,
        current_time: Time
    ) -> UUID | None:
        if signed_access_token is None:
            return None

        access_token = await self.access_token_signing.access_token(
            signed_access_token,
        )

        if access_token is None:
            return None

        return valid_access_token(access_token, current_time).user_id
