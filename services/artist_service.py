"""
=========================================================
Music Collection Manager
Artist Service
=========================================================

Milestone 3E

Domain service for the Artists table.

Wraps Repository access with Artist-specific validation
and the Artist <-> Song relationship, maintained through
the Sing junction table, so UI code never touches SQLite
or the Sing table directly.
"""

from __future__ import annotations

from typing import Any

from core.context import DatabaseContext
from core.repository import Repository, repository_for
from services.base_service import Service, ServiceError


class ArtistValidationError(ServiceError):
    """Raised when Artist data fails validation."""


class ArtistService(Service):
    """
    Domain service for browsing, editing, and linking Artists.
    """

    def __init__(self, context: DatabaseContext) -> None:
        super().__init__(context, "Artists")

        self._sing: Repository = repository_for(context, "Sing")
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
        """Return artists ordered by Surname, then Name."""

        return self.repository.all(
            order_by=["Surname", "Name"],
            limit=limit,
            offset=offset,
        )

    def get(self, artist_id: int) -> dict[str, Any] | None:
        """Return one artist by ArtistID, or None when absent."""

        return self.repository.get(artist_id)

    def require(self, artist_id: int) -> dict[str, Any]:
        """Return one artist by ArtistID, raising when absent."""

        return self.repository.require(artist_id)

    # ========================================================
    # Write
    # ========================================================

    def create(
        self,
        *,
        surname: str,
        name: str | None = None,
    ) -> int:
        """
        Create a new artist.

        Args:
            surname:
                Required. Cannot be blank.

            name:
                Optional given name.

        Returns:
            The new ArtistID.
        """

        clean_surname = self._validated_surname(surname)

        new_id = self.repository.insert(
            {
                "Name": name,
                "Surname": clean_surname,
            },
            commit=True,
        )

        return int(new_id)

    def update(
        self,
        artist_id: int,
        *,
        surname: str | None = None,
        name: str | None = None,
        clear_name: bool = False,
    ) -> bool:
        """
        Update an existing artist.

        Only the fields supplied are changed. Pass
        ``clear_name=True`` to set Name back to NULL, since
        ``name=None`` alone means "leave Name unchanged".

        Returns:
            True when the artist was updated.
        """

        self.require(artist_id)

        values: dict[str, Any] = {}

        if surname is not None:
            values["Surname"] = self._validated_surname(surname)

        if name is not None:
            values["Name"] = name
        elif clear_name:
            values["Name"] = None

        if not values:
            raise ArtistValidationError(
                "update() requires at least one field to change."
            )

        return self.repository.update(
            artist_id,
            values,
            commit=True,
        )

    def delete(self, artist_id: int) -> bool:
        """
        Delete an artist.

        Propagates the database's own integrity error when the
        artist is still linked to songs through Sing - callers
        should remove those links first via remove_song().
        """

        self.require(artist_id)

        return self.repository.delete(
            artist_id,
            commit=True,
        )

    # ========================================================
    # Artist <-> Song relationship (Sing)
    # ========================================================

    def songs_for_artist(
        self,
        artist_id: int,
    ) -> list[dict[str, Any]]:
        """Return every song linked to this artist, by Title."""

        self.require(artist_id)

        links = self._sing.find({"ArtistID": artist_id})

        songs = [
            self._songs.require(link["SongID"])
            for link in links
        ]

        songs.sort(key=lambda song: song["Title"] or "")

        return songs

    def add_song(self, artist_id: int, song_id: int) -> None:
        """Link a song to this artist through Sing."""

        self.require(artist_id)
        self._songs.require(song_id)

        if self._sing.exists(
            {"ArtistID": artist_id, "SongID": song_id}
        ):
            raise ArtistValidationError(
                f"Song {song_id} is already linked to "
                f"artist {artist_id}."
            )

        self._sing.insert(
            {"ArtistID": artist_id, "SongID": song_id},
            commit=True,
        )

    def remove_song(self, artist_id: int, song_id: int) -> bool:
        """Unlink a song from this artist. Returns True if removed."""

        return self._sing.delete(
            {"ArtistID": artist_id, "SongID": song_id},
            commit=True,
        )

    # ========================================================
    # Internal helpers
    # ========================================================

    @staticmethod
    def _validated_surname(surname: str) -> str:
        cleaned = surname.strip()

        if not cleaned:
            raise ArtistValidationError(
                "Artist surname cannot be blank."
            )

        return cleaned