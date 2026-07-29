from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "jellyfin-smudged.css"
README_PATH = ROOT / "README.md"
SMUDGE_DIR = ROOT / "assets" / "smudges"
DEXTER_PATH = ROOT / "assets" / "dexter" / "dexter-unimpressed.webp"
SPRITE_PATH = ROOT / "assets" / "poster-lottery.webp"

CELL = 160
DEXTER_SLOT = 37


def fit_into_cell(path: Path, max_size: int) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    x = (CELL - image.width) // 2
    y = (CELL - image.height) // 2
    cell.alpha_composite(image, (x, y))
    return cell


def build_sprite() -> None:
    smudges = sorted(SMUDGE_DIR.glob("*.webp"))
    if len(smudges) != 30:
        raise RuntimeError(f"Expected 30 Smudges, found {len(smudges)}")
    if not DEXTER_PATH.is_file():
        raise RuntimeError("Dexter asset is missing")

    frames = [smudges[i % len(smudges)] for i in range(49)]
    frames.insert(DEXTER_SLOT, DEXTER_PATH)

    sprite = Image.new("RGBA", (CELL * 50, CELL), (0, 0, 0, 0))
    for index, path in enumerate(frames):
        max_size = 96 if path == DEXTER_PATH else 146
        sprite.alpha_composite(fit_into_cell(path, max_size), (index * CELL, 0))

    sprite.save(SPRITE_PATH, "WEBP", lossless=True, method=6)


POSTER_SECTION = r'''/* Poster Smudging: a CSS-only 50-slot character lottery.
   The lottery runs invisibly and pauses whenever a poster is revealed.
   The sprite contains 49 Smudge slots and one smaller Dexter slot. */
.card,
.cardBox,
.cardScalable,
.itemsContainer,
.vertical-wrap {
  overflow: visible !important;
}

.card {
  position: relative !important;
  --smudge-lottery-offset: 0s;
}

.card::after {
  content: "" !important;
  position: absolute !important;
  right: -24px !important;
  left: auto !important;
  bottom: 12px !important;
  width: var(--smudge-hover-size) !important;
  height: var(--smudge-hover-size) !important;
  z-index: 10;
  opacity: 0;
  pointer-events: none !important;
  background-image: url("https://cdn.jsdelivr.net/gh/westkitty/get_smudged@main/assets/poster-lottery.webp") !important;
  background-repeat: no-repeat !important;
  background-size: 5000% 100% !important;
  background-position: 0 center;
  filter: drop-shadow(0 8px 12px rgba(0,0,0,.25));
  transform: rotate(-5deg);
  transition: opacity 120ms ease-out, transform 120ms ease-out;
  animation: smudgePosterLottery var(--smudge-lottery-duration, 150s) steps(49, end) infinite !important;
  animation-delay: var(--smudge-lottery-offset) !important;
  animation-play-state: running !important;
}

.card:is(:hover, :focus-within, :focus-visible) {
  z-index: 12 !important;
}

.card:is(:hover, :focus-within, :focus-visible)::after {
  opacity: var(--smudge-hover-opacity) !important;
  animation-play-state: paused !important;
}

.card:nth-child(2n) { --smudge-lottery-offset: -17s; }
.card:nth-child(3n) { --smudge-lottery-offset: -41s; }
.card:nth-child(4n) { --smudge-lottery-offset: -68s; }
.card:nth-child(5n) { --smudge-lottery-offset: -93s; }
.card:nth-child(6n) { --smudge-lottery-offset: -119s; }
.card:nth-child(7n) { --smudge-lottery-offset: -137s; }

.card:nth-child(2n)::after {
  left: -20px !important;
  right: auto !important;
  transform: rotate(4deg);
}

.card:nth-child(3n)::after {
  bottom: 18px !important;
  width: 108px !important;
  height: 108px !important;
}

.card:nth-child(5n)::after {
  bottom: 6px !important;
  width: 128px !important;
  height: 128px !important;
  transform: rotate(-7deg);
}

@keyframes smudgePosterLottery {
  from { background-position: 0 center; }
  to   { background-position: 100% center; }
}

'''

COMPATIBILITY_OVERRIDES = r'''
/* CSS-lottery compatibility overrides. */
html[data-migraine-mode="true"] .card::after,
html.migraine-mode .card::after {
  opacity: 0 !important;
  animation-play-state: paused !important;
}

html[data-migraine-mode="true"] .card:is(:hover, :focus-within, :focus-visible)::after,
html.migraine-mode .card:is(:hover, :focus-within, :focus-visible)::after {
  opacity: .42 !important;
}

@media (prefers-reduced-motion: reduce) {
  .card::after {
    animation-play-state: paused !important;
  }
}
'''


def patch_css() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    start_marker = "/* Poster Smudging. */"
    end_marker = "/* Calm everything down in Migraine Mode. */"

    if start_marker in css:
        before, remainder = css.split(start_marker, 1)
        _, after = remainder.split(end_marker, 1)
        css = before + POSTER_SECTION + end_marker + after
    elif "/* Poster Smudging: a CSS-only 50-slot character lottery." not in css:
        raise RuntimeError("Could not locate the poster-smudging section")

    if "/* CSS-lottery compatibility overrides. */" not in css:
        css = css.rstrip() + "\n" + COMPATIBILITY_OVERRIDES

    if css.count("{") != css.count("}"):
        raise RuntimeError("CSS braces are unbalanced")

    ambient = css.split("/* Poster Smudging", 1)[0]
    if "dexter" in ambient.lower():
        raise RuntimeError("Dexter was found in a background section")

    if css.count("assets/poster-lottery.webp") != 1:
        raise RuntimeError("Poster sprite must be referenced exactly once")

    CSS_PATH.write_text(css, encoding="utf-8")


def patch_readme() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    text = text.replace(
        "- **Poster Smudging** — a Smudge appears when a poster is hovered or keyboard-focused",
        "- **Poster Smudging** — a CSS-only lottery picks a different character behind posters without a browser add-on",
    )
    text = text.replace(
        "- **Rare Dexter cameo** — Dexter appears only on occasional poster hover; he is never used in the background",
        "- **Rare Dexter cameo** — Dexter occupies one of 50 poster-lottery slots and is never used in the background",
    )
    text = text.replace(
        "- Dexter is referenced only by the rare `nth-child(17n + 5)` hover/focus rule.",
        "- The poster sprite contains 49 Smudge slots and one smaller Dexter slot.",
    )
    README_PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    build_sprite()
    patch_css()
    patch_readme()
    print("Enabled the CSS-only 1-in-50 poster lottery.")
