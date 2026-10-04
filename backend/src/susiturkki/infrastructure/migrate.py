"""Vanhat tietokannat siirretään henkilöiksi ja nykyiseen sarakemalliin."""

from susiturkki.domain.name import split_name

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


def upgrade_shape(connection) -> None:
    _split_person_names(connection)
    _add_entry_choices(connection)
    connection.commit()


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


def _split_person_names(connection) -> None:
    if not _has_column(connection, "persons", "name"):
        return
    _add_name_columns(connection)
    _copy_names(connection)
    connection.execute("ALTER TABLE persons DROP COLUMN name")


def _add_name_columns(connection) -> None:
    if _has_column(connection, "persons", "given_name"):
        return
    connection.execute("ALTER TABLE persons ADD COLUMN given_name TEXT NOT NULL DEFAULT ''")
    connection.execute("ALTER TABLE persons ADD COLUMN family_name TEXT NOT NULL DEFAULT ''")
    connection.execute("ALTER TABLE persons ADD COLUMN birth_year INTEGER")


def _copy_names(connection) -> None:
    for row in connection.execute("SELECT id, name FROM persons"):
        _store_split(connection, row)


def _store_split(connection, row) -> None:
    given, family = split_name(row["name"])
    connection.execute("UPDATE persons SET given_name = ?, family_name = ? WHERE id = ?", (given, family, row["id"]))


def _add_entry_choices(connection) -> None:
    if not _has_table(connection, "entries") or _has_column(connection, "entries", "style"):
        return
    connection.execute("ALTER TABLE entries ADD COLUMN style TEXT NOT NULL DEFAULT 'free'")
    connection.execute("ALTER TABLE entries ADD COLUMN conditions TEXT NOT NULL DEFAULT 'normal'")


def _has_table(connection, name: str) -> bool:
    rows = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?", (name,))
    return rows.fetchone() is not None


def _has_column(connection, table: str, column: str) -> bool:
    rows = connection.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in rows)
