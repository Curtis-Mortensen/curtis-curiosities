# Scrape Ventures

Extracts venture names from an Airtable `listRowsMatchingNameAndFilters` JSON export into `ventures.csv`.

```bash
python extract_ventures.py
```

## STS2 card tier list (Mobalytics)

Offline tier-list viewer. Full plan: `recreating-tier-list.html`.

### Open the viewer

Open `tier-list/index.html` directly in a browser — no HTTP server needed. Images load from `tier-list/assets/`.

### Refresh when Mobalytics updates rankings

```bash
pip install -r requirements.txt   # first time only
python3 tier-list/scrape/refresh-tier-list.py
```

Offline re-parse from a saved GraphQL response (no network):

```bash
python3 tier-list/scrape/refresh-tier-list.py --raw
```

See tier changes after a refresh:

```bash
python3 tier-list/scrape/diff-tier-lists.py
```

### What to edit by hand

| File | Why |
|------|-----|
| `tier-list/data/methodology.json` | S–D tier definitions and intro copy. **Not scraped** — update manually when Mobalytics changes their methodology text. |
| `tier-list/viewer.js` | Viewer behavior (search, nav, tooltips). |
| `tier-list/viewer.css` | Viewer styling. |
| `tier-list/index.html` (shell only) | Page structure **outside** the `<!-- tier-data:start -->` … `<!-- tier-data:end -->` markers (title, header, footer). Re-run `build-viewer.py` after editing so markers stay intact. |

### Do not edit by hand — regenerate instead

These files are **outputs of the scrape pipeline**. Edit the source (methodology, viewer JS/CSS) or re-run refresh; do not hand-tweak generated data.

| File | Regenerate with |
|------|-----------------|
| Baked JSON inside `tier-list/index.html` (between tier-data markers) | `refresh-tier-list.py` or `build-viewer.py` |
| `tier-list/data/tier-lists.json` | `fetch-tier-lists.py` (or full `refresh-tier-list.py`) |
| `tier-list/data/card-metadata.json` | `fetch-card-metadata.py` |
| `tier-list/assets/manifest.json` | `download-images.py` |
| `tier-list/assets/thumbs/`, `tier-list/assets/full/` | `download-images.py` |
| `STS2/tier-lists-raw.json` | `fetch-tier-lists.py` (live fetch) |

**Rule of thumb:** rankings, images, metadata, and the inline `window.TIER_DATA` block are always regenerated. Only `methodology.json` and the viewer source files (`viewer.js`, `viewer.css`, HTML shell) are meant for human edits.

Generated backups (safe to delete locally): `tier-list/data/tier-lists.previous.json`, `tier-list/data/snapshots/*.json`.

### Pipeline outputs (reference)

- `tier-list/data/tier-lists.json` — 403 cards across 5 characters (Mobalytics rankings)
- `tier-list/data/methodology.json` — S–D tier definitions (**manual**)
- `tier-list/data/card-metadata.json` — cost, type, rarity, description (Spire Codex)
- `STS2/tier-lists-raw.json` — saved Mobalytics GraphQL response
- `tier-list/assets/manifest.json` — local thumb/full paths for the viewer
- `tier-list/index.html` — offline viewer (shell + baked data)
