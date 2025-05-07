from enum import Enum


class Tag(Enum):
    user = "User"
    book = "Book"
    chapter = "Chapter"
    monitoring = "Monitoring"


tags_metadata = [
    {
        "name": Tag.user.value,
        "description": "Current user endpoints.",
    },
    {
        "name": Tag.book.value,
        "description": "Book endpoints.",
    },
    {
        "name": Tag.chapter.value,
        "description": "Book chapter endpoints.",
    },
    {
        "name": Tag.monitoring.value,
        "description": "Monitoring endpoints.",
    },
]
