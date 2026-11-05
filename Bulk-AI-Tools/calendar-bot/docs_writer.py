"""Add a finished work order to the shared Google Docs calendar.

The pipeline gives this file one complete event and the link to its
FieldNation folder. This writer reads the existing document so it can add the
job in the right date section without replacing headings, notes, or formatting
that a person already put there.
"""

from datetime import date as Date, datetime
import hashlib
import re

from google_auth import get_google_service


class GoogleDocsWriter:
    """Insert one stable, linked work-order block into an existing Doc."""

    def __init__(self, credentials_path, token_path):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self._service = None

    @property
    def service(self):
        # Wait for sign-in until the pipeline has a valid job to write.
        if self._service is None:
            self._service = get_google_service(
                "docs", "v1", self.credentials_path, self.token_path
            )
        return self._service

    def write(self, event, job_key: str, document_id: str, folder_url: str) -> dict:
        """Insert a formatted job unless its marker or exact WO is already present."""
        document = self.service.documents().get(
            documentId=document_id, includeTabsContent=True
        ).execute()
        tab_id, content, named_ranges = _tab_content(document)
        paragraphs = _paragraphs(content)
        marker_name = _marker_name(job_key)

        if marker_name in named_ranges:
            return _result(document_id, marker_name, "already_written")

        if event.wo_number and _contains_work_order(paragraphs, event.wo_number):
            return _result(document_id, marker_name, "work_order_already_present")

        insertion = _insertion_plan(paragraphs, event)
        text, title_range, review_range, link_range = _job_text(event, folder_url)
        if insertion["prefix"]:
            text = insertion["prefix"] + text
            title_range = _shift_range(title_range, insertion["prefix"])
            review_range = _shift_range(review_range, insertion["prefix"])
            link_range = _shift_range(link_range, insertion["prefix"])

        index = insertion["index"]
        total = _utf16_length(text)
        requests = [{
            "insertText": {
                "location": {"index": index, "tabId": tab_id},
                "text": text,
            }
        }]

        # Text inserted beside a heading or a link can copy its style. Give the
        # new work-order paragraphs their own plain-text style before applying
        # the two bold labels and the one folder link below.
        body_start = _utf16_length(insertion["prefix"])
        requests.append({
            "updateParagraphStyle": {
                "range": {
                    "startIndex": index + body_start,
                    "endIndex": index + total,
                    "tabId": tab_id,
                },
                "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                "fields": "namedStyleType",
            }
        })
        requests.append({
            "updateTextStyle": {
                "range": {
                    "startIndex": index + body_start,
                    "endIndex": index + total,
                    "tabId": tab_id,
                },
                "textStyle": {"bold": False},
                "fields": "bold,link",
            }
        })

        for start, end, style in insertion["heading_ranges"]:
            requests.append({
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": index + start,
                        "endIndex": index + end,
                        "tabId": tab_id,
                    },
                    "paragraphStyle": {"namedStyleType": style},
                    "fields": "namedStyleType",
                }
            })

        requests.extend([
            _bold_request(index, tab_id, title_range),
            _bold_request(index, tab_id, review_range),
            {
                "updateTextStyle": {
                    "range": {
                        "startIndex": index + link_range[0],
                        "endIndex": index + link_range[1],
                        "tabId": tab_id,
                    },
                    "textStyle": {"link": {"url": folder_url}},
                    "fields": "link",
                }
            },
            {
                "createNamedRange": {
                    "name": marker_name,
                    "range": {
                        "startIndex": index,
                        "endIndex": index + total,
                        "tabId": tab_id,
                    },
                }
            },
        ])
        response = self.service.documents().batchUpdate(
            documentId=document_id,
            body={
                "requests": requests,
                "writeControl": {"requiredRevisionId": document["revisionId"]},
            },
        ).execute()
        return _result(document_id, marker_name, "inserted", response)


def _result(document_id, marker_name, status, response=None):
    marker_id = ""
    if response:
        marker_id = response.get("replies", [{}])[-1].get("createNamedRange", {}).get("namedRangeId", "")
    return {
        "document_id": document_id,
        "url": f"https://docs.google.com/document/d/{document_id}/edit",
        "status": status,
        "marker": marker_name,
        "named_range_id": marker_id,
    }


def _tab_content(document):
    """Read the first tab body while keeping its native tab identifier."""
    tab = document["tabs"][0]
    tab_document = tab["documentTab"]
    return (tab["tabProperties"]["tabId"], tab_document["body"]["content"],
            tab_document.get("namedRanges", {}))


def _paragraphs(content):
    """Collect paragraph text and Docs' UTF-16 positions without flattening the Doc."""
    result = []
    for element in content:
        paragraph = element.get("paragraph")
        if not paragraph:
            continue
        text = "".join(
            item.get("textRun", {}).get("content", "")
            for item in paragraph.get("elements", [])
        )
        result.append({
            "start": element["startIndex"],
            "end": element["endIndex"],
            "text": text,
            "style": paragraph.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT"),
            "bold": any(
                item.get("textRun", {}).get("textStyle", {}).get("bold")
                for item in paragraph.get("elements", [])
            ),
        })
    return result


def _marker_name(job_key):
    return "CalendarBot_" + hashlib.sha256(job_key.encode("utf-8")).hexdigest()


def _contains_work_order(paragraphs, number):
    """Match either common label while keeping longer work-order numbers distinct."""
    number = re.sub(
        r"^\s*(?:WO|WORK\s+ORDER)\s*(?:number\s*)?(?:#\s*)?[:\-]?\s*",
        "", number, flags=re.IGNORECASE,
    )
    label = re.compile(
        r"\b(?:WO|WORK\s+ORDER)\s*(?:number\s*)?(?:#\s*)?[:\-]?\s*"
        + re.escape(number) + r"(?![A-Za-z0-9])",
        re.IGNORECASE,
    )
    return any(label.search(paragraph["text"]) for paragraph in paragraphs)


def _insertion_plan(paragraphs, event):
    """Find an existing date section or add missing month/date headings in order."""
    target_date = Date.fromisoformat(event.date.strip())
    month_text = target_date.strftime("%B")
    date_text = target_date.strftime("%A, %-d %B, %Y")
    month_index = _matching_month_index(paragraphs, target_date)

    if month_index is None:
        at = len(paragraphs)
        for i, paragraph in enumerate(paragraphs):
            existing_month = _month_key(paragraphs, i) if paragraph["style"] == "HEADING_1" else None
            if existing_month and existing_month > target_date.strftime("%Y-%m"):
                at = i
                break
        index = min(paragraphs[at]["start"] if at < len(paragraphs) else _document_end(paragraphs),
                    _document_end(paragraphs))
        prefix = month_text + "\n" + date_text + "\n"
        return {
            "index": index, "prefix": prefix,
            "heading_ranges": [
                (0, _utf16_length(month_text + "\n"), "HEADING_1"),
                (_utf16_length(month_text + "\n"), _utf16_length(prefix), "HEADING_2"),
            ],
        }

    month_end = next((i for i in range(month_index + 1, len(paragraphs))
                      if paragraphs[i]["style"] == "HEADING_1"), len(paragraphs))
    date_index = next((i for i in range(month_index + 1, month_end)
                       if paragraphs[i]["style"] == "HEADING_2"
                       and _date_from_text(paragraphs[i]["text"]) == target_date), None)
    if date_index is not None:
        section_end = next((i for i in range(date_index + 1, month_end)
                            if paragraphs[i]["style"] == "HEADING_2"), month_end)
        return {
            "index": _arrival_insertion_index(paragraphs, date_index, section_end, event),
            "prefix": "", "heading_ranges": [],
        }

    at = month_end
    for i in range(month_index + 1, month_end):
        existing_date = _date_from_text(paragraphs[i]["text"])
        if existing_date and existing_date >= target_date:
            at = i
            break
    index = min(paragraphs[at]["start"] if at < len(paragraphs) else _document_end(paragraphs),
                _document_end(paragraphs))
    prefix = date_text + "\n"
    return {
        "index": index, "prefix": prefix,
        "heading_ranges": [(0, _utf16_length(prefix), "HEADING_2")],
    }


def _arrival_insertion_index(paragraphs, start, end, event):
    """Place the job before a later timed title when the old entries expose times."""
    wanted = _time_minutes(event.earliest_arrival)
    target_date = Date.fromisoformat(event.date)
    # Some older entries carry their date in the title instead of a Heading 2.
    # Treat the first different dated title as the end of this day's section.
    next_dated_title = next((i for i in range(start + 1, end)
                             if _date_from_text(paragraphs[i]["text"])
                             and _date_from_text(paragraphs[i]["text"]) != target_date), end)
    section_end = min(end, next_dated_title)
    title_indices = [i for i in range(start + 1, section_end)
                     if _is_job_title(paragraphs, i, section_end)]
    for position, title_index in enumerate(title_indices):
        following = title_indices[position + 1] if position + 1 < len(title_indices) else section_end
        title_date = _date_from_text(paragraphs[title_index]["text"])
        if title_date and title_date != target_date:
            continue
        arrival = _arrival_for_entry(paragraphs, title_index, following)
        if arrival is not None and arrival > wanted:
            return paragraphs[title_index]["start"]
    if section_end < end:
        return paragraphs[section_end]["start"]
    if section_end > start + 1:
        return min(paragraphs[section_end - 1]["end"], _document_end(paragraphs))
    return min(paragraphs[start]["end"], _document_end(paragraphs))


def _is_job_title(paragraphs, index, end):
    """Recognize dated, numbered, or clearly paired titles, not review labels."""
    paragraph = paragraphs[index]
    if paragraph["style"] in ("HEADING_1", "HEADING_2"):
        return False
    text = paragraph["text"].strip()
    if _date_from_text(text) or re.search(
        r"\b(?:WO|WORK\s+ORDER)\s*(?:number\s*)?(?:#\s*)?[:\-]?\s*[A-Za-z0-9]",
        text, re.IGNORECASE,
    ):
        return True
    if not paragraph["bold"] or paragraph["style"] != "NORMAL_TEXT":
        return False
    # Some older jobs have a bold service title but no work-order number.
    # Their next line names the arrival window, which separates them from the
    # bold After-Action Review heading and other bold labels.
    for following in paragraphs[index + 1:min(end, index + 4)]:
        if _arrival_label_time(following["text"]) is not None:
            return True
        if following["bold"] or _is_named_heading(following):
            break
    return False


def _arrival_for_entry(paragraphs, title_index, following):
    """Read an arrival time from a dated title or its labeled detail line."""
    title_text = paragraphs[title_index]["text"]
    if _date_from_text(title_text):
        found = _time_from_text(title_text)
        if found is not None:
            return found
    for index in range(title_index + 1, following):
        arrival = _arrival_label_time(paragraphs[index]["text"])
        if arrival is not None:
            return arrival
    for index in range(title_index + 1, following):
        match = re.search(r"\bTime\s*[:\-]\s*(\d{1,2}:\d{2}(?:\s*[AP]\.?\s*M\.?)?)",
                          paragraphs[index]["text"], re.IGNORECASE)
        if match:
            return _time_from_text(match.group(1))
    return None


def _arrival_label_time(text):
    """Read the arrival or onsite service window used in older calendar entries."""
    match = re.search(
        r"\b(?:arrival(?:\s+window)?|arrival\s+time|arrive|on[- ]site\s+service\s+window)"
        r"\s*[:\-]?\s*(\d{1,2}:\d{2}(?:\s*[AP]\.?\s*M\.?)?)",
        text, re.IGNORECASE,
    )
    return _time_from_text(match.group(1)) if match else None


def _is_named_heading(paragraph):
    return paragraph["style"] in ("HEADING_1", "HEADING_2")


def _job_text(event, folder_url):
    title = event.title or "Work order"
    if event.wo_number:
        work_order = event.wo_number.strip()
        if not re.match(r"^WO\b", work_order, re.IGNORECASE):
            work_order = f"WO {work_order}"
        title += f" ({work_order})"
    rows = [title]
    title_range = (0, _utf16_length(title))
    rows.append(f"Arrival: {_arrival_window(event)}")
    rows.extend([
        f"Duration: {event.duration_minutes} minutes",
        f"Estimated drive from Mesa Temple: {event.drive_minutes} minutes",
        f"City: {event.city}",
    ])
    for label, value in (
        ("Store", event.store), ("Address", event.address), ("Buyer", event.buyer),
        ("Contact", event.contact), ("Phone", event.phone), ("Pay", event.pay),
        ("Scope", event.scope), ("Instructions", event.instructions),
        ("Deliverables", event.deliverables),
    ):
        if value:
            rows.append(f"{label}: {value}")
    rows.append("FieldNation folder")
    link_range = (sum(_utf16_length(line + "\n") for line in rows[:-1]),
                  sum(_utf16_length(line + "\n") for line in rows))
    rows.extend([
        "After-Action Review", "MOD:", "RE Name:", "Time on site:", "Closing Notes:",
    ])
    review_start = sum(_utf16_length(line + "\n") for line in rows[:-5])
    review_end = review_start + _utf16_length("After-Action Review")
    return "\n".join(rows) + "\n", title_range, (review_start, review_end), link_range


def _arrival_window(event):
    if event.latest_arrival:
        return f"{event.earliest_arrival}–{event.latest_arrival}"
    return event.earliest_arrival


def _bold_request(index, tab_id, span):
    return {
        "updateTextStyle": {
            "range": {
                "startIndex": index + span[0],
                "endIndex": index + span[1],
                "tabId": tab_id,
            },
            "textStyle": {"bold": True},
            "fields": "bold",
        }
    }


def _shift_range(span, prefix):
    shift = _utf16_length(prefix)
    return span[0] + shift, span[1] + shift


def _utf16_length(text):
    return len(text.encode("utf-16-le")) // 2


def _document_end(paragraphs):
    return paragraphs[-1]["end"] - 1 if paragraphs else 1


def _matching_month_index(paragraphs, target_date):
    target = target_date.strftime("%Y-%m")
    month_name = target_date.strftime("%B").casefold()
    for index, paragraph in enumerate(paragraphs):
        if paragraph["style"] != "HEADING_1":
            continue
        title = paragraph["text"].strip()
        key = _month_key(paragraphs, index)
        if title.casefold() == month_name and (key is None or key == target):
            return index
        try:
            if datetime.strptime(title, "%B %Y").strftime("%Y-%m") == target:
                return index
        except ValueError:
            continue
    return None


def _month_key(paragraphs, index):
    """Use a month heading's date entries to recover the year when it is omitted."""
    title = paragraphs[index]["text"].strip()
    try:
        return datetime.strptime(title, "%B %Y").strftime("%Y-%m")
    except ValueError:
        pass
    try:
        month_number = datetime.strptime(title, "%B").month
    except ValueError:
        return None
    end = next((i for i in range(index + 1, len(paragraphs))
                if paragraphs[i]["style"] == "HEADING_1"), len(paragraphs))
    dates = [
        _date_from_text(paragraphs[i]["text"])
        for i in range(index + 1, end)
    ]
    matching = [date for date in dates if date and date.month == month_number]
    if matching:
        return min(matching).strftime("%Y-%m")
    return None


def _date_from_text(text):
    text = text.strip()
    candidates = ("%A, %d %B, %Y", "%A, %B %d, %Y", "%B %d, %Y", "%Y-%m-%d")
    for format_string in candidates:
        try:
            return datetime.strptime(text, format_string).date()
        except ValueError:
            continue
    inline = re.search(r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+"
                       r"([A-Z][a-z]+\s+\d{1,2},\s+\d{4})", text)
    if inline:
        return datetime.strptime(inline.group(1), "%B %d, %Y").date()
    return None


def _time_from_text(text):
    match = re.search(r"\b(\d{1,2}):(\d{2})(?:\s*([AP])\.?\s*M\.?)?\b", text, re.IGNORECASE)
    if not match:
        return None
    hour, minute = int(match.group(1)), int(match.group(2))
    suffix = (match.group(3) or "").upper()
    if suffix:
        hour = hour % 12 + (12 if suffix == "P" else 0)
    return hour * 60 + minute


def _time_minutes(text):
    return _time_from_text(text)
