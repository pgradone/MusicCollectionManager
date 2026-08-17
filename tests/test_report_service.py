"""
=========================================================
Music Collection Manager
Report Service Tests
=========================================================

Milestone 5A (1/N)

pytest tests for services/report_service.py.

Runs against the dedicated CRUD test database
(tests/Musi_crud_test.db), never the production database.
Every test cleans up any row it creates.

Assertions compare before/after deltas rather than absolute
numbers, since the CRUD test database already has substantial
seed data - a delta check is correct regardless of what that
seed data happens to contain.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from core.context import DatabaseContext
from core.repository import repository_for
from services.report_service import ReportService

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATABASE = PROJECT_ROOT / "tests" / "Musi_crud_test.db"


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture()
def context() -> Iterator[DatabaseContext]:
    """
    Provide a DatabaseContext pointed at the dedicated CRUD
    test database, restoring the singleton's original database
    path afterwards so later tests are unaffected.
    """

    if not TEST_DATABASE.exists():
        raise FileNotFoundError(
            f"Test database not found:\n{TEST_DATABASE}"
        )

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
def reports(context: DatabaseContext) -> ReportService:
    """Provide a ReportService bound to the CRUD test database."""

    return ReportService(context)


# ============================================================
# Counts
# ============================================================


def test_counts_match_repository_counts(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    stats = reports.dashboard_stats()

    assert stats.artist_count == repository_for(context, "Artists").count()
    assert stats.song_count == repository_for(context, "Songs").count()
    assert stats.record_count == repository_for(context, "Records").count()
    assert stats.program_count == repository_for(context, "Programs").count()
    assert stats.style_count == repository_for(context, "Styles").count()


# ============================================================
# Missing metadata
# ============================================================


def test_songs_missing_bpm_increases_for_song_without_bpm(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    before = reports.dashboard_stats().songs_missing_bpm

    song_id = songs.insert({"Title": "NoBpmTestSong"}, commit=True)

    try:
        after = reports.dashboard_stats().songs_missing_bpm
        assert after == before + 1
    finally:
        songs.delete(song_id, commit=True)


def test_songs_missing_bpm_unchanged_for_song_with_bpm(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    before = reports.dashboard_stats().songs_missing_bpm

    song_id = songs.insert(
        {"Title": "HasBpmTestSong", "BPM": 128.0}, commit=True
    )

    try:
        after = reports.dashboard_stats().songs_missing_bpm
        assert after == before
    finally:
        songs.delete(song_id, commit=True)


def test_records_missing_artist_increases_for_record_without_artist(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    records = repository_for(context, "Records")
    before = reports.dashboard_stats().records_missing_artist

    record_id = records.insert(
        {"Title": "NoArtistTestRecord"}, commit=True
    )

    try:
        after = reports.dashboard_stats().records_missing_artist
        assert after == before + 1
    finally:
        records.delete(record_id, commit=True)


# ============================================================
# Average BPM
# ============================================================


def test_average_bpm_recomputes_with_new_song(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    before = reports.dashboard_stats()
    assert before.average_bpm is not None

    song_id = songs.insert(
        {"Title": "KnownBpmTestSong", "BPM": 100.0}, commit=True
    )

    try:
        after = reports.dashboard_stats()
        assert after.songs_with_bpm == before.songs_with_bpm + 1

        expected_avg = (
            before.average_bpm * before.songs_with_bpm + 100.0
        ) / after.songs_with_bpm
        assert after.average_bpm is not None
        assert abs(after.average_bpm - expected_avg) < 1e-9
    finally:
        songs.delete(song_id, commit=True)


# ============================================================
# Collection value
# ============================================================


def test_collection_value_includes_unsold_valued_record(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    records = repository_for(context, "Records")
    before = reports.dashboard_stats().collection_value_eur

    record_id = records.insert(
        {"Title": "ValuedTestRecord", "Val2026": 50}, commit=True
    )

    try:
        after = reports.dashboard_stats().collection_value_eur
        assert after == pytest.approx(before + 50)
    finally:
        records.delete(record_id, commit=True)


def test_collection_value_excludes_sold_record(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    records = repository_for(context, "Records")
    before = reports.dashboard_stats()

    record_id = records.insert(
        {
            "Title": "SoldTestRecord",
            "Val2026": 999,
            "soldDate": "2026-01-01",
            "soldValEur": 75,
        },
        commit=True,
    )

    try:
        after = reports.dashboard_stats()
        # Sold, so its Val2026 must NOT be counted as current value.
        assert after.collection_value_eur == pytest.approx(
            before.collection_value_eur
        )
        assert after.sold_value_eur == pytest.approx(
            before.sold_value_eur + 75
        )
        assert after.sold_record_count == before.sold_record_count + 1
        assert (
            after.unsold_record_count == before.unsold_record_count
        )
    finally:
        records.delete(record_id, commit=True)


# ============================================================
# Recently added programs
# ============================================================


def test_recently_added_programs_puts_newest_first(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    programs = repository_for(context, "Programs")

    program_id = programs.insert(
        {
            "ProgName": "RecentTestProgram",
            "DateCreate": "2099-01-01 00:00:00",
        },
        commit=True,
    )

    try:
        stats = reports.dashboard_stats(recent_limit=1)
        assert stats.recently_added_programs[0]["ProgramID"] == program_id
    finally:
        programs.delete(program_id, commit=True)


def test_recent_limit_controls_result_count(
    reports: ReportService,
) -> None:
    stats = reports.dashboard_stats(recent_limit=3)

    assert len(stats.recently_added_programs) == 3

# ============================================================
# Integrity / anomaly reports
# ============================================================


def test_songs_without_artists_includes_new_unlinked_song(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    song_id = songs.insert({"Title": "UnlinkedArtistTestSong"}, commit=True)

    try:
        results = reports.songs_without_artists()
        assert any(song["SongID"] == song_id for song in results)
    finally:
        songs.delete(song_id, commit=True)


def test_songs_without_artists_excludes_linked_song(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    sing = repository_for(context, "Sing")
    artists = repository_for(context, "Artists")
    existing_artist = artists.all(limit=1)[0]

    song_id = songs.insert({"Title": "LinkedArtistTestSong"}, commit=True)
    sing.insert(
        {"ArtistID": existing_artist["ArtistID"], "SongID": song_id},
        commit=True,
    )

    try:
        results = reports.songs_without_artists()
        assert all(song["SongID"] != song_id for song in results)
    finally:
        sing.delete(
            {"ArtistID": existing_artist["ArtistID"], "SongID": song_id},
            commit=True,
        )
        songs.delete(song_id, commit=True)


def test_songs_without_records_includes_new_unlinked_song(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    song_id = songs.insert({"Title": "UnlinkedRecordTestSong"}, commit=True)

    try:
        results = reports.songs_without_records()
        assert any(song["SongID"] == song_id for song in results)
    finally:
        songs.delete(song_id, commit=True)


def test_artists_without_songs_includes_new_unlinked_artist(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert(
        {"Surname": "UnlinkedSongsTestArtist"}, commit=True
    )

    try:
        results = reports.artists_without_songs()
        assert any(
            artist["ArtistID"] == artist_id for artist in results
        )
    finally:
        artists.delete(artist_id, commit=True)


def test_records_without_songs_includes_new_unlinked_record(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    records = repository_for(context, "Records")
    record_id = records.insert(
        {"Title": "UnlinkedSongsTestRecord"}, commit=True
    )

    try:
        results = reports.records_without_songs()
        assert any(
            record["RecordID"] == record_id for record in results
        )
    finally:
        records.delete(record_id, commit=True)


def test_duplicate_artists_finds_case_insensitive_match(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    artists = repository_for(context, "Artists")
    first_id = artists.insert(
        {"Surname": "DupeTestSurname", "Name": "Alex"}, commit=True
    )
    second_id = artists.insert(
        {"Surname": "  dupetestsurname  ", "Name": "ALEX"}, commit=True
    )

    try:
        groups = reports.duplicate_artists()
        matching_group = next(
            (
                group
                for group in groups
                if any(a["ArtistID"] == first_id for a in group)
            ),
            None,
        )
        assert matching_group is not None
        found_ids = {a["ArtistID"] for a in matching_group}
        assert found_ids == {first_id, second_id}
    finally:
        artists.delete(first_id, commit=True)
        artists.delete(second_id, commit=True)


def test_duplicate_artists_never_groups_null_surnames(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    artists = repository_for(context, "Artists")
    first_id = artists.insert({"Surname": "NoSurnameA"}, commit=True)
    # Two artists with genuinely no surname must never be treated as
    # duplicates of each other.
    second_id = artists.insert({"Surname": "NoSurnameB"}, commit=True)

    try:
        groups = reports.duplicate_artists()
        for group in groups:
            group_ids = {a["ArtistID"] for a in group}
            assert not ({first_id, second_id} <= group_ids)
    finally:
        artists.delete(first_id, commit=True)
        artists.delete(second_id, commit=True)


def test_songs_sung_by_many_artists_includes_collaboration(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    artists = repository_for(context, "Artists")
    sing = repository_for(context, "Sing")

    song_id = songs.insert({"Title": "CollabTestSong"}, commit=True)
    artist_a_id = artists.insert(
        {"Surname": "CollabArtistA"}, commit=True
    )
    artist_b_id = artists.insert(
        {"Surname": "CollabArtistB"}, commit=True
    )
    sing.insert({"ArtistID": artist_a_id, "SongID": song_id}, commit=True)
    sing.insert({"ArtistID": artist_b_id, "SongID": song_id}, commit=True)

    try:
        results = reports.songs_sung_by_many_artists()
        entry = next(
            (song for song in results if song["SongID"] == song_id),
            None,
        )
        assert entry is not None
        found_artist_ids = {a["ArtistID"] for a in entry["artists"]}
        assert found_artist_ids == {artist_a_id, artist_b_id}
    finally:
        sing.delete(
            {"ArtistID": artist_a_id, "SongID": song_id}, commit=True
        )
        sing.delete(
            {"ArtistID": artist_b_id, "SongID": song_id}, commit=True
        )
        songs.delete(song_id, commit=True)
        artists.delete(artist_a_id, commit=True)
        artists.delete(artist_b_id, commit=True)


def test_songs_sung_by_many_artists_excludes_single_artist_song(
    reports: ReportService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    artists = repository_for(context, "Artists")
    sing = repository_for(context, "Sing")

    song_id = songs.insert({"Title": "SoloTestSong"}, commit=True)
    artist_id = artists.insert({"Surname": "SoloTestArtist"}, commit=True)
    sing.insert({"ArtistID": artist_id, "SongID": song_id}, commit=True)

    try:
        results = reports.songs_sung_by_many_artists()
        assert all(song["SongID"] != song_id for song in results)
    finally:
        sing.delete({"ArtistID": artist_id, "SongID": song_id}, commit=True)
        songs.delete(song_id, commit=True)
        artists.delete(artist_id, commit=True)