"""
=========================================================
Music Collection Manager
Artwork Service
=========================================================

Milestone 7A (1/N)

Cover images for Records.

Each cover is one image file in the artwork folder, named after
the record's ID (artwork/1234.jpg). The database is not touched:
there is no column or table for artwork, so adding this feature
changes nothing in Musi.db and nothing in a backup of it.

Whatever image the user picks (PNG, JPEG, GIF, WebP, BMP, TIFF) is
converted to a JPEG no larger than MAX_SIZE pixels on its longest
side, so the folder stays small and every cover has the same
format. Transparent areas become white, and a photo taken sideways
is turned the right way up.

Like core/export.py and core/backup.py this is independent of
DatabaseContext: it only knows about files.
"""

from __future__ import annotations

import contextlib
import os
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

import config

MAX_SIZE = 1000
JPEG_QUALITY = 90


class ArtworkError(Exception):
    """Raised when an image cannot be used as a cover."""


class ArtworkService:
    """Stores, finds and removes the cover image of a record."""

    def __init__(self, folder: Path | None = None) -> None:
        # Read config at construction so a test (or a different
        # configuration) can redirect the folder.
        self.folder = folder if folder is not None else config.ARTWORK_FOLDER

    def path_for(self, record_id: int) -> Path:
        """Where this record's cover is (or would be) stored."""

        return self.folder / f"{record_id}.jpg"

    def get(self, record_id: int) -> Path | None:
        """The cover's path, or None when the record has none."""

        path = self.path_for(record_id)

        return path if path.is_file() else None

    def set_image(self, record_id: int, source: Path) -> Path:
        """
        Make `source` the record's cover, replacing any existing one.

        The new file is written completely before it replaces the
        old one, so a failure never loses the cover already there.
        """

        image = self._load(source)

        destination = self.path_for(record_id)
        temporary = destination.with_name(destination.name + ".tmp")

        try:
            self.folder.mkdir(parents=True, exist_ok=True)
            image.save(temporary, format="JPEG", quality=JPEG_QUALITY)
            os.replace(temporary, destination)
        except OSError as exc:
            with contextlib.suppress(OSError):
                temporary.unlink(missing_ok=True)
            raise ArtworkError(f"Cannot save the cover: {exc}") from exc

        return destination

    def read(self, record_id: int) -> bytes | None:
        """The cover file's exact bytes, or None when there is no cover."""

        path = self.get(record_id)

        if path is None:
            return None

        try:
            return path.read_bytes()
        except OSError as exc:
            raise ArtworkError(f"Cannot read the cover: {exc}") from exc

    def write_raw(self, record_id: int, data: bytes) -> Path:
        """
        Put back exactly the bytes read() returned, without converting
        them again. Used to bring a deleted record's cover back.
        """

        destination = self.path_for(record_id)
        temporary = destination.with_name(destination.name + ".tmp")

        try:
            self.folder.mkdir(parents=True, exist_ok=True)
            temporary.write_bytes(data)
            os.replace(temporary, destination)
        except OSError as exc:
            with contextlib.suppress(OSError):
                temporary.unlink(missing_ok=True)
            raise ArtworkError(f"Cannot save the cover: {exc}") from exc

        return destination

    def remove(self, record_id: int) -> bool:
        """Delete the record's cover. True if there was one."""

        path = self.path_for(record_id)

        if not path.is_file():
            return False

        path.unlink()

        return True

    @staticmethod
    def _load(source: Path) -> Image.Image:
        try:
            with Image.open(source) as opened:
                opened.load()
                image = ImageOps.exif_transpose(opened)
                image = ArtworkService._flatten(image)
        except FileNotFoundError as exc:
            raise ArtworkError(f"File not found: {source.name}") from exc
        except (
            UnidentifiedImageError,
            Image.DecompressionBombError,
            OSError,
            ValueError,
        ) as exc:
            raise ArtworkError(
                f"{source.name} is not an image that can be read."
            ) from exc

        image.thumbnail((MAX_SIZE, MAX_SIZE))

        return image

    @staticmethod
    def _flatten(image: Image.Image) -> Image.Image:
        """RGB copy, with any transparency shown against white."""

        has_alpha = image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        )

        if not has_alpha:
            return image.convert("RGB")

        rgba = image.convert("RGBA")
        background = Image.new("RGB", rgba.size, (255, 255, 255))
        background.paste(rgba, mask=rgba.getchannel("A"))

        return background
