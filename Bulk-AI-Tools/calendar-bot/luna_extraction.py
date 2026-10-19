"""Ask Luna to turn extracted work-order text into one strict event record.

The response is constrained by a JSON schema that matches EventData. Only
request identifiers and token usage are returned as metadata; job text and
credentials are not copied into logs by this module. The response ID tracks
the saved answer, while the request ID identifies the API call itself.
"""

import json

from openai import OpenAI

from models import EventData


EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": "string", "description": "Work date as YYYY-MM-DD, or blank if unknown."},
        "earliest_arrival": {"type": "string", "description": "Earliest arrival as 24-hour HH:MM, or blank if unknown."},
        "latest_arrival": {"type": "string", "description": "Latest arrival as 24-hour HH:MM, or blank if absent."},
        "duration_minutes": {"type": "integer", "description": "Estimated onsite work duration in minutes, or 0 if unknown."},
        "city": {"type": "string", "description": "Work city."},
        "store": {"type": "string"},
        "title": {"type": "string"},
        "wo_number": {"type": "string"},
        "address": {"type": "string"},
        "buyer": {"type": "string"},
        "contact": {"type": "string"},
        "phone": {"type": "string"},
        "pay": {"type": "string"},
        "scope": {"type": "string"},
        "instructions": {"type": "string"},
        "deliverables": {"type": "string"},
    },
    "required": [
        "date", "earliest_arrival", "latest_arrival", "duration_minutes", "city",
        "store", "title", "wo_number", "address", "buyer", "contact", "phone",
        "pay", "scope", "instructions", "deliverables",
    ],
    "additionalProperties": False,
}


def extract_event(text: str, source_names: tuple[str, ...]) -> tuple[EventData, dict]:
    """Extract event fields using Luna and return safe request/usage details."""
    client = OpenAI()
    response = client.responses.create(
        model="gpt-6-luna",
        reasoning={"effort": "high"},
        input=[
            {
                "role": "system",
                "content": (
                    "Extract one field-service work order into the requested JSON. "
                    "Use only details supported by the source text. Return blank strings "
                    "for missing optional information, 0 for a missing duration, and use "
                    "YYYY-MM-DD and 24-hour HH:MM formats. Only return a date when its "
                    "year is supported by the source text; do not fill in a missing year. "
                    "Convert stated work duration to whole minutes. Do not guess a city "
                    "or appointment time."
                ),
            },
            {
                "role": "user",
                "content": f"Source files: {', '.join(source_names)}\n\nWork order text:\n{text}",
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "calendar_event",
                "strict": True,
                "schema": EVENT_SCHEMA,
            }
        },
    )
    values = json.loads(response.output_text)
    event = EventData(**values)
    usage = response.usage.model_dump(mode="json") if response.usage else None
    metadata = {
        "model": response.model,
        "response_id": response.id,
        "request_id": response._request_id,
        "usage": usage,
    }
    return event, metadata
