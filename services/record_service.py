"""
=========================================================
Music Collection Manager
Record Service
=========================================================

Milestone 3E

Domain service for the Records table.

Wraps three relationships:

* Records -> Artist   - a direct ArtistID foreign key (not a
                         junction table; a record has at most
                         one artist, and ArtistID may be NULL
                         for various-artist releases).

* Records -> Tracks    - via Contain. Position is a free-form
                          label (e.g. "A1", "B2", "1A1"), not a
                          plain sequence number, because it
                          records the physical vinyl side and
                          track - so callers set it explicitly
                          rather than having it auto-assigned.

* Records -> Discogs   - an optional single link. The database
                          enforces that a Discogs release can be
                          linked to at most one record.
"""

from __future__ import annotations

from typing import Any

from core.context import DatabaseContext
from core.repository import Repository, repository_for
from services.base_service import Service, ServiceError


class RecordValidationError(ServiceError):
    """Raised when Record data fails validation."""


class RecordService(Service):
    """
    Domain service for browsing, editing, and linking Records.
    """

    def __init__(self, context: DatabaseContext) -> None:
        super().__init__(context, "Records")

        self._contain: Repository = repository_for(context, "Contain")
        self._songs: Repository = repository_for(context, "Songs")
        self._artists: Repository = repository_for(context, "Artists")
        self._discogs: Repository = repository_for(context, "Discogs")

    # ========================================================
    # Read
    # ========================================================

    def list_all(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """Return records ordered by Title."""

        return self.repository.all(
            order_by="Title",
            limit=limit,
            offset=offset,
        )

    def get(self, record_id: int) -> dict[str, Any] | None:
        """Return one record by RecordID, or None when absent."""

        return self.repository.get(record_id)

    def require(self, record_id: int) -> dict[str, Any]:
        """Return one record by RecordID, raising when absent."""

        return self.repository.require(record_id)

    # ========================================================
    # Write
    # ========================================================

    def create(
        self,
        *,
        title: str,
        artist_id: int | None = None,
        record_house: str | None = None,
        support: str | None = None,
        mike: int | None = None,
        tito: int | None = None,
        anno: int | None = None,
    ) -> int:
        """
        Create a new record.

        Args:
            title:
                Required. Cannot be blank.

            artist_id:
                Optional - some releases (compilations, various
                artists) have no single artist. Validated against
                Artists when given.

        Returns:
            The new RecordID.
        """

        clean_title = self._validated_title(title)

        if artist_id is not None:
            self._artists.require(artist_id)

        new_id = self.repository.insert(
            {
                "Title": clean_title,
                "Record House": record_house,
                "Mike": mike,
                "Tito": tito,
                "Support": support,
                "ArtistID": artist_id,
                "Anno": anno,
                "Val2026": None,
                "soldDate": None,
                "soldValEur": None,
                "Discogs_release": None,
            },
            commit=True,
        )

        return int(new_id)

    def update(
        self,
        record_id: int,
        *,
        title: str | None = None,
        artist_id: int | None = None,
        record_house: str | None = None,
        support: str | None = None,
        mike: int | None = None,
        tito: int | None = None,
        anno: int | None = None,
        val2026: float | None = None,
        sold_date: str | None = None,
        sold_val_eur: float | None = None,
        clear_artist: bool = False,
        clear_record_house: bool = False,
        clear_support: bool = False,
        clear_anno: bool = False,
        clear_val2026: bool = False,
        clear_sold_date: bool = False,
        clear_sold_val_eur: bool = False,
    ) -> bool:
        """
        Update an existing record.

        Only the fields supplied are changed. Pass the matching
        ``clear_*`` flag to set a nullable field back to NULL,
        since leaving an argument as None means "leave unchanged".

        Returns:
            True when the record was updated.
        """

        self.require(record_id)

        values: dict[str, Any] = {}

        if title is not None:
            values["Title"] = self._validated_title(title)

        if artist_id is not None:
            self._artists.require(artist_id)
            values["ArtistID"] = artist_id
        elif clear_artist:
            values["ArtistID"] = None

        if record_house is not None:
            values["Record House"] = record_house
        elif clear_record_house:
            values["Record House"] = None

        if support is not None:
            values["Support"] = support
        elif clear_support:
            values["Support"] = None

        if mike is not None:
            values["Mike"] = mike

        if tito is not None:
            values["Tito"] = tito

        if anno is not None:
            values["Anno"] = anno
        elif clear_anno:
            values["Anno"] = None

        if val2026 is not None:
            values["Val2026"] = val2026
        elif clear_val2026:
            values["Val2026"] = None

        if sold_date is not None:
            values["soldDate"] = sold_date
        elif clear_sold_date:
            values["soldDate"] = None

        if sold_val_eur is not None:
            values["soldValEur"] = sold_val_eur
        elif clear_sold_val_eur:
            values["soldValEur"] = None

        if not values:
            raise RecordValidationError(
                "update() requires at least one field to change."
            )

        return self.repository.update(
            record_id,
            values,
            commit=True,
        )

    def delete(self, record_id: int) -> bool:
        """
        Delete a record.

        Propagates the database's own integrity error when the
        record still has tracks through Contain - callers should
        remove those tracks first via remove_track().
        """

        self.require(record_id)

        return self.repository.delete(
            record_id,
            commit=True,
        )

    # ========================================================
    # Record -> Artist (direct foreign key)
    # ========================================================

    def artist_for_record(
        self,
        record_id: int,
    ) -> dict[str, Any] | None:
        """Return the artist for this record, or None when unset."""

        record = self.require(record_id)

        if record["ArtistID"] is None:
            return None

        return self._artists.require(record["ArtistID"])

    # ========================================================
    # Record -> Tracks (Contain)
    # ========================================================

    def tracks_for_record(
        self,
        record_id: int,
    ) -> list[dict[str, Any]]:
        """
        Return every track on this record, ordered by Position.
        Tracks with no Position sort last.
        """

        self.require(record_id)

        links = self._contain.find({"RecordID": record_id})

        tracks = []

        for link in links:
            song = dict(self._songs.require(link["SongID"]))
            song["Position"] = link["Position"]
            tracks.append(song)

        tracks.sort(
            key=lambda track: (
                track["Position"] is None,
                track["Position"] or "",
            )
        )

        return tracks

    def add_track(
        self,
        record_id: int,
        song_id: int,
        *,
        position: str | None = None,
    ) -> None:
        """
        Add a song as a track on this record.

        Args:
            position:
                Optional side/track label (e.g. "A1"). Must be
                unique on this record when given - it is not
                auto-assigned, since the correct next label
                depends on the release's own side layout.
        """

        self.require(record_id)
        self._songs.require(song_id)

        if self._contain.exists(
            {"RecordID": record_id, "SongID": song_id}
        ):
            raise RecordValidationError(
                f"Song {song_id} is already a track on "
                f"record {record_id}."
            )

        if position is not None and self._position_taken(
            record_id, position
        ):
            raise RecordValidationError(
                f"Position {position!r} is already used on "
                f"record {record_id}."
            )

        self._contain.insert(
            {
                "RecordID": record_id,
                "SongID": song_id,
                "Position": position,
            },
            commit=True,
        )

    def remove_track(self, record_id: int, song_id: int) -> bool:
        """Remove a track from this record. Returns True if removed."""

        return self._contain.delete(
            {"RecordID": record_id, "SongID": song_id},
            commit=True,
        )

    def reorder_track(
        self,
        record_id: int,
        song_id: int,
        new_position: str | None,
    ) -> bool:
        """
        Change the Position label of an existing track.

        Pass ``new_position=None`` to clear the label.
        """

        self.require(record_id)

        key = {"RecordID": record_id, "SongID": song_id}
        self._contain.require(key)

        if new_position is not None and self._position_taken(
            record_id, new_position, exclude_song_id=song_id
        ):
            raise RecordValidationError(
                f"Position {new_position!r} is already used on "
                f"record {record_id}."
            )

        return self._contain.update(
            key,
            {"Position": new_position},
            commit=True,
        )

    # ========================================================
    # Record -> Discogs (optional single link)
    # ========================================================

    def discogs_info(
        self,
        record_id: int,
    ) -> dict[str, Any] | None:
        """Return the linked Discogs row, or None when unlinked."""

        record = self.require(record_id)

        if record["Discogs_release"] is None:
            return None

        return self._discogs.get(record["Discogs_release"])

    def link_discogs(self, record_id: int, release_id: str) -> None:
        """
        Link this record to a Discogs release.

        The database enforces that a release can be linked to at
        most one record, so this raises the database's own
        integrity error if release_id is already linked elsewhere.
        """

        self.require(record_id)
        self._discogs.require(release_id)

        self.repository.update(
            record_id,
            {"Discogs_release": release_id},
            commit=True,
        )

    def unlink_discogs(self, record_id: int) -> None:
        """Remove this record's Discogs link, if any."""

        self.require(record_id)

        self.repository.update(
            record_id,
            {"Discogs_release": None},
            commit=True,
        )

    # ========================================================
    # Internal helpers
    # ========================================================

    def _position_taken(
        self,
        record_id: int,
        position: str,
        *,
        exclude_song_id: int | None = None,
    ) -> bool:
        matches = self._contain.find(
            {"RecordID": record_id, "Position": position}
        )

        if exclude_song_id is not None:
            matches = [
                match
                for match in matches
                if match["SongID"] != exclude_song_id
            ]

        return len(matches) > 0

    @staticmethod
    def _validated_title(title: str) -> str:
        cleaned = title.strip()

        if not cleaned:
            raise RecordValidationError(
                "Record title cannot be blank."
            )

        return cleaned