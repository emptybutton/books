from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Never
from uuid import UUID, uuid4

from effect import (
    Effect,
    IdentifiedValue,
    New,
    dead,
    existing,
    just,
    many,
    mutated,
    new,
)

from books.entities.auth.access_token import AccessToken, valid_access_token
from books.entities.core.book.chapter import (
    Chapter,
    ChapterIdentifiedEntity,
    deleted_chapter,
    edited_chapter,
    found_chapter,
    new_chapter,
    viewed_chapter,
)
from books.entities.core.book.chapter_number import (
    ChapterNumber,
    default_next_chapter_number,
)
from books.entities.core.book.chapter_text_version import (
    ChapterTextVersion,
)
from books.entities.core.book.views import Views, no_views
from books.entities.time.time import Time


class NotUniqueChapterNumberError(Exception): ...


class NotAuthorError(Exception): ...


@dataclass(frozen=True)
class Book(IdentifiedValue[UUID]):
    author_id: UUID
    name: str
    chapters: tuple[Chapter, ...]
    last_modification_time: Time

    def __post_init__(self) -> None:
        """
        :raises books.entities.core.book.book.NotUniqueChapterNumberError:
        """

        chapter_number_counter = Counter(
            chapter.number for chapter in self.chapters
        )
        if max(chapter_number_counter.values()) > 1:
            raise NotUniqueChapterNumberError

    def __iter__(self) -> Iterator[Chapter]:
        return iter(self.chapters)


type BookIdentifiedEntity = Book | ChapterIdentifiedEntity


def accessible_book_for_editing(
    book: Book, access_token: AccessToken, current_time: Time
) -> Book:
    """
    :raises books.entities.auth.access_token.ExpiredAccessTokenError:
    :raises books.entities.core.book.book.NotAuthorError:
    """

    access_token = valid_access_token(access_token, current_time)

    if access_token.user_id != book.author_id:
        raise NotAuthorError

    return book


def book_views(book: Book) -> Views:
    return sum((chapter.views for chapter in book), no_views)


def new_book(
    access_token: AccessToken, book_name: str, current_time: Time
) -> New[Book]:
    """
    :raises books.entities.auth.access_token.ExpiredAccessTokenError:
    """

    access_token = valid_access_token(access_token, current_time)

    return new(Book(
        id=uuid4(),
        author_id=access_token.user_id,
        name=book_name,
        chapters=tuple(),
        last_modification_time=current_time,
    ))


def deleted_book(
    book: Book, access_token: AccessToken, current_time: Time
) -> Effect[
    None, Never, Never, Never, Book | Chapter | ChapterTextVersion
]:
    """
    :raises books.entities.auth.access_token.ExpiredAccessTokenError:
    :raises books.entities.core.book.book.NotAuthorError:
    """

    book = accessible_book_for_editing(book, access_token, current_time)

    return (
        many(deleted_chapter(chapter) for chapter in book)
        & dead(book)
        & Effect(None)
    )


def book_with_new_chapter(
    book: Book,
    access_token: AccessToken,
    chapter_number: ChapterNumber | None,
    chapter_text: str,
    current_time: Time,
) -> Effect[Book, Chapter | ChapterTextVersion, Never, Book]:
    """
    :raises books.entities.auth.access_token.ExpiredAccessTokenError:
    :raises books.entities.core.book.book.NotAuthorError:
    :raises books.entities.core.book.chapter.NotUniqueChapterNumberError:
    """

    book = accessible_book_for_editing(book, access_token, current_time)

    if chapter_number is None:
        chapter_number = default_next_chapter_number(
            chapter.number for chapter in book.chapters
        )

    new_chapter_ = new_chapter(
        book.id, chapter_number, chapter_text, current_time
    )

    book_with_new_chapter_ = mutated(Book(
        id=book.id,
        name=book.name,
        author_id=book.id,
        chapters=(*book, just(new_chapter_)),
        last_modification_time=current_time,
    ))

    return new_chapter_ & book_with_new_chapter_


def book_without_deleted_chapter(
    book: Book,
    access_token: AccessToken,
    chapter_number: ChapterNumber,
    current_time: Time,
) -> Effect[Book, Never, Never, Book, Chapter]:
    """
    :raises books.entities.auth.access_token.ExpiredAccessTokenError:
    :raises books.entities.core.book.book.NotAuthorError:
    """

    book = accessible_book_for_editing(book, access_token, current_time)

    deleted_chapter = dead(found_chapter(book, chapter_number))

    book_without_deleted_chapter_ = mutated(Book(
        id=book.id,
        name=book.name,
        author_id=book.id,
        chapters=tuple(
            chapter for chapter in book if chapter.is_(just(deleted_chapter))
        ),
        last_modification_time=current_time,
    ))

    return deleted_chapter & book_without_deleted_chapter_


def book_with_viewed_chapter(
    book: Book,
    chapter_number: ChapterNumber
) -> Effect[Book, Never, Never, Chapter]:
    """
    :raises books.entities.core.book.chapter.NoChapterError:
    """

    chapter_to_view = found_chapter(book, chapter_number)

    viewed_chapter_ = viewed_chapter(chapter_to_view)

    book_with_viewed_chapter_ = existing(Book(
        id=book.id,
        name=book.name,
        author_id=book.author_id,
        chapters=(*book.chapters, just(viewed_chapter_)),
        last_modification_time=book.last_modification_time,
    ))

    return viewed_chapter_ & book_with_viewed_chapter_


def book_with_edited_chapter(
    book: Book,
    access_token: AccessToken,
    chapter_number: ChapterNumber,
    new_chapter_text: str,
    current_time: Time,
) -> Effect[Book, ChapterTextVersion, Never, Chapter | Book]:
    """
    :raises books.entities.auth.access_token.ExpiredAccessTokenError:
    :raises books.entities.core.book.book.NotAuthorError:
    :raises books.entities.core.book.chapter.NoChapterError:
    """

    book = accessible_book_for_editing(book, access_token, current_time)

    chapter_to_edit = found_chapter(book, chapter_number)

    edited_chapter_ = edited_chapter(
        chapter_to_edit, new_chapter_text, current_time
    )
    book_with_edited_chapter_ = mutated(Book(
        id=book.id,
        name=book.name,
        author_id=book.author_id,
        chapters=(*book.chapters, just(edited_chapter_)),
        last_modification_time=current_time,
    ))

    return edited_chapter_ & book_with_edited_chapter_
