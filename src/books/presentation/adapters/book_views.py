from dataclasses import dataclass

from in_memory_db import InMemoryDb

from books.application.ports.book_views import BookViews
from books.entities.auth.user import User
from books.entities.core.book.book import Book, book_views
from books.entities.core.book.chapter import Chapter
from books.entities.core.book.chapter_number import ChapterNumber
from books.infrastructure.book_loading import (
    loaded_book_from_in_memory_db,
    loaded_chapter_from_in_memory_db,
)
from books.presentation.fastapi.schemas.output import (
    BookSchema,
    ChapterSchema,
    ChapterTextVersionSchema,
)


@dataclass(frozen=True)
class BooksAndChaptersFromInMemoryDbAsBookViews(
    BookViews[Book | None, Chapter | None]
):
    db: InMemoryDb

    async def book_view(self, book_name: str, /) -> Book | None:
        book = self.db.subset(Book).select_one(lambda it: it.name == book_name)

        if book is None:
            return None

        return loaded_book_from_in_memory_db(self.db, book)

    async def book_chapter_view(
        self,
        book: Book,
        book_chapter_number: ChapterNumber,
        /
    ) -> Chapter | None:
        chapter = self.db.subset(Chapter).select_one(lambda it: (
            it.book_id == book.id and it.number == book_chapter_number
        ))

        if chapter is None:
            return None

        return loaded_chapter_from_in_memory_db(self.db, chapter)


@dataclass(frozen=True)
class BookSchemasAndChapterSchemasFromInMemoryDbAsBookViews(
    BookViews[BookSchema | None, ChapterSchema | None]
):
    db: InMemoryDb

    async def book_view(self, book_name: str, /) -> BookSchema | None:
        book = self.db.subset(Book).select_one(lambda it: it.name == book_name)

        if book is None:
            return None

        book = loaded_book_from_in_memory_db(self.db, book)
        author = self.db.subset(User).select_one(
            lambda it: it.id == book.author_id
        )
        chapter_numbers = (chapter.number.int for chapter in book.chapters)

        if author is None:
            raise ValueError("no author in in-memory-db")  # noqa: TRY003

        return BookSchema(
            name=book.name,
            authorName=author.name,
            chapterNumbers=tuple(sorted(chapter_numbers)),
            lastModificationTime=book.last_modification_time.datetime,
            views=book_views(book).int,
        )

    async def book_chapter_view(
        self,
        book: Book,
        book_chapter_number: ChapterNumber,
        /
    ) -> ChapterSchema | None:
        chapter = self.db.subset(Chapter).select_one(lambda it: (
            it.book_id == book.id and it.number == book_chapter_number
        ))

        if chapter is None:
            return None

        chapter = loaded_chapter_from_in_memory_db(self.db, chapter)
        text_versions = sorted(chapter.text_versions, key=lambda it: it.number)

        text_version_schemas = tuple(
            ChapterTextVersionSchema(number=version.number, text=version.str)
            for version in text_versions
        )

        return ChapterSchema(
            number=chapter.number.int,
            textVersions=text_version_schemas,
            views=chapter.views.int,
            lastModificationTime=chapter.last_modification_time.datetime,
        )
