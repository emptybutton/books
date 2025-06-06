from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from fastapi.responses import Response
from pydantic import BaseModel, Field, PositiveInt

from books.application.edit_chapter import EditChapter
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.schemas.output import (
    FailedAuthenticationSchema,
    NoBookSchema,
    NoChapterSchema,
    NotAuthorSchema,
)
from books.presentation.fastapi.tags import Tag


edit_chapter_router = APIRouter()


class EditChapterSchema(BaseModel):
    new_text: str = Field(alias="newText")


@edit_chapter_router.post(
    "/chapters/versions",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_404_NOT_FOUND: {"model": NoBookSchema | NoChapterSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": FailedAuthenticationSchema},
        status.HTTP_403_FORBIDDEN: {"model": NotAuthorSchema},
    },
    summary="Edit chapter",
    description=(
        "Edit book chapter."
        " Creates a new and most up-to-date version of a chapter."
        " Available if a current user is a book author."
    ),
    tags=[Tag.chapter],
)
@inject
async def edit_chapter_route(
    edit_chapter: FromDishka[EditChapter[str]],
    request_body: EditChapterSchema,
    book_name: Annotated[str, Query(alias="bookName")],
    chapter_number_int: Annotated[PositiveInt, Query(alias="chapterNumber")],
    signed_access_token: AccessTokenCookie.StrOrNoneWithLock = None,
) -> Response:
    await edit_chapter(
        signed_access_token,
        book_name,
        chapter_number_int,
        request_body.new_text,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
