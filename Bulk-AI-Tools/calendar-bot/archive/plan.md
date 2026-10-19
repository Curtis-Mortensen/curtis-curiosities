# Calendar Bot: threaded Python MVP

## Summary

Archive the existing contents of `Bulk-AI-Tools/calendar-bot`, then build a small command-line pipeline:

**PDFs/screenshots → extracted text → Luna 6 High → event JSON → Google Calendar + local Markdown + local FieldNation folder.**

This phase includes real Google Calendar integration. Google Docs and Drive remain local substitutes.

## Processing and interfaces

- Run with `python run.py`, defaulting to an ignored `uploads/` directory and four worker threads; expose `--uploads`, `--workers`, and `--calendar-id`.
- Each immediate upload subfolder represents one WO. Combine its PDFs and screenshots into one extraction. Treat each loose file as a separate WO.
- Use `ThreadPoolExecutor` to process jobs concurrently. Serialize shared Markdown, processed-file list, YAML, and Calendar writes.
- Separate input discovery, text extraction, Luna extraction, drive estimates, Calendar writing, Markdown insertion, file copying, and logging into small Python modules with readable introductory comments.
- Extract embedded PDF text with `pypdf`. Use Tesseract for screenshots and scanned PDF pages, rendering PDF pages through Poppler.
- Call the OpenAI Responses API with `model="gpt-6-luna"`, `reasoning={"effort": "high"}`, and structured JSON output. These settings are supported by [the model documentation](https://developers.openai.com/api/docs/models/gpt-6-luna).
- JSON contains the arrival window, estimated work duration, city, store abbreviation, and fields from the provided Markdown example. Missing optional information stays blank.

## Output behavior

**Calendar**

- Use a separate OAuth helper and Calendar writer, with local `credentials.json` and `token.json`.
- Default to the authenticated user’s primary calendar; allow another calendar ID.
- Use `America/Phoenix`.
- Event start = earliest arrival minus outbound drive time.
- Event end = earliest arrival plus estimated work duration.
- Include the arrival window, duration, drive estimate, and extracted job details in the description.
- Use a stable event ID derived from the upload job’s relative path so interruption recovery cannot create another event for that same job. Google supports [client-supplied IDs for this purpose](https://developers.google.com/workspace/calendar/api/guides/create-events).

**Local Markdown and FieldNation**

- Follow the supplied Markdown example’s month/date headings, bold job title, WO number, and labeled fields.
- Insert dates chronologically and jobs by earliest arrival within each date. Create missing headings and preserve existing notes.
- Every new job gets a blank After-Action Review containing MOD, RE Name, Time on site, and Closing Notes.
- Copy original inputs into `local/FieldNation/City-Date-Store/`, such as `Show-Low-2026-10-16-JCP/`. Leave that folder available for later photos.
- Use `Unknown-Store` when the optional store abbreviation cannot be extracted.
- Add source filenames, relative to uploads, to `processed.md` only after every destination succeeds.

**Drive estimates**

Use this editable table, in minutes:

| Minutes | Cities |
|---|---|
| 15 | Mesa |
| 30 | Gilbert, Apache Junction, Tempe |
| 45 | Chandler, Scottsdale, Phoenix, Gold Canyon, Queen Creek, Fountain Hills |
| 60 | Surprise, Glendale, Peoria, Goodyear, Avondale, Buckeye, San Tan Valley, Maricopa |
| 75 | Casa Grande |
| 90 | Payson |
| 120 | Tucson, Prescott, Sedona |
| 150 | Flagstaff |
| 180 | Show Low, Pinetop-Lakeside |

Document Mesa Temple as the approximate origin. Explicitly record that future agents **must not automatically improve this script or add maps, routing, traffic, or address-based calculations**.

## Errors, logging, and recovery

- Require a readable job date, earliest arrival, positive work duration, and a city present in the table before creating any destination output.
- Insufficient information produces a terminal error and YAML error entry. Discard the incomplete extraction; create no Calendar entry, Markdown entry, job folder, or processed-file entry.
- No paused-job state, correction interface, or partial JSON storage. A later rerun retries failed extraction from its inputs.
- For valid jobs, checkpoint complete event data and each destination’s status in YAML. Reruns resume unfinished destination steps.
- Record timestamps, source files, stage starts/completions, durations, model/request metadata, output locations, Calendar IDs, skips, and errors. Never log credentials.
- Protect shared YAML writes with a thread lock and atomic file replacement. Make destination steps repeatable so interruption between a successful write and its checkpoint does not duplicate output.
- Continue other jobs after one fails; exit nonzero if any job fails.
- Keep only checks necessary for these requested behaviors. Add no retry framework, database, web interface, or extra systems.

## Archive, documentation, and verification

- Move every existing item into `archive/`, including the research, Markdown example, calendar sample, and download metadata.
- Add setup/run instructions, dependencies, approved-plan documentation, design decisions, and a development log. Leave `AGENTS.md` untouched.
- Gitignore uploads, local outputs, YAML runtime logs, processed-file records, credentials, virtual environments, and caches.
- Manually verify multiple concurrent jobs, grouped screenshots, searchable/scanned PDFs, chronological insertion, blank reviews, preserved notes, duplicate reruns, interruption recovery, and insufficient-information errors.
- Verify a labeled Calendar test event and read it back. Record actual verification results and any outstanding setup.
- Add no committed tests, smoke scripts, or CI.

**Current prerequisites:** this environment has no `OPENAI_API_KEY`, OCR tools, or required Python packages installed; no Google credential files were found in the project. Live API verification requires those credentials and dependency setup.
