from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field, PositiveInt

from books.application.edit_chapter import EditChapter
from books.application.ports.map import NotUniqueUserNameError
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.schemas.output import NotUniqueUserNameSchema
from books.presentation.fastapi.tags import Tag


edit_chapter_router = APIRouter()


class EditChapterSchema(BaseModel):
    new_chapter_text: str = Field(alias="newChapterText")


@edit_chapter_router.post(
    "/users/me",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": BaseModel},
        status.HTTP_409_CONFLICT: {"model": NotUniqueUserNameSchema},
    },
    summary="Sign up",
    description="Sign up a new user as a current user.",
    tags=[Tag.current_user, Tag.user],
)
@inject
async def edit_chapter_route(
    edit_chapter: FromDishka[EditChapter[str]],
    request_body: EditChapterSchema,
    book_name: Annotated[str, Query(alias="bookName")],
    chapter_number_int: Annotated[PositiveInt, Query(alias="chapterNumber")],
    signed_access_token: AccessTokenCookie.StrOrNoneWithLock,
) -> Response:
    try:
        result = await edit_chapter(
            signed_access_token,
            book_name,
            chapter_number_int,
            request_body.new_chapter_text,
        )
    except NotUniqueUserNameError:
        response_body = NotUniqueUserNameSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status_code=status.HTTP_409_CONFLICT)

    response = JSONResponse({}, status_code=status.HTTP_201_CREATED)

    cookie = AccessTokenCookie(response)
    cookie.set(
        result.signed_access_token,
        result.signed_access_token_expiration_time.datetime,
    )

    return response
