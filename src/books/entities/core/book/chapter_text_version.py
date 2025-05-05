from dataclasses import dataclass
from uuid import UUID, uuid4

from effect import IdentifiedValue, New, new


@dataclass(frozen=True)
class ChapterTextVersion(IdentifiedValue[UUID]):
    chapter_id: UUID
    str: str
    number: int


def first_chapter_text_version(
    chapter_id: UUID, chapter_text: str
) -> New[ChapterTextVersion]:
    return new(ChapterTextVersion(uuid4(), chapter_id, chapter_text, 1))


def next_chapter_text_version(
    text_version: ChapterTextVersion,
    new_text_version_text: str,
) -> New[ChapterTextVersion]:
    return new(ChapterTextVersion(
        uuid4(),
        text_version.chapter_id,
        new_text_version_text,
        text_version.number + 1,
    ))
