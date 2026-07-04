#!/usr/bin/env python3
"""
Convert pixel rectangles on a card design into nanDeck coordinates.

Designed for agent workflows: read a JSON regions file (from the HTML region
picker or hand-authored), emit nanDeck IMAGE/TEXT/RECTANGLE snippets in inches,
cm, or millimeters.

Usage:
  python pixels-to-nandeck.py regions.json
  python pixels-to-nandeck.py regions.json --dpi 600 --unit inch
  python pixels-to-nandeck.py --image design.png --dpi 600 --card-size 2.5,3.5
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


CARD_PRESETS: dict[str, tuple[float, float]] = {
    "poker": (2.5, 3.5),
    "tarot": (2.75, 4.75),
    "mini": (1.75, 2.5),
    "square": (2.5, 2.5),
}

PAGE_PRESETS: dict[str, tuple[float, float]] = {
    "letter": (8.5, 11.0),
    "a4": (8.27, 11.69),
    "legal": (8.5, 14.0),
}


@dataclass
class Region:
    name: str
    x: float
    y: float
    width: float
    height: float
    kind: str = "image"
    note: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Region:
        return cls(
            name=str(data.get("name", "region")),
            x=float(data["x"]),
            y=float(data["y"]),
            width=float(data["width"]),
            height=float(data["height"]),
            kind=str(data.get("kind", "image")),
            note=str(data.get("note", "")),
        )


def pixels_to_unit(value_px: float, dpi: float, unit: str) -> float:
    inches = value_px / dpi
    if unit == "inch":
        return inches
    if unit == "cm":
        return inches * 2.54
    if unit == "mm":
        return inches * 25.4
    raise ValueError(f"Unsupported unit: {unit}")


def format_value(value: float, unit: str) -> str:
    if unit == "inch":
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return f"{value:.3f}".rstrip("0").rstrip(".")


def rect_to_nandeck(region: Region, dpi: float, unit: str, card_range: str) -> str:
    x = pixels_to_unit(region.x, dpi, unit)
    y = pixels_to_unit(region.y, dpi, unit)
    w = pixels_to_unit(region.width, dpi, unit)
    h = pixels_to_unit(region.height, dpi, unit)

    fx = format_value(x, unit)
    fy = format_value(y, unit)
    fw = format_value(w, unit)
    fh = format_value(h, unit)

    if region.kind == "text":
        return f'TEXT = {card_range}, [{region.name}], {fx}, {fy}, {fw}, {fh}, left, wordwrap'
    if region.kind == "rectangle":
        return f'RECTANGLE = {card_range}, {fx}, {fy}, {fw}, {fh}, #000000'
    return f'IMAGE = {card_range}, {region.name}.png, {fx}, {fy}, {fw}, {fh}, 0, CN'


def scale_regions(
    regions: Iterable[Region],
    image_width: float,
    image_height: float,
    target_width_px: float,
    target_height_px: float,
) -> list[Region]:
    if image_width <= 0 or image_height <= 0:
        raise ValueError("Image dimensions must be positive")

    scale_x = target_width_px / image_width
    scale_y = target_height_px / image_height

    scaled: list[Region] = []
    for region in regions:
        scaled.append(
            Region(
                name=region.name,
                x=region.x * scale_x,
                y=region.y * scale_y,
                width=region.width * scale_x,
                height=region.height * scale_y,
                kind=region.kind,
                note=region.note,
            )
        )
    return scaled


def load_image_size(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit(
            "Pillow is required for --image. Install with: pip install pillow"
        ) from exc

    with Image.open(path) as image:
        return image.size


def build_header(
    unit: str,
    card_width: float,
    card_height: float,
    page_width: float | None,
    page_height: float | None,
    dpi: int,
) -> list[str]:
    lines = [
        f"UNIT = {unit.upper()}",
        "",
        f"DPI = {dpi}",
        f"CARDSIZE = {card_width}, {card_height}",
    ]
    if page_width is not None and page_height is not None:
        lines.append(f"PAGE = {page_width}, {page_height}, PORTRAIT, HV")
    lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("regions_file", nargs="?", help="JSON file exported from region picker")
    parser.add_argument("--dpi", type=int, default=600, help="Target print DPI (default: 600)")
    parser.add_argument("--unit", choices=("inch", "cm", "mm"), default="inch")
    parser.add_argument("--range", default="[all]", dest="card_range")
    parser.add_argument("--image", type=Path, help="Optional source image for dimension checks")
    parser.add_argument(
        "--card-size",
        help="Physical card size in inches, e.g. 2.5,3.5 or preset name like poker",
    )
    parser.add_argument(
        "--page-size",
        help="Physical page size in inches, e.g. 8.5,11 or preset name like letter",
    )
    parser.add_argument(
        "--scale-to-card",
        action="store_true",
        help="Scale pixel regions to the target card pixel size at --dpi",
    )
    parser.add_argument("--json", action="store_true", help="Print converted regions as JSON")
    args = parser.parse_args()

    if not args.regions_file:
        parser.print_help()
        return 1

    payload = json.loads(Path(args.regions_file).read_text(encoding="utf-8"))
    regions = [Region.from_dict(item) for item in payload.get("regions", payload)]

    dpi = int(payload.get("dpi", args.dpi))
    unit = str(payload.get("unit", args.unit)).lower()
    card_range = str(payload.get("range", args.card_range))

    card_width_in, card_height_in = CARD_PRESETS["poker"]
    if args.card_size:
        if args.card_size in CARD_PRESETS:
            card_width_in, card_height_in = CARD_PRESETS[args.card_size]
        else:
            card_width_in, card_height_in = map(float, args.card_size.split(","))

    page_width_in: float | None = None
    page_height_in: float | None = None
    if args.page_size:
        if args.page_size in PAGE_PRESETS:
            page_width_in, page_height_in = PAGE_PRESETS[args.page_size]
        else:
            page_width_in, page_height_in = map(float, args.page_size.split(","))

    image_width = float(payload.get("imageWidth", 0))
    image_height = float(payload.get("imageHeight", 0))
    if args.image:
        image_width, image_height = load_image_size(args.image)

    target_width_px = card_width_in * dpi
    target_height_px = card_height_in * dpi

    if args.scale_to_card and image_width and image_height:
        regions = scale_regions(
            regions, image_width, image_height, target_width_px, target_height_px
        )

    if args.json:
        converted = [
            {
                "name": region.name,
                "kind": region.kind,
                "pixels": {
                    "x": round(region.x),
                    "y": round(region.y),
                    "width": round(region.width),
                    "height": round(region.height),
                },
                unit: {
                    "x": pixels_to_unit(region.x, dpi, unit),
                    "y": pixels_to_unit(region.y, dpi, unit),
                    "width": pixels_to_unit(region.width, dpi, unit),
                    "height": pixels_to_unit(region.height, dpi, unit),
                },
            }
            for region in regions
        ]
        print(json.dumps({"dpi": dpi, "unit": unit, "regions": converted}, indent=2))
        return 0

    if unit == "inch":
        card_w, card_h = card_width_in, card_height_in
    elif unit == "cm":
        card_w, card_h = card_width_in * 2.54, card_height_in * 2.54
    else:
        card_w, card_h = card_width_in * 25.4, card_height_in * 25.4

    lines = build_header(unit, card_w, card_h, page_width_in, page_height_in, dpi)
    lines.append("; --- measured regions ---")
    for region in regions:
        if region.note:
            lines.append(f"; {region.name}: {region.note}")
        lines.append(rect_to_nandeck(region, dpi, unit, card_range))

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
