"""
=========================================================
Music Collection Manager
Discogs Import Tests
=========================================================

Milestone 6B (1/N)

pytest tests for services/discogs_import.py.

Runs against the dedicated CRUD test database
(tests/Musi_crud_test.db), never the production database. CSV files
are written to pytest's tmp_path. Test release ids are six digits
starting 9902/9903 and every test removes the rows it adds.
"""

from __future__ import annotations

import csv
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from core.context import DatabaseContext
from core.database import QueryError
from core.repository import repository_for
from services.discogs_import import (
    DiscogsImporter,
    DiscogsImportError,
    ImportPreview,
)
from services.record_service import RecordService

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATABASE = PROJECT_ROOT / "tests" / "Musi_crud_test.db"

HEADER = [
    "Catalog#",
    "Artist",
    "Title",
    "Label",
    "Format",
    "Rating",
    "Released",
    "release_id",
    "CollectionFolder",
    "Date Added",
    "Collection Media Condition",
    "Collection Sleeve Condition",
    "Collection Notes",
]


# ============================================================
# Fixtures and helpers
# ============================================================


@pytest.fixture()
def context() -> Iterator[DatabaseContext]:
    if not TEST_DATABASE.exists():
        raise FileNotFoundError(f"Test database not found:\n{TEST_DATABASE}")

    db_context = DatabaseContext()
    original_path = db_context.database.database

    db_context.database.database = TEST_DATABASE
    db_context.start(load_schema=True)

    try:
        yield db_context
    finally:
        db_context.close()
        db_context.database.database = original_path


@pytest.fixture()
def importer(context: DatabaseContext) -> DiscogsImporter:
    return DiscogsImporter(context)


def write_export(
    path: Path,
    rows: list[dict[str, str]],
    *,
    header: list[str] | None = None,
) -> Path:
    """Write a Discogs-style export (with the BOM Excel adds)."""

    columns = header if header is not None else HEADER

    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return path


def add_release(
    context: DatabaseContext, release_id: str, **values: Any
) -> None:
    repository_for(context, "Discogs").insert(
        {
            "ID": 990000 + int(release_id[2:]),
            "release_id": release_id,
            "Artist": values.pop("Artist", "Zzz Artist"),
            "Title": values.pop("Title", "Zzz Title"),
            **values,
        },
        commit=True,
    )


def drop_releases(context: DatabaseContext, *release_ids: str) -> None:
    discogs = repository_for(context, "Discogs")
    for release_id in release_ids:
        discogs.delete(release_id, commit=True)


# ============================================================
# read_export
# ============================================================


def test_read_export_cleans_values_and_handles_bom(
    importer: DiscogsImporter, tmp_path: Path
) -> None:
    path = write_export(
        tmp_path / "export.csv",
        [
            {
                "Artist": "  Some Artist  ",
                "Title": "A Title",
                "release_id": "990201",
                "Rating": "",
                "Collection Notes": "kept",
            }
        ],
    )

    rows, problems = importer.read_export(path)

    assert problems == []
    assert rows[0]["release_id"] == "990201"
    assert rows[0]["Artist"] == "Some Artist"  # stripped
    assert rows[0]["Rating"] is None  # blank becomes NULL
    assert rows[0]["Collection Notes"] == "kept"


def test_read_export_ignores_columns_it_does_not_know(
    importer: DiscogsImporter, tmp_path: Path
) -> None:
    path = write_export(
        tmp_path / "export.csv",
        [{"release_id": "990202", "Title": "T", "Mystery": "x"}],
        header=["release_id", "Title", "Mystery"],
    )

    rows, _ = importer.read_export(path)

    assert rows == [{"release_id": "990202", "Title": "T"}]


def test_read_export_without_release_id_column_is_rejected(
    importer: DiscogsImporter, tmp_path: Path
) -> None:
    path = write_export(
        tmp_path / "not_discogs.csv",
        [{"Title": "T"}],
        header=["Title"],
    )

    with pytest.raises(DiscogsImportError, match="release_id"):
        importer.read_export(path)


def test_read_export_missing_file_is_a_clear_error(
    importer: DiscogsImporter, tmp_path: Path
) -> None:
    with pytest.raises(DiscogsImportError, match="Cannot read"):
        importer.read_export(tmp_path / "nope.csv")


def test_read_export_skips_bad_and_duplicate_ids(
    importer: DiscogsImporter, tmp_path: Path
) -> None:
    path = write_export(
        tmp_path / "export.csv",
        [
            {"release_id": "990203", "Title": "first"},
            {"release_id": "", "Title": "no id"},
            {"release_id": "abc", "Title": "bad id"},
            {"release_id": "990203", "Title": "duplicate"},
        ],
    )

    rows, problems = importer.read_export(path)

    assert [r["Title"] for r in rows] == ["first"]
    assert len(problems) == 3
    assert any("more than once" in p for p in problems)


# ============================================================
# preview
# ============================================================


def test_preview_classifies_new_changed_unchanged_and_missing(
    importer: DiscogsImporter, context: DatabaseContext, tmp_path: Path
) -> None:
    add_release(context, "990211", Title="Keep Same", Rating="3")
    add_release(context, "990212", Title="Old Title")
    add_release(context, "990213", Title="Absent From File")
    total_before = len(repository_for(context, "Discogs").all())

    try:
        path = write_export(
            tmp_path / "export.csv",
            [
                {"release_id": "990211", "Artist": "Zzz Artist",
                 "Title": "Keep Same", "Rating": "3"},
                {"release_id": "990212", "Artist": "Zzz Artist",
                 "Title": "New Title"},
                {"release_id": "990214", "Artist": "Fresh", "Title": "Brand New"},
            ],
        )

        preview = importer.preview(path)

        assert [r["release_id"] for r in preview.new_rows] == ["990214"]
        assert [c.release_id for c in preview.changes] == ["990212"]
        assert preview.changes[0].updates == {"Title": "New Title"}
        assert preview.changes[0].previous == {"Title": "Old Title"}
        assert preview.unchanged_count == 1
        # Every database release not in the file, mine included.
        assert preview.missing_count == total_before - 2
        assert preview.has_work
    finally:
        drop_releases(context, "990211", "990212", "990213")


def test_preview_only_compares_columns_present_in_the_file(
    importer: DiscogsImporter, context: DatabaseContext, tmp_path: Path
) -> None:
    add_release(context, "990215", Title="Untouched", Rating="4")

    try:
        path = write_export(
            tmp_path / "export.csv",
            [{"release_id": "990215", "Rating": "5"}],
            header=["release_id", "Rating"],
        )

        preview = importer.preview(path)

        assert preview.changes[0].updates == {"Rating": "5"}
    finally:
        drop_releases(context, "990215")


def test_preview_does_not_change_the_database(
    importer: DiscogsImporter, context: DatabaseContext, tmp_path: Path
) -> None:
    before = len(repository_for(context, "Discogs").all())
    path = write_export(
        tmp_path / "export.csv",
        [{"release_id": "990216", "Title": "Would Be New"}],
    )

    importer.preview(path)

    assert len(repository_for(context, "Discogs").all()) == before


# ============================================================
# apply
# ============================================================


def test_apply_inserts_new_and_updates_changed(
    importer: DiscogsImporter, context: DatabaseContext, tmp_path: Path
) -> None:
    discogs = repository_for(context, "Discogs")
    add_release(context, "990221", Title="Old Title")
    highest_id = max(row["ID"] for row in discogs.all())

    try:
        path = write_export(
            tmp_path / "export.csv",
            [
                {"release_id": "990221", "Artist": "Zzz Artist",
                 "Title": "Updated Title"},
                {"release_id": "990222", "Artist": "Fresh", "Title": "Brand New",
                 "Format": '12"'},
            ],
        )

        result = importer.apply(importer.preview(path))

        assert (result.inserted, result.updated) == (1, 1)
        assert discogs.require("990221")["Title"] == "Updated Title"
        new = discogs.require("990222")
        assert new["Title"] == "Brand New"
        assert new["Format"] == '12"'
        assert new["ID"] == highest_id + 1
        assert new["discogs_url"] == "https://www.discogs.com/release/990222"
    finally:
        drop_releases(context, "990221", "990222")


def test_apply_is_idempotent(
    importer: DiscogsImporter, context: DatabaseContext, tmp_path: Path
) -> None:
    try:
        path = write_export(
            tmp_path / "export.csv",
            [{"release_id": "990223", "Artist": "Fresh", "Title": "Once"}],
        )

        importer.apply(importer.preview(path))
        second = importer.preview(path)

        assert not second.has_work
        assert second.unchanged_count == 1
    finally:
        drop_releases(context, "990223")


def test_apply_never_deletes_releases_missing_from_the_file(
    importer: DiscogsImporter, context: DatabaseContext, tmp_path: Path
) -> None:
    add_release(context, "990224", Title="Not In The File")

    try:
        path = write_export(
            tmp_path / "export.csv",
            [{"release_id": "990225", "Artist": "Fresh", "Title": "Other"}],
        )

        importer.apply(importer.preview(path))

        assert repository_for(context, "Discogs").get("990224") is not None
    finally:
        drop_releases(context, "990224", "990225")


def test_apply_keeps_record_links_intact(
    importer: DiscogsImporter, context: DatabaseContext, tmp_path: Path
) -> None:
    records = RecordService(context)
    record_id = records.create(title="Zzz Linked Import Record")
    add_release(context, "990226", Title="Before")
    records.link_discogs(record_id, "990226")

    try:
        path = write_export(
            tmp_path / "export.csv",
            [{"release_id": "990226", "Artist": "Zzz Artist", "Title": "After"}],
        )

        importer.apply(importer.preview(path))

        record = records.require(record_id)
        assert record["Discogs_release"] == "990226"
        assert repository_for(context, "Discogs").require("990226")["Title"] == "After"
    finally:
        records.unlink_discogs(record_id)
        records.delete(record_id)
        drop_releases(context, "990226")


def test_apply_with_nothing_to_do_writes_nothing(
    importer: DiscogsImporter, context: DatabaseContext
) -> None:
    before = len(repository_for(context, "Discogs").all())

    result = importer.apply(ImportPreview())

    assert (result.inserted, result.updated) == (0, 0)
    assert len(repository_for(context, "Discogs").all()) == before


def test_apply_is_all_or_nothing(
    importer: DiscogsImporter,
    context: DatabaseContext,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    discogs = repository_for(context, "Discogs")
    add_release(context, "990227", Title="Original Title")

    real_insert = importer._discogs.insert
    calls = {"count": 0}

    def flaky_insert(values: dict[str, Any], **kwargs: Any) -> Any:
        calls["count"] += 1
        if calls["count"] == 2:
            raise QueryError("simulated failure on the second insert")
        return real_insert(values, **kwargs)

    monkeypatch.setattr(importer._discogs, "insert", flaky_insert)

    try:
        path = write_export(
            tmp_path / "export.csv",
            [
                {"release_id": "990228", "Artist": "A", "Title": "First New"},
                {"release_id": "990229", "Artist": "B", "Title": "Second New"},
                {"release_id": "990227", "Artist": "Zzz Artist",
                 "Title": "Changed Title"},
            ],
        )

        with pytest.raises(QueryError):
            importer.apply(importer.preview(path))

        # The first insert and the update were rolled back too.
        assert discogs.get("990228") is None
        assert discogs.get("990229") is None
        assert discogs.require("990227")["Title"] == "Original Title"
    finally:
        drop_releases(context, "990227", "990228", "990229")
