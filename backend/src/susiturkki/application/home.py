from dataclasses import dataclass

from susiturkki.application.access import require_group, require_person
from susiturkki.application.ports import Clock, SkiRepository
from susiturkki.domain.models import Group, Person
from susiturkki.domain.rules import logging_open
from susiturkki.domain.stats import default_place, quick_places


@dataclass(frozen=True)
class ParticipantHome:
    person: Person
    groups: tuple[Group, ...]
    default_place: str | None
    places: tuple[str, ...]
    can_create: bool


def participant_home(repository: SkiRepository, clock: Clock, token: str) -> ParticipantHome:
    person = require_person(repository, token)
    return _home_for(repository, clock, person)


def _home_for(repository: SkiRepository, clock: Clock, person: Person) -> ParticipantHome:
    memberships = repository.list_memberships(person.id)
    groups = _groups(repository, memberships)
    return _assemble(repository, clock, person, groups)


def _assemble(repository, clock, person: Person, groups: tuple[Group, ...]) -> ParticipantHome:
    return ParticipantHome(person, groups, _default(repository, person), _places(repository, groups), logging_open(clock.now()))


def _groups(repository: SkiRepository, memberships) -> tuple[Group, ...]:
    groups = [require_group(repository, item.group_id) for item in memberships]
    return tuple(sorted(groups, key=lambda group: (group.name, group.id)))


def _default(repository: SkiRepository, person: Person) -> str | None:
    return default_place(person.id, repository.list_entries_for_person(person.id))


def _places(repository: SkiRepository, groups: tuple[Group, ...]) -> tuple[str, ...]:
    return quick_places(_entries(repository, groups))


def _entries(repository: SkiRepository, groups: tuple[Group, ...]) -> list:
    entries = []
    for group in groups:
        entries.extend(repository.list_entries_for_group(group.id))
    return entries
