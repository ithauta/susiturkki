import secrets

from susiturkki.application.access import require_group, require_participant
from susiturkki.application.ports import SkiRepository
from susiturkki.domain.models import Participant
from susiturkki.domain.place import require_name


def add_participant(repository: SkiRepository, group_id: int, name: str) -> Participant:
    require_group(repository, group_id)
    return repository.add_participant(group_id, require_name(name), new_link_token())


def rename_participant(repository: SkiRepository, participant_id: int, name: str) -> Participant:
    require_participant(repository, participant_id)
    return repository.rename_participant(participant_id, require_name(name))


def remove_participant(repository: SkiRepository, participant_id: int) -> None:
    require_participant(repository, participant_id)
    repository.delete_participant(participant_id)


def renew_link(repository: SkiRepository, participant_id: int) -> Participant:
    require_participant(repository, participant_id)
    return repository.replace_token(participant_id, new_link_token())


def new_link_token() -> str:
    return secrets.token_urlsafe(32)
