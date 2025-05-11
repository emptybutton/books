from dataclasses import asdict
from datetime import UTC, datetime
from uuid import UUID

from dirty_equals import IsUUID
from in_memory_db import InMemoryDb
from pytest import fixture, mark

from books.application.create_chapter import CreateChapter
from books.entities.auth.access_token import AccessToken
from books.entities.auth.user import User
from books.entities.core.book.book import Book
from books.entities.core.book.chapter import Chapter
from books.entities.time.time import Time


@fixture(scope="session")
def book1() -> Book:
    return Book(
        id=UUID(int=1),
        name="BOOK",
        author_id=UUID(int=1),
        chapters=tuple(),
        last_modification_time=Time(datetime(2000, 1, 1, tzinfo=UTC)),
        creation_time=Time(datetime(2000, 1, 1, tzinfo=UTC)),
    )


@fixture(scope="session")
def user1() -> User:
    return User(id=UUID(int=1), name="user", password_hash="X")


@fixture(autouse=True)
def add_data_to_db(db: InMemoryDb, book1: Book, user1: User) -> None:
    db.insert(user1)
    db.insert(book1)


@fixture()
def valid_access_token() -> AccessToken:
    return AccessToken(
        user_id=UUID(int=1),
        expriration_time=Time(datetime(2077, 1, 1, tzinfo=UTC)),
    )


async def test_no_errors_with_chapter_number(
    operation: CreateChapter[AccessToken | None],
    valid_access_token: AccessToken,
) -> None:
    await operation(valid_access_token, "BOOK", 1, "TEXT")


@mark.parametrize(
    "stage", ["book_length", "user_length", "chapter_length", "chapters"]
)
async def test_db_with_chapter_number(
    operation: CreateChapter[AccessToken | None],
    stage: str,
    db: InMemoryDb,
    valid_access_token: AccessToken,
    current_time: Time,
) -> None:
    await operation(valid_access_token, "BOOK", 1, "TEXT")

    if stage == "books":
        assert len(db.subset(Book)) == 1

    if stage == "users":
        assert len(db.subset(User)) == 1

    if stage == "chapter_length":
        assert len(db.subset(Chapter)) == 1

    if stage == "chapters":
        chapter = next(iter(db.subset(Chapter)))

        assert asdict(chapter) == {
            "id": IsUUID(4),
            "book_id": UUID(int=1),
            "number": {"int": 1},
            "last_modification_time": asdict(current_time),
            "creation_time": asdict(current_time),
            "text_versions": ({
                "id": IsUUID(4),
                "chapter_id": IsUUID(4),
                "str": "TEXT",
                "number": 1,
            },),
            "views": {"int": 0},
        }
