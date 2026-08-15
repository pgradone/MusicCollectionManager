"""
=========================================================
Music Collection Manager
Relationship Operations Tests
=========================================================

Milestone 3G (2/N)

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
    link,
    list_related,
    reorder,
    unlink,
)
from core.relationships import Relationship, discover_relationships
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