# Draft plan — Publish Research-Bot HTML on a public Ruby site (VPS)

**Status:** Decisions locked in `Published-Research/dev-decisions.md` (2026-07-11). This file is historical draft context; where it conflicts, **dev-decisions.md wins**.  
**Folder:** `Published-Research/`  
**Audience:** Coding newbie with a VPS who wants Research-Bot pages public and mostly automatic  
**Related:** `Research-Bot/` (writers of self-contained HTML reports)

---

## Locked direction (summary)

See `dev-decisions.md` for the full board. Short version:

- Self-contained Research-Bot HTML stays the report format (no ERB rewrite).
- Minimal **Rails** travel-log / adventure-artifacts blog; research = **field notes** → full HTML view.
- Publish **all** of `Research-Bot/`; **serve that folder** on the VPS (no copies).
- URLs under `https://throwingstarfish.studio/research/<report>`.
- Deploy **automatically on merge to `main` only** (no unmerged PR deploys, no manual steady-state steps).
- Bio copy: `bio.md`.

---

## Intent (one paragraph)

Keep Research-Bot’s current workflow: agents ship **one self-contained `.html` file per report** (CSS inside the file, readable offline without the repo). Add a separate, thin **public Rails site** under `Published-Research` that runs on your VPS as a travel log / artifacts home, lists Research-Bot reports as field notes, and serves the HTML at stable public URLs under throwingstarfish.studio. Automation means: when a PR **merges to `main`**, the live site updates with whatever is now in `Research-Bot/` — no SSH publish ritual.

---

## Current facts (what already exists)

- ~17 Research-Bot HTML reports today (one-off topics in `Research-Bot/` plus the `Apocalypse-Story/` series).
- Each file is a full document: `<!DOCTYPE html>`, embedded `<style>`, tables, citations — no shared CSS framework, no build step.
- Research-Bot README tells agents **not** to invent a `docs/` folder; topic series live in named folders; the human organizes.
- This monorepo has no existing Ruby web app for research hosting (other projects are separate; we do not copy their stacks).

---

## The big format question: HTML → Ruby, or keep HTML?

You asked whether we should rewrite reports into Ruby templates, keep them self-contained, or auto-convert. Here is the tradeoff in plain language.

| Approach | What it means | Self-contained offline? | Newbie / MVP fit |
|----------|---------------|-------------------------|------------------|
| **A. Serve HTML as HTML** | Ruby (or nginx) serves the `.html` files almost untouched; Ruby only builds an index / nav shell | Yes — originals stay openable as single files | Best fit |
| **B. Rewrite every report as ERB/Haml** | Content lives inside Ruby templates with a shared layout | Only if you also keep a separate HTML export | Heavy; fights Research-Bot agents |
| **C. Auto-convert HTML → Ruby views** | A script strips `<html>`/`<head>` and wraps body into ERB | Possible if converter also writes a standalone copy | Extra moving parts; converters break on custom CSS |
| **D. Change Research-Bot to Markdown, generate both** | Agents write `.md`; pipeline builds self-contained HTML *and* site pages | Yes, if pipeline emits standalone HTML | Bigger Research-Bot change; not needed for first public site |

**Planning recommendation (pending your MCQ answers):** Prefer **A**, optionally with a tiny wrapper (site header/footer around an iframe, or a shared chrome page that links into bare HTML). Do **not** convert Research-Bot deliverables into Ruby templates for v1. That preserves agent instructions and offline docs.

If you later want shared site branding without losing offline files, prefer **generate a published copy** (still HTML) plus an index — not a one-way rewrite into ERB.

---

## Decision board (answer these MCQs)

Mark one letter per question. Until you answer, the “Sample approved-shaped plan” below assumes the **recommended** choices in bold.

### Q1 — Content format on the live site

What should a visitor’s browser primarily receive for each report?

- **A)** The same self-contained HTML file Research-Bot already produces (copied or linked into Published-Research)
- B) A Ruby template (ERB) version of each report, rewritten once and maintained in Ruby
- C) Auto-converted Ruby views regenerated from HTML whenever Research-Bot changes
- D) Markdown in git; HTML and/or ERB generated for both offline docs and the site

**Recommended: A**

### Q2 — How much Ruby do we actually need?

- **A)** Tiny Ruby app (Sinatra or plain Rack) that lists published reports and serves static HTML from a folder
- B) Full Rails app (ActiveRecord, admin UI, users, etc.)
- C) Ruby static-site generator (e.g. Bridgetown/Jekyll-style) that builds HTML on the VPS or on your laptop, then nginx serves only static files
- D) No Ruby process: nginx (or Caddy) serves static files only; Ruby optional later

**Recommended: A or C for “I want a Ruby site”; D is fine if “Ruby” was about familiarity and you only need public URLs.**  
Newbie note: **C/D** are often easiest to keep running (no always-on app). **A** is still small and matches “Ruby site” literally.

### Q3 — Site chrome (nav, brand, “back to index”) vs pure document

- **A)** Bare documents: public URL opens the research HTML exactly as authored (index page separate)
- **B)** Thin site shell: Ruby (or static) index + optional header link “All research”; report pages stay self-contained
- C) Wrap every report in a shared layout (nav on every page) by injecting into HTML or using iframes
- D) Fully restyle all reports to one design system (shared CSS outside each file)

**Recommended: B** (preserves offline files; gives a public front door)

### Q4 — What gets published?

- **A)** Everything under Research-Bot automatically
- **B)** Explicit allowlist / `published:` manifest (you choose which reports go live)
- C) Only named series folders (e.g. Apocalypse-Story), never one-off car/travel notes
- D) Two tiers: public catalog + “unlisted” URLs for private/share links

**Recommended: B** (personal research includes car trips, local fireworks, etc. — probably not all public)

### Q5 — How does the VPS get new pages? (“automatically”)

- **A)** You SSH and `git pull` when you remember
- **B)** On push to `main` (or a `publish` branch), a simple deploy hook / cron pulls and restarts or rebuilds
- C) Agent/CI copies files into `Published-Research/public/` and opens a PR; merge triggers deploy
- D) VPS polls GitHub every N minutes

**Recommended: B or C.** Newbie-friendly path: **C** for curation in git, **B** for “once merged, site updates.”

### Q6 — Where do published file copies live in the repo?

- **A)** `Published-Research/public/reports/...` copies (or generated copies) of selected HTML
- B) Symlinks / relative links into `../Research-Bot/` (no copies)
- C) Only URLs/metadata in Published-Research; VPS checks out whole monorepo and serves from Research-Bot paths
- D) Separate publish-only git repo

**Recommended: A** for clear “what is live” inventory; avoids accidentally exposing unpublished drafts via path guessing if the whole Research-Bot tree is web-rooted.

### Q7 — Domain / URL shape (fill in later; pick pattern now)

- **A)** `https://research.yourdomain.com/` index + `/reports/slug.html`
- B) Path on an existing site: `https://yourdomain.com/research/...`
- C) IP + port for now, domain later
- D) GitHub Pages / Cloudflare Pages instead of VPS (Ruby local build only)

**Recommended: A or B** once DNS exists; **C** is fine for first smoke on the VPS.

### Q8 — Newbie ops comfort (honest constraint)

Pick the highest complexity you are willing to maintain yourself:

- **A)** “I can copy-paste SSH commands and edit one config file”
- B) “I can run Docker Compose and read logs”
- C) “I already run Rails/Passenger/Puma somewhere”
- D) “I want zero servers — use a static host”

**Recommended: match Q2 to this answer.** If **A** or **D**, bias hard to static files + nginx/Caddy (Ruby used to *generate* the index, not to stay running 24/7).

---

## Sample plan (locked answers: see `dev-decisions.md`)

Shape for a later implementation pass — still described as plan steps, not code in this PR.

### Goals

1. Public travel-log / adventure-artifacts home (bio + blog surface) on throwingstarfish.studio.
2. Research section as field notes → full self-contained HTML reports.
3. Research-Bot agents keep writing HTML the way they do today.
4. All `Research-Bot/**/*.html` served from the monorepo checkout (no copies, no allowlist).
5. Auto-deploy on **merge to `main` only** (no unmerged PR production deploys, no manual steady-state).

### Non-goals (v1)

- No user accounts, comments, search backend, or CMS for reports.
- No rewriting reports into ERB.
- No redesign of every report’s internal CSS into one theme.
- No tests/CI smoke scripts unless you explicitly ask later (per monorepo agent rules).
- Do not pull architecture from other monorepo projects.
- No production deploys from open/unmerged PRs.

### Proposed folder shape (later implementation)

```text
Published-Research/
  README.md
  bio.md
  dev-decisions.md
  master-plan.md
  dev-log.md
  .cursor/plans/            # historical draft
  # later: minimal Rails app (travel blog + /research routes)
  # later: deploy/ (nginx + systemd + GitHub Action notes)
Research-Bot/               # served as-is from VPS monorepo checkout
  *.html
  Apocalypse-Story/*.html
```

### Publish flow (happy path)

```text
Research-Bot agent finishes report.html on a PR
        │
        ▼
PR merges to main
        │
        ▼
GitHub Action / webhook: VPS git pull (+ Rails restart if needed)
        │
        ▼
Rails scans Research-Bot/ and serves new file at
throwingstarfish.studio/research/<slug>
```

### Rails’ job (thin)

- Home / travel-log chrome + bio.
- Field-notes index from filesystem scan of Research-Bot HTML.
- Report show: shared layout around the self-contained HTML (iframe or body extract — pick at implement time).
- Research content stays HTML. Rails is the travel-site librarian, not the report author.

### HTML “conversion” decision

- **Do not** convert reports to Ruby templates for v1.
- **Do** keep originals in `Research-Bot/` as the editable source of truth and the live file source.

### VPS newbie path (ops sketch)

1. Point throwingstarfish.studio (or confirm DNS) at the VPS.
2. Install nginx (or Caddy) + git + Ruby/Rails runtime.
3. Clone this monorepo; Rails app lives under Published-Research; reads sibling `Research-Bot/`.
4. systemd unit for Puma; nginx terminates TLS and proxies.
5. GitHub Action on `push` to `main`: SSH/`git pull` + restart — **only after merge**, never for open PR branches.
6. HTTPS via Let’s Encrypt.

### Privacy / safety checklist before go-live

- Entire Research-Bot tree is intentional public surface (human accepted; repo already public).
- Confirm reports do not embed private emails, addresses, or credentials beyond what is already in the public repo.
- Robots / indexing policy — separate small decision later if needed.

### Implementation phases (after this plan PR — still no calendar estimates)

1. Scaffold minimal Rails under Published-Research (home, bio, field-notes index, report show).
2. Wire filesystem catalog of `Research-Bot/**/*.html` + slug rules for `/research/<report>`.
3. VPS + nginx + Puma + TLS for throwingstarfish.studio.
4. Merge-to-main auto-deploy Action/webhook.
5. Optional polish: series grouping (Apocalypse-Story), travel post templates, field-notes card styling.

---

## Alternatives we considered and de-prioritized

1. **Sinatra-only or static SSG** — dropped once human chose minimal Rails blog + research day one.
2. **Rewrite HTML → ERB as source of truth** — breaks Research-Bot agent contract.
3. **Auto HTML→ERB converter** — brittle on bespoke per-report CSS.
4. **Allowlist + HTML copies** — superseded; publish all and serve from Research-Bot.
5. **Deploy unmerged PR branches to production** — explicitly rejected.
6. **Manual `bin/deploy` as steady state** — rejected; automation required.

---

## Remaining open questions (non-blocking)

- Exact slug scheme for nested paths (e.g. `Apocalypse-Story/...`).
- Iframe vs body-extract for wrapping HTML in site chrome.
- Whether Apocalypse-Story gets a dedicated series index page on day one.

---

## Approval gate

**Closed 2026-07-11.** Answers live in `dev-decisions.md`; approved execution summary in `master-plan.md`.
