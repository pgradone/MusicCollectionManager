# ====================================================
# Milestone 2F test script test_repository_composite_keys.py
#   by CharGpt fgradone
# ====================================================

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.context import DatabaseContext
from core.database import QueryError
from core.repository import PrimaryKeyError, repository_for


ROOT_DIR = Path(__file__).resolve().parents[1]
TEST_DATABASE = ROOT_DIR / "tests" / "Musi_crud_test.db"


def show(label: str, value: Any) -> None:
    print(f"    {label}: {value}")


def equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(
            f"{message}: expected {expected!r}, got {actual!r}"
        )


def true(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def raises(expected: type[BaseException], operation: Any, description: str) -> None:
    try:
        operation()
    except expected as exc:
        print(f"    PASS: {description} -> {type(exc).__name__}: {exc}")
    except Exception as exc:
        raise AssertionError(
            f"{description}: expected {expected.__name__}, "
            f"got {type(exc).__name__}: {exc}"
        ) from exc
    else:
        raise AssertionError(
            f"{description}: expected {expected.__name__}, "
            "but no exception was raised."
        )


def ids(repository: Any, column: str, limit: int = 50) -> list[Any]:
    rows = repository.find(order_by=column, limit=limit)
    values = [row[column] for row in rows if row[column] is not None]
    if not values:
        raise AssertionError(
            f"No usable {column} values in {repository.table_name}."
        )
    return values


def unused_pair(
    repository: Any,
    left_column: str,
    left_values: list[Any],
    right_column: str,
    right_values: list[Any],
) -> tuple[Any, Any]:
    existing = {
        (row[left_column], row[right_column])
        for row in repository.find()
    }
    for left in left_values:
        for right in right_values:
            if (left, right) not in existing:
                return left, right
    raise AssertionError(
        f"Could not find an unused ({left_column}, {right_column}) pair."
    )


def main() -> None:
    print()
    print("# Milestone 2F - Composite-key CRUD and Foreign-key Behavior")
    print()

    if not TEST_DATABASE.exists():
        raise FileNotFoundError(f"Test database not found:\n{TEST_DATABASE}")

    show("Database", TEST_DATABASE)

    context: DatabaseContext | None = None

    try:
        print("\n[1] DatabaseContext")
        context = DatabaseContext()
        context.database.database = TEST_DATABASE
        context.start(load_schema=True)
        show("Started", context.started)
        show("Database", context.database.database_path)

        print("\n[2] Foreign-key enforcement")
        fk_state = context.database.fetchone("PRAGMA foreign_keys")
        assert fk_state is not None
        show("PRAGMA foreign_keys", int(fk_state[0]))
        equal(int(fk_state[0]), 1, "Foreign-key enforcement")

        print("\n[3] Association repositories")
        belong = repository_for(context, "Belong")
        contain = repository_for(context, "Contain")
        sing = repository_for(context, "Sing")

        show("Belong PK", belong.primary_key_columns)
        show("Contain PK", contain.primary_key_columns)
        show("Sing PK", sing.primary_key_columns)

        equal(belong.primary_key_columns, ["SongID", "StyleID"],
              "Belong composite primary key")
        equal(contain.primary_key_columns, ["RecordID", "SongID"],
              "Contain composite primary key")
        equal(sing.primary_key_columns, ["ArtistID", "SongID"],
              "Sing composite primary key")

        print("\n[4] Parent records")
        songs = repository_for(context, "Songs")
        styles = repository_for(context, "Styles")
        records = repository_for(context, "Records")
        artists = repository_for(context, "Artists")

        song_ids = ids(songs, "SongID")
        style_ids = ids(styles, "StyleID")
        record_ids = ids(records, "RecordID")
        artist_ids = ids(artists, "ArtistID")

        show("Song IDs available", len(song_ids))
        show("Style IDs available", len(style_ids))
        show("Record IDs available", len(record_ids))
        show("Artist IDs available", len(artist_ids))

        print("\n[5] Belong - INSERT / GET")
        belong_pair = unused_pair(
            belong, "SongID", song_ids, "StyleID", style_ids
        )
        show("New key", belong_pair)
        belong.insert(
            {"SongID": belong_pair[0], "StyleID": belong_pair[1]},
            commit=True,
        )
        row = belong.get(belong_pair)
        show("Retrieved row", row)
        true(row is not None, "Belong INSERT should be retrievable")
        print(
            "    PASS: Belong has no non-PK columns, so UPDATE is not "
            "meaningful without changing its composite key."
        )
        true(belong.delete(belong_pair, commit=True),
             "Belong DELETE should succeed")
        equal(belong.get(belong_pair), None,
              "Deleted Belong row should be absent")

        print("\n[6] Sing - INSERT / GET / DELETE")
        sing_pair = unused_pair(
            sing, "ArtistID", artist_ids, "SongID", song_ids
        )
        sing.insert(
            {"ArtistID": sing_pair[0], "SongID": sing_pair[1]},
            commit=True,
        )
        row = sing.get(sing_pair)
        show("Retrieved row", row)
        true(row is not None, "Sing INSERT should be retrievable")
        true(sing.delete(sing_pair, commit=True),
             "Sing DELETE should succeed")
        equal(sing.get(sing_pair), None,
              "Deleted Sing row should be absent")

        print("\n[7] Contain - INSERT / GET")
        contain_pair = unused_pair(
            contain, "RecordID", record_ids, "SongID", song_ids
        )
        contain.insert(
            {
                "RecordID": contain_pair[0],
                "SongID": contain_pair[1],
                "Position": "2F-Test",
            },
            commit=True,
        )
        row = contain.get(contain_pair)
        show("Retrieved row", row)
        true(row is not None, "Contain INSERT should be retrievable")
        if row is not None:
            equal(row["Position"], "2F-Test",
                  "Contain Position after INSERT")

        print("\n[8] Contain - UPDATE")
        true(
            contain.update(
                contain_pair,
                {"Position": "2F-Updated"},
                commit=True,
            ),
            "Contain UPDATE should succeed",
        )
        row = contain.get(contain_pair)
        show("Updated row", row)
        true(row is not None, "Updated Contain row should exist")
        if row is not None:
            equal(row["Position"], "2F-Updated",
                  "Contain Position after UPDATE")

        print("\n[9] Contain - DELETE")
        true(contain.delete(contain_pair, commit=True),
             "Contain DELETE should succeed")
        equal(contain.get(contain_pair), None,
              "Deleted Contain row should be absent")

        print("\n[10] Invalid composite keys")
        raises(
            PrimaryKeyError,
            lambda: belong.get((belong_pair[0],)),
            "Belong rejects incomplete composite key",
        )
        raises(
            PrimaryKeyError,
            lambda: contain.get(
                (contain_pair[0], contain_pair[1], "extra")
            ),
            "Contain rejects oversized composite key",
        )
        raises(
            PrimaryKeyError,
            lambda: sing.get(None),
            "Sing rejects None composite key",
        )

        print("\n[11] Foreign-key behavior")
        invalid_song = -900000001
        invalid_style = -900000002
        invalid_record = -900000003
        invalid_artist = -900000004

        raises(
            QueryError,
            lambda: belong.insert(
                {"SongID": invalid_song, "StyleID": style_ids[0]}
            ),
            "Belong rejects unknown SongID",
        )
        context.database.rollback()

        raises(
            QueryError,
            lambda: belong.insert(
                {"SongID": song_ids[0], "StyleID": invalid_style}
            ),
            "Belong rejects unknown StyleID",
        )
        context.database.rollback()

        raises(
            QueryError,
            lambda: sing.insert(
                {"ArtistID": invalid_artist, "SongID": song_ids[0]}
            ),
            "Sing rejects unknown ArtistID",
        )
        context.database.rollback()

        raises(
            QueryError,
            lambda: contain.insert(
                {
                    "RecordID": invalid_record,
                    "SongID": song_ids[0],
                    "Position": "FK-Test",
                }
            ),
            "Contain rejects unknown RecordID",
        )
        context.database.rollback()

        print(
            "    INFO: Contain.SongID has no declared SQLite FK in the "
            "existing schema; no FK assertion is made for it."
        )

        print("\n[12] Database integrity")
        integrity = context.database.integrity_check()
        show("Integrity check", integrity)
        equal(integrity, "ok", "SQLite integrity check")

        print("\n[13] Foreign-key integrity")
        violations = context.database.fetchall("PRAGMA foreign_key_check")
        show("Foreign-key violations", len(violations))
        equal(len(violations), 0, "Foreign-key violations")

        print("\n[14] Final state")
        equal(belong.get(belong_pair), None,
              "Belong test row must be absent")
        equal(sing.get(sing_pair), None,
              "Sing test row must be absent")
        equal(contain.get(contain_pair), None,
              "Contain test row must be absent")
        print("    PASS: All temporary composite-key rows removed.")

        print("\n[15] Milestone 2F completed successfully.")

    finally:
        if context is not None:
            context.close()
        print("\nDatabaseContext closed.")


if __name__ == "__main__":
    main()
