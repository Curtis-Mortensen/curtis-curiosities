# Draft plan — Publish Research-Bot HTML on a public Ruby site (VPS)

**Status:** Draft for human approval (no code in this pass)  
**Folder:** `Published-Research/`  
**Audience:** Coding newbie with a VPS who wants Research-Bot pages public and mostly automatic  
**Related:** `Research-Bot/` (writers of self-contained HTML reports)

---

## Intent (one paragraph)

Keep Research-Bot’s current workflow: agents ship **one self-contained `.html` file per report** (CSS inside the file, readable offline without the repo). Add a separate, thin **public site** under `Published-Research` that runs on your VPS with a small Ruby stack, lists the reports you choose to publish, and serves them at stable public URLs. Automation should mean: when you (or an agent) mark a report as publishable, the live site updates without hand-editing a server by SSH every time.

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

## Sample plan (assumes recommended answers: Q1=A, Q2=A or C, Q3=B, Q4=B, Q5=B/C, Q6=A)

This is the shape we would implement **after** you approve — still described as plan steps, not code.

### Goals

1. Public front door listing only allowlisted research reports.
2. Each report URL serves self-contained HTML (same reading experience as opening the file locally).
3. Research-Bot agents keep writing HTML the way they do today.
4. Publishing is a deliberate step (manifest), then deploy is mostly automatic.
5. VPS setup is documented in short “do these commands” form for a newbie.

### Non-goals (v1)

- No user accounts, comments, search backend, or CMS.
- No rewriting reports into ERB.
- No redesign of every report’s internal CSS into one theme.
- No tests/CI smoke scripts unless you explicitly ask later (per monorepo agent rules).
- Do not pull architecture from other monorepo projects.

### Proposed folder shape (later implementation)

```text
Published-Research/
  README.md                 # already started
  dev-log.md
  .cursor/plans/            # this draft
  manifest.yml              # allowlist: slug, title, source path, date, series, public: true
  public/                   # what the web server exposes
    index.html              # catalog (generated)
    reports/                # copies of allowlisted Research-Bot HTML
  scripts/                  # (later) sync-from-manifest, build-index
  app/                      # only if Q2=A: tiny Sinatra/Rack app
  deploy/                   # nginx/Caddy snippet + systemd notes for the VPS
```

### Publish flow (happy path)

```text
Research-Bot agent finishes report.html
        │
        ▼
Human (or later a small checklist) adds an entry to manifest.yml
        │
        ▼
sync script copies file → public/reports/<slug>.html
        │
        ▼
build-index writes public/index.html (title, date, series links)
        │
        ▼
git commit + push
        │
        ▼
VPS deploy hook: git pull → (optional) rebuild → reload nginx
        │
        ▼
Public visitors see updated catalog + report URLs
```

### Ruby’s job (thin)

- **If Sinatra/Rack (Q2=A):** routes for `/` (catalog from manifest) and `/reports/:slug` (send file). Static middleware for assets if any.
- **If SSG (Q2=C):** a Rake task or Ruby script reads `manifest.yml`, copies HTML, writes `index.html`; process exits; nginx serves `public/`.
- **Either way:** Research content stays HTML. Ruby is the librarian, not the author.

### HTML “conversion” decision (locked in this sample)

- **Do not** convert reports to Ruby templates for v1.
- **Do** optionally post-process a *published copy* only if needed (example: inject a single “← All research” link into `<body>`). Keep the Research-Bot original untouched.
- **Do** keep originals in `Research-Bot/` as the editable source of truth.

### VPS newbie path (ops sketch)

1. Point a domain (or subdomain) DNS A-record at the VPS.
2. Install nginx (or Caddy) + git.
3. Clone this monorepo to e.g. `/var/www/curtis-curiosities` (or a sparse checkout of Published-Research if you prefer later).
4. Web root = `Published-Research/public` (not the whole monorepo, so unpublished Research-Bot files are not web-visible).
5. Deploy: `git pull` in a hook on push, or a 5-line cron.
6. HTTPS via Let’s Encrypt (Certbot or Caddy automatic).
7. If you chose a always-on Ruby app: one systemd unit running Puma/Rack behind nginx; if SSG/static, skip that unit entirely.

### Privacy / safety checklist before go-live

- Review allowlist: exclude personal logistics (travel, local events, vehicle fitment) unless you want them public.
- Confirm reports do not embed private emails, addresses, or credentials.
- Robots: decide if the catalog should be indexed by Google (`robots.txt` / noindex) — separate small decision later.

### Implementation phases (after approval — still no calendar estimates)

1. **Manifest + sync design** — finalize `manifest.yml` fields; document “how to publish one report.”
2. **Static catalog MVP** — generate `public/index.html` + copy allowlisted files; open locally in a browser.
3. **VPS static serve** — nginx/Caddy serves `public/`; HTTPS; first 1–2 reports live.
4. **Automation** — deploy hook on push; optional Ruby Sinatra only if you still want a dynamic Ruby process.
5. **Polish (optional)** — series grouping, “updated at,” bare inject of back-link, custom domain branding on index only.

---

## Alternatives we considered and de-prioritized

1. **Rails full app** — overkill for serving documents; more to break for a newbie.
2. **Rewrite HTML → ERB as source of truth** — breaks Research-Bot agent contract (self-contained HTML) and dual-maintenance pain.
3. **Auto HTML→ERB converter** — brittle on bespoke per-report CSS; little benefit over serving HTML.
4. **Serving entire `Research-Bot/` tree from the web root** — easy, but publishes drafts and personal one-offs by accident.

---

## Open questions (beyond the MCQs)

- Preferred domain / subdomain?
- Should Apocalypse-Story be one public series page with child links?
- Do you want a visible “Published-Research” brand name on the index, or your name / another project name?
- Any reports that must stay private forever even if someone knows the path?

---

## Approval gate

Please reply with letters for **Q1–Q8** (and any overrides). After that, this draft can move toward `master-plan.md` in this folder and implementation can start in a later pass.
