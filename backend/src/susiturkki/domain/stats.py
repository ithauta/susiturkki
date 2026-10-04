from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from susiturkki.domain.distance import kilometers_from_tenths
from susiturkki.domain.models import Entry, Participant, ordered_members
from susiturkki.domain.rules import logging_open
from susiturkki.domain.season import entry_in_season, season_months, season_week_starts
from susiturkki.domain.time import in_helsinki, local_date, week_start

RECENT_LIMIT = 5


@dataclass(frozen=True)
class MemberKilometers:
    participant_id: int
    name: str
    kilometers: Decimal


@dataclass(frozen=True)
class PeriodStats:
    key: str
    members: tuple[MemberKilometers, ...]


@dataclass(frozen=True)
class RecentSki:
    performed_on: date
    kilometers: Decimal
    place: str | None
    style: str
    conditions: str


@dataclass(frozen=True)
class MemberRecent:
    participant_id: int
    name: str
    entries: tuple[RecentSki, ...]


@dataclass(frozen=True)
class SeasonStats:
    season: int
    can_create: bool
    season_totals: tuple[MemberKilometers, ...]
    months: tuple[PeriodStats, ...]
    weeks: tuple[PeriodStats, ...]
    recent: tuple[MemberRecent, ...]


def season_stats(participants, entries, start_year: int, now) -> SeasonStats:
    in_season = [entry for entry in entries if entry_in_season(entry, start_year)]
    return _season_stats(participants, entries, in_season, start_year, now)


def quick_places(entries: list[Entry]) -> tuple[str, ...]:
    ordered = sorted(entries, key=_by_recent, reverse=True)
    return _unique_places(ordered)


def default_place(participant_id: int, entries: list[Entry]) -> str | None:
    own = [entry for entry in entries if entry.participant_id == participant_id]
    if not own:
        return None
    return max(own, key=_by_recent).place


def _season_stats(participants, entries, in_season, start_year: int, now) -> SeasonStats:
    return SeasonStats(
        start_year,
        logging_open(now),
        member_totals(participants, in_season),
        _month_stats(participants, in_season, start_year),
        _week_stats(participants, in_season, start_year),
        recent_by_member(participants, entries),
    )


def member_totals(participants, entries) -> tuple[MemberKilometers, ...]:
    tenths = _tenths_by_participant(entries)
    members = ordered_members(list(participants))
    return tuple(_member_kilometers(person, tenths) for person in members)


def recent_by_member(participants, entries) -> tuple[MemberRecent, ...]:
    members = ordered_members(list(participants))
    return tuple(_member_recent(person, entries) for person in members)


def _month_stats(participants, entries, start_year: int) -> tuple[PeriodStats, ...]:
    months = season_months(start_year)
    return tuple(_month_period(participants, entries, year, month) for year, month in months)


def _week_stats(participants, entries, start_year: int) -> tuple[PeriodStats, ...]:
    weeks = season_week_starts(start_year)
    return tuple(_week_period(participants, entries, monday) for monday in weeks)


def _month_period(participants, entries, year: int, month: int) -> PeriodStats:
    selected = [entry for entry in entries if _in_month(entry, year, month)]
    return PeriodStats(f"{year:04d}-{month:02d}", member_totals(participants, selected))


def _week_period(participants, entries, monday: date) -> PeriodStats:
    selected = [entry for entry in entries if _in_week(entry, monday)]
    return PeriodStats(monday.isoformat(), member_totals(participants, selected))


def _member_recent(person: Participant, entries) -> MemberRecent:
    own = [entry for entry in entries if entry.participant_id == person.id]
    newest = sorted(own, key=_by_recent, reverse=True)[:RECENT_LIMIT]
    skis = tuple(_recent_ski(entry) for entry in newest)
    return MemberRecent(person.id, person.name, skis)


def _member_kilometers(person: Participant, tenths: dict[int, int]) -> MemberKilometers:
    kilometers = kilometers_from_tenths(tenths.get(person.id, 0))
    return MemberKilometers(person.id, person.name, kilometers)


def _tenths_by_participant(entries) -> dict[int, int]:
    sums: dict[int, int] = {}
    for entry in entries:
        sums[entry.participant_id] = sums.get(entry.participant_id, 0) + entry.distance_tenths
    return sums


def _recent_ski(entry: Entry) -> RecentSki:
    kilometers = kilometers_from_tenths(entry.distance_tenths)
    return RecentSki(local_date(entry.performed_at), kilometers, entry.place, entry.style, entry.conditions)


def _unique_places(ordered: list[Entry]) -> tuple[str, ...]:
    seen: list[str] = []
    for entry in ordered:
        if entry.place and entry.place not in seen:
            seen.append(entry.place)
    return tuple(seen)


def _by_recent(entry: Entry) -> tuple:
    return (in_helsinki(entry.performed_at), entry.id)


def _in_month(entry: Entry, year: int, month: int) -> bool:
    local = in_helsinki(entry.performed_at)
    return local.year == year and local.month == month


def _in_week(entry: Entry, monday: date) -> bool:
    return week_start(local_date(entry.performed_at)) == monday
