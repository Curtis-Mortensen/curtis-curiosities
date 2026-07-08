# Scrape Ventures

Extracts venture names from an Airtable `listRowsMatchingNameAndFilters` JSON export into `ventures.csv`.

```bash
python extract_ventures.py
```

## STS2 card tier list (Mobalytics)

Stage 1 scraper for the offline tier-list viewer (see `recreating-tier-list.html`):

```bash
pip install -r requirements.txt
python tier-list/scrape/fetch-tier-lists.py
```

Output: `tier-list/data/tier-lists.json` (403 cards across 5 characters). Raw GraphQL response saved to `STS2/tier-lists-raw.json`.
