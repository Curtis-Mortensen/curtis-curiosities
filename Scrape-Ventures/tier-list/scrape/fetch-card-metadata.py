#!/usr/bin/env python3
"""
Fetch card metadata (cost, type, rarity, description) from Spire Codex for tooltips.

Spire Codex is used for metadata only — Mobalytics tier rankings stay authoritative.
Downloads the bulk /api/cards list once, maps entries to our tier-list slugs by id/name.

Reads:  tier-list/data/tier-lists.json
Writes: tier-list/data/card-metadata.json
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "tier-list" / "data" / "tier-lists.json"
OUT_PATH = ROOT / "tier-list" / "data" / "card-metadata.json"
SPIRE_CODEX_URL = "https://spire-codex.com/api/cards"
USER_AGENT = "Scrape-Ventures/STS2-tier-list (offline viewer)"


def load_tier_lists(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def fetch_all_cards() -> list[dict]:
    request = urllib.request.Request(
        SPIRE_CODEX_URL,
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def codex_id_to_slug(card_id: str) -> str:
    """Turn Spire Codex id CRASH_LANDING into slug crash-landing."""
    return card_id.lower().replace("_", "-")


def format_cost(card: dict) -> str:
    """Human-readable energy / star cost for tooltip display."""
    if card.get("is_x_star_cost"):
        stars = card.get("star_cost")
        return f"{stars}★" if stars is not None else "X★"
    if card.get("star_cost") is not None:
        return f"{card['star_cost']}★"
    if card.get("is_x_cost"):
        return "X"
    return str(card.get("cost", 0))


def build_lookup(codex_cards: list[dict]) -> tuple[dict[str, dict], dict[str, dict]]:
    """Index Spire Codex cards by slug and by lowercase name."""
    by_slug: dict[str, dict] = {}
    by_name: dict[str, dict] = {}
    for card in codex_cards:
        slug = codex_id_to_slug(card["id"])
        by_slug[slug] = card
        by_name[card["name"].lower()] = card
    return by_slug, by_name


def pick_metadata(card: dict) -> dict:
    """Keep only the fields the hover tooltip needs."""
    entry = {
        "name": card["name"],
        "cost": format_cost(card),
        "type": card.get("type"),
        "rarity": card.get("rarity"),
        "description": card.get("description"),
    }
    keywords = card.get("keywords")
    if keywords:
        entry["keywords"] = keywords
    return entry


def resolve_card(
    slug: str,
    name: str,
    by_slug: dict[str, dict],
    by_name: dict[str, dict],
) -> dict | None:
    """Match a tier-list slug to a Spire Codex card record."""
    if slug in by_slug:
        return by_slug[slug]
    if name.lower() in by_name:
        return by_name[name.lower()]
    alt = slug.replace("-", "_")
    for card in by_slug.values():
        if codex_id_to_slug(card["id"]) == slug or card["id"].lower() == alt:
            return card
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch Spire Codex card metadata for tier-list tooltips."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DATA_PATH,
        help=f"Tier list JSON (default: {DATA_PATH.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT_PATH,
        help=f"Output metadata JSON (default: {OUT_PATH.relative_to(ROOT)})",
    )
    args = parser.parse_args()

    tier_data = load_tier_lists(args.data)
    codex_cards = fetch_all_cards()
    by_slug, by_name = build_lookup(codex_cards)

    cards_out: dict[str, dict] = {}
    missing: list[str] = []

    for card in tier_data["cards"]:
        slug = card["slug"]
        match = resolve_card(slug, card["name"], by_slug, by_name)
        if match:
            cards_out[slug] = pick_metadata(match)
        else:
            missing.append(slug)

    output = {
        "source": "spire-codex",
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "cardCount": len(cards_out),
        "missingCount": len(missing),
        "missingSlugs": missing,
        "cards": cards_out,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(f"Wrote {len(cards_out)} card metadata entries to {args.out.relative_to(ROOT)}")
    if missing:
        print(f"Missing from Spire Codex ({len(missing)}): {', '.join(missing)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
