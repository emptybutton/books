from dishka import Provider, Scope, make_async_container, provide

from books.main.common.di import CommonProvider
from books.presentation.fastapi.app import FastAPIAppRouters
from books.presentation.fastapi.routers import all_routers


class FastAPIProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> FastAPIAppRouters:
        return all_routers


container = make_async_container(FastAPIProvider(), CommonProvider())
