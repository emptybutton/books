from fastapi import APIRouter, status
from fastapi.responses import Response

from books.presentation.fastapi.tags import Tag


healthcheck_router = APIRouter()


@healthcheck_router.get(
    "/health",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_204_NO_CONTENT: {}},
    description="Checking if the server can accept requests.",
    tags=[Tag.monitoring],
)
def healthcheck() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
