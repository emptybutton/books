from collections.abc import Iterable
from dataclasses import dataclass


class NegativeOrZeroChapterNumberError(Exception): ...


@dataclass(frozen=True)
class ChapterNumber:
    int: int

    def __post_init__(self) -> None:
        """
        :raises books.entities.core.book.chapter_number.NegativeOrZeroChapterNumberError:
        """  # noqa: E501

        if self.int <= 0:
            raise NegativeOrZeroChapterNumberError


def default_next_chapter_number(
    chapters_numbers: Iterable[ChapterNumber]
) -> ChapterNumber:
    chapters_number_ints = (
        chapters_number.int for chapters_number in chapters_numbers
    )

    return ChapterNumber(
        max(chapters_number_ints, default=0) + 1
    )
