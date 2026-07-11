# Published-Research — Master Plan

Append-only record of **approved** plans. Binding details and MCQ answers live in `dev-decisions.md`; this file is the execution brief.

---

## 2026-07-11 — Travel-log Rails site hosting Research-Bot (approved)

### Intent

Run a minimal Rails site on the VPS as the public home for a **travel log and adventure artifacts** (throwingstarfish.studio). Surface all Research-Bot self-contained HTML reports as a **field notes** section that opens into the modern HTML report view. Keep Research-Bot’s agent workflow unchanged.

### Locked choices (see `dev-decisions.md`)

| Topic | Choice |
|-------|--------|
| Report format | Self-contained Research-Bot HTML (no ERB rewrite) |
| Stack | Minimal Rails (blog + research day one) |
| Chrome | Shared layout; field notes → full HTML |
| Publish scope | All of `Research-Bot/` |
| File location | Serve from `Research-Bot/` on the monorepo checkout |
| URLs | `https://throwingstarfish.studio/research/<report>` |
| Deploy | Automatic on **merge to `main` only**; no unmerged PR deploys; no manual steady-state |
| Bio | `bio.md` |

### Day-one deliverables (implementation — not in the decisions PR)

1. Minimal Rails app under `Published-Research/`
2. Home / travel framing + bio
3. Field-notes index scanning `Research-Bot/**/*.html`
4. Report route under `/research/...`
5. VPS: nginx + Puma + TLS
6. GitHub Action / webhook: merge to `main` → pull → restart

### Explicit non-goals (v1)

Unmerged PR production deploys; HTML→ERB conversion; allowlist/copies; CMS/auth/search; copying code from other monorepo folders; tests/smoke scripts unless requested.

### Status

**Planning complete.** Implementation is a separate pass against this brief + `dev-decisions.md`.
