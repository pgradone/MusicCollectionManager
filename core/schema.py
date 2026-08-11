"""
=========================================================
MusicCollectionManager
Schema Manager
=========================================================

Provides a typed, cached representation of the SQLite
database schema.

The SchemaManager deliberately sits above DatabaseManager.
It does not open its own SQLite connection and it does not
execute application CRUD operations.

Responsibilities
----------------
* Discover database tables.
* Describe columns.
* Describe primary keys.
* Describe foreign keys.
* Describe indexes.
* Determine parent/child relationships.
* Identify likely association/junction tables.
* Cache schema information for efficient UI use.

Compatible with:
    Python 3.14
    Pylance Strict
    mypy
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from core.database import DatabaseManager


# =========================================================
# Column metadata
# =========================================================


@dataclass(slots=True, frozen=True)
class ColumnInfo:
    """Describe one SQLite table column."""

    cid: int
    name: str
    data_type: str
    not_null: bool
    default_value: str | None
    primary_key: bool


# =========================================================
# Foreign-key metadata
# =========================================================


@dataclass(slots=True, frozen=True)
class ForeignKeyInfo:
    """Describe one SQLite foreign-key relationship."""

    id: int
    sequence: int
    column: str
    referenced_table: str
    referenced_column: str
    on_update: str
    on_delete: str
    match: str


# =========================================================
# Index metadata
# =========================================================


@dataclass(slots=True, frozen=True)
class IndexInfo:
    """Describe one SQLite index."""

    sequence: int
    name: str
    unique: bool
    origin: str
    partial: bool


# =========================================================
# Table metadata
# =========================================================


@dataclass(slots=True)
class TableInfo:
    """
    Complete metadata describing one database table.
    """

    name: str

    columns: list[ColumnInfo] = field(default_factory=list)

    foreign_keys: list[ForeignKeyInfo] = field(
        default_factory=list
    )

    indexes: list[IndexInfo] = field(
        default_factory=list
    )

    row_count: int = 0

    parent_tables: set[str] = field(
        default_factory=set
    )

    child_tables: set[str] = field(
        default_factory=set
    )

    association_table: bool = False

    # -----------------------------------------------------
    # Primary key
    # -----------------------------------------------------

    @property
    def primary_key(self) -> ColumnInfo | None:
        """
        Return the first primary-key column.

        For a composite primary key, use primary_key_columns.
        """

        for column in self.columns:
            if column.primary_key:
                return column

        return None

    # -----------------------------------------------------

    @property
    def primary_key_columns(self) -> list[ColumnInfo]:
        """Return all primary-key columns."""

        return [
            column
            for column in self.columns
            if column.primary_key
        ]

    # -----------------------------------------------------

    @property
    def is_composite_primary_key(self) -> bool:
        """Return True when the table has multiple PK columns."""

        return len(self.primary_key_columns) > 1

    # -----------------------------------------------------
    # Foreign keys
    # -----------------------------------------------------

    @property
    def has_foreign_keys(self) -> bool:
        """Return True when the table contains foreign keys."""

        return bool(self.foreign_keys)

    # -----------------------------------------------------

    @property
    def is_association_table(self) -> bool:
        """
        Return True when the database identifies this table
        as an association/junction table.
        """

        return self.association_table

    # -----------------------------------------------------
    # Column lookup
    # -----------------------------------------------------

    def column(
        self,
        name: str,
    ) -> ColumnInfo | None:
        """
        Return one column by name.

        Comparison is case-insensitive.
        """

        lookup = name.casefold()

        for column in self.columns:
            if column.name.casefold() == lookup:
                return column

        return None

    # -----------------------------------------------------

    def has_column(
        self,
        name: str,
    ) -> bool:
        """Return True when the named column exists."""

        return self.column(name) is not None


# =========================================================
# Schema manager
# =========================================================


class SchemaManager:
    """
    Discover and cache the SQLite schema.

    DatabaseManager remains the sole owner of the SQLite
    connection. SchemaManager only consumes its metadata
    APIs.
    """

    def __init__(
        self,
        database: DatabaseManager,
    ) -> None:

        self.db = database

        self._tables: dict[str, TableInfo] = {}

        self.loaded = False

    # =====================================================
    # Cache management
    # =====================================================

    def clear(self) -> None:
        """Clear all cached schema information."""

        self._tables.clear()

        self.loaded = False

    # -----------------------------------------------------

    def load(self) -> None:
        """
        Discover and cache the complete database schema.

        This method is deliberately explicit. Creating a
        SchemaManager does not automatically query the
        database.
        """

        self.clear()

        table_names = self.db.tables()

        discovered: dict[str, TableInfo] = {}

        for table_name in table_names:

            table = TableInfo(
                name=table_name
            )

            table.columns = self._load_columns(
                table_name
            )

            table.foreign_keys = (
                self._load_foreign_keys(
                    table_name
                )
            )

            table.indexes = self._load_indexes(
                table_name
            )

            table.row_count = self.db.count(
                table_name
            )

            table.association_table = (
                self.db.is_association_table(
                    table_name
                )
            )

            key = self._normalise(
                table_name
            )

            discovered[key] = table

        self._build_relationships(
            discovered
        )

        self._tables = discovered

        self.loaded = True

    # -----------------------------------------------------

    def refresh(self) -> None:
        """Reload the database schema."""

        self.load()

    # =====================================================
    # Table access
    # =====================================================

    @property
    def tables(self) -> dict[str, TableInfo]:
        """
        Return the cached table dictionary.

        The dictionary should be treated as read-only by
        callers.
        """

        return self._tables

    # -----------------------------------------------------

    def get_table(
        self,
        table_name: str,
    ) -> TableInfo:
        """
        Return metadata for one table.

        Raises:
            KeyError: if the table does not exist.
        """

        key = self._normalise(
            table_name
        )

        table = self._tables.get(key)

        if table is None:
            raise KeyError(
                f"Unknown table '{table_name}'."
            )

        return table

    # -----------------------------------------------------

    def get_table_or_none(
        self,
        table_name: str,
    ) -> TableInfo | None:
        """Return table metadata or None."""

        return self._tables.get(
            self._normalise(table_name)
        )

    # -----------------------------------------------------

    def table_names(self) -> list[str]:
        """Return cached table names alphabetically."""

        return sorted(
            (
                table.name
                for table in self._tables.values()
            ),
            key=str.casefold,
        )

    # =====================================================
    # Relationship access
    # =====================================================

    def parent_tables(
        self,
        table_name: str,
    ) -> list[TableInfo]:
        """
        Return tables referenced by the selected table.
        """

        table = self.get_table(
            table_name
        )

        result: list[TableInfo] = []

        for parent_name in sorted(
            table.parent_tables,
            key=str.casefold,
        ):

            parent = self.get_table_or_none(
                parent_name
            )

            if parent is not None:
                result.append(parent)

        return result

    # -----------------------------------------------------

    def child_tables(
        self,
        table_name: str,
    ) -> list[TableInfo]:
        """
        Return tables containing foreign keys pointing
        to the selected table.
        """

        table = self.get_table(
            table_name
        )

        result: list[TableInfo] = []

        for child_name in sorted(
            table.child_tables,
            key=str.casefold,
        ):

            child = self.get_table_or_none(
                child_name
            )

            if child is not None:
                result.append(child)

        return result

    # -----------------------------------------------------

    def foreign_keys_to(
        self,
        table_name: str,
    ) -> list[
        tuple[TableInfo, ForeignKeyInfo]
    ]:
        """
        Return foreign keys in other tables that reference
        the selected table.
        """

        target = self.get_table(
            table_name
        )

        target_key = target.name.casefold()

        result: list[
            tuple[TableInfo, ForeignKeyInfo]
        ] = []

        for table in self._tables.values():

            for foreign_key in table.foreign_keys:

                if (
                    foreign_key
                    .referenced_table
                    .casefold()
                    == target_key
                ):

                    result.append(
                        (
                            table,
                            foreign_key,
                        )
                    )

        return result

    # =====================================================
    # Convenience queries
    # =====================================================

    def association_tables(
        self,
    ) -> list[TableInfo]:
        """Return all detected association tables."""

        return sorted(
            (
                table
                for table in self._tables.values()
                if table.is_association_table
            ),
            key=lambda table: table.name.casefold(),
        )

    # -----------------------------------------------------

    def tables_with_foreign_keys(
        self,
    ) -> list[TableInfo]:
        """Return all tables containing foreign keys."""

        return sorted(
            (
                table
                for table in self._tables.values()
                if table.has_foreign_keys
            ),
            key=lambda table: table.name.casefold(),
        )

    # =====================================================
    # Collection protocol
    # =====================================================

    def __contains__(
        self,
        table_name: str,
    ) -> bool:
        """Return True when a table exists in the cache."""

        return (
            self._normalise(table_name)
            in self._tables
        )

    # -----------------------------------------------------

    def __len__(self) -> int:
        """Return the number of cached tables."""

        return len(self._tables)

    # -----------------------------------------------------

    def __iter__(self) -> Iterator[TableInfo]:
        """Iterate through tables alphabetically."""

        for name in self.table_names():

            yield self._tables[
                self._normalise(name)
            ]

    # =====================================================
    # Internal loading helpers
    # =====================================================

    def _load_columns(
        self,
        table_name: str,
    ) -> list[ColumnInfo]:
        """Load column metadata for a table."""

        columns: list[ColumnInfo] = []

        for row in self.db.columns(
            table_name
        ):

            default_value: str | None

            raw_default = row["dflt_value"]

            if raw_default is None:
                default_value = None
            else:
                default_value = str(
                    raw_default
                )

            columns.append(
                ColumnInfo(
                    cid=int(row["cid"]),
                    name=str(row["name"]),
                    data_type=str(
                        row["type"] or ""
                    ),
                    not_null=bool(
                        row["notnull"]
                    ),
                    default_value=default_value,
                    primary_key=bool(
                        row["pk"]
                    ),
                )
            )

        return columns

    # -----------------------------------------------------

    def _load_foreign_keys(
        self,
        table_name: str,
    ) -> list[ForeignKeyInfo]:
        """Load foreign-key metadata."""

        foreign_keys: list[
            ForeignKeyInfo
        ] = []

        for row in self.db.foreign_keys(
            table_name
        ):

            foreign_keys.append(
                ForeignKeyInfo(
                    id=int(row["id"]),
                    sequence=int(row["seq"]),
                    column=str(row["from"]),
                    referenced_table=str(
                        row["table"]
                    ),
                    referenced_column=str(
                        row["to"]
                    ),
                    on_update=str(
                        row["on_update"] or ""
                    ),
                    on_delete=str(
                        row["on_delete"] or ""
                    ),
                    match=str(
                        row["match"] or ""
                    ),
                )
            )

        return foreign_keys

    # -----------------------------------------------------

    def _load_indexes(
        self,
        table_name: str,
    ) -> list[IndexInfo]:
        """Load index metadata."""

        indexes: list[IndexInfo] = []

        for row in self.db.indexes(
            table_name
        ):

            indexes.append(
                IndexInfo(
                    sequence=int(
                        row["seq"]
                    ),
                    name=str(
                        row["name"]
                    ),
                    unique=bool(
                        row["unique"]
                    ),
                    origin=str(
                        row["origin"]
                    ),
                    partial=bool(
                        row["partial"]
                    ),
                )
            )

        return indexes

    # =====================================================
    # Relationship graph
    # =====================================================

    def _build_relationships(
        self,
        tables: dict[str, TableInfo],
    ) -> None:
        """
        Build parent/child relationships between tables.
        """

        for table in tables.values():

            table.parent_tables.clear()
            table.child_tables.clear()

        for table in tables.values():

            for foreign_key in (
                table.foreign_keys
            ):

                parent_key = (
                    foreign_key
                    .referenced_table
                    .casefold()
                )

                parent = tables.get(
                    parent_key
                )

                if parent is None:
                    continue

                table.parent_tables.add(
                    parent.name
                )

                parent.child_tables.add(
                    table.name
                )

    # =====================================================
    # Utility
    # =====================================================

    @staticmethod
    def _normalise(
        table_name: str,
    ) -> str:
        """Return the canonical cache key."""

        return table_name.strip().casefold()
