"""Keep a readable trail of each run for the people who use this bot.

The pipeline records its stages here, and this file also owns the lock that
keeps shared log and checkpoint changes from stepping on one another.
"""

from datetime import datetime, timezone
from pathlib import Path
import threading
import time

import yaml


# All shared output files use this one lock, so two jobs never write at once.
LOCK = threading.RLock()


def timestamp() -> str:
    """Return a sortable timestamp with an explicit UTC marker."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_state(path: Path) -> dict:
    """Read saved checkpoints and run notes, starting with an empty notebook."""
    if not path.exists():
        return {"checkpoints": {}, "logs": []}
    with path.open(encoding="utf-8") as state_file:
        return yaml.safe_load(state_file) or {"checkpoints": {}, "logs": []}


def write_state(path: Path, state: dict) -> None:
    """Replace the whole YAML notebook safely after a complete write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(path.name + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as state_file:
        yaml.safe_dump(state, state_file, sort_keys=False, allow_unicode=True)
    temporary_path.replace(path)


def record(path: Path, job_key: str, stage: str, status: str, **details) -> None:
    """Add one small stage note without storing extracted text or secrets."""
    with LOCK:
        state = read_state(path)
        logs = state.setdefault("logs", [])
        logs.append({
            "time": timestamp(),
            "job": job_key,
            "stage": stage,
            "status": status,
            **details,
        })
        write_state(path, state)


def start(path: Path, job_key: str, stage: str, **details) -> float:
    """Write a stage-start marker and return the clock value for its duration."""
    record(path, job_key, stage, "started", **details)
    return time.monotonic()


def finish(path: Path, job_key: str, stage: str, began: float, status: str = "completed", **details) -> None:
    """Write a stage-finish marker with the time spent in that stage."""
    record(path, job_key, stage, status, duration_seconds=round(time.monotonic() - began, 3), **details)
