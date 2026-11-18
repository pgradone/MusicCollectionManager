"""
=========================================================
Music Collection Manager
Schema Assumption Tests
=========================================================

Milestone 8A (1/N)

Some behaviour in the application is only correct because of how the
database is designed. These tests turn those assumptions into checks,
run against BOTH the real database and the test copy, so a future
schema change that breaks one fails loudly here, with an explanation.

1. No foreign key cascades.
   Undo delete (services/delete_undo.py) re-inserts the single row
   that was deleted. That restores everything only because every
   foreign key is NO ACTION / RESTRICT: a row that other rows depend
   on cannot be deleted at all. A CASCADE, SET NULL or SET DEFAULT
   rule would let a delete silently change other rows too, and undo
   would then bring back only part of the picture.

2. The main tables have a single-column primary key.
   The record list, delete, undo and navigation all identify a row by
   one key value.

Read-only: neither database is modified.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

import config
from core.context import DatabaseContext

MAIN_TABLES = ["Artists", "Songs", "Records", "Programs", "Styles"]
SAFE_DELETE_RULES = {"NO ACTION", "RESTRICT"}

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASES = {
    "real database": config.DATABASE_FILE,
    "test database": PROJECT_ROOT / "tests" / "Musi_crud_test.db",
}


@pytest.fixture(params=list(DATABASES), ids=list(DATABASES))
def context(request: pytest.FixtureRequest) -> Iterator[DatabaseContext]:
    path = DATABASES[request.param]

    if not path.exists():
        pytest.skip(f"{request.param} not found: {path}")

    db_context = DatabaseContext()
    original_path = db_context.database.database

    db_context.database.database = path
    db_context.start(load_schema=True)

    try:
        yield db_context
    finally:
        db_context.close()
        db_context.database.database = original_path


def test_no_foreign_key_cascades_on_delete(context: DatabaseContext) -> None:
    offenders = [
        f"{table.name}.{fk.column} -> {fk.referenced_table}."
        f"{fk.referenced_column} ON DELETE {fk.on_delete}"
        for table in context.schema.tables.values()
        for fk in table.foreign_keys
        if fk.on_delete.upper() not in SAFE_DELETE_RULES
    ]

    assert not offenders, (
        "Undo delete assumes no foreign key cascades, but these do: "
        + "; ".join(offenders)
        + ". Either make them NO ACTION, or teach services/delete_undo.py "
        "to capture and restore the rows they would change."
    )


@pytest.mark.parametrize("table", MAIN_TABLES)
def test_main_tables_have_a_single_column_primary_key(
    context: DatabaseContext, table: str
) -> None:
    assert context.database.primary_key(table) is not None, (
        f"{table} has no single-column primary key; the record list, "
        "delete and undo all identify a row by one key value."
    )
