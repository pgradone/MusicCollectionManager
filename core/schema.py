"""
=========================================================
MusicCollectionManager
Schema Manager
=========================================================

Reads and caches the SQLite schema.

This module contains only metadata classes and the basic
SchemaManager skeleton.

The actual schema loading implementation will be added in
the next part.

Compatible with

    Python 3.14
    Pylance Strict
    mypy
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from core.database import DatabaseManager


# =========================================================
# Column metadata
# =========================================================

@dataclass(slots=True, frozen=True)
class ColumnInfo:
    """
    Describes one SQLite column.
    """

    cid: int

    name: str

    data_type: str

    not_null: bool

    default_value: str | None

    primary_key: bool


# =========================================================
# Foreign key metadata
# =========================================================

@dataclass(slots=True, frozen=True)
class ForeignKeyInfo:
    """
    Describes one SQLite foreign key.
    """

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
    """
    Describes one SQLite index.
    """

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

    columns: list[ColumnInfo] = field(default_factory=lambda: [])

    foreign_keys: list[ForeignKeyInfo] = field(default_factory=lambda: [])

    indexes: list[IndexInfo] = field(default_factory=lambda: [])

    row_count: int = 0

    parent_tables: set[str] = field(default_factory=lambda: set())

    child_tables: set[str] = field(default_factory=lambda: set())

    # -----------------------------------------------------

    @property
    def primary_key(self) -> ColumnInfo | None:
        """
        Return the primary key column.
        """

        for column in self.columns:

            if column.primary_key:

                return column

        return None

    # -----------------------------------------------------

    def column(
        self,
        name: str,
    ) -> ColumnInfo | None:
        """
        Return one column by name.
        """

        upper = name.upper()

        for column in self.columns:

            if column.name.upper() == upper:

                return column

        return None

    # -----------------------------------------------------

    def has_column(
        self,
        name: str,
    ) -> bool:

        return self.column(name) is not None


# =========================================================
# Schema manager
# =========================================================

class SchemaManager:
    """
    Loads and caches the SQLite schema.
    """

    def __init__(
        self,
        database: DatabaseManager,
    ) -> None:

        self.db = database

        self._tables: dict[str, TableInfo] = {}

        self.loaded = False

    # -----------------------------------------------------

    def clear(self) -> None:

        self._tables.clear()

        self.loaded = False

    # -----------------------------------------------------

    @property
    def tables(self) -> dict[str, TableInfo]:

        return self._tables

    # -----------------------------------------------------

    def get_table(
        self,
        table_name: str,
    ) -> TableInfo:

        key = table_name.upper()

        if key not in self._tables:

            raise KeyError(
                f"Unknown table '{table_name}'."
            )

        return self._tables[key]

    # -----------------------------------------------------

    def table_names(self) -> list[str]:

        return sorted(self._tables.keys())

    # -----------------------------------------------------

    def __contains__(
        self,
        table_name: str,
    ) -> bool:

        return table_name.upper() in self._tables

    # -----------------------------------------------------

    def __len__(self) -> int:

        return len(self._tables)

    # -----------------------------------------------------

    def __iter__(self) -> Iterator[TableInfo]:

        return iter(self._tables.values())

    # -----------------------------------------------------

    def load(self) -> None:
        """
        Implemented in Response 2.
        """
        raise NotImplementedError