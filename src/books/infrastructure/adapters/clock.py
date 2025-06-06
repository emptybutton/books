from dataclasses import dataclass
from datetime import UTC, datetime

from books.application.ports.clock import Clock
from books.entities.time.time import Time


@dataclass(frozen=True)
class StoppedClock(Clock):
    current_time: Time

    async def get_current_time(self) -> Time:
        return self.current_time


@dataclass(frozen=True)
class LocalHostClock(Clock):
    async def get_current_time(self) -> Time:
        return Time(datetime=datetime.now(UTC))
