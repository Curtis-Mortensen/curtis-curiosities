# Plan draft — DriveThruCards Playwright deck uploader

Working draft mirrored from `DriveThruCards-Deck-Automator/master-plan.md`.

## Intent

Automate the partner beta “Create US Poker Deck from Image Files Upload” so card art can be uploaded in batches (by shared back, ≤130 cards), converted to CMYK by DTC, and exported as print PDFs.

## Blockers found

- Builder deep links require partner login (confirmed via curl).
- Cloud agent cannot complete a live upload without credentials.

## Delivered in scaffold

- Folder layout + organize-by-back script
- Playwright step stubs
- Headed **Microsoft Edge** + persistent profile (`auth/edge-profile/`)
- Long-job page-shift waits + heartbeats (`src/waits.js`) for ~10 min DTC jobs
- Offline HTML explainer: `docs/plan-explainer.html`
- Research notes in master-plan / dev-log

## Next

1. Local `npm run auth:save` (Edge login)
2. Headed 2-card dry run through auto-correct; lock selectors + busy UI hooks
3. Confirm download vs publish (`--mode make`) waits
4. Multi-batch runner once one batch finishes cleanly
