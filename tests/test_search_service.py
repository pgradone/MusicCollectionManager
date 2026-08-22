"""
=========================================================
Music Collection Manager
Search Service Tests
=========================================================

Milestone 5B (1/N)

pytest tests for services/search_service.py.

Runs against the dedicated CRUD test database
(tests/Musi_crud_test.db), never the production database.
Every test cleans up any row it creates.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from core.context import DatabaseContext
from core.repository import repository_for
from services.search_service import SearchService

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
def search(context: DatabaseContext) -> SearchService:
    """Provide a SearchService bound to the CRUD test database."""

    return SearchService(context)


# ============================================================
# Blank query
# ============================================================


def test_blank_query_returns_nothing(search: SearchService) -> None:
    assert search.search("") == []
    assert search.search("   ") == []


# ============================================================
# Per-entity matching
# ============================================================


def test_matches_artist_by_surname(
    search: SearchService, context: DatabaseContext
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert(
        {"Surname": "ZzzSearchTestSurname", "Name": "Alex"}, commit=True
    )

    try:
        results = search.search("zzzsearchtestsurname")
        matching = [r for r in results if r.primary_key_value == artist_id]
        assert len(matching) == 1
        assert matching[0].table == "Artists"
        assert matching[0].primary_key_column == "ArtistID"
    finally:
        artists.delete(artist_id, commit=True)


def test_matches_artist_by_name_not_just_surname(
    search: SearchService, context: DatabaseContext
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert(
        {"Surname": "SomeoneElse", "Name": "ZzzSearchTestFirstName"},
        commit=True,
    )

    try:
        results = search.search("zzzsearchtestfirstname")
        assert any(r.primary_key_value == artist_id for r in results)
    finally:
        artists.delete(artist_id, commit=True)


def test_matches_song_by_title(
    search: SearchService, context: DatabaseContext
) -> None:
    songs = repository_for(context, "Songs")
    song_id = songs.insert({"Title": "ZzzSearchTestSongTitle"}, commit=True)

    try:
        results = search.search("searchtestsongtitle")
        matching = [r for r in results if r.primary_key_value == song_id]
        assert len(matching) == 1
        assert matching[0].table == "Songs"
        assert matching[0].primary_key_column == "SongID"
    finally:
        songs.delete(song_id, commit=True)


def test_matches_record_by_title(
    search: SearchService, context: DatabaseContext
) -> None:
    records = repository_for(context, "Records")
    record_id = records.insert(
        {"Title": "ZzzSearchTestRecordTitle"}, commit=True
    )

    try:
        results = search.search("searchtestrecordtitle")
        matching = [r for r in results if r.primary_key_value == record_id]
        assert len(matching) == 1
        assert matching[0].table == "Records"
        assert matching[0].primary_key_column == "RecordID"
    finally:
        records.delete(record_id, commit=True)


def test_matches_program_by_name(
    search: SearchService, context: DatabaseContext
) -> None:
    programs = repository_for(context, "Programs")
    program_id = programs.insert(
        {"ProgName": "ZzzSearchTestProgName"}, commit=True
    )

    try:
        results = search.search("searchtestprogname")
        matching = [r for r in results if r.primary_key_value == program_id]
        assert len(matching) == 1
        assert matching[0].table == "Programs"
        assert matching[0].primary_key_column == "ProgramID"
    finally:
        programs.delete(program_id, commit=True)


def test_matches_program_by_description_not_just_name(
    search: SearchService, context: DatabaseContext
) -> None:
    programs = repository_for(context, "Programs")
    program_id = programs.insert(
        {
            "ProgName": "UnrelatedName",
            "Description": "ZzzSearchTestDescriptionText",
        },
        commit=True,
    )

    try:
        results = search.search("searchtestdescriptiontext")
        assert any(r.primary_key_value == program_id for r in results)
    finally:
        programs.delete(program_id, commit=True)


def test_matches_style_by_label(
    search: SearchService, context: DatabaseContext
) -> None:
    styles = repository_for(context, "Styles")
    style_id = styles.insert(
        {"Label": "ZzzSearchTestStyleLabel"}, commit=True
    )

    try:
        results = search.search("searchteststylelabel")
        matching = [r for r in results if r.primary_key_value == style_id]
        assert len(matching) == 1
        assert matching[0].table == "Styles"
        assert matching[0].primary_key_column == "StyleID"
    finally:
        styles.delete(style_id, commit=True)


# ============================================================
# Matching semantics
# ============================================================


def test_matching_is_case_insensitive(
    search: SearchService, context: DatabaseContext
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert(
        {"Surname": "ZzzMixedCaseTest"}, commit=True
    )

    try:
        assert any(
            r.primary_key_value == artist_id
            for r in search.search("ZZZMIXEDCASETEST")
        )
        assert any(
            r.primary_key_value == artist_id
            for r in search.search("zzzmixedcasetest")
        )
    finally:
        artists.delete(artist_id, commit=True)


def test_matching_is_substring_not_prefix_only(
    search: SearchService, context: DatabaseContext
) -> None:
    songs = repository_for(context, "Songs")
    song_id = songs.insert(
        {"Title": "Prefix ZzzMiddleSubstring Suffix"}, commit=True
    )

    try:
        results = search.search("zzzmiddlesubstring")
        assert any(r.primary_key_value == song_id for r in results)
    finally:
        songs.delete(song_id, commit=True)


def test_no_match_returns_empty(search: SearchService) -> None:
    assert search.search("ZzzThisStringShouldMatchNothingAtAll") == []