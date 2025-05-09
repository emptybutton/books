from in_memory_db import InMemoryDb

from books.entities.core.book.book import Book
from books.entities.core.book.chapter import Chapter
from books.entities.core.book.chapter_text_version import ChapterTextVersion


def loaded_book_from_in_memory_db(db: InMemoryDb, book: Book) -> Book:
    chapters = db.subset(Chapter).select_many(
        lambda it: it.book_id == book.id
    )
    loaded_chapters = tuple(
        loaded_chapter_from_in_memory_db(db, chapter)
        for chapter in chapters
    )

    return Book(
        id=book.id,
        author_id=book.author_id,
        name=book.name,
        chapters=loaded_chapters,
        last_modification_time=book.last_modification_time,
        creation_time=book.creation_time,
    )


def loaded_chapter_from_in_memory_db(
    db: InMemoryDb, chapter: Chapter
) -> Chapter:
    loaded_text_versions = db.subset(ChapterTextVersion).select_many(
        lambda it: it.chapter_id == chapter.id
    )

    return Chapter(
        id=chapter.id,
        book_id=chapter.book_id,
        number=chapter.number,
        last_modification_time=chapter.last_modification_time,
        creation_time=chapter.creation_time,
        text_versions=loaded_text_versions,
        views=chapter.views,
    )
