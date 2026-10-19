"""Turn a Job's PDFs and pictures into text for the language model.

Searchable PDF pages use their embedded words. Pages without usable text are
rendered one at a time for Tesseract, just like standalone screenshots. This
module hands the combined text to luna_extraction.py.
"""

from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from pypdf import PdfReader

from models import Job


def extract_text(job: Job) -> str:
    """Read every input in a job and label its text with the source filename."""
    sections: list[str] = []
    for path, source_name in zip(job.files, job.source_names):
        if path.suffix.casefold() == ".pdf":
            text = _extract_pdf(path)
        else:
            with Image.open(path) as image:
                text = pytesseract.image_to_string(image)
        sections.append(f"--- {source_name} ---\n{text.strip()}")
    return "\n\n".join(sections)


def _extract_pdf(path: Path) -> str:
    """Keep searchable page text and OCR only the pages that have no text."""
    reader = PdfReader(path)
    pages: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        embedded = (page.extract_text() or "").strip()
        if embedded:
            pages.append(embedded)
        else:
            image = convert_from_path(path, first_page=page_number, last_page=page_number)[0]
            pages.append(pytesseract.image_to_string(image).strip())
    return "\n\n".join(pages)
