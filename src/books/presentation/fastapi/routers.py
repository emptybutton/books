from collections.abc import Iterator

from fastapi import APIRouter

from books.presentation.fastapi.routes.create_book import create_book_router
from books.presentation.fastapi.routes.create_chapter import (
    create_chapter_router,
)
from books.presentation.fastapi.routes.delete_book import delete_book_router
from books.presentation.fastapi.routes.delete_chapter import (
    delete_chapter_router,
)
from books.presentation.fastapi.routes.edit_chapter import edit_chapter_router
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


_book_routers = (
    create_book_router,
    delete_book_router,
    view_book_with_name_router,
)

_chapter_routers = (
    create_chapter_router,
    edit_chapter_router,
    delete_chapter_router,
    view_chapter_router,
)

_current_user_routers = (
    sign_up_router,
    sign_in_router,
    sign_out_router,
    view_current_user_router,
)

_other_user_routers = (
    view_user_with_name_router,
)

_monitoring_routers = (
    healthcheck_router,
)


all_routers = (
    *_book_routers,
    *_chapter_routers,
    *_current_user_routers,
    *_other_user_routers,
    *_monitoring_routers,
)


class UnknownRouterError(Exception): ...


def ordered(*routers: APIRouter) -> Iterator[APIRouter]:
    for router in all_routers:
        if router not in routers:
            raise UnknownRouterError

        yield router
