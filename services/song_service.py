"""
=========================================================
Music Collection Manager
Song Service
=========================================================

Milestone 3E

Domain service for the Songs table.

Songs sit at the centre of the schema, so this service
also wraps the three junction tables that connect a song
to the rest of the collection:

* Sing    - Song <-> Artist
* Belong  - Song <-> Style
* Contain - Song <-> Record (with track Position)

Track reordering within a record is owned by RecordService,
not here - records_for_song() is a read-only view of where a
song currently sits.
"""

from __future__ import annotations

from typing import Any

from core.context import DatabaseContext
from core.repository import Repository, repository_for
from services.base_service import Service, ServiceError


class SongValidationError(ServiceError):
    """Raised when Song data fails validation."""


class SongService(Service):
    """
    Domain service for browsing, editing, and linking Songs.
    """

    def __init__(self, context: DatabaseContext) -> None:
        super().__init__(context, "Songs")

        self._sing: Repository = repository_for(context, "Sing")
        self._artists: Repository = repository_for(context, "Artists")
        self._belong: Repository = repository_for(context, "Belong")
        self._styles: Repository = repository_for(context, "Styles")
        self._contain: Repository = repository_for(context, "Contain")
        self._records: Repository = repository_for(context, "Records")
        self._schedule: Repository = repository_for(context, "Schedule")
        self._programs: Repository = repository_for(context, "Programs")

    # ========================================================
    # Read
    # ========================================================

    def list_all(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """Return songs ordered by Title."""

        return self.repository.all(
            order_by="Title",
            limit=limit,
            offset=offset,
        )

    def get(self, song_id: int) -> dict[str, Any] | None:
        """Return one song by SongID, or None when absent."""

        return self.repository.get(song_id)

    def require(self, song_id: int) -> dict[str, Any]:
        """Return one song by SongID, raising when absent."""

        return self.repository.require(song_id)

    # ========================================================
    # Write
    # ========================================================

    def create(
        self,
        *,
        title: str,
        bpm: float | None = None,
        year: int | None = None,
        time: str | None = None,
    ) -> int:
        """
        Create a new song.

        Args:
            title:
                Required. Cannot be blank.

            bpm, year, time:
                Optional. Passed through as-is.

        Returns:
            The new SongID.
        """

        clean_title = self._validated_title(title)

        new_id = self.repository.insert(
            {
                "Title": clean_title,
                "BPM": bpm,
                "Year": year,
                "Time": time,
            },
            commit=True,
        )

        return int(new_id)

    def update(
        self,
        song_id: int,
        *,
        title: str | None = None,
        bpm: float | None = None,
        year: int | None = None,
        time: str | None = None,
        clear_bpm: bool = False,
        clear_year: bool = False,
        clear_time: bool = False,
    ) -> bool:
        """
        Update an existing song.

        Only the fields supplied are changed. Pass the matching
        ``clear_*`` flag to set a field back to NULL, since
        leaving an argument as None means "leave unchanged".

        Returns:
            True when the song was updated.
        """

        self.require(song_id)

        values: dict[str, Any] = {}

        if title is not None:
            values["Title"] = self._validated_title(title)

        if bpm is not None:
            values["BPM"] = bpm
        elif clear_bpm:
            values["BPM"] = None

        if year is not None:
            values["Year"] = year
        elif clear_year:
            values["Year"] = None

        if time is not None:
            values["Time"] = time
        elif clear_time:
            values["Time"] = None

        if not values:
            raise SongValidationError(
                "update() requires at least one field to change."
            )

        return self.repository.update(
            song_id,
            values,
            commit=True,
        )

    def delete(self, song_id: int) -> bool:
        """
        Delete a song.

        Propagates the database's own integrity error when the
        song is still linked through Sing, Belong, or Contain -
        callers should remove those links first.
        """

        self.require(song_id)

        return self.repository.delete(
            song_id,
            commit=True,
        )

    # ========================================================
    # Song <-> Artist relationship (Sing)
    # ========================================================

    def artists_for_song(
        self,
        song_id: int,
    ) -> list[dict[str, Any]]:
        """Return every artist linked to this song, by Surname."""

        self.require(song_id)

        links = self._sing.find({"SongID": song_id})

        artists = [
            self._artists.require(link["ArtistID"])
            for link in links
        ]

        artists.sort(
            key=lambda artist: (
                artist["Surname"] or "",
                artist["Name"] or "",
            )
        )

        return artists

    def add_artist(self, song_id: int, artist_id: int) -> None:
        """Link an artist to this song through Sing."""

        self.require(song_id)
        self._artists.require(artist_id)

        if self._sing.exists(
            {"ArtistID": artist_id, "SongID": song_id}
        ):
            raise SongValidationError(
                f"Artist {artist_id} is already linked to "
                f"song {song_id}."
            )

        self._sing.insert(
            {"ArtistID": artist_id, "SongID": song_id},
            commit=True,
        )

    def remove_artist(self, song_id: int, artist_id: int) -> bool:
        """Unlink an artist from this song. Returns True if removed."""

        return self._sing.delete(
            {"ArtistID": artist_id, "SongID": song_id},
            commit=True,
        )

    # ========================================================
    # Song <-> Style relationship (Belong)
    # ========================================================

    def styles_for_song(
        self,
        song_id: int,
    ) -> list[dict[str, Any]]:
        """Return every style linked to this song, by Label."""

        self.require(song_id)

        links = self._belong.find({"SongID": song_id})

        styles = [
            self._styles.require(link["StyleID"])
            for link in links
        ]

        styles.sort(key=lambda style: style["Label"] or "")

        return styles

    def add_style(self, song_id: int, style_id: int) -> None:
        """Link a style to this song through Belong."""

        self.require(song_id)
        self._styles.require(style_id)

        if self._belong.exists(
            {"SongID": song_id, "StyleID": style_id}
        ):
            raise SongValidationError(
                f"Style {style_id} is already linked to "
                f"song {song_id}."
            )

        self._belong.insert(
            {"SongID": song_id, "StyleID": style_id},
            commit=True,
        )

    def remove_style(self, song_id: int, style_id: int) -> bool:
        """Unlink a style from this song. Returns True if removed."""

        return self._belong.delete(
            {"SongID": song_id, "StyleID": style_id},
            commit=True,
        )

    # ========================================================
    # Song -> Record relationship (Contain, read-only)
    # ========================================================

    def records_for_song(
        self,
        song_id: int,
    ) -> list[dict[str, Any]]:
        """
        Return every record containing this song, each with its
        track Position on that record.

        Adding, removing, and reordering tracks is owned by
        RecordService - this is a read-only reverse lookup.
        """

        self.require(song_id)

        links = self._contain.find({"SongID": song_id})

        records = []

        for link in links:
            record = dict(self._records.require(link["RecordID"]))
            record["Position"] = link["Position"]
            records.append(record)

        records.sort(key=lambda record: record["Title"] or "")

        return records

    # ========================================================
    # Song -> Program relationship (Schedule, read-only)
    # ========================================================

    def programs_scheduling_song(
        self,
        song_id: int,
    ) -> list[dict[str, Any]]:
        """
        Return every program that has scheduled this song, each with
        its scheduled Position, ordered by the program's DateSched
        then ProgName.

        Adding, removing, and reordering schedule slots is owned by
        ProgramService - this is a read-only reverse lookup, and
        Schedule.SongID is a soft foreign key (never declared with a
        FOREIGN KEY constraint in the schema).
        """

        self.require(song_id)

        links = self._schedule.find({"SongID": song_id})

        programs = []

        for link in links:
            program = dict(self._programs.require(link["ProgramID"]))
            program["Position"] = link["Position"]
            programs.append(program)

        programs.sort(
            key=lambda program: (
                program["DateSched"] or "",
                program["ProgName"] or "",
            )
        )

        return programs

    # ========================================================
    # Internal helpers
    # ========================================================

    @staticmethod
    def _validated_title(title: str) -> str:
        cleaned = title.strip()

        if not cleaned:
            raise SongValidationError(
                "Song title cannot be blank."
            )

        return cleaned