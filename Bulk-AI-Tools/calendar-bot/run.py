"""Offer a simple command line for the Calendar Bot pipeline.

This file loads private Google destination IDs and command-line choices, then
hands the work to pipeline.py so each upload can be processed by its own thread.
"""

import argparse
import os
from pathlib import Path
import sys

from dotenv import load_dotenv

from pipeline import run_pipeline, safe_error_summary


PROJECT = Path(__file__).resolve().parent


def main() -> int:
    """Read the user's choices and start the threaded upload pipeline."""
    load_dotenv(PROJECT / ".env")
    parser = argparse.ArgumentParser(description="Turn uploaded work orders into Calendar events, Drive folders, and Google Docs notes.")
    parser.add_argument("--uploads", type=Path, default=PROJECT / "uploads", help="Folder containing PDFs and screenshots")
    parser.add_argument("--workers", type=int, default=4, help="Number of jobs to process at once")
    parser.add_argument("--calendar-id", default=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
                        help="Google Calendar ID (defaults to GOOGLE_CALENDAR_ID or primary)")
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be at least 1")
    document_id = os.getenv("GOOGLE_DOC_ID", "").strip()
    drive_folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "").strip()
    if not document_id:
        parser.error("Set GOOGLE_DOC_ID in the private .env file; copy .env.example and add the Google Doc ID.")
    if not drive_folder_id:
        parser.error("Set GOOGLE_DRIVE_FOLDER_ID in the private .env file; copy .env.example and add the parent Drive folder ID.")
    try:
        return run_pipeline(args.uploads.expanduser().resolve(), args.workers, args.calendar_id,
                            document_id, drive_folder_id, PROJECT)
    except Exception as error:
        print(f"Calendar Bot could not start: {safe_error_summary(error, 'startup')}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
