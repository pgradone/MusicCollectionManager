from __future__ import annotations

from pathlib import Path
import shutil

from core.context import DatabaseContext
from core.database import DatabaseManager
from core.repository import Repository


SOURCE_DATABASE = Path("Musi.db")
TEST_DATABASE = Path("tests/Musi_crud_test.db")


def main() -> None:
    print("=" * 60)
    print("Milestone 2A-B - Safe Repository CRUD Test")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Create a fresh copy of the real database
    # ---------------------------------------------------------

    print("\n[1] Preparing test database")

    if not SOURCE_DATABASE.exists():
        raise FileNotFoundError(
            f"Source database not found: {SOURCE_DATABASE}"
        )

    TEST_DATABASE.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(SOURCE_DATABASE, TEST_DATABASE)

    print(f"    Source: {SOURCE_DATABASE.resolve()}")
    print(f"    Test:   {TEST_DATABASE.resolve()}")

    # ---------------------------------------------------------
    # 2. Configure the DatabaseManager for the test copy
    # ---------------------------------------------------------

    print("\n[2] Opening test database")

    database = DatabaseManager()

    # Make absolutely sure there is no active connection.
    database.disconnect()

    # Point the singleton at the copied database.
    database.database = TEST_DATABASE.resolve()

    print(f"    Database: {database.database_path}")

    # ---------------------------------------------------------
    # 3. Start the application context
    # ---------------------------------------------------------

    with DatabaseContext(database) as context:

        print("\n[3] DatabaseContext")

        print(f"    Started: {context.started}")
        print(f"    Database: {context.database.database_path}")

        # -----------------------------------------------------
        # 4. Create repository for Artists
        # -----------------------------------------------------

        repository = Repository(
            context,
            "Artists",
        )

        print("\n[4] Artists repository")

        print(f"    Table: {repository.table_name}")
        print(f"    Columns: {repository.columns}")
        print(f"    Primary key: {repository.primary_key_columns}")
        print(f"    Initial row count: {repository.row_count}")

        initial_count = repository.row_count

        # -----------------------------------------------------
        # 5. INSERT
        # -----------------------------------------------------

        print("\n[5] INSERT")

        inserted_id = repository.insert(
            {
                "Name": "MCM_TEST",
                "Surname": "Repository",
            },
            commit=True,
        )

        print(f"    Inserted primary key: {inserted_id}")

        if inserted_id is None:
            raise RuntimeError("INSERT did not return a primary key.")

        # -----------------------------------------------------
        # 6. Verify INSERT
        # -----------------------------------------------------

        inserted = repository.get(inserted_id)

        print(f"    Inserted record: {inserted}")

        if inserted is None:
            raise RuntimeError("Inserted record could not be retrieved.")

        if inserted["Name"] != "MCM_TEST":
            raise RuntimeError("Inserted Name does not match.")

        if inserted["Surname"] != "Repository":
            raise RuntimeError("Inserted Surname does not match.")

        if repository.row_count != initial_count + 1:
            raise RuntimeError("Row count did not increase after INSERT.")

        print("    INSERT verified.")

        # -----------------------------------------------------
        # 7. UPDATE
        # -----------------------------------------------------

        print("\n[6] UPDATE")

        updated = repository.update(
            inserted_id,
            {
                "Name": "MCM_TEST_UPDATED",
                "Surname": "RepositoryUpdated",
            },
            commit=True,
        )

        print(f"    Update result: {updated}")

        if not updated:
            raise RuntimeError("UPDATE reported failure.")

        updated_record = repository.get(inserted_id)

        print(f"    Updated record: {updated_record}")

        if updated_record is None:
            raise RuntimeError("Updated record could not be retrieved.")

        if updated_record["Name"] != "MCM_TEST_UPDATED":
            raise RuntimeError("UPDATE did not change Name.")

        if updated_record["Surname"] != "RepositoryUpdated":
            raise RuntimeError("UPDATE did not change Surname.")

        print("    UPDATE verified.")

        # -----------------------------------------------------
        # 8. EXISTS
        # -----------------------------------------------------

        print("\n[7] EXISTS")

        exists = repository.exists(inserted_id)

        print(f"    Record exists: {exists}")

        if not exists:
            raise RuntimeError(
                "Record should exist before DELETE."
            )

        print("    EXISTS verified.")

        # -----------------------------------------------------
        # 9. DELETE
        # -----------------------------------------------------

        print("\n[8] DELETE")

        deleted = repository.delete(
            inserted_id,
            commit=True,
        )

        print(f"    Delete result: {deleted}")

        if not deleted:
            raise RuntimeError("DELETE reported failure.")

        # -----------------------------------------------------
        # 10. Verify DELETE
        # -----------------------------------------------------

        deleted_record = repository.get(inserted_id)

        print(f"    Record after DELETE: {deleted_record}")

        if deleted_record is not None:
            raise RuntimeError(
                "Record still exists after DELETE."
            )

        if repository.row_count != initial_count:
            raise RuntimeError(
                "Row count did not return to its original value."
            )

        print("    DELETE verified.")

    # ---------------------------------------------------------
    # 11. Final result
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("MILESTONE 2A-B PASSED")
    print("=" * 60)

    print("\nAll CRUD operations were performed on:")
    print(f"    {TEST_DATABASE.resolve()}")

    print("\nYour original database was NOT modified:")
    print(f"    {SOURCE_DATABASE.resolve()}")

    print("\nOperations verified:")
    print("    INSERT")
    print("    GET")
    print("    UPDATE")
    print("    EXISTS")
    print("    DELETE")


if __name__ == "__main__":
    main()