from susiturkki.domain.errors import RuleError
from susiturkki.domain.time import in_helsinki

EARLIEST_BIRTH_YEAR = 1900


def accepted_birth_year(year: int | None, now) -> int | None:
    if year is None:
        return None
    if year < EARLIEST_BIRTH_YEAR or year > in_helsinki(now).year:
        raise RuleError("birth_year_invalid")
    return year
