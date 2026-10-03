from susiturkki.domain.models import Entry, Participant
from susiturkki.domain.stats import season_stats
from tests.conftest import at


def test_totals_follow_the_selected_season_and_weeks() -> None:
    stats = season_stats(_people(), _entries(), 2025, at(2025, 10, 15))
    assert stats.can_create is True
    assert _kilometers(stats.season_totals, "Aino") == "15.0"
    assert _kilometers(stats.season_totals, "Leevi") == "3.5"
    assert _period(stats.months, "2025-10", "Aino") == "15.0"
    assert _period(stats.weeks, "2025-09-29", "Aino") == "10.0"
    assert _period(stats.months, "2026-01", "Leevi") == "3.5"


def test_recent_entries_ignore_the_selected_season() -> None:
    stats = season_stats(_people(), _entries(), 2025, at(2025, 10, 15))
    aino = next(member for member in stats.recent if member.name == "Aino")
    dates = [ski.performed_on.isoformat() for ski in aino.entries]
    assert dates == ["2025-10-08", "2025-10-01", "2024-03-01"]
    assert aino.entries[-1].place == "Vanha latu"


def test_only_five_newest_entries_are_kept() -> None:
    extra = [_ski(index, 1, at(2025, 10, index), 10) for index in range(1, 8)]
    stats = season_stats(_people(), extra, 2025, at(2025, 10, 15))
    aino = next(member for member in stats.recent if member.name == "Aino")
    assert len(aino.entries) == 5
    assert aino.entries[0].performed_on.isoformat() == "2025-10-07"


def _people() -> list[Participant]:
    return [Participant(1, 1, "Aino", "a"), Participant(2, 1, "Leevi", "b")]


def _entries() -> list[Entry]:
    return [
        _ski(1, 1, at(2025, 10, 1), 100, "Sievi"),
        _ski(2, 1, at(2025, 10, 8), 50, "Sievi"),
        _ski(3, 2, at(2026, 1, 15), 35, "Kuusamo"),
        _ski(4, 1, at(2024, 3, 1), 20, "Vanha latu"),
    ]


def _ski(entry_id: int, participant_id: int, performed, tenths: int, place: str = "Latu") -> Entry:
    return Entry(entry_id, participant_id, performed, tenths, place, performed)


def _kilometers(members, name: str) -> str:
    return str(next(member.kilometers for member in members if member.name == name))


def _period(periods, key: str, name: str) -> str:
    period = next(item for item in periods if item.key == key)
    return _kilometers(period.members, name)
