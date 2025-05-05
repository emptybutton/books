from abc import ABC, abstractmethod
from uuid import UUID


class UserViews[UserViewT](ABC):
    @abstractmethod
    async def view_of_user_with_id(self, id: UUID | None, /) -> UserViewT: ...

    @abstractmethod
    async def view_of_user_with_name(self, name: str, /) -> UserViewT: ...
