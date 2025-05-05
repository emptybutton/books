from dataclasses import dataclass

from effect import just

from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.clock import Clock
from books.application.ports.map import Map
from books.application.ports.transaction import Transaction
from books.application.ports.users import Users
from books.entities.auth.password import Password, PasswordHashes
from books.entities.auth.user import signed_up_user
from books.entities.time.time import Time


@dataclass(frozen=True)
class Output[SignedAccessTokenT]:
    signed_access_token: SignedAccessTokenT
    signed_access_token_expiration_time: Time


@dataclass(frozen=True)
class SignUp[SignedAccessTokenT]:
    access_token_signing: AccessTokenSigning[SignedAccessTokenT]
    users: Users
    map: Map
    transaction: Transaction
    clock: Clock
    password_hashes: PasswordHashes

    async def __call__(
        self,
        user_name: str,
        password: str,
    ) -> Output[SignedAccessTokenT]:
        """
        :raises books.application.ports.map.NotUniqueUserNameError:
        """

        current_time = await self.clock.get_current_time()

        signed_up_user_ = signed_up_user(
            user_name,
            Password(password),
            current_time,
            self.password_hashes,
        )

        async with self.transaction:
            await self.map(signed_up_user_)

        access_token = just(signed_up_user_).access_token
        signed_access_token = await (
            self.access_token_signing.signed_access_token(access_token)
        )
        return Output(signed_access_token, access_token.expriration_time)
