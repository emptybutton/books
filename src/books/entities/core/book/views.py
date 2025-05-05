from dataclasses import dataclass


class NegativeViewsError(Exception): ...


@dataclass(frozen=True)
class Views:
    int: int

    def __post_init__(self) -> None:
        """
        :raises books.entities.core.book.views.NegativeViewsError:
        """

        if self.int < 0:
            raise NegativeViewsError

    def __add__(self, other: "Views") -> "Views":
        return Views(self.int + other.int)


no_views = Views(0)


def increased_views(views: Views) -> Views:
    return Views(views.int + 1)
