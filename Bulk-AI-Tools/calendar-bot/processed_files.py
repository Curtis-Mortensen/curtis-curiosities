"""Remember which upload files have reached every destination.

The pipeline asks this file before starting work and adds source paths only
after Calendar, Markdown, and the copied-input folder are all complete.
"""

from pathlib import Path

from runtime_log import LOCK


def read_processed(path: Path) -> set[str]:
    """Return the saved upload-relative paths, or an empty set for a new run."""
    with LOCK:
        if not path.exists():
            return set()
        with path.open(encoding="utf-8") as processed_file:
            return {line.strip() for line in processed_file if line.strip()}


def add_processed(path: Path, source_names: tuple[str, ...]) -> None:
    """Add paths once, keeping the file easy for a person to read."""
    with LOCK:
        existing = read_processed(path)
        existing.update(source_names)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_name(path.name + ".tmp")
        temporary_path.write_text("".join(f"{name}\n" for name in sorted(existing)), encoding="utf-8")
        temporary_path.replace(path)
