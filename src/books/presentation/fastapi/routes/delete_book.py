from contextlib import suppress
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from fastapi.responses import Response

from books.application.delete_book import DeleteBook
from books.entities.core.book.book import NoBookError
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.schemas.output import (
    FailedAuthenticationSchema,
    NotAuthorSchema,
)
from books.presentation.fastapi.tags import Tag


delete_book_router = APIRouter()


@delete_book_router.delete(
    "/books",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": FailedAuthenticationSchema},
        status.HTTP_403_FORBIDDEN: {"model": NotAuthorSchema},
    },
    summary="Delete book",
    description=(
        "Delete book."
        " If a book has already been deleted,"
        " the response body will be empty."
        " Available if a current user is a book author."
    ),
    tags=[Tag.book],
)
@inject
async def delete_book_route(
    delete_book: FromDishka[DeleteBook[str]],
    book_name: Annotated[str, Query(alias="name")],
    signed_access_token: AccessTokenCookie.StrOrNoneWithLock,
) -> Response:
    with suppress(NoBookError):
        await delete_book(signed_access_token, book_name)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
