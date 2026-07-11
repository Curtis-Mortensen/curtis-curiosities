# Published-Research

This folder is the **publishing / public-site home** for a travel-log blog that also surfaces Research-Bot reports as field notes.

## What this is (ELI5)

`Research-Bot/` is where agents write long, self-contained HTML research papers (CSS baked into each file so one file opens in a browser offline).

`Published-Research/` is *not* where research gets written. It holds the **public site plan**, **bio**, **binding decisions**, and (later) the thin Rails app that runs on the VPS at throwingstarfish.studio — travel log + adventure artifacts, with research as one section.

## Status

**Decisions locked** in `dev-decisions.md`. Plan draft still in `.cursor/plans/` for history; implement only after / according to those decisions. No Rails app code in this folder yet.

| Doc | Role |
|-----|------|
| [`dev-decisions.md`](dev-decisions.md) | Binding human answers (MCQs + product framing) |
| [`master-plan.md`](master-plan.md) | Approved execution brief |
| [`bio.md`](bio.md) | Site bio / about voice |
| [`.cursor/plans/published-research-hosting.plan.md`](.cursor/plans/published-research-hosting.plan.md) | Earlier draft plan (superseded where it conflicts with decisions) |
| [`dev-log.md`](dev-log.md) | What changed during planning |

## Relationship to other folders

- **Source of truth for report HTML:** `Research-Bot/` (served directly; no copies)
- **This folder:** site identity, decisions, and later the Rails + deploy pieces
- Do not reinvent Research-Bot’s writing rules here; agents keep producing self-contained HTML there
- Do not pull stacks from other monorepo projects
