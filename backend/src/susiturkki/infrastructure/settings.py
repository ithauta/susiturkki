import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_path: str
    admin_password: str
    session_secret: str


def load_settings() -> Settings:
    return Settings(_database_path(), _required("ADMIN_PASSWORD"), _required("SESSION_SECRET"))


def _database_path() -> str:
    return os.environ.get("DATABASE_PATH", "susiturkki.db")


def _required(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise RuntimeError(f"missing {name}")
    return value
