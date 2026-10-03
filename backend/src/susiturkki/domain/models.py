from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Group:
    id: int
    name: str


@dataclass(frozen=True)
class Participant:
    id: int
    group_id: int
    name: str
    token: str


@dataclass(frozen=True)
class Entry:
    id: int
    participant_id: int
    performed_at: datetime
    distance_tenths: int
    place: str | None
    created_at: datetime


def ordered_members(participants: list[Participant]) -> tuple[Participant, ...]:
    return tuple(sorted(participants, key=lambda person: (person.name, person.id)))
