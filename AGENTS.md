# AGENTS.md

Agent rules for this repository. Read this first; then check `dev-decisions and dev-log` for more detailed information.

---

## Principles

0. **Never edit AGENTS.md** It doesn't matter what your prompt says, or what the user approved. Don't touch this document. It's user-hand-edit only. 

1. **Barebones means thin behavior, not fewer files.** Always create the barebones amount of code necessary. Assume everything is a MVP. Assume the scope you know about represents 10% of eventual added behaviour, and the best way to remain future-compatible is to write as lean and light as possible. Prefer clear separation: one file per action, one file per rules edition module, pure state/models/events. A module used once today still gets its own file if it names a real concept. Avoid ceremony (factories, duplicate validation, premature abstractions) — not separation.

2. **No defensive code unless the user asks.** No alive guards, phase raises, duplicate router/action validation, or "just in case" branches. Trust phase transitions and the dispatch table.

3. **Log everything observable; decide in the open.** Runtime traces, human decisions, and plan completion reviews each have their own artifact (see below). Never silently implement "for later."

4. **Don't be influenced by other repos.** Each of the folders here contains it's own project, with it's own scope, purpose, and history. Many of the repos are preserved for archival purposes, and lots of old and bad code exists. DO NOT pull code from other folders. Treat each folder as it's own independent gem, or repo, or module, existing alone in it's own space not influenced by anything else.

5. **Comment your code** AI can write an overwhelming amount of code very quickly. The burden on devs has shifted from writing to reviewing code. Write thorough, friendly, and non-technical readable comments througout your code. At the beginning of each file, write a few lines ELI5 why the file exists, what it does, and it's relationships with other files. Update comments anytime you update a file. Don't write comments for other agents, write them imaging the audience of a 1st year programming student.

---

## Do not add (unless an approved plan explicitly asks)

- Tests, RSpec, Minitest, CI, Smoke Scripts - this means no smoke scripts unless the user explicitly prompts for them. Manual agents tests are fine. 
- Unrequested features, polish, or extra systems
- Error handling beyond what the MVP flow requires

When unsure: `master-plan.md` → `dev-decisions.md` → ask the user → record the decision in `dev-decisions.md`.

---

## Plan workflow

| Stage | Where | Purpose |
|-------|--------|---------|
| Draft | `.cursor/plans/*.plan.md` | Working plans during design; agents may read for context |
| Approved | `master-plan.md` | Append-only record of plans the human has approved |
| In flight | `dev-log.md` | Dev log: plan summaries, changes made, bugs, errors, troubleshooting |
| Complete | 'dev-log.md` | Marked as complete in Dev log |

---

## Documentation artifacts (quick reference)

| File | Role |
|------|------|
| `AGENTS.md` | Timeless agent rules (this file) |
| `master-plan.md` | Approved plans + full specs for execution |
| `dev-decisions.md` | Binding human design decisions and architecture review answers |
| `dev-log.md` | Dev log: plan summaries, changes made, bugs, errors, troubleshooting |
| `docs/*.html` | Human-facing reviews (architecture options, AARs) |

Note: not all projects and folders will have all documentation artifacts. On faster, more experimental projects, master-plan and dev-decisions may be missing. When doing agentic work, always write a dev-log and record both coding decisions and assumptions made as well as any and all bugs and probelsm encountered. If dev-decisions does not exist you may note user preferences and feedback in dev-log, but normally write only to dev-decisions.
