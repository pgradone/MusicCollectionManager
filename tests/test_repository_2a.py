"""
Milestone 2A repository smoke test.

Read-only test against the application's configured database.
No INSERT, UPDATE, or DELETE operations are performed.
"""

from core.context import DatabaseContext
from core.repository import Repository


def main() -> None:
    with DatabaseContext() as context:

        print()
        print("=" * 60)
        print("MusicCollectionManager - Milestone 2A")
        print("Generic Repository Smoke Test")
        print("=" * 60)

        print()
        print("Database:")
        print(f"  {context.database.database_path}")

        print()
        print("Schema:")
        print(f"  Tables discovered: {len(context.schema)}")

        # -------------------------------------------------
        # Artists
        # -------------------------------------------------

        artists = Repository(
            context,
            "Artists",
        )

        print()
        print("Artists")
        print(f"  Columns: {len(artists.columns)}")
        print(f"  Primary key: {artists.primary_key_columns}")
        print(f"  Rows: {artists.count()}")

        artist_rows = artists.all(
            order_by=artists.primary_key_columns[0],
            limit=3,
        )

        for row in artist_rows:
            print(f"  {row}")

        # -------------------------------------------------
        # Songs
        # -------------------------------------------------

        songs = Repository(
            context,
            "Songs",
        )

        print()
        print("Songs")
        print(f"  Primary key: {songs.primary_key_columns}")
        print(f"  Rows: {songs.count()}")

        song_rows = songs.all(
            order_by=songs.primary_key_columns[0],
            limit=3,
        )

        for row in song_rows:
            print(f"  {row}")

        # -------------------------------------------------
        # Schedule - composite PK
        # -------------------------------------------------

        schedule = Repository(
            context,
            "Schedule",
        )

        print()
        print("Schedule")
        print(
            f"  Primary key: "
            f"{schedule.primary_key_columns}"
        )
        print(
            f"  Composite key: "
            f"{schedule.is_composite_key}"
        )
        print(f"  Rows: {schedule.count()}")

        schedule_rows = schedule.all(
            order_by=schedule.primary_key_columns,
            limit=3,
        )

        for row in schedule_rows:
            print(f"  {row}")

        # -------------------------------------------------
        # Foreign-key metadata
        # -------------------------------------------------

        belong = Repository(
            context,
            "Belong",
        )

        print()
        print("Belong")
        print(
            f"  Primary key: "
            f"{belong.primary_key_columns}"
        )
        print(
            f"  Foreign keys: "
            f"{belong.foreign_key_columns}"
        )

        for column in belong.foreign_key_columns:
            print(
                f"  {column} -> "
                f"{belong.foreign_key_targets(column)}"
            )

        # -------------------------------------------------
        # Completion
        # -------------------------------------------------

        print()
        print("=" * 60)
        print("MILESTONE 2A READ-ONLY TEST PASSED")
        print("=" * 60)


if __name__ == "__main__":
    main()