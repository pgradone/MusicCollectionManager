"""
=========================================================
Music Collection Manager
Report Service
=========================================================

Milestone 5A (1/N)

Domain service for dashboard statistics.

Deliberately not built on the four entity services
(ArtistService, SongService, etc.) - dashboard statistics need
aggregate reads across whole tables, not single-row business
operations, so this talks to Repository directly. Every method
here is read-only.

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