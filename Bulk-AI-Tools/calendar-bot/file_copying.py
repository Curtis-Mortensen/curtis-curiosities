"""This file places a job's original pictures and documents in FieldNation.

The pipeline passes the discovered files and their upload-relative names.
This copy keeps folders inside a work order intact, so two files with the same
name do not replace each other; later job photos can be added beside them.
City and store names become safe single folder-name pieces before they are used
to build the destination path.
"""

from pathlib import Path
import re
import shutil


def copy_inputs(job, event, fieldnation_root: Path) -> str:
    """Copy original inputs into the city, date, and store folder."""
    store = event.store or "Unknown-Store"
    folder_name = f"{_slug(event.city or 'Unknown')}-{event.date}-{_slug(store)}"
    destination = Path(fieldnation_root) / folder_name
    key_parts = Path(job.key).parts

    for source, source_name in zip(job.files, job.source_names):
        relative = Path(source_name)
        # Grouped jobs use the work-order folder as their key. Remove that
        # outer folder while retaining any nested folders under it.
        if len(key_parts) and relative.parts[:len(key_parts)] == key_parts:
            relative = Path(*relative.parts[len(key_parts):])
        if not relative.parts or relative == Path("."):
            relative = Path(source).name
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return str(destination)


def _slug(value: str) -> str:
    words = re.sub(r"[\W_]+", "-", value.strip(), flags=re.UNICODE).strip("-")
    return words or "Unknown-Store"
