from dataclasses import dataclass
from datetime import date

from susiturkki.domain.errors import RuleError
from susiturkki.domain.season import season_bounds, season_start_year
from susiturkki.domain.time import in_helsinki


@dataclass(frozen=True)
class SeasonGoal:
    person_id: int
    season_start_year: int
    distance_tenths: int | None
    target_on: date | None


def goal_season_start_year(moment) -> int:
    opened = season_start_year(moment)
    if opened is not None:
        return opened
    return in_helsinki(moment).year


def kilometers_editable(moment) -> bool:
    return in_helsinki(moment).month >= 10


def shift_target(day: date) -> date:
    return _same_day(day.year + 1, day.month, day.day)


def carry_goal(previous: SeasonGoal) -> SeasonGoal:
    return SeasonGoal(previous.person_id, previous.season_start_year + 1, previous.distance_tenths, _shifted(previous.target_on))


def ensure_kilometers_open(current: int | None, requested: int | None, now) -> None:
    if current == requested or kilometers_editable(now):
        return
    raise RuleError("target_km_closed")


def required_target(tenths: int | None, target: date | None, start_year: int) -> date | None:
    if tenths is None:
        return None
    if target is None:
        raise RuleError("target_date_required")
    ensure_date_in_season(target, start_year)
    return target


def ensure_date_in_season(target: date, start_year: int) -> None:
    first, last = season_bounds(start_year)
    if target < first or target > last:
        raise RuleError("outside_season")


def moved_target(goal: SeasonGoal | None, performed_on: date, latest_on: date, open_season: int | None) -> date | None:
    target = _active_target(goal, open_season)
    if target is None or performed_on <= target or latest_on == target:
        return None
    return latest_on


def _same_day(year: int, month: int, day: int) -> date:
    try:
        return date(year, month, day)
    except ValueError:
        return date(year, month, day - 1)


def _shifted(day: date | None) -> date | None:
    if day is None:
        return None
    return shift_target(day)


def _active_target(goal: SeasonGoal | None, open_season: int | None) -> date | None:
    if goal is None or open_season is None or goal.season_start_year != open_season:
        return None
    return goal.target_on
