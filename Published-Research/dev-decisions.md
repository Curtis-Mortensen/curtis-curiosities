# Published-Research — Dev Decisions

Binding human decisions for the public travel / field-notes site that hosts Research-Bot reports.  
Recorded 2026-07-11 after MCQ discussion. Implementation must follow these unless a newer entry supersedes them.

---

## Product framing

- The public site is a **home for a travel log and adventure artifacts**, not a research-only microsite.
- **Research** is one section of that site, themed like **field notes** until the visitor opens the **modern self-contained HTML** view of a report.
- Site bio source for the about/home voice: `Published-Research/bio.md` (travel, places lived, mission, work as traveling IT tech, Questweight Studios).
- Public host path: **`https://throwingstarfish.studio/research/<report>`** (research under the throwingstarfish.studio site).

---

## MCQ answers (locked)

### Q1 — Content format on the live site → **A**

Visitors get the **same self-contained HTML** Research-Bot already produces. Do **not** rewrite reports into ERB as the source of truth. Do **not** auto-convert HTML → Ruby views for v1. Research-Bot agents keep shipping offline-openable `.html` files.

### Q2 — How much Ruby → **Rails (minimal)**

Use a **minimal Rails** app so day one can include:

1. A thin **blog / travel-log** surface (home for adventures + artifacts)
2. A **research / field-notes** section that indexes and opens Research-Bot HTML

Constraints the human set:

- Rails is OK (prior experience), but **minimum breakable surface** and **minimum viable code**
- Prefer filesystem-backed research catalog over a CMS/DB for reports on day one
- No unrequested extras (admin, auth, search, etc.)

### Q3 — Site chrome → **C** (with field-notes framing)

Reports appear inside the **shared site layout / nav**. Presentation pattern:

1. Field-notes style listing / teaser in the travel-site chrome  
2. Navigate into the **modern HTML report** view (still the Research-Bot file, wrapped or framed by site chrome—not a separate ERB rewrite of the content)

### Q4 — What gets published → **A**

**Everything under `Research-Bot/`** is publishable. The monorepo is already public; no allowlist required for v1.

### Q5 — How the VPS gets new pages → **Fully automatic on merge to `main`**

- **No manual deploy steps** (no SSH `git pull` as the normal path).
- **No unmerged PRs on production.** Opening or updating a PR must not change the live site.
- Normal authoring path stays PRs; when a PR **merges into `main`**, automation updates the VPS (webhook or GitHub Action → `git pull` / restart as needed).
- New Research-Bot HTML on `main` becomes live because the app **serves that folder** (see Q6).

### Q6 — Where published files live → **C**

**Serve directly from `Research-Bot/`** in the monorepo checkout on the VPS.

- No publish copies under `Published-Research/public/reports/`
- No symlinks (Q6-B rejected in favor of C)
- `Published-Research/` holds site plan, bio, decisions, and (later) the Rails app / deploy config—not duplicate report bodies

### Q7 — URL shape → **path on throwingstarfish.studio**

- Base: `https://throwingstarfish.studio/`
- Research reports: `https://throwingstarfish.studio/research/<report>`  
  (`<report>` = stable slug derived from the HTML filename / relative path; exact slug rules to be fixed at implementation)

### Q8 — Ops comfort → **Rails OK; optimize for hard-to-break MVP**

- Willing to run Rails (done it before; beginner-friendly)
- Day-one priority: **get it running**, small surface area, little to babysit
- Prefer boring deploy automation over clever infra

---

## Day-one scope (approved direction)

In scope:

- Minimal Rails app for travel-log home + bio + field-notes research section
- Scan/serve all `Research-Bot/**/*.html`
- Shared layout; field notes → full HTML report
- Auto-deploy when PRs merge to `main`
- Target URL space under throwingstarfish.studio

Out of scope for v1 (unless a new decision says otherwise):

- Unmerged PR previews on production
- HTML → ERB conversion pipeline
- Allowlist / two-tier public vs unlisted
- Manual publish scripts as the steady-state process
- Copying or mirroring report HTML into Published-Research
- Pulling design/code from other monorepo project folders

---

## Implications for the earlier draft plan

The draft in `.cursor/plans/published-research-hosting.plan.md` recommended an allowlist and optional static copies. Those recommendations are **superseded** by this file:

| Draft suggestion | Locked decision |
|------------------|-----------------|
| Allowlist (Q4=B) | Publish all Research-Bot (Q4=A) |
| Copies in `public/reports/` (Q6=A) | Serve from Research-Bot (Q6=C) |
| Tiny Sinatra *or* static SSG as default | Minimal Rails blog + research |
| Bare or thin chrome (Q3=A/B) | Shared layout + field-notes framing (Q3=C) |
| Manual or semi-manual deploy OK | Merge-to-main automatic only |

When plan docs disagree with this file, **this file wins**.
