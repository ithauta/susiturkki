import sqlite3
import threading
from datetime import datetime

from susiturkki.domain.errors import RuleError
from susiturkki.domain.models import Entry, Group, Participant, Person
from susiturkki.domain.goal import SeasonGoal
from susiturkki.infrastructure.migrate import upgrade_if_legacy, upgrade_shape
from susiturkki.infrastructure.sqlite_rows import (
    dump_time,
    entry_from,
    entry_params,
    goal_from,
    goal_params,
    group_from,
    new_entry,
    participant_from,
    person_from,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    given_name TEXT NOT NULL,
    family_name TEXT NOT NULL,
    birth_year INTEGER,
    token TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id),
    person_id INTEGER NOT NULL REFERENCES persons(id),
    UNIQUE (group_id, person_id)
);
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
    performed_at TEXT NOT NULL,
    distance_tenths INTEGER NOT NULL,
    place TEXT,
    created_at TEXT NOT NULL,
    style TEXT NOT NULL DEFAULT 'free',
    conditions TEXT NOT NULL DEFAULT 'normal'
);
CREATE TABLE IF NOT EXISTS season_goals (
    person_id INTEGER NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
    season_start_year INTEGER NOT NULL,
    distance_tenths INTEGER,
    target_on TEXT,
    PRIMARY KEY (person_id, season_start_year)
);
CREATE INDEX IF NOT EXISTS entries_person ON entries(person_id);
"""

SELECT_GROUPS = "SELECT id, name FROM groups ORDER BY name, id"
SELECT_GROUP = "SELECT id, name FROM groups WHERE id = ?"
INSERT_GROUP = "INSERT INTO groups (name) VALUES (?)"
UPDATE_GROUP = "UPDATE groups SET name = ? WHERE id = ?"
DELETE_GROUP = "DELETE FROM groups WHERE id = ?"
COUNT_PARTICIPANTS = "SELECT COUNT(*) AS total FROM participants WHERE group_id = ?"
COUNT_ENTRIES = """
SELECT COUNT(*) AS total FROM entries e
JOIN participants m ON m.person_id = e.person_id
WHERE m.group_id = ?
"""
MEMBER_COLUMNS = "m.id, m.group_id, s.given_name, s.family_name, s.token, m.person_id"
SELECT_PARTICIPANTS = f"""
SELECT {MEMBER_COLUMNS} FROM participants m
JOIN persons s ON s.id = m.person_id
WHERE m.group_id = ? ORDER BY s.family_name, s.given_name, m.id
"""
SELECT_PARTICIPANT = f"""
SELECT {MEMBER_COLUMNS} FROM participants m
JOIN persons s ON s.id = m.person_id WHERE m.id = ?
"""
SELECT_MEMBERSHIPS = f"""
SELECT {MEMBER_COLUMNS} FROM participants m
JOIN persons s ON s.id = m.person_id WHERE m.person_id = ? ORDER BY m.id
"""
COUNT_MEMBERSHIPS = "SELECT COUNT(*) AS total FROM participants WHERE person_id = ?"
PERSON_COLUMNS = "id, given_name, family_name, birth_year, token"
SELECT_PERSONS = f"SELECT {PERSON_COLUMNS} FROM persons ORDER BY family_name, given_name, id"
SELECT_PERSON = f"SELECT {PERSON_COLUMNS} FROM persons WHERE id = ?"
SELECT_PERSON_TOKEN = f"SELECT {PERSON_COLUMNS} FROM persons WHERE token = ?"
INSERT_PERSON = "INSERT INTO persons (given_name, family_name, token) VALUES (?, ?, ?)"
INSERT_MEMBERSHIP = "INSERT INTO participants (group_id, person_id) VALUES (?, ?)"
UPDATE_PERSON = "UPDATE persons SET given_name = ?, family_name = ? WHERE id = ?"
UPDATE_BIRTH = "UPDATE persons SET birth_year = ? WHERE id = ?"
SELECT_GOAL = """
SELECT person_id, season_start_year, distance_tenths, target_on
FROM season_goals WHERE person_id = ? AND season_start_year = ?
"""
UPSERT_GOAL = """
INSERT INTO season_goals (person_id, season_start_year, distance_tenths, target_on)
VALUES (?, ?, ?, ?)
ON CONFLICT (person_id, season_start_year) DO UPDATE SET
distance_tenths = excluded.distance_tenths, target_on = excluded.target_on
"""
UPDATE_TOKEN = "UPDATE persons SET token = ? WHERE id = ?"
DELETE_MEMBERSHIP = "DELETE FROM participants WHERE id = ?"
DELETE_PERSON = "DELETE FROM persons WHERE id = ?"
INSERT_ENTRY = """
INSERT INTO entries (person_id, performed_at, distance_tenths, place, created_at, style, conditions)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""
UPDATE_ENTRY = """
UPDATE entries SET performed_at = ?, distance_tenths = ?, place = ?, style = ?, conditions = ? WHERE id = ?
"""
DELETE_ENTRY = "DELETE FROM entries WHERE id = ?"
ENTRY_COLUMNS = "id, person_id AS participant_id, performed_at, distance_tenths, place, created_at, style, conditions"
SELECT_ENTRY = f"SELECT {ENTRY_COLUMNS} FROM entries WHERE id = ?"
SELECT_PERSON_ENTRIES = f"""
SELECT {ENTRY_COLUMNS} FROM entries WHERE person_id = ? ORDER BY performed_at DESC, id DESC
"""
SELECT_GROUP_ENTRIES = """
SELECT e.id, m.id AS participant_id, e.performed_at, e.distance_tenths, e.place, e.created_at, e.style, e.conditions
FROM entries e JOIN participants m ON m.person_id = e.person_id
WHERE m.group_id = ? ORDER BY e.performed_at DESC, e.id DESC
"""


class SqliteSkiRepository:
    def __init__(self, path: str) -> None:
        self._lock = threading.Lock()
        self._connection = sqlite3.connect(path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._prepare()

    def add_group(self, name: str) -> Group:
        return Group(self._insert(INSERT_GROUP, (name,)), name)

    def rename_group(self, group_id: int, name: str) -> Group:
        self._ensure_changed(UPDATE_GROUP, (name, group_id), "group_not_found")
        return Group(group_id, name)

    def delete_group(self, group_id: int) -> None:
        try:
            self._ensure_changed(DELETE_GROUP, (group_id,), "group_not_found")
        except sqlite3.IntegrityError:
            raise RuleError("group_not_empty") from None

    def list_groups(self) -> list[Group]:
        return [group_from(row) for row in self._rows(SELECT_GROUPS)]

    def get_group(self, group_id: int) -> Group | None:
        return _first(self._rows(SELECT_GROUP, (group_id,)), group_from)

    def count_participants(self, group_id: int) -> int:
        return self._count(COUNT_PARTICIPANTS, (group_id,))

    def count_entries(self, group_id: int) -> int:
        return self._count(COUNT_ENTRIES, (group_id,))

    def add_participant(self, group_id: int, given_name: str, family_name: str, token: str) -> Participant:
        person_id = self._insert(INSERT_PERSON, (given_name, family_name, token))
        return self._membership(group_id, person_id)

    def add_membership(self, group_id: int, person_id: int) -> Participant:
        self._person(person_id)
        return self._membership(group_id, person_id)

    def list_persons(self) -> list[Person]:
        return [person_from(row) for row in self._rows(SELECT_PERSONS)]

    def get_person_by_token(self, token: str) -> Person | None:
        return _first(self._rows(SELECT_PERSON_TOKEN, (token,)), person_from)

    def list_memberships(self, person_id: int) -> list[Participant]:
        rows = self._rows(SELECT_MEMBERSHIPS, (person_id,))
        return [participant_from(row) for row in rows]

    def rename_participant(self, participant_id: int, given_name: str, family_name: str) -> Participant:
        person_id = self._participant(participant_id).person_id
        self._ensure_changed(UPDATE_PERSON, (given_name, family_name, person_id), "participant_not_found")
        return self._participant(participant_id)

    def set_birth_year(self, person_id: int, year: int | None) -> None:
        self._ensure_changed(UPDATE_BIRTH, (year, person_id), "participant_not_found")

    def get_goal(self, person_id: int, season: int) -> SeasonGoal | None:
        return _first(self._rows(SELECT_GOAL, (person_id, season)), goal_from)

    def save_goal(self, goal: SeasonGoal) -> None:
        self._change(UPSERT_GOAL, goal_params(goal))

    def delete_participant(self, participant_id: int) -> None:
        person_id = self._participant(participant_id).person_id
        self._ensure_changed(DELETE_MEMBERSHIP, (participant_id,), "participant_not_found")
        self._drop_person_without_groups(person_id)

    def list_participants(self, group_id: int) -> list[Participant]:
        rows = self._rows(SELECT_PARTICIPANTS, (group_id,))
        return [participant_from(row) for row in rows]

    def get_participant(self, participant_id: int) -> Participant | None:
        return _first(self._rows(SELECT_PARTICIPANT, (participant_id,)), participant_from)

    def replace_token(self, participant_id: int, token: str) -> Participant:
        person_id = self._participant(participant_id).person_id
        self._ensure_changed(UPDATE_TOKEN, (token, person_id), "participant_not_found")
        return self._participant(participant_id)

    def add_entry(self, person_id: int, performed_at: datetime, distance_tenths: int, place, created_at, style="free", conditions="normal") -> Entry:
        params = entry_params(person_id, performed_at, distance_tenths, place, created_at, style, conditions)
        row_id = self._insert(INSERT_ENTRY, params)
        return new_entry(row_id, person_id, performed_at, distance_tenths, place, created_at, style, conditions)

    def update_entry(self, entry_id: int, performed_at: datetime, distance_tenths: int, place, style="free", conditions="normal") -> Entry:
        params = (dump_time(performed_at), distance_tenths, place, style, conditions, entry_id)
        self._ensure_changed(UPDATE_ENTRY, params, "entry_not_found")
        return self._entry(entry_id)

    def delete_entry(self, entry_id: int) -> None:
        self._ensure_changed(DELETE_ENTRY, (entry_id,), "entry_not_found")

    def get_entry(self, entry_id: int) -> Entry | None:
        return _first(self._rows(SELECT_ENTRY, (entry_id,)), entry_from)

    def list_entries_for_person(self, person_id: int) -> list[Entry]:
        rows = self._rows(SELECT_PERSON_ENTRIES, (person_id,))
        return [entry_from(row) for row in rows]

    def list_entries_for_group(self, group_id: int) -> list[Entry]:
        return [entry_from(row) for row in self._rows(SELECT_GROUP_ENTRIES, (group_id,))]

    def _prepare(self) -> None:
        self._connection.execute("PRAGMA foreign_keys = ON")
        upgrade_if_legacy(self._connection)
        upgrade_shape(self._connection)
        self._connection.executescript(SCHEMA)

    def _membership(self, group_id: int, person_id: int) -> Participant:
        try:
            row_id = self._insert(INSERT_MEMBERSHIP, (group_id, person_id))
        except sqlite3.IntegrityError:
            raise RuleError("already_member") from None
        return self._participant(row_id)

    def _drop_person_without_groups(self, person_id: int) -> None:
        if self._count(COUNT_MEMBERSHIPS, (person_id,)) == 0:
            self._change(DELETE_PERSON, (person_id,))

    def _person(self, person_id: int) -> Person:
        person = _first(self._rows(SELECT_PERSON, (person_id,)), person_from)
        if person is None:
            raise RuleError("participant_not_found")
        return person

    def _participant(self, participant_id: int) -> Participant:
        participant = self.get_participant(participant_id)
        if participant is None:
            raise RuleError("participant_not_found")
        return participant

    def _entry(self, entry_id: int) -> Entry:
        entry = self.get_entry(entry_id)
        if entry is None:
            raise RuleError("entry_not_found")
        return entry

    def _ensure_changed(self, sql: str, params: tuple, missing_code: str) -> None:
        if self._change(sql, params) == 0:
            raise RuleError(missing_code)

    def _insert(self, sql: str, params: tuple) -> int:
        row_id, _changed = self._run(sql, params)
        return row_id

    def _change(self, sql: str, params: tuple) -> int:
        _row_id, changed = self._run(sql, params)
        return changed

    def _run(self, sql: str, params: tuple) -> tuple[int, int]:
        with self._lock:
            try:
                cursor = self._connection.execute(sql, params)
            except sqlite3.IntegrityError:
                self._connection.rollback()
                raise
            outcome = (int(cursor.lastrowid or 0), cursor.rowcount)
            self._connection.commit()
            return outcome

    def _count(self, sql: str, params: tuple) -> int:
        return int(self._rows(sql, params)[0]["total"])

    def _rows(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._lock:
            return list(self._connection.execute(sql, params))


def _first(rows: list[sqlite3.Row], build):
    if not rows:
        return None
    return build(rows[0])
