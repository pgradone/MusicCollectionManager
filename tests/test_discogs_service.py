"""
=========================================================
Music Collection Manager
Discogs Service Tests
=========================================================

Milestone 6A (1/N)

pytest tests for services/discogs_service.py.

Runs against the dedicated CRUD test database
(tests/Musi_crud_test.db), never the production database.
Every test cleans up the rows it creates. Release ids start with
"99" so they cannot collide with real Discogs ids in the seed data.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from core.context import DatabaseContext
from core.database import QueryError
from core.repository import repository_for
from services.discogs_service import DiscogsService, parse_release_id
from services.record_service import RecordService

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATABASE = PROJECT_ROOT / "tests" / "Musi_crud_test.db"


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture()
def context() -> Iterator[DatabaseContext]:
    if not TEST_DATABASE.exists():
        raise FileNotFoundError(f"Test database not found:\n{TEST_DATABASE}")

    db_context = DatabaseContext()
    original_path = db_context.database.database

    db_context.database.database = TEST_DATABASE
    db_context.start(load_schema=True)

    try:
        yield db_context
    finally:
        db_context.close()
        db_context.database.database = original_path


@pytest.fixture()
def discogs(context: DatabaseContext) -> DiscogsService:
    return DiscogsService(context)


def _add_release(
    context: DatabaseContext, release_id: str, artist: str, title: str
) -> None:
    repository_for(context, "Discogs").insert(
        {
            "ID": 990000 + int(release_id[2:]),
            "release_id": release_id,
            "Artist": artist,
            "Title": title,
        },
        commit=True,
    )


def _drop_release(context: DatabaseContext, release_id: str) -> None:
    repository_for(context, "Discogs").delete(release_id, commit=True)


# ============================================================
# parse_release_id
# ============================================================


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1000559", "1000559"),
        ("  1000559  ", "1000559"),
        ("r1000559", "1000559"),
        ("R1000559", "1000559"),
        ("[r1000559]", "1000559"),
        ("https://www.discogs.com/release/1000559", "1000559"),
        (
            "https://www.discogs.com/release/1000559-Donna-Summer-Bad-Girls",
            "1000559",
        ),
        ("https://www.discogs.com/it/release/98675-Bad-Girls", "98675"),
        ("", None),
        ("   ", None),
        ("not an id", None),
        ("12ab", None),
    ],
)
def test_parse_release_id(text: str, expected: str | None) -> None:
    assert parse_release_id(text) == expected


# ============================================================
# lookup
# ============================================================


def test_lookup_unlinked_release_has_no_record(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    _add_release(context, "990001", "Nobody", "Unlinked Release")

    try:
        result = discogs.lookup("990001")

        assert result is not None
        assert result.release["Title"] == "Unlinked Release"
        assert result.record is None
        assert result.artist is None
        assert result.tracks == []
    finally:
        _drop_release(context, "990001")


def test_lookup_linked_release_returns_record_artist_and_tracks(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    records = RecordService(context)
    artists = repository_for(context, "Artists")
    songs = repository_for(context, "Songs")

    artist_id = artists.insert({"Surname": "ZzzDiscogsArtist"}, commit=True)
    record_id = records.create(title="Zzz Linked Record", artist_id=artist_id)
    first_song = songs.insert({"Title": "Zzz Second Side"}, commit=True)
    second_song = songs.insert({"Title": "Zzz First Side"}, commit=True)
    records.add_track(record_id, first_song, position="B1")
    records.add_track(record_id, second_song, position="A1")
    _add_release(context, "990002", "ZzzDiscogsArtist", "Zzz Linked Record")
    records.link_discogs(record_id, "990002")

    try:
        result = discogs.lookup("[r990002]")

        assert result is not None
        assert result.record is not None
        assert result.record["RecordID"] == record_id
        assert result.artist is not None
        assert result.artist["ArtistID"] == artist_id
        # Ordered by Position label, not insertion order.
        assert [t["Position"] for t in result.tracks] == ["A1", "B1"]
        assert [t["SongID"] for t in result.tracks] == [
            second_song,
            first_song,
        ]
    finally:
        records.unlink_discogs(record_id)
        records.remove_track(record_id, first_song)
        records.remove_track(record_id, second_song)
        records.delete(record_id)
        songs.delete(first_song, commit=True)
        songs.delete(second_song, commit=True)
        artists.delete(artist_id, commit=True)
        _drop_release(context, "990002")


def test_lookup_accepts_a_discogs_url(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    _add_release(context, "990003", "Nobody", "Via Url")

    try:
        result = discogs.lookup(
            "https://www.discogs.com/release/990003-Nobody-Via-Url"
        )

        assert result is not None
        assert result.release["release_id"] == "990003"
    finally:
        _drop_release(context, "990003")


def test_lookup_unknown_release_returns_none(discogs: DiscogsService) -> None:
    assert discogs.lookup("999999999") is None


def test_lookup_text_without_an_id_returns_none(
    discogs: DiscogsService,
) -> None:
    assert discogs.lookup("hello") is None
    assert discogs.lookup("") is None


# ============================================================
# list_releases
# ============================================================


def test_list_releases_filters_by_link_state(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    records = RecordService(context)
    record_id = records.create(title="Zzz List Record")
    _add_release(context, "990004", "A", "Linked One")
    _add_release(context, "990005", "A", "Unlinked One")
    records.link_discogs(record_id, "990004")

    try:
        linked = {r["release_id"]: r for r in discogs.list_releases(linked=True)}
        unlinked = {
            r["release_id"]: r for r in discogs.list_releases(linked=False)
        }
        everything = {r["release_id"] for r in discogs.list_releases()}

        assert "990004" in linked and "990005" not in linked
        assert "990005" in unlinked and "990004" not in unlinked
        assert {"990004", "990005"} <= everything
        assert linked["990004"]["RecordID"] == record_id
        assert linked["990004"]["RecordTitle"] == "Zzz List Record"
        assert unlinked["990005"]["RecordID"] is None
    finally:
        records.unlink_discogs(record_id)
        records.delete(record_id)
        _drop_release(context, "990004")
        _drop_release(context, "990005")


# ============================================================
# suggest_records
# ============================================================


def _record_with_artist(
    context: DatabaseContext, surname: str, title: str
) -> tuple[int, int]:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert({"Surname": surname}, commit=True)
    record_id = RecordService(context).create(title=title, artist_id=artist_id)
    return record_id, artist_id


def _drop_record(
    context: DatabaseContext, record_id: int, artist_id: int
) -> None:
    RecordService(context).delete(record_id)
    repository_for(context, "Artists").delete(artist_id, commit=True)


def test_suggest_records_ranks_the_matching_record_first(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    right_id, right_artist = _record_with_artist(
        context, "Zzzquux Band", "Zzzquux Anthem"
    )
    wrong_id, wrong_artist = _record_with_artist(
        context, "Other Group", "Something Else Entirely"
    )
    _add_release(context, "990006", "Zzzquux Band", "Zzzquux Anthem")

    try:
        suggestions = discogs.suggest_records("990006")

        assert suggestions
        assert suggestions[0].record["RecordID"] == right_id
        assert suggestions[0].score > 0.9
        assert all(
            suggestions[i].score >= suggestions[i + 1].score
            for i in range(len(suggestions) - 1)
        )
        assert wrong_id not in {s.record["RecordID"] for s in suggestions[:1]}
    finally:
        _drop_release(context, "990006")
        _drop_record(context, right_id, right_artist)
        _drop_record(context, wrong_id, wrong_artist)


def test_suggest_records_handles_artist_prefixed_title_and_suffix(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    # Real data: the record title carries the artist, and Discogs
    # adds a "(5)" disambiguation suffix to the artist name.
    record_id, artist_id = _record_with_artist(
        context, "Zzzalien", "Zzzalien Video Games"
    )
    _add_release(context, "990007", "Zzzalien (5)", "Video Games")

    try:
        suggestions = discogs.suggest_records("990007")

        assert suggestions
        assert suggestions[0].record["RecordID"] == record_id
    finally:
        _drop_release(context, "990007")
        _drop_record(context, record_id, artist_id)


def test_suggest_records_skips_records_already_linked(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    record_id, artist_id = _record_with_artist(
        context, "Zzzlinked Band", "Zzzlinked Title"
    )
    _add_release(context, "990008", "Zzzlinked Band", "Zzzlinked Title")
    _add_release(context, "990009", "Zzzlinked Band", "Zzzlinked Title")
    RecordService(context).link_discogs(record_id, "990008")

    try:
        suggestions = discogs.suggest_records("990009")

        assert record_id not in {s.record["RecordID"] for s in suggestions}
    finally:
        RecordService(context).unlink_discogs(record_id)
        _drop_release(context, "990008")
        _drop_release(context, "990009")
        _drop_record(context, record_id, artist_id)


def test_suggest_records_respects_limit(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    _add_release(context, "990010", "The", "A")

    try:
        assert len(discogs.suggest_records("990010", limit=2, minimum=0.0)) <= 2
    finally:
        _drop_release(context, "990010")


def test_suggest_records_unknown_release_returns_empty(
    discogs: DiscogsService,
) -> None:
    assert discogs.suggest_records("999999999") == []


# ============================================================
# confirm_match
# ============================================================


def test_confirm_match_links_release_to_record(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    record_id, artist_id = _record_with_artist(
        context, "Zzzconfirm Band", "Zzzconfirm Title"
    )
    _add_release(context, "990011", "Zzzconfirm Band", "Zzzconfirm Title")

    try:
        discogs.confirm_match("990011", record_id)

        result = discogs.lookup("990011")
        assert result is not None
        assert result.record is not None
        assert result.record["RecordID"] == record_id
    finally:
        RecordService(context).unlink_discogs(record_id)
        _drop_release(context, "990011")
        _drop_record(context, record_id, artist_id)


def test_confirm_match_rejects_release_already_linked_elsewhere(
    discogs: DiscogsService, context: DatabaseContext
) -> None:
    first_id, first_artist = _record_with_artist(context, "Zzzone", "Zzzone")
    second_id, second_artist = _record_with_artist(context, "Zzztwo", "Zzztwo")
    _add_release(context, "990012", "Zzzone", "Zzzone")
    discogs.confirm_match("990012", first_id)

    try:
        with pytest.raises(QueryError):
            discogs.confirm_match("990012", second_id)
    finally:
        RecordService(context).unlink_discogs(first_id)
        _drop_release(context, "990012")
        _drop_record(context, first_id, first_artist)
        _drop_record(context, second_id, second_artist)
