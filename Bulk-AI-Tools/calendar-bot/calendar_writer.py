"""This file turns one finished job into a Google Calendar appointment.

The run pipeline gives it a complete EventData record and a stable job key.
Google sign-in stays in google_auth.py, while this file handles the event's
arrival window, travel time, details, and safe repeat writes. An unknown end
time stays blank in the details instead of looking like a dangling range.
"""

import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from googleapiclient.errors import HttpError

from google_auth import get_calendar_service


TIME_ZONE = "America/Phoenix"


class CalendarWriter:
    """Create or find the one calendar event belonging to a job."""

    def __init__(self, credentials_path: Path, token_path: Path):
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        self._service = None

    @property
    def service(self):
        # Authentication waits until a valid job is ready for this destination.
        if self._service is None:
            self._service = get_calendar_service(self.credentials_path, self.token_path)
        return self._service

    def write(self, event, job_key: str, calendar_id: str) -> dict:
        event_id = "cb" + hashlib.sha256(job_key.encode("utf-8")).hexdigest()
        local_zone = ZoneInfo(TIME_ZONE)
        arrival = datetime.fromisoformat(f"{event.date}T{event.earliest_arrival}").replace(tzinfo=local_zone)
        start = arrival - timedelta(minutes=event.drive_minutes)
        end = arrival + timedelta(minutes=event.duration_minutes)
        body = {
            "id": event_id,
            "summary": event.title or f"{event.city} work order {event.wo_number}".strip(),
            "location": event.address,
            "description": _description(event),
            "start": {"dateTime": start.isoformat(), "timeZone": TIME_ZONE},
            "end": {"dateTime": end.isoformat(), "timeZone": TIME_ZONE},
        }
        try:
            saved = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        except HttpError as error:
            if error.resp.status != 404:
                raise
            try:
                saved = self.service.events().insert(calendarId=calendar_id, body=body).execute()
            except HttpError as insert_error:
                if insert_error.resp.status != 409:
                    raise
                # The same stable ID may have been created between the lookup
                # and insert; read that event so a rerun returns its real link.
                saved = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        return {"id": saved["id"], "url": saved.get("htmlLink", ""), "calendar_id": calendar_id}


def _description(event) -> str:
    lines = [
        f"Arrival window: {_arrival_window(event)}",
        f"Estimated work: {event.duration_minutes} minutes",
        f"Estimated drive from Mesa Temple: {event.drive_minutes} minutes",
        f"City: {event.city}",
    ]
    for label, value in (
        ("Store", event.store), ("Work order", event.wo_number), ("Address", event.address),
        ("Buyer", event.buyer), ("Contact", event.contact), ("Phone", event.phone),
        ("Pay", event.pay), ("Scope", event.scope), ("Instructions", event.instructions),
        ("Deliverables", event.deliverables),
    ):
        if value:
            lines.append(f"{label}: {value}")
    return "\n".join(lines)


def _arrival_window(event) -> str:
    if event.latest_arrival:
        return f"{event.earliest_arrival}–{event.latest_arrival}"
    return event.earliest_arrival
