from collections.abc import Iterable
from dataclasses import dataclass
from typing import Never
from uuid import UUID, uuid4

from effect import (
    Effect,
    IdentifiedValue,
    Mutated,
    dead,
    just,
    many,
    mutated,
    new,
)

from books.entities.core.book.chapter_number import ChapterNumber
from books.entities.core.book.chapter_text_version import (
    ChapterTextVersion,
    first_chapter_text_version,
    next_chapter_text_version,
)
from books.entities.core.book.views import Views, increased_views, no_views
from books.entities.time.time import Time


class NoAnyChapterTextVersionError(Exception): ...


class NoChapterError(Exception): ...


@dataclass(frozen=True)
class Chapter(IdentifiedValue[UUID]):
    book_id: UUID
    number: ChapterNumber
    last_modification_time: Time
    creation_time: Time
    text_versions: tuple[ChapterTextVersion, ...]
    views: Views

    def __post_init__(self) -> None:
        """
        :raises books.entities.core.book.chapter.NoAnyChapterTextVersionError:
        """

        if not self.text_versions:
            raise NoAnyChapterTextVersionError


type ChapterIdentifiedEntity = Chapter | ChapterTextVersion


def last_chapter_text_version(chapter: Chapter) -> ChapterTextVersion:
    return max(chapter.text_versions, key=lambda it: it.number)


def new_chapter(
    book_id: UUID,
    chapter_number: ChapterNumber,
    chapter_text: str,
    current_time: Time,
) -> Effect[Chapter, Chapter | ChapterTextVersion]:
    new_chapter_id = uuid4()

    new_chapter_text_version = first_chapter_text_version(
        new_chapter_id, chapter_text
    )
    new_chapter = new(Chapter(
        id=new_chapter_id,
        book_id=book_id,
        number=chapter_number,
        last_modification_time=current_time,
        creation_time=current_time,
        text_versions=(just(new_chapter_text_version),),
        views=no_views,
    ))

    return new_chapter_text_version & new_chapter


def deleted_chapter(
    chapter: Chapter
) -> Effect[None, Never, Never, Never, Chapter | ChapterTextVersion]:
    return (
        many(dead(text_version) for text_version in chapter.text_versions)
        & dead(chapter)
        & Effect(None)
    )


def viewed_chapter(chapter: Chapter) -> Mutated[Chapter]:
    return mutated(Chapter(
        id=chapter.id,
        book_id=chapter.book_id,
        number=chapter.number,
        last_modification_time=chapter.last_modification_time,
        creation_time=chapter.creation_time,
        text_versions=chapter.text_versions,
        views=increased_views(chapter.views),
    ))


def edited_chapter(
    chapter: Chapter,
    new_chapter_text: str,
    current_time: Time,
) -> Effect[Chapter, ChapterTextVersion, Never, Chapter]:
    new_chapter_text_version = next_chapter_text_version(
        last_chapter_text_version(chapter),
        new_chapter_text,
    )

    edited_chapter = mutated(Chapter(
        id=chapter.id,
        book_id=chapter.book_id,
        number=chapter.number,
        last_modification_time=current_time,
        creation_time=chapter.creation_time,
        text_versions=(
            *chapter.text_versions, just(new_chapter_text_version)
        ),
        views=chapter.views,
    ))

    return new_chapter_text_version & edited_chapter


def found_chapter(
    chapters: Iterable[Chapter], chapter_number: ChapterNumber
) -> Chapter:
    """
    :raises books.entities.core.book.chapter.NoChapterError:
    """

    try:
        return next(
            chapter for chapter in chapters
            if chapter.number == chapter_number
        )
    except StopIteration:
        raise NoChapterError from None
