"""
=========================================================
Music Collection Manager
Generic Metadata-Aware Repository
=========================================================

Milestone 2A

Provides generic CRUD operations for SQLite tables using
the metadata discovered by SchemaManager.

Design goals
------------
* Do not duplicate CRUD code for every table.
* Respect single and composite primary keys.
* Validate table and column names against the loaded schema.
* Quote SQLite identifiers safely.
* Use parameterized SQL values.
* Keep transaction control in DatabaseManager.
* Do not contain any PySide6/UI code.

Compatible with Python 3.14 and Pylance Strict.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from core.context import DatabaseContext
from core.database import DatabaseError, QueryError
from core.schema import TableInfo


# =========================================================
# Exceptions
# =========================================================


class RepositoryError(DatabaseError):
    """Base exception for repository operations."""


class RepositoryValidationError(RepositoryError):
    """Raised when repository input does not match the schema."""


class RecordNotFoundError(RepositoryError):
    """Raised when an expected database record does not exist."""


class PrimaryKeyError(RepositoryValidationError):
    """Raised when primary-key information is invalid."""


# =========================================================
# Repository
# =========================================================


class Repository:
    """
    Generic metadata-aware repository for one SQLite table.

    The repository does not own a database connection.

    It uses DatabaseContext, which provides:
        context.database -> DatabaseManager
        context.schema   -> SchemaManager
    """

    def __init__(
        self,
        context: DatabaseContext,
        table_name: str,
    ) -> None:
        self.context = context
        self.db = context.database
        self.schema = context.schema

        if not self.schema.loaded:
            self.schema.load()

        self.table: TableInfo = self.schema.get_table(table_name)

    # =====================================================
    # Basic metadata
    # =====================================================

    @property
    def table_name(self) -> str:
        """Return the actual SQLite table name."""

        return self.table.name

    @property
    def columns(self) -> list[str]:
        """Return column names in SQLite declaration order."""

        return [
            column.name
            for column in self.table.columns
        ]

    @property
    def primary_key_columns(self) -> list[str]:
        """Return all primary-key column names."""

        return [
            column.name
            for column in self.table.primary_key_columns
        ]

    @property
    def is_composite_key(self) -> bool:
        """Return True when the table has a composite primary key."""

        return self.table.is_composite_primary_key

    @property
    def foreign_key_columns(self) -> list[str]:
        """Return columns participating in foreign keys."""

        return [
            foreign_key.column
            for foreign_key in self.table.foreign_keys
        ]

    @property
    def row_count(self) -> int:
        """Return the current number of rows."""

        return self.count()

    # =====================================================
    # Identifier handling
    # =====================================================

    @staticmethod
    def _quote_identifier(identifier: str) -> str:
        """
        Quote a SQLite identifier.

        SQLite identifiers cannot be passed as SQL parameters,
        so table and column names must be validated and quoted
        separately from values.
        """

        if not identifier:
            raise RepositoryValidationError(
                "SQLite identifier cannot be empty."
            )

        escaped = identifier.replace('"', '""')

        return f'"{escaped}"'

    # -----------------------------------------------------

    def _validate_columns(
        self,
        values: Mapping[str, Any],
    ) -> None:
        """
        Ensure every supplied column exists in this table.
        """

        known_columns = {
            column.casefold()
            for column in self.columns
        }

        for column in values:
            if column.casefold() not in known_columns:
                raise RepositoryValidationError(
                    f"Unknown column '{column}' "
                    f"for table '{self.table_name}'."
                )

    # -----------------------------------------------------

    def _actual_column_name(
        self,
        column_name: str,
    ) -> str:
        """
        Return the schema's actual column spelling.

        SQLite column lookup is case-insensitive, but using
        the actual declared name keeps generated SQL clear.
        """

        column = self.table.column(column_name)

        if column is None:
            raise RepositoryValidationError(
                f"Unknown column '{column_name}' "
                f"for table '{self.table_name}'."
            )

        return column.name

    # =====================================================
    # Primary-key handling
    # =====================================================

    def _normalise_key(
        self,
        key: Any,
    ) -> dict[str, Any]:
        """
        Convert a primary-key argument into a dictionary.

        Supported forms
        ----------------
        Single primary key:

            repository.get(123)

        or:

            repository.get({"ArtistID": 123})

        Composite primary key:

            repository.get({
                "ProgramID": 10,
                "Position": 3,
            })

        or:

            repository.get((10, 3))
        """

        primary_keys = self.primary_key_columns

        if not primary_keys:
            raise PrimaryKeyError(
                f"Table '{self.table_name}' has no primary key."
            )

        # Dictionary form
        if isinstance(key, Mapping):
            result: dict[str, Any] = {}

            supplied = {
                name.casefold(): value
                for name, value in key.items()
            }

            for primary_key in primary_keys:
                lookup = primary_key.casefold()

                if lookup not in supplied:
                    raise PrimaryKeyError(
                        f"Missing primary-key value "
                        f"'{primary_key}'."
                    )

                result[primary_key] = supplied[lookup]

            return result

        # Single scalar form
        if len(primary_keys) == 1:
            return {
                primary_keys[0]: key,
            }

        # Composite sequence form
        if isinstance(key, Sequence) and not isinstance(
            key,
            (str, bytes, bytearray),
        ):
            if len(key) != len(primary_keys):
                raise PrimaryKeyError(
                    f"Table '{self.table_name}' requires "
                    f"{len(primary_keys)} primary-key values; "
                    f"received {len(key)}."
                )

            return dict(
                zip(
                    primary_keys,
                    key,
                )
            )

        raise PrimaryKeyError(
            f"Invalid primary key for table "
            f"'{self.table_name}'."
        )

    # -----------------------------------------------------

    def _where_primary_key(
        self,
        key: Any,
    ) -> tuple[str, tuple[Any, ...]]:
        """
        Build a WHERE clause for a primary key.

        Returns:
            SQL WHERE fragment
            parameter tuple
        """

        key_values = self._normalise_key(key)

        clauses: list[str] = []
        parameters: list[Any] = []

        for column_name, value in key_values.items():
            quoted = self._quote_identifier(
                self._actual_column_name(column_name)
            )

            if value is None:
                clauses.append(
                    f"{quoted} IS NULL"
                )
            else:
                clauses.append(
                    f"{quoted} = ?"
                )
                parameters.append(value)

        return (
            " AND ".join(clauses),
            tuple(parameters),
        )

    # =====================================================
    # READ
    # =====================================================

    def all(
        self,
        *,
        order_by: str | Sequence[str] | None = None,
        descending: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Return all rows.

        Args:
            order_by:
                Optional column name or sequence of column names.

            descending:
                Apply DESC ordering when True.

        Returns:
            List of ordinary dictionaries.
        """

        sql = (
            f"SELECT * FROM "
            f"{self._quote_identifier(self.table_name)}"
        )

        if order_by is not None:
            if isinstance(order_by, str):
                order_columns = [order_by]
            else:
                order_columns = list(order_by)

            self._validate_order_columns(order_columns)

            direction = "DESC" if descending else "ASC"

            sql += " ORDER BY "
            sql += ", ".join(
                self._quote_identifier(
                    self._actual_column_name(column)
                )
                for column in order_columns
            )
            sql += f" {direction}"

        rows = self.db.fetchall(sql)

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    # -----------------------------------------------------

    def find(
        self,
        filters: Mapping[str, Any] | None = None,
        *,
        order_by: str | Sequence[str] | None = None,
        descending: bool = False,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Return rows matching equality filters.

        Example:

            repository.find({
                "StyleID": 4,
            })
        """

        if filters is None:
            filters = {}

        self._validate_columns(filters)

        sql = (
            f"SELECT * FROM "
            f"{self._quote_identifier(self.table_name)}"
        )

        clauses: list[str] = []
        parameters: list[Any] = []

        for column_name, value in filters.items():
            actual_name = self._actual_column_name(
                column_name
            )

            quoted = self._quote_identifier(actual_name)

            if value is None:
                clauses.append(
                    f"{quoted} IS NULL"
                )
            else:
                clauses.append(
                    f"{quoted} = ?"
                )
                parameters.append(value)

        if clauses:
            sql += " WHERE " + " AND ".join(clauses)

        if order_by is not None:
            if isinstance(order_by, str):
                order_columns = [order_by]
            else:
                order_columns = list(order_by)

            self._validate_order_columns(order_columns)

            direction = "DESC" if descending else "ASC"

            sql += " ORDER BY "
            sql += ", ".join(
                self._quote_identifier(
                    self._actual_column_name(column)
                )
                for column in order_columns
            )
            sql += f" {direction}"

        if limit is not None:
            if limit < 0:
                raise RepositoryValidationError(
                    "limit cannot be negative."
                )

            sql += " LIMIT ?"
            parameters.append(limit)

        if offset is not None:
            if offset < 0:
                raise RepositoryValidationError(
                    "offset cannot be negative."
                )

            if limit is None:
                sql += " LIMIT -1"

            sql += " OFFSET ?"
            parameters.append(offset)

        rows = self.db.fetchall(
            sql,
            tuple(parameters),
        )

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    # -----------------------------------------------------

    def get(
        self,
        key: Any,
    ) -> dict[str, Any] | None:
        """
        Return one row by primary key.

        Returns None when the record does not exist.
        """

        where_sql, parameters = self._where_primary_key(
            key
        )

        sql = (
            f"SELECT * FROM "
            f"{self._quote_identifier(self.table_name)} "
            f"WHERE {where_sql} "
            f"LIMIT 1"
        )

        row = self.db.fetchone(
            sql,
            parameters,
        )

        if row is None:
            return None

        return self._row_to_dict(row)

    # -----------------------------------------------------

    def require(
        self,
        key: Any,
    ) -> dict[str, Any]:
        """
        Return one row by primary key.

        Raises RecordNotFoundError when absent.
        """

        row = self.get(key)

        if row is None:
            raise RecordNotFoundError(
                f"Record not found in table "
                f"'{self.table_name}'."
            )

        return row

    # -----------------------------------------------------

    def count(
        self,
        filters: Mapping[str, Any] | None = None,
    ) -> int:
        """Return the number of matching rows."""

        if filters is None:
            filters = {}

        self._validate_columns(filters)

        sql = (
            f"SELECT COUNT(*) AS total "
            f"FROM {self._quote_identifier(self.table_name)}"
        )

        clauses: list[str] = []
        parameters: list[Any] = []

        for column_name, value in filters.items():
            quoted = self._quote_identifier(
                self._actual_column_name(column_name)
            )

            if value is None:
                clauses.append(
                    f"{quoted} IS NULL"
                )
            else:
                clauses.append(
                    f"{quoted} = ?"
                )
                parameters.append(value)

        if clauses:
            sql += " WHERE " + " AND ".join(clauses)

        row = self.db.fetchone(
            sql,
            tuple(parameters),
        )

        if row is None:
            return 0

        return int(row["total"])

    # =====================================================
    # CREATE
    # =====================================================

    def insert(
        self,
        values: Mapping[str, Any],
        *,
        commit: bool = False,
    ) -> Any:
        """
        Insert one row.

        Args:
            values:
                Mapping of column names to values.

            commit:
                When True, commit immediately.

        Returns:
            SQLite last_insert_rowid() when available.

        Notes:
            For tables with manually supplied primary keys,
            the returned rowid should not be treated as the
            primary-key value unless the table actually uses
            INTEGER PRIMARY KEY semantics.
        """

        if not values:
            raise RepositoryValidationError(
                "Insert requires at least one value."
            )

        self._validate_columns(values)

        columns: list[str] = []
        parameters: list[Any] = []

        for column_name, value in values.items():
            columns.append(
                self._actual_column_name(column_name)
            )
            parameters.append(value)

        quoted_columns = ", ".join(
            self._quote_identifier(column)
            for column in columns
        )

        placeholders = ", ".join(
            "?" for _ in parameters
        )

        sql = (
            f"INSERT INTO "
            f"{self._quote_identifier(self.table_name)} "
            f"({quoted_columns}) "
            f"VALUES ({placeholders})"
        )

        try:
            self.db.execute(
                sql,
                tuple(parameters),
            )

            if commit:
                self.db.commit()

        except QueryError:
            raise

        return self.db.last_insert_id

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        key: Any,
        values: Mapping[str, Any],
        *,
        commit: bool = False,
    ) -> bool:
        """
        Update one row identified by its primary key.

        Returns:
            True when a row was updated.
            False when no matching row exists.
        """

        if not values:
            raise RepositoryValidationError(
                "Update requires at least one value."
            )

        self._validate_columns(values)

        key_values = self._normalise_key(key)

        # Do not silently allow PK changes through this method.
        primary_key_names = {
            name.casefold()
            for name in self.primary_key_columns
        }

        for column_name in values:
            if column_name.casefold() in primary_key_names:
                raise RepositoryValidationError(
                    "Primary-key columns cannot be changed "
                    "by Repository.update()."
                )

        assignments: list[str] = []
        parameters: list[Any] = []

        for column_name, value in values.items():
            actual_name = self._actual_column_name(
                column_name
            )

            assignments.append(
                f"{self._quote_identifier(actual_name)} = ?"
            )

            parameters.append(value)

        where_sql, key_parameters = (
            self._where_primary_key(key_values)
        )

        parameters.extend(key_parameters)

        sql = (
            f"UPDATE "
            f"{self._quote_identifier(self.table_name)} "
            f"SET {', '.join(assignments)} "
            f"WHERE {where_sql}"
        )

        cursor = self.db.execute(
            sql,
            tuple(parameters),
        )

        if commit:
            self.db.commit()

        return cursor.rowcount > 0

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        key: Any,
        *,
        commit: bool = False,
    ) -> bool:
        """
        Delete one row identified by its primary key.

        Returns:
            True when a row was deleted.
            False when no matching row existed.

        SQLite foreign-key enforcement is controlled by
        DatabaseManager. Integrity errors are allowed to
        propagate as QueryError.
        """

        where_sql, parameters = self._where_primary_key(
            key
        )

        sql = (
            f"DELETE FROM "
            f"{self._quote_identifier(self.table_name)} "
            f"WHERE {where_sql}"
        )

        cursor = self.db.execute(
            sql,
            parameters,
        )

        if commit:
            self.db.commit()

        return cursor.rowcount > 0

    # =====================================================
    # Utility operations
    # =====================================================

    def exists(
        self,
        key: Any,
    ) -> bool:
        """Return True when a primary-key record exists."""

        return self.get(key) is not None

    # -----------------------------------------------------

    def primary_key_for(
        self,
        row: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Extract the complete primary key from a row.

        Useful for UI code that receives a row dictionary.
        """

        self._validate_columns(row)

        result: dict[str, Any] = {}

        for column_name in self.primary_key_columns:
            if column_name not in row:
                # Case-insensitive fallback.
                found = False

                for supplied_name, value in row.items():
                    if (
                        supplied_name.casefold()
                        == column_name.casefold()
                    ):
                        result[column_name] = value
                        found = True
                        break

                if not found:
                    raise PrimaryKeyError(
                        f"Row does not contain primary-key "
                        f"column '{column_name}'."
                    )
            else:
                result[column_name] = row[column_name]

        return result

    # -----------------------------------------------------

    def foreign_key_targets(
        self,
        column_name: str,
    ) -> list[tuple[str, str]]:
        """
        Return foreign-key targets for a column.

        Returns:
            List of (table, column) pairs.
        """

        actual_name = self._actual_column_name(
            column_name
        )

        return [
            (
                foreign_key.referenced_table,
                foreign_key.referenced_column,
            )
            for foreign_key in self.table.foreign_keys
            if (
                foreign_key.column.casefold()
                == actual_name.casefold()
            )
        ]

    # =====================================================
    # Internal helpers
    # =====================================================

    def _validate_order_columns(
        self,
        columns: Sequence[str],
    ) -> None:
        """Validate ORDER BY columns against the schema."""

        known_columns = {
            column.casefold()
            for column in self.columns
        }

        for column in columns:
            if column.casefold() not in known_columns:
                raise RepositoryValidationError(
                    f"Unknown ORDER BY column '{column}' "
                    f"for table '{self.table_name}'."
                )

    # -----------------------------------------------------

    @staticmethod
    def _row_to_dict(
        row: Any,
    ) -> dict[str, Any]:
        """Convert sqlite3.Row to a normal dictionary."""

        if hasattr(row, "keys"):
            return {
                str(key): row[key]
                for key in row.keys()
            }

        if isinstance(row, Mapping):
            return dict(row)

        raise RepositoryError(
            "Database returned an unsupported row type."
        )


# =========================================================
# Convenience factory
# =========================================================


def repository_for(
    context: DatabaseContext,
    table_name: str,
) -> Repository:
    """
    Create a Repository for a table.

    This small factory is useful for future service and UI
    code where the table name is selected dynamically.
    """

    return Repository(
        context=context,
        table_name=table_name,
    )
