# Card folders

## How to organize by backs

1. Put real art under `source/` (gitignored) or any folder you point the manifest at.
2. Edit a `manifest.json` that lists each card’s front, back, and quantity.
3. Run:

```bash
npm run organize -- path/to/manifest.json
```

4. Open `batches/summary.json`. Each `batch-*` folder is ≤ 130 cards and ready for Playwright.

### Grouping rule (default)

Cards that share the same `back` path stay together. When a group would blow past 130, it splits. Different back designs become different batches when that keeps uploads small — or pack everything into one deck with:

```json
"batchStrategy": "single-deck"
```

### Naming inside a batch

The organizer renames copies to DTC’s suggested pattern:

- `backs/001back.jpg`
- `fronts/001front.jpg`

Shared backs are only copied once; `batch.json` points many fronts at that one back file.

### Image checklist (from DTC upload notes)

- JPG preferred (PNG prints look washed out)
- ≤ 5 MB each
- Ideal: 825 × 1125 px
- Keep important art ≥ 40 px inside the trim
- CMYK is ideal; the beta builder converts if needed

## Example

`manifest.example.json` references `_example/` placeholder files so you can run:

```bash
npm run organize:example
```

Replace those placeholders with real art before a live upload.