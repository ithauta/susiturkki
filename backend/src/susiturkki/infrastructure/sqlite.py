import sqlite3
import threading
from datetime import datetime

from susiturkki.domain.errors import RuleError
from susiturkki.domain.models import Entry, Group, Participant
from susiturkki.infrastructure.sqlite_rows import (
    dump_time,
    entry_from,
    entry_params,
    group_from,
    new_entry,
    participant_from,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id),
    name TEXT NOT NULL,
    token TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    participant_id INTEGER NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
    performed_at TEXT NOT NULL,
    distance_tenths INTEGER NOT NULL,
    place TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS entries_participant ON entries(participant_id);
"""

SELECT_GROUPS = "SELECT id, name FROM groups ORDER BY name, id"
SELECT_GROUP = "SELECT id, name FROM groups WHERE id = ?"
INSERT_GROUP = "INSERT INTO groups (name) VALUES (?)"
UPDATE_GROUP = "UPDATE groups SET name = ? WHERE id = ?"
DELETE_GROUP = "DELETE FROM groups WHERE id = ?"
COUNT_PARTICIPANTS = "SELECT COUNT(*) AS total FROM participants WHERE group_id = ?"
COUNT_ENTRIES = """
SELECT COUNT(*) AS total FROM entries e
JOIN participants p ON p.id = e.participant_id
WHERE p.group_id = ?
"""
SELECT_PARTICIPANTS = """
SELECT id, group_id, name, token FROM participants
WHERE group_id = ? ORDER BY name, id
"""
SELECT_PARTICIPANT = "SELECT id, group_id, name, token FROM participants WHERE id = ?"
SELECT_PARTICIPANT_TOKEN = "SELECT id, group_id, name, token FROM participants WHERE token = ?"
INSERT_PARTICIPANT = "INSERT INTO participants (group_id, name, token) VALUES (?, ?, ?)"
UPDATE_PARTICIPANT = "UPDATE participants SET name = ? WHERE id = ?"
UPDATE_TOKEN = "UPDATE participants SET token = ? WHERE id = ?"
DELETE_PARTICIPANT = "DELETE FROM participants WHERE id = ?"
INSERT_ENTRY = """
INSERT INTO entries (participant_id, performed_at, distance_tenths, place, created_at)
VALUES (?, ?, ?, ?, ?)
"""
UPDATE_ENTRY = """
UPDATE entries SET performed_at = ?, distance_tenths = ?, place = ? WHERE id = ?
"""
DELETE_ENTRY = "DELETE FROM entries WHERE id = ?"
SELECT_ENTRY = """
SELECT id, participant_id, performed_at, distance_tenths, place, created_at
FROM entries WHERE id = ?
"""
SELECT_PARTICIPANT_ENTRIES = """
SELECT id, participant_id, performed_at, distance_tenths, place, created_at
FROM entries WHERE participant_id = ? ORDER BY performed_at DESC, id DESC
"""
SELECT_GROUP_ENTRIES = """
SELECT e.id, e.participant_id, e.performed_at, e.distance_tenths, e.place, e.created_at
FROM entries e JOIN participants p ON p.id = e.participant_id
WHERE p.group_id = ? ORDER BY e.performed_at DESC, e.id DESC
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

    def add_participant(self, group_id: int, name: str, token: str) -> Participant:
        row_id = self._insert(INSERT_PARTICIPANT, (group_id, name, token))
        return Participant(row_id, group_id, name, token)

    def rename_participant(self, participant_id: int, name: str) -> Participant:
        self._ensure_changed(UPDATE_PARTICIPANT, (name, participant_id), "participant_not_found")
        return self._participant(participant_id)

    def delete_participant(self, participant_id: int) -> None:
        self._ensure_changed(DELETE_PARTICIPANT, (participant_id,), "participant_not_found")

    def list_participants(self, group_id: int) -> list[Participant]:
        rows = self._rows(SELECT_PARTICIPANTS, (group_id,))
        return [participant_from(row) for row in rows]

    def get_participant(self, participant_id: int) -> Participant | None:
        return _first(self._rows(SELECT_PARTICIPANT, (participant_id,)), participant_from)

    def get_participant_by_token(self, token: str) -> Participant | None:
        rows = self._rows(SELECT_PARTICIPANT_TOKEN, (token,))
        return _first(rows, participant_from)

    def replace_token(self, participant_id: int, token: str) -> Participant:
        self._ensure_changed(UPDATE_TOKEN, (token, participant_id), "participant_not_found")
        return self._participant(participant_id)

    def add_entry(self, participant_id: int, performed_at: datetime, distance_tenths: int, place, created_at) -> Entry:
        params = entry_params(participant_id, performed_at, distance_tenths, place, created_at)
        row_id = self._insert(INSERT_ENTRY, params)
        return new_entry(row_id, participant_id, performed_at, distance_tenths, place, created_at)

    def update_entry(self, entry_id: int, performed_at: datetime, distance_tenths: int, place) -> Entry:
        params = (dump_time(performed_at), distance_tenths, place, entry_id)
        self._ensure_changed(UPDATE_ENTRY, params, "entry_not_found")
        return self._entry(entry_id)

    def delete_entry(self, entry_id: int) -> None:
        self._ensure_changed(DELETE_ENTRY, (entry_id,), "entry_not_found")

    def get_entry(self, entry_id: int) -> Entry | None:
        return _first(self._rows(SELECT_ENTRY, (entry_id,)), entry_from)

    def list_entries_for_participant(self, participant_id: int) -> list[Entry]:
        rows = self._rows(SELECT_PARTICIPANT_ENTRIES, (participant_id,))
        return [entry_from(row) for row in rows]

    def list_entries_for_group(self, group_id: int) -> list[Entry]:
        return [entry_from(row) for row in self._rows(SELECT_GROUP_ENTRIES, (group_id,))]

    def _prepare(self) -> None:
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._connection.executescript(SCHEMA)

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
            cursor = self._connection.execute(sql, params)
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
