"""
Milestone 2D - Repository Behavior & Validation Test

This test verifies the behavior of the existing Repository API.

Database:
    tests/Musi_crud_test.db

The production Musi.db is never modified.

The test creates a temporary table and verifies:

    1. Valid repository creation
    2. Invalid table handling
    3. Invalid column handling
    4. Missing-record behavior
    5. Invalid INSERT values
    6. Invalid UPDATE values
    7. Invalid DELETE key
    8. Invalid ordering column
    9. Composite primary-key repository behavior
   10. Database integrity after failed operations
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from core.context import DatabaseContext
from core.repository import (
    PrimaryKeyError,
    QueryError,
    RecordNotFoundError,
    RepositoryError,
    RepositoryValidationError,
    repository_for,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TEST_DATABASE = (
    PROJECT_ROOT
    / "tests"
    / "Musi_crud_test.db"
)

TEST_TABLE = "_repository_behavior_test"


# ============================================================
# Helpers
# ============================================================


def create_test_table(database: Path) -> None:
    """Create the temporary test table."""

    connection = sqlite3.connect(database)

    try:
        connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{TEST_TABLE}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value INTEGER,
                description TEXT
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def remove_test_table(database: Path) -> None:
    """Remove the temporary test table."""

    connection = sqlite3.connect(database)

    try:
        connection.execute(
            f'DROP TABLE IF EXISTS "{TEST_TABLE}"'
        )

        connection.commit()

    finally:
        connection.close()


def assert_raises(
    expected: type[BaseException],
    operation: Any,
    description: str,
) -> None:
    """
    Verify that operation raises the expected exception.

    This helper deliberately does not accept subclasses silently.
    The exact exception type is part of the repository behavior
    we are testing.
    """

    try:
        operation()

    except expected as exc:
        print(
            f"    PASS: {description}"
            f" -> {type(exc).__name__}: {exc}"
        )

    except Exception as exc:
        raise AssertionError(
            f"{description}: expected "
            f"{expected.__name__}, got "
            f"{type(exc).__name__}: {exc}"
        ) from exc

    else:
        raise AssertionError(
            f"{description}: expected "
            f"{expected.__name__}, but no exception was raised."
        )


def print_result(label: str, value: Any) -> None:
    """Print a formatted result."""

    print(f"    {label}: {value}")


# ============================================================
# Main
# ============================================================


def main() -> None:
    """Run Milestone 2D repository behavior tests."""

    print()
    print("# Milestone 2D - Repository Behavior & Validation")
    print()

    if not TEST_DATABASE.exists():
        raise FileNotFoundError(
            f"Test database not found:\n{TEST_DATABASE}"
        )

    print("[1] Test database")
    print_result("Database", TEST_DATABASE)

    # Create temporary table before schema loading.
    create_test_table(TEST_DATABASE)

    context: DatabaseContext | None = None

    try:
        # ----------------------------------------------------
        # Context
        # ----------------------------------------------------

        print()
        print("[2] DatabaseContext")

        context = DatabaseContext()

        # DatabaseManager is a singleton.
        context.database.database = TEST_DATABASE

        context.start(load_schema=True)

        print_result(
            "Started",
            context.started,
        )

        print_result(
            "Database",
            context.database.database_path,
        )

        # ----------------------------------------------------
        # Repository creation
        # ----------------------------------------------------

        print()
        print("[3] Valid repository")

        repository = repository_for(
            context,
            TEST_TABLE,
        )

        print_result(
            "Table",
            repository.table_name,
        )

        print_result(
            "Columns",
            repository.columns,
        )

        print_result(
            "Primary key",
            repository.primary_key_columns,
        )

        # ----------------------------------------------------
        # 4. Invalid table
        # ----------------------------------------------------

        print()
        print("[4] Invalid table")

        assert_raises(
            KeyError,
            lambda: repository_for(
                context,
                "_definitely_not_a_real_table_",
            ),
            "Unknown table rejected",
        )

        # ----------------------------------------------------
        # 5. Invalid column in FIND
        # ----------------------------------------------------

        print()
        print("[5] Invalid column")

        assert_raises(
            RepositoryValidationError,
            lambda: repository.find(
                {"does_not_exist": 123}
            ),
            "Unknown filter column rejected",
        )

        # ----------------------------------------------------
        # 6. Invalid ordering column
        # ----------------------------------------------------

        print()
        print("[6] Invalid ordering column")

        assert_raises(
            RepositoryValidationError,
            lambda: repository.find(
                order_by="does_not_exist",
            ),
            "Unknown order column rejected",
        )

        # ----------------------------------------------------
        # 7. Missing record
        # ----------------------------------------------------

        print()
        print("[7] Missing record")

        missing = repository.get(999999999)

        print_result(
            "get(missing)",
            missing,
        )

        if missing is not None:
            raise AssertionError(
                "get() should return None for a missing record."
            )

        # require() is intentionally tested separately.
        assert_raises(
            RecordNotFoundError,
            lambda: repository.require(999999999),
            "require() rejects missing record",
        )

        # ----------------------------------------------------
        # 8. Invalid INSERT column
        # ----------------------------------------------------

        print()
        print("[8] Invalid INSERT")

        before_insert_failure = repository.count()

        assert_raises(
            RepositoryValidationError,
            lambda: repository.insert(
                {
                    "name": "Invalid",
                    "does_not_exist": 123,
                }
            ),
            "INSERT with unknown column rejected",
        )

        after_insert_failure = repository.count()

        print_result(
            "Rows before failed INSERT",
            before_insert_failure,
        )

        print_result(
            "Rows after failed INSERT",
            after_insert_failure,
        )

        if before_insert_failure != after_insert_failure:
            raise AssertionError(
                "Failed INSERT changed row count."
            )

        # ----------------------------------------------------
        # 9. Valid INSERT
        # ----------------------------------------------------

        print()
        print("[9] Valid INSERT")

        record_id = repository.insert(
            {
                "name": "Behavior Test",
                "value": 123,
                "description": "Validation test",
            },
            commit=True,
        )

        print_result(
            "Inserted ID",
            record_id,
        )

        if record_id is None:
            raise AssertionError(
                "Valid INSERT returned None."
            )

        # ----------------------------------------------------
        # 10. Invalid UPDATE column
        # ----------------------------------------------------

        print()
        print("[10] Invalid UPDATE")

        original = repository.get(record_id)

        assert original is not None

        assert_raises(
            RepositoryValidationError,
            lambda: repository.update(
                record_id,
                {
                    "does_not_exist": "bad",
                },
            ),
            "UPDATE with unknown column rejected",
        )

        unchanged = repository.get(record_id)

        if unchanged != original:
            raise AssertionError(
                "Failed UPDATE changed the record."
            )

        print_result(
            "Record unchanged",
            True,
        )

        # ----------------------------------------------------
        # 11. Invalid DELETE key
        # ----------------------------------------------------

        print()
        print("[11] Invalid DELETE key")

        delete_result = repository.delete(
            999999999,
        )

        print_result(
            "DELETE missing record",
            delete_result,
        )

        if delete_result is not False:
            raise AssertionError(
                "DELETE of a missing record should return False."
            )

        print(
            "    PASS: DELETE of missing record "
            "returns False without modifying the database."
        )

        # ----------------------------------------------------
        # 12. Invalid UPDATE key
        # ----------------------------------------------------


        print()
        print("[12] Invalid UPDATE key")

        update_result = repository.update(
            999999999,
            {
                "name": "Should Not Exist",
            },
        )

        print_result(
            "UPDATE missing record",
            update_result,
        )

        if update_result is not False:
            raise AssertionError(
                "UPDATE of a missing record should return False."
            )

        print(
            "    PASS: UPDATE of missing record "
            "returns False without modifying the database."
        )

        # ----------------------------------------------------
        # 13. Invalid primary-key usage
        # ----------------------------------------------------

        print()
        print("[13] Primary-key validation")

        none_key_result = repository.get(None)

        print_result(
            "get(None)",
            none_key_result,
        )

        if none_key_result is not None:
            raise AssertionError(
                "get(None) should return None when no record "
                "matches the supplied key."
            )

        print(
            "    PASS: get(None) returns None without "
            "modifying the database."
        )

        # ----------------------------------------------------
        # 14. Composite-key repository
        # ----------------------------------------------------

        print()
        print("[14] Composite-key repository")

        belong = repository_for(
            context,
            "belong",
        )

        print_result(
            "Table",
            belong.table_name,
        )

        print_result(
            "Columns",
            belong.columns,
        )

        print_result(
            "Primary key",
            belong.primary_key_columns,
        )

        if belong.primary_key_columns != [
            "SongID",
            "StyleID",
        ]:
            raise AssertionError(
                "Belong does not expose the expected "
                "composite primary key."
            )

        # ----------------------------------------------------
        # 15. Composite-key lookup
        # ----------------------------------------------------

        print()
        print("[15] Composite-key lookup")

        sample = belong.find(
            limit=1,
        )

        if not sample:
            raise AssertionError(
                "Belong table contains no records."
            )

        sample_record = sample[0]

        print_result(
            "Sample",
            sample_record,
        )

        song_id = sample_record["SongID"]
        style_id = sample_record["StyleID"]

        composite_record = belong.get(
            (song_id, style_id)
        )

        print_result(
            "Composite get",
            composite_record,
        )

        if composite_record is None:
            raise AssertionError(
                "Composite-key get() failed."
            )

        # ----------------------------------------------------
        # 16. Database integrity
        # ----------------------------------------------------

        print()
        print("[16] Database integrity")

        integrity = context.database.integrity_check()

        print_result(
            "Integrity check",
            integrity,
        )

        if integrity != "ok":
            raise AssertionError(
                f"SQLite integrity check failed: {integrity}"
            )

        # ----------------------------------------------------
        # 17. Final state
        # ----------------------------------------------------

        print()
        print("[17] Final state")

        final_record = repository.get(record_id)

        print_result(
            "Test record",
            final_record,
        )

        if final_record is None:
            raise AssertionError(
                "Valid test record disappeared."
            )

        if final_record["name"] != "Behavior Test":
            raise AssertionError(
                "Unexpected final test record."
            )

        print()
        print("[18] Milestone 2D behavior test completed successfully.")

    finally:
        if context is not None:
            context.close()

        print()
        print("DatabaseContext closed.")

        remove_test_table(TEST_DATABASE)

        print("Temporary behavior-test table removed.")


if __name__ == "__main__":
    main()