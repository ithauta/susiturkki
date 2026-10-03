from datetime import datetime, timezone

from susiturkki.domain.season import (
    default_season_start_year,
    is_in_season,
    season_start_year,
    season_week_starts,
)
from tests.conftest import at


def test_season_opens_on_october_first() -> None:
    assert season_start_year(at(2025, 9, 30, 23, 59)) is None
    assert season_start_year(at(2025, 10, 1, 0, 0)) == 2025


def test_season_closes_after_april() -> None:
    assert season_start_year(at(2026, 4, 30, 23, 59)) == 2025
    assert season_start_year(at(2026, 5, 1, 0, 0)) is None


def test_january_belongs_to_previous_october() -> None:
    assert season_start_year(at(2026, 1, 15)) == 2025


def test_helsinki_offset_decides_the_season() -> None:
    still_april_in_utc = datetime(2026, 4, 30, 21, 30, tzinfo=timezone.utc)
    assert is_in_season(still_april_in_utc) is False


def test_off_season_defaults_to_last_ended_season() -> None:
    assert default_season_start_year(at(2026, 7, 1)) == 2025


def test_first_week_starts_on_monday_before_october() -> None:
    assert season_week_starts(2025)[0].isoformat() == "2025-09-29"
