"""
=========================================================
Music Collection Manager
Concrete Service Tests
=========================================================

Milestone 3E

pytest tests for the concrete services built on top of
services/base_service.py.

Runs against the dedicated CRUD test database
(tests/Musi_crud_test.db), never the production database.
Every test cleans up any row it creates.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from core.context import DatabaseContext
from core.database import QueryError
from core.repository import RecordNotFoundError, repository_for
from services.artist_service import ArtistService, ArtistValidationError
from services.song_service import SongService, SongValidationError
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
def artists(context: DatabaseContext) -> ArtistService:
    """Provide an ArtistService bound to the CRUD test database."""

    return ArtistService(context)
@pytest.fixture()
def songs(context: DatabaseContext) -> SongService:
    """Provide a SongService bound to the CRUD test database."""

    return SongService(context)

# ============================================================
# Create / Read
# ============================================================


def test_create_and_get_artist(artists: ArtistService) -> None:
    artist_id = artists.create(surname="Testov", name="Alex")

    try:
        row = artists.get(artist_id)

        assert row is not None
        assert row["Surname"] == "Testov"
        assert row["Name"] == "Alex"
    finally:
        artists.delete(artist_id)


def test_create_rejects_blank_surname(artists: ArtistService) -> None:
    with pytest.raises(ArtistValidationError):
        artists.create(surname="   ")


def test_list_all_orders_by_surname_then_name(
    artists: ArtistService,
) -> None:
    first_id = artists.create(surname="Aaaaardvark")
    second_id = artists.create(surname="Zzzzyzx")

    try:
        rows = artists.list_all()

        index_first = next(
            i
            for i, row in enumerate(rows)
            if row["ArtistID"] == first_id
        )
        index_second = next(
            i
            for i, row in enumerate(rows)
            if row["ArtistID"] == second_id
        )

        assert index_first < index_second
    finally:
        artists.delete(first_id)
        artists.delete(second_id)


# ============================================================
# Update
# ============================================================


def test_update_changes_surname(artists: ArtistService) -> None:
    artist_id = artists.create(surname="Before")

    try:
        updated = artists.update(artist_id, surname="After")
        row = artists.require(artist_id)

        assert updated is True
        assert row["Surname"] == "After"
    finally:
        artists.delete(artist_id)


def test_update_clear_name(artists: ArtistService) -> None:
    artist_id = artists.create(surname="Hasaname", name="Something")

    try:
        artists.update(artist_id, clear_name=True)
        row = artists.require(artist_id)

        assert row["Name"] is None
    finally:
        artists.delete(artist_id)


def test_artist_update_requires_at_least_one_field(
    artists: ArtistService,
) -> None:
    artist_id = artists.create(surname="Lonely")

    try:
        with pytest.raises(ArtistValidationError):
            artists.update(artist_id)
    finally:
        artists.delete(artist_id)


def test_update_unknown_artist_raises_not_found(
    artists: ArtistService,
) -> None:
    with pytest.raises(RecordNotFoundError):
        artists.update(999_999_999, surname="Nobody")


# ============================================================
# Delete
# ============================================================


def test_delete_removes_artist(artists: ArtistService) -> None:
    artist_id = artists.create(surname="Temporary")

    artists.delete(artist_id)

    assert artists.get(artist_id) is None


# ============================================================
# Artist <-> Song relationship (Sing)
# ============================================================


def test_songs_for_artist_empty_when_no_links(
    artists: ArtistService,
) -> None:
    artist_id = artists.create(surname="NoSongsYet")

    try:
        assert artists.songs_for_artist(artist_id) == []
    finally:
        artists.delete(artist_id)


def test_add_and_remove_song_link(
    artists: ArtistService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    artist_id = artists.create(surname="LinkedArtist")

    try:
        artists.add_song(artist_id, existing_song["SongID"])

        linked = artists.songs_for_artist(artist_id)

        assert [
            song["SongID"] for song in linked
        ] == [existing_song["SongID"]]

        removed = artists.remove_song(
            artist_id,
            existing_song["SongID"],
        )

        assert removed is True
        assert artists.songs_for_artist(artist_id) == []
    finally:
        artists.delete(artist_id)


def test_add_song_twice_raises(
    artists: ArtistService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    artist_id = artists.create(surname="DoubleLinker")

    try:
        artists.add_song(artist_id, existing_song["SongID"])

        with pytest.raises(ArtistValidationError):
            artists.add_song(artist_id, existing_song["SongID"])
    finally:
        artists.remove_song(artist_id, existing_song["SongID"])
        artists.delete(artist_id)


def test_add_song_unknown_song_raises_not_found(
    artists: ArtistService,
) -> None:
    artist_id = artists.create(surname="WouldBeLinker")

    try:
        with pytest.raises(RecordNotFoundError):
            artists.add_song(artist_id, 999_999_999)
    finally:
        artists.delete(artist_id)


def test_delete_artist_with_song_link_raises(
    artists: ArtistService,
    context: DatabaseContext,
) -> None:
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    artist_id = artists.create(surname="StillLinked")

    artists.add_song(artist_id, existing_song["SongID"])

    try:
        with pytest.raises(QueryError):
            artists.delete(artist_id)
    finally:
        artists.remove_song(artist_id, existing_song["SongID"])
        artists.delete(artist_id)

# ============================================================
# SongService: Create / Read
# ============================================================


def test_create_and_get_song(songs: SongService) -> None:
    song_id = songs.create(title="Test Track", bpm=128.0, year=2026)

    try:
        row = songs.get(song_id)

        assert row is not None
        assert row["Title"] == "Test Track"
        assert row["BPM"] == 128.0
        assert row["Year"] == 2026
    finally:
        songs.delete(song_id)


def test_create_rejects_blank_title(songs: SongService) -> None:
    with pytest.raises(SongValidationError):
        songs.create(title="   ")


# ============================================================
# SongService: Update
# ============================================================


def test_update_changes_title(songs: SongService) -> None:
    song_id = songs.create(title="Before")

    try:
        updated = songs.update(song_id, title="After")
        row = songs.require(song_id)

        assert updated is True
        assert row["Title"] == "After"
    finally:
        songs.delete(song_id)


def test_update_clear_bpm(songs: SongService) -> None:
    song_id = songs.create(title="HasBPM", bpm=140.0)

    try:
        songs.update(song_id, clear_bpm=True)
        row = songs.require(song_id)

        assert row["BPM"] is None
    finally:
        songs.delete(song_id)


def test_song_update_requires_at_least_one_field(songs: SongService) -> None:
    song_id = songs.create(title="Lonely")

    try:
        with pytest.raises(SongValidationError):
            songs.update(song_id)
    finally:
        songs.delete(song_id)


def test_update_unknown_song_raises_not_found(
    songs: SongService,
) -> None:
    with pytest.raises(RecordNotFoundError):
        songs.update(999_999_999, title="Nobody")


# ============================================================
# SongService: Delete
# ============================================================


def test_delete_removes_song(songs: SongService) -> None:
    song_id = songs.create(title="Temporary")

    songs.delete(song_id)

    assert songs.get(song_id) is None


# ============================================================
# SongService: Song <-> Artist relationship (Sing)
# ============================================================


def test_artists_for_song_empty_when_no_links(
    songs: SongService,
) -> None:
    song_id = songs.create(title="NoArtistsYet")

    try:
        assert songs.artists_for_song(song_id) == []
    finally:
        songs.delete(song_id)


def test_add_and_remove_artist_link(
    songs: SongService,
    context: DatabaseContext,
) -> None:
    artists_repo = repository_for(context, "Artists")
    existing_artist = artists_repo.all(limit=1)[0]

    song_id = songs.create(title="LinkedSong")

    try:
        songs.add_artist(song_id, existing_artist["ArtistID"])

        linked = songs.artists_for_song(song_id)

        assert [
            artist["ArtistID"] for artist in linked
        ] == [existing_artist["ArtistID"]]

        removed = songs.remove_artist(
            song_id,
            existing_artist["ArtistID"],
        )

        assert removed is True
        assert songs.artists_for_song(song_id) == []
    finally:
        songs.delete(song_id)


def test_add_artist_twice_raises(
    songs: SongService,
    context: DatabaseContext,
) -> None:
    artists_repo = repository_for(context, "Artists")
    existing_artist = artists_repo.all(limit=1)[0]

    song_id = songs.create(title="DoubleLinkedSong")

    try:
        songs.add_artist(song_id, existing_artist["ArtistID"])

        with pytest.raises(SongValidationError):
            songs.add_artist(song_id, existing_artist["ArtistID"])
    finally:
        songs.remove_artist(song_id, existing_artist["ArtistID"])
        songs.delete(song_id)


# ============================================================
# SongService: Song <-> Style relationship (Belong)
# ============================================================


def test_styles_for_song_empty_when_no_links(
    songs: SongService,
) -> None:
    song_id = songs.create(title="NoStylesYet")

    try:
        assert songs.styles_for_song(song_id) == []
    finally:
        songs.delete(song_id)


def test_add_and_remove_style_link(
    songs: SongService,
    context: DatabaseContext,
) -> None:
    styles_repo = repository_for(context, "Styles")
    existing_style = styles_repo.all(limit=1)[0]

    song_id = songs.create(title="StyledSong")

    try:
        songs.add_style(song_id, existing_style["StyleID"])

        linked = songs.styles_for_song(song_id)

        assert [
            style["StyleID"] for style in linked
        ] == [existing_style["StyleID"]]

        removed = songs.remove_style(
            song_id,
            existing_style["StyleID"],
        )

        assert removed is True
        assert songs.styles_for_song(song_id) == []
    finally:
        songs.delete(song_id)


def test_add_style_twice_raises(
    songs: SongService,
    context: DatabaseContext,
) -> None:
    styles_repo = repository_for(context, "Styles")
    existing_style = styles_repo.all(limit=1)[0]

    song_id = songs.create(title="DoubleStyledSong")

    try:
        songs.add_style(song_id, existing_style["StyleID"])

        with pytest.raises(SongValidationError):
            songs.add_style(song_id, existing_style["StyleID"])
    finally:
        songs.remove_style(song_id, existing_style["StyleID"])
        songs.delete(song_id)


# ============================================================
# SongService: Song -> Record relationship (Contain, read-only)
# ============================================================


def test_records_for_song_reflects_existing_contain_rows(
    context: DatabaseContext,
    songs: SongService,
) -> None:
    contain = repository_for(context, "Contain")
    existing_link = contain.all(limit=1)[0]

    records = songs.records_for_song(existing_link["SongID"])

    matching = [
        record
        for record in records
        if record["RecordID"] == existing_link["RecordID"]
    ]

    assert len(matching) == 1
    assert matching[0]["Position"] == existing_link["Position"]


def test_records_for_song_empty_for_new_song(
    songs: SongService,
) -> None:
    song_id = songs.create(title="NotOnAnyRecordYet")

    try:
        assert songs.records_for_song(song_id) == []
    finally:
        songs.delete(song_id)