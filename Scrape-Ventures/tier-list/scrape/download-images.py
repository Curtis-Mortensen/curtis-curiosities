#!/usr/bin/env python3
"""
Copy local card thumbnails and download full hover art for the tier-list viewer.

Stage 2 of the Mobalytics STS2 tier-list recreation (see recreating-tier-list.html).
Reads tier-list/data/tier-lists.json, copies AVIF thumbs from the saved STS2 snapshot,
downloads full .webp art from Mobalytics CDN, and writes assets/manifest.json for Stage 3.

Reads:  tier-list/data/tier-lists.json, STS2/{slug}_19D0.avif
Writes: tier-list/assets/thumbs/{slug}.avif (symlinks by default)
        tier-list/assets/full/{slug}.webp
        tier-list/assets/manifest.json
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Paths relative to Scrape-Ventures/
ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "tier-list" / "data" / "tier-lists.json"
STS2_DIR = ROOT / "STS2"
ASSETS_DIR = ROOT / "tier-list" / "assets"
THUMBS_DIR = ASSETS_DIR / "thumbs"
FULL_DIR = ASSETS_DIR / "full"
MANIFEST_PATH = ASSETS_DIR / "manifest.json"

SPIRE_CODEX_URL = "https://cdn.spire-codex.com/cards-full/stable/{slug}.webp"
USER_AGENT = "Scrape-Ventures/STS2-tier-list (offline viewer)"


def load_tier_lists(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def unique_slugs(cards: list[dict]) -> list[str]:
    """Preserve JSON order while deduplicating slugs (403 unique cards)."""
    seen: set[str] = set()
    slugs: list[str] = []
    for card in cards:
        slug = card.get("slug")
        if not slug or slug in seen:
            continue
        seen.add(slug)
        slugs.append(slug)
    return slugs


def slug_icon_urls(cards: list[dict]) -> dict[str, str]:
    """Map each slug to its Mobalytics iconUrl for full-art download."""
    urls: dict[str, str] = {}
    for card in cards:
        slug = card.get("slug")
        icon_url = card.get("iconUrl")
        if slug and icon_url and slug not in urls:
            urls[slug] = icon_url
    return urls


def sts2_thumb_path(slug: str) -> Path:
    return STS2_DIR / f"{slug}_19D0.avif"


def thumb_dest_path(slug: str) -> Path:
    return THUMBS_DIR / f"{slug}.avif"


def full_dest_path(slug: str) -> Path:
    return FULL_DIR / f"{slug}.webp"


def manifest_thumb_path(slug: str) -> str:
    return f"assets/thumbs/{slug}.avif"


def manifest_full_path(slug: str) -> str:
    return f"assets/full/{slug}.webp"


def copy_thumb(slug: str, *, use_symlink: bool) -> str:
    """
    Link or copy STS2 AVIF into assets/thumbs/.
    Returns status: copied, linked, skipped, or missing.
    """
    source = sts2_thumb_path(slug)
    dest = thumb_dest_path(slug)

    if not source.is_file():
        return "missing"

    if dest.exists() or dest.is_symlink():
        return "skipped"

    dest.parent.mkdir(parents=True, exist_ok=True)

    if use_symlink:
        # Relative link keeps the manifest portable inside Scrape-Ventures/.
        relative_source = Path("../../../STS2") / source.name
        dest.symlink_to(relative_source)
        return "linked"

    shutil.copy2(source, dest)
    return "copied"


def download_url(url: str, dest: Path) -> bool:
    """Download a URL to dest. Returns True on success."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        dest.write_bytes(response.read())
    return True


def download_full(slug: str, icon_url: str) -> str:
    """
    Download full hover art for one card.
    Returns: downloaded, skipped, mobalytics, spire_codex, or failed.
    """
    dest = full_dest_path(slug)
    if dest.is_file() and dest.stat().st_size > 0:
        return "skipped"

    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        download_url(icon_url, dest)
        return "downloaded"
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            print(f"warning: {slug} Mobalytics CDN HTTP {exc.code}", file=sys.stderr)
    except OSError as exc:
        print(f"warning: {slug} Mobalytics CDN error: {exc}", file=sys.stderr)

    # Spire Codex uses underscores instead of hyphens in filenames.
    fallback_url = SPIRE_CODEX_URL.format(slug=slug.replace("-", "_"))
    try:
        download_url(fallback_url, dest)
        print(f"info: {slug} used Spire Codex fallback", file=sys.stderr)
        return "spire_codex"
    except (urllib.error.HTTPError, OSError) as exc:
        print(f"error: {slug} failed both sources: {exc}", file=sys.stderr)
        return "failed"

    return "failed"


def build_manifest(slugs: list[str], entries: dict[str, dict]) -> dict:
    manifest: dict[str, dict] = {}
    for slug in slugs:
        entry = entries.get(slug)
        if not entry:
            continue
        manifest[slug] = {
            "thumb": entry["thumb"],
            "full": entry["full"],
        }
        if entry.get("thumbStatus") == "missing":
            manifest[slug]["thumbMissing"] = True
        if entry.get("fullStatus") == "failed":
            manifest[slug]["fullMissing"] = True
        if entry.get("fullSource") == "spire_codex":
            manifest[slug]["fullSource"] = "spire_codex"
    return manifest


def consolidate(
    data: dict,
    *,
    thumbs: bool,
    full: bool,
    use_symlink: bool,
) -> dict:
    cards = data.get("cards") or []
    slugs = unique_slugs(cards)
    icon_urls = slug_icon_urls(cards)

    thumb_counts = {"linked": 0, "copied": 0, "skipped": 0, "missing": 0}
    full_counts = {"downloaded": 0, "spire_codex": 0, "skipped": 0, "failed": 0}

    entries: dict[str, dict] = {}

    for slug in slugs:
        entry = {
            "thumb": manifest_thumb_path(slug),
            "full": manifest_full_path(slug),
        }

        if thumbs:
            thumb_status = copy_thumb(slug, use_symlink=use_symlink)
            entry["thumbStatus"] = thumb_status
            thumb_counts[thumb_status] = thumb_counts.get(thumb_status, 0) + 1

        if full:
            icon_url = icon_urls.get(slug, "")
            full_status = download_full(slug, icon_url) if icon_url else "failed"
            entry["fullStatus"] = full_status
            if full_status == "spire_codex":
                entry["fullSource"] = "spire_codex"
            if full_status in full_counts:
                full_counts[full_status] += 1
            elif full_status == "downloaded":
                full_counts["downloaded"] += 1

        entries[slug] = entry

    manifest = {
        "source": data.get("source", "mobalytics"),
        "fetchedAt": data.get("fetchedAt"),
        "cardCount": len(slugs),
        "paths": build_manifest(slugs, entries),
    }

    if thumbs or full:
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        with MANIFEST_PATH.open("w", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2, ensure_ascii=False)
            handle.write("\n")

    return {
        "slugCount": len(slugs),
        "thumbCounts": thumb_counts,
        "fullCounts": full_counts,
        "manifestPath": MANIFEST_PATH,
        "failedSlugs": [
            slug
            for slug, entry in entries.items()
            if entry.get("thumbStatus") == "missing" or entry.get("fullStatus") == "failed"
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=DATA_PATH,
        help=f"Tier list JSON (default: {DATA_PATH.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy AVIF thumbs instead of symlinking to STS2/",
    )
    parser.add_argument(
        "--thumbs-only",
        action="store_true",
        help="Only consolidate thumbnails (skip full-art download)",
    )
    parser.add_argument(
        "--full-only",
        action="store_true",
        help="Only download full hover art (skip thumbnail copy)",
    )
    args = parser.parse_args()

    if args.thumbs_only and args.full_only:
        raise SystemExit("Use at most one of --thumbs-only or --full-only")

    data = load_tier_lists(args.data)
    result = consolidate(
        data,
        thumbs=not args.full_only,
        full=not args.thumbs_only,
        use_symlink=not args.copy,
    )

    print(f"Processed {result['slugCount']} card slugs from {args.data}")

    if not args.full_only:
        counts = result["thumbCounts"]
        print(
            "Thumbs: "
            f"linked={counts.get('linked', 0)}, "
            f"copied={counts.get('copied', 0)}, "
            f"skipped={counts.get('skipped', 0)}, "
            f"missing={counts.get('missing', 0)}"
        )

    if not args.thumbs_only:
        counts = result["fullCounts"]
        print(
            "Full art: "
            f"downloaded={counts.get('downloaded', 0)}, "
            f"spire_codex={counts.get('spire_codex', 0)}, "
            f"skipped={counts.get('skipped', 0)}, "
            f"failed={counts.get('failed', 0)}"
        )

    print(f"Wrote manifest to {result['manifestPath']}")

    if result["failedSlugs"]:
        print(f"Failed or missing: {len(result['failedSlugs'])} slugs", file=sys.stderr)
        for slug in result["failedSlugs"][:20]:
            print(f"  - {slug}", file=sys.stderr)
        if len(result["failedSlugs"]) > 20:
            print(f"  … and {len(result['failedSlugs']) - 20} more", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
