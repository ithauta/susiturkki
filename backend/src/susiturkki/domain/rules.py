from datetime import datetime, timedelta
from enum import Enum

from susiturkki.domain.errors import RuleError
from susiturkki.domain.season import is_in_season
from susiturkki.domain.time import in_helsinki

PAST_LIMIT = timedelta(days=14)
EDIT_WINDOW = timedelta(days=7)


class Actor(Enum):
    PARTICIPANT = "participant"
    ADMIN = "admin"


def logging_open(now: datetime) -> bool:
    return is_in_season(now)


def within_edit_window(created_at: datetime, now: datetime) -> bool:
    return in_helsinki(now) - in_helsinki(created_at) <= EDIT_WINDOW


def validate_new_entry(actor: Actor, performed_at: datetime, now: datetime) -> None:
    if actor is Actor.ADMIN:
        ensure_admin_activity(performed_at, now)
        return
    ensure_participant_create(performed_at, now)


def validate_participant_update(created_at: datetime, performed_at: datetime, now: datetime) -> None:
    ensure_edit_window(created_at, now)
    ensure_participant_activity(performed_at, now)


def validate_participant_delete(created_at: datetime, now: datetime) -> None:
    ensure_edit_window(created_at, now)


def ensure_admin_activity(performed_at: datetime, now: datetime) -> None:
    ensure_not_in_future(performed_at, now)
    ensure_activity_in_season(performed_at)


def ensure_participant_create(performed_at: datetime, now: datetime) -> None:
    ensure_logging_open(now)
    ensure_participant_activity(performed_at, now)


def ensure_participant_activity(performed_at: datetime, now: datetime) -> None:
    ensure_not_in_future(performed_at, now)
    ensure_within_past_limit(performed_at, now)
    ensure_activity_in_season(performed_at)


def ensure_logging_open(now: datetime) -> None:
    if not logging_open(now):
        raise RuleError("outside_season")


def ensure_edit_window(created_at: datetime, now: datetime) -> None:
    if not within_edit_window(created_at, now):
        raise RuleError("edit_window_closed")


def ensure_not_in_future(performed_at: datetime, now: datetime) -> None:
    if in_helsinki(performed_at) > in_helsinki(now):
        raise RuleError("in_future")


def ensure_within_past_limit(performed_at: datetime, now: datetime) -> None:
    earliest = in_helsinki(now) - PAST_LIMIT
    if in_helsinki(performed_at) < earliest:
        raise RuleError("too_far_in_past")


def ensure_activity_in_season(performed_at: datetime) -> None:
    if not is_in_season(performed_at):
        raise RuleError("outside_season")
