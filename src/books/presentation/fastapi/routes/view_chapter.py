from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse, Response
from pydantic import PositiveInt

from books.application.view_chapter import ViewChapter
from books.entities.core.book.book import NoBookError
from books.entities.core.book.chapter import NoChapterError
from books.presentation.fastapi.schemas.output import (
    BookSchema,
    ChapterSchema,
)
from books.presentation.fastapi.tags import Tag


view_chapter_router = APIRouter()


@view_chapter_router.post(
    "/chapters/views",
    responses={
        status.HTTP_200_OK: {"model": ChapterSchema},
        status.HTTP_204_NO_CONTENT: {},
    },
    summary="View chapter",
    description=(
        "View chapter with its number and book name."
        " If there is no book with an input name"
        " or chapter with an input number,"
        " the response body will be empty."
    ),
    tags=[Tag.chapter],
)
@inject
async def view_chapter_route(
    view_chapter: FromDishka[
        ViewChapter[BookSchema | None, ChapterSchema | None]
    ],
    book_name: Annotated[str, Query(alias="bookName")],
    chapter_number_int: Annotated[PositiveInt, Query(alias="chapterNumber")],
) -> Response:
    try:
        view = await view_chapter(book_name, chapter_number_int)
    except (NoBookError, NoChapterError):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    if view is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    response_body = view.model_dump(mode="json", by_alias=True)
    return JSONResponse(response_body)
