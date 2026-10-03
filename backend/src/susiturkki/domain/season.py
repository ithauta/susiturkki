from datetime import date, timedelta

from susiturkki.domain.time import in_helsinki, local_date, week_start


def season_start_year(moment) -> int | None:
    local = in_helsinki(moment)
    if local.month >= 10:
        return local.year
    if local.month <= 4:
        return local.year - 1
    return None


def is_in_season(moment) -> bool:
    return season_start_year(moment) is not None


def default_season_start_year(now) -> int:
    current = season_start_year(now)
    if current is not None:
        return current
    return in_helsinki(now).year - 1


def season_bounds(start_year: int) -> tuple[date, date]:
    return date(start_year, 10, 1), date(start_year + 1, 4, 30)


def season_months(start_year: int) -> tuple[tuple[int, int], ...]:
    autumn = tuple((start_year, month) for month in (10, 11, 12))
    spring = tuple((start_year + 1, month) for month in (1, 2, 3, 4))
    return autumn + spring


def season_week_starts(start_year: int) -> tuple[date, ...]:
    first, last = season_bounds(start_year)
    return tuple(_mondays_through(week_start(first), last))


def entry_in_season(entry, start_year: int) -> bool:
    first, last = season_bounds(start_year)
    day = local_date(entry.performed_at)
    return first <= day <= last


def _mondays_through(monday: date, last: date) -> list[date]:
    mondays: list[date] = []
    current = monday
    while current <= last:
        mondays.append(current)
        current += timedelta(days=7)
    return mondays
