"""
=========================================================
Music Collection Manager
Artwork Service Tests
=========================================================

Milestone 7A (1/N)

pytest tests for services/artwork_service.py.

Every test works in pytest's tmp_path with images generated on the
spot, so nothing touches the real artwork folder.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

import config
from services.artwork_service import MAX_SIZE, ArtworkError, ArtworkService


@pytest.fixture()
def artwork(tmp_path: Path) -> ArtworkService:
    return ArtworkService(tmp_path / "artwork")


def make_image(
    path: Path,
    size: tuple[int, int] = (300, 200),
    mode: str = "RGB",
    colour: object = (200, 30, 30),
) -> Path:
    Image.new(mode, size, colour).save(path)  # type: ignore[arg-type]
    return path


def open_cover(path: Path) -> tuple[tuple[int, int], str, str | None]:
    with Image.open(path) as image:
        return image.size, image.mode, image.format


# ============================================================
# set_image / get
# ============================================================


def test_a_record_without_a_cover_has_none(artwork: ArtworkService) -> None:
    assert artwork.get(42) is None


def test_set_image_stores_a_jpeg_named_after_the_record(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    source = make_image(tmp_path / "cover.png")

    stored = artwork.set_image(42, source)

    assert stored == artwork.folder / "42.jpg"
    assert artwork.get(42) == stored
    size, mode, image_format = open_cover(stored)
    assert (size, mode, image_format) == ((300, 200), "RGB", "JPEG")
    assert source.exists()  # the original is left alone


def test_the_folder_is_created_when_needed(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    assert not artwork.folder.exists()

    artwork.set_image(1, make_image(tmp_path / "a.png"))

    assert artwork.folder.is_dir()


def test_a_large_image_is_shrunk_keeping_its_proportions(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    source = make_image(tmp_path / "big.png", size=(3000, 1500))

    size, _, _ = open_cover(artwork.set_image(7, source))

    assert size == (MAX_SIZE, MAX_SIZE // 2)


def test_a_small_image_is_not_enlarged(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    source = make_image(tmp_path / "small.png", size=(120, 80))

    size, _, _ = open_cover(artwork.set_image(7, source))

    assert size == (120, 80)


@pytest.mark.parametrize("extension", ["png", "gif", "bmp", "webp", "tiff", "jpg"])
def test_common_image_formats_are_accepted(
    artwork: ArtworkService, tmp_path: Path, extension: str
) -> None:
    source = make_image(tmp_path / f"cover.{extension}")

    _, mode, image_format = open_cover(artwork.set_image(3, source))

    assert (mode, image_format) == ("RGB", "JPEG")


def test_transparency_is_shown_against_white(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    source = make_image(
        tmp_path / "clear.png", size=(10, 10), mode="RGBA", colour=(0, 0, 0, 0)
    )

    stored = artwork.set_image(5, source)

    with Image.open(stored) as image:
        red, green, blue = image.getpixel((5, 5))  # type: ignore[misc]
    assert min(red, green, blue) > 240  # white, not black


def test_a_sideways_photo_is_turned_upright(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    # A phone stores the picture rotated and records the turn needed in
    # the EXIF "orientation" tag (6 = rotate 90 degrees clockwise).
    source = tmp_path / "phone.jpg"
    exif = Image.Exif()
    exif[0x0112] = 6
    Image.new("RGB", (300, 200), (10, 120, 10)).save(source, exif=exif)

    size, _, _ = open_cover(artwork.set_image(9, source))

    assert size == (200, 300)


def test_setting_a_new_image_replaces_the_old_one(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    artwork.set_image(11, make_image(tmp_path / "one.png", size=(100, 100)))
    artwork.set_image(11, make_image(tmp_path / "two.png", size=(60, 40)))

    size, _, _ = open_cover(artwork.path_for(11))
    assert size == (60, 40)
    assert [p.name for p in artwork.folder.iterdir()] == ["11.jpg"]


# ============================================================
# Bad input
# ============================================================


def test_a_file_that_is_not_an_image_is_rejected(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    text = tmp_path / "notes.txt"
    text.write_text("not a picture", encoding="utf-8")

    with pytest.raises(ArtworkError, match="notes.txt"):
        artwork.set_image(1, text)

    assert artwork.get(1) is None


def test_a_missing_file_is_rejected(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    with pytest.raises(ArtworkError, match="File not found"):
        artwork.set_image(1, tmp_path / "nope.png")


def test_a_rejected_image_leaves_the_existing_cover_untouched(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    artwork.set_image(2, make_image(tmp_path / "good.png", size=(50, 50)))
    before = artwork.path_for(2).read_bytes()
    bad = tmp_path / "broken.png"
    bad.write_bytes(b"\x89PNG not really")

    with pytest.raises(ArtworkError):
        artwork.set_image(2, bad)

    assert artwork.path_for(2).read_bytes() == before
    assert [p.name for p in artwork.folder.iterdir()] == ["2.jpg"]


# ============================================================
# remove
# ============================================================


def test_remove_deletes_the_cover_and_says_so(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    artwork.set_image(4, make_image(tmp_path / "a.png"))

    assert artwork.remove(4) is True
    assert artwork.get(4) is None


def test_remove_with_no_cover_returns_false(artwork: ArtworkService) -> None:
    assert artwork.remove(4) is False


def test_remove_only_touches_that_record(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    artwork.set_image(4, make_image(tmp_path / "a.png"))
    artwork.set_image(5, make_image(tmp_path / "b.png"))

    artwork.remove(4)

    assert artwork.get(5) is not None


# ============================================================
# Configuration
# ============================================================


def test_the_default_folder_comes_from_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(config, "ARTWORK_FOLDER", tmp_path / "configured")

    assert ArtworkService().folder == tmp_path / "configured"


# ============================================================
# read / write_raw (used to bring a deleted record's cover back)
# ============================================================


def test_read_returns_none_without_a_cover(artwork: ArtworkService) -> None:
    assert artwork.read(8) is None


def test_read_returns_the_stored_bytes(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    artwork.set_image(8, make_image(tmp_path / "a.png"))

    assert artwork.read(8) == artwork.path_for(8).read_bytes()


def test_write_raw_puts_back_exactly_what_read_returned(
    artwork: ArtworkService, tmp_path: Path
) -> None:
    artwork.set_image(8, make_image(tmp_path / "a.png"))
    saved = artwork.read(8)
    assert saved is not None
    artwork.remove(8)

    artwork.write_raw(8, saved)

    assert artwork.read(8) == saved
    assert [p.name for p in artwork.folder.iterdir()] == ["8.jpg"]


def test_write_raw_failure_is_an_artwork_error(tmp_path: Path) -> None:
    blocker = tmp_path / "artwork"
    blocker.write_text("a file where the folder should be", encoding="utf-8")

    with pytest.raises(ArtworkError):
        ArtworkService(blocker).write_raw(1, b"data")


def test_set_image_failure_to_create_the_folder_is_an_artwork_error(
    tmp_path: Path,
) -> None:
    blocker = tmp_path / "artwork"
    blocker.write_text("a file where the folder should be", encoding="utf-8")
    source = make_image(tmp_path / "a.png")

    with pytest.raises(ArtworkError, match="Cannot save the cover"):
        ArtworkService(blocker).set_image(1, source)
