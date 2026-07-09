"""
=========================================================
Music Collection Manager
Database Manager
=========================================================

Author : OpenAI / ChatGPT

This module provides the ONLY access point to the SQLite
database.

No other part of the application should import sqlite3.

Responsibilities

    • Open / close database
    • Execute SQL
    • Transactions
    • Query logging
    • Timing
    • Schema access
    • Context manager support

"""

from __future__ import annotations

import sqlite3
import logging
import time

from pathlib import Path
from types import TracebackType
from typing import Any
from typing import Optional
from typing import Sequence
from typing import Type

import config


class DatabaseError(Exception):
    """Base database exception."""


class ConnectionError(DatabaseError):
    """Cannot connect to database."""


class QueryError(DatabaseError):
    """SQL execution error."""


class DatabaseManager:
    """
    Singleton SQLite manager.

    There should only ever be ONE instance of this class.
    """

    _instance = None

    # --------------------------------------------------

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    # --------------------------------------------------

    def __init__(self):

        if hasattr(self, "_initialised"):

            return

        self._initialised = True

        self.database: Path = config.DATABASE_FILE

        self.connection: Optional[sqlite3.Connection] = None

        self.cursor: Optional[sqlite3.Cursor] = None

        self.connected = False

        self.logger = logging.getLogger("Database")

    # --------------------------------------------------
    # Context manager
    # --------------------------------------------------

    def __enter__(self):

        self.connect()

        return self

    # --------------------------------------------------

    def __exit__(self,
                 exc_type, # type: ignore
                 exc_val, # type: ignore
                 exc_tb): # type: ignore

        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self.disconnect()

    # --------------------------------------------------
    # Connection
    # --------------------------------------------------

    def connect(self):

        """
        Connect to SQLite.
        """

        if self.connected:

            return

        if not self.database.exists():

            raise ConnectionError(
                f"Database not found:\n{self.database}"
            )

        self.logger.info(
            "Opening database %s",
            self.database
        )

        try:

            self.connection = sqlite3.connect(
                self.database,
                detect_types=sqlite3.PARSE_DECLTYPES,
            )

            self.connection.row_factory = sqlite3.Row

            self.cursor = self.connection.cursor()

            #
            # IMPORTANT
            #

            self.cursor.execute(
                "PRAGMA foreign_keys = ON"
            )

            self.connected = True

            self.logger.info("Connected.")

        except sqlite3.Error as err:

            raise ConnectionError(str(err))

    # --------------------------------------------------

    def disconnect(self):

        """
        Close database.
        """

        if not self.connected:
            assert self.cursor is not None
            return

        self.connection.close() # type: ignore

        self.connected = False

        self.logger.info("Disconnected.")

    # --------------------------------------------------

    def commit(self):

        if self.connection:

            self.connection.commit()

    # --------------------------------------------------

    def rollback(self):

        if self.connection:

            self.connection.rollback()

    # --------------------------------------------------

    def begin(self):

        self.execute("BEGIN")

    # --------------------------------------------------
    # Internal helpers
    # --------------------------------------------------

    def _timer(self):

        return time.perf_counter()

    # --------------------------------------------------

    def _log_query(
        self,
        sql: str,
        elapsed: float
    ):

        self.logger.debug(
            "%.3f ms | %s",
            elapsed * 1000,
            sql.replace("\n", " ")
        )

    # --------------------------------------------------
    # SQL execution
    # --------------------------------------------------

    def execute(
        self,
        sql: str,
        parameters: Sequence[Any] | None = None
    ) -> sqlite3.Cursor:

        """
        Execute one SQL statement.

        Returns the cursor.
        """

        if not self.connected:

            self.connect()

        assert self.cursor is not None

        if parameters is None:

            parameters = ()

        start = self._timer()

        try:

            cursor = self.cursor.execute(
                sql,
                tuple(parameters)
            )

        except sqlite3.Error as err:

            self.logger.exception(sql)

            raise QueryError(str(err))

        elapsed = self._timer() - start

        self._log_query(sql, elapsed)

        return cursor

    # --------------------------------------------------

    def executemany(
        self,
        sql: str,
        values: Sequence[Sequence[Any]]
    ):

        if not self.connected:

            self.connect()

        assert self.cursor is not None

        start = self._timer()

        try:

            self.cursor.executemany(
                sql,
                values
            )

        except sqlite3.Error as err:

            raise QueryError(str(err))

        elapsed = self._timer() - start

        self._log_query(sql, elapsed)

    # --------------------------------------------------

    def fetchone(
        self,
        sql: str,
        parameters=None # type: ignore
    ):

        return self.execute(
            sql,
            parameters # type: ignore
        ).fetchone()

    # --------------------------------------------------

    def fetchall(
        self,
        sql: str,
        parameters=None # type: ignore
    ):

        return self.execute(
            sql,
            parameters # type: ignore
        ).fetchall()
    
    # --------------------------------------------------
    # Transaction context manager
    # --------------------------------------------------

    class _Transaction:
        """
        Internal transaction context manager.

        Usage:
            with db.transaction():
                ...
        """

        def __init__(self, db: "DatabaseManager"):
            self.db = db

        def __enter__(self):
            self.db.begin()
            return self.db

        def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
        ) -> bool:

            if exc_type is None:
                self.db.commit()
            else:
                self.db.rollback()

            # propagate any exception
            return False

    # --------------------------------------------------

    def transaction(self):
        """
        Returns a transaction context manager.
        """

        return DatabaseManager._Transaction(self)

    # --------------------------------------------------
    # Schema information
    # --------------------------------------------------

    def tables(self) -> list[str]:
        """
        Return all user tables.
        """

        rows = self.fetchall( # type: ignore
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )

        return [row["name"] for row in rows]

    # --------------------------------------------------

    def columns(self, table: str):

        return self.fetchall( # type: ignore
            f"PRAGMA table_info([{table}])"
        )

    # --------------------------------------------------

    def foreign_keys(self, table: str):

        return self.fetchall( # type: ignore
            f"PRAGMA foreign_key_list([{table}])"
        )

    # --------------------------------------------------

    def indexes(self, table: str):

        return self.fetchall( # type: ignore
            f"PRAGMA index_list([{table}])"
        )

    # --------------------------------------------------

    def primary_key(self, table: str):

        for column in self.columns(table):

            if column["pk"]:
                return column["name"]

        return None

    # --------------------------------------------------

    def table_exists(self, table: str) -> bool:

        row = self.fetchone( # type: ignore
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?
            """,
            (table,)
        )

        return row is not None

    # --------------------------------------------------
    # Generic helpers
    # --------------------------------------------------

    def count(self, table: str) -> int:

        row = self.fetchone( # type: ignore
            f"SELECT COUNT(*) AS total FROM [{table}]"
        )

        return int(row["total"])

    # --------------------------------------------------

    def exists(
        self,
        table: str,
        pk_name: str,
        value # type: ignore
    ) -> bool:

        row = self.fetchone( # type: ignore
            f"""
            SELECT 1
            FROM [{table}]
            WHERE [{pk_name}] = ?
            LIMIT 1
            """,
            (value,)
        )

        return row is not None

    # --------------------------------------------------

    @property
    def last_insert_id(self):

        row = self.fetchone( # type: ignore
            "SELECT last_insert_rowid() AS id"
        )

        return row["id"]

    # --------------------------------------------------
    # Maintenance
    # --------------------------------------------------

    def vacuum(self):

        self.logger.info("VACUUM")

        self.execute("VACUUM")

    # --------------------------------------------------

    def integrity_check(self):

        row = self.fetchone( # type: ignore
            "PRAGMA integrity_check"
        )

        return row[0]

    # --------------------------------------------------

    def analyze(self):

        self.logger.info("ANALYZE")

        self.execute("ANALYZE")

    # --------------------------------------------------
    # Database information
    # --------------------------------------------------

    @property
    def sqlite_version(self):

        row = self.fetchone( # type: ignore
            "SELECT sqlite_version() AS version"
        )

        return row["version"]

    # --------------------------------------------------

    @property
    def database_size(self):

        return self.database.stat().st_size

    # --------------------------------------------------

    @property
    def database_name(self):

        return self.database.name

    # --------------------------------------------------

    @property
    def database_path(self):

        return str(self.database)

    # --------------------------------------------------

    def info(self) -> dict: # type: ignore
        """
        Returns general information about the database.
        """

        return {

            "database": self.database_name,

            "path": self.database_path,

            "sqlite_version": self.sqlite_version,

            "size": self.database_size,

            "tables": len(self.tables()),

            "connected": self.connected

        } # type: ignore
 
