from dataclasses import dataclass

from susiturkki.application.access import require_group, require_participant_token
from susiturkki.application.ports import Clock, SkiRepository
from susiturkki.domain.models import Group, Participant
from susiturkki.domain.rules import logging_open
from susiturkki.domain.stats import default_place, quick_places


@dataclass(frozen=True)
class ParticipantHome:
    group: Group
    participant: Participant
    default_place: str | None
    places: tuple[str, ...]
    can_create: bool


def participant_home(repository: SkiRepository, clock: Clock, token: str) -> ParticipantHome:
    participant = require_participant_token(repository, token)
    return _home_for(repository, clock, participant)


def _home_for(repository: SkiRepository, clock: Clock, participant: Participant) -> ParticipantHome:
    entries = repository.list_entries_for_group(participant.group_id)
    return ParticipantHome(
        require_group(repository, participant.group_id),
        participant,
        default_place(participant.id, entries),
        quick_places(entries),
        logging_open(clock.now()),
    )
