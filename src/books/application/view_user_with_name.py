from dataclasses import dataclass

from books.application.ports.transaction import Transaction
from books.application.ports.user_views import UserViews


@dataclass(frozen=True)
class ViewUserWithName[SignedAccessTokenT, UserViewT]:
    user_views: UserViews[UserViewT]
    transaction: Transaction

    async def __call__(self, user_name: str) -> UserViewT:
        async with self.transaction:
            return await self.user_views.view_of_user_with_name(user_name)
