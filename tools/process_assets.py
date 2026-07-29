from __future__ import annotations

import csv
import shutil
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "Archive.zip"
WORK = ROOT / ".asset-work"
MAX_DIMENSION = 128
WEBP_QUALITY = 58

ASSET_MAP = {
    "ChatGPT Image Jul 29, 2026, 11_15_42 AM (1).png": "assets/smudges/smudge-01-hyper-pounce.webp",
    "ChatGPT Image Jul 29, 2026, 11_15_42 AM (2).png": "assets/smudges/smudge-02-speed-walk.webp",
    "ChatGPT Image Jul 29, 2026, 11_15_43 AM (10).png": "assets/smudges/smudge-03-startled-dance.webp",
    "ChatGPT Image Jul 29, 2026, 11_15_43 AM (3).png": "assets/smudges/smudge-04-tall-sit.webp",
    "ChatGPT Image Jul 29, 2026, 11_15_43 AM (4).png": "assets/smudges/smudge-05-puffed-stand.webp",
    "ChatGPT Image Jul 29, 2026, 11_15_43 AM (5).png": "assets/smudges/smudge-06-wide-eyed-sit.webp",
    "ChatGPT Image Jul 29, 2026, 11_15_43 AM (6).png": "assets/smudges/smudge-07-low-stalk.webp",
    "ChatGPT Image Jul 29, 2026, 11_15_43 AM (7).png": "assets/smudges/smudge-08-goblin-claw.webp",
    "ChatGPT Image Jul 29, 2026, 11_15_43 AM (8).png": "assets/smudges/smudge-09-vertical-grab.webp",
    "ChatGPT Image Jul 29, 2026, 11_15_43 AM (9).png": "assets/smudges/smudge-10-full-sprint.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (1).png": "assets/smudges/smudge-11-whirlwind.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (10).png": "assets/smudges/smudge-12-upside-down-flail.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (2).png": "assets/smudges/smudge-13-low-pounce.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (3).png": "assets/smudges/smudge-14-boxing-stance.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (4).png": "assets/smudges/smudge-15-grumpy-loaf.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (5).png": "assets/smudges/smudge-16-sideways-startle.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (6).png": "assets/smudges/smudge-17-puffball-crouch.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (7).png": "assets/smudges/smudge-18-belly-roll.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (8).png": "assets/smudges/smudge-19-alert-stand.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_07 AM (9).png": "assets/smudges/smudge-20-long-stretch.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_29 AM (1).png": "assets/smudges/smudge-21-tornado-spin.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_29 AM (2).png": "assets/smudges/smudge-22-slide-pounce.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_30 AM (10).png": "assets/smudges/smudge-23-upside-down-drop.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_30 AM (3).png": "assets/smudges/smudge-24-meerkat-stand.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_30 AM (4).png": "assets/smudges/smudge-25-judgment-loaf.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_30 AM (5).png": "assets/smudges/smudge-26-arched-side-eye.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_30 AM (6).png": "assets/smudges/smudge-27-sneak-crawl.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_30 AM (7).png": "assets/smudges/smudge-28-chaos-roll.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_30 AM (8).png": "assets/smudges/smudge-29-bristled-stand.webp",
    "ChatGPT Image Jul 29, 2026, 11_16_30 AM (9).png": "assets/smudges/smudge-30-downward-stretch.webp",
    "ChatGPT Image Jul 29, 2026, 11_17_06 AM.png": "assets/dexter/dexter-unimpressed.webp",
}


def prepare_image(source: Path, destination: Path) -> tuple[int, int, int]:
    with Image.open(source) as opened:
        image = opened.convert("RGBA")

    alpha = image.getchannel("A")
    bounding_box = alpha.getbbox()
    if bounding_box is None:
        raise ValueError(f"Image is completely transparent: {source.name}")

    image = image.crop(bounding_box)
    padding = max(4, round(max(image.size) * 0.02))
    canvas = Image.new(
        "RGBA",
        (image.width + 2 * padding, image.height + 2 * padding),
        (0, 0, 0, 0),
    )
    canvas.alpha_composite(image, (padding, padding))
    image = canvas

    if max(image.size) > MAX_DIMENSION:
        scale = MAX_DIMENSION / max(image.size)
        image = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.LANCZOS,
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(
        destination,
        "WEBP",
        quality=WEBP_QUALITY,
        method=6,
        exact=True,
    )
    return image.width, image.height, destination.stat().st_size


def main() -> None:
    if not ARCHIVE.exists():
        raise FileNotFoundError(f"Upload {ARCHIVE.name} to the repository root first.")

    shutil.rmtree(WORK, ignore_errors=True)
    WORK.mkdir(parents=True)

    try:
        with ZipFile(ARCHIVE) as archive:
            archive.extractall(WORK)

        source_by_name = {
            path.name: path
            for path in WORK.rglob("*.png")
            if "__MACOSX" not in path.parts and not path.name.startswith("._")
        }

        missing = sorted(set(ASSET_MAP) - set(source_by_name))
        unexpected = sorted(set(source_by_name) - set(ASSET_MAP))
        if missing or unexpected:
            raise RuntimeError(
                "Archive contents did not match the reviewed image set. "
                f"Missing: {missing or 'none'}; unexpected: {unexpected or 'none'}"
            )

        rows: list[tuple[str, str, int, int, int]] = []
        for original_name, relative_destination in ASSET_MAP.items():
            destination = ROOT / relative_destination
            width, height, size = prepare_image(source_by_name[original_name], destination)
            rows.append((original_name, relative_destination, width, height, size))

        with (ROOT / "ASSET_MANIFEST.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["original_filename", "new_path", "width", "height", "bytes"])
            writer.writerows(rows)

        smudges = sum(path.startswith("assets/smudges/") for path in ASSET_MAP.values())
        dexters = sum(path.startswith("assets/dexter/") for path in ASSET_MAP.values())
        if smudges != 30 or dexters != 1:
            raise AssertionError(f"Expected 30 Smudges and 1 Dexter, got {smudges} and {dexters}.")

        print(f"Created {smudges} Smudge assets and {dexters} Dexter asset.")
        print("Dexter destination: assets/dexter/dexter-unimpressed.webp")
    finally:
        shutil.rmtree(WORK, ignore_errors=True)


if __name__ == "__main__":
    main()
