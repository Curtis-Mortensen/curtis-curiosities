# Calendar Bot

Turn work-order PDFs and screenshots into Google Calendar appointments, entries in the fixed annual Google Doc, and original-file uploads in the real FieldNation Drive folder. Each immediate subfolder in `uploads/` is one work order. Each loose supported file is a separate work order. Files inside a job folder can be nested.

The bot uses four worker threads by default. It reads searchable PDF text with pypdf, uses Tesseract and Poppler for images and scanned PDF pages, and asks [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) for structured event details with high reasoning effort.

## Setup

Use Python 3.11 or newer. Install Tesseract with English language data and Poppler, then install the Python dependencies:

```bash
# Debian / Ubuntu:
sudo apt-get install python3-venv tesseract-ocr tesseract-ocr-eng poppler-utils
# Fedora uses: sudo dnf install tesseract tesseract-langpack-eng poppler-utils

cd Bulk-AI-Tools/calendar-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# On a fresh checkout, copy .env.example to .env before entering your key.
```

Set `OPENAI_API_KEY`, `GOOGLE_DOC_ID`, and `GOOGLE_DRIVE_FOLDER_ID` in `.env`. The two destination IDs pin the existing annual document and FieldNation folder; the bot does not search by name or create a new annual document. Optionally set `GOOGLE_CALENDAR_ID`; its default is `primary`. Actual IDs, credentials, inputs, and runtime files are ignored by Git. Clickable links to the configured document and folder are also saved in ignored `local/destinations.md`.

The current workspace has dependencies in `.venv`, a configured OpenAI key, authorized Google client/token files reused from Hermes on the user's local NAS, and the confirmed original annual document and FieldNation folder configured. Keep those private settings when using this workspace. Verification details are in `dev-log.md`.

Enable Calendar, Docs, and Drive APIs in the Google Cloud project, configure its OAuth consent screen, and download a desktop OAuth client JSON as `credentials.json`. If the Google app is in testing, your account must be an allowed test user. The [Google Calendar Python setup](https://developers.google.com/workspace/calendar/api/quickstart/python) explains desktop sign-in setup.

Sign in once before processing real jobs:

```bash
python google_auth.py
# If this terminal cannot open a browser:
python google_auth.py --no-browser
```

Open the printed URL in a browser on the same machine. The helper waits for a local callback and saves `token.json`; later runs refresh that token. When running on a remote machine, forward the printed callback port through SSH before opening the URL. `credentials.json` identifies the app; `token.json` grants access. An unattended pipeline run reports a sign-in instruction if the token is missing. Reused tokens keep their saved permissions during refresh; new sign-ins request Calendar events, Docs, and Drive access. The configured workspace already has a working grant for all three, so no new sign-in is needed here.

## Run

```bash
mkdir -p uploads/WO-12345
# Put PDFs or screenshots in that folder, then:
python run.py
python run.py --uploads /path/to/uploads --workers 4 --calendar-id primary
```

Supported files are PDF, PNG, JPG/JPEG, WEBP, TIFF, and BMP. The uploads path defaults to this project’s `uploads/` directory, even when you invoke `run.py` from another working directory. The project’s `.env` and runtime paths are also resolved from the script location.

Every job must have a readable date, earliest arrival, positive work duration, and a city in the editable table in `drive_estimates.py`. Missing optional information stays blank. A job that lacks required information is reported as an error and gets no Calendar event, Docs entry, Drive job folder, processed-file entry, or saved partial extraction. Other jobs continue, and the process exits with status 1 if any job fails.

Calendar times use `America/Phoenix`. The appointment starts at the earliest arrival minus the outbound drive estimate and ends at the earliest arrival plus the estimated onsite work duration. The description contains the arrival window and extracted work details. Travel home is outside the appointment.

## Files and recovery

| Location | Contents |
|---|---|
| Google Doc selected by `GOOGLE_DOC_ID` | Month/date sections, job details, a real Drive job-folder link, and blank After-Action Reviews |
| Drive folder selected by `GOOGLE_DRIVE_FOLDER_ID` | `City-Date-Store/` job folders containing original files and nested source folders |
| `local/destinations.md` | Private clickable links to the configured annual Google Doc and FieldNation Drive folder |
| `processed.md` | Upload-relative source names, added only after all destinations succeed |
| `runtime.yaml` | Timestamps, durations, safe request metadata, errors, validated checkpoints, fixed destination IDs, and pre-generated Drive IDs |

The FieldNation job folder uses `Unknown-Store` when no store abbreviation is available. Original uploads retain nested paths, and later photos remain untouched. The After-Action Review contains MOD, RE Name, Time on site, and Closing Notes. The Docs writer preserves existing document content, native headings, formatting, and human notes while inserting new jobs. The document also contains a clickable link to the main FieldNation folder.

Rerun the same command after an interruption. A validated checkpoint resumes unfinished destinations without another extraction call. Calendar uses a [stable client-supplied event ID](https://developers.google.com/workspace/calendar/api/guides/create-events) derived from the job’s upload-relative path. Docs records a named range with its insertion so a repeated write recognizes the job; an existing matching work-order label also avoids duplication. Drive IDs are saved in YAML before creation so an interrupted response can be recovered without uploading another copy. The Docs step waits for the Drive job-folder URL. A source is marked processed only after all three Google destinations succeed.

Keep job paths stable and treat completed uploads as immutable. Reusing a path represents the same Calendar event. A pending checkpoint is bound to its original calendar, document, and parent folder IDs; resume with those destinations. The bot is a command-line batch tool: run one instance at a time. Its lock coordinates worker threads within that instance.

Earlier local Markdown/FieldNation outputs are retained. Completed source records keep their completed status; this destination change does not backfill historical jobs. Pending validated checkpoints can finish the new cloud destinations while retaining completed Calendar work.

The drive estimates use Mesa Temple as the approximate origin. **Future agents must not automatically improve these estimates or add maps, routing, traffic, or address-based calculations.** A person can edit the fixed city table.

## Project files

`run.py` loads settings; `pipeline.py` connects the steps. Discovery, PDF/OCR extraction, Luna extraction, validation and drive estimates, Google authorization, Calendar writing, Docs insertion, Drive uploads, processed-source tracking, and runtime logging each have their own module. The earlier local Markdown/copy modules remain available as records of the original MVP implementation; the current pipeline writes to real Google destinations.

The approved specification is in `master-plan.md`, design choices are in `dev-decisions.md`, and actual verification results and outstanding setup are recorded in `dev-log.md`. The project’s three original files are preserved in `archive/`.
