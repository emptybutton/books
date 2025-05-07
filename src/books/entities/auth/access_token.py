from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from books.entities.time.time import Time


@dataclass(frozen=True)
class AccessToken:
    user_id: UUID
    expriration_time: Time


def is_access_token_expired(
    access_token: AccessToken, current_time: Time
) -> bool:
    return current_time.datetime >= access_token.expriration_time.datetime


def issued_access_token(user_id: UUID, current_time: Time) -> AccessToken:
    return AccessToken(
        user_id,
        current_time.map(lambda it: it + timedelta(days=365)),
    )


def invalid_access_token(
    access_token: AccessToken, current_time: Time
) -> AccessToken:
    return AccessToken(access_token.user_id, current_time)


class AuthenticationError(Exception): ...


def authenticating_access_token(
    access_token: AccessToken | None, current_time: Time
) -> AccessToken:
    """
    :raises books.entities.auth.access_token.AuthenticationError:
    """

    if (
        access_token is None
        or is_access_token_expired(access_token, current_time)
    ):
        raise AuthenticationError

    return access_token
