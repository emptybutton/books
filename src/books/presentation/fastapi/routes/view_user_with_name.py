from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse, Response

from books.application.view_user_with_name import ViewUserWithName
from books.presentation.fastapi.schemas.output import UserSchema
from books.presentation.fastapi.tags import Tag


view_user_with_name_router = APIRouter()


@view_user_with_name_router.get(
    "/users",
    responses={
        status.HTTP_200_OK: {"model": UserSchema},
        status.HTTP_204_NO_CONTENT: {},
    },
    summary="View user with name",
    description=(
        "View user with name."
        " If there is no user with an input name,"
        " the response body will be empty."
    ),
    tags=[Tag.other_user, Tag.user],
)
@inject
async def view_user_with_name_route(
    view_user_with_name: FromDishka[ViewUserWithName[str, UserSchema | None]],
    user_name: Annotated[str, Query(alias="name")],
) -> Response:
    view = await view_user_with_name(user_name)

    if view is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    response_body = view.model_dump(mode="json", by_alias=True)
    return JSONResponse(response_body)
