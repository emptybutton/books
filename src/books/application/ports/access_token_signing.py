from abc import ABC, abstractmethod

from books.entities.auth.access_token import AccessToken


class AccessTokenSigning[SignedAccessTokenT](ABC):
    @abstractmethod
    async def signed_access_token(
        self, access_token: AccessToken, /
    ) -> SignedAccessTokenT: ...

    @abstractmethod
    async def access_token(
        self, signed_access_token: SignedAccessTokenT, /
    ) -> AccessToken | None: ...
