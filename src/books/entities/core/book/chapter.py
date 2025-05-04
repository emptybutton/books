from dataclasses import dataclass
from uuid import UUID, uuid4

from effect import IdentifiedValue, New, new

from books.entities.time.time import Time


class InvalidChapterNumberError(Exception): ...


@dataclass(frozen=True)
class ChapterNumber:
    int: int

    def __post_init__(self) -> None:
        """
        :raises books.entities.core.book.chapter.InvalidChapterNumberError:
        """

        if self.int <= 0:
            raise InvalidChapterNumberError


@dataclass(frozen=True)
class Chapter(IdentifiedValue[UUID]):
    book_id: UUID
    number: ChapterNumber
    last_modification_time: Time
    text: str
