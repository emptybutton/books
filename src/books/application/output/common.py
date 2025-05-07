from dataclasses import dataclass

from books.entities.time.time import Time


@dataclass(frozen=True)
class AccessTokenData[SignedAccessTokenT]:
    signed_access_token: SignedAccessTokenT
    signed_access_token_expiration_time: Time
