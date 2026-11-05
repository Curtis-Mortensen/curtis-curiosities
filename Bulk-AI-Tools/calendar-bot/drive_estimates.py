"""Validate required event details and add the approved Mesa-area drive time.

The estimate table is intentionally editable by a person. Mesa Temple is the
approximate origin. Future changes must not automatically improve these
estimates or add maps, routing, traffic, or address-based calculations.
"""

from dataclasses import replace
from datetime import datetime

from models import EventData


# Times are rough fixed estimates from Mesa Temple, in minutes.
DRIVE_MINUTES = {
    "Mesa": 15,
    "Gilbert": 30,
    "Apache Junction": 30,
    "Tempe": 30,
    "Chandler": 45,
    "Scottsdale": 45,
    "Phoenix": 45,
    "Gold Canyon": 45,
    "Queen Creek": 45,
    "Fountain Hills": 45,
    "Surprise": 60,
    "Glendale": 60,
    "Peoria": 60,
    "Goodyear": 60,
    "Avondale": 60,
    "Buckeye": 60,
    "San Tan Valley": 60,
    "Maricopa": 60,
    "Casa Grande": 75,
    "Payson": 90,
    "Tucson": 120,
    "Prescott": 120,
    "Sedona": 120,
    "Flagstaff": 150,
    "Show Low": 180,
    "Pinetop-Lakeside": 180,
}

_CITY_NAMES = {city.casefold(): city for city in DRIVE_MINUTES}


def validate_event(event: EventData) -> EventData:
    """Check required fields, standardize date/time/city, and attach drive time."""
    date_text = event.date.strip()
    if not date_text:
        raise ValueError("Work date is required in YYYY-MM-DD format")
    try:
        parsed_date = datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError as error:
        raise ValueError("Work date must use YYYY-MM-DD format") from error
    if parsed_date.isoformat() != date_text:
        raise ValueError("Work date must use YYYY-MM-DD format")
    normalized_date = parsed_date.isoformat()

    arrival_text = event.earliest_arrival.strip()
    if not arrival_text:
        raise ValueError("Earliest arrival time is required in HH:MM format")
    try:
        earliest = datetime.strptime(arrival_text, "%H:%M").strftime("%H:%M")
    except ValueError as error:
        raise ValueError("Earliest arrival time must use 24-hour HH:MM format") from error
    latest = event.latest_arrival.strip()
    if latest:
        try:
            latest = datetime.strptime(latest, "%H:%M").strftime("%H:%M")
        except ValueError as error:
            raise ValueError("Latest arrival time must use 24-hour HH:MM format") from error
    city = _CITY_NAMES.get(event.city.strip().casefold())
    if city is None:
        raise ValueError(f"City is missing or has no approved drive estimate: {event.city!r}")
    if event.duration_minutes <= 0:
        raise ValueError("Work duration must be a positive number of minutes")
    return replace(
        event,
        date=normalized_date,
        earliest_arrival=earliest,
        latest_arrival=latest,
        city=city,
        drive_minutes=DRIVE_MINUTES[city],
    )
