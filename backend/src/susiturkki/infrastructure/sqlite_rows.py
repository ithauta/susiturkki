from datetime import datetime

from susiturkki.domain.models import Entry, Group, Participant, Person
from susiturkki.domain.time import in_helsinki


def dump_time(moment: datetime) -> str:
    return in_helsinki(moment).isoformat()


def load_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def group_from(row) -> Group:
    return Group(int(row["id"]), row["name"])


def person_from(row) -> Person:
    return Person(int(row["id"]), row["name"], row["token"])


def participant_from(row) -> Participant:
    return Participant(int(row["id"]), int(row["group_id"]), row["name"], row["token"], int(row["person_id"]))


def entry_from(row) -> Entry:
    return Entry(
        int(row["id"]),
        int(row["participant_id"]),
        load_time(row["performed_at"]),
        int(row["distance_tenths"]),
        row["place"],
        load_time(row["created_at"]),
    )


def entry_params(participant_id: int, performed_at, tenths: int, place, created_at) -> tuple:
    return (participant_id, dump_time(performed_at), tenths, place, dump_time(created_at))


def new_entry(row_id: int, participant_id: int, performed_at, tenths: int, place, created_at) -> Entry:
    return Entry(row_id, participant_id, in_helsinki(performed_at), tenths, place, in_helsinki(created_at))
