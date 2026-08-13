"""
=========================================================
Music Collection Manager
Service Layer Tests
=========================================================

Milestone 3D

pytest tests for the Service base class defined in
services/base_service.py.

Read-only against the application's configured database.
No INSERT, UPDATE, or DELETE operations are performed.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from core.context import DatabaseContext
from core.repository import Repository, repository_for
from services.base_service import Service, ServiceError


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture()
def context() -> Iterator[DatabaseContext]:
    """Provide a started DatabaseContext against the real database."""

    with DatabaseContext() as db_context:
        yield db_context


# ============================================================
# Construction
# ============================================================


def test_service_binds_repository_for_table(
    context: DatabaseContext,
) -> None:
    service = Service(context, "Artists")

    assert service.table_name == "Artists"
    assert isinstance(service.repository, Repository)


def test_service_repository_matches_repository_for_helper(
    context: DatabaseContext,
) -> None:
    service = Service(context, "Songs")
    expected = repository_for(context, "Songs")

    assert service.repository.table_name == expected.table_name
    assert service.repository.columns == expected.columns


def test_service_stores_the_context_it_was_given(
    context: DatabaseContext,
) -> None:
    service = Service(context, "Artists")

    assert service.context is context


# ============================================================
# Composite-key tables
# ============================================================


def test_service_supports_composite_key_tables(
    context: DatabaseContext,
) -> None:
    service = Service(context, "Schedule")

    assert service.repository.is_composite_key is True
    assert service.repository.primary_key_columns == [
        "ProgramID",
        "Position",
    ]


# ============================================================
# Error handling
# ============================================================


def test_service_unknown_table_raises_key_error(
    context: DatabaseContext,
) -> None:
    with pytest.raises(KeyError):
        Service(context, "NoSuchTable123")


def test_service_error_is_a_plain_exception() -> None:
    assert issubclass(ServiceError, Exception)

    with pytest.raises(ServiceError):
        raise ServiceError("boom")