from dataclasses import dataclass
from datetime import datetime

from susiturkki.domain.name import display_name


@dataclass(frozen=True)
class Group:
    id: int
    name: str


@dataclass(frozen=True)
class Person:
    id: int
    given_name: str
    family_name: str
    token: str
    birth_year: int | None = None

    @property
    def name(self) -> str:
        return display_name(self.given_name, self.family_name)


@dataclass(frozen=True)
class Participant:
    id: int
    group_id: int
    given_name: str
    family_name: str
    token: str
    person_id: int = 0

    @property
    def name(self) -> str:
        return display_name(self.given_name, self.family_name)


@dataclass(frozen=True)
class Entry:
    id: int
    participant_id: int
    performed_at: datetime
    distance_tenths: int
    place: str | None
    created_at: datetime
    style: str = "free"
    conditions: str = "normal"


def ordered_members(participants: list[Participant]) -> tuple[Participant, ...]:
    return tuple(sorted(participants, key=_member_order))


def _member_order(person: Participant) -> tuple:
    return (person.family_name, person.given_name, person.id)
