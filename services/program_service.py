"""
=========================================================
Music Collection Manager
Program Service
=========================================================

Milestone 3E (4/4)

Domain service for the Programs table.

Wraps Programs -> Schedule, the running order of songs
played in a program (a DJ set / broadcast).

Schedule's primary key is (ProgramID, Position) - Position is
part of the key, not a plain column, so changing a song's slot
means deleting and re-inserting the row (done atomically via a
transaction), not updating it in place.

Song_Artist and Record are free-text historical snapshots the
caller supplies (e.g. "Title * Artist", built by hand or from a
song lookup at the UI layer) - this service does not derive
them. Only BPM and Year are auto-copied from Songs when
omitted, since those are plain numeric facts about the song at
scheduling time.
"""

from __future__ import annotations

from typing import Any

from core.context import DatabaseContext
from core.repository import Repository, repository_for
from services.base_service import Service, ServiceError


class ProgramValidationError(ServiceError):
    """Raised when Program or Schedule data fails validation."""


class ProgramService(Service):
    """
    Domain service for browsing, editing, and scheduling Programs.
    """

    def __init__(self, context: DatabaseContext) -> None:
        super().__init__(context, "Programs")

        self._schedule: Repository = repository_for(context, "Schedule")
        self._songs: Repository = repository_for(context, "Songs")

    # ========================================================
    # Read
    # ========================================================

    def list_all(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """Return programs ordered by DateSched."""

        return self.repository.all(
            order_by="DateSched",
            limit=limit,
            offset=offset,
        )

    def get(self, program_id: int) -> dict[str, Any] | None:
        """Return one program by ProgramID, or None when absent."""

        return self.repository.get(program_id)

    def require(self, program_id: int) -> dict[str, Any]:
        """Return one program by ProgramID, raising when absent."""

        return self.repository.require(program_id)

    # ========================================================
    # Write
    # ========================================================

    def create(
        self,
        *,
        prog_name: str,
        date_sched: str | None = None,
        date_create: str | None = None,
        description: str | None = None,
    ) -> int:
        """
        Create a new program.

        Args:
            prog_name:
                Required. Cannot be blank.

        Returns:
            The new ProgramID.
        """

        clean_name = self._validated_name(prog_name)

        new_id = self.repository.insert(
            {
                "ProgName": clean_name,
                "DateSched": date_sched,
                "DateCreate": date_create,
                "Description": description,
            },
            commit=True,
        )

        return int(new_id)

    def update(
        self,
        program_id: int,
        *,
        prog_name: str | None = None,
        date_sched: str | None = None,
        date_create: str | None = None,
        description: str | None = None,
        clear_date_sched: bool = False,
        clear_date_create: bool = False,
        clear_description: bool = False,
    ) -> bool:
        """
        Update an existing program.

        Only the fields supplied are changed. Pass the matching
        ``clear_*`` flag to set a nullable field back to NULL.

        Returns:
            True when the program was updated.
        """

        self.require(program_id)

        values: dict[str, Any] = {}

        if prog_name is not None:
            values["ProgName"] = self._validated_name(prog_name)

        if date_sched is not None:
            values["DateSched"] = date_sched
        elif clear_date_sched:
            values["DateSched"] = None

        if date_create is not None:
            values["DateCreate"] = date_create
        elif clear_date_create:
            values["DateCreate"] = None

        if description is not None:
            values["Description"] = description
        elif clear_description:
            values["Description"] = None

        if not values:
            raise ProgramValidationError(
                "update() requires at least one field to change."
            )

        return self.repository.update(
            program_id,
            values,
            commit=True,
        )

    def delete(self, program_id: int) -> bool:
        """
        Delete a program.

        Propagates the database's own integrity error when the
        program still has scheduled songs - callers should clear
        the schedule first via remove_song().
        """

        self.require(program_id)

        return self.repository.delete(
            program_id,
            commit=True,
        )

    # ========================================================
    # Program -> Schedule (running order)
    # ========================================================

    def schedule_for_program(
        self,
        program_id: int,
    ) -> list[dict[str, Any]]:
        """Return the full running order, ordered by Position."""

        self.require(program_id)

        entries = self._schedule.find({"ProgramID": program_id})

        entries.sort(key=lambda entry: entry["Position"])

        return entries

    def add_song(
        self,
        program_id: int,
        position: float,
        *,
        song_id: int | None = None,
        song_artist: str | None = None,
        record: str | None = None,
        bpm: float | None = None,
        year: int | None = None,
    ) -> None:
        """
        Add a slot to a program's running order.

        Args:
            position:
                Required - Position is part of Schedule's primary
                key, so it must be unique within this program.

            song_id:
                Optional - a slot can exist without a linked song
                (e.g. an announcement or intro).

            song_artist, record:
                Optional free-text snapshots (e.g. "Title * Artist")
                supplied by the caller; not derived here.

            bpm, year:
                Optional - copied from the linked song when omitted
                and song_id is given.
        """

        self.require(program_id)

        if song_id is not None:
            song = self._songs.require(song_id)

            if bpm is None:
                bpm = song["BPM"]

            if year is None:
                year = song["Year"]

        if self._schedule.exists(
            {"ProgramID": program_id, "Position": position}
        ):
            raise ProgramValidationError(
                f"Position {position!r} is already scheduled on "
                f"program {program_id}."
            )

        self._schedule.insert(
            {
                "ProgramID": program_id,
                "Position": position,
                "SongID": song_id,
                "Song_Artist": song_artist,
                "Record": record,
                "BPM": bpm,
                "Year": year,
            },
            commit=True,
        )

    def remove_song(self, program_id: int, position: float) -> bool:
        """Remove a slot from a program's running order."""

        return self._schedule.delete(
            {"ProgramID": program_id, "Position": position},
            commit=True,
        )

    def move_song(
        self,
        program_id: int,
        old_position: float,
        new_position: float,
    ) -> None:
        """
        Move a slot to a new Position.

        Position is part of Schedule's primary key, so this
        cannot be a plain UPDATE - the row is deleted and
        re-inserted with its other data unchanged, atomically.
        """

        self.require(program_id)

        old_key = {"ProgramID": program_id, "Position": old_position}
        entry = self._schedule.require(old_key)

        if old_position == new_position:
            return

        if self._schedule.exists(
            {"ProgramID": program_id, "Position": new_position}
        ):
            raise ProgramValidationError(
                f"Position {new_position!r} is already scheduled "
                f"on program {program_id}."
            )

        moved = dict(entry)
        moved["Position"] = new_position

        with self.context.database.transaction():
            self._schedule.delete(old_key, commit=False)
            self._schedule.insert(moved, commit=False)

    # ========================================================
    # Internal helpers
    # ========================================================

    @staticmethod
    def _validated_name(prog_name: str) -> str:
        cleaned = prog_name.strip()

        if not cleaned:
            raise ProgramValidationError(
                "Program name cannot be blank."
            )

        return cleaned