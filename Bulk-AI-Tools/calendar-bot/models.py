"""Small shared records for one upload job and the event found inside it.

Discovery creates Jobs, then the extractors fill EventData. Keeping these
records in one place lets the later calendar and file writers share the same
plain description of a job.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Job:
    """The input files that belong together as one work order."""

    key: str
    files: tuple[Path, ...]
    source_names: tuple[str, ...]


@dataclass(frozen=True)
class EventData:
    """The calendar details extracted from a Job, with blanks for unknowns."""

    date: str
    earliest_arrival: str
    duration_minutes: int
    city: str
    latest_arrival: str = ""
    store: str = ""
    title: str = ""
    wo_number: str = ""
    address: str = ""
    buyer: str = ""
    contact: str = ""
    phone: str = ""
    pay: str = ""
    scope: str = ""
    instructions: str = ""
    deliverables: str = ""
    drive_minutes: int = 0
