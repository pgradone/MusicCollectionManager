"""
=========================================================
Music Collection Manager
Delete Undo
=========================================================

Milestone 7B (1/N)

Remembers the last record deleted from a main table so it can be
put back - the cheapest undo that is also safe.

Why this is safe: every foreign key in the database is NO ACTION and
the application turns enforcement on, so a record that other records
still depend on cannot be deleted at all. A deletion therefore only
ever removes one row (and, for a Record, its cover image), and
re-inserting that exact row, with its original primary key, puts
everything back. Undeclared ("soft") references such as
Records.ArtistID start pointing at the right row again by themselves.

Deliberately limited:

* one level - only the most recent deletion is remembered;
* in memory - forgotten when the application closes;
* restoring is refused if the primary key has been taken since.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from core.context import DatabaseContext
from core.repository import repository_for
from services.artwork_service import ArtworkError, ArtworkService

logger = logging.getLogger(__name__)


class UndoError(Exception):
    """Raised when a deletion cannot be undone."""


@dataclass(frozen=True, slots=True)
class DeletedRecord:
    """A deleted row, exactly as it was, with its cover if it had one."""

    table: str
    primary_key_column: str
    row: dict[str, Any]
    cover: bytes | None = None

    @property
    def primary_key_value(self) -> Any:
        return self.row[self.primary_key_column]


@dataclass(frozen=True, slots=True)
class RestoreResult:
    record: DeletedRecord
    # None: the record had no cover. False: it had one that could not
    # be written back (the row itself is restored regardless).
    cover_restored: bool | None


class DeleteUndo:
    """Deletes a row and remembers it so the deletion can be undone."""

    def __init__(
        self,
        context: DatabaseContext,
        artwork: ArtworkService | None = None,
    ) -> None:
        self.context = context
        self._artwork_override = artwork
        self._last: DeletedRecord | None = None

    @property
    def _artwork(self) -> ArtworkService:
        # Looked up each time, like the rest of the application, so a
        # changed configuration is honoured.
        if self._artwork_override is not None:
            return self._artwork_override

        return ArtworkService()

    @property
    def last(self) -> DeletedRecord | None:
        """The deletion that restore() would undo, if any."""

        return self._last

    def delete(self, table: str, key: Any) -> DeletedRecord:
        """
        Delete one row and remember it. Nothing is remembered, and
        nothing is lost, if the database refuses the deletion (for
        example because other records still link to this one).
        """

        primary_key = self.context.database.primary_key(table)

        if primary_key is None:
            raise ValueError(f"{table} has no single-column primary key.")

        repository = repository_for(self.context, table)
        row = dict(repository.require(key))

        # Read the cover before deleting anything: if it cannot be
        # read, the deletion is abandoned rather than losing it.
        cover = self._artwork.read(key) if table == "Records" else None

        repository.delete(key, commit=True)

        if table == "Records":
            try:
                self._artwork.remove(key)
            except OSError as exc:
                logger.warning(
                    "Could not remove the cover of deleted record %s: %s",
                    key,
                    exc,
                )

        self._last = DeletedRecord(table, primary_key, row, cover)

        return self._last

    def restore(self) -> RestoreResult:
        """Put the last deleted record back, with its original ID."""

        deleted = self._last

        if deleted is None:
            raise UndoError("There is nothing to restore.")

        repository = repository_for(self.context, deleted.table)
        key = deleted.primary_key_value

        if repository.get(key) is not None:
            raise UndoError(
                f"{deleted.table} #{key} cannot be restored: "
                "that ID is now used by another record."
            )

        repository.insert(deleted.row, commit=True)
        self._last = None

        cover_restored: bool | None = None

        if deleted.cover is not None:
            try:
                self._artwork.write_raw(key, deleted.cover)
                cover_restored = True
            except ArtworkError as exc:
                logger.warning(
                    "Restored %s #%s but not its cover: %s",
                    deleted.table,
                    key,
                    exc,
                )
                cover_restored = False

        return RestoreResult(deleted, cover_restored)
