# Scrape-Ventures dev log

## 2026-07-08 — STS2 tier list Phase 1 (Stage 1: scrape tier list data)

**Plan:** `recreating-tier-list.html` Stage 1

### Goal

Fetch Mobalytics card tier rankings (S/A/B/C/D per character) into normalized JSON for the offline tier-list viewer (Stages 2–3).

### What was built

| Path | Purpose |
|------|---------|
| `tier-list/scrape/fetch-tier-lists.py` | GraphQL fetch + normalize → `tier-list/data/tier-lists.json` |
| `tier-list/scrape/bookmarklet.js` | Browser console fallback when curl fetch is blocked |
| `requirements.txt` | `curl_cffi` for Cloudflare bypass |
| `STS2/tier-lists-raw.json` | Saved Mobalytics GraphQL response |
| `tier-list/data/tier-lists.json` | Normalized output (403 cards × 5 characters) |

### Run

```bash
cd Scrape-Ventures
pip install -r requirements.txt
python tier-list/scrape/fetch-tier-lists.py
```

Re-parse without network:

```bash
python tier-list/scrape/fetch-tier-lists.py --raw
```

### Decisions / assumptions

- **Cloudflare:** Plain `curl` returns 403. `curl_cffi` with Chrome impersonation works from this environment.
- **Character mapping:** Each `NgfDocumentCmWidgetTierListMakerV1` widget `id` matches `tierLists.values[].id`. Character slug parsed from widget title (e.g. "Ironclad Tier List" → `ironclad`).
- **Multiplayer excluded:** Sixth tier list (21 cards) skipped to match Mobalytics editorial scope.
- **Necrobinder TBD row:** Present in API with 0 cards; kept in `tiers.TBD`.
- **Card count:** 403 ranked cards (81 Ironclad, 80 Silent, 82 Regent, 80 Necrobinder, 80 Defect). Plan estimated ~440; 424 total in API includes 21 multiplayer cards not ranked on the public list.

### Bugs / issues

- None during implementation. Live fetch succeeded on first corrected GraphQL schema attempt.

### Status

**Stage 1 complete.** Ready for Stage 2 (consolidate card images).

**2026-07-08 (later):** Updated `recreating-tier-list.html` with Stage 1 findings and Stage 2 prep details.
