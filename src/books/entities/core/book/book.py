from dataclasses import dataclass
from uuid import UUID

from effect import Effect, IdentifiedValue

from books.entities.core.book.chapter import Chapter, ChapterNumber
from books.entities.time.time import Time


@dataclass(frozen=True)
class Book(IdentifiedValue[UUID]):
    author_id: UUID
    chapters: tuple[Chapter, ...]


def book_last_modification_time(book: Book) -> Time:
    last_modification_times = (
        chapter.last_modification_time for chapter in book.chapters
    )

    return max(last_modification_times, key=lambda it: it.datetime)


class NoChaptersForChapterNumber


def book_with_new_chapter(
    chapter_number: ChapterNumber | None,
    chapter_text: str,
) -> Effect[Book, Chapter, Book]:
