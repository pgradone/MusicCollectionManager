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
from services.program_service import ProgramService, ProgramValidationError
from services.record_service import RecordService, RecordValidationError
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
@pytest.fixture()
def records(context: DatabaseContext) -> RecordService:
    """Provide a RecordService bound to the CRUD test database."""

    return RecordService(context)
@pytest.fixture()
def programs(context: DatabaseContext) -> ProgramService:
    """Provide a ProgramService bound to the CRUD test database."""

    return ProgramService(context)

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

# ============================================================
# RecordService: Create / Read
# ============================================================


def test_record_create_and_get(records: RecordService) -> None:
    record_id = records.create(title="Test Record", support="LP Vinyl")

    try:
        row = records.get(record_id)

        assert row is not None
        assert row["Title"] == "Test Record"
        assert row["Support"] == "LP Vinyl"
    finally:
        records.delete(record_id)


def test_record_create_rejects_blank_title(
    records: RecordService,
) -> None:
    with pytest.raises(RecordValidationError):
        records.create(title="   ")


def test_record_create_validates_artist_exists(
    records: RecordService,
) -> None:
    with pytest.raises(RecordNotFoundError):
        records.create(title="Orphan", artist_id=999_999_999)


# ============================================================
# RecordService: Update
# ============================================================


def test_record_update_changes_title(records: RecordService) -> None:
    record_id = records.create(title="Before")

    try:
        updated = records.update(record_id, title="After")
        row = records.require(record_id)

        assert updated is True
        assert row["Title"] == "After"
    finally:
        records.delete(record_id)


def test_record_update_requires_at_least_one_field(
    records: RecordService,
) -> None:
    record_id = records.create(title="Lonely")

    try:
        with pytest.raises(RecordValidationError):
            records.update(record_id)
    finally:
        records.delete(record_id)


def test_record_update_unknown_record_raises_not_found(
    records: RecordService,
) -> None:
    with pytest.raises(RecordNotFoundError):
        records.update(999_999_999, title="Nobody")


# ============================================================
# RecordService: Delete
# ============================================================


def test_record_delete_removes_record(records: RecordService) -> None:
    record_id = records.create(title="Temporary")

    records.delete(record_id)

    assert records.get(record_id) is None


# ============================================================
# RecordService: Record -> Artist (direct foreign key)
# ============================================================


def test_record_artist_for_record_none_when_unset(
    records: RecordService,
) -> None:
    record_id = records.create(title="NoArtist")

    try:
        assert records.artist_for_record(record_id) is None
    finally:
        records.delete(record_id)


def test_record_artist_for_record_returns_artist(
    records: RecordService,
    context: DatabaseContext,
) -> None:
    artists_repo = repository_for(context, "Artists")
    existing_artist = artists_repo.all(limit=1)[0]

    record_id = records.create(
        title="HasArtist",
        artist_id=existing_artist["ArtistID"],
    )

    try:
        artist = records.artist_for_record(record_id)

        assert artist is not None
        assert artist["ArtistID"] == existing_artist["ArtistID"]
    finally:
        records.delete(record_id)


# ============================================================
# RecordService: Record -> Tracks (Contain)
# ============================================================


def test_record_tracks_for_record_empty_when_no_tracks(
    records: RecordService,
) -> None:
    record_id = records.create(title="NoTracksYet")

    try:
        assert records.tracks_for_record(record_id) == []
    finally:
        records.delete(record_id)


def test_record_add_and_remove_track(
    records: RecordService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]

    record_id = records.create(title="TrackedRecord")

    try:
        records.add_track(
            record_id,
            existing_song["SongID"],
            position="A1",
        )

        tracks = records.tracks_for_record(record_id)

        assert [track["SongID"] for track in tracks] == [
            existing_song["SongID"]
        ]
        assert tracks[0]["Position"] == "A1"

        removed = records.remove_track(
            record_id,
            existing_song["SongID"],
        )

        assert removed is True
        assert records.tracks_for_record(record_id) == []
    finally:
        records.delete(record_id)


def test_record_add_track_twice_raises(
    records: RecordService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]

    record_id = records.create(title="DoubleTrackRecord")

    try:
        records.add_track(record_id, existing_song["SongID"])

        with pytest.raises(RecordValidationError):
            records.add_track(record_id, existing_song["SongID"])
    finally:
        records.remove_track(record_id, existing_song["SongID"])
        records.delete(record_id)


def test_record_add_track_duplicate_position_raises(
    records: RecordService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    first_song, second_song = songs_repo.all(limit=2)

    record_id = records.create(title="CollidingPositions")

    try:
        records.add_track(
            record_id, first_song["SongID"], position="A1"
        )

        with pytest.raises(RecordValidationError):
            records.add_track(
                record_id, second_song["SongID"], position="A1"
            )
    finally:
        records.remove_track(record_id, first_song["SongID"])
        records.delete(record_id)


def test_record_reorder_track_changes_position(
    records: RecordService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]

    record_id = records.create(title="ReorderedRecord")

    try:
        records.add_track(
            record_id, existing_song["SongID"], position="A1"
        )

        records.reorder_track(
            record_id, existing_song["SongID"], "B3"
        )

        tracks = records.tracks_for_record(record_id)

        assert tracks[0]["Position"] == "B3"
    finally:
        records.remove_track(record_id, existing_song["SongID"])
        records.delete(record_id)


def test_record_delete_with_track_raises(
    records: RecordService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]

    record_id = records.create(title="StillHasTrack")
    records.add_track(record_id, existing_song["SongID"])

    try:
        with pytest.raises(QueryError):
            records.delete(record_id)
    finally:
        records.remove_track(record_id, existing_song["SongID"])
        records.delete(record_id)


# ============================================================
# RecordService: Record -> Discogs (optional single link)
# ============================================================


def test_record_link_and_unlink_discogs(
    records: RecordService,
    context: DatabaseContext,
) -> None:
    discogs_repo = repository_for(context, "Discogs")
    linked_releases = {
        row["Discogs_release"]
        for row in repository_for(context, "Records").find(
            {}
        )
        if row["Discogs_release"] is not None
    }
    free_release = next(
        row["release_id"]
        for row in discogs_repo.all(limit=20)
        if row["release_id"] not in linked_releases
    )

    record_id = records.create(title="DiscogsLinked")

    try:
        assert records.discogs_info(record_id) is None

        records.link_discogs(record_id, free_release)

        info = records.discogs_info(record_id)
        assert info is not None
        assert info["release_id"] == free_release

        records.unlink_discogs(record_id)

        assert records.discogs_info(record_id) is None
    finally:
        records.delete(record_id)


def test_record_link_discogs_unknown_release_raises(
    records: RecordService,
) -> None:
    record_id = records.create(title="BadDiscogsLink")

    try:
        with pytest.raises(RecordNotFoundError):
            records.link_discogs(record_id, "no-such-release-id")
    finally:
        records.delete(record_id)

# ============================================================
# ProgramService: Create / Read
# ============================================================


def test_program_create_and_get(programs: ProgramService) -> None:
    program_id = programs.create(
        prog_name="Test Show",
        description="A test broadcast",
    )

    try:
        row = programs.get(program_id)

        assert row is not None
        assert row["ProgName"] == "Test Show"
        assert row["Description"] == "A test broadcast"
    finally:
        programs.delete(program_id)


def test_program_create_rejects_blank_name(
    programs: ProgramService,
) -> None:
    with pytest.raises(ProgramValidationError):
        programs.create(prog_name="   ")


# ============================================================
# ProgramService: Update
# ============================================================


def test_program_update_changes_name(
    programs: ProgramService,
) -> None:
    program_id = programs.create(prog_name="Before")

    try:
        updated = programs.update(program_id, prog_name="After")
        row = programs.require(program_id)

        assert updated is True
        assert row["ProgName"] == "After"
    finally:
        programs.delete(program_id)


def test_program_update_requires_at_least_one_field(
    programs: ProgramService,
) -> None:
    program_id = programs.create(prog_name="Lonely")

    try:
        with pytest.raises(ProgramValidationError):
            programs.update(program_id)
    finally:
        programs.delete(program_id)


def test_program_update_unknown_program_raises_not_found(
    programs: ProgramService,
) -> None:
    with pytest.raises(RecordNotFoundError):
        programs.update(999_999_999, prog_name="Nobody")


# ============================================================
# ProgramService: Delete
# ============================================================


def test_program_delete_removes_program(
    programs: ProgramService,
) -> None:
    program_id = programs.create(prog_name="Temporary")

    programs.delete(program_id)

    assert programs.get(program_id) is None


# ============================================================
# ProgramService: Program -> Schedule (running order)
# ============================================================


def test_program_schedule_empty_when_no_songs(
    programs: ProgramService,
) -> None:
    program_id = programs.create(prog_name="EmptyShow")

    try:
        assert programs.schedule_for_program(program_id) == []
    finally:
        programs.delete(program_id)


def test_program_add_and_remove_song(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]

    program_id = programs.create(prog_name="ScheduledShow")

    try:
        programs.add_song(
            program_id,
            1.0,
            song_id=existing_song["SongID"],
            song_artist="Test Title * Test Artist",
        )

        schedule = programs.schedule_for_program(program_id)

        assert len(schedule) == 1
        assert schedule[0]["SongID"] == existing_song["SongID"]
        assert (
            schedule[0]["Song_Artist"]
            == "Test Title * Test Artist"
        )

        removed = programs.remove_song(program_id, 1.0)

        assert removed is True
        assert programs.schedule_for_program(program_id) == []
    finally:
        programs.delete(program_id)


def test_program_add_song_duplicate_position_raises(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    first_song, second_song = songs_repo.all(limit=2)

    program_id = programs.create(prog_name="CollidingSlots")

    try:
        programs.add_song(
            program_id, 1.0, song_id=first_song["SongID"]
        )

        with pytest.raises(ProgramValidationError):
            programs.add_song(
                program_id, 1.0, song_id=second_song["SongID"]
            )
    finally:
        programs.remove_song(program_id, 1.0)
        programs.delete(program_id)


def test_program_add_song_without_song_id_allows_slot(
    programs: ProgramService,
) -> None:
    program_id = programs.create(prog_name="AnnouncementShow")

    try:
        programs.add_song(
            program_id,
            1.0,
            song_artist="[Station ID announcement]",
        )

        schedule = programs.schedule_for_program(program_id)

        assert schedule[0]["SongID"] is None
    finally:
        programs.remove_song(program_id, 1.0)
        programs.delete(program_id)


def test_program_add_song_auto_fills_bpm_and_year(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = next(
        song
        for song in songs_repo.all(limit=50)
        if song["BPM"] is not None and song["Year"] is not None
    )

    program_id = programs.create(prog_name="AutoFilledShow")

    try:
        programs.add_song(
            program_id, 1.0, song_id=existing_song["SongID"]
        )

        schedule = programs.schedule_for_program(program_id)

        assert schedule[0]["BPM"] == existing_song["BPM"]
        assert schedule[0]["Year"] == existing_song["Year"]
    finally:
        programs.remove_song(program_id, 1.0)
        programs.delete(program_id)


def test_program_move_song_changes_position(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]

    program_id = programs.create(prog_name="ReorderedShow")

    try:
        programs.add_song(
            program_id, 1.0, song_id=existing_song["SongID"]
        )

        programs.move_song(program_id, 1.0, 5.0)

        schedule = programs.schedule_for_program(program_id)

        assert len(schedule) == 1
        assert schedule[0]["Position"] == 5.0
        assert schedule[0]["SongID"] == existing_song["SongID"]
    finally:
        programs.remove_song(program_id, 5.0)
        programs.delete(program_id)


def test_program_move_song_to_taken_position_raises(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    first_song, second_song = songs_repo.all(limit=2)

    program_id = programs.create(prog_name="BlockedMoveShow")

    try:
        programs.add_song(
            program_id, 1.0, song_id=first_song["SongID"]
        )
        programs.add_song(
            program_id, 2.0, song_id=second_song["SongID"]
        )

        with pytest.raises(ProgramValidationError):
            programs.move_song(program_id, 1.0, 2.0)
    finally:
        programs.remove_song(program_id, 1.0)
        programs.remove_song(program_id, 2.0)
        programs.delete(program_id)


def test_program_delete_with_scheduled_song_raises(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]

    program_id = programs.create(prog_name="StillScheduled")
    programs.add_song(
        program_id, 1.0, song_id=existing_song["SongID"]
    )

    try:
        with pytest.raises(QueryError):
            programs.delete(program_id)
    finally:
        programs.remove_song(program_id, 1.0)
        programs.delete(program_id)

# ============================================================
# SongService: Song -> Program relationship (Schedule, read-only)
# ============================================================


def test_programs_scheduling_song_empty_for_new_song(
    songs: SongService,
) -> None:
    song_id = songs.create(title="NeverScheduled")

    try:
        assert songs.programs_scheduling_song(song_id) == []
    finally:
        songs.delete(song_id)


def test_programs_scheduling_song_reflects_schedule(
    songs: SongService,
    programs: ProgramService,
) -> None:
    song_id = songs.create(title="ScheduledSong")
    program_id = programs.create(prog_name="ShowForScheduledSong")

    try:
        programs.add_song(program_id, 1.0, song_id=song_id)

        scheduled_on = songs.programs_scheduling_song(song_id)

        assert len(scheduled_on) == 1
        assert scheduled_on[0]["ProgramID"] == program_id
        assert scheduled_on[0]["Position"] == 1.0
    finally:
        programs.remove_song(program_id, 1.0)
        programs.delete(program_id)
        songs.delete(song_id)


# ============================================================
# ProgramService: swap_positions
# ============================================================


def test_swap_positions_exchanges_two_slots(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    song_a, song_b = songs_repo.all(limit=2)

    program_id = programs.create(prog_name="SwapPositionsTest")

    try:
        programs.add_song(program_id, 1.0, song_id=song_a["SongID"])
        programs.add_song(program_id, 2.0, song_id=song_b["SongID"])

        programs.swap_positions(program_id, 1.0, 2.0)

        schedule = {
            entry["SongID"]: entry["Position"]
            for entry in programs.schedule_for_program(program_id)
        }
        assert schedule[song_a["SongID"]] == 2.0
        assert schedule[song_b["SongID"]] == 1.0
    finally:
        for entry in programs.schedule_for_program(program_id):
            programs.remove_song(program_id, entry["Position"])
        programs.delete(program_id)


def test_swap_positions_preserves_other_fields(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    song_a, song_b = songs_repo.all(limit=2)

    program_id = programs.create(prog_name="SwapPositionsFieldsTest")

    try:
        programs.add_song(
            program_id, 1.0, song_id=song_a["SongID"],
            song_artist="Song A * Artist A",
        )
        programs.add_song(
            program_id, 2.0, song_id=song_b["SongID"],
            song_artist="Song B * Artist B",
        )

        programs.swap_positions(program_id, 1.0, 2.0)

        by_song = {
            entry["SongID"]: entry
            for entry in programs.schedule_for_program(program_id)
        }
        assert by_song[song_a["SongID"]]["Song_Artist"] == "Song A * Artist A"
        assert by_song[song_a["SongID"]]["Position"] == 2.0
        assert by_song[song_b["SongID"]]["Song_Artist"] == "Song B * Artist B"
        assert by_song[song_b["SongID"]]["Position"] == 1.0
    finally:
        for entry in programs.schedule_for_program(program_id):
            programs.remove_song(program_id, entry["Position"])
        programs.delete(program_id)


def test_swap_positions_same_position_is_a_no_op(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]

    program_id = programs.create(prog_name="SwapNoOpTest")

    try:
        programs.add_song(program_id, 1.0, song_id=existing_song["SongID"])

        programs.swap_positions(program_id, 1.0, 1.0)

        schedule = programs.schedule_for_program(program_id)
        assert len(schedule) == 1
        assert schedule[0]["Position"] == 1.0
    finally:
        programs.remove_song(program_id, 1.0)
        programs.delete(program_id)


def test_swap_positions_unknown_position_raises_not_found(
    programs: ProgramService,
    context: DatabaseContext,
) -> None:
    songs_repo = repository_for(context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]

    program_id = programs.create(prog_name="SwapUnknownPositionTest")

    try:
        programs.add_song(program_id, 1.0, song_id=existing_song["SongID"])

        with pytest.raises(RecordNotFoundError):
            programs.swap_positions(program_id, 1.0, 999.0)
    finally:
        programs.remove_song(program_id, 1.0)
        programs.delete(program_id)
