from susiturkki.domain.errors import RuleError


def normalize_place(place: str | None) -> str | None:
    if place is None:
        return None
    trimmed = place.strip()
    if not trimmed:
        return None
    return trimmed


def require_name(name: str) -> str:
    trimmed = name.strip()
    if not trimmed:
        raise RuleError("name_required")
    return trimmed
