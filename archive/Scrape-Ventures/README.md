# Scrape Ventures

This folder contains the Airtable export and small script that turns its venture rows into a CSV. The Slay the Spire 2 tier-list project now lives separately in [`../../STS2-Tier-List/`](../../STS2-Tier-List/).

## Extract venture names

Run from this folder:

```bash
python3 extract_ventures.py
```

The script reads `listRowsMatchingNameAndFilters` and writes `ventures.csv`. You can pass different input and output paths:

```bash
python3 extract_ventures.py path/to/input.json path/to/output.csv
```
