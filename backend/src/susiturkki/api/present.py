from susiturkki.application.entries import OwnEntry
from susiturkki.application.groups import GroupDetails
from susiturkki.application.home import ParticipantHome
from susiturkki.domain.distance import kilometers_from_tenths
from susiturkki.domain.models import Entry, Group, Participant
from susiturkki.domain.stats import MemberKilometers, MemberRecent, PeriodStats, RecentSki, SeasonStats
from susiturkki.domain.time import in_helsinki


def named_json(group: Group) -> dict:
    return {"id": group.id, "name": group.name}


def group_json(details: GroupDetails) -> dict:
    return {
        "id": details.group.id,
        "name": details.group.name,
        "participants": [participant_json(person) for person in details.participants],
    }


def participant_json(person: Participant) -> dict:
    return {"id": person.id, "group_id": person.group_id, "name": person.name, "token": person.token}


def home_json(home: ParticipantHome) -> dict:
    return _identity_json(home) | _logging_json(home)


def entry_json(entry: Entry) -> dict:
    return {
        "id": entry.id,
        "participant_id": entry.participant_id,
        "performed_at": in_helsinki(entry.performed_at).isoformat(),
        "kilometers": str(kilometers_from_tenths(entry.distance_tenths)),
        "place": entry.place,
        "created_at": in_helsinki(entry.created_at).isoformat(),
    }


def own_entry_json(view: OwnEntry) -> dict:
    payload = entry_json(view.entry)
    payload["can_edit"] = view.can_edit
    return payload


def stats_json(stats: SeasonStats) -> dict:
    return {
        "season": stats.season,
        "can_create": stats.can_create,
        "season_totals": members_json(stats.season_totals),
        "months": periods_json(stats.months),
        "weeks": periods_json(stats.weeks),
        "recent": recent_json(stats.recent),
    }


def members_json(members: tuple[MemberKilometers, ...]) -> list[dict]:
    return [_member_json(member) for member in members]


def periods_json(periods: tuple[PeriodStats, ...]) -> list[dict]:
    return [{"key": period.key, "members": members_json(period.members)} for period in periods]


def recent_json(members: tuple[MemberRecent, ...]) -> list[dict]:
    return [_member_recent_json(member) for member in members]


def _identity_json(home: ParticipantHome) -> dict:
    return {
        "group_id": home.group.id,
        "group_name": home.group.name,
        "participant_id": home.participant.id,
        "name": home.participant.name,
    }


def _logging_json(home: ParticipantHome) -> dict:
    return {"default_place": home.default_place, "places": list(home.places), "can_create": home.can_create}


def _member_json(member: MemberKilometers) -> dict:
    return {"participant_id": member.participant_id, "name": member.name, "kilometers": str(member.kilometers)}


def _member_recent_json(member: MemberRecent) -> dict:
    return {
        "participant_id": member.participant_id,
        "name": member.name,
        "entries": [_recent_ski_json(ski) for ski in member.entries],
    }


def _recent_ski_json(ski: RecentSki) -> dict:
    return {"performed_on": ski.performed_on.isoformat(), "kilometers": str(ski.kilometers), "place": ski.place}
