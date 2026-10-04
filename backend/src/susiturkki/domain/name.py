from susiturkki.domain.errors import RuleError


def display_name(given_name: str, family_name: str) -> str:
    return f"{given_name} {family_name}".strip()


def split_name(name: str) -> tuple[str, str]:
    given, _gap, family = name.strip().partition(" ")
    return given, family.strip()


def require_given_name(given_name: str) -> str:
    trimmed = given_name.strip()
    if not trimmed:
        raise RuleError("given_name_required")
    return trimmed


def clean_family_name(family_name: str | None) -> str:
    if family_name is None:
        return ""
    return family_name.strip()
