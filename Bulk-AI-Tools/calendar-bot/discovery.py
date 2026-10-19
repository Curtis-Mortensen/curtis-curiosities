"""Find the supported files a person dropped into the uploads folder.

Each first-level folder is one work order and may contain nested files. A file
placed directly in uploads is its own work order. The returned source names
stay relative to uploads so later logs can identify the original inputs.
"""

from pathlib import Path

from models import Job


SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp"}


def discover_jobs(uploads: Path) -> list[Job]:
    """Return supported loose files and populated immediate folders in order."""
    jobs: list[Job] = []

    for entry in sorted(uploads.iterdir(), key=lambda path: path.name.casefold()):
        if entry.is_dir():
            files = tuple(
                path
                for path in sorted(entry.rglob("*"), key=lambda path: path.as_posix().casefold())
                if path.is_file() and path.suffix.casefold() in SUPPORTED_EXTENSIONS
            )
            if files:
                names = tuple(path.relative_to(uploads).as_posix() for path in files)
                jobs.append(Job(key=entry.relative_to(uploads).as_posix(), files=files, source_names=names))
        elif entry.is_file() and entry.suffix.casefold() in SUPPORTED_EXTENSIONS:
            name = entry.relative_to(uploads).as_posix()
            jobs.append(Job(key=name, files=(entry,), source_names=(name,)))

    return jobs
