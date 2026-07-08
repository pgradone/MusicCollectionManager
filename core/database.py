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
from typing import Any, Iterable, Optional

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
                 exc_type,
                 exc_val,
                 exc_tb):

        if exc_type is None:

            self.commit()

        else:

            self.rollback()

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

            return

        self.connection.close()

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
        parameters: Iterable[Any] | None = None
    ) -> sqlite3.Cursor:

        """
        Execute one SQL statement.

        Returns the cursor.
        """

        if not self.connected:

            self.connect()

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
        values: Iterable[Iterable[Any]]
    ):

        if not self.connected:

            self.connect()

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
        parameters=None
    ):

        return self.execute(
            sql,
            parameters
        ).fetchone()

    # --------------------------------------------------

    def fetchall(
        self,
        sql: str,
        parameters=None
    ):

        return self.execute(
            sql,
            parameters
        ).fetchall()