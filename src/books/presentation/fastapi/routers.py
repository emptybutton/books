from collections.abc import Iterator

from fastapi import APIRouter

from books.presentation.fastapi.routes.healthcheck import (
    healthcheck_router,
)
from books.presentation.fastapi.routes.sign_in import sign_in_router
from books.presentation.fastapi.routes.sign_out import sign_out_router
from books.presentation.fastapi.routes.sign_up import sign_up_router
from books.presentation.fastapi.routes.view_book_with_name import (
    view_book_with_name_router,
)
from books.presentation.fastapi.routes.view_chapter import view_chapter_router
from books.presentation.fastapi.routes.view_current_user import (
    view_current_user_router,
)
from books.presentation.fastapi.routes.view_user_with_name import (
    view_user_with_name_router,
)


all_routers = (
    healthcheck_router,
    sign_up_router,
    sign_in_router,
    sign_out_router,
    view_current_user_router,
    view_user_with_name_router,
    view_book_with_name_router,
    view_chapter_router,
)


class UnknownRouterError(Exception): ...


def ordered(*routers: APIRouter) -> Iterator[APIRouter]:
    for router in all_routers:
        if router not in routers:
            raise UnknownRouterError

        yield router
