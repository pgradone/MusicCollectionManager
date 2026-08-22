"""
=========================================================
Music Collection Manager
Search Service
=========================================================

Milestone 5B (1/N)

Domain service for global, cross-entity search - "Provide global
search across relevant entities" from the original specification's
Search & Reports phase.

This is distinct from main.py's existing per-table filter_rows(),
which only hides/shows rows already loaded in the currently browsed
table. This searches Artists, Songs, Records, Programs, and Styles
all at once, regardless of which table (if any) is currently open.

Deliberately not built on the four entity services - a cross-table
substring search needs a full scan of each table's searchable text
columns, not single-row business operations, so this talks to
Repository directly. Read-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.context import DatabaseContext
from core.repository import Repository, repository_for


@dataclass(frozen=True, slots=True)
class SearchResult:
    """One matched row from a global search."""

    table: str
    primary_key_column: str
    primary_key_value: Any
    row: dict[str, Any]


class SearchService:
    """Domain service for case-insensitive substring search across entities."""

    def __init__(self, context: DatabaseContext) -> None:
        self.context = context

        self._artists: Repository = repository_for(context, "Artists")
        self._songs: Repository = repository_for(context, "Songs")
        self._records: Repository = repository_for(context, "Records")
        self._programs: Repository = repository_for(context, "Programs")
        self._styles: Repository = repository_for(context, "Styles")

    def search(self, query: str) -> list[SearchResult]:
        """
        Case-insensitive substring search across:

        * Artists  - Name, Surname
        * Songs    - Title
        * Records  - Title
        * Programs - ProgName, Description
        * Styles   - Label

        Returns an empty list for a blank query rather than every
        row in every table.
        """

        needle = query.strip().casefold()

        if not needle:
            return []

        results: list[SearchResult] = []

        for artist in self._artists.all(order_by="Surname"):
            if self._matches(needle, artist.get("Name"), artist.get("Surname")):
                results.append(
                    SearchResult("Artists", "ArtistID", artist["ArtistID"], artist)
                )

        for song in self._songs.all(order_by="Title"):
            if self._matches(needle, song.get("Title")):
                results.append(
                    SearchResult("Songs", "SongID", song["SongID"], song)
                )

        for record in self._records.all(order_by="Title"):
            if self._matches(needle, record.get("Title")):
                results.append(
                    SearchResult("Records", "RecordID", record["RecordID"], record)
                )

        for program in self._programs.all(order_by="ProgName"):
            if self._matches(
                needle, program.get("ProgName"), program.get("Description")
            ):
                results.append(
                    SearchResult(
                        "Programs", "ProgramID", program["ProgramID"], program
                    )
                )

        for style in self._styles.all(order_by="Label"):
            if self._matches(needle, style.get("Label")):
                results.append(
                    SearchResult("Styles", "StyleID", style["StyleID"], style)
                )

        return results

    @staticmethod
    def _matches(needle: str, *haystacks: Any) -> bool:
        return any(
            needle in str(haystack).casefold()
            for haystack in haystacks
            if haystack is not None
        )