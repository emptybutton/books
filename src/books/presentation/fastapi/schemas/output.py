from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, PositiveInt


class SimpleBookSchema(BaseModel):
    name: str


class UserSchema(BaseModel):
    name: str
    written_books: tuple[SimpleBookSchema, ...] = Field(alias="writtenBooks")


class ChapterTextVersionSchema(BaseModel):
    number: PositiveInt
    text: str


class ChapterSchema(BaseModel):
    number: PositiveInt
    text_versions: tuple[ChapterTextVersionSchema, ...] = Field(
        alias="textVersions"
    )
    last_modification_time: datetime = Field(alias="lastModificationTime")
    creation_time: datetime = Field(alias="creationTime")
    views: int = Field(ge=0)


class BookSchema(BaseModel):
    name: str
    author_name: str = Field(alias="authorName")
    chapter_numbers: tuple[PositiveInt, ...] = Field(alias="chapterNumbers")
    last_modification_time: datetime = Field(alias="lastModificationTime")
    creation_time: datetime = Field(alias="creationTime")
    views: int = Field(ge=0)


class FailedAuthenticationSchema(BaseModel):
    type: Literal["failedAuthentication"] = "failedAuthentication"


class NoBookSchema(BaseModel):
    type: Literal["noBook"] = "noBook"


class NoChapterSchema(BaseModel):
    type: Literal["noChapter"] = "noChapter"


class NotAuthorSchema(BaseModel):
    type: Literal["notAuthor"] = "notAuthor"


class NotUniqueChapterNumberSchema(BaseModel):
    type: Literal["notUniqueChapterNumber"] = "notUniqueChapterNumber"


class NotUniqueUserNameSchema(BaseModel):
    type: Literal["notUniqueUserName"] = "notUniqueUserName"


class NotUniqueBookNameSchema(BaseModel):
    type: Literal["notUniqueBookName"] = "notUniqueBookName"


class FailedSigningInSchema(BaseModel):
    type: Literal["failedSigningIn"] = "failedSigningIn"
