from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import Response
from pydantic import BaseModel

from books.application.create_book import CreateBook
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.schemas.output import (
    FailedAuthenticationSchema,
    NotUniqueBookNameSchema,
)
from books.presentation.fastapi.tags import Tag


create_book_router = APIRouter()


class CreateBookSchema(BaseModel):
    name: str


@create_book_router.post(
    "/books",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"content": None},
        status.HTTP_401_UNAUTHORIZED: {"model": FailedAuthenticationSchema},
        status.HTTP_409_CONFLICT: {"model": NotUniqueBookNameSchema},
    },
    summary="Create book",
    description="Create an empty book authored by a current user.",
    tags=[Tag.book],
)
@inject
async def create_book_route(
    create_book: FromDishka[CreateBook[str]],
    request_body: CreateBookSchema,
    signed_access_token: AccessTokenCookie.StrOrNoneWithLock = None,
) -> Response:
    await create_book(signed_access_token, request_body.name)

    return Response(status_code=status.HTTP_201_CREATED)
