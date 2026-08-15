"""
=========================================================
Music Collection Manager
Relationship Operations Tests
=========================================================

Milestone 3G (2/N, 3/N)

pytest tests for core/relationship_operations.py.

Runs against the dedicated CRUD test database
(tests/Musi_crud_test.db), never the production database.
Every test cleans up any row it creates.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from core.context import DatabaseContext
from core.relationship_operations import (
    RelationshipError,
    get_target,
    link,
    list_referencing,
    list_related,
    reorder,
    set_target,
    unlink,
)
from core.relationships import (
    DIRECT,
    Relationship,
    SoftForeignKey,
    discover_relationships,
)
from core.repository import RecordNotFoundError, repository_for

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
def sing_relationship(context: DatabaseContext) -> Relationship:
    """The Artists <-> Songs relationship through Sing."""

    relationships = discover_relationships(context, "Artists")

    return next(
        r for r in relationships if r.target_table == "Songs"
    )


@pytest.fixture()
def contain_relationship(context: DatabaseContext) -> Relationship:
    """The Records <-> Songs relationship through Contain."""

    relationships = discover_relationships(context, "Records")

    return next(
        r for r in relationships if r.target_table == "Songs"
    )


@pytest.fixture()
def discogs_relationship(context: DatabaseContext) -> Relationship:
    """The Records -> Discogs direct relationship."""

    relationships = discover_relationships(context, "Records")

    return next(
        r
        for r in relationships
        if r.kind == DIRECT and r.target_table == "Discogs"
    )


@pytest.fixture()
def record_artist_soft_fk() -> SoftForeignKey:
    """Records.ArtistID -> Artists.ArtistID is not a declared FK."""

    return SoftForeignKey(
        table="Records",
        column="ArtistID",
        referenced_table="Artists",
        referenced_column="ArtistID",
    )


@pytest.fixture()
def records_to_artist_relationship(
    context: DatabaseContext,
    record_artist_soft_fk: SoftForeignKey,
) -> Relationship:
    """The Records -> Artist direct relationship (soft FK)."""

    relationships = discover_relationships(
        context, "Records", soft_foreign_keys=[record_artist_soft_fk]
    )

    return next(
        r
        for r in relationships
        if r.kind == DIRECT and r.target_table == "Artists"
    )


@pytest.fixture()
def artist_to_records_relationship(
    context: DatabaseContext,
    record_artist_soft_fk: SoftForeignKey,
) -> Relationship:
    """The Artists <- Records reverse_direct relationship (soft FK)."""

    relationships = discover_relationships(
        context, "Artists", soft_foreign_keys=[record_artist_soft_fk]
    )

    return next(
        r for r in relationships if r.target_table == "Records"
    )


# ============================================================
# list_related
# ============================================================


def test_list_related_empty_when_no_links(
    context: DatabaseContext,
    sing_relationship: Relationship,
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert(
        {"Surname": "NoSongsYet"}, commit=True
    )

    try:
        assert (
            list_related(context, sing_relationship, artist_id)
            == []
        )
    finally:
        artists.delete(artist_id, commit=True)


def test_link_and_list_related(
    context: DatabaseContext,
    sing_relationship: Relationship,
) -> None:
    artists = repository_for(context, "Artists")
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    artist_id = artists.insert(
        {"Surname": "LinkedArtist"}, commit=True
    )

    try:
        link(
            context,
            sing_relationship,
            artist_id,
            existing_song["SongID"],
        )

        related = list_related(
            context, sing_relationship, artist_id
        )

        assert [row["SongID"] for row in related] == [
            existing_song["SongID"]
        ]
    finally:
        unlink(
            context,
            sing_relationship,
            artist_id,
            existing_song["SongID"],
        )
        artists.delete(artist_id, commit=True)


def test_link_stores_extra_values(
    context: DatabaseContext,
    contain_relationship: Relationship,
) -> None:
    records = repository_for(context, "Records")
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    record_id = records.insert(
        {"Title": "PositionTestRecord"}, commit=True
    )

    try:
        link(
            context,
            contain_relationship,
            record_id,
            existing_song["SongID"],
            extra_values={"Position": "A1"},
        )

        related = list_related(
            context, contain_relationship, record_id
        )

        assert related[0]["Position"] == "A1"
    finally:
        unlink(
            context,
            contain_relationship,
            record_id,
            existing_song["SongID"],
        )
        records.delete(record_id, commit=True)


# ============================================================
# link: validation
# ============================================================


def test_link_duplicate_raises(
    context: DatabaseContext,
    sing_relationship: Relationship,
) -> None:
    artists = repository_for(context, "Artists")
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    artist_id = artists.insert(
        {"Surname": "DoubleLinker"}, commit=True
    )

    try:
        link(
            context,
            sing_relationship,
            artist_id,
            existing_song["SongID"],
        )

        with pytest.raises(RelationshipError):
            link(
                context,
                sing_relationship,
                artist_id,
                existing_song["SongID"],
            )
    finally:
        unlink(
            context,
            sing_relationship,
            artist_id,
            existing_song["SongID"],
        )
        artists.delete(artist_id, commit=True)


def test_link_validates_own_key_exists(
    context: DatabaseContext,
    sing_relationship: Relationship,
) -> None:
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    with pytest.raises(RecordNotFoundError):
        link(
            context,
            sing_relationship,
            999_999_999,
            existing_song["SongID"],
        )


def test_link_validates_other_key_exists(
    context: DatabaseContext,
    sing_relationship: Relationship,
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert(
        {"Surname": "WouldBeLinker"}, commit=True
    )

    try:
        with pytest.raises(RecordNotFoundError):
            link(
                context,
                sing_relationship,
                artist_id,
                999_999_999,
            )
    finally:
        artists.delete(artist_id, commit=True)


# ============================================================
# unlink
# ============================================================


def test_unlink_removes_link(
    context: DatabaseContext,
    sing_relationship: Relationship,
) -> None:
    artists = repository_for(context, "Artists")
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    artist_id = artists.insert(
        {"Surname": "SoonUnlinked"}, commit=True
    )

    try:
        link(
            context,
            sing_relationship,
            artist_id,
            existing_song["SongID"],
        )

        removed = unlink(
            context,
            sing_relationship,
            artist_id,
            existing_song["SongID"],
        )

        assert removed is True
        assert (
            list_related(context, sing_relationship, artist_id)
            == []
        )
    finally:
        artists.delete(artist_id, commit=True)


# ============================================================
# reorder
# ============================================================


def test_reorder_changes_extra_column_value(
    context: DatabaseContext,
    contain_relationship: Relationship,
) -> None:
    records = repository_for(context, "Records")
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    record_id = records.insert(
        {"Title": "ReorderedRecord"}, commit=True
    )

    try:
        link(
            context,
            contain_relationship,
            record_id,
            existing_song["SongID"],
            extra_values={"Position": "A1"},
        )

        reorder(
            context,
            contain_relationship,
            record_id,
            existing_song["SongID"],
            "Position",
            "B3",
        )

        related = list_related(
            context, contain_relationship, record_id
        )

        assert related[0]["Position"] == "B3"
    finally:
        unlink(
            context,
            contain_relationship,
            record_id,
            existing_song["SongID"],
        )
        records.delete(record_id, commit=True)


def test_reorder_rejects_unknown_column(
    context: DatabaseContext,
    contain_relationship: Relationship,
) -> None:
    records = repository_for(context, "Records")
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    record_id = records.insert(
        {"Title": "BadColumnRecord"}, commit=True
    )

    try:
        link(
            context,
            contain_relationship,
            record_id,
            existing_song["SongID"],
        )

        with pytest.raises(RelationshipError):
            reorder(
                context,
                contain_relationship,
                record_id,
                existing_song["SongID"],
                "NotARealColumn",
                "X",
            )
    finally:
        unlink(
            context,
            contain_relationship,
            record_id,
            existing_song["SongID"],
        )
        records.delete(record_id, commit=True)


def test_reorder_unknown_link_raises_not_found(
    context: DatabaseContext,
    contain_relationship: Relationship,
) -> None:
    records = repository_for(context, "Records")
    songs = repository_for(context, "Songs")
    existing_song = songs.all(limit=1)[0]

    record_id = records.insert(
        {"Title": "NeverLinkedRecord"}, commit=True
    )

    try:
        with pytest.raises(RecordNotFoundError):
            reorder(
                context,
                contain_relationship,
                record_id,
                existing_song["SongID"],
                "Position",
                "A1",
            )
    finally:
        records.delete(record_id, commit=True)


# ============================================================
# Non-junction relationships are rejected
# ============================================================


def test_operations_reject_non_junction_relationship(
    context: DatabaseContext,
) -> None:
    direct_relationship = next(
        r
        for r in discover_relationships(context, "Records")
        if r.target_table == "Discogs"
    )

    with pytest.raises(RelationshipError):
        list_related(context, direct_relationship, 1)

    with pytest.raises(RelationshipError):
        link(context, direct_relationship, 1, "some-release")

    with pytest.raises(RelationshipError):
        unlink(context, direct_relationship, 1, "some-release")

    with pytest.raises(RelationshipError):
        reorder(
            context, direct_relationship, 1, "some-release", "X", 1
        )


# ============================================================
# get_target / set_target (direct)
# ============================================================


def test_get_target_none_when_fk_unset(
    context: DatabaseContext,
    discogs_relationship: Relationship,
) -> None:
    records = repository_for(context, "Records")
    record_id = records.insert(
        {"Title": "NoDiscogsYet"}, commit=True
    )

    try:
        assert (
            get_target(context, discogs_relationship, record_id)
            is None
        )
    finally:
        records.delete(record_id, commit=True)


def test_set_target_and_get_target(
    context: DatabaseContext,
    discogs_relationship: Relationship,
) -> None:
    records = repository_for(context, "Records")
    discogs = repository_for(context, "Discogs")

    linked_releases = {
        row["Discogs_release"]
        for row in records.find({})
        if row["Discogs_release"] is not None
    }
    free_release = next(
        row["release_id"]
        for row in discogs.all(limit=20)
        if row["release_id"] not in linked_releases
    )

    record_id = records.insert(
        {"Title": "WillBeLinked"}, commit=True
    )

    try:
        set_target(
            context, discogs_relationship, record_id, free_release
        )

        target = get_target(
            context, discogs_relationship, record_id
        )

        assert target is not None
        assert target["release_id"] == free_release

        set_target(context, discogs_relationship, record_id, None)

        assert (
            get_target(context, discogs_relationship, record_id)
            is None
        )
    finally:
        records.delete(record_id, commit=True)


def test_set_target_validates_own_key_exists(
    context: DatabaseContext,
    discogs_relationship: Relationship,
) -> None:
    discogs = repository_for(context, "Discogs")
    any_release = discogs.all(limit=1)[0]

    with pytest.raises(RecordNotFoundError):
        set_target(
            context,
            discogs_relationship,
            999_999_999,
            any_release["release_id"],
        )


def test_set_target_validates_target_key_exists(
    context: DatabaseContext,
    discogs_relationship: Relationship,
) -> None:
    records = repository_for(context, "Records")
    record_id = records.insert(
        {"Title": "BadTargetRecord"}, commit=True
    )

    try:
        with pytest.raises(RecordNotFoundError):
            set_target(
                context,
                discogs_relationship,
                record_id,
                "no-such-release-id",
            )
    finally:
        records.delete(record_id, commit=True)


def test_set_target_with_soft_fk(
    context: DatabaseContext,
    records_to_artist_relationship: Relationship,
) -> None:
    records = repository_for(context, "Records")
    artists = repository_for(context, "Artists")
    existing_artist = artists.all(limit=1)[0]

    record_id = records.insert(
        {"Title": "SoftFkRecord"}, commit=True
    )

    try:
        set_target(
            context,
            records_to_artist_relationship,
            record_id,
            existing_artist["ArtistID"],
        )

        target = get_target(
            context, records_to_artist_relationship, record_id
        )

        assert target is not None
        assert target["ArtistID"] == existing_artist["ArtistID"]
    finally:
        records.delete(record_id, commit=True)


def test_get_target_rejects_wrong_kind(
    context: DatabaseContext,
    contain_relationship: Relationship,
) -> None:
    with pytest.raises(RelationshipError):
        get_target(context, contain_relationship, 1)


# ============================================================
# list_referencing (reverse_direct)
# ============================================================


def test_list_referencing_empty_when_none(
    context: DatabaseContext,
    artist_to_records_relationship: Relationship,
) -> None:
    artists = repository_for(context, "Artists")
    artist_id = artists.insert(
        {"Surname": "NoRecordsYet"}, commit=True
    )

    try:
        assert (
            list_referencing(
                context, artist_to_records_relationship, artist_id
            )
            == []
        )
    finally:
        artists.delete(artist_id, commit=True)


def test_list_referencing_returns_matching_rows(
    context: DatabaseContext,
    records_to_artist_relationship: Relationship,
    artist_to_records_relationship: Relationship,
) -> None:
    artists = repository_for(context, "Artists")
    records = repository_for(context, "Records")

    artist_id = artists.insert(
        {"Surname": "HasARecord"}, commit=True
    )
    record_id = records.insert(
        {"Title": "TheirOnlyRecord"}, commit=True
    )

    try:
        set_target(
            context,
            records_to_artist_relationship,
            record_id,
            artist_id,
        )

        referencing = list_referencing(
            context, artist_to_records_relationship, artist_id
        )

        assert [row["RecordID"] for row in referencing] == [
            record_id
        ]
    finally:
        records.delete(record_id, commit=True)
        artists.delete(artist_id, commit=True)


def test_list_referencing_rejects_wrong_kind(
    context: DatabaseContext,
    discogs_relationship: Relationship,
) -> None:
    with pytest.raises(RelationshipError):
        list_referencing(context, discogs_relationship, 1)