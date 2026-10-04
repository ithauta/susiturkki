import sqlite3
from pathlib import Path

from susiturkki.infrastructure.sqlite import SqliteSkiRepository

LEGACY = """
CREATE TABLE groups (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE participants (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    token TEXT NOT NULL UNIQUE
);
CREATE TABLE entries (
    id INTEGER PRIMARY KEY,
    participant_id INTEGER NOT NULL,
    performed_at TEXT NOT NULL,
    distance_tenths INTEGER NOT NULL,
    place TEXT,
    created_at TEXT NOT NULL
);
"""


def test_combined_name_splits_into_given_and_family(tmp_path: Path) -> None:
    path = tmp_path / "named.db"
    _named_person(path)
    person = SqliteSkiRepository(str(path)).get_person_by_token("secret")
    assert person is not None
    assert person.given_name == "Aino"
    assert person.family_name == "Korhonen"


def test_legacy_membership_becomes_a_shared_person(tmp_path: Path) -> None:
    path = tmp_path / "legacy.db"
    _legacy(path)
    repository = SqliteSkiRepository(str(path))
    person = repository.get_person_by_token("secret")
    memberships = repository.list_participants(1)
    assert person is not None and person.name == "Aino"
    assert memberships[0].person_id == person.id
    assert repository.list_entries_for_person(person.id)[0].distance_tenths == 101


def _named_person(path: Path) -> None:
    connection = sqlite3.connect(path)
    connection.execute("CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT NOT NULL, token TEXT NOT NULL UNIQUE)")
    connection.execute("INSERT INTO persons (name, token) VALUES ('Aino Korhonen', 'secret')")
    connection.commit()
    connection.close()


def _legacy(path: Path) -> None:
    connection = sqlite3.connect(path)
    connection.executescript(LEGACY)
    connection.execute("INSERT INTO groups (name) VALUES ('Pohjoinen')")
    connection.execute("INSERT INTO participants (group_id, name, token) VALUES (1, 'Aino', 'secret')")
    _legacy_entry(connection)
    connection.commit()
    connection.close()


def _legacy_entry(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        INSERT INTO entries (participant_id, performed_at, distance_tenths, place, created_at)
        VALUES (1, '2025-10-14T12:00:00', 101, 'Sievi', '2025-10-14T12:00:00')
        """
    )
