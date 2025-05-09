from enum import Enum


class Tag(Enum):
    user = "User"
    current_user = "Current user"
    other_user = "Other user"
    book = "Book"
    chapter = "Chapter"
    monitoring = "Monitoring"


tags_metadata = [
    {
        "name": Tag.current_user.value,
        "description": "Current user endpoints.",
    },
    {
        "name": Tag.other_user.value,
        "description": "Other user endpoints.",
    },
    {
        "name": Tag.user.value,
        "description": "User endpoints.",
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
