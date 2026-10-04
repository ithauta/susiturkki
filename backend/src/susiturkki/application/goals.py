from dataclasses import dataclass
from datetime import date

from susiturkki.application.access import require_person
from susiturkki.application.ports import Clock, SkiRepository
from susiturkki.domain.birth import accepted_birth_year
from susiturkki.domain.distance import optional_tenths
from susiturkki.domain.goal import (
    SeasonGoal,
    carry_goal,
    ensure_kilometers_open,
    goal_season_start_year,
    kilometers_editable,
    moved_target,
    required_target,
)
from susiturkki.domain.models import Person
from susiturkki.domain.season import entry_in_season, season_start_year
from susiturkki.domain.time import local_date


@dataclass(frozen=True)
class Profile:
    person: Person
    season: int
    goal: SeasonGoal | None
    kilometers_editable: bool


def read_profile(repository: SkiRepository, clock: Clock, token: str) -> Profile:
    return _profile(repository, clock, require_person(repository, token))


def save_profile(repository, clock, token: str, birth_year: int | None, kilometers, target_on: date | None) -> Profile:
    person = require_person(repository, token)
    _store_birth(repository, clock, person.id, birth_year)
    _store_goal(repository, clock, person.id, kilometers, target_on)
    return read_profile(repository, clock, token)


def follow_target(repository: SkiRepository, person_id: int, performed_at, now) -> None:
    season = season_start_year(now)
    if season is None or season_start_year(performed_at) != season:
        return
    _move_target(repository, person_id, performed_at, season)


def _profile(repository: SkiRepository, clock: Clock, person: Person) -> Profile:
    now = clock.now()
    season = goal_season_start_year(now)
    return Profile(person, season, settled_goal(repository, person.id, season), kilometers_editable(now))


def settled_goal(repository: SkiRepository, person_id: int, season: int) -> SeasonGoal | None:
    current = repository.get_goal(person_id, season)
    if current is not None:
        return current
    return _carry(repository, person_id, season)


def _carry(repository: SkiRepository, person_id: int, season: int) -> SeasonGoal | None:
    previous = repository.get_goal(person_id, season - 1)
    if previous is None or previous.distance_tenths is None:
        return None
    carried = carry_goal(previous)
    repository.save_goal(carried)
    return carried


def _store_birth(repository, clock, person_id: int, birth_year: int | None) -> None:
    repository.set_birth_year(person_id, accepted_birth_year(birth_year, clock.now()))


def _store_goal(repository, clock, person_id: int, kilometers, target_on: date | None) -> None:
    now = clock.now()
    season = goal_season_start_year(now)
    current = settled_goal(repository, person_id, season)
    tenths = optional_tenths(kilometers)
    ensure_kilometers_open(_tenths_of(current), tenths, now)
    repository.save_goal(SeasonGoal(person_id, season, tenths, required_target(tenths, target_on, season)))


def _tenths_of(goal: SeasonGoal | None) -> int | None:
    if goal is None:
        return None
    return goal.distance_tenths


def _move_target(repository: SkiRepository, person_id: int, performed_at, season: int) -> None:
    goal = repository.get_goal(person_id, season)
    latest = latest_day(repository.list_entries_for_person(person_id), season)
    if latest is None:
        return
    _save_moved(repository, goal, moved_target(goal, local_date(performed_at), latest, season))


def _save_moved(repository: SkiRepository, goal: SeasonGoal | None, moved: date | None) -> None:
    if goal is None or moved is None:
        return
    repository.save_goal(SeasonGoal(goal.person_id, goal.season_start_year, goal.distance_tenths, moved))


def latest_day(entries, start_year: int) -> date | None:
    chosen = [local_date(entry.performed_at) for entry in entries if entry_in_season(entry, start_year)]
    if not chosen:
        return None
    return max(chosen)
