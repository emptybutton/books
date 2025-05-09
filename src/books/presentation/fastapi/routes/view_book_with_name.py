from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse, Response

from books.application.view_book_with_name import ViewBookWithName
from books.presentation.fastapi.schemas.output import (
    BookSchema,
    ChapterSchema,
)
from books.presentation.fastapi.tags import Tag


view_book_with_name_router = APIRouter()


@view_book_with_name_router.get(
    "/books",
    responses={
        status.HTTP_200_OK: {"model": BookSchema},
        status.HTTP_204_NO_CONTENT: {},
    },
    summary="View book with name",
    description=(
        "View book with name."
        " If there is no book with an input name,"
        " the response body will be empty."
    ),
    tags=[Tag.book],
)
@inject
async def view_book_with_name_route(
    view_book: FromDishka[
        ViewBookWithName[BookSchema | None, ChapterSchema | None]
    ],
    book_name: Annotated[str, Query(alias="name")],
) -> Response:
    view = await view_book(book_name)

    if view is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    response_body = view.model_dump(mode="json", by_alias=True)
    return JSONResponse(response_body)
