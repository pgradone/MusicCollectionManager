"""
=========================================================
Music Collection Manager
Service Layer Foundation
=========================================================

Milestone 3D

Provides the common base class for application services.

Architecture:

    UI
      |
      v
    Service
      |
      v
    Repository
      |
      v
    DatabaseContext
      |              |
      v              v
DatabaseManager   SchemaManager

Services:

* do not import sqlite3;
* do not construct SQL;
* do not own database connections;
* delegate persistence to Repository;
* receive an existing DatabaseContext.
"""

from __future__ import annotations

from core.context import DatabaseContext
from core.repository import Repository, repository_for


class ServiceError(Exception):
    """Base exception for service-layer errors."""


class Service:
    """
    Base class for application services.

    Each concrete service receives an existing
    DatabaseContext and creates a Repository for the
    table handled by that service.

    The service does not own the database lifecycle.
    """

    def __init__(
        self,
        context: DatabaseContext,
        table_name: str,
    ) -> None:
        self.context = context
        self.repository: Repository = repository_for(
            context,
            table_name,
        )

    @property
    def table_name(self) -> str:
        """Return the table handled by this service."""

        return self.repository.table_name