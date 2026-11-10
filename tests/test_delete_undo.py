"""
=========================================================
Music Collection Manager
Delete Undo Tests
=========================================================

Milestone 7B (1/N)

pytest tests for services/delete_undo.py.

Runs against the dedicated CRUD test database
(tests/Musi_crud_test.db) with covers kept in pytest's tmp_path, so
neither the production database nor the real artwork folder is
touched. Every test removes the rows it creates.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from core.context import DatabaseContext
from core.database import QueryError
from core.repository import RecordNotFoundError, repository_for
from services.artwork_service import ArtworkError, ArtworkService
from services.delete_undo import DeleteUndo, UndoError
from services.record_service import RecordService

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATABASE = PROJECT_ROOT / "tests" / "Musi_crud_test.db"


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
def artwork(tmp_path: Path) -> ArtworkService:
    return ArtworkService(tmp_path / "artwork")


@pytest.fixture()
def undo(context: DatabaseContext, artwork: ArtworkService) -> DeleteUndo:
    return DeleteUndo(context, artwork)


def picture(tmp_path: Path) -> Path:
    path = tmp_path / "cover.png"
    Image.new("RGB", (80, 60), (10, 200, 90)).save(path)
    return path


# ============================================================
# delete + restore
# ============================================================


def test_restore_brings_back_exactly_the_deleted_row(
    undo: DeleteUndo, context: DatabaseContext
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert(
        {"Surname": "ZzzUndoArtist", "Name": "Alex"}, commit=True
    )
    original = dict(artists.require(artist_id))

    try:
        deleted = undo.delete("Artists", artist_id)

        assert artists.get(artist_id) is None
        assert deleted.row == original
        assert undo.last is deleted

        result = undo.restore()

        assert dict(artists.require(artist_id)) == original
        assert result.record is deleted
        assert result.cover_restored is None
        assert undo.last is None
    finally:
        artists.delete(artist_id, commit=True)


@pytest.mark.parametrize(
    ("table", "values"),
    [
        ("Artists", {"Surname": "ZzzUndoEach"}),
        ("Songs", {"Title": "ZzzUndoEach", "BPM": 123.5, "Year": 99}),
        ("Records", {"Title": "ZzzUndoEach", "Val2026": 12}),
        ("Programs", {"ProgName": "ZzzUndoEach", "Description": "d"}),
        ("Styles", {"Label": "ZzzUndoEach"}),
    ],
)
def test_every_main_table_can_be_restored(
    undo: DeleteUndo,
    context: DatabaseContext,
    table: str,
    values: dict[str, object],
) -> None:
    repository = repository_for(context, table)
    key = repository.insert(values, commit=True)
    original = dict(repository.require(key))

    try:
        undo.delete(table, key)
        assert repository.get(key) is None

        undo.restore()

        assert dict(repository.require(key)) == original
    finally:
        repository.delete(key, commit=True)


def test_a_record_keeps_its_discogs_link_when_restored(
    undo: DeleteUndo, context: DatabaseContext
) -> None:
    records = RecordService(context)
    record_id = records.create(title="ZzzUndoDiscogs")
    repository_for(context, "Discogs").insert(
        {"ID": 990999, "release_id": "990999", "Artist": "A", "Title": "T"},
        commit=True,
    )
    records.link_discogs(record_id, "990999")

    try:
        undo.delete("Records", record_id)
        undo.restore()

        assert records.require(record_id)["Discogs_release"] == "990999"
    finally:
        records.unlink_discogs(record_id)
        records.delete(record_id)
        repository_for(context, "Discogs").delete("990999", commit=True)


# ============================================================
# covers
# ============================================================


def test_a_records_cover_goes_with_the_deletion_and_comes_back(
    undo: DeleteUndo,
    context: DatabaseContext,
    artwork: ArtworkService,
    tmp_path: Path,
) -> None:
    records = RecordService(context)
    record_id = records.create(title="ZzzUndoCover")
    artwork.set_image(record_id, picture(tmp_path))
    original_bytes = artwork.path_for(record_id).read_bytes()

    try:
        undo.delete("Records", record_id)
        assert artwork.get(record_id) is None  # not left behind

        result = undo.restore()

        assert result.cover_restored is True
        assert artwork.path_for(record_id).read_bytes() == original_bytes
    finally:
        records.delete(record_id)


def test_the_record_is_restored_even_if_its_cover_cannot_be_written(
    undo: DeleteUndo,
    context: DatabaseContext,
    artwork: ArtworkService,
    tmp_path: Path,
) -> None:
    records = RecordService(context)
    record_id = records.create(title="ZzzUndoCoverFails")
    artwork.set_image(record_id, picture(tmp_path))

    try:
        undo.delete("Records", record_id)

        with patch.object(
            artwork, "write_raw", side_effect=ArtworkError("disk full")
        ):
            result = undo.restore()

        assert result.cover_restored is False
        assert records.get(record_id) is not None
    finally:
        records.delete(record_id)


def test_only_records_have_covers_so_other_tables_never_touch_them(
    undo: DeleteUndo,
    context: DatabaseContext,
    artwork: ArtworkService,
    tmp_path: Path,
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert({"Surname": "ZzzUndoOther"}, commit=True)
    artwork.set_image(artist_id, picture(tmp_path))  # same number, other table

    try:
        undo.delete("Artists", artist_id)

        assert artwork.get(artist_id) is not None
        assert undo.last is not None and undo.last.cover is None
    finally:
        undo.restore()
        artists.delete(artist_id, commit=True)


# ============================================================
# refusals
# ============================================================


def test_nothing_to_restore_is_an_error(undo: DeleteUndo) -> None:
    with pytest.raises(UndoError, match="nothing to restore"):
        undo.restore()


def test_a_restore_happens_only_once(
    undo: DeleteUndo, context: DatabaseContext
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert({"Surname": "ZzzUndoOnce"}, commit=True)

    try:
        undo.delete("Artists", artist_id)
        undo.restore()

        with pytest.raises(UndoError):
            undo.restore()
    finally:
        artists.delete(artist_id, commit=True)


def test_only_the_most_recent_deletion_is_remembered(
    undo: DeleteUndo, context: DatabaseContext
) -> None:
    artists = repository_for(context, "Artists")
    first = artists.insert({"Surname": "ZzzUndoFirst"}, commit=True)
    second = artists.insert({"Surname": "ZzzUndoSecond"}, commit=True)

    try:
        undo.delete("Artists", first)
        undo.delete("Artists", second)

        undo.restore()

        assert artists.get(second) is not None
        assert artists.get(first) is None  # the earlier one is gone for good
    finally:
        artists.delete(second, commit=True)


def test_restore_refuses_when_the_id_has_been_taken_since(
    undo: DeleteUndo, context: DatabaseContext
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert({"Surname": "ZzzUndoTaken"}, commit=True)

    try:
        undo.delete("Artists", artist_id)
        # SQLite may give a deleted row's ID to a new one - simulate that.
        artists.insert(
            {"ArtistID": artist_id, "Surname": "ZzzUndoNewcomer"}, commit=True
        )

        with pytest.raises(UndoError, match=f"Artists #{artist_id}"):
            undo.restore()

        assert artists.require(artist_id)["Surname"] == "ZzzUndoNewcomer"
        assert undo.last is not None  # still remembered
    finally:
        artists.delete(artist_id, commit=True)


def test_a_deletion_the_database_refuses_loses_and_remembers_nothing(
    undo: DeleteUndo,
    context: DatabaseContext,
    artwork: ArtworkService,
    tmp_path: Path,
) -> None:
    # A record with a track is protected by a foreign key.
    records = RecordService(context)
    songs = repository_for(context, "Songs")
    record_id = records.create(title="ZzzUndoBlocked")
    song_id = songs.insert({"Title": "ZzzUndoBlockedSong"}, commit=True)
    records.add_track(record_id, song_id, position="A1")
    artwork.set_image(record_id, picture(tmp_path))

    try:
        with pytest.raises(QueryError):
            undo.delete("Records", record_id)

        assert records.get(record_id) is not None
        assert artwork.get(record_id) is not None  # cover untouched
        assert undo.last is None
    finally:
        records.remove_track(record_id, song_id)
        songs.delete(song_id, commit=True)
        records.delete(record_id)


def test_deleting_a_row_that_does_not_exist_is_an_error(
    undo: DeleteUndo,
) -> None:
    with pytest.raises(RecordNotFoundError):
        undo.delete("Artists", 987654321)

    assert undo.last is None
