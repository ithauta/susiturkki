from datetime import date

from susiturkki.domain.goal import SeasonGoal, carry_goal, goal_season_start_year, kilometers_editable, moved_target, required_target, shift_target
from tests.conftest import at


def test_february_29_moves_to_february_28() -> None:
    assert shift_target(date(2024, 2, 29)) == date(2025, 2, 28)


def test_goal_season_is_the_upcoming_one_in_summer() -> None:
    assert goal_season_start_year(at(2026, 5, 2)) == 2026
    assert goal_season_start_year(at(2026, 1, 10)) == 2025
    assert kilometers_editable(at(2025, 12, 31)) is True
    assert kilometers_editable(at(2026, 1, 1)) is False


def test_carried_goal_keeps_kilometers_and_shifts_the_day() -> None:
    carried = carry_goal(SeasonGoal(1, 2025, 1000, date(2026, 3, 15)))
    assert carried.season_start_year == 2026
    assert carried.distance_tenths == 1000
    assert carried.target_on == date(2027, 3, 15)


def test_a_ski_after_the_target_uses_the_latest_day() -> None:
    goal = SeasonGoal(1, 2025, 1000, date(2026, 1, 15))
    assert moved_target(goal, date(2026, 1, 20), date(2026, 1, 20), 2025) == date(2026, 1, 20)
    assert moved_target(goal, date(2026, 1, 10), date(2026, 1, 10), 2025) is None


def test_target_date_must_belong_to_the_season() -> None:
    assert required_target(None, None, 2025) is None
    assert required_target(100, date(2026, 3, 1), 2025) == date(2026, 3, 1)
    assert _code(lambda: required_target(100, None, 2025)) == "target_date_required"
    assert _code(lambda: required_target(100, date(2026, 6, 1), 2025)) == "outside_season"


def _code(call) -> str:
    try:
        call()
    except Exception as error:
        return error.code
    return ""
