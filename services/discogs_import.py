"""
=========================================================
Music Collection Manager
Discogs Collection Import
=========================================================

Milestone 6B (1/N)

Bring a newer Discogs collection export (the CSV you can download
from your Discogs collection) into the Discogs table.

* Releases already in the table (matched on release_id) are
  UPDATED when any exported column differs.
* Releases not in the table yet are ADDED, with the next free ID
  and the usual https://www.discogs.com/release/<id> link.
* Nothing is ever DELETED. A release that is in the database but
  missing from the file is only counted, because it may be linked
  to a Record and removing it is the user's decision.
* Records are never touched, and release_id is never changed, so
  existing Record <-> release links stay valid.

Reading the file and previewing the outcome change nothing;
apply() does all its writes in a single transaction, so a failure
part-way leaves the table exactly as it was.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from core.context import DatabaseContext
from core.repository import Repository, repository_for

# The columns a Discogs collection export carries (besides
# release_id, which identifies the row). ID and discogs_url are
# not in the export; the importer fills them in for new rows.
IMPORT_COLUMNS = [
    "Catalog#",
    "Artist",
    "Title",
    "Label",
    "Format",
    "Rating",
    "Released",
    "CollectionFolder",
    "Date Added",
    "Collection Media Condition",
    "Collection Sleeve Condition",
    "Collection Notes",
]

RELEASE_URL = "https://www.discogs.com/release/"


class DiscogsImportError(Exception):
    """Raised when a file cannot be read as a Discogs collection export."""


@dataclass(frozen=True, slots=True)
class ImportChange:
    """One existing release whose exported data differs."""

    release_id: str
    updates: dict[str, Any]
    previous: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ImportPreview:
    """What an import would do, computed without changing anything."""

    new_rows: list[dict[str, Any]] = field(default_factory=list)
    changes: list[ImportChange] = field(default_factory=list)
    unchanged_count: int = 0
    missing_count: int = 0
    problems: list[str] = field(default_factory=list)

    @property
    def has_work(self) -> bool:
        return bool(self.new_rows or self.changes)


@dataclass(frozen=True, slots=True)
class ImportResult:
    inserted: int
    updated: int


class DiscogsImporter:
    """Reads a Discogs export and applies it to the Discogs table."""

    def __init__(self, context: DatabaseContext) -> None:
        self.context = context
        self._discogs: Repository = repository_for(context, "Discogs")

    # ========================================================
    # Reading
    # ========================================================

    def read_export(
        self, path: Path
    ) -> tuple[list[dict[str, Any]], list[str]]:
        """
        Parse the file into cleaned row dicts (release_id plus
        whichever IMPORT_COLUMNS the file has; blank cells become
        None). Returns (rows, problems); problems describe rows that
        were skipped.
        """

        try:
            with open(path, newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)
                header = reader.fieldnames or []

                if "release_id" not in header:
                    raise DiscogsImportError(
                        "This does not look like a Discogs collection "
                        "export: there is no release_id column."
                    )

                present = [c for c in IMPORT_COLUMNS if c in header]
                rows: list[dict[str, Any]] = []
                problems: list[str] = []
                seen: set[str] = set()

                for line_number, raw in enumerate(reader, start=2):
                    release_id = (raw.get("release_id") or "").strip()

                    if not release_id.isdigit():
                        problems.append(
                            f"Line {line_number}: missing or invalid "
                            f"release_id ({release_id!r}) - skipped."
                        )
                        continue

                    if release_id in seen:
                        problems.append(
                            f"Line {line_number}: release {release_id} "
                            "appears more than once - first one kept."
                        )
                        continue

                    seen.add(release_id)

                    row: dict[str, Any] = {"release_id": release_id}
                    for column in present:
                        value = (raw.get(column) or "").strip()
                        row[column] = value or None
                    rows.append(row)
        except (OSError, UnicodeDecodeError, csv.Error) as exc:
            raise DiscogsImportError(f"Cannot read the file: {exc}") from exc

        return rows, problems

    # ========================================================
    # Preview and apply
    # ========================================================

    def preview(self, path: Path) -> ImportPreview:
        """Work out what importing this file would do, without doing it."""

        rows, problems = self.read_export(path)
        existing = {row["release_id"]: row for row in self._discogs.all()}

        new_rows: list[dict[str, Any]] = []
        changes: list[ImportChange] = []
        unchanged = 0

        for row in rows:
            current = existing.get(row["release_id"])

            if current is None:
                new_rows.append(row)
                continue

            updates = {
                column: value
                for column, value in row.items()
                if column != "release_id"
                and not self._same(current.get(column), value)
            }

            if updates:
                changes.append(
                    ImportChange(
                        row["release_id"],
                        updates,
                        {column: current.get(column) for column in updates},
                    )
                )
            else:
                unchanged += 1

        in_file = {row["release_id"] for row in rows}

        return ImportPreview(
            new_rows=new_rows,
            changes=changes,
            unchanged_count=unchanged,
            missing_count=len(set(existing) - in_file),
            problems=problems,
        )

    def apply(self, preview: ImportPreview) -> ImportResult:
        """
        Write a preview's inserts and updates in one transaction. A
        failure part-way rolls everything back.
        """

        if not preview.has_work:
            return ImportResult(0, 0)

        next_id = (
            max((row["ID"] or 0 for row in self._discogs.all()), default=0) + 1
        )

        with self.context.database.transaction():
            for offset, row in enumerate(preview.new_rows):
                values = dict(row)
                values["ID"] = next_id + offset
                values["discogs_url"] = RELEASE_URL + row["release_id"]
                self._discogs.insert(values, commit=False)

            for change in preview.changes:
                self._discogs.update(
                    change.release_id, change.updates, commit=False
                )

        return ImportResult(len(preview.new_rows), len(preview.changes))

    @staticmethod
    def _same(current: Any, incoming: Any) -> bool:
        return (None if current is None else str(current)) == incoming
