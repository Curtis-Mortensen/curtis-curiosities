#!/usr/bin/env python3
"""Contact sheets of ALL rendered fronts for bulk QA (one sheet per section)."""
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path("/home/fin/nandeck-test/drive-test/full-output")
QA = Path("/home/fin/nandeck-test/drive-test/full-deck-output")

sections = ["items", "prompts", "monsters", "diplomacy", "challenges"]
for sec in sections:
    files = sorted(OUT.glob(f"full-{sec}_*.png"))
    if not files:
        continue
    tw, th = 206, 281  # quarter-size thumbs
    cols = 10
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 8), rows * (th + 8)), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = (i % cols) * (tw + 8), (i // cols) * (th + 8)
        sheet.paste(im, (x, y))
        d.text((x + 4, y + 2), f.stem.split("_")[1], fill=(255, 255, 0))
    sheet.save(QA / f"qa-sheet-{sec}.png")
    print(f"{sec}: {len(files)} cards -> qa-sheet-{sec}.png ({sheet.size[0]}x{sheet.size[1]})")

# back edge check
import numpy as np
bk = Image.open("/home/fin/nandeck-test/drive-test/card_back.png").convert("RGB")
a = np.asarray(bk).astype(int)
dark = a.mean(axis=2) < 120
lc = np.where(dark[:, :200].any(axis=0))[0]
rc = np.where(dark[:, -200:].any(axis=0))[0]
tr = np.where(dark[:200, :].any(axis=1))[0]
br = np.where(dark[-200:, :].any(axis=1))[0]
print(f"back edges: left dark col={lc.min()}, from-right={824 - rc.max()}, top row={tr.min()}, from-bottom={1124 - br.max()}")
