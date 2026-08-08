"""
=========================================================
MusicCollectionManager
Database Context
=========================================================

Coordinates the application's DatabaseManager and
SchemaManager.

This class does NOT replace DatabaseManager.

DatabaseManager remains responsible for SQLite access.
SchemaManager remains responsible for database metadata.

DatabaseContext simply provides one convenient object
through which application components can access both.

Compatible with Python 3.14 and Pylance Strict.
"""

from __future__ import annotations

from core.database import DatabaseManager
from core.schema import SchemaManager


class DatabaseContext:
    """
    Application-level context for database access.

    The context owns no independent SQLite connection.
    It uses the existing DatabaseManager singleton and
    gives SchemaManager access to that same manager.
    """

    def __init__(
        self,
        database: DatabaseManager | None = None,
    ) -> None:
        """
        Create a database context.

        Args:
            database:
                Optional existing DatabaseManager.

                When omitted, the application's existing
                DatabaseManager singleton is used.
        """

        self.database = (
            database
            if database is not None
            else DatabaseManager()
        )

        self.schema = SchemaManager(
            self.database
        )

        self._started = False

    # =====================================================
    # Lifecycle
    # =====================================================

    @property
    def started(self) -> bool:
        """Return True when the context has been started."""

        return self._started

    # -----------------------------------------------------

    def start(
        self,
        load_schema: bool = True,
    ) -> None:
        """
        Start the database context.

        The database connection is opened first. The schema
        is then optionally loaded.

        Args:
            load_schema:
                When True, load the complete database schema.
        """

        if self._started:
            return

        self.database.connect()

        if load_schema:
            self.schema.load()

        self._started = True

    # -----------------------------------------------------

    def refresh_schema(self) -> None:
        """
        Refresh cached schema information.

        The database connection must be available.
        """

        if not self.database.connected:
            self.database.connect()

        self.schema.refresh()

    # -----------------------------------------------------

    def close(self) -> None:
        """
        Close the database context.

        The schema cache is cleared and the shared database
        connection is disconnected.
        """

        self.schema.clear()

        self.database.disconnect()

        self._started = False

    # =====================================================
    # Context-manager support
    # =====================================================

    def __enter__(self) -> DatabaseContext:
        """Start and return the context."""

        self.start()

        return self

    # -----------------------------------------------------

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        """Close the context."""

        self.close()