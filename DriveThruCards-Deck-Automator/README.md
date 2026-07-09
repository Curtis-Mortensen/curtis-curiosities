# DriveThruCards Deck Automator

Playwright helper for DriveThruCards' partner **US Poker Deck from Image Files Upload (Beta)** tool.

Goal: batch-upload card backs + fronts, let DTC convert to CMYK / assemble a print PDF, and stay under the builder's **130-card** deck cap by organizing work into back-design batches.

## What we learned (site access)

| Check | Result |
|---|---|
| `https://tools.drivethrucards.com/builder/deck/images/back/<id>` | **Requires login.** Unauthenticated requests 302 → `/builder/deck`, which only shows a login popup. |
| Builder JS (`/builder/js/deck/deck.js`) | Public. Confirms steps: images → lists/edit → assemble → export. Assemble UI pairs `.checkboxes-backs` with `.checkboxes-fronts` and enforces `deckMinCards` / `deckMaxCards`. |
| Image upload notes (from the live UI) | JPG preferred, max **5 MB**, recommended **825×1125**, keep important art **≥40px** inside trim, name like `001back.jpg` / `001front.jpg`. |
| Partner print specs | Final PDF is still back/front interleaved, CMYK, bleed 1/8", PDF/X-1a:2003. The beta builder is meant to produce that for you. |

You cannot drive a real deck session from this cloud environment without partner credentials. Locally: log in once (or store a storage state), then run the scripts.

## Quick start (local)

```bash
cd DriveThruCards-Deck-Automator
npm install
npx playwright install chromium

# 1) Put art under cards/ (see cards/README.md)
# 2) Build batch folders from a manifest
node src/organize-batches.js cards/manifest.example.json

# 3) Save a logged-in browser session (opens a window; you log in)
npm run auth:save

# 4) Dry-run one batch against the builder (headed, slow)
npm run upload:batch -- --batch cards/batches/batch-01-shared-back
```

Credentials stay in `auth/storage-state.json` (gitignored). Never commit them.

## Layout

```
DriveThruCards-Deck-Automator/
  cards/                 # your art + manifests + generated batches
  src/                   # organize + Playwright steps
  scripts/               # npm entrypoints
  auth/                  # local login state (gitignored)
  master-plan.md         # approved research + implementation plan
  dev-log.md             # what we tried and decided
```

## Status

Research + folder layout + skeleton code. Upload selectors still need a logged-in pass to harden against the live DOM.