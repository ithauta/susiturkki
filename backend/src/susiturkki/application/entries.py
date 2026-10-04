from dataclasses import dataclass
from decimal import Decimal

from susiturkki.application.access import (
    require_entry,
    require_group,
    require_own_entry,
    require_participant_in_group,
    require_person,
)
from susiturkki.application.ports import Clock, SkiRepository
from susiturkki.application.goals import follow_target
from susiturkki.domain.choice import parse_conditions, parse_style
from susiturkki.domain.distance import parse_distance_tenths
from susiturkki.domain.models import Entry
from susiturkki.domain.place import normalize_place
from susiturkki.domain.rules import (
    Actor,
    ensure_admin_activity,
    validate_new_entry,
    validate_participant_delete,
    validate_participant_update,
    within_edit_window,
)
from susiturkki.domain.time import in_helsinki


@dataclass(frozen=True)
class OwnEntry:
    entry: Entry
    can_edit: bool


def list_own_entries(repository: SkiRepository, clock: Clock, token: str) -> list[OwnEntry]:
    person = require_person(repository, token)
    return _own_views(repository, clock, person.id)


def list_group_entries(repository: SkiRepository, group_id: int) -> list[Entry]:
    require_group(repository, group_id)
    return repository.list_entries_for_group(group_id)


def add_participant_entry(repository, clock, token: str, performed_at, distance_km: Decimal, place, style, conditions) -> Entry:
    person = require_person(repository, token)
    entry = _save_new(repository, clock, person.id, performed_at, distance_km, place, Actor.PARTICIPANT, style, conditions)
    follow_target(repository, person.id, entry.performed_at, clock.now())
    return entry


def add_admin_entry(repository, clock, group_id: int, participant_id: int, performed_at, distance_km, place, style, conditions) -> Entry:
    participant = require_participant_in_group(repository, group_id, participant_id)
    return _save_new(repository, clock, participant.person_id, performed_at, distance_km, place, Actor.ADMIN, style, conditions)


def update_participant_entry(repository, clock, token: str, entry_id: int, performed_at, distance_km, place, style, conditions) -> Entry:
    person = require_person(repository, token)
    entry = require_own_entry(repository, person.id, entry_id)
    validate_participant_update(entry.created_at, performed_at, clock.now())
    saved = _save_update(repository, entry.id, performed_at, distance_km, place, style, conditions)
    follow_target(repository, person.id, saved.performed_at, clock.now())
    return saved


def update_admin_entry(repository, clock, entry_id: int, performed_at, distance_km, place, style, conditions) -> Entry:
    entry = require_entry(repository, entry_id)
    ensure_admin_activity(performed_at, clock.now())
    return _save_update(repository, entry.id, performed_at, distance_km, place, style, conditions)


def delete_participant_entry(repository: SkiRepository, clock: Clock, token: str, entry_id: int) -> None:
    person = require_person(repository, token)
    entry = require_own_entry(repository, person.id, entry_id)
    validate_participant_delete(entry.created_at, clock.now())
    repository.delete_entry(entry.id)


def delete_admin_entry(repository: SkiRepository, entry_id: int) -> None:
    entry = require_entry(repository, entry_id)
    repository.delete_entry(entry.id)


def _own_views(repository: SkiRepository, clock: Clock, person_id: int) -> list[OwnEntry]:
    now = clock.now()
    entries = repository.list_entries_for_person(person_id)
    return [OwnEntry(entry, within_edit_window(entry.created_at, now)) for entry in entries]


def _save_new(repository, clock, person_id: int, performed_at, distance_km, place, actor: Actor, style, conditions) -> Entry:
    now = clock.now()
    validate_new_entry(actor, performed_at, now)
    return repository.add_entry(person_id, in_helsinki(performed_at), _tenths(distance_km), _place(place), now, parse_style(style), parse_conditions(conditions))


def _save_update(repository, entry_id: int, performed_at, distance_km, place, style, conditions) -> Entry:
    performed = in_helsinki(performed_at)
    return repository.update_entry(entry_id, performed, _tenths(distance_km), _place(place), parse_style(style), parse_conditions(conditions))


def _tenths(distance_km: Decimal) -> int:
    return parse_distance_tenths(distance_km)


def _place(place: str | None) -> str | None:
    return normalize_place(place)
