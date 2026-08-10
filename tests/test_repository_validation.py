from __future__ import annotations

from core.context import DatabaseContext
from core.repository import Repository


def print_repository_details(
    context: DatabaseContext,
    table_name: str,
) -> None:
    """Print repository metadata and sample rows for one table."""

    print(f"\n[Table: {table_name}]")

    repository = Repository(context, table_name)

    print(f"  Columns: {repository.columns}")
    print(f"  Primary key: {repository.primary_key_columns}")
    print(f"  Foreign keys: {repository.foreign_key_columns}")
    print(f"  Row count: {repository.row_count}")

    records = repository.find(limit=3)

    print("  Sample records:")

    if not records:
        print("    <no rows>")
    else:
        for record in records:
            print(f"    {record}")


def main() -> None:
    """Run the Milestone 2B repository validation."""

    print("=" * 60)
    print("Milestone 2B - Repository Validation")
    print("=" * 60)

    with DatabaseContext() as context:
        print("\n[1] DatabaseContext")
        print(f"  Started: {context.started}")
        print(f"  Database: {context.database.database_path}")

        print("\n[2] Schema")

        tables = context.schema.tables

        print(f"  Tables found: {len(tables)}")

        for table_name in tables:
            print(f"    - {table_name}")

        print("\n[3] Repository validation")

        tables_to_test = [
            "Artists",
            "Songs",
            "Records",
            "Belong",
            "Contain",
            "Sing",
        ]

        available_tables = {
            table.lower(): table
            for table in tables
        }

        for requested_table in tables_to_test:
            actual_table = available_tables.get(
                requested_table.lower()
            )

            if actual_table is None:
                print(
                    f"\n[Table: {requested_table}]"
                    "\n  NOT FOUND - skipped."
                )
                continue

            print_repository_details(
                context,
                actual_table,
            )

        print("\n[4] Repository validation completed successfully.")

    print("\nDatabaseContext closed.")


if __name__ == "__main__":
    main()