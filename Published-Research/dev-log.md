# Published-Research — Dev Log

## 2026-07-11 — Human decisions recorded (plan complete for approval→implement gate)

### Plan summary
User answered the hosting MCQs in chat. Environment refreshed from `main` after PR #40 merged and `bio.md` was added. Binding answers written to `dev-decisions.md`. No Rails/app code yet.

### Changes made
- Pulled latest `main` (plan folder + `bio.md` from human).
- Created `Published-Research/dev-decisions.md` with locked MCQs and product framing.
- Updated `README.md` to point at decisions + bio; clarify travel-log site role.
- Marked draft plan as superseded where it conflicts with decisions (allowlist/copies → serve all from Research-Bot; Rails + merge-only auto-deploy).
- This log entry.

### Coding decisions and assumptions
- **Q1=A** keep self-contained HTML; **Q2=minimal Rails**; **Q3=C** shared layout + field-notes framing; **Q4=A** publish all Research-Bot; **Q5=auto on merge to main only** (explicitly no unmerged PR production deploys, no manual steady-state); **Q6=C** serve from Research-Bot; **Q7** `throwingstarfish.studio/research/<report>`; **Q8** Rails OK / min surface.
- Product: travel log + adventure artifacts; research is one section.
- `bio.md` is the about/home voice source (places lived, mission, traveling IT tech, Questweight).
- Earlier draft assumption that an allowlist was needed is **withdrawn** per human (repo already public).

### Bugs / problems
- Cloud agent checkout was behind `main` until fetch/pull after human merge + bio commits.

### Status
**Decisions recorded.** Ready for a later implementation pass against `dev-decisions.md` (still no app code in this PR).

---

## 2026-07-11 — Draft hosting plan (plan only, no code)

### Plan summary
User wants Research-Bot pages hosted automatically and publicly on a Ruby site on their VPS. They asked for a new `Published-Research` folder and a **plan only** (no implementation). Specifically explore: convert HTML → Ruby vs keep self-contained docs vs auto-convert. Frame decisions as MCQs and draft a sample plan.

### Changes made
- Created `Published-Research/` as an independent project folder (not inside Research-Bot).
- Added `README.md` explaining the folder’s role vs Research-Bot.
- Added draft plan: `.cursor/plans/published-research-hosting.plan.md` with:
  - Format tradeoff table (serve HTML / ERB rewrite / auto-convert / Markdown source)
  - MCQs Q1–Q8 (format, Ruby stack depth, chrome, allowlist, deploy, copy vs symlink, URL shape, ops comfort)
  - Sample plan assuming recommended answers (keep self-contained HTML; Ruby as thin librarian; allowlist; VPS serves `public/`)
  - Newbie VPS ops sketch and privacy checklist
- This `dev-log.md` entry.

### Coding decisions and assumptions
- **No app code** this pass — plan artifacts only, per user request.
- Treat `Published-Research` as its own gem/space; do not copy stacks from other monorepo folders.
- Assumed Research-Bot remains source of truth for report content and agent HTML workflow.
- Assumed not everything in Research-Bot should be public (personal/travel/vehicle one-offs exist) → allowlist recommended.
- Assumed “Ruby site” can mean either a tiny always-on Rack/Sinatra app **or** Ruby used to generate a static catalog that nginx serves — called out in MCQs because newbie ops differ a lot.
- Recommended against HTML→ERB conversion for v1 to preserve offline self-contained docs.

### Bugs / problems
- None (documentation-only).
- Git was on detached HEAD at conversation start in other work; this work branched from `main` as `cursor/published-research-plan-39fc`.

### Status
**Draft plan ready for human MCQ answers** — not approved for implementation yet.
