from dishka import Provider, Scope, make_async_container, provide

from books.main.common.di import CommonProvider
from books.presentation.fastapi.app import (
    FastAPIAppCoroutines,
    FastAPIAppRouters,
)
from books.presentation.fastapi.routers import all_routers


class FastAPIProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> FastAPIAppRouters:
        return all_routers

    @provide
    def provide_coroutines(self) -> FastAPIAppCoroutines:
        return []


container = make_async_container(FastAPIProvider(), CommonProvider())
