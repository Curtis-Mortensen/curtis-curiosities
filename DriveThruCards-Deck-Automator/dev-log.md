# Dev log — DriveThruCards Deck Automator

## 2026-07-09 — Edge (headed), long waits, HTML explainer

### Plan summary

User feedback: run in **their Microsoft Edge** (visible, not headless) so they can log in and watch; DTC steps can each take **~10 minutes** (color correct, render sheet, publish); add a plain-language offline HTML doc; explain how Playwright detects page shifts.

### Changes made

- `src/browser.js` / `scripts/auth-save.js` — `chromium.launchPersistentContext` with `channel: 'msedge'`, `headless: false`, profile at `auth/edge-profile/`.
- `src/waits.js` — `waitForPageShift` / URL / selector / busy-clear helpers with 20-minute timeout and 30s heartbeats.
- `src/steps/edit-images.js` + `export-pdf.js` + `src/run-batch.js` — use long waits; support `--mode make|update|download` and `--keep-open`.
- `docs/plan-explainer.html` — self-contained CSS, offline-friendly simple plan + wait explainer.
- Updated README, master-plan, gitignore (`auth/edge-profile/`).

### Coding decisions / assumptions

- Persistent Edge profile is preferred over cookie-only `storageState` so the user sees “their” browser session.
- `longJobTimeoutMs = 20 minutes` based on observed ~10-minute jobs (buffer for slower runs).
- Busy selectors are a best-effort list; will tighten after a live headed run if DTC uses different overlays.
- Assumption: Microsoft Edge is installed on the machine that runs the scripts.

### Bugs / problems

- None new in this pass (no live Edge in the cloud agent environment to exercise `msedge` channel).

### Status

Scaffold updated for Edge + waits + HTML doc. Still needs a local headed dry run to lock upload/assemble selectors.

---

## 2026-07-09 — Research + project scaffold

### Plan summary

Investigate whether the DriveThruCards beta deck image uploader is reachable without login, document the wizard, and create a new repo folder with a card-organization plan (by backs / 130-card batches) plus Playwright skeleton code.

### Site access checks

- Fetched `https://tools.drivethrucards.com/builder/deck/images/back/6a4ff5a3138d6`
  - Response: **302 → `/builder/deck`** when unauthenticated.
  - `/builder/deck` returns 200 HTML titled “Deck Builder” but body is a **login Fancybox** (`show_login_return_popup = true`, posts to `validate_login_credentials.php`). No upload dropzone in the logged-out HTML.
- `https://tools.drivethrucards.com/` redirects toward `site.drivethrucards.com`, which returned **Cloudflare challenge (403)** from this environment.
- Conclusion: **cannot operate the deck editor without a partner login.** Research continued via public JS/CSS + user screenshots + partner help docs.

### Public builder JS (`/builder/js/deck/deck.js`)

Confirmed page classes and flows:

- `.page-deck-index` — list/delete decks
- `.page-deck-images` — uploaded image delete handlers
- `.page-deck-lists` — edit/warnings, sortable order, `deck/cleanup/<deck_id>/<image_id>` auto-fix, Next gated on warnings
- `.page-deck-assemble` — `.checkboxes-backs` / `.checkboxes-fronts`, quantities, `deckMinCards` / `deckMaxCards`, finish
- `.page-deck-export` — purchase/export hooks; assemble `next_step` values: `make`, `update`, `download`

### Upload notes (from user screenshot of step 1)

- Max 5 MB; JPG preferred over PNG; 825×1125; CMYK preferred; 40px safe inset; name `001back.jpg` / `001front.jpg`.

### Partner print specs (help center)

- Interleaved back/front PDF, CMYK ≤240% ink, 1/8" bleed, US Poker final layout 2.75"×3.75", PDF/X-1a:2003.

### Deck size note

- User: tool max **130** cards.
- Partner FAQ discusses physical decks up to ~250 before banding issues. Automation will treat **130 as hard max** until a logged-in session prints the real `deckMaxCards`.

### Coding decisions / assumptions

- New independent folder `DriveThruCards-Deck-Automator/` (do not pull from NanDeck-Scripts or other repos).
- Organize primarily **by shared back file**, then pack to ≤130.
- Auth via Playwright `storageState` after a one-time human login (no passwords in git).
- Skeleton selectors based on public class names; must be verified headed after login.
- Assumption: assemble can reuse one uploaded back with many fronts; if false, organizer will duplicate back files per card.

### Bugs / problems

- WebFetch of the deep builder URL timed out; raw `curl` worked and clarified the login redirect.
- Cloudflare blocks some `site.drivethrucards.com` pages from this agent network.
- No live upload DOM without credentials — upload locator remains best-effort (`input[type=file]` + dropzone text).

### Changes made

- Created branch `cursor/drivethrucards-deck-automator-e9e4`
- Added project folder with README, master-plan, manifest example, organize script, Playwright step stubs, package.json, gitignore
- Updated monorepo README projects table

### Status

Research + scaffold complete. Next human step: run `npm run auth:save` locally with partner credentials, then harden selectors on a 2-card dry run.