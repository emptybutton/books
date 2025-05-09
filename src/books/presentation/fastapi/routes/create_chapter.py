from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from fastapi.responses import Response
from pydantic import BaseModel, PositiveInt

from books.application.create_chapter import CreateChapter
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.schemas.output import (
    FailedAuthenticationSchema,
    NoBookSchema,
    NotAuthorSchema,
    NotUniqueChapterNumberSchema,
)
from books.presentation.fastapi.tags import Tag


create_chapter_router = APIRouter()


class CreateChapterSchema(BaseModel):
    text: str
    number: PositiveInt


@create_chapter_router.post(
    "/chapters",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"content": None},
        status.HTTP_401_UNAUTHORIZED: {"model": FailedAuthenticationSchema},
        status.HTTP_403_FORBIDDEN: {"model": NotAuthorSchema},
        status.HTTP_404_NOT_FOUND: {"model": NoBookSchema},
        status.HTTP_409_CONFLICT: {"model": NotUniqueChapterNumberSchema},
    },
    summary="Create book chapter",
    description="Create a chapter for any book authored by a current user.",
    tags=[Tag.chapter],
)
@inject
async def create_chapter_route(
    create_chapter: FromDishka[CreateChapter[str]],
    book_name: Annotated[str, Query(alias="bookName")],
    request_body: CreateChapterSchema,
    signed_access_token: AccessTokenCookie.StrOrNoneWithLock = None,
) -> Response:
    await create_chapter(
        signed_access_token,
        book_name,
        request_body.number,
        request_body.text,
    )

    return Response(status_code=status.HTTP_201_CREATED)
