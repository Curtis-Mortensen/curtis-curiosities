# Published-Research

This folder is the **publishing home** for Research-Bot reports you want on a public website.

## What this is (ELI5)

`Research-Bot/` is where agents write long, self-contained HTML research papers (CSS baked into each file so one file opens in a browser offline).

`Published-Research/` is *not* where research gets written. It is where we plan and later build the thin “storefront”: a public Ruby-hosted site on your VPS that lists chosen reports and serves them to anyone with a link.

## Status

**Plan only — no app code yet.** See the draft plan and answer the multiple-choice decisions before any implementation.

| Doc | Role |
|-----|------|
| [`.cursor/plans/published-research-hosting.plan.md`](.cursor/plans/published-research-hosting.plan.md) | Working draft: MCQs, recommended shape, VPS newbie path |
| [`dev-log.md`](dev-log.md) | What was decided/assumed during planning |

## Relationship to other folders

- **Source of truth for content:** `Research-Bot/` (and topic subfolders like `Apocalypse-Story/`)
- **This folder:** publish pipeline plan + (later) the site that hosts selected copies
- Do not reinvent Research-Bot’s writing rules here; agents keep producing self-contained HTML there unless an approved plan says otherwise.
