import secrets

from susiturkki.domain.errors import RuleError


def ensure_password(given: str, expected: str) -> None:
    if not secrets.compare_digest(given.encode(), expected.encode()):
        raise RuleError("invalid_credentials")
