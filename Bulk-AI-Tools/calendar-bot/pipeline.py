"""Connect the small Calendar Bot steps into one resumable job pipeline.

Discovery supplies jobs, extraction fills in their event details, and the
Calendar, Drive, and Docs writers save a validated event. A YAML notebook lets
a later run pick up at the first unfinished cloud destination.
"""

from dataclasses import asdict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from calendar_writer import CalendarWriter
from discovery import discover_jobs
from docs_writer import GoogleDocsWriter
from drive_estimates import validate_event
from drive_writer import GoogleDriveWriter
from luna_extraction import extract_event
from models import EventData, Job
from processed_files import add_processed, read_processed
from runtime_log import LOCK, finish, read_state, record, start, write_state
from text_extraction import extract_text


MODEL = "gpt-6-luna"
DESTINATIONS = ("calendar", "drive", "docs")


def _checkpoint(runtime_path: Path, job: Job) -> dict | None:
    """Find this job's saved work while holding the shared-file lock."""
    with LOCK:
        return read_state(runtime_path).get("checkpoints", {}).get(job.key)


def _save_checkpoint(runtime_path: Path, job: Job, checkpoint: dict) -> None:
    """Save complete event data and destination progress in the YAML notebook."""
    with LOCK:
        state = read_state(runtime_path)
        state.setdefault("checkpoints", {})[job.key] = checkpoint
        write_state(runtime_path, state)


def safe_error_summary(error: Exception, stage: str = "pipeline") -> str:
    """Give a useful failure hint without copying provider text into logs."""
    error_type = type(error).__name__

    # This exact message comes from our local event validator, so it names the
    # missing work-order detail without exposing anything sent to a provider.
    if stage == "validation" and type(error) is ValueError:
        detail = str(error)
    # The OAuth helper's message is written by this project and tells the user
    # how to finish sign-in. Other RuntimeErrors may contain provider text.
    elif error_type == "RuntimeError" and str(error).startswith((
        "Google sign-in is required.", "Google Calendar sign-in is required."
    )):
        detail = str(error)
    else:
        status = getattr(error, "status_code", None)
        response = getattr(error, "resp", None)
        if status is None and response is not None:
            status = getattr(response, "status", None)
        if status in (401, 403):
            detail = f"authorization was rejected (HTTP {status})"
        elif status == 404:
            detail = "the requested resource was not found (HTTP 404)"
        elif status == 429:
            detail = "the service rate limit was reached (HTTP 429)"
        elif isinstance(status, int) and status >= 500:
            detail = f"the service is temporarily unavailable (HTTP {status})"
        else:
            detail = f"{error_type}: details were omitted to protect credentials"
    return f"{stage}: {detail}"


def _run_destination(name: str, job: Job, event: EventData, calendar: CalendarWriter,
                     drive: GoogleDriveWriter, docs: GoogleDocsWriter, calendar_id: str,
                     document_id: str, drive_folder_id: str, drive_folder_url: str) -> dict:
    """Perform one destination while holding the common output lock."""
    with LOCK:
        if name == "calendar":
            return calendar.write(event, job.key, calendar_id)
        if name == "drive":
            return drive.write(job, event, drive_folder_id)
        return docs.write(event, job.key, document_id, drive_folder_url)


def process_job(job: Job, runtime_path: Path, processed_path: Path,
                calendar: CalendarWriter, drive: GoogleDriveWriter, docs: GoogleDocsWriter,
                calendar_id: str, document_id: str,
                drive_folder_id: str) -> tuple[bool, str | None]:
    """Process one job, returning false if any required step still needs work."""
    source_names = job.source_names
    processed = read_processed(processed_path)
    if all(name in processed for name in source_names):
        record(runtime_path, job.key, "job", "skipped", reason="all_sources_processed", sources=list(source_names))
        return True, None

    checkpoint = _checkpoint(runtime_path, job)
    if checkpoint and checkpoint.get("sources") != list(source_names):
        checkpoint = None
    if checkpoint and checkpoint.get("event"):
        requested_targets = {
            "calendar_id": calendar_id,
            "document_id": document_id,
            "drive_folder_id": drive_folder_id,
        }
        changed_targets = {
            name: {"saved": checkpoint.get(name, value), "requested": value}
            for name, value in requested_targets.items()
            if checkpoint.get(name, value) != value
        }
        if changed_targets:
            record(runtime_path, job.key, "job", "error", error="checkpoint_target_mismatch",
                   changed_targets=changed_targets)
            return False, "checkpoint belongs to different Google destinations; use the original target IDs to resume"
        # Older pending work only knew Calendar and local destinations. Keep its
        # validated event and Calendar result, then add the new cloud targets.
        for name, value in requested_targets.items():
            checkpoint.setdefault(name, value)
        destinations = checkpoint.setdefault("destinations", {})
        for name in DESTINATIONS:
            destinations.setdefault(name, {"done": False})
        _save_checkpoint(runtime_path, job, checkpoint)

    if not checkpoint or not checkpoint.get("event"):
        stage = "text_extraction"
        try:
            began = start(runtime_path, job.key, "text_extraction", sources=list(source_names))
            try:
                text = extract_text(job)
            except Exception:
                finish(runtime_path, job.key, "text_extraction", began, status="error")
                raise
            finish(runtime_path, job.key, "text_extraction", began)

            stage = "luna_extraction"
            began = start(runtime_path, job.key, "luna_extraction", model=MODEL, reasoning_effort="high",
                          response_format="structured_json", sources=list(source_names))
            try:
                event, metadata = extract_event(text, source_names)
            except Exception:
                finish(runtime_path, job.key, "luna_extraction", began, status="error", model=MODEL)
                raise
            finish(runtime_path, job.key, "luna_extraction", began, model=MODEL, request_metadata=metadata)

            stage = "validation"
            began = start(runtime_path, job.key, "validation")
            try:
                event = validate_event(event)
            except Exception:
                finish(runtime_path, job.key, "validation", began, status="error")
                raise
            finish(runtime_path, job.key, "validation", began, city=event.city, drive_minutes=event.drive_minutes)
            stage = "checkpoint"
            checkpoint = {
                "sources": list(source_names),
                "calendar_id": calendar_id,
                "document_id": document_id,
                "drive_folder_id": drive_folder_id,
                "event": asdict(event),
                "destinations": {name: {"done": False} for name in DESTINATIONS},
                "error": None,
            }
            _save_checkpoint(runtime_path, job, checkpoint)
        except Exception as error:
            summary = safe_error_summary(error, stage)
            record(runtime_path, job.key, "job", "error", sources=list(source_names), error=summary)
            return False, summary

    event = EventData(**checkpoint["event"])
    succeeded = True
    last_error = None
    for name in DESTINATIONS:
        destination = checkpoint.setdefault("destinations", {}).setdefault(name, {"done": False})
        if destination.get("done"):
            continue
        if name == "docs" and not checkpoint["destinations"]["drive"].get("done"):
            drive_error = checkpoint["destinations"]["drive"].get("error", "Drive has not created a job folder yet")
            reason = f"docs: waiting for the Drive folder; {drive_error}"
            destination["error"] = reason
            _save_checkpoint(runtime_path, job, checkpoint)
            succeeded = False
            last_error = reason
            began = start(runtime_path, job.key, "docs", document_id=document_id)
            finish(runtime_path, job.key, "docs", began, status="skipped", reason=reason)
            continue
        details = {"calendar_id": calendar_id} if name == "calendar" else (
            {"drive_folder_id": drive_folder_id} if name == "drive" else {"document_id": document_id}
        )
        began = start(runtime_path, job.key, name, **details)
        try:
            drive_folder_url = checkpoint["destinations"]["drive"]["output"]["url"] if name == "docs" else ""
            output = _run_destination(name, job, event, calendar, drive, docs, calendar_id,
                                      document_id, drive_folder_id, drive_folder_url)
            destination.update({"done": True, "output": output})
            destination.pop("error", None)
            _save_checkpoint(runtime_path, job, checkpoint)
            finish(runtime_path, job.key, name, began, output=output, calendar_id=calendar_id if name == "calendar" else None)
        except Exception as error:
            succeeded = False
            destination["error"] = safe_error_summary(error, name)
            last_error = destination["error"]
            _save_checkpoint(runtime_path, job, checkpoint)
            finish(runtime_path, job.key, name, began, status="error", error=destination["error"])

    if succeeded and all(checkpoint["destinations"][name].get("done") for name in DESTINATIONS):
        add_processed(processed_path, source_names)
        checkpoint["processed"] = True
        _save_checkpoint(runtime_path, job, checkpoint)
        record(runtime_path, job.key, "job", "completed", sources=list(source_names))
        return True, None
    record(runtime_path, job.key, "job", "incomplete", sources=list(source_names))
    return False, last_error or "pipeline: one or more destinations remain incomplete"


def run_pipeline(uploads: Path, workers: int, calendar_id: str, document_id: str,
                 drive_folder_id: str, project: Path) -> int:
    """Discover jobs and let a fixed pool of workers process them together."""
    uploads.mkdir(parents=True, exist_ok=True)
    runtime_path = project / "runtime.yaml"
    processed_path = project / "processed.md"

    began = start(runtime_path, "", "discovery", uploads=str(uploads))
    try:
        jobs = discover_jobs(uploads)
    except Exception as error:
        finish(runtime_path, "", "discovery", began, status="error")
        summary = safe_error_summary(error, "discovery")
        record(runtime_path, "", "run", "error", uploads=str(uploads), error=summary)
        raise
    finish(runtime_path, "", "discovery", began, jobs=len(jobs))
    if not jobs:
        record(runtime_path, "", "run", "completed", jobs=0, uploads=str(uploads))
        print(f"No upload jobs found in {uploads}")
        return 0

    # The writers keep OAuth setup lazy so an empty or fully skipped run needs no login.
    calendar = CalendarWriter(project / "credentials.json", project / "token.json")
    drive = GoogleDriveWriter(project / "credentials.json", project / "token.json")
    docs = GoogleDocsWriter(project / "credentials.json", project / "token.json")
    failures = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(process_job, job, runtime_path, processed_path, calendar, drive, docs,
                        calendar_id, document_id, drive_folder_id): job
            for job in jobs
        }
        for future in as_completed(futures):
            job = futures[future]
            try:
                succeeded, error_detail = future.result()
                if not succeeded:
                    failures += 1
                    print(f"Failed: {job.key} — {error_detail}")
                else:
                    print(f"Done: {job.key}")
            except Exception as error:
                failures += 1
                error_detail = safe_error_summary(error, "job worker")
                record(runtime_path, job.key, "job", "error", error=error_detail)
                print(f"Failed: {job.key} — {error_detail}")
    record(runtime_path, "", "run", "completed" if not failures else "error",
           jobs=len(jobs), failures=failures, uploads=str(uploads), calendar_id=calendar_id,
           document_id=document_id, drive_folder_id=drive_folder_id)
    return 1 if failures else 0
