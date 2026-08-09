from core.context import DatabaseContext
from core.repository import Repository


DATABASE_TABLE = "Artists"


def main() -> None:
    print("=" * 60)
    print("Milestone 2A - Repository Integration Test")
    print("=" * 60)

    with DatabaseContext() as context:
        print("\n[1] DatabaseContext")
        print(f"    Started: {context.started}")
        print(f"    Database: {context.database.database_path()}")

        print("\n[2] Schema")
        print(f"    Tables found: {len(context.schema.tables)}")

        for table in context.schema.tables:
            print(f"      - {table}")

        print(f"\n[3] Repository: {DATABASE_TABLE}")

        repository = Repository(
            context,
            DATABASE_TABLE,
        )

        print(f"    Table: {repository.table_name}")
        print(f"    Columns: {repository.columns}")
        print(f"    Primary key: {repository.primary_key_columns}")
        print(f"    Row count: {repository.row_count()}")

        print("\n[4] First records")

        records = repository.all(limit=5)

        for record in records:
            print(f"    {record}")

        print("\n[5] Integration test completed successfully.")

    print("\nDatabaseContext closed.")


if __name__ == "__main__":
    main()