from contextlib import suppress
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from fastapi.responses import Response
from pydantic import PositiveInt

from books.application.delete_chapter import DeleteChapter
from books.entities.core.book.chapter import NoChapterError
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.schemas.output import (
    FailedAuthenticationSchema,
    NoBookSchema,
    NotAuthorSchema,
)
from books.presentation.fastapi.tags import Tag


delete_chapter_router = APIRouter()


@delete_chapter_router.delete(
    "/chapters",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": FailedAuthenticationSchema},
        status.HTTP_403_FORBIDDEN: {"model": NotAuthorSchema},
        status.HTTP_404_NOT_FOUND: {"model": NoBookSchema},
    },
    summary="Delete chapter",
    description=(
        "Delete book chapter."
        " If a chapter has already been deleted,"
        " the response body will be empty."
        " Available if a current user is a book author."
    ),
    tags=[Tag.chapter],
)
@inject
async def delete_chapter_route(
    delete_chapter: FromDishka[DeleteChapter[str]],
    book_name: Annotated[str, Query(alias="bookName")],
    chapter_number_int: Annotated[PositiveInt, Query(alias="chapterNumber")],
    signed_access_token: AccessTokenCookie.StrOrNoneWithLock = None,
) -> Response:
    with suppress(NoChapterError):
        await delete_chapter(signed_access_token, book_name, chapter_number_int)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
