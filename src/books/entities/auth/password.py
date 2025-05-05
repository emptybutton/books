from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Password:
    str: str


class PasswordHashes(ABC):
    @abstractmethod
    def hash(self, password: Password) -> str: ...

    @abstractmethod
    def is_hash_valid(self, hash: str, password: Password) -> bool: ...
