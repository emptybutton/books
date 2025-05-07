from dataclasses import dataclass

from books.application.output.common import AccessTokenData
from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.clock import Clock
from books.entities.auth.user import signed_out_user


type Output[SignedAccessTokenT] = AccessTokenData[SignedAccessTokenT] | None


@dataclass(frozen=True)
class SignOut[SignedAccessTokenT]:
    clock: Clock
    access_token_signing: AccessTokenSigning[SignedAccessTokenT]

    async def __call__(
        self, signed_access_token: SignedAccessTokenT
    ) -> Output[SignedAccessTokenT]:
        if signed_access_token is None:
            return None

        access_token = await self.access_token_signing.access_token(
            signed_access_token
        )

        if access_token is None:
            return None

        current_time = await self.clock.get_current_time()
        signed_out_user_ = signed_out_user(access_token, current_time)

        access_token = signed_out_user_.access_token
        return AccessTokenData(
            await self.access_token_signing.signed_access_token(access_token),
            access_token.expriration_time,
        )
