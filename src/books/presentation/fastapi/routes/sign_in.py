from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from books.application.sign_in import FailedSigningInError, SignIn
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.schemas.output import (
    FailedSigningInSchema,
    NotUniqueUserNameSchema,
)
from books.presentation.fastapi.tags import Tag


sign_in_router = APIRouter()


class SignInSchema(BaseModel):
    user_name: str = Field(alias="userName")
    password: str


@sign_in_router.put(
    "/users",
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_400_BAD_REQUEST: {"model": NotUniqueUserNameSchema},
    },
    summary="Sign in",
    description="Sign in as a current user.",
    tags=[Tag.user],
)
@inject
async def sign_in_route(
    sign_in: FromDishka[SignIn[str]],
    request_body: SignInSchema,
) -> Response:
    try:
        result = await sign_in(request_body.user_name, request_body.password)
    except FailedSigningInError:
        response_body = FailedSigningInSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status.HTTP_400_BAD_REQUEST)

    response = Response({}, status_code=status.HTTP_204_NO_CONTENT)

    cookie = AccessTokenCookie(response)
    cookie.set(
        result.signed_access_token,
        result.signed_access_token_expiration_time.datetime,
    )

    return response
