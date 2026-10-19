#!/usr/bin/env python3
"""
Fetch Mobalytics STS2 card tier list rankings and write normalized JSON.

Mobalytics stores tier lists in a GraphQL API. Plain curl gets blocked by
Cloudflare, so this script uses curl_cffi (Chrome TLS fingerprint) when
fetching live. You can also pass a saved DevTools response via --raw.

Reads:  Mobalytics GraphQL (live) or STS2/tier-lists-raw.json (--raw)
Writes: tier-list/data/tier-lists.json
        STS2/tier-lists-raw.json (when fetching live)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Paths relative to Scrape-Ventures/
ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "STS2" / "tier-lists-raw.json"
OUT_PATH = ROOT / "tier-list" / "data" / "tier-lists.json"

GRAPHQL_URL = "https://mobalytics.gg/api/sts2/v1/graphql/query"

# Mobalytics omits multiplayer cards on the public tier list page.
SKIP_CHARACTERS = {"multiplayer"}

TIER_LIST_QUERY = """
query Sts2TierLists($input: Sts2UserGeneratedDocumentInputBySlug!) {
  game: sts2 {
    documents {
      userGeneratedDocumentBySlug(input: $input) {
        error
        data {
          data {
            tierLists {
              values {
                id
                tierSections {
                  name
                  staticDataItems {
                    name
                    slug
                    iconUrl
                    linkUrl
                    type
                  }
                }
                staticDataSources {
                  slug
                  tags { slug groupSlug }
                }
              }
            }
          }
          content {
            __typename
            ... on NgfDocumentCmWidgetTierListMakerV1 {
              id
              data { title }
            }
          }
        }
      }
    }
  }
}
"""


def fetch_live() -> dict:
    """POST the tier-list GraphQL query to Mobalytics."""
    try:
        from curl_cffi import requests
    except ImportError as exc:
        raise SystemExit(
            "curl_cffi is required for live fetch. Install with: pip install curl_cffi\n"
            "Or save a DevTools response to STS2/tier-lists-raw.json and use --raw."
        ) from exc

    payload = {
        "operationName": "Sts2TierLists",
        "variables": {"input": {"slug": "cards", "type": "tier-lists"}},
        "query": TIER_LIST_QUERY,
    }
    response = requests.post(GRAPHQL_URL, json=payload, impersonate="chrome")
    response.raise_for_status()
    body = response.json()
    if body.get("errors"):
        raise SystemExit(f"GraphQL errors: {json.dumps(body['errors'], indent=2)}")
    return body


def load_raw(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def character_slug_from_title(title: str) -> str | None:
    """Turn widget title 'Ironclad Tier List' into slug 'ironclad'."""
    match = re.match(r"^(\w+)\s+Tier\s+List$", title.strip(), re.IGNORECASE)
    if not match:
        return None
    return match.group(1).lower()


def widget_character_map(content: list) -> dict[str, dict]:
    """
    Map each tier-list widget id to character metadata.

    Widget ids match tierLists.values[].id. We skip Multiplayer to match
    the Mobalytics editorial list scope.
    """
    mapping: dict[str, dict] = {}
    index = 0
    for widget in content:
        if widget.get("__typename") != "NgfDocumentCmWidgetTierListMakerV1":
            continue
        index += 1
        title = (widget.get("data") or {}).get("title") or ""
        character = character_slug_from_title(title)
        if not character or character in SKIP_CHARACTERS:
            continue
        mapping[widget["id"]] = {
            "character": character,
            "title": title,
            "anchorId": f"{index}-{character}-tier-list-2",
            "widgetIndex": index,
        }
    return mapping


def normalize(payload: dict) -> dict:
    """Turn GraphQL response into viewer-friendly tier-list JSON."""
    doc = payload["data"]["game"]["documents"]["userGeneratedDocumentBySlug"]["data"]
    tier_values = doc["data"]["tierLists"]["values"]
    by_id = {entry["id"]: entry for entry in tier_values}
    widgets = widget_character_map(doc.get("content") or [])

    characters = []
    flat_cards = []

    for widget_id, meta in widgets.items():
        entry = by_id.get(widget_id)
        if entry is None:
            # ids can be short ("5") or full uuid; try prefix match
            for key, value in by_id.items():
                if key == widget_id or key.startswith(widget_id):
                    entry = value
                    break
        if entry is None:
            print(f"warning: no tier list data for widget {widget_id}", file=sys.stderr)
            continue

        tiers: dict[str, list] = {}
        for section in entry.get("tierSections") or []:
            tier_name = section.get("name")
            if not tier_name:
                continue
            cards = []
            for item in section.get("staticDataItems") or []:
                card = {
                    "name": item.get("name"),
                    "slug": item.get("slug"),
                    "iconUrl": item.get("iconUrl"),
                    "linkUrl": item.get("linkUrl"),
                    "type": item.get("type"),
                }
                cards.append(card)
                flat_cards.append(
                    {
                        "name": card["name"],
                        "slug": card["slug"],
                        "tier": tier_name,
                        "character": meta["character"],
                        "iconUrl": card["iconUrl"],
                        "linkUrl": card["linkUrl"],
                    }
                )
            tiers[tier_name] = cards

        characters.append(
            {
                "character": meta["character"],
                "title": meta["title"],
                "anchorId": meta["anchorId"],
                "widgetIndex": meta["widgetIndex"],
                "tiers": tiers,
            }
        )

    # Stable page order from the live Mobalytics layout.
    order = ["ironclad", "silent", "regent", "necrobinder", "defect"]
    characters.sort(key=lambda row: order.index(row["character"]))

    return {
        "source": "mobalytics",
        "documentSlug": "cards",
        "documentType": "tier-lists",
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "characterCount": len(characters),
        "cardCount": len(flat_cards),
        "characters": characters,
        "cards": flat_cards,
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw",
        nargs="?",
        const=str(RAW_PATH),
        default=None,
        metavar="PATH",
        help="Parse saved GraphQL JSON instead of fetching (default: STS2/tier-lists-raw.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUT_PATH,
        help=f"Normalized output path (default: {OUT_PATH.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--no-save-raw",
        action="store_true",
        help="Do not write STS2/tier-lists-raw.json when fetching live",
    )
    args = parser.parse_args()

    if args.raw:
        raw_path = Path(args.raw)
        payload = load_raw(raw_path)
        print(f"Loaded raw response from {raw_path}")
    else:
        payload = fetch_live()
        print("Fetched tier list from Mobalytics GraphQL")
        if not args.no_save_raw:
            write_json(RAW_PATH, payload)
            print(f"Wrote raw response to {RAW_PATH}")

    normalized = normalize(payload)
    write_json(args.output, normalized)
    print(
        f"Wrote {normalized['cardCount']} cards across "
        f"{normalized['characterCount']} characters to {args.output}"
    )


if __name__ == "__main__":
    main()
