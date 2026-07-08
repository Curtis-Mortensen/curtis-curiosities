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
cd Scrape-Ventures
python3 tier-list/scrape/build-viewer.py
# open tier-list/index.html in a browser
```

Previously required `python3 -m http.server` before bake step was added.

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

**Stage 3 complete.** Ready for Stage 4 (character navigation polish only — no embeds or external links).

## 2026-07-08 — STS2 tier list bake step (file:// offline)

**Plan:** `recreating-tier-list.html` Stage 3 extension / Stage 5 prep

### Goal

Open `tier-list/index.html` directly without running a local HTTP server.

### What was built

| Path | Purpose |
|------|---------|
| `tier-list/scrape/build-viewer.py` | Inlines `tier-lists.json` + `manifest.json` into `index.html` as `window.TIER_DATA` |
| `tier-list/viewer.js` | Prefers baked data; `fetch()` fallback for dev without re-bake |
| `tier-list/index.html` | Re-baked with ~171 KB inline JSON (403 cards) |

### Run

```bash
cd Scrape-Ventures
python3 tier-list/scrape/build-viewer.py
# open tier-list/index.html in a browser
```

Full refresh: `fetch-tier-lists.py` → `download-images.py` → `build-viewer.py`.

### Decisions / assumptions

- **Bake into same `index.html`:** marker comments (`tier-data:start` / `tier-data:end`) let the script re-inject on refresh.
- **Images stay external:** only JSON is inlined; `assets/thumbs/` and `assets/full/` remain separate (~189 MB).
- **No server for normal use:** `fetch()` blocked on `file://` is resolved by inline script; relative image paths still work on `file://`.

### Verification

- `build-viewer.py` reports 403 cards baked; `index.html` contains `window.TIER_DATA` with `crash-landing`.

### Status

**Bake step complete.** Viewer is self-contained for data; ship `tier-list/` folder for offline use.

## 2026-07-08 — STS2 tier list methodology + metadata tooltips

**Plan:** Stage 3 extension

### Goal

Add Mobalytics-style tier methodology at page top and Spire Codex card metadata in hover tooltips.

### What was built

| Path | Purpose |
|------|---------|
| `tier-list/data/methodology.json` | S–D tier definitions + intro/disclaimer copy |
| `tier-list/scrape/fetch-card-metadata.py` | Bulk fetch from Spire Codex → `card-metadata.json` |
| `tier-list/data/card-metadata.json` | 401/403 cards: cost, type, rarity, description, keywords |
| `viewer.js` / `viewer.css` | Methodology panel, enriched hover tooltip, nav link |
| `build-viewer.py` | Now bakes methodology + metadata into `index.html` |

### Run

```bash
python3 tier-list/scrape/fetch-card-metadata.py
python3 tier-list/scrape/build-viewer.py
```

### Decisions / assumptions

- **Tiers from Mobalytics only;** Spire Codex used for metadata, not rankings.
- **2 missing Spire Codex slugs:** `follow-through`, `unrelenting-plus` — tooltips show art only.
- **Methodology** is static JSON (edited from live Mobalytics page copy), not scraped.

### Status

Shipped in Stage 3. Stage 4 remains character nav polish only.

## 2026-07-08 — STS2 tier list Phase 4 (Stage 4: character navigation polish)

**Plan:** `recreating-tier-list.html` Stage 4

### Goal

Polish sticky character jump navigation: active-section highlight on scroll, smooth hash jumps, keyboard traversal, mobile layout.

### What was built

| Path | Purpose |
|------|---------|
| `tier-list/viewer.js` | Scroll-spy (`setupCharacterNavScrollSpy`), smooth scroll (`setupNavSmoothScroll`), keyboard nav (`setupNavKeyboard`) |
| `tier-list/viewer.css` | `.is-active` pill style, `focus-visible` rings, mobile horizontal-scroll nav, `scroll-behavior: smooth` |

### Run

No new scripts. Open `tier-list/index.html` in a browser (or re-bake if JSON changed).

### Decisions / assumptions

- **Scroll-spy:** IntersectionObserver with header-offset fallback picks the section whose top has passed the sticky header.
- **Reduced motion:** `scroll-behavior: smooth` only when `prefers-reduced-motion: no-preference`.
- **Mobile:** Below 640px, nav pills scroll horizontally instead of wrapping to a tall block.
- **Out of scope:** YouTube embeds, wiki/Mobalytics crosslinks (unchanged from plan).

### Bugs / issues

- None during implementation.

### Status

**Stage 4 complete.** Viewer feature set is done; Stage 5 is the documented refresh pipeline only.

## 2026-07-08 — STS2 tier list Phase 5 (Stage 5: refresh workflow)

**Plan:** `recreating-tier-list.html` Stage 5

### Goal

Single-command refresh when Mobalytics updates rankings, plus tier-change diff between runs.

### What was built

| Path | Purpose |
|------|---------|
| `tier-list/scrape/refresh-tier-list.py` | Orchestrates fetch → images → metadata → bake; backs up JSON; runs diff |
| `tier-list/scrape/diff-tier-lists.py` | Compare two `tier-lists.json` files; report moved/added/removed cards |
| `tier-list/data/snapshots/` | Timestamped backups (gitignored JSON; `.gitkeep` in repo) |
| `tier-list/.gitignore` | Ignores `tier-lists.previous.json` and snapshot JSON files |

### Run

```bash
cd Scrape-Ventures
python3 tier-list/scrape/refresh-tier-list.py          # live Mobalytics fetch
python3 tier-list/scrape/refresh-tier-list.py --raw    # offline from STS2/tier-lists-raw.json
python3 tier-list/scrape/diff-tier-lists.py            # manual diff (previous vs current)
```

Flags: `--skip-fetch`, `--skip-images`, `--skip-metadata`, `--skip-bake`, `--no-backup`, `--no-diff`.

### Decisions / assumptions

- **Backup before fetch:** Copies current JSON to `tier-lists.previous.json` and `data/snapshots/tier-lists-{UTC}.json`.
- **Diff exit code 2** when placements changed (0 = identical); refresh treats 2 as success.
- **Methodology still manual** — not scraped; edit `methodology.json` by hand if Mobalytics copy changes.
- **Never hand-edit baked `index.html`** — re-run refresh or `build-viewer.py`.

### Bugs / issues

- None during implementation.

### Status

**Stage 5 complete.** STS2 tier-list project (Stages 1–5) is shippable.

## 2026-07-08 — README: hand-edit vs generated files

Updated `README.md` with tables for what to edit manually (`methodology.json`, viewer source) vs what to regenerate via `refresh-tier-list.py` (tier data, baked `index.html`, images, metadata).

## 2026-07-08 — Revert tier-list bake step (serve over HTTP again)

**User correction:** Viewer should load JSON via `fetch()` over a local HTTP server, not inlined `window.TIER_DATA` for `file://`.

**Reverted from:** commit `a87a77e` bake step (Phase 3 extension).

| File | Change |
|------|--------|
| `tier-list/viewer.js` | Removed `window.TIER_DATA` shortcut; always fetches JSON |
| `tier-list/index.html` | Removed ~240 KB inline bake block; footer shows `python3 -m http.server` |
| `tier-list/scrape/refresh-tier-list.py` | Dropped `build-viewer.py` step and `--skip-bake` flag |
| `README.md` | Open instructions → `cd tier-list && python3 -m http.server 8080` |

**Run viewer:**

```bash
cd tier-list && python3 -m http.server 8080
# open http://localhost:8080
```

`build-viewer.py` left in repo but no longer called by refresh pipeline.

## 2026-07-08 — Tier list viewer UX: right TOC, cursor preview, visible card names

**User request:** Match Mobalytics layout more closely; fix Ctrl+F by putting readable text on the page.

| File | Change |
|------|--------|
| `tier-list/index.html` | Two-column layout: main content + right sidebar ("On this page") |
| `tier-list/viewer.css` | Sticky vertical nav on the right; small `.card-name` labels under thumbs; fixed `.card-preview` panel |
| `tier-list/viewer.js` | Shared preview follows cursor to the right; per-card hover popovers removed |

**Notes:**
- Card names are tiny (0.5rem) on purpose — visible enough for browser find/highlight, not for reading.
- Preview stays to the right of the cursor; viewport padding clamps it inward instead of flipping sides.
- Below 900px width, TOC collapses to a horizontal strip above the tier rows.

## 2026-07-08 — Search scroll restore

Clearing the search box restores the scroll position from before the first keystroke of that search session.
