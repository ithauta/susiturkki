import secrets

from susiturkki.application.access import require_group, require_participant
from susiturkki.application.ports import SkiRepository
from susiturkki.domain.models import Participant, Person
from susiturkki.domain.name import clean_family_name, require_given_name


def add_participant(repository: SkiRepository, group_id: int, given_name: str, family_name: str) -> Participant:
    require_group(repository, group_id)
    return repository.add_participant(group_id, require_given_name(given_name), clean_family_name(family_name), new_link_token())


def join_group(repository: SkiRepository, group_id: int, person_id: int) -> Participant:
    require_group(repository, group_id)
    return repository.add_membership(group_id, person_id)


def enroll(repository: SkiRepository, group_id: int, given_name: str | None, family_name: str | None, person_id: int | None) -> Participant:
    if person_id is not None:
        return join_group(repository, group_id, person_id)
    return add_participant(repository, group_id, given_name or "", family_name)


def list_persons(repository: SkiRepository) -> list[Person]:
    return repository.list_persons()


def rename_participant(repository: SkiRepository, participant_id: int, given_name: str, family_name: str) -> Participant:
    require_participant(repository, participant_id)
    return repository.rename_participant(participant_id, require_given_name(given_name), clean_family_name(family_name))


def remove_participant(repository: SkiRepository, participant_id: int) -> None:
    require_participant(repository, participant_id)
    repository.delete_participant(participant_id)


def renew_link(repository: SkiRepository, participant_id: int) -> Participant:
    require_participant(repository, participant_id)
    return repository.replace_token(participant_id, new_link_token())


def new_link_token() -> str:
    return secrets.token_urlsafe(32)
