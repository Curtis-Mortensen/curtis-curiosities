# Calendar Bot Design Decisions

These decisions implement the plan approved on 2026-10-18 and the user's instruction to complete it. `master-plan.md` preserves the full approved specification.

- Use Python with `ThreadPoolExecutor`, defaulting to four workers. Keep each input/output action in a small module and share simple immutable job and event records.
- Use OpenAI Responses with `gpt-6-luna`, high reasoning effort, and strict structured JSON. Keep extraction grounded in the uploaded text; missing required details fail before any job destination is created.
- Use real Google Calendar with OAuth client and token files. Use local Markdown and FieldNation folders in place of Google Docs and Drive.
- Use `America/Phoenix`, include outbound travel before the earliest arrival, and end after the estimated onsite work duration.
- Estimate travel from Mesa Temple using the approved editable city table. Future agents must not automatically improve this script or add maps, routing, traffic, or address-based calculations.
- Identify a job by its upload-relative path. Preserve that identity across Calendar writes and checkpoint recovery. Completed source paths are immutable; input editing and rescheduling are outside this MVP.
- Share one thread lock across destination writes, processed records, and YAML state. Save complete validated events and per-destination completion in YAML, using atomic replacement. Run one process at a time; process-wide scheduling is outside this plan.
- Start Google consent explicitly through `google_auth.py`. Pipeline runs use an existing token and report the sign-in command when access is missing, so a batch does not wait indefinitely for a browser.
- Archive every item present at implementation start. This checkout had only the plan, development log, and calendar sample. The research, download metadata, and Markdown example mentioned by the plan were absent. The Markdown format therefore follows the specified month/date headings, bold WO title, labeled fields, and blank review labels.
- User authorized Luna 6 High subagents for parallel implementation followed by primary-agent review. Credentials may be reused from the user's existing setup; keep them in ignored private files and never record their values in logs.
- Add no committed tests, smoke scripts, or CI. Use disposable manual exercises to verify the behaviors listed in the approved plan, and record actual results in `dev-log.md`.

## 2026-10-18 — Resume after interruption

- User requested continuing with GPT-6 Luna subagents at high reasoning effort, followed by primary-agent review. Three agents reviewed the pipeline, extraction, and output modules separately.
- User corrected the credential source: Hermes runs on the local NAS at `192.168.1.83`, not on the VPS. Use that NAS for Hermes credential discovery. The user supplied the `fin` SSH account and later suggested `curtis`; keep the supplied password out of project documentation and source files.
- Keep the plan's live Calendar verification outstanding until an authorized Google token is available. Local service doubles verify request behavior but do not count as a live Calendar write/readback.

## 2026-10-18 — Authorized NAS credentials and live completion

- User corrected the NAS password for `fin`; SSH access succeeded. Reuse the Google client and authorized token from `/home/fin/.hermes/` in ignored project files with permissions 0600. Leave the NAS files unchanged and never record password or token values.
- Preserve saved scopes when loading a reused Google token. Replacing Hermes' original Calendar grant with `calendar.events` produced Google's `invalid_scope` refresh error; refreshing with its original saved scopes succeeded. New interactive authorization continues to request only `calendar.events`. A Luna High agent implemented and manually checked the helper change, and the primary agent reviewed and verified it with Google.
- The approved live Calendar write/readback requirement is now satisfied. Keep the clearly labeled synthetic verification event available for the user to inspect; temporary input/output files from the manual exercise were removed automatically.

## 2026-10-18 — Fixed annual document and real FieldNation Drive output

- User requested real Docs/Drive destinations and confirmed the original annual Google Doc. Discovery found two additional `.md` copies; leave those copies alone. The selected IDs live only in ignored `.env`; real links are also in ignored `local/destinations.md`.
- Replace the local stand-ins with a Docs writer and a Drive writer. Preserve existing document content and add scoped native text/style updates. Each job links to its real Drive subfolder, while the document title area links to the main FieldNation folder.
- Use the existing YAML runtime notebook to persist pre-generated Drive IDs before creating uploads/folders, and use Docs named ranges in the same batch as insertion to recognize completed jobs after interruption. Keep Calendar's existing stable IDs. Bind checkpoints to the fixed Google destination IDs.
- Completed sources remain completed; this request does not authorize backfilling all past local outputs. Live synthetic writer checks use temporary cloud artifacts and a copy of the existing document, with cleanup after verification.
