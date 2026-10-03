import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_path: str
    admin_password: str
    session_secret: str
    session_https: bool


def load_settings() -> Settings:
    return Settings(_required("DATABASE_PATH"), _required("ADMIN_PASSWORD"), _required("SESSION_SECRET"), _flag("SESSION_HTTPS"))


def _required(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise RuntimeError(f"missing {name}")
    return value


def _flag(name: str) -> bool:
    return _bool(name, _required(name))


def _bool(name: str, value: str) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise RuntimeError(f"invalid {name}")
