from susiturkki.application.access import membership_for, require_group, require_person
from susiturkki.application.ports import Clock, SkiRepository
from susiturkki.domain.season import default_season_start_year
from susiturkki.domain.stats import SeasonStats, season_stats


def statistics_for_token(repository, clock, token: str, season: int | None, group_id: int | None = None) -> SeasonStats:
    person = require_person(repository, token)
    membership = membership_for(repository, person.id, group_id)
    return statistics_for_group(repository, clock, membership.group_id, season)


def statistics_for_group(repository: SkiRepository, clock: Clock, group_id: int, season: int | None) -> SeasonStats:
    require_group(repository, group_id)
    return _statistics(repository, clock, group_id, season)


def _statistics(repository: SkiRepository, clock: Clock, group_id: int, season: int | None) -> SeasonStats:
    now = clock.now()
    start_year = season if season is not None else default_season_start_year(now)
    participants = repository.list_participants(group_id)
    entries = repository.list_entries_for_group(group_id)
    return season_stats(participants, entries, start_year, now)
