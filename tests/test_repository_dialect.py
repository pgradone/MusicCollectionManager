"""
=========================================================
Music Collection Manager
Repository Dialect Tests
=========================================================

Milestone 8A (1/N)

The repository's SQL dialect text is kept in as few places as
possible so that another database could replace it. These tests pin
down the paging clause (the one place LIMIT / OFFSET is spelled) and
check that the by-key lookup carries no paging syntax at all.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from core.context import DatabaseContext
from core.repository import Repository, RepositoryValidationError, repository_for

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATABASE = PROJECT_ROOT / "tests" / "Musi_crud_test.db"


@pytest.fixture()
def context() -> Iterator[DatabaseContext]:
    db_context = DatabaseContext()
    original_path = db_context.database.database

    db_context.database.database = TEST_DATABASE
    db_context.start(load_schema=True)

    try:
        yield db_context
    finally:
        db_context.close()
        db_context.database.database = original_path


@pytest.mark.parametrize(
    ("limit", "offset", "expected_sql", "expected_parameters"),
    [
        (None, None, "", []),
        (5, None, " LIMIT ?", [5]),
        (5, 10, " LIMIT ? OFFSET ?", [5, 10]),
        (0, 0, " LIMIT ? OFFSET ?", [0, 0]),
        # SQLite will not take an OFFSET on its own, so an unbounded
        # LIMIT is added.
        (None, 10, " LIMIT -1 OFFSET ?", [10]),
    ],
)
def test_paging_sql(
    limit: int | None,
    offset: int | None,
    expected_sql: str,
    expected_parameters: list[Any],
) -> None:
    assert Repository._paging_sql(limit, offset) == (
        expected_sql,
        expected_parameters,
    )


@pytest.mark.parametrize(
    ("limit", "offset", "message"),
    [(-1, None, "limit"), (None, -1, "offset"), (3, -2, "offset")],
)
def test_paging_sql_rejects_negative_values(
    limit: int | None, offset: int | None, message: str
) -> None:
    with pytest.raises(RepositoryValidationError, match=message):
        Repository._paging_sql(limit, offset)


def test_all_and_find_use_the_same_paging(context: DatabaseContext) -> None:
    artists = repository_for(context, "Artists")

    assert len(artists.all(limit=3, offset=2)) == 3
    assert len(artists.find({}, limit=3, offset=2)) == 3
    assert [r["ArtistID"] for r in artists.all(limit=3, offset=2)] == [
        r["ArtistID"] for r in artists.find({}, limit=3, offset=2)
    ]
    # offset without limit still works
    assert len(artists.all(offset=len(artists.all()) - 2)) == 2


def test_looking_up_one_row_by_key_sends_no_paging_syntax(
    context: DatabaseContext,
) -> None:
    artists = repository_for(context, "Artists")
    sent: list[str] = []
    real_fetchone = context.database.fetchone

    def spy(sql: str, *args: Any, **kwargs: Any) -> Any:
        sent.append(sql)
        return real_fetchone(sql, *args, **kwargs)

    context.database.fetchone = spy  # type: ignore[method-assign]
    try:
        assert artists.get(1) is not None
    finally:
        context.database.fetchone = real_fetchone  # type: ignore[method-assign]

    assert sent and all("LIMIT" not in sql.upper() for sql in sent)
