from fastapi import APIRouter, Depends, Response

from susiturkki.api.deps import get_clock, get_repository
from susiturkki.api.present import entry_json, home_json, own_entry_json, profile_json, stats_json
from susiturkki.api.schemas import EntryBody, ProfileBody
from susiturkki.application.entries import (
    add_participant_entry,
    delete_participant_entry,
    list_own_entries,
    update_participant_entry,
)
from susiturkki.application.goals import read_profile, save_profile
from susiturkki.application.home import participant_home
from susiturkki.application.statistics import statistics_for_token

router = APIRouter(prefix="/api/p")


@router.get("/{token}")
def read_home(token: str, repository=Depends(get_repository), clock=Depends(get_clock)) -> dict:
    return home_json(participant_home(repository, clock, token))


@router.get("/{token}/entries")
def read_entries(token: str, repository=Depends(get_repository), clock=Depends(get_clock)) -> list[dict]:
    return [own_entry_json(view) for view in list_own_entries(repository, clock, token)]


@router.post("/{token}/entries", status_code=201)
def create_entry(token: str, body: EntryBody, repository=Depends(get_repository), clock=Depends(get_clock)) -> dict:
    entry = add_participant_entry(repository, clock, token, body.performed_at, body.distance_km, body.place, body.style, body.conditions)
    return entry_json(entry)


@router.patch("/{token}/entries/{entry_id}")
def patch_entry(token: str, entry_id: int, body: EntryBody, repository=Depends(get_repository), clock=Depends(get_clock)) -> dict:
    entry = update_participant_entry(repository, clock, token, entry_id, body.performed_at, body.distance_km, body.place, body.style, body.conditions)
    return entry_json(entry)


@router.delete("/{token}/entries/{entry_id}", status_code=204)
def remove_entry(token: str, entry_id: int, repository=Depends(get_repository), clock=Depends(get_clock)) -> Response:
    delete_participant_entry(repository, clock, token, entry_id)
    return Response(status_code=204)


@router.get("/{token}/profile")
def read_person_profile(token: str, repository=Depends(get_repository), clock=Depends(get_clock)) -> dict:
    return profile_json(read_profile(repository, clock, token))


@router.patch("/{token}/profile")
def patch_person_profile(token: str, body: ProfileBody, repository=Depends(get_repository), clock=Depends(get_clock)) -> dict:
    saved = save_profile(repository, clock, token, body.birth_year, body.distance_km, body.target_on)
    return profile_json(saved)


@router.get("/{token}/stats")
def read_stats(token: str, season: int | None = None, group_id: int | None = None, repository=Depends(get_repository), clock=Depends(get_clock)) -> dict:
    return stats_json(statistics_for_token(repository, clock, token, season, group_id))
