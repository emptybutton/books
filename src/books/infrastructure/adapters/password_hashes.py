import hashlib
from dataclasses import dataclass
from secrets import token_urlsafe

from books.entities.auth.password import Password, PasswordHashes


class PasswordsAsPasswordHashes(PasswordHashes):
    def hash(self, password: Password) -> str:
        return password.str

    def is_hash_valid(self, hash: str, password: Password) -> bool:
        return hash == password.str


@dataclass(frozen=True)
class Pbkdf2HmacPasswordHashes(PasswordHashes):
    salt_lenght: int
    iterations: int
    hash_lenght: int | None

    def hash(self, password: Password) -> str:
        salt = token_urlsafe(self.salt_lenght).encode()
        hash_ = hashlib.pbkdf2_hmac(
            "sha256",
            password.str.encode(),
            salt,
            self.iterations,
            self.hash_lenght,
        )
        return f"{salt.decode()}.{hash_.hex()}"

    def is_hash_valid(self, salt_and_hash_hex: str, password: Password) -> bool:
        separator = salt_and_hash_hex.index(".")

        salt = salt_and_hash_hex[:separator].encode()
        hash_hex = salt_and_hash_hex[separator + 1:]

        hash_ = hashlib.pbkdf2_hmac(
            "sha256",
            password.str.encode(),
            salt,
            self.iterations,
            self.hash_lenght,
        )

        return hash_.hex() == hash_hex
