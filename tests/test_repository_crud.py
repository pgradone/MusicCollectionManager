"""
Milestone 2C - Repository CRUD Integration Test

Uses the dedicated test database:

    tests/Musi_crud_test.db

The original Musi.db is never modified.

The test creates a temporary table, loads it into the schema,
and exercises the generic Repository CRUD API.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from core.context import DatabaseContext
from core.repository import repository_for


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TEST_DATABASE = PROJECT_ROOT / "tests" / "Musi_crud_test.db"

TEST_TABLE = "_repository_crud_test"


# ============================================================
# Helpers
# ============================================================


def create_test_table(database: Path) -> None:
    """Create the temporary CRUD test table."""

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
    """Remove the temporary CRUD test table."""

    connection = sqlite3.connect(database)

    try:
        connection.execute(
            f'DROP TABLE IF EXISTS "{TEST_TABLE}"'
        )

        connection.commit()

    finally:
        connection.close()


def print_result(label: str, value: Any) -> None:
    """Print a consistently formatted test result."""

    print(f"    {label}: {value}")


# ============================================================
# Main test
# ============================================================


def main() -> None:
    """Run the Milestone 2C repository CRUD test."""

    print()
    print("# Milestone 2C - Repository CRUD")
    print()

    if not TEST_DATABASE.exists():
        raise FileNotFoundError(
            f"Test database not found:\n{TEST_DATABASE}"
        )

    print("[1] Test database")
    print_result("Database", TEST_DATABASE)

    # --------------------------------------------------------
    # IMPORTANT:
    # Create the table BEFORE the schema is loaded.
    # --------------------------------------------------------

    create_test_table(TEST_DATABASE)

    context: DatabaseContext | None = None

    try:
        print()
        print("[2] DatabaseContext")

        context = DatabaseContext()

        # DatabaseManager is a singleton.
        # Explicitly select the dedicated CRUD database BEFORE
        # connecting and loading the schema.
        context.database.database = TEST_DATABASE

        context.start(load_schema=True)

        print_result("Started", context.started)
        print_result(
            "Database",
            context.database.database_path,
        )

        # ----------------------------------------------------
        # Verify the temporary table
        # ----------------------------------------------------

        print()
        print("[3] Temporary CRUD table")

        table = context.schema.get_table(TEST_TABLE)

        print_result("Table", table.name)

        # Do not assume TableInfo has a "column_names" property.
        # The Repository exposes the normalized column names.
        #
        # We verify the same information through Repository below.

        # ----------------------------------------------------
        # Repository
        # ----------------------------------------------------

        print()
        print("[4] Repository")

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
        # Verify expected metadata
        # ----------------------------------------------------

        expected_columns = [
            "id",
            "name",
            "value",
            "description",
        ]

        if repository.columns != expected_columns:
            raise AssertionError(
                "Unexpected repository columns.\n"
                f"Expected: {expected_columns}\n"
                f"Actual:   {repository.columns}"
            )

        if repository.primary_key_columns != ["id"]:
            raise AssertionError(
                "Unexpected primary key.\n"
                f"Expected: ['id']\n"
                f"Actual:   {repository.primary_key_columns}"
            )

        # ----------------------------------------------------
        # Initial state
        # ----------------------------------------------------

        print()
        print("[5] Initial state")

        initial_count = repository.count()

        print_result("Row count", initial_count)

        if initial_count != 0:
            raise AssertionError(
                f"Expected empty test table, got {initial_count} rows."
            )

        # ----------------------------------------------------
        # INSERT
        # ----------------------------------------------------

        print()
        print("[6] INSERT")

        first_id = repository.insert(
            {
                "name": "First Record",
                "value": 100,
                "description": "Inserted by Milestone 2C",
            },
            commit=True,
        )

        print_result("Inserted ID", first_id)

        if first_id is None:
            raise AssertionError(
                "Repository.insert() returned None."
            )

        # ----------------------------------------------------
        # GET
        # ----------------------------------------------------

        print()
        print("[7] GET")

        first_record = repository.get(first_id)

        print_result("Record", first_record)

        if first_record is None:
            raise AssertionError(
                "Repository.get() failed to retrieve inserted record."
            )

        if first_record["name"] != "First Record":
            raise AssertionError(
                "Retrieved record has unexpected name."
            )

        if first_record["value"] != 100:
            raise AssertionError(
                "Retrieved record has unexpected value."
            )

        # ----------------------------------------------------
        # INSERT second record
        # ----------------------------------------------------

        print()
        print("[8] INSERT second record")

        second_id = repository.insert(
            {
                "name": "Second Record",
                "value": 200,
                "description": "Second CRUD record",
            },
            commit=True,
        )

        print_result("Inserted ID", second_id)

        if second_id is None:
            raise AssertionError(
                "Second insert returned None."
            )

        # ----------------------------------------------------
        # COUNT
        # ----------------------------------------------------

        print()
        print("[9] COUNT")

        count = repository.count()

        print_result("Row count", count)

        if count != 2:
            raise AssertionError(
                f"Expected 2 rows, got {count}."
            )

        # ----------------------------------------------------
        # EXISTS
        # ----------------------------------------------------

        print()
        print("[10] EXISTS")

        first_exists = repository.exists(first_id)
        second_exists = repository.exists(second_id)

        print_result(
            "First record exists",
            first_exists,
        )

        print_result(
            "Second record exists",
            second_exists,
        )

        if not first_exists:
            raise AssertionError(
                "First record should exist."
            )

        if not second_exists:
            raise AssertionError(
                "Second record should exist."
            )

        # ----------------------------------------------------
        # FIND
        # ----------------------------------------------------

        print()
        print("[11] FIND")

        records = repository.find(
            {"value": 200},
        )

        print_result("Matching records", records)

        if len(records) != 1:
            raise AssertionError(
                f"Expected one matching record, got {len(records)}."
            )

        if records[0]["name"] != "Second Record":
            raise AssertionError(
                "FIND returned the wrong record."
            )

        # ----------------------------------------------------
        # FIND with ordering and limit
        # ----------------------------------------------------

        print()
        print("[12] FIND with ordering and limit")

        records = repository.find(
            order_by="id",
            limit=1,
        )

        print_result("First record", records)

        if len(records) != 1:
            raise AssertionError(
                "Expected exactly one record from limited FIND."
            )

        if records[0]["id"] != first_id:
            raise AssertionError(
                "Ordered FIND returned the wrong record."
            )

        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

        print()
        print("[13] UPDATE")

        updated = repository.update(
            first_id,
            {
                "name": "Updated Record",
                "value": 999,
                "description": "Updated by Milestone 2C",
            },
            commit=True,
        )

        print_result("Updated", updated)

        if not updated:
            raise AssertionError(
                "Repository.update() returned False."
            )

        updated_record = repository.get(first_id)

        print_result(
            "Updated record",
            updated_record,
        )

        if updated_record is None:
            raise AssertionError(
                "Updated record could not be retrieved."
            )

        if updated_record["name"] != "Updated Record":
            raise AssertionError(
                "UPDATE did not change the name."
            )

        if updated_record["value"] != 999:
            raise AssertionError(
                "UPDATE did not change the value."
            )

        # ----------------------------------------------------
        # DELETE
        # ----------------------------------------------------

        print()
        print("[14] DELETE")

        deleted = repository.delete(
            second_id,
            commit=True,
        )

        print_result("Deleted", deleted)

        if not deleted:
            raise AssertionError(
                "Repository.delete() returned False."
            )

        # ----------------------------------------------------
        # Verify DELETE
        # ----------------------------------------------------

        print()
        print("[15] Verify DELETE")

        deleted_record = repository.get(second_id)
        remaining_count = repository.count()

        print_result(
            "Deleted record",
            deleted_record,
        )

        print_result(
            "Remaining rows",
            remaining_count,
        )

        if deleted_record is not None:
            raise AssertionError(
                "Deleted record can still be retrieved."
            )

        if remaining_count != 1:
            raise AssertionError(
                f"Expected 1 remaining row, got {remaining_count}."
            )

        # ----------------------------------------------------
        # Final state
        # ----------------------------------------------------

        print()
        print("[16] Final state")

        final_records = repository.all()

        for record in final_records:
            print(f"    {record}")

        if len(final_records) != 1:
            raise AssertionError(
                "Final table should contain exactly one record."
            )

        if final_records[0]["id"] != first_id:
            raise AssertionError(
                "Unexpected final record."
            )

        print()
        print("[17] Milestone 2C completed successfully.")

    finally:
        # ----------------------------------------------------
        # Close the context.
        # ----------------------------------------------------

        if context is not None:
            context.close()

        print()
        print("DatabaseContext closed.")

        # ----------------------------------------------------
        # Remove temporary table.
        # ----------------------------------------------------

        remove_test_table(TEST_DATABASE)

        print("Temporary CRUD table removed.")


if __name__ == "__main__":
    main()