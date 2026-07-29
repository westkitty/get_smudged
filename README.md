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
- `tools/process_assets.py` — deterministic rename/optimization script

The original 1024–1536 px PNG files total about 53 MB. The processor trims transparent margins, retains transparency, resizes each asset to a maximum dimension of 128 px, and converts the complete set to roughly 140 KB of WebP files—appropriate for the 72–130 px sizes used by the Jellyfin CSS.

## Finish the asset import

On the `smudge-assets` branch, upload the original file as `Archive.zip` at the repository root. The `Process Smudge archive` GitHub Action will:

1. verify the exact reviewed set of 30 Smudges and one Dexter;
2. assign the descriptive filenames;
3. crop, resize, and convert the images to transparent WebP;
4. put Dexter only in `assets/dexter/`;
5. generate `ASSET_MANIFEST.csv`;
6. delete the source archive; and
7. commit the finished assets back to the branch.

## Install in Jellyfin

1. Merge the `smudge-assets` branch into `main` after the assets are generated.
2. Open **Dashboard → Branding → Custom CSS**.
3. Keep the current theme CSS.
4. Append the contents of `jellyfin-smudged.css` after it.
5. Save and hard-refresh the Jellyfin page.

All asset URLs use jsDelivr against the public `main` branch:

```text
https://cdn.jsdelivr.net/gh/westkitty/get_smudged@main/...
```

## Behavior and safety

- Decorative images use `pointer-events: none`.
- Dexter is referenced only by the rare `nth-child(17n + 5)` hover/focus rule.
- Dexter is absent from both ambient background-image lists.
- `prefers-reduced-motion` disables migration.
- Migraine Mode disables movement and lowers the Smudges' prominence.
