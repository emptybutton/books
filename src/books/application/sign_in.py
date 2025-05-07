from dataclasses import dataclass

from books.application.output.common import AccessTokenData
from books.application.ports.access_token_signing import AccessTokenSigning
from books.application.ports.clock import Clock
from books.application.ports.map import Map
from books.application.ports.transaction import Transaction
from books.application.ports.users import Users
from books.entities.auth.password import Password, PasswordHashes
from books.entities.auth.user import InvalidPasswordError, signed_in_user


class FailedSigningInError(Exception): ...


@dataclass(frozen=True)
class SignIn[SignedAccessTokenT]:
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
    ) -> AccessTokenData[SignedAccessTokenT]:
        """
        :raises books.application.sign_in.FailedSigningInError:
        """

        current_time = await self.clock.get_current_time()

        async with self.transaction:
            user = await self.users.user_with_name(user_name)

            if user is None:
                raise FailedSigningInError

            try:
                signed_in_user_ = signed_in_user(
                    user, Password(password), current_time, self.password_hashes
                )
            except InvalidPasswordError as error:
                raise FailedSigningInError from error

        access_token = signed_in_user_.access_token
        signed_access_token = await (
            self.access_token_signing.signed_access_token(access_token)
        )
        return AccessTokenData(
            signed_access_token, access_token.expriration_time
        )
