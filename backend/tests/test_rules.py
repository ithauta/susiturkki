from datetime import timedelta
from decimal import Decimal

import pytest

from susiturkki.domain.distance import parse_distance_tenths
from susiturkki.domain.errors import RuleError
from susiturkki.domain.place import normalize_place, require_name
from susiturkki.domain.rules import (
    Actor,
    ensure_admin_activity,
    validate_new_entry,
    validate_participant_delete,
    validate_participant_update,
)
from tests.conftest import at


def test_distance_accepts_one_decimal() -> None:
    assert parse_distance_tenths(Decimal("10.1")) == 101


def test_distance_rejects_extra_precision_and_zero() -> None:
    assert _code(lambda: parse_distance_tenths(Decimal("10.11"))) == "distance_precision"
    assert _code(lambda: parse_distance_tenths(Decimal("0"))) == "distance_not_positive"


def test_place_and_name_are_trimmed() -> None:
    assert normalize_place("  Sievin valaistulatu  ") == "Sievin valaistulatu"
    assert normalize_place("   ") is None
    assert require_name("  Aino ") == "Aino"
    assert _code(lambda: require_name("  ")) == "name_required"


def test_participant_can_log_exactly_fourteen_days_back() -> None:
    now = at(2025, 10, 15)
    validate_new_entry(Actor.PARTICIPANT, now - timedelta(days=14), now)


def test_participant_cannot_log_beyond_fourteen_days_or_the_future() -> None:
    now = at(2025, 10, 15)
    too_old = now - timedelta(days=14, seconds=1)
    assert _code(lambda: validate_new_entry(Actor.PARTICIPANT, too_old, now)) == "too_far_in_past"
    assert _code(lambda: validate_new_entry(Actor.PARTICIPANT, now + timedelta(seconds=1), now)) == "in_future"


def test_off_season_day_is_rejected_inside_the_past_limit() -> None:
    now = at(2025, 10, 5)
    assert _code(lambda: validate_new_entry(Actor.PARTICIPANT, at(2025, 9, 28), now)) == "outside_season"


def test_participant_cannot_create_while_season_is_closed() -> None:
    now = at(2026, 5, 10)
    assert _code(lambda: validate_new_entry(Actor.PARTICIPANT, at(2026, 4, 30), now)) == "outside_season"


def test_edit_window_is_seven_days_from_creation() -> None:
    now = at(2026, 5, 10)
    validate_participant_delete(now - timedelta(days=7), now)
    closed = now - timedelta(days=7, seconds=1)
    assert _code(lambda: validate_participant_delete(closed, now)) == "edit_window_closed"


def test_update_keeps_the_fourteen_day_limit() -> None:
    now = at(2025, 10, 15)
    created = now - timedelta(days=1)
    too_old = now - timedelta(days=14, seconds=1)
    assert _code(lambda: validate_participant_update(created, too_old, now)) == "too_far_in_past"


def test_admin_can_log_a_past_season_but_not_summer_or_future() -> None:
    now = at(2025, 10, 15)
    ensure_admin_activity(at(2025, 3, 1), now)
    assert _code(lambda: ensure_admin_activity(at(2025, 6, 1), now)) == "outside_season"
    assert _code(lambda: ensure_admin_activity(now + timedelta(minutes=1), now)) == "in_future"


def _code(action) -> str:
    with pytest.raises(RuleError) as caught:
        action()
    return caught.value.code
