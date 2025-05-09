from datetime import UTC, datetime
from typing import Annotated, Any, ClassVar

from fastapi import Cookie as FastAPICookie
from fastapi import Depends, Response
from fastapi.security import APIKeyCookie


class CookieAnnotationKeeperType(type):
    type StrOrNoneWithLock = str | None
    type StrWithLock = str
    type StrOrNone = str | None
    type Str = str

    key: str

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        *,
        scheme_name: str,
        description: str,
        key: str,
    ) -> "CookieAnnotationKeeperType":
        type_ = super().__new__(cls, name, bases, namespace)

        api_key_with_auto_error = APIKeyCookie(
            name=key,
            scheme_name=scheme_name,
            description=description,
            auto_error=True,
        )
        api_key_without_auto_error = APIKeyCookie(
            name=key,
            scheme_name=scheme_name,
            description=description,
            auto_error=False,
        )

        type_.StrOrNoneWithLock = Annotated[
            str | None, Depends(api_key_without_auto_error)
        ]  # type: ignore[assignment]
        type_.StrWithLock = Annotated[str, Depends(api_key_with_auto_error)]  # type: ignore[assignment]

        type_.StrOrNone = Annotated[str | None, FastAPICookie(alias=key)]  # type: ignore[assignment]
        type_.Str = Annotated[str, FastAPICookie(alias=key)]  # type: ignore[assignment]

        type_.key = key

        return type_


class AccessTokenCookie(
    metaclass=CookieAnnotationKeeperType,
    key="accessToken",
    scheme_name="Access token cookie",
    description=(
        "Required for various commands."
        " Obtained after signing in or signing up."
    ),
):
    type StrOrNoneWithLock = str | None
    type StrWithLock = str
    type StrOrNone = str | None
    type Str = str

    key: ClassVar[str]

    def __init__(self, response: Response) -> None:
        self.response = response

    def set(self, token: str, expiration_datetime: datetime) -> None:
        age_timedelta = expiration_datetime - datetime.now(UTC)

        self.response.set_cookie(
            self.key,
            token,
            httponly=True,
            max_age=int(age_timedelta.total_seconds()),
        )

    def clear(self) -> None:
        self.response.delete_cookie(self.key)
