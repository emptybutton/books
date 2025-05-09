from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import Response

from books.application.sign_out import SignOut
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.tags import Tag


sign_out_router = APIRouter()


@sign_out_router.delete(
    "/users/me",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_204_NO_CONTENT: {}},
    summary="Sign out",
    description=(
        "Sign out as a current user."
        " If there is no current user, nothing happens."
    ),
    tags=[Tag.current_user, Tag.user],
)
@inject
async def sign_out_route(
    sign_out: FromDishka[SignOut[str]],
    signed_access_token: AccessTokenCookie.StrOrNone,
) -> Response:
    result = await sign_out(signed_access_token)

    response = Response(status_code=status.HTTP_204_NO_CONTENT)

    if result is not None:
        cookie = AccessTokenCookie(response)
        cookie.set(
            result.signed_access_token,
            result.signed_access_token_expiration_time.datetime,
        )

    return response
