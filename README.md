# Get Smudged

A lightweight set of transparent WebP assets and optional Jellyfin CSS for:

- **Ambient Smudging** — static Smudges hidden around the interface
- **Poster Smudging** — a Smudge appears when a poster is hovered or keyboard-focused
- **Smudge Migration** — a single background layer moves the group very slowly
- **Rare Dexter cameo** — Dexter appears only on occasional poster hover; he is never used in the background

## Files

- `assets/smudges/` — 30 individually named Smudge poses
- `assets/dexter/dexter-unimpressed.webp` — the one Dexter easter egg
- `jellyfin-smudged.css` — paste after your existing Jellyfin Custom CSS
- `ASSET_MANIFEST.csv` — original filename to new optimized asset mapping

The original 1024–1536 px PNG files totaled about 53 MB. These WebP assets were trimmed, resized to a maximum dimension of 512 px, and optimized to about 1.6 MB total while retaining transparency.

## Install in Jellyfin

1. Open **Dashboard → Branding → Custom CSS**.
2. Keep your current theme CSS.
3. Append the contents of `jellyfin-smudged.css` after it.
4. Save and hard-refresh the Jellyfin page.

All asset URLs use jsDelivr against the public `main` branch:

```text
https://cdn.jsdelivr.net/gh/westkitty/get_smudged@main/...
```

## Behavior and safety

- Decorative images use `pointer-events: none`.
- Dexter is referenced only by the rare `nth-child(17n + 5)` hover/focus rule.
- `prefers-reduced-motion` disables migration.
- Migraine Mode disables movement and lowers the Smudges' prominence.
