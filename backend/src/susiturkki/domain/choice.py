from susiturkki.domain.errors import RuleError

DEFAULT_STYLE = "free"
DEFAULT_CONDITIONS = "normal"
STYLES = frozenset({DEFAULT_STYLE, "classic", "ungroomed"})
CONDITIONS = frozenset({"slick", DEFAULT_CONDITIONS, "heavy"})


def parse_style(value: str | None) -> str:
    return _known(value, DEFAULT_STYLE, STYLES, "style_invalid")


def parse_conditions(value: str | None) -> str:
    return _known(value, DEFAULT_CONDITIONS, CONDITIONS, "conditions_invalid")


def _known(value: str | None, default: str, allowed: frozenset[str], code: str) -> str:
    chosen = default if not value else value
    if chosen not in allowed:
        raise RuleError(code)
    return chosen
