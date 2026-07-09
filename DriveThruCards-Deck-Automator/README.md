# DriveThruCards Deck Automator

Playwright helper for DriveThruCards' partner **US Poker Deck from Image Files Upload (Beta)** tool.

Goal: batch-upload card backs + fronts, let DTC convert to CMYK / assemble a print PDF, and stay under the builder's **130-card** deck cap by organizing work into back-design batches.

**Start here (simple, offline):** open [`docs/plan-explainer.html`](docs/plan-explainer.html) in any browser — CSS is inlined. Technical detail lives in [`master-plan.md`](master-plan.md).

## What we learned (site access)

| Check | Result |
|---|---|
| `https://tools.drivethrucards.com/builder/deck/images/back/<id>` | **Requires login.** Unauthenticated requests 302 → `/builder/deck`, which only shows a login popup. |
| Builder JS (`/builder/js/deck/deck.js`) | Public. Confirms steps: images → lists/edit → assemble → export. Assemble UI pairs `.checkboxes-backs` with `.checkboxes-fronts` and enforces `deckMinCards` / `deckMaxCards`. |
| Image upload notes (from the live UI) | JPG preferred, max **5 MB**, recommended **825×1125**, keep important art **≥40px** inside trim, name like `001back.jpg` / `001front.jpg`. |
| Partner print specs | Final PDF is still back/front interleaved, CMYK, bleed 1/8", PDF/X-1a:2003. The beta builder is meant to produce that for you. |
| Real wait times (user testing) | Auto-correct colors ~10 min; render sheet ~10 min; publish ~10 min. Scripts wait on **page shifts**, not fixed sleeps (see `src/waits.js`). |

## Browser: Microsoft Edge (headed — you watch)

Runs against **your installed Edge** in a normal window (`channel: 'msedge'`), with a persistent profile under `auth/edge-profile/` so you can log in once and observe every step. Not headless.

## Quick start (local)

```bash
cd DriveThruCards-Deck-Automator
npm install

# 1) Put art under cards/ (see cards/README.md)
# 2) Build batch folders from a manifest
node src/organize-batches.js cards/manifest.example.json

# 3) Open Edge, log into DriveThru, press Enter in the terminal
npm run auth:save

# 4) Dry-run one batch (watch Edge; long jobs print heartbeats)
npm run upload:batch -- --batch cards/batches/batch-01-shared-red --start-url "https://tools.drivethrucards.com/builder/deck/images/back/YOUR_ID"

# Publish instead of PDF download:
# npm run upload:batch -- --batch ... --mode make --keep-open
```

Login stays in `auth/edge-profile/` (gitignored). Never commit it.

## Layout

```
DriveThruCards-Deck-Automator/
  docs/plan-explainer.html   # simple offline HTML guide (self-contained CSS)
  cards/                     # your art + manifests + generated batches
  src/                       # organize + Playwright steps + waits.js
  scripts/                   # npm entrypoints (Edge login)
  auth/                      # local Edge profile (gitignored)
  master-plan.md             # technical plan
  dev-log.md                 # what we tried and decided
```

## Status

Research + folder layout + skeleton code. Edge + long-wait helpers are in place. Upload/assemble selectors still need a logged-in headed pass to harden against the live DOM.