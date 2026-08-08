```python
"""
Schema metadata and relationship management for MusicCollectionManager.

The SchemaManager reads SQLite metadata through DatabaseManager and
provides a typed, cached representation of the database structure.

The schema layer deliberately does not execute arbitrary application SQL.
It is responsible only for discovering and describing the database.

Compatible with Python 3.14 and Pylance Strict.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from core.database import DatabaseManager


@dataclass(slots=True, frozen=True)
class ColumnInfo:
    """Metadata describing one SQLite table column."""

    cid: int
    name: str
    data_type: str
    not_null: bool
    default_value: str | None
    primary_key: bool


@dataclass(slots=True, frozen=True)
class ForeignKeyInfo:
    """Metadata describing one SQLite foreign-key relationship."""

    id: int
    sequence: int
    column: str
    referenced_table: str
    referenced_column: str
    on_update: str
    on_delete: str
    match: str


@dataclass(slots=True, frozen=True)
class IndexInfo:
    """Metadata describing one SQLite index."""

    sequence: int
    name: str
    unique: bool
    origin: str
    partial: bool


@dataclass(slots=True)
class TableInfo:
    """Complete metadata describing one database table."""

    name: str
    columns: list[ColumnInfo] = field(default_factory=list)
    foreign_keys: list[ForeignKeyInfo] = field(default_factory=list)
    indexes: list[IndexInfo] = field(default_factory=list)
    row_count: int = 0
    parent_tables: set[str] = field(default_factory=set)
    child_tables: set[str] = field(default_factory=set)

    @property
    def primary_key(self) -> ColumnInfo | None:
        """Return the first primary-key column, if one exists."""

        for column in self.columns:
            if column.primary_key:
                return column

        return None

    @property
    def primary_key_columns(self) -> list[ColumnInfo]:
        """
        Return all primary-key columns.

        SQLite permits composite primary keys, so callers should not
        assume that ``primary_key`` is sufficient.
        """

        return [
            column
            for column in self.columns
            if column.primary_key
        ]

    @property
    def is_composite_primary_key(self) -> bool:
        """Return True when the table has more than one PK column."""

        return len(self.primary_key_columns) > 1

    @property
    def has_foreign_keys(self) -> bool:
        """Return True when the table contains at least one foreign key."""

        return bool(self.foreign_keys)

    @property
    def is_junction_table(self) -> bool:
        """
        Return True when the table appears to be a relationship table.

        A junction table is identified conservatively as a table with at
        least two foreign keys. This is metadata classification only; it
        does not impose any application-specific meaning.
        """

        return len(self.foreign_keys) >= 2

    def column(self, name: str) -> ColumnInfo | None:
        """Return a column by name, using case-insensitive comparison."""

        lookup_name = name.casefold()

        for column in self.columns:
            if column.name.casefold() == lookup_name:
                return column

        return None

    def has_column(self, name: str) -> bool:
        """Return True when the table contains the named column."""

        return self.column(name) is not None


class SchemaManager:
    """
    Discover, cache, and query SQLite schema metadata.

    The manager keeps the database schema in memory after ``load()``.
    Call ``refresh()`` when the underlying database structure changes.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.db = database
        self._tables: dict[str, TableInfo] = {}
        self.loaded = False

    @property
    def tables(self) -> dict[str, TableInfo]:
        """
        Return the cached tables.

        The returned dictionary is the manager's internal dictionary.
        Callers should treat it as read-only.
        """

        return self._tables

    def clear(self) -> None:
        """Discard all cached schema information."""

        self._tables.clear()
        self.loaded = False

    def load(self) -> None:
        """
        Load the complete database schema into memory.

        The method first discovers all user tables, then loads their
        columns, foreign keys, indexes, and row counts. Finally it builds
        the parent/child relationship graph.
        """

        tables = self.db.tables()

        discovered: dict[str, TableInfo] = {}

        for table_name in tables:
            table = TableInfo(name=table_name)

            table.columns = self._load_columns(table_name)
            table.foreign_keys = self._load_foreign_keys(table_name)
            table.indexes = self._load_indexes(table_name)
            table.row_count = self._load_row_count(table_name)

            discovered[table_name.casefold()] = table

        self._build_relationship_graph(discovered)

        self._tables = discovered
        self.loaded = True

    def refresh(self) -> None:
        """Discard cached metadata and reload the database schema."""

        self.clear()
        self.load()

    def get_table(self, table_name: str) -> TableInfo:
        """
        Return metadata for a table.

        Raises:
            KeyError: If the requested table is not present.
        """

        key = self._normalise_table_key(table_name)

        try:
            return self._tables[key]
        except KeyError as exc:
            raise KeyError(
                f"Unknown table '{table_name}'."
            ) from exc

    def get_table_or_none(
        self,
        table_name: str,
    ) -> TableInfo | None:
        """Return table metadata or None when the table does not exist."""

        return self._tables.get(
            self._normalise_table_key(table_name)
        )

    def table_names(self) -> list[str]:
        """Return cached table names in alphabetical order."""

        return sorted(
            (table.name for table in self._tables.values()),
            key=str.casefold,
        )

    def parent_tables(self, table_name: str) -> list[TableInfo]:
        """
        Return tables referenced by the specified table's foreign keys.
        """

        table = self.get_table(table_name)

        result: list[TableInfo] = []

        for parent_name in sorted(
            table.parent_tables,
            key=str.casefold,
        ):
            parent = self.get_table_or_none(parent_name)

            if parent is not None:
                result.append(parent)

        return result

    def child_tables(self, table_name: str) -> list[TableInfo]:
        """
        Return tables that contain foreign keys referencing this table.
        """

        table = self.get_table(table_name)

        result: list[TableInfo] = []

        for child_name in sorted(
            table.child_tables,
            key=str.casefold,
        ):
            child = self.get_table_or_none(child_name)

            if child is not None:
                result.append(child)

        return result

    def foreign_keys_to(
        self,
        table_name: str,
    ) -> list[tuple[TableInfo, ForeignKeyInfo]]:
        """
        Return all foreign keys in other tables pointing to ``table_name``.
        """

        target = self.get_table(table_name)
        target_name = target.name.casefold()

        result: list[tuple[TableInfo, ForeignKeyInfo]] = []

        for table in self._tables.values():
            for foreign_key in table.foreign_keys:
                if (
                    foreign_key.referenced_table.casefold()
                    == target_name
                ):
                    result.append((table, foreign_key))

        return result

    def __contains__(self, table_name: str) -> bool:
        """Return True when the table exists in the cached schema."""

        return (
            self._normalise_table_key(table_name)
            in self._tables
        )

    def __len__(self) -> int:
        """Return the number of cached tables."""

        return len(self._tables)

    def __iter__(self) -> Iterator[TableInfo]:
        """Iterate over cached tables in alphabetical order."""

        for table_name in self.table_names():
            yield self._tables[table_name.casefold()]

    def _load_columns(
        self,
        table_name: str,
    ) -> list[ColumnInfo]:
        """Load column metadata for one table."""

        result: list[ColumnInfo] = []

        for row in self.db.columns(table_name):
            result.append(
                ColumnInfo(
                    cid=int(row["cid"]),
                    name=str(row["name"]),
                    data_type=str(row["type"] or ""),
                    not_null=bool(row["notnull"]),
                    default_value=(
                        None
                        if row["dflt_value"] is None
                        else str(row["dflt_value"])
                    ),
                    primary_key=bool(row["pk"]),
                )
            )

        return result

    def _load_foreign_keys(
        self,
        table_name: str,
    ) -> list[ForeignKeyInfo]:
        """Load foreign-key metadata for one table."""

        result: list[ForeignKeyInfo] = []

        for row in self.db.foreign_keys(table_name):
            result.append(
                ForeignKeyInfo(
                    id=int(row["id"]),
                    sequence=int(row["seq"]),
                    column=str(row["from"]),
                    referenced_table=str(row["table"]),
                    referenced_column=str(row["to"]),
                    on_update=str(row["on_update"] or ""),
                    on_delete=str(row["on_delete"] or ""),
                    match=str(row["match"] or ""),
                )
            )

        return result

    def _load_indexes(
        self,
        table_name: str,
    ) -> list[IndexInfo]:
        """Load index metadata for one table."""

        result: list[IndexInfo] = []

        for row in self.db.indexes(table_name):
            result.append(
                IndexInfo(
                    sequence=int(row["seq"]),
                    name=str(row["name"]),
                    unique=bool(row["unique"]),
                    origin=str(row["origin"]),
                    partial=bool(row["partial"]),
                )
            )

        return result

    def _load_row_count(
        self,
        table_name: str,
    ) -> int:
        """
        Return the number of rows in a table.

        Table names originate from SQLite's schema and are therefore not
        user-entered SQL. They are still quoted defensively.
        """

        quoted_table = self._quote_identifier(table_name)

        row = self.db.fetchone(
            f"SELECT COUNT(*) AS row_count "
            f"FROM {quoted_table}"
        )

        if row is None:
            return 0

        value = row["row_count"]

        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def _build_relationship_graph(
        self,
        tables: dict[str, TableInfo],
    ) -> None:
        """Populate parent and child table relationships."""

        for table in tables.values():
            table.parent_tables.clear()
            table.child_tables.clear()

        for table in tables.values():
            for foreign_key in table.foreign_keys:
                parent_key = (
                    foreign_key.referenced_table.casefold()
                )

                parent = tables.get(parent_key)

                if parent is None:
                    continue

                table.parent_tables.add(parent.name)
                parent.child_tables.add(table.name)

    @staticmethod
    def _normalise_table_key(
        table_name: str,
    ) -> str:
        """Return the canonical dictionary key for a table name."""

        return table_name.strip().casefold()

    @staticmethod
    def _quote_identifier(identifier: str) -> str:
        """
        Quote a SQLite identifier safely.

        Double quotes are escaped according to SQLite's identifier rules.
        """

        escaped = identifier.replace('"', '""')
        return f'"{escaped}"'
```
