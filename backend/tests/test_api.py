from datetime import timedelta

from tests.conftest import add_member, at, login, make_app


def test_unknown_token_and_bad_password_are_rejected() -> None:
    app = make_app(at(2025, 10, 15))
    assert app.client.get("/api/p/missing").status_code == 404
    assert app.client.post("/api/admin/login", json={"password": "wrong"}).status_code == 401
    assert app.client.get("/api/admin/groups").status_code == 401


def test_home_does_not_show_another_group() -> None:
    app = _open(at(2025, 10, 15))
    first = add_member(app, "Pohjoinen", "Aino")
    second = add_member(app, "Etelä", "Leevi")
    _log(app, second["participant"]["token"], "2025-10-14T12:00:00", "4.0", "Etelän latu")
    home = app.client.get(f"/api/p/{first['participant']['token']}").json()
    assert home["places"] == []
    assert home["can_create"] is True


def test_new_entry_trims_place_and_stays_editable() -> None:
    app = _open(at(2025, 10, 15))
    token = add_member(app)["participant"]["token"]
    created = _log(app, token, "2025-10-14T12:00:00", "10.1", "  Sievin valaistulatu ")
    own = app.client.get(f"/api/p/{token}/entries").json()
    assert created["kilometers"] == "10.1"
    assert created["place"] == "Sievin valaistulatu"
    assert own[0]["can_edit"] is True


def test_stats_include_only_the_token_group() -> None:
    app = _open(at(2025, 10, 15))
    first = add_member(app, "Pohjoinen", "Aino")
    second = add_member(app, "Etelä", "Leevi")
    _log(app, second["participant"]["token"], "2025-10-14T12:00:00", "4.0", "Etelän latu")
    _log(app, first["participant"]["token"], "2025-10-14T12:00:00", "10.1", "Sievi")
    stats = app.client.get(f"/api/p/{first['participant']['token']}/stats").json()
    names = {member["name"] for member in stats["season_totals"]}
    assert names == {"Aino"}


def test_places_default_to_the_participants_latest() -> None:
    app = _open(at(2025, 10, 15))
    group = add_member(app)
    other = app.client.post(f"/api/admin/groups/{group['group']['id']}/participants", json={"name": "Leevi"})
    _log(app, other.json()["token"], "2025-10-10T12:00:00", "2.0", "Kuusamo")
    _log(app, group["participant"]["token"], "2025-10-12T12:00:00", "3.0", "Sievi")
    _log(app, group["participant"]["token"], "2025-10-14T12:00:00", "1.0", None)
    home = app.client.get(f"/api/p/{group['participant']['token']}").json()
    assert home["default_place"] is None
    assert home["places"] == ["Sievi", "Kuusamo"]


def test_participant_cannot_log_while_season_is_closed() -> None:
    app = _open(at(2026, 5, 10))
    token = add_member(app)["participant"]["token"]
    blocked = _post_entry(app, token, "2026-04-30T12:00:00", "5.0")
    stats = app.client.get(f"/api/p/{token}/stats").json()
    assert blocked.json()["code"] == "outside_season"
    assert stats["season"] == 2025
    assert stats["can_create"] is False


def test_admin_can_log_past_season_days_only() -> None:
    app = _open(at(2026, 5, 10))
    member = add_member(app)
    allowed = _admin_entry(app, member, "2026-04-20T12:00:00", "6.0")
    summer = _admin_entry(app, member, "2025-06-02T12:00:00", "1.0")
    assert allowed.status_code == 201
    assert summer.json()["code"] == "outside_season"


def test_participant_cannot_backdate_beyond_fourteen_days() -> None:
    app = _open(at(2025, 10, 15))
    token = add_member(app)["participant"]["token"]
    too_old = _post_entry(app, token, "2025-09-30T12:00:00", "1.0")
    assert too_old.json()["code"] == "too_far_in_past"


def test_participant_can_edit_and_delete_a_fresh_entry() -> None:
    app = _open(at(2025, 10, 15))
    token = add_member(app)["participant"]["token"]
    created = _log(app, token, "2025-10-14T12:00:00", "2.0", "Sievi")
    patched = _patch(app, f"/api/p/{token}/entries/{created['id']}", "2025-10-13T08:00:00", "2.5", "Sievi")
    assert patched.json()["kilometers"] == "2.5"
    assert patched.json()["created_at"].startswith("2025-10-15")
    assert app.client.delete(f"/api/p/{token}/entries/{created['id']}").status_code == 204


def test_old_entry_is_closed_for_the_participant() -> None:
    app = _open(at(2026, 5, 10))
    member = add_member(app)
    entry_id = _aged_entry(app, member["participant"]["id"])
    blocked = _patch(app, f"/api/p/{member['participant']['token']}/entries/{entry_id}", "2026-04-28T12:00:00", "1.0", "Sievi")
    assert blocked.json()["code"] == "edit_window_closed"


def test_admin_can_change_a_closed_entry() -> None:
    app = _open(at(2026, 5, 10))
    member = add_member(app)
    entry_id = _aged_entry(app, member["participant"]["id"])
    updated = _patch(app, f"/api/admin/entries/{entry_id}", "2025-03-01T12:00:00", "8.0", "Vanha")
    listed = app.client.get(f"/api/admin/groups/{member['group']['id']}/entries")
    assert updated.status_code == 200
    assert listed.json()[0]["kilometers"] == "8.0"


def test_removing_a_member_deletes_entries_and_link() -> None:
    app = _open(at(2025, 10, 15))
    member = add_member(app)
    _log(app, member["participant"]["token"], "2025-10-14T12:00:00", "1.0", "Sievi")
    removed = app.client.delete(f"/api/admin/participants/{member['participant']['id']}")
    assert removed.status_code == 204
    assert app.client.get(f"/api/p/{member['participant']['token']}").status_code == 404
    assert app.client.get(f"/api/admin/groups/{member['group']['id']}/entries").json() == []
    assert app.client.delete(f"/api/admin/groups/{member['group']['id']}").status_code == 204


def test_group_with_a_member_cannot_be_deleted() -> None:
    app = _open(at(2025, 10, 15))
    member = add_member(app)
    blocked = app.client.delete(f"/api/admin/groups/{member['group']['id']}")
    assert blocked.status_code == 409
    assert blocked.json()["code"] == "group_not_empty"


def test_renewed_link_replaces_the_old_one() -> None:
    app = make_app(at(2025, 10, 15))
    login(app)
    member = add_member(app)
    renewed = app.client.post(f"/api/admin/participants/{member['participant']['id']}/link")
    assert renewed.status_code == 200
    old_token = member["participant"]["token"]
    assert app.client.get(f"/api/p/{old_token}").status_code == 404
    assert app.client.get(f"/api/p/{renewed.json()['token']}").status_code == 200


def test_logout_ends_the_admin_session() -> None:
    app = make_app(at(2025, 10, 15))
    login(app)
    assert app.client.post("/api/admin/logout").status_code == 204
    assert app.client.get("/api/admin/groups").status_code == 401


def _open(moment):
    app = make_app(moment)
    login(app)
    return app


def _patch(app, path: str, performed_at: str, distance: str, place: str):
    body = {"performed_at": performed_at, "distance_km": distance, "place": place}
    return app.client.patch(path, json=body)


def _log(app, token: str, performed_at: str, distance: str, place: str | None) -> dict:
    response = _post_entry(app, token, performed_at, distance, place)
    assert response.status_code == 201
    return response.json()


def _post_entry(app, token: str, performed_at: str, distance: str, place: str | None = "Sievi"):
    return app.client.post(
        f"/api/p/{token}/entries",
        json={"performed_at": performed_at, "distance_km": distance, "place": place},
    )


def _admin_entry(app, member: dict, performed_at: str, distance: str):
    return app.client.post(
        f"/api/admin/groups/{member['group']['id']}/entries",
        json={
            "participant_id": member["participant"]["id"],
            "performed_at": performed_at,
            "distance_km": distance,
            "place": "Latu",
        },
    )


def _aged_entry(app, participant_id: int) -> int:
    created = app.clock.moment - timedelta(days=8)
    stored = app.repository.add_entry(participant_id, at(2026, 4, 28), 10, "Sievi", created)
    return stored.id
