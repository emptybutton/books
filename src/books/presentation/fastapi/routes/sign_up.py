from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import Response
from pydantic import BaseModel, Field

from books.application.sign_up import SignUp
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.schemas.output import NotUniqueUserNameSchema
from books.presentation.fastapi.tags import Tag


sign_up_router = APIRouter()


class SignUpSchema(BaseModel):
    user_name: str = Field(alias="userName")
    password: str


@sign_up_router.post(
    "/users/me",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"content": None},
        status.HTTP_409_CONFLICT: {"model": NotUniqueUserNameSchema},
    },
    summary="Sign up",
    description="Sign up a new user as a current user.",
    tags=[Tag.current_user, Tag.user],
)
@inject
async def sign_up_route(
    sign_up: FromDishka[SignUp[str]],
    request_body: SignUpSchema,
) -> Response:
    result = await sign_up(request_body.user_name, request_body.password)

    response = Response(status_code=status.HTTP_201_CREATED)

    cookie = AccessTokenCookie(response)
    cookie.set(
        result.signed_access_token,
        result.signed_access_token_expiration_time.datetime,
    )

    return response
