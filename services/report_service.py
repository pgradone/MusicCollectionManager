"""
=========================================================
Music Collection Manager
Report Service
=========================================================

Milestone 5A (1/N, 2/N)

Domain service for dashboard statistics and a curated set of
collection integrity/anomaly reports, chosen from the saved
queries found in the legacy Musi.accdb (confirmed via its
object catalog: DuplicateArtists, Songs Without Records,
Songs Without Artists, Artists Without Songs, Records Without
Songs, SongsSungByManyArtists).

Deliberately not built on the four entity services
(ArtistService, SongService, etc.) - reports need aggregate
reads across whole tables, not single-row business operations,
so this talks to Repository directly. Every method here is
read-only.

Note on "recently added" items: only Programs has a creation
timestamp (DateCreate) in this schema. Artists, Songs, Records,
and Styles have no such column at all (confirmed by inspecting
the actual table DDL), so "recently added" can only be offered
for Programs - it is not something this service can fake for
the others.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.context import DatabaseContext
from core.repository import Repository, repository_for


@dataclass(frozen=True, slots=True)
class DashboardStats:
    """A snapshot of collection-wide statistics."""

    artist_count: int
    song_count: int
    record_count: int
    program_count: int
    style_count: int

    average_bpm: float | None
    songs_with_bpm: int

    collection_value_eur: float
    sold_value_eur: float
    unsold_record_count: int
    sold_record_count: int

    songs_missing_bpm: int
    songs_missing_year: int
    records_missing_artist: int

    recently_added_programs: list[dict[str, Any]]


class ReportService:
    """Domain service for dashboard-level collection statistics."""

    def __init__(self, context: DatabaseContext) -> None:
        self.context = context

        self._artists: Repository = repository_for(context, "Artists")
        self._songs: Repository = repository_for(context, "Songs")
        self._records: Repository = repository_for(context, "Records")
        self._programs: Repository = repository_for(context, "Programs")
        self._styles: Repository = repository_for(context, "Styles")
        self._sing: Repository = repository_for(context, "Sing")
        self._contain: Repository = repository_for(context, "Contain")

    def dashboard_stats(self, *, recent_limit: int = 5) -> DashboardStats:
        """
        Compute a fresh snapshot of collection-wide statistics.

        Args:
            recent_limit:
                How many recently-created programs to include.
        """

        songs = self._songs.all()
        records = self._records.all()

        bpm_values = [
            song["BPM"] for song in songs if song["BPM"] is not None
        ]
        average_bpm = (
            sum(bpm_values) / len(bpm_values) if bpm_values else None
        )

        unsold_records = [
            record for record in records if record["soldDate"] is None
        ]
        sold_records = [
            record
            for record in records
            if record["soldDate"] is not None
        ]

        collection_value = sum(
            record["Val2026"] or 0 for record in unsold_records
        )
        sold_value = sum(
            record["soldValEur"] or 0 for record in sold_records
        )

        recently_added_programs = self._programs.all(
            order_by="DateCreate",
            descending=True,
            limit=recent_limit,
        )

        return DashboardStats(
            artist_count=self._artists.count(),
            song_count=self._songs.count(),
            record_count=self._records.count(),
            program_count=self._programs.count(),
            style_count=self._styles.count(),
            average_bpm=average_bpm,
            songs_with_bpm=len(bpm_values),
            collection_value_eur=float(collection_value),
            sold_value_eur=float(sold_value),
            unsold_record_count=len(unsold_records),
            sold_record_count=len(sold_records),
            songs_missing_bpm=sum(
                1 for song in songs if song["BPM"] is None
            ),
            songs_missing_year=sum(
                1 for song in songs if song["Year"] is None
            ),
            records_missing_artist=sum(
                1 for record in records if record["ArtistID"] is None
            ),
            recently_added_programs=recently_added_programs,
        )

    # ========================================================
    # Integrity / anomaly reports
    # ========================================================

    def songs_without_artists(self) -> list[dict[str, Any]]:
        """Songs with no artist linked through Sing."""

        songs = self._songs.all(order_by="Title")
        linked_song_ids = {row["SongID"] for row in self._sing.all()}

        return [
            song for song in songs if song["SongID"] not in linked_song_ids
        ]

    def songs_without_records(self) -> list[dict[str, Any]]:
        """Songs that are not a track on any record."""

        songs = self._songs.all(order_by="Title")
        linked_song_ids = {row["SongID"] for row in self._contain.all()}

        return [
            song for song in songs if song["SongID"] not in linked_song_ids
        ]

    def artists_without_songs(self) -> list[dict[str, Any]]:
        """Artists with no song linked through Sing."""

        artists = self._artists.all(order_by="Surname")
        linked_artist_ids = {row["ArtistID"] for row in self._sing.all()}

        return [
            artist
            for artist in artists
            if artist["ArtistID"] not in linked_artist_ids
        ]

    def records_without_songs(self) -> list[dict[str, Any]]:
        """Records with no track linked through Contain."""

        records = self._records.all(order_by="Title")
        linked_record_ids = {row["RecordID"] for row in self._contain.all()}

        return [
            record
            for record in records
            if record["RecordID"] not in linked_record_ids
        ]

    def duplicate_artists(self) -> list[list[dict[str, Any]]]:
        """
        Groups of 2+ artists sharing the same Surname and Name,
        compared case-insensitively after trimming whitespace.

        Artists with no Surname are never grouped together, since a
        shared NULL doesn't indicate an actual duplicate - it just
        means neither has a surname on file.
        """

        artists = self._artists.all(order_by="Surname")

        groups: dict[tuple[str, str], list[dict[str, Any]]] = {}

        for artist in artists:
            surname = artist["Surname"]

            if not surname:
                continue

            key = (
                surname.strip().casefold(),
                (artist["Name"] or "").strip().casefold(),
            )
            groups.setdefault(key, []).append(artist)

        return [group for group in groups.values() if len(group) > 1]

    def songs_sung_by_many_artists(self) -> list[dict[str, Any]]:
        """
        Songs linked to more than one artist through Sing, each
        with the list of artists that sing it attached under the
        "artists" key.
        """

        artist_ids_by_song: dict[int, list[int]] = {}

        for row in self._sing.all():
            artist_ids_by_song.setdefault(row["SongID"], []).append(
                row["ArtistID"]
            )

        results = []

        for song_id, artist_ids in artist_ids_by_song.items():
            if len(artist_ids) < 2:
                continue

            song = dict(self._songs.require(song_id))
            song["artists"] = [
                self._artists.require(artist_id)
                for artist_id in artist_ids
            ]
            results.append(song)

        results.sort(key=lambda song: song["Title"] or "")

        return results