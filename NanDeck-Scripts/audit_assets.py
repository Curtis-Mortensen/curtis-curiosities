#!/usr/bin/env python3
"""Asset audit: pick best copy (root vs drive-assets) for every workbook image ref.
Also inspect card-back source candidates. Writes manifest.json + report."""
import json
from pathlib import Path

import numpy as np
import openpyxl
from PIL import Image

BASE = Path("/home/fin/nandeck-test/drive-test")
ASSETS = BASE / "drive-assets"

def load(p):
    im = Image.open(p)
    im.load()
    return im

def is_tile(im):
    """nanDECK-style placeholder: mostly flat saturated red/green."""
    a = np.asarray(im.convert("RGB").resize((60, 60)), dtype=np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = ((r > 110) & (g < 70) & (b < 70)).mean()
    green = ((g > 90) & (r < 100) & (b < 100)).mean()
    return red > 0.5 or green > 0.5

def pick(ref):
    """Choose the best available copy for an image reference."""
    cands = []
    for p in [BASE / ref, ASSETS / ref]:
        if p.exists():
            try:
                im = load(p)
                cands.append((p, im, is_tile(im)))
            except Exception:
                pass
    if not cands:
        return None, "MISSING everywhere"
    real = [(p, im) for p, im, t in cands if not t]
    if real:
        p, im = max(real, key=lambda x: x[1].width * x[1].height)
        return p, f"real {im.size} from {p.parent.name}"
    p, im = cands[0]
    return p, f"ONLY-TILE {im.size} from {p.parent.name}"

wb = openpyxl.load_workbook(BASE / "Unified-Cards-Sheet.xlsx", data_only=True)
manifest = {}
print("== ITEMS (56) ==")
items = wb["Items"]
for i, row in enumerate(items.iter_rows(min_row=2, values_only=True), start=1):
    ref = str(row[17]).strip()
    p, note = pick(ref)
    manifest[f"item_{i:02d}"] = {"ref": ref, "path": str(p) if p else None, "note": note}
    flag = "" if p and "real" in note else "  <<<"
    print(f"  {i:02d} {ref:44s} {note}{flag}")

print("== MONSTERS (13) ==")
mons = wb["Monsters"]
for i, row in enumerate(mons.iter_rows(min_row=2, values_only=True), start=1):
    ref = str(row[6]).strip() if row[6] else ""
    if not ref:
        manifest[f"monster_{i:02d}"] = {"ref": None, "path": None, "note": "no image (cut card)"}
        continue
    p, note = pick(ref)
    manifest[f"monster_{i:02d}"] = {"ref": ref, "path": str(p) if p else None, "note": note}
    flag = "" if p and "real" in note else "  <<<"
    print(f"  {i:02d} {ref:24s} {note}{flag}")

print("== CHALLENGES (12) ==")
chal = wb["Challenges"]
for i, row in enumerate(chal.iter_rows(min_row=2, values_only=True), start=1):
    ref = str(row[3]).strip() if row[3] else ""
    p, note = pick(ref)
    manifest[f"challenge_{i:02d}"] = {"ref": ref, "path": str(p) if p else None, "note": note}
    flag = "" if p and "real" in note else "  <<<"
    print(f"  {i:02d} {ref:24s} {note}{flag}")

# icons + frames + border: always drive-assets (verified)
for k, f in [("icon_bow", "bow.png"), ("icon_finesse", "finesse.png"), ("icon_fire", "fire.png"),
             ("icon_healing", "healing.png"), ("icon_ice", "ice.png"), ("icon_armor", "armor.png"),
             ("icon_light", "light.png"), ("icon_shield", "shield.png"), ("icon_pet", "pet.png"),
             ("icon_theft", "theft.png"), ("icon_heavy_weapon", "heavy_weapon.png"),
             ("icon_instrument", "instrument.png"), ("frame_basic", "frame_basic.png"),
             ("frame_instant", "frame_instant.png"), ("frame_rare", "frame_rare.png"),
             ("border_black", str(BASE / "diplomacy_black_border.png")), ("blank", "blank.png")]:
    p = Path(f) if f.startswith("/") else ASSETS / f
    if not p.exists():
        manifest[k] = {"path": None, "note": "MISSING"}
        print(f"  {k:16s} MISSING")
        continue
    im = load(p)
    t = is_tile(im)
    manifest[k] = {"path": str(p), "note": f"{'TILE!' if t else 'real'} {im.size}"}
    print(f"  {k:16s} {'TILE!' if t else 'real'} {im.size}")

# card-back source candidates
print("\n== card back candidates ==")
for name in ["item back.png", "background for cards.png", "background cards.png",
             "old-bone-dice-roll--t3chat--1.png", "bone-dice-roll-.png",
             "Copy of bone-dice-roll-.png", "bone-dice-roll-__108BNWzk.png",
             "class board background.png"]:
    p = ASSETS / name
    if p.exists():
        im = load(p)
        a = np.asarray(im.convert("RGBA"))
        alpha_frac = float((a[..., 3] < 50).mean())
        print(f"  {name:40s} {im.size} mode={im.mode} transparent={alpha_frac:.2f}")
    else:
        print(f"  {name:40s} MISSING")

out = BASE / "asset-manifest.json"
out.write_text(json.dumps(manifest, indent=2))
print("manifest saved ->", out)
print(f"\nmanifest -> {out}")
