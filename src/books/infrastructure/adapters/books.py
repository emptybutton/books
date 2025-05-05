from dataclasses import dataclass

from in_memory_db import InMemoryDb

from books.application.ports.books import Books
from books.entities.core.book.book import Book
from books.entities.core.book.chapter import Chapter
from books.entities.core.book.chapter_text_version import ChapterTextVersion


@dataclass(frozen=True)
class InMemoryBooks(Books):
    db: InMemoryDb

    async def book_with_name(self, name: str, /) -> Book | None:
        book = self.db.subset(Book).select_one(lambda it: it.name == name)

        return None if book is None else self._loaded_book(book)

    def _loaded_book(self, book: Book) -> Book:
        chapters = self.db.subset(Chapter).select_many(
            lambda it: it.book_id == book.id
        )
        loaded_chapters = tuple(map(self._loaded_chapter, chapters))

        return Book(
            id=book.id,
            author_id=book.author_id,
            name=book.name,
            chapters=loaded_chapters,
            last_modification_time=book.last_modification_time,
        )

    def _loaded_chapter(self, chapter: Chapter) -> Chapter:
        loaded_text_versions = self.db.subset(ChapterTextVersion).select_many(
            lambda it: it.chapter_id == chapter.id
        )

        return Chapter(
            id=chapter.id,
            book_id=chapter.book_id,
            number=chapter.number,
            last_modification_time=chapter.last_modification_time,
            text_versions=loaded_text_versions,
            views=chapter.views,
        )
