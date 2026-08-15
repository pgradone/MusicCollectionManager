"""
=========================================================
Music Collection Manager
Relationship Operations
=========================================================

Milestone 3G (2/N, 3/N)

Generic CRUD for the relationships discovered by
core/relationships.py - list, link, unlink, and reorder for
junction relationships; get/set/list for direct and
reverse_direct ones - all driven entirely by a Relationship
description rather than by per-table code.
"""

from __future__ import annotations

from typing import Any

from core.context import DatabaseContext
from core.relationships import DIRECT, JUNCTION, REVERSE_DIRECT, Relationship
from core.repository import repository_for


class RelationshipError(Exception):
    """Raised when a relationship operation is used incorrectly."""


def list_related(
    context: DatabaseContext,
    relationship: Relationship,
    own_key: Any,
) -> list[dict[str, Any]]:
    """
    List every row on the other side of a junction relationship
    for one row of the source table.

    Args:
        own_key:
            The source table's primary-key value (e.g. an
            ArtistID when relationship.source_table is
            "Artists").

    Each returned row is the target row's own columns, plus any
    of the junction's extra_columns (e.g. Position on Contain).
    """

    _require_junction(relationship)
    assert relationship.junction_table is not None
    assert relationship.own_fk_column is not None
    assert relationship.other_fk_column is not None

    junction_repo = repository_for(context, relationship.junction_table)
    target_repo = repository_for(context, relationship.target_table)

    links = junction_repo.find(
        {relationship.own_fk_column: own_key}
    )

    results: list[dict[str, Any]] = []

    for link in links:
        row = dict(
            target_repo.require(link[relationship.other_fk_column])
        )

        for column in relationship.extra_columns:
            row[column] = link.get(column)

        results.append(row)

    return results


def link(
    context: DatabaseContext,
    relationship: Relationship,
    own_key: Any,
    other_key: Any,
    *,
    extra_values: dict[str, Any] | None = None,
) -> None:
    """
    Connect own_key to other_key through a junction relationship.

    Validates that both rows exist before creating the link, and
    raises RelationshipError if the pair is already linked.
    """

    _require_junction(relationship)
    assert relationship.junction_table is not None
    assert relationship.own_fk_column is not None
    assert relationship.other_fk_column is not None

    source_repo = repository_for(context, relationship.source_table)
    target_repo = repository_for(context, relationship.target_table)
    junction_repo = repository_for(context, relationship.junction_table)

    source_repo.require(own_key)
    target_repo.require(other_key)

    key = {
        relationship.own_fk_column: own_key,
        relationship.other_fk_column: other_key,
    }

    if junction_repo.exists(key):
        raise RelationshipError(
            f"{relationship.target_table} {other_key!r} is "
            f"already linked to {relationship.source_table} "
            f"{own_key!r} through {relationship.junction_table}."
        )

    payload: dict[str, Any] = dict(key)

    if extra_values:
        payload.update(extra_values)

    junction_repo.insert(payload, commit=True)


def unlink(
    context: DatabaseContext,
    relationship: Relationship,
    own_key: Any,
    other_key: Any,
) -> bool:
    """
    Remove the link between own_key and other_key.

    Returns True when a link was removed.
    """

    _require_junction(relationship)
    assert relationship.junction_table is not None
    assert relationship.own_fk_column is not None
    assert relationship.other_fk_column is not None

    junction_repo = repository_for(context, relationship.junction_table)

    return junction_repo.delete(
        {
            relationship.own_fk_column: own_key,
            relationship.other_fk_column: other_key,
        },
        commit=True,
    )


def reorder(
    context: DatabaseContext,
    relationship: Relationship,
    own_key: Any,
    other_key: Any,
    column: str,
    new_value: Any,
) -> bool:
    """
    Change the value of one of the junction's extra columns for
    an existing link (e.g. moving a track's Position on Contain).

    column must be one of relationship.extra_columns - this is
    not restricted to position-like columns specifically, since
    the engine has no way to know which column means "order"
    for an arbitrary schema.
    """

    _require_junction(relationship)
    assert relationship.junction_table is not None
    assert relationship.own_fk_column is not None
    assert relationship.other_fk_column is not None

    if column not in relationship.extra_columns:
        raise RelationshipError(
            f"{column!r} is not an extra column on "
            f"{relationship.junction_table} - available: "
            f"{relationship.extra_columns!r}."
        )

    junction_repo = repository_for(context, relationship.junction_table)

    key = {
        relationship.own_fk_column: own_key,
        relationship.other_fk_column: other_key,
    }

    junction_repo.require(key)

    return junction_repo.update(
        key,
        {column: new_value},
        commit=True,
    )


def get_target(
    context: DatabaseContext,
    relationship: Relationship,
    own_key: Any,
) -> dict[str, Any] | None:
    """
    Fetch the single related row for one source row of a
    "direct" relationship (e.g. the Artist a Record points at).

    Args:
        own_key:
            The source table's primary-key value (e.g. a
            RecordID when relationship.source_table is
            "Records").

    Returns None when the foreign key column is NULL on the
    source row.
    """

    _require_kind(relationship, DIRECT)
    assert relationship.fk_column is not None

    source_repo = repository_for(context, relationship.source_table)
    target_repo = repository_for(context, relationship.target_table)

    source_row = source_repo.require(own_key)
    fk_value = source_row[relationship.fk_column]

    if fk_value is None:
        return None

    return target_repo.get(fk_value)


def set_target(
    context: DatabaseContext,
    relationship: Relationship,
    own_key: Any,
    target_key: Any,
) -> bool:
    """
    Point a "direct" relationship's foreign key at target_key,
    or clear it when target_key is None.

    Validates that own_key exists, and that target_key exists
    when it is not None.
    """

    _require_kind(relationship, DIRECT)
    assert relationship.fk_column is not None

    source_repo = repository_for(context, relationship.source_table)
    source_repo.require(own_key)

    if target_key is not None:
        target_repo = repository_for(
            context, relationship.target_table
        )
        target_repo.require(target_key)

    return source_repo.update(
        own_key,
        {relationship.fk_column: target_key},
        commit=True,
    )


def list_referencing(
    context: DatabaseContext,
    relationship: Relationship,
    own_key: Any,
) -> list[dict[str, Any]]:
    """
    List every row in another table whose foreign key points
    back at one row of a "reverse_direct" relationship (e.g.
    every Record by one Artist).

    Args:
        own_key:
            The source table's primary-key value (e.g. an
            ArtistID when relationship.source_table is
            "Artists").
    """

    _require_kind(relationship, REVERSE_DIRECT)
    assert relationship.fk_column is not None
    assert relationship.fk_table is not None

    source_repo = repository_for(context, relationship.source_table)
    source_repo.require(own_key)

    fk_repo = repository_for(context, relationship.fk_table)

    return fk_repo.find({relationship.fk_column: own_key})


def _require_kind(relationship: Relationship, expected: str) -> None:
    if relationship.kind != expected:
        raise RelationshipError(
            f"This operation only supports {expected!r} "
            f"relationships, not {relationship.kind!r}."
        )


def _require_junction(relationship: Relationship) -> None:
    _require_kind(relationship, JUNCTION)