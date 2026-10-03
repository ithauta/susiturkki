"""Vanha tietokanta, jossa jäsenyydellä oli oma nimi ja linkki, siirretään henkilöiksi."""

REWRITE = """
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    token TEXT NOT NULL UNIQUE
);
INSERT INTO persons (id, name, token)
SELECT id, name, token FROM participants;
CREATE TABLE memberships (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id),
    person_id INTEGER NOT NULL REFERENCES persons(id),
    UNIQUE (group_id, person_id)
);
INSERT INTO memberships (id, group_id, person_id)
SELECT id, group_id, id FROM participants;
CREATE TABLE entries_next (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
    performed_at TEXT NOT NULL,
    distance_tenths INTEGER NOT NULL,
    place TEXT,
    created_at TEXT NOT NULL
);
INSERT INTO entries_next (id, person_id, performed_at, distance_tenths, place, created_at)
SELECT id, participant_id, performed_at, distance_tenths, place, created_at FROM entries;
DROP TABLE entries;
DROP TABLE participants;
ALTER TABLE memberships RENAME TO participants;
ALTER TABLE entries_next RENAME TO entries;
"""


def upgrade_if_legacy(connection) -> None:
    if _legacy_participants(connection):
        _rewrite(connection)


def _legacy_participants(connection) -> bool:
    if not _has_table(connection, "participants"):
        return False
    return _has_column(connection, "participants", "name")


def _rewrite(connection) -> None:
    connection.execute("PRAGMA foreign_keys = OFF")
    connection.executescript(REWRITE)
    connection.execute("PRAGMA foreign_keys = ON")


def _has_table(connection, name: str) -> bool:
    rows = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?", (name,))
    return rows.fetchone() is not None


def _has_column(connection, table: str, column: str) -> bool:
    rows = connection.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in rows)
