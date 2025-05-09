from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import jwt as pyjwt

from books.application.ports.access_token_signing import AccessTokenSigning
from books.entities.auth.access_token import AccessToken
from books.entities.time.time import Time
from books.infrastructure.alias import JWT


@dataclass(frozen=True)
class AccessTokenSigningAsIdentification(
    AccessTokenSigning[AccessToken | None]
):
    async def signed_access_token(
        self, access_token: AccessToken
    ) -> AccessToken:
        return access_token

    async def access_token(
        self, access_token: AccessToken | None
    ) -> AccessToken | None:
        return access_token


@dataclass(frozen=True)
class AccessTokenSigningToHS256JWT(AccessTokenSigning[JWT]):
    secret: str = field(repr=False)

    async def signed_access_token(self, access_token: AccessToken) -> JWT:
        return pyjwt.encode(
            algorithm="HS256",
            headers={"exp": access_token.expriration_time.datetime.timestamp()},
            payload={"id": access_token.user_id.hex},
            key=self.secret,
        )

    async def access_token(self, jwt: JWT) -> AccessToken | None:
        try:
            jwt_data: dict[str, Any]
            jwt_data = pyjwt.decode_complete(
                jwt, self.secret, algorithms="HS256"
            )
        except pyjwt.DecodeError:
            return None

        headers = jwt_data["header"]
        payload = jwt_data["payload"]

        user_id_hex: str | None = payload.get("id")
        expiration_timestamp: int | float = headers.get("exp")

        if user_id_hex is None or expiration_timestamp is None:
            return None

        try:
            user_id = UUID(hex=user_id_hex)
        except ValueError:
            return None

        try:
            expiration_datetime = datetime.fromtimestamp(
                expiration_timestamp, UTC
            )
        except OverflowError:
            return None

        expiration_time = Time(expiration_datetime)

        return AccessToken(user_id, expiration_time)
