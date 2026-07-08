# Scrape Ventures

Extracts venture names from an Airtable `listRowsMatchingNameAndFilters` JSON export into `ventures.csv`.

```bash
python extract_ventures.py
```

## STS2 card tier list (Mobalytics)

Offline tier-list viewer pipeline (see `recreating-tier-list.html`):

```bash
pip install -r requirements.txt
python3 tier-list/scrape/fetch-tier-lists.py   # Stage 1: rankings JSON
python3 tier-list/scrape/download-images.py    # Stage 2: thumbs + full art
python3 tier-list/scrape/fetch-card-metadata.py # Spire Codex cost/type/rarity
python3 tier-list/scrape/build-viewer.py       # Bake JSON into index.html
```

Open `tier-list/index.html` directly in a browser — no HTTP server needed. Images load from `tier-list/assets/`.

Refresh workflow (re-run all four after Mobalytics updates):

```bash
python3 tier-list/scrape/fetch-tier-lists.py
python3 tier-list/scrape/download-images.py
python3 tier-list/scrape/fetch-card-metadata.py
python3 tier-list/scrape/build-viewer.py
```

Outputs:
- `tier-list/data/tier-lists.json` — 403 cards across 5 characters
- `tier-list/data/methodology.json` — S–D tier definitions (Mobalytics copy)
- `tier-list/data/card-metadata.json` — cost, type, rarity, description (Spire Codex)
- `STS2/tier-lists-raw.json` — saved Mobalytics GraphQL response
- `tier-list/assets/manifest.json` — local thumb/full paths for the viewer
- `tier-list/index.html` — offline viewer with baked data (open via `file://`)
