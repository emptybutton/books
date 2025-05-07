from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response

from books.application.view_current_user import ViewCurrentUser
from books.presentation.fastapi.cookies import AccessTokenCookie
from books.presentation.fastapi.schemas.output import UserSchema
from books.presentation.fastapi.tags import Tag


view_user_router = APIRouter()


@view_user_router.get(
    "/user",
    responses={
        status.HTTP_200_OK: {"model": UserSchema},
        status.HTTP_204_NO_CONTENT: {},
    },
    summary="View user",
    description="View current user.",
    tags=[Tag.user],
)
@inject
async def view_user_route(
    view_user: FromDishka[ViewCurrentUser[str, UserSchema | None]],
    signed_access_token: AccessTokenCookie.StrOrNone = None,
) -> Response:
    view = await view_user(signed_access_token)

    if view is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    response_body = view.model_dump(mode="json", by_alias=True)
    return JSONResponse(response_body)
