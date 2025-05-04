from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from books.entities.time.time import Time


@dataclass
class AccessToken:
    user_id: UUID
    expriration_time: Time


def issued_access_token(user_id: UUID, current_time: Time) -> AccessToken:
    return AccessToken(
        user_id,
        current_time.map(lambda it: it + timedelta(days=365)),
    )
