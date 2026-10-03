from susiturkki.application.ports import SkiRepository
from susiturkki.domain.errors import RuleError
from susiturkki.domain.models import Entry, Group, Participant


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


def require_participant_token(repository: SkiRepository, token: str) -> Participant:
    participant = repository.get_participant_by_token(token)
    if participant is None:
        raise RuleError("participant_not_found")
    return participant


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


def require_own_entry(repository: SkiRepository, participant_id: int, entry_id: int) -> Entry:
    entry = require_entry(repository, entry_id)
    if entry.participant_id != participant_id:
        raise RuleError("entry_not_found")
    return entry
