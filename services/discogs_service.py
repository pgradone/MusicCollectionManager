"""
=========================================================
Music Collection Manager
Discogs Service
=========================================================

Milestone 6A (1/N)

Access the collection by Discogs release identifier: given a
release ID (or a pasted URL / "[r123]" tag), find the Discogs
release, the Record linked to it, that record's artist, and its
songs. Also suggests which Record an unlinked release probably
belongs to, so the many releases in the Discogs export that have
no Record yet can be connected.

Works only on the data already in the database (the Discogs table
is a collection export). It makes no calls to discogs.com. Reads
only, except confirm_match(), which delegates to
RecordService.link_discogs().
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any

from core.context import DatabaseContext
from core.repository import Repository, repository_for
from services.record_service import RecordService

_RELEASE_URL = re.compile(r"/release/(\d+)")
_RELEASE_TAG = re.compile(r"^\[?r?(\d+)\]?$", re.IGNORECASE)
_DISAMBIGUATION = re.compile(r"\s*\(\d+\)\s*$")


def parse_release_id(text: str) -> str | None:
    """
    Extract a Discogs release ID from what a user might paste:
    "1000559", "r1000559", "[r1000559]", or a discogs.com release
    URL. Returns the digits as a string (release_id is stored as
    text), or None when nothing usable is found.
    """

    cleaned = text.strip()

    if not cleaned:
        return None

    url_match = _RELEASE_URL.search(cleaned)

    if url_match:
        return url_match.group(1)

    tag_match = _RELEASE_TAG.match(cleaned)

    if tag_match:
        return tag_match.group(1)

    return None


def _normalise(text: Any) -> str:
    """Lower-case, drop Discogs '(5)' suffixes, punctuation and 'the'."""

    if text is None:
        return ""

    value = _DISAMBIGUATION.sub("", str(text)).casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    value = re.sub(r"\bthe\b", " ", value)

    return " ".join(value.split())


@dataclass(frozen=True, slots=True)
class DiscogsLookup:
    """Everything reachable from one Discogs release."""

    release: dict[str, Any]
    record: dict[str, Any] | None
    artist: dict[str, Any] | None
    tracks: list[dict[str, Any]]


@dataclass(frozen=True, slots=True)
class MatchSuggestion:
    """A Record that probably corresponds to an unlinked release."""

    record: dict[str, Any]
    score: float


class DiscogsService:
    """Domain service for reaching the collection via Discogs IDs."""

    def __init__(self, context: DatabaseContext) -> None:
        self.context = context

        self._discogs: Repository = repository_for(context, "Discogs")
        self._records: Repository = repository_for(context, "Records")
        self._artists: Repository = repository_for(context, "Artists")
        self._contain: Repository = repository_for(context, "Contain")
        self._songs: Repository = repository_for(context, "Songs")
        self._record_service = RecordService(context)

    # ========================================================
    # Lookup by release id
    # ========================================================

    def get_release(self, release_id: str) -> dict[str, Any] | None:
        """Return the Discogs row for release_id, or None."""

        return self._discogs.get(release_id)

    def lookup(self, text: str) -> DiscogsLookup | None:
        """
        Resolve pasted text (ID, tag or URL) to a release and what
        hangs off it. None when the text has no ID or no such
        release exists. record/artist are None and tracks is empty
        for a release that has no Record linked yet.
        """

        release_id = parse_release_id(text)

        if release_id is None:
            return None

        release = self.get_release(release_id)

        if release is None:
            return None

        matches = self._records.find({"Discogs_release": release_id})

        if not matches:
            return DiscogsLookup(release, None, None, [])

        record = matches[0]
        artist = (
            self._artists.get(record["ArtistID"])
            if record["ArtistID"] is not None
            else None
        )

        return DiscogsLookup(
            release, record, artist, self._tracks(record["RecordID"])
        )

    def _tracks(self, record_id: int) -> list[dict[str, Any]]:
        tracks = []

        for link in self._contain.find({"RecordID": record_id}):
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

    # ========================================================
    # Listing releases
    # ========================================================

    def list_releases(
        self, *, linked: bool | None = None
    ) -> list[dict[str, Any]]:
        """
        Every Discogs release with its linked record's id and title
        (None when unlinked) added as "RecordID" and "RecordTitle".

        linked=True keeps only releases that have a record,
        linked=False only those that do not, None keeps all.
        """

        record_by_release = {
            record["Discogs_release"]: record
            for record in self._records.all()
            if record["Discogs_release"] is not None
        }

        results = []

        for release in self._discogs.all(order_by="Artist"):
            record = record_by_release.get(release["release_id"])

            if linked is True and record is None:
                continue

            if linked is False and record is not None:
                continue

            row = dict(release)
            row["RecordID"] = record["RecordID"] if record else None
            row["RecordTitle"] = record["Title"] if record else None
            results.append(row)

        return results

    # ========================================================
    # Matching unlinked releases to records
    # ========================================================

    def suggest_records(
        self, release_id: str, *, limit: int = 5, minimum: float = 0.5
    ) -> list[MatchSuggestion]:
        """
        Records that probably belong to this release, best first.

        Only Records with no Discogs link are considered - a record
        can hold one release, and the database enforces that a
        release belongs to at most one record. Titles in this
        collection often start with the artist, so artist and title
        are compared together as well as the title alone.
        """

        release = self.get_release(release_id)

        if release is None:
            return []

        release_artist = _normalise(release["Artist"])
        release_title = _normalise(release["Title"])
        release_both = f"{release_artist} {release_title}".strip()

        artist_names = {
            artist["ArtistID"]: _normalise(
                f"{artist['Name'] or ''} {artist['Surname'] or ''}"
            )
            for artist in self._artists.all()
        }

        suggestions = []

        for record in self._records.all():
            if record["Discogs_release"] is not None:
                continue

            record_title = _normalise(record["Title"])
            record_artist = artist_names.get(record["ArtistID"], "")
            record_both = f"{record_artist} {record_title}".strip()

            score = max(
                self._similarity(release_both, record_both),
                self._similarity(release_both, record_title),
                self._similarity(release_title, record_title)
                * (0.9 if release_artist == record_artist else 0.6),
            )

            if score >= minimum:
                suggestions.append(MatchSuggestion(dict(record), score))

        suggestions.sort(key=lambda item: item.score, reverse=True)

        return suggestions[:limit]

    @staticmethod
    def _similarity(left: str, right: str) -> float:
        if not left or not right:
            return 0.0

        matcher = SequenceMatcher(None, left, right)

        if matcher.real_quick_ratio() < 0.3 or matcher.quick_ratio() < 0.3:
            return 0.0

        return matcher.ratio()

    def confirm_match(self, release_id: str, record_id: int) -> None:
        """Link the release to the record (RecordService.link_discogs)."""

        self._record_service.link_discogs(record_id, release_id)
