from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from books.application.ports.map import (
    NotUniqueBookNameError,
    NotUniqueUserNameError,
)
from books.application.sign_in import FailedSigningInError
from books.entities.auth.access_token import AuthenticationError
from books.entities.core.book.book import (
    NoBookError,
    NotAuthorError,
    NotUniqueChapterNumberError,
)
from books.entities.core.book.chapter import NoChapterError
from books.presentation.fastapi.schemas.output import (
    FailedAuthenticationSchema,
    FailedSigningInSchema,
    NoBookSchema,
    NoChapterSchema,
    NotAuthorSchema,
    NotUniqueBookNameSchema,
    NotUniqueChapterNumberSchema,
    NotUniqueUserNameSchema,
)


def add_error_handling(app: FastAPI) -> None:
    _add_400_error_handling(app)
    _add_401_error_handling(app)
    _add_403_error_handling(app)
    _add_404_error_handling(app)
    _add_409_error_handling(app)


def _add_404_error_handling(app: FastAPI) -> None:
    @app.exception_handler(NoBookError)
    def _(_: object, __: object) -> JSONResponse:
        response_body = NoBookSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status.HTTP_404_NOT_FOUND)

    @app.exception_handler(NoChapterError)
    def _(_: object, __: object) -> JSONResponse:
        response_body = NoChapterSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status.HTTP_404_NOT_FOUND)


def _add_401_error_handling(app: FastAPI) -> None:
    @app.exception_handler(AuthenticationError)
    def _(_: object, __: object) -> JSONResponse:
        response_body = FailedAuthenticationSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status.HTTP_401_UNAUTHORIZED)


def _add_403_error_handling(app: FastAPI) -> None:
    @app.exception_handler(NotAuthorError)
    def _(_: object, __: object) -> JSONResponse:
        response_body = NotAuthorSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status.HTTP_403_FORBIDDEN)


def _add_400_error_handling(app: FastAPI) -> None:
    @app.exception_handler(FailedSigningInError)
    def _(_: object, __: object) -> JSONResponse:
        response_body = FailedSigningInSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status.HTTP_400_BAD_REQUEST)


def _add_409_error_handling(app: FastAPI) -> None:
    @app.exception_handler(NotUniqueUserNameError)
    def _(_: object, __: object) -> JSONResponse:
        response_body = NotUniqueUserNameSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status.HTTP_409_CONFLICT)

    @app.exception_handler(NotUniqueBookNameError)
    def _(_: object, __: object) -> JSONResponse:
        response_body = NotUniqueBookNameSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status.HTTP_409_CONFLICT)

    @app.exception_handler(NotUniqueChapterNumberError)
    def _(_: object, __: object) -> JSONResponse:
        response_body = NotUniqueChapterNumberSchema().model_dump(
            mode="json", by_alias=True
        )
        return JSONResponse(response_body, status.HTTP_409_CONFLICT)
