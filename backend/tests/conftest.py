from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from susiturkki.api.factory import create_app
from susiturkki.infrastructure.settings import Settings
from susiturkki.infrastructure.sqlite import SqliteSkiRepository

HELSINKI = ZoneInfo("Europe/Helsinki")
PASSWORD = "secret-password"


class FixedClock:
    def __init__(self, moment: datetime) -> None:
        self.moment = moment

    def now(self) -> datetime:
        return self.moment


@dataclass
class AppFixture:
    client: TestClient
    repository: SqliteSkiRepository
    clock: FixedClock


def at(year: int, month: int, day: int, hour: int = 12, minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=HELSINKI)


def make_app(moment: datetime, session_https: bool = False) -> AppFixture:
    clock = FixedClock(moment)
    repository = SqliteSkiRepository(":memory:")
    settings = Settings("ignored.db", PASSWORD, "session-secret", session_https)
    client = TestClient(create_app(settings, repository, clock))
    return AppFixture(client, repository, clock)


def login(app: AppFixture) -> None:
    response = app.client.post("/api/admin/login", json={"password": PASSWORD})
    assert response.status_code == 204


def add_member(app: AppFixture, group_name: str = "Laturyhmä", member_name: str = "Aino") -> dict:
    group = app.client.post("/api/admin/groups", json={"name": group_name})
    assert group.status_code == 201
    member = app.client.post(
        f"/api/admin/groups/{group.json()['id']}/participants",
        json={"name": member_name},
    )
    assert member.status_code == 201
    return {"group": group.json(), "participant": member.json()}
