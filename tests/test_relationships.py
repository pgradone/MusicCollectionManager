"""
=========================================================
Music Collection Manager
Relationship Discovery Tests
=========================================================

Milestone 3G (1/N)

pytest tests for core/relationships.py.

Read-only against the application's configured database.
No INSERT, UPDATE, or DELETE operations are performed.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from core.context import DatabaseContext
from core.relationships import (
    DIRECT,
    JUNCTION,
    REVERSE_DIRECT,
    SoftForeignKey,
    discover_relationships,
)


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture()
def context() -> Iterator[DatabaseContext]:
    """Provide a started DatabaseContext against the real database."""

    with DatabaseContext() as db_context:
        yield db_context


# ============================================================
# Guard: schema must be loaded
# ============================================================


def test_requires_loaded_schema() -> None:
    unstarted_context = DatabaseContext()

    with pytest.raises(RuntimeError):
        discover_relationships(unstarted_context, "Artists")


# ============================================================
# Junction relationships (declared, both directions)
# ============================================================


def test_artists_junction_to_songs_via_sing(
    context: DatabaseContext,
) -> None:
    relationships = discover_relationships(context, "Artists")

    matches = [
        r
        for r in relationships
        if r.kind == JUNCTION and r.target_table == "Songs"
    ]

    assert len(matches) == 1
    assert matches[0].junction_table == "Sing"
    assert matches[0].own_fk_column == "ArtistID"
    assert matches[0].other_fk_column == "SongID"


def test_songs_junction_to_artists_via_sing(
    context: DatabaseContext,
) -> None:
    relationships = discover_relationships(context, "Songs")

    matches = [
        r
        for r in relationships
        if r.kind == JUNCTION and r.target_table == "Artists"
    ]

    assert len(matches) == 1
    assert matches[0].junction_table == "Sing"
    assert matches[0].own_fk_column == "SongID"
    assert matches[0].other_fk_column == "ArtistID"


def test_songs_junction_to_styles_via_belong(
    context: DatabaseContext,
) -> None:
    relationships = discover_relationships(context, "Songs")

    matches = [
        r
        for r in relationships
        if r.kind == JUNCTION and r.target_table == "Styles"
    ]

    assert len(matches) == 1
    assert matches[0].junction_table == "Belong"


def test_songs_junction_to_records_via_contain_has_position(
    context: DatabaseContext,
) -> None:
    relationships = discover_relationships(context, "Songs")

    matches = [
        r
        for r in relationships
        if r.kind == JUNCTION and r.target_table == "Records"
    ]

    assert len(matches) == 1
    assert matches[0].junction_table == "Contain"
    assert "Position" in matches[0].extra_columns


# ============================================================
# Direct relationships (declared)
# ============================================================


def test_records_direct_to_discogs(
    context: DatabaseContext,
) -> None:
    relationships = discover_relationships(context, "Records")

    matches = [
        r
        for r in relationships
        if r.kind == DIRECT and r.target_table == "Discogs"
    ]

    assert len(matches) == 1
    assert matches[0].fk_column == "Discogs_release"


def test_programs_reverse_direct_to_schedule(
    context: DatabaseContext,
) -> None:
    relationships = discover_relationships(context, "Programs")

    matches = [
        r
        for r in relationships
        if r.kind == REVERSE_DIRECT and r.target_table == "Schedule"
    ]

    assert len(matches) == 1
    assert matches[0].fk_column == "ProgramID"


# ============================================================
# Undeclared ("soft") relationships
# ============================================================


def test_records_to_artists_undiscovered_without_soft_fk(
    context: DatabaseContext,
) -> None:
    relationships = discover_relationships(context, "Records")

    matches = [
        r for r in relationships if r.target_table == "Artists"
    ]

    assert matches == []


def test_records_direct_to_artists_with_soft_fk(
    context: DatabaseContext,
) -> None:
    soft_fk = SoftForeignKey(
        table="Records",
        column="ArtistID",
        referenced_table="Artists",
        referenced_column="ArtistID",
    )

    relationships = discover_relationships(
        context, "Records", soft_foreign_keys=[soft_fk]
    )

    matches = [
        r
        for r in relationships
        if r.kind == DIRECT and r.target_table == "Artists"
    ]

    assert len(matches) == 1
    assert matches[0].fk_column == "ArtistID"


def test_artists_reverse_direct_to_records_with_soft_fk(
    context: DatabaseContext,
) -> None:
    soft_fk = SoftForeignKey(
        table="Records",
        column="ArtistID",
        referenced_table="Artists",
        referenced_column="ArtistID",
    )

    relationships = discover_relationships(
        context, "Artists", soft_foreign_keys=[soft_fk]
    )

    matches = [
        r
        for r in relationships
        if r.kind == REVERSE_DIRECT and r.target_table == "Records"
    ]

    assert len(matches) == 1
    assert matches[0].fk_column == "ArtistID"
    assert matches[0].fk_table == "Records"

# ============================================================
# numeric_extra_columns (junction) / order_column (reverse_direct)
# ============================================================


def test_contain_position_is_not_numeric(
    context: DatabaseContext,
) -> None:
    relationships = discover_relationships(context, "Records")

    contain = next(
        r
        for r in relationships
        if r.kind == JUNCTION and r.target_table == "Songs"
    )

    assert contain.extra_columns == ("Position",)
    assert contain.numeric_extra_columns == ()


def test_programs_schedule_has_order_column(
    context: DatabaseContext,
) -> None:
    soft_fk = SoftForeignKey(
        table="Schedule",
        column="SongID",
        referenced_table="Songs",
        referenced_column="SongID",
    )

    relationships = discover_relationships(
        context, "Programs", soft_foreign_keys=[soft_fk]
    )

    schedule = next(
        r
        for r in relationships
        if r.kind == REVERSE_DIRECT and r.target_table == "Schedule"
    )

    assert schedule.order_column == "Position"


def test_records_reverse_direct_has_no_order_column(
    context: DatabaseContext,
) -> None:
    soft_fk = SoftForeignKey(
        table="Records",
        column="ArtistID",
        referenced_table="Artists",
        referenced_column="ArtistID",
    )

    relationships = discover_relationships(
        context, "Artists", soft_foreign_keys=[soft_fk]
    )

    records = next(
        r
        for r in relationships
        if r.kind == REVERSE_DIRECT and r.target_table == "Records"
    )

    # Records' primary key is just RecordID - a single column, not
    # (ArtistID, <something numeric>) - so this must not be flagged
    # as an ordered child table.
    assert records.order_column is None
