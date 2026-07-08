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

## 2026-07-08 — STS2 tier list Phase 2 (Stage 2: consolidate card images)

**Plan:** `recreating-tier-list.html` Stage 2

### Goal

Give every ranked card a local thumbnail and full hover image, plus a manifest for the Stage 3 HTML viewer.

### What was built

| Path | Purpose |
|------|---------|
| `tier-list/scrape/download-images.py` | Copy/link thumbs, download full art, emit manifest |
| `tier-list/assets/thumbs/{slug}.avif` | 403 symlinks → `STS2/{slug}_19D0.avif` |
| `tier-list/assets/full/{slug}.webp` | 403 Mobalytics CDN hover images (~189 MB total) |
| `tier-list/assets/manifest.json` | Slug → thumb/full paths for viewer |

### Run

```bash
cd Scrape-Ventures
python3 tier-list/scrape/download-images.py
```

Options: `--copy` (real AVIF copies instead of symlinks), `--thumbs-only`, `--full-only`.

### Decisions / assumptions

- **Thumbs via symlinks:** Default links into existing `STS2/` AVIFs to avoid duplicating ~few MB of icons. Use `--copy` if symlinks are unsupported.
- **Full art source:** Mobalytics CDN only; Spire Codex fallback implemented but unused (0 CDN 404s).
- **Idempotent:** Re-run skips existing thumb links and full webp files.
- **Multiplayer AVIFs:** 21 extra thumbs in `STS2/` correctly left out (not in tier list JSON).

### Bugs / issues

- None. All 403 slugs got thumb + full with zero failures.

### Status

**Stage 2 complete.** Ready for Stage 3 (static HTML viewer).

**2026-07-08 (later):** Updated `recreating-tier-list.html` with Stage 2 findings and Stage 3 prep details.

## 2026-07-08 — STS2 tier list Phase 3 (Stage 3: static HTML viewer)

**Plan:** `recreating-tier-list.html` Stage 3

### Goal

Offline searchable tier-list page: 5 characters, S–D tier rows, hover full-card preview, Ctrl+F card names.

### What was built

| Path | Purpose |
|------|---------|
| `tier-list/index.html` | Page shell: header, search, character nav, main container |
| `tier-list/viewer.css` | Dark theme, tier rows, card grid, hover popover |
| `tier-list/viewer.js` | Fetch JSON + manifest, build DOM, search filter |

### Run

```bash
cd Scrape-Ventures/tier-list
python3 -m http.server 8080
# open http://localhost:8080
```

`file://` blocks `fetch()` — local HTTP server required for Stage 3 MVP.

### Decisions / assumptions

- **Split files:** `index.html` + `viewer.css` + `viewer.js` (not single-file embed) for easier review.
- **Card names:** visually hidden `.card-name` spans in DOM for Ctrl+F and screen readers.
- **Necrobinder TBD:** empty TBD row rendered with "No cards yet" placeholder.
- **Search:** optional filter box hides non-matches and scrolls first hit into view.
- **Images:** manifest paths first; falls back to remote `iconUrl` if a slug is missing locally.

### Verification

- HTTP 200 for `index.html`, JSON, manifest, sample thumb + full art.
- 403 cards across 5 characters; 0 missing manifest paths; 1 empty Necrobinder TBD row.

### Bugs / issues

- None during implementation.

### Status

**Stage 3 complete.** Ready for Stage 4 (parity polish — theme, YouTube embeds, methodology blurb).
