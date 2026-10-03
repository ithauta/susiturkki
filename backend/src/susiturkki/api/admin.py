from fastapi import APIRouter, Depends, Request, Response

from susiturkki.api.deps import get_clock, get_repository, get_settings, require_admin
from susiturkki.api.present import entry_json, group_json, named_json, participant_json, stats_json
from susiturkki.api.schemas import AdminEntryBody, EntryBody, NameBody, PasswordBody
from susiturkki.application.auth import ensure_password
from susiturkki.application.entries import add_admin_entry, delete_admin_entry, list_group_entries, update_admin_entry
from susiturkki.application.groups import create_group, delete_group, list_groups, rename_group
from susiturkki.application.statistics import statistics_for_group
from susiturkki.application.participants import add_participant, remove_participant, rename_participant, renew_link

public = APIRouter(prefix="/api/admin")
secured = APIRouter(prefix="/api/admin", dependencies=[Depends(require_admin)])


@public.post("/login", status_code=204)
def login(body: PasswordBody, request: Request, settings=Depends(get_settings)) -> Response:
    ensure_password(body.password, settings.admin_password)
    request.session["is_admin"] = True
    return Response(status_code=204)


@public.post("/logout", status_code=204)
def logout(request: Request) -> Response:
    request.session.clear()
    return Response(status_code=204)


@secured.get("/groups")
def read_groups(repository=Depends(get_repository)) -> list[dict]:
    return [group_json(details) for details in list_groups(repository)]


@secured.post("/groups", status_code=201)
def post_group(body: NameBody, repository=Depends(get_repository)) -> dict:
    return named_json(create_group(repository, body.name))


@secured.patch("/groups/{group_id}")
def patch_group(group_id: int, body: NameBody, repository=Depends(get_repository)) -> dict:
    return named_json(rename_group(repository, group_id, body.name))


@secured.delete("/groups/{group_id}", status_code=204)
def remove_group(group_id: int, repository=Depends(get_repository)) -> Response:
    delete_group(repository, group_id)
    return Response(status_code=204)


@secured.post("/groups/{group_id}/participants", status_code=201)
def post_participant(group_id: int, body: NameBody, repository=Depends(get_repository)) -> dict:
    return participant_json(add_participant(repository, group_id, body.name))


@secured.patch("/participants/{participant_id}")
def patch_participant(participant_id: int, body: NameBody, repository=Depends(get_repository)) -> dict:
    return participant_json(rename_participant(repository, participant_id, body.name))


@secured.delete("/participants/{participant_id}", status_code=204)
def delete_participant(participant_id: int, repository=Depends(get_repository)) -> Response:
    remove_participant(repository, participant_id)
    return Response(status_code=204)


@secured.post("/participants/{participant_id}/link")
def post_link(participant_id: int, repository=Depends(get_repository)) -> dict:
    return participant_json(renew_link(repository, participant_id))


@secured.get("/groups/{group_id}/stats")
def read_group_stats(group_id: int, season: int | None = None, repository=Depends(get_repository), clock=Depends(get_clock)) -> dict:
    return stats_json(statistics_for_group(repository, clock, group_id, season))


@secured.get("/groups/{group_id}/entries")
def read_entries(group_id: int, repository=Depends(get_repository)) -> list[dict]:
    return [entry_json(entry) for entry in list_group_entries(repository, group_id)]


@secured.post("/groups/{group_id}/entries", status_code=201)
def post_entry(group_id: int, body: AdminEntryBody, repository=Depends(get_repository), clock=Depends(get_clock)) -> dict:
    entry = add_admin_entry(
        repository, clock, group_id, body.participant_id, body.performed_at, body.distance_km, body.place
    )
    return entry_json(entry)


@secured.patch("/entries/{entry_id}")
def patch_entry(entry_id: int, body: EntryBody, repository=Depends(get_repository), clock=Depends(get_clock)) -> dict:
    entry = update_admin_entry(repository, clock, entry_id, body.performed_at, body.distance_km, body.place)
    return entry_json(entry)


@secured.delete("/entries/{entry_id}", status_code=204)
def remove_entry(entry_id: int, repository=Depends(get_repository)) -> Response:
    delete_admin_entry(repository, entry_id)
    return Response(status_code=204)
