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
```

Outputs:
- `tier-list/data/tier-lists.json` — 403 cards across 5 characters
- `STS2/tier-lists-raw.json` — saved Mobalytics GraphQL response
- `tier-list/assets/manifest.json` — local thumb/full paths for the viewer
