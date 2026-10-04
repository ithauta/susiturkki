from datetime import date, datetime

from susiturkki.domain.goal import SeasonGoal
from susiturkki.domain.models import Entry, Group, Participant, Person
from susiturkki.domain.time import in_helsinki


def dump_time(moment: datetime) -> str:
    return in_helsinki(moment).isoformat()


def load_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def group_from(row) -> Group:
    return Group(int(row["id"]), row["name"])


def person_from(row) -> Person:
    return Person(int(row["id"]), row["given_name"], row["family_name"], row["token"], _birth(row))


def participant_from(row) -> Participant:
    return Participant(int(row["id"]), int(row["group_id"]), row["given_name"], row["family_name"], row["token"], int(row["person_id"]))


def entry_from(row) -> Entry:
    performed = load_time(row["performed_at"])
    created = load_time(row["created_at"])
    return new_entry(int(row["id"]), int(row["participant_id"]), performed, int(row["distance_tenths"]), row["place"], created, row["style"], row["conditions"])


def entry_params(participant_id: int, performed_at, tenths: int, place, created_at, style: str, conditions: str) -> tuple:
    return (participant_id, dump_time(performed_at), tenths, place, dump_time(created_at), style, conditions)


def new_entry(row_id: int, participant_id: int, performed_at, tenths: int, place, created_at, style: str, conditions: str) -> Entry:
    return Entry(row_id, participant_id, in_helsinki(performed_at), tenths, place, in_helsinki(created_at), style, conditions)


def goal_from(row) -> SeasonGoal:
    return SeasonGoal(int(row["person_id"]), int(row["season_start_year"]), _tenths(row), _day(row))


def goal_params(goal: SeasonGoal) -> tuple:
    return (goal.person_id, goal.season_start_year, goal.distance_tenths, _iso(goal.target_on))


def _birth(row) -> int | None:
    if row["birth_year"] is None:
        return None
    return int(row["birth_year"])


def _tenths(row) -> int | None:
    if row["distance_tenths"] is None:
        return None
    return int(row["distance_tenths"])


def _day(row) -> date | None:
    if row["target_on"] is None:
        return None
    return date.fromisoformat(row["target_on"])


def _iso(day: date | None) -> str | None:
    if day is None:
        return None
    return day.isoformat()
