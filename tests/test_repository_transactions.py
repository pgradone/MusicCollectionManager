"""
Milestone 2E - Repository Transaction Semantics

Tests transaction and commit behavior of Repository.

The production database Musi.db is never used.

Test database:
    tests/Musi_crud_test.db
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from core.context import DatabaseContext
from core.repository import repository_for


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TEST_DATABASE = (
    PROJECT_ROOT
    / "tests"
    / "Musi_crud_test.db"
)

TEST_TABLE = "_repository_transaction_test"


def create_test_table(database: Path) -> None:
    """Create the temporary transaction test table."""

    connection = sqlite3.connect(database)

    try:
        connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{TEST_TABLE}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value INTEGER
            )
            """
        )

        connection.commit()

    finally:
        connection.close()


def remove_test_table(database: Path) -> None:
    """Remove the temporary transaction test table."""

    connection = sqlite3.connect(database)

    try:
        connection.execute(
            f'DROP TABLE IF EXISTS "{TEST_TABLE}"'
        )

        connection.commit()

    finally:
        connection.close()


def print_result(label: str, value: Any) -> None:
    """Print a formatted result."""

    print(f"    {label}: {value}")


def main() -> None:
    """Run Milestone 2E."""

    print()
    print("# Milestone 2E - Repository Transaction Semantics")
    print()

    if not TEST_DATABASE.exists():
        raise FileNotFoundError(
            f"Test database not found:\n{TEST_DATABASE}"
        )

    print("[1] Test database")
    print_result("Database", TEST_DATABASE)

    create_test_table(TEST_DATABASE)

    context: DatabaseContext | None = None

    try:
        print()
        print("[2] DatabaseContext")

        context = DatabaseContext()

        # The DatabaseManager is a singleton, so explicitly
        # point it at the CRUD test database.
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

        print()
        print("[3] Repository")

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

        # ====================================================
        # 4. Initial state
        # ====================================================

        print()
        print("[4] Initial state")

        initial_count = repository.count()

        print_result(
            "Row count",
            initial_count,
        )

        if initial_count != 0:
            raise AssertionError(
                "Transaction test table is not empty."
            )

        # ====================================================
        # 5. INSERT without commit
        # ====================================================

        print()
        print("[5] INSERT commit=False")

        record_id = repository.insert(
            {
                "name": "Uncommitted Insert",
                "value": 100,
            },
            commit=False,
        )

        print_result(
            "Inserted ID",
            record_id,
        )

        visible = repository.get(record_id)

        print_result(
            "Visible before commit",
            visible,
        )

        if visible is None:
            raise AssertionError(
                "Inserted record is not visible "
                "inside the active connection."
            )

        # ====================================================
        # 6. Explicit rollback
        # ====================================================

        print()
        print("[6] Explicit rollback")

        context.database.rollback()

        rolled_back = repository.get(record_id)

        print_result(
            "Record after rollback",
            rolled_back,
        )

        if rolled_back is not None:
            raise AssertionError(
                "commit=False INSERT survived rollback."
            )

        # ====================================================
        # 7. INSERT with commit
        # ====================================================

        print()
        print("[7] INSERT commit=True")

        committed_id = repository.insert(
            {
                "name": "Committed Insert",
                "value": 200,
            },
            commit=True,
        )

        print_result(
            "Inserted ID",
            committed_id,
        )

        committed_record = repository.get(
            committed_id
        )

        print_result(
            "Record after commit",
            committed_record,
        )

        if committed_record is None:
            raise AssertionError(
                "commit=True INSERT was not persisted."
            )

        # ====================================================
        # 8. UPDATE without commit
        # ====================================================

        print()
        print("[8] UPDATE commit=False")

        update_result = repository.update(
            committed_id,
            {
                "value": 300,
            },
            commit=False,
        )

        print_result(
            "Update result",
            update_result,
        )

        if update_result is not True:
            raise AssertionError(
                "Expected UPDATE to return True."
            )

        updated = repository.get(
            committed_id
        )

        print_result(
            "Updated value before rollback",
            updated,
        )

        if updated is None:
            raise AssertionError(
                "Updated record disappeared."
            )

        if updated["value"] != 300:
            raise AssertionError(
                "UPDATE did not change the value."
            )

        # ====================================================
        # 9. Rollback UPDATE
        # ====================================================

        print()
        print("[9] Rollback UPDATE")

        context.database.rollback()

        restored = repository.get(
            committed_id
        )

        print_result(
            "Record after rollback",
            restored,
        )

        if restored is None:
            raise AssertionError(
                "Committed record disappeared."
            )

        if restored["value"] != 200:
            raise AssertionError(
                "Rollback did not restore committed value."
            )

        # ====================================================
        # 10. UPDATE with commit=True
        # ====================================================

        print()
        print("[10] UPDATE commit=True")

        update_result = repository.update(
            committed_id,
            {
                "value": 400,
            },
            commit=True,
        )

        print_result(
            "Update result",
            update_result,
        )

        committed_update = repository.get(
            committed_id
        )

        print_result(
            "Value after commit",
            committed_update,
        )

        if committed_update is None:
            raise AssertionError(
                "Record disappeared after UPDATE."
            )

        if committed_update["value"] != 400:
            raise AssertionError(
                "commit=True UPDATE was not persisted."
            )

        # ====================================================
        # 11. DELETE without commit
        # ====================================================

        print()
        print("[11] DELETE commit=False")

        delete_result = repository.delete(
            committed_id,
            commit=False,
        )

        print_result(
            "Delete result",
            delete_result,
        )

        if delete_result is not True:
            raise AssertionError(
                "Expected DELETE to return True."
            )

        deleted_before_rollback = repository.get(
            committed_id
        )

        print_result(
            "Record before rollback",
            deleted_before_rollback,
        )

        if deleted_before_rollback is not None:
            raise AssertionError(
                "DELETE did not remove the record."
            )

        # ====================================================
        # 12. Rollback DELETE
        # ====================================================

        print()
        print("[12] Rollback DELETE")

        context.database.rollback()

        restored_after_delete = repository.get(
            committed_id
        )

        print_result(
            "Record after rollback",
            restored_after_delete,
        )

        if restored_after_delete is None:
            raise AssertionError(
                "Rollback did not restore deleted record."
            )

        # ====================================================
        # 13. DELETE with commit=True
        # ====================================================

        print()
        print("[13] DELETE commit=True")

        delete_result = repository.delete(
            committed_id,
            commit=True,
        )

        print_result(
            "Delete result",
            delete_result,
        )

        if delete_result is not True:
            raise AssertionError(
                "Expected DELETE to return True."
            )

        deleted = repository.get(
            committed_id
        )

        print_result(
            "Record after commit",
            deleted,
        )

        if deleted is not None:
            raise AssertionError(
                "commit=True DELETE was not persisted."
            )

        # ====================================================
        # 14. Integrity
        # ====================================================

        print()
        print("[14] Database integrity")

        integrity = context.database.integrity_check()

        print_result(
            "Integrity check",
            integrity,
        )

        if integrity != "ok":
            raise AssertionError(
                f"SQLite integrity check failed: {integrity}"
            )

        print()
        print(
            "[15] Milestone 2E transaction test "
            "completed successfully."
        )

    finally:
        if context is not None:
            context.close()

        print()
        print("DatabaseContext closed.")

        remove_test_table(TEST_DATABASE)

        print("Temporary transaction-test table removed.")


if __name__ == "__main__":
    main()