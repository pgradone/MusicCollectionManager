"""
=========================================================
Music Collection Manager
Relationship Operations
=========================================================

Milestone 3G (2/N)

Generic CRUD for the relationships discovered by
core/relationships.py - list, link, unlink, and reorder,
driven entirely by a Relationship description rather than by
per-table code.

This chunk covers "junction" relationships only (two-foreign-
key tables such as Sing, Contain, Belong). "direct" and
"reverse_direct" operations are a separate, smaller follow-up,
since their key semantics differ enough from junctions that
folding them into the same functions would blur what each
call actually does.
"""

from __future__ import annotations

from typing import Any

from core.context import DatabaseContext
from core.relationships import JUNCTION, Relationship
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

    junction_repo = repository_for(context, relationship.junction_table)  # type: ignore[arg-type]
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

    source_repo = repository_for(context, relationship.source_table)
    target_repo = repository_for(context, relationship.target_table)
    junction_repo = repository_for(context, relationship.junction_table)  # type: ignore[arg-type]

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

    junction_repo = repository_for(context, relationship.junction_table)  # type: ignore[arg-type]

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

    if column not in relationship.extra_columns:
        raise RelationshipError(
            f"{column!r} is not an extra column on "
            f"{relationship.junction_table} - available: "
            f"{relationship.extra_columns!r}."
        )

    junction_repo = repository_for(context, relationship.junction_table)  # type: ignore[arg-type]

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


def _require_junction(relationship: Relationship) -> None:
    if relationship.kind != JUNCTION:
        raise RelationshipError(
            f"This operation only supports junction "
            f"relationships, not {relationship.kind!r}."
        )