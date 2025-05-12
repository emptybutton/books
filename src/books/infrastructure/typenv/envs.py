from dataclasses import dataclass
from pathlib import Path

import typenv


@dataclass(kw_only=True, frozen=True)
class Envs:
    jwt_secret: str
    telegram_secrets_file_path: Path

    @classmethod
    def load(cls) -> "Envs":
        env = typenv.Env()

        return Envs(
            jwt_secret=env.str("JWT_SECRET"),
            telegram_secrets_file_path=Path(
                env.str("TELEGRAM_SECRETS_FILE_PATH")
            ),
        )
