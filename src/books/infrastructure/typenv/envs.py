from dataclasses import dataclass

import typenv


@dataclass(kw_only=True, frozen=True, slots=True)
class Envs:
    jwt_secret: str

    @classmethod
    def load(cls) -> "Envs":
        env = typenv.Env()

        return Envs(jwt_secret=env.str("JWT_SECRET"))
