from dataclasses import dataclass

from susiturkki.application.access import require_group
from susiturkki.application.ports import SkiRepository
from susiturkki.domain.errors import RuleError
from susiturkki.domain.models import Group, Participant
from susiturkki.domain.place import require_name


@dataclass(frozen=True)
class GroupDetails:
    group: Group
    participants: tuple[Participant, ...]


def list_groups(repository: SkiRepository) -> list[GroupDetails]:
    return [_group_details(repository, group) for group in repository.list_groups()]


def create_group(repository: SkiRepository, name: str) -> Group:
    return repository.add_group(require_name(name))


def rename_group(repository: SkiRepository, group_id: int, name: str) -> Group:
    require_group(repository, group_id)
    return repository.rename_group(group_id, require_name(name))


def delete_group(repository: SkiRepository, group_id: int) -> None:
    require_group(repository, group_id)
    _ensure_group_empty(repository, group_id)
    repository.delete_group(group_id)


def _group_details(repository: SkiRepository, group: Group) -> GroupDetails:
    participants = tuple(repository.list_participants(group.id))
    return GroupDetails(group, participants)


def _ensure_group_empty(repository: SkiRepository, group_id: int) -> None:
    if repository.count_participants(group_id) or repository.count_entries(group_id):
        raise RuleError("group_not_empty")
