"""
=========================================================
Music Collection Manager
Relationship Discovery
=========================================================

Milestone 3G (1/N)

Schema-driven discovery of how tables relate to each other,
built entirely from the foreign-key and primary-key metadata
SchemaManager already exposes - no hardcoded knowledge of any
specific table or column name.

This is deliberately generic: discover_relationships() works
against any SQLite database with declared foreign keys, not
just this one. It is the foundation for a relationship editor
that can drive any table's UI without per-table code - the
same idea main.py already applies for basic CRUD, extended
here to relationships between tables.

Known limitation - and why soft_foreign_keys exists
-----------------------------------------------------
Only DECLARED foreign keys are discoverable through PRAGMA
metadata. This database has several columns that function as
references but were never declared with a FOREIGN KEY
constraint (confirmed by inspecting the actual table DDL):

* Records.ArtistID  -> Artists.ArtistID  (plain INTEGER column)
* Schedule.SongID   -> Songs.SongID      (plain INTEGER column)

Callers that know about such gaps in a particular database can
pass them explicitly as `soft_foreign_keys`; they are then
treated identically to declared foreign keys for the purposes
of discovery. This keeps the engine itself free of any
knowledge specific to this application - the list of gaps is
data supplied by the caller, not code inside this module.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from core.context import DatabaseContext
from core.schema import SchemaManager, TableInfo

RelationshipKind = str
JUNCTION: RelationshipKind = "junction"
DIRECT: RelationshipKind = "direct"
REVERSE_DIRECT: RelationshipKind = "reverse_direct"


@dataclass(frozen=True, slots=True)
class SoftForeignKey:
    """
    A foreign-key relationship that exists in practice but was
    never declared with a FOREIGN KEY constraint in the schema.
    """

    table: str
    column: str
    referenced_table: str
    referenced_column: str


@dataclass(frozen=True, slots=True)
class Relationship:
    """
    Describes one way a table relates to another table.

    kind:
        "junction"        - a two-foreign-key table sits between
                             the two tables (e.g. Sing between
                             Artists and Songs).
        "direct"          - the table itself holds a foreign key
                             column pointing at target_table
                             (e.g. Records.ArtistID).
        "reverse_direct"  - the reverse of "direct": some other
                             table (fk_table) holds a foreign key
                             pointing back at this table.
    """

    kind: RelationshipKind
    target_table: str

    # "junction" only
    junction_table: str | None = None
    own_fk_column: str | None = None
    other_fk_column: str | None = None
    extra_columns: tuple[str, ...] = ()

    # "direct" / "reverse_direct" only
    fk_column: str | None = None
    fk_table: str | None = None


# A foreign key, declared or soft, reduced to the three things
# relationship discovery actually needs.
_FKTuple = tuple[str, str, str]  # (column, ref_table, ref_column)


def discover_relationships(
    context: DatabaseContext,
    table_name: str,
    *,
    soft_foreign_keys: Sequence[SoftForeignKey] = (),
) -> list[Relationship]:
    """
    Discover every relationship `table_name` participates in.

    Requires the context's schema to already be loaded (i.e.
    context.start() must have been called).
    """

    schema = _loaded_schema(context)
    table = schema.get_table(table_name)

    own_fks, incoming = _augmented_foreign_keys(
        schema, soft_foreign_keys
    )

    relationships: list[Relationship] = []
    relationships.extend(
        _junction_relationships(schema, table, own_fks)
    )
    relationships.extend(
        _direct_relationships(table, own_fks)
    )
    relationships.extend(
        _reverse_direct_relationships(schema, table, incoming)
    )

    return relationships


def _loaded_schema(context: DatabaseContext) -> SchemaManager:
    if not context.schema.loaded:
        raise RuntimeError(
            "DatabaseContext schema is not loaded - call "
            "context.start() first."
        )

    return context.schema


def _augmented_foreign_keys(
    schema: SchemaManager,
    soft_foreign_keys: Sequence[SoftForeignKey],
) -> tuple[dict[str, list[_FKTuple]], dict[str, list[tuple[str, _FKTuple]]]]:
    """
    Build two lookups combining declared and soft foreign keys:

    * own_fks[table]      -> foreign keys declared on that table
    * incoming[table]     -> (owning_table, foreign_key) pairs
                              that reference that table
    """

    own_fks: dict[str, list[_FKTuple]] = {}
    incoming: dict[str, list[tuple[str, _FKTuple]]] = {}

    for table in schema.tables.values():
        fk_tuples = [
            (fk.column, fk.referenced_table, fk.referenced_column)
            for fk in table.foreign_keys
        ]
        own_fks[table.name] = fk_tuples

        for fk_tuple in fk_tuples:
            _, ref_table, _ = fk_tuple
            incoming.setdefault(ref_table, []).append(
                (table.name, fk_tuple)
            )

    for soft in soft_foreign_keys:
        fk_tuple = (
            soft.column,
            soft.referenced_table,
            soft.referenced_column,
        )
        own_fks.setdefault(soft.table, []).append(fk_tuple)
        incoming.setdefault(soft.referenced_table, []).append(
            (soft.table, fk_tuple)
        )

    return own_fks, incoming


def _junction_relationships(
    schema: SchemaManager,
    table: TableInfo,
    own_fks: dict[str, list[_FKTuple]],
) -> list[Relationship]:
    """
    Association tables with one foreign key pointing back at
    `table` - the other foreign key names the related table.

    Association-table detection itself is based only on
    declared foreign keys (it is a property of the schema, not
    something soft_foreign_keys is meant to override).
    """

    relationships: list[Relationship] = []
    own_key = table.name.casefold()

    for junction in schema.association_tables():
        junction_fks = own_fks.get(junction.name, [])

        own_fk = None
        other_fk = None

        for fk_column, ref_table, _ in junction_fks:
            if ref_table.casefold() == own_key:
                own_fk = (fk_column, ref_table)
            else:
                other_fk = (fk_column, ref_table)

        if own_fk is None or other_fk is None:
            continue

        key_columns = {fk[0] for fk in junction_fks}
        extra_columns = tuple(
            column.name
            for column in junction.columns
            if column.name not in key_columns
        )

        relationships.append(
            Relationship(
                kind=JUNCTION,
                target_table=other_fk[1],
                junction_table=junction.name,
                own_fk_column=own_fk[0],
                other_fk_column=other_fk[0],
                extra_columns=extra_columns,
            )
        )

    return relationships


def _direct_relationships(
    table: TableInfo,
    own_fks: dict[str, list[_FKTuple]],
) -> list[Relationship]:
    """
    Foreign keys (declared or soft) held directly on `table`
    itself, e.g. Records.ArtistID -> Artists. Skipped for
    association tables, since those are already fully described
    by the junction relationships of the tables they connect.
    """

    if table.is_association_table:
        return []

    return [
        Relationship(
            kind=DIRECT,
            target_table=ref_table,
            fk_column=fk_column,
            fk_table=table.name,
        )
        for fk_column, ref_table, _ in own_fks.get(table.name, [])
    ]


def _reverse_direct_relationships(
    schema: SchemaManager,
    table: TableInfo,
    incoming: dict[str, list[tuple[str, _FKTuple]]],
) -> list[Relationship]:
    """
    Foreign keys (declared or soft) on other, non-association
    tables that point back at `table`, e.g.
    Artists <- Records.ArtistID.
    """

    relationships: list[Relationship] = []

    for owning_table_name, (fk_column, _, _) in incoming.get(
        table.name, []
    ):
        owning_table = schema.get_table_or_none(owning_table_name)

        if owning_table is not None and (
            owning_table.is_association_table
        ):
            continue

        relationships.append(
            Relationship(
                kind=REVERSE_DIRECT,
                target_table=owning_table_name,
                fk_column=fk_column,
                fk_table=owning_table_name,
            )
        )

    return relationships