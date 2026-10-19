# Scrape Ventures

Extracts venture names from an Airtable `listRowsMatchingNameAndFilters` JSON export into `ventures.csv`.

```bash
python extract_ventures.py
```

## STS2 card tier list (Mobalytics)

Local tier-list viewer (Mobalytics rankings + Spire Codex tooltips). Full plan: `recreating-tier-list.html`.

### Open the viewer

From the `Scrape-Ventures` folder:

```bash
cd tier-list && python3 -m http.server 8080
```

Then open http://localhost:8080 in your browser.

The viewer loads JSON with `fetch()`. Browsers block that on `file://`, so double-clicking `index.html` will not work — use the local server above.

### Refresh when Mobalytics updates rankings

Re-fetches rankings, images, and card metadata. Does **not** rewrite `index.html` — the viewer always reads live JSON from `data/` and `assets/`.

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
| `tier-list/index.html` | Page shell (title, header, footer). |

### Do not edit by hand — regenerate instead

These files are **outputs of the scrape pipeline**. Edit the source (methodology, viewer JS/CSS) or re-run refresh; do not hand-tweak generated data.

| File | Regenerate with |
|------|-----------------|
| `tier-list/data/tier-lists.json` | `fetch-tier-lists.py` (or full `refresh-tier-list.py`) |
| `tier-list/data/card-metadata.json` | `fetch-card-metadata.py` |
| `tier-list/assets/manifest.json` | `download-images.py` |
| `tier-list/assets/thumbs/`, `tier-list/assets/full/` | `download-images.py` |
| `STS2/tier-lists-raw.json` | `fetch-tier-lists.py` (live fetch) |

**Rule of thumb:** rankings, images, and metadata are always regenerated. Only `methodology.json` and the viewer source files (`viewer.js`, `viewer.css`, `index.html`) are meant for human edits.

Generated backups (safe to delete locally): `tier-list/data/tier-lists.previous.json`, `tier-list/data/snapshots/*.json`.

### Pipeline outputs (reference)

- `tier-list/data/tier-lists.json` — 403 cards across 5 characters (Mobalytics rankings)
- `tier-list/data/methodology.json` — S–D tier definitions (**manual**)
- `tier-list/data/card-metadata.json` — cost, type, rarity, description (Spire Codex)
- `STS2/tier-lists-raw.json` — saved Mobalytics GraphQL response
- `tier-list/assets/manifest.json` — local thumb/full paths for the viewer
- `tier-list/index.html` — viewer shell (`viewer.js` + `viewer.css`; serve over HTTP)
