from susiturkki.application.ports import SkiRepository
from susiturkki.domain.errors import RuleError
from susiturkki.domain.models import Entry, Group, Participant, Person


def require_group(repository: SkiRepository, group_id: int) -> Group:
    group = repository.get_group(group_id)
    if group is None:
        raise RuleError("group_not_found")
    return group


def require_participant(repository: SkiRepository, participant_id: int) -> Participant:
    participant = repository.get_participant(participant_id)
    if participant is None:
        raise RuleError("participant_not_found")
    return participant


def require_person(repository: SkiRepository, token: str) -> Person:
    person = repository.get_person_by_token(token)
    if person is None:
        raise RuleError("participant_not_found")
    return person


def membership_for(repository: SkiRepository, person_id: int, group_id: int | None) -> Participant:
    return _chosen(repository.list_memberships(person_id), group_id)


def require_entry(repository: SkiRepository, entry_id: int) -> Entry:
    entry = repository.get_entry(entry_id)
    if entry is None:
        raise RuleError("entry_not_found")
    return entry


def require_participant_in_group(repository: SkiRepository, group_id: int, participant_id: int) -> Participant:
    require_group(repository, group_id)
    participant = require_participant(repository, participant_id)
    if participant.group_id != group_id:
        raise RuleError("participant_not_found")
    return participant


def require_own_entry(repository: SkiRepository, person_id: int, entry_id: int) -> Entry:
    entry = require_entry(repository, entry_id)
    if entry.participant_id != person_id:
        raise RuleError("entry_not_found")
    return entry


def _chosen(memberships: list[Participant], group_id: int | None) -> Participant:
    if group_id is None:
        return _only_membership(memberships)
    return _matching_group(memberships, group_id)


def _only_membership(memberships: list[Participant]) -> Participant:
    if len(memberships) != 1:
        raise RuleError("group_not_found")
    return memberships[0]


def _matching_group(memberships: list[Participant], group_id: int) -> Participant:
    found = [item for item in memberships if item.group_id == group_id]
    if not found:
        raise RuleError("group_not_found")
    return found[0]
