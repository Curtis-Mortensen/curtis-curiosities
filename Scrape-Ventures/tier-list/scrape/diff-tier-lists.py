#!/usr/bin/env python3
"""
Compare two tier-list JSON snapshots and print what changed.

Use after refresh-tier-list.py (or any fetch-tier-lists.py run) to see cards
that moved tiers, were added, or dropped from the Mobalytics rankings.

Reads:  two tier-list/data/tier-lists*.json files (old vs new)
Writes: human-readable summary to stdout; optional JSON report with --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_NEW = ROOT / "tier-list" / "data" / "tier-lists.json"
DEFAULT_OLD = ROOT / "tier-list" / "data" / "tier-lists.previous.json"

CHARACTER_ORDER = ["ironclad", "silent", "regent", "necrobinder", "defect"]
TIER_ORDER = ["S", "A", "B", "C", "D", "TBD"]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def placements(data: dict) -> dict[tuple[str, str], dict]:
    """Map (character, slug) to name + tier for every ranked card."""
    result: dict[tuple[str, str], dict] = {}
    for card in data.get("cards", []):
        character = card.get("character")
        slug = card.get("slug")
        if not character or not slug:
            continue
        result[(character, slug)] = {
            "name": card.get("name") or slug,
            "tier": card.get("tier") or "?",
        }
    return result


def tier_sort_key(tier: str) -> int:
    try:
        return TIER_ORDER.index(tier)
    except ValueError:
        return len(TIER_ORDER)


def character_sort_key(character: str) -> int:
    try:
        return CHARACTER_ORDER.index(character)
    except ValueError:
        return len(CHARACTER_ORDER)


def compare(old_data: dict, new_data: dict) -> dict:
    """Build a structured diff between two normalized tier-list files."""
    old = placements(old_data)
    new = placements(new_data)

    moved: list[dict] = []
    added: list[dict] = []
    removed: list[dict] = []

    for (character, slug), old_card in old.items():
        if (character, slug) not in new:
            removed.append(
                {
                    "character": character,
                    "slug": slug,
                    "name": old_card["name"],
                    "tier": old_card["tier"],
                }
            )
            continue
        new_card = new[(character, slug)]
        if old_card["tier"] != new_card["tier"]:
            moved.append(
                {
                    "character": character,
                    "slug": slug,
                    "name": new_card["name"],
                    "fromTier": old_card["tier"],
                    "toTier": new_card["tier"],
                }
            )

    for (character, slug), new_card in new.items():
        if (character, slug) not in old:
            added.append(
                {
                    "character": character,
                    "slug": slug,
                    "name": new_card["name"],
                    "tier": new_card["tier"],
                }
            )

    moved.sort(
        key=lambda row: (
            character_sort_key(row["character"]),
            tier_sort_key(row["fromTier"]),
            row["name"].lower(),
        )
    )
    added.sort(
        key=lambda row: (
            character_sort_key(row["character"]),
            tier_sort_key(row["tier"]),
            row["name"].lower(),
        )
    )
    removed.sort(
        key=lambda row: (
            character_sort_key(row["character"]),
            tier_sort_key(row["tier"]),
            row["name"].lower(),
        )
    )

    return {
        "oldFetchedAt": old_data.get("fetchedAt"),
        "newFetchedAt": new_data.get("fetchedAt"),
        "oldCardCount": old_data.get("cardCount", len(old)),
        "newCardCount": new_data.get("cardCount", len(new)),
        "moved": moved,
        "added": added,
        "removed": removed,
        "unchangedCount": len(old) - len(removed) - len(moved),
    }


def format_report(diff: dict, old_path: Path, new_path: Path) -> str:
    """Turn the structured diff into plain text for the terminal."""
    lines = [
        f"Compared {old_path.name} → {new_path.name}",
        f"  old: {diff['oldCardCount']} cards ({diff['oldFetchedAt']})",
        f"  new: {diff['newCardCount']} cards ({diff['newFetchedAt']})",
        "",
    ]

    if not diff["moved"] and not diff["added"] and not diff["removed"]:
        lines.append("No tier placement changes.")
        return "\n".join(lines)

    if diff["moved"]:
        lines.append(f"Moved ({len(diff['moved'])}):")
        for row in diff["moved"]:
            lines.append(
                f"  {row['character']}: {row['name']} ({row['slug']}) "
                f"{row['fromTier']} → {row['toTier']}"
            )
        lines.append("")

    if diff["added"]:
        lines.append(f"Added ({len(diff['added'])}):")
        for row in diff["added"]:
            lines.append(
                f"  {row['character']}: {row['name']} ({row['slug']}) → {row['tier']}"
            )
        lines.append("")

    if diff["removed"]:
        lines.append(f"Removed ({len(diff['removed'])}):")
        for row in diff["removed"]:
            lines.append(
                f"  {row['character']}: {row['name']} ({row['slug']}) was {row['tier']}"
            )
        lines.append("")

    lines.append(f"Unchanged placements: {diff['unchangedCount']}")
    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "old",
        nargs="?",
        type=Path,
        default=DEFAULT_OLD,
        help=f"Older snapshot (default: {DEFAULT_OLD.relative_to(ROOT)})",
    )
    parser.add_argument(
        "new",
        nargs="?",
        type=Path,
        default=DEFAULT_NEW,
        help=f"Newer snapshot (default: {DEFAULT_NEW.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON instead of a text report",
    )
    args = parser.parse_args()

    if not args.old.is_file():
        print(f"Missing old file: {args.old}", file=sys.stderr)
        return 1
    if not args.new.is_file():
        print(f"Missing new file: {args.new}", file=sys.stderr)
        return 1

    diff = compare(load_json(args.old), load_json(args.new))

    if args.json:
        print(json.dumps(diff, indent=2, ensure_ascii=False))
    else:
        print(format_report(diff, args.old, args.new))

    has_changes = bool(diff["moved"] or diff["added"] or diff["removed"])
    return 2 if has_changes else 0


if __name__ == "__main__":
    sys.exit(main())
