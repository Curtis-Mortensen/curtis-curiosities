#!/usr/bin/env python3
"""
Bake tier-list JSON into index.html so the viewer works on file:// without a server.

Browsers block fetch() for local JSON files, but inline <script> data and relative
image paths both work offline. Run this after fetch-tier-lists.py and download-images.py.

Reads:  tier-list/data/tier-lists.json, tier-list/assets/manifest.json, tier-list/index.html
Writes: tier-list/index.html (injects window.TIER_DATA between marker comments)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "tier-list" / "data" / "tier-lists.json"
MANIFEST_PATH = ROOT / "tier-list" / "assets" / "manifest.json"
INDEX_PATH = ROOT / "tier-list" / "index.html"

START_MARKER = "<!-- tier-data:start -->"
END_MARKER = "<!-- tier-data:end -->"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def bake_block(tiers: dict, manifest: dict) -> str:
    """Build the inline script tag with both JSON payloads."""
    payload = json.dumps(
        {"tiers": tiers, "manifest": manifest},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return (
        f"{START_MARKER}\n"
        f'  <script id="tier-data-baked">\n'
        f"  window.TIER_DATA = {payload};\n"
        f"  </script>\n"
        f"  {END_MARKER}"
    )


def inject_data(html: str, block: str) -> str:
    """Replace content between bake markers, or fail with a clear message."""
    start = html.find(START_MARKER)
    end = html.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        raise ValueError(
            f"Missing bake markers in {INDEX_PATH.name}. "
            f"Expected {START_MARKER} and {END_MARKER}."
        )
    end += len(END_MARKER)
    return html[:start] + block + html[end:]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bake tier-list JSON into index.html for offline file:// use."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DATA_PATH,
        help=f"Tier list JSON (default: {DATA_PATH.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST_PATH,
        help=f"Image manifest (default: {MANIFEST_PATH.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=INDEX_PATH,
        help=f"Viewer HTML to update (default: {INDEX_PATH.relative_to(ROOT)})",
    )
    args = parser.parse_args()

    tiers = load_json(args.data)
    manifest = load_json(args.manifest)
    html = args.index.read_text(encoding="utf-8")

    baked = inject_data(html, bake_block(tiers, manifest))
    args.index.write_text(baked, encoding="utf-8")

    card_count = tiers.get("cardCount", len(tiers.get("cards", [])))
    print(f"Baked {card_count} cards into {args.index.relative_to(ROOT)}")
    print("Open tier-list/index.html directly — no HTTP server needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
