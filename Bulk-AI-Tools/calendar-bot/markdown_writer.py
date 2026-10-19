"""This file adds completed work orders to the local Markdown calendar.

It owns only the readable calendar page; the pipeline supplies a complete
EventData record and job key. Hidden markers let reruns recognize a job while
leaving any notes people wrote around it untouched. It builds each update in a
nearby temporary file, then switches the finished page into place at once.
"""

from datetime import date as Date, datetime
import os
from pathlib import Path
import re
import tempfile


def write_markdown(path: Path, event, job_key: str) -> str:
    """Add a job in date and arrival order, then return the page path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.exists() else "# Work Orders\n"
    marker = _marker(event, job_key)
    if f"<!-- calendar-bot-job: {marker} -->" in text:
        return str(path)

    block = _job_block(event, marker)
    month_title = Date.fromisoformat(event.date).strftime("%B %Y")
    month_heading = f"## {month_title}"
    date_heading = f"### {event.date} ({Date.fromisoformat(event.date).strftime('%A')})"
    lines = text.splitlines()

    month_index = _heading_index(lines, "## ", month_title)
    if month_index is None:
        month_start = _insert_month(lines, month_heading, month_title)
        lines = month_start
        month_index = _heading_index(lines, "## ", month_title)
    date_index = _heading_index(lines, "### ", date_heading[4:])
    month_end = _next_heading(lines, month_index + 1, ("## ",))
    if date_index is None or date_index >= month_end:
        insert_at = month_end
        for index in range(month_index + 1, month_end):
            match = re.match(r"### (\d{4}-\d{2}-\d{2})", lines[index])
            if match and match.group(1) > event.date:
                insert_at = index
                break
        date_lines = [date_heading, "", *block, ""]
        lines[insert_at:insert_at] = date_lines
    else:
        section_end = _next_heading(lines, date_index + 1, ("## ", "### "))
        # Compare only jobs with our markers. Human notes remain in place.
        insert_at = section_end
        for index in range(date_index + 1, section_end):
            found = re.match(r"<!-- calendar-bot-job: (\d{4}-\d{2}-\d{2})\|(\d{2}:\d{2})\|(.*) -->", lines[index])
            if found and (found.group(2), found.group(3)) > (event.earliest_arrival, job_key):
                insert_at = index
                break
        if insert_at == section_end:
            # Append after the last marked job, before trailing human notes.
            for index in range(section_end - 1, date_index, -1):
                if lines[index] == "<!-- /calendar-bot-job -->":
                    insert_at = index + 1
                    break
            if insert_at == section_end:
                insert_at = date_index + 1
                while insert_at < section_end and not lines[insert_at].strip():
                    insert_at += 1
        lines[insert_at:insert_at] = ["", *block, ""]

    _replace_text_atomically(path, "\n".join(lines).rstrip() + "\n")
    return str(path)


def _marker(event, job_key: str) -> str:
    return f"{event.date}|{event.earliest_arrival}|{job_key}"


def _job_block(event, marker: str) -> list[str]:
    title = event.title or "Work order"
    if event.wo_number:
        title = f"{title} (WO {event.wo_number})"
    rows = [
        f"<!-- calendar-bot-job: {marker} -->",
        f"**{title}**",
        "",
        f"- Arrival: {_arrival_window(event)}",
        f"- Duration: {event.duration_minutes} minutes",
        f"- City: {event.city}",
    ]
    for label, value in (
        ("Store", event.store), ("Address", event.address), ("Buyer", event.buyer),
        ("Contact", event.contact), ("Phone", event.phone), ("Pay", event.pay),
        ("Scope", event.scope), ("Instructions", event.instructions), ("Deliverables", event.deliverables),
    ):
        if value:
            rows.append(f"- {label}: {value}")
    rows.extend([
        "", "**After-Action Review**", "", "- MOD:", "- RE Name:",
        "- Time on site:", "- Closing Notes:", "<!-- /calendar-bot-job -->",
    ])
    return rows


def _heading_index(lines: list[str], prefix: str, title: str):
    for index, line in enumerate(lines):
        if line.startswith(prefix) and line[len(prefix):] == title:
            return index
    return None


def _next_heading(lines: list[str], start: int, prefixes: tuple[str, ...]) -> int:
    for index in range(start, len(lines)):
        if lines[index].startswith(prefixes):
            return index
    return len(lines)


def _insert_month(lines: list[str], heading: str, title: str) -> list[str]:
    target = datetime.strptime(title, "%B %Y").strftime("%Y-%m")
    position = len(lines)
    for index, line in enumerate(lines):
        if line.startswith("## "):
            try:
                existing = datetime.strptime(line[3:], "%B %Y").strftime("%Y-%m")
            except ValueError:
                continue
            if existing > target:
                position = index
                break
    lines[position:position] = ["", heading, ""]
    return lines


def _arrival_window(event) -> str:
    if event.latest_arrival:
        return f"{event.earliest_arrival}–{event.latest_arrival}"
    return event.earliest_arrival


def _replace_text_atomically(path: Path, content: str) -> None:
    """Write beside the page first, then switch it in one filesystem step."""
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
