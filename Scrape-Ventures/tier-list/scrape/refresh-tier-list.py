#!/usr/bin/env python3
"""
Run the full STS2 tier-list refresh pipeline in one command.

When Mobalytics updates rankings, this script:
  1. Backs up the current tier-lists.json (for diffing)
  2. fetch-tier-lists.py      — Mobalytics GraphQL → tier-lists.json
  3. download-images.py       — thumbs + full hover art + manifest
  4. fetch-card-metadata.py   — Spire Codex tooltips
  5. build-viewer.py          — bake JSON into index.html for file://
  6. diff-tier-lists.py       — show tier moves vs the backup

Edit tier-list/data/methodology.json by hand if Mobalytics copy changes — it is
not scraped. Never hand-edit the baked JSON inside index.html; re-run this script.

Reads/writes: everything under tier-list/ and STS2/tier-lists-raw.json
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRAPE_DIR = Path(__file__).resolve().parent
TIER_LISTS_PATH = ROOT / "tier-list" / "data" / "tier-lists.json"
PREVIOUS_PATH = ROOT / "tier-list" / "data" / "tier-lists.previous.json"
SNAPSHOTS_DIR = ROOT / "tier-list" / "data" / "snapshots"


def backup_tier_lists() -> Path | None:
    """
    Keep a copy of the current rankings before fetching new data.

    Writes tier-lists.previous.json and a timestamped file under snapshots/.
    Returns the previous-path backup, or None if there was nothing to save.
    """
    if not TIER_LISTS_PATH.is_file():
        return None

    PREVIOUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TIER_LISTS_PATH, PREVIOUS_PATH)

    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snapshot_path = SNAPSHOTS_DIR / f"tier-lists-{stamp}.json"
    shutil.copy2(TIER_LISTS_PATH, snapshot_path)
    print(f"Backed up {TIER_LISTS_PATH.relative_to(ROOT)} → {PREVIOUS_PATH.relative_to(ROOT)}", flush=True)
    print(f"Snapshot: {snapshot_path.relative_to(ROOT)}", flush=True)
    return PREVIOUS_PATH


def run_script(name: str, extra_args: list[str]) -> None:
    """Run a scrape/*.py helper and stop the pipeline if it fails."""
    script = SCRAPE_DIR / name
    command = [sys.executable, str(script), *extra_args]
    print(f"\n=== {name} ===", flush=True)
    subprocess.run(command, check=True, cwd=ROOT)


def run_diff(old_path: Path, new_path: Path) -> int:
    """Print tier placement changes; exit code 2 means something changed."""
    print("\n=== diff-tier-lists.py ===", flush=True)
    result = subprocess.run(
        [sys.executable, str(SCRAPE_DIR / "diff-tier-lists.py"), str(old_path), str(new_path)],
        cwd=ROOT,
    )
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw",
        nargs="?",
        const=str(ROOT / "STS2" / "tier-lists-raw.json"),
        default=None,
        metavar="PATH",
        help="Pass --raw to fetch-tier-lists.py (offline re-parse from saved GraphQL)",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not copy tier-lists.json before fetching",
    )
    parser.add_argument(
        "--no-diff",
        action="store_true",
        help="Skip diff-tier-lists.py at the end",
    )
    parser.add_argument(
        "--skip-fetch",
        action="store_true",
        help="Skip fetch-tier-lists.py (rebuild viewer from existing JSON)",
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Skip download-images.py",
    )
    parser.add_argument(
        "--skip-metadata",
        action="store_true",
        help="Skip fetch-card-metadata.py",
    )
    parser.add_argument(
        "--skip-bake",
        action="store_true",
        help="Skip build-viewer.py",
    )
    args = parser.parse_args()

    backup_path: Path | None = None
    if not args.skip_fetch and not args.no_backup:
        backup_path = backup_tier_lists()

    if not args.skip_fetch:
        fetch_args: list[str] = []
        if args.raw is not None:
            fetch_args.append("--raw")
            if args.raw:
                fetch_args.append(args.raw)
        run_script("fetch-tier-lists.py", fetch_args)

    if not args.skip_images:
        run_script("download-images.py", [])

    if not args.skip_metadata:
        run_script("fetch-card-metadata.py", [])

    if not args.skip_bake:
        run_script("build-viewer.py", [])

    if args.no_diff or args.skip_fetch:
        print("\nRefresh complete.")
        return 0

    if backup_path is None or not backup_path.is_file():
        print("\nNo previous tier-lists.json to diff against (first run or --no-backup).")
        print("Refresh complete.")
        return 0

    diff_code = run_diff(backup_path, TIER_LISTS_PATH)
    print("\nRefresh complete.")
    return 0 if diff_code in (0, 2) else diff_code


if __name__ == "__main__":
    sys.exit(main())
