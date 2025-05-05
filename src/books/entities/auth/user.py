from dataclasses import dataclass
from uuid import UUID, uuid4

from effect import Effect, IdentifiedValue, just, new

from books.entities.auth.access_token import (
    AccessToken,
    invalid_access_token,
    issued_access_token,
)
from books.entities.auth.password import Password, PasswordHashes
from books.entities.time.time import Time


class InvalidPasswordError(Exception): ...


@dataclass(frozen=True)
class User(IdentifiedValue[UUID]):
    name: str
    password_hash: str


type UserIdentifiedEntity = User


@dataclass(frozen=True)
class PrimaryAuthenticatedUser:
    user: User
    access_token: AccessToken


def primary_authenticated_user(
    user: User, current_time: Time
) -> PrimaryAuthenticatedUser:
    issued_access_token_ = issued_access_token(user.id, current_time)

    return PrimaryAuthenticatedUser(user, issued_access_token_)


def signed_up_user(
    user_name: str,
    password: Password,
    current_time: Time,
    password_hashes: PasswordHashes,
) -> Effect[PrimaryAuthenticatedUser, User]:
    password_hash = password_hashes.hash(password)
    user = new(User(id=uuid4(), name=user_name, password_hash=password_hash))

    return user & Effect(primary_authenticated_user(just(user), current_time))


def signed_in_user(
    user: User,
    password: Password,
    current_time: Time,
    password_hashes: PasswordHashes,
) -> PrimaryAuthenticatedUser:
    """
    :raises books.entities.auth.user.InvalidPasswordError:
    """

    if not password_hashes.is_hash_valid(user.password_hash, password):
        raise InvalidPasswordError

    return primary_authenticated_user(user, current_time)


@dataclass(frozen=True)
class SignedOutUser:
    access_token: AccessToken


def signed_out_user(
    access_token: AccessToken, current_time: Time
) -> SignedOutUser:
    access_token = invalid_access_token(access_token, current_time)

    return SignedOutUser(access_token)
