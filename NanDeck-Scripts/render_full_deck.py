#!/usr/bin/env python3
"""
render_full_deck.py — deterministic full-deck renderer (replaces broken Wine renders).

Fixes all six reported defects:
  1. text drawn directly ON the frame's opaque navy panel (no white boxes)
  2. icons from the 12 verified real icon PNGs in drive-assets/
  3. larger text (bumped pt sizes + auto-fit shrink, floor 10pt) at 300dpi
  4. real frame_instant.png for Instant items
  5. real full-res art for every card (placeholder thumbs bypassed)
  6. card back rebuilt from item back.png, uniformly scaled & centered

Geometry taken verbatim from the full-*.nde nanDECK scripts (UNIT=INCH, DPI=300).
Fonts: Liberation Sans (Arial metric-compatible).
"""
import json
import sys
from pathlib import Path

import numpy as np
import openpyxl
from PIL import Image, ImageDraw, ImageFont

BASE = Path("/home/fin/nandeck-test/drive-test")
ASSETS = BASE / "drive-assets"
ROOT = BASE
OUT = BASE / "full-output"
W, H = 825, 1125
DPI = 300
def IN(v):  # inches -> px at 300 dpi
    return int(round(v * DPI))

FONTS = {
    "reg": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "ital": "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    "boldital": "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
    # Serif (Times-metric) family for card titles (Curtis 2026-09-09)
    "serif": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "serifbold": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "serifital": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
}
ICON_NAMES = ["bow", "finesse", "fire", "healing", "ice", "armor", "light",
              "shield", "pet", "theft", "heavy_weapon", "instrument"]

_manifest = json.loads((BASE / "asset-manifest.json").read_text())

def font(kind, pt):
    return ImageFont.truetype(FONTS[kind], int(round(pt * DPI / 72)))

def open_real(ref):
    """Find the best real copy of an image ref (assets preferred, skip tiles)."""
    ref = ref.strip()
    cands = [ASSETS / ref, ROOT / ref]
    if not (ASSETS / ref).exists() and not (ROOT / ref).exists():
        # case-insensitive / suffix search as last resort
        for d in (ASSETS, ROOT):
            m = [p for p in d.glob(f"*{ref}*")] or [p for p in d.glob(f"*{Path(ref).stem}*")]
            cands.extend(m)
    scored = []
    for p in cands:
        if not p.exists():
            continue
        try:
            im = Image.open(p)
        except Exception:
            continue
        a = np.asarray(im.convert("RGB")).astype(np.float32)
        is_tile = (a.std() < 18.0)  # placeholder tiles are flat/4-quadrant flats
        scored.append((is_tile, -im.size[0] * im.size[1], str(p), im))
    scored.sort(key=lambda t: (t[0], t[1]))
    if not scored or scored[0][0]:
        raise SystemExit(f"no real image for ref {ref!r}: {[s[2] for s in scored]}")
    return scored[0][3]

def paste_fit(canvas, im, box):
    """nanDECK 'CN': fit keeping aspect, centered in box."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    s = min(bw / im.width, bh / im.height)
    nw, nh = max(1, round(im.width * s)), max(1, round(im.height * s))
    im2 = im.resize((nw, nh), Image.LANCZOS).convert("RGBA")
    canvas.alpha_composite(im2, (x0 + (bw - nw) // 2, y0 + (bh - nh) // 2))

def paste_stretch(canvas, im, box):
    x0, y0, x1, y1 = box
    im2 = im.resize((x1 - x0, y1 - y0), Image.LANCZOS).convert("RGBA")
    canvas.alpha_composite(im2, (x0, y0))

def paste_zoom(canvas, im, box, focus=None):
    """Zoom-crop: scale art to COVER the box (no bars), then crop to fit.
    focus = (fx, fy) in 0..1 source-relative coords to keep in the crop
    center (e.g. (0.5, 0.15) keeps the top visible); None = center crop."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    s = max(bw / im.width, bh / im.height)
    nw, nh = max(bw, round(im.width * s)), max(bh, round(im.height * s))
    im2 = im.resize((nw, nh), Image.LANCZOS).convert("RGBA")
    if focus:
        cx, cy = focus[0] * nw, focus[1] * nh
    else:
        cx, cy = nw / 2, nh / 2
    left = int(min(max(0, cx - bw / 2), nw - bw))
    top = int(min(max(0, cy - bh / 2), nh - bh))
    im2 = im2.crop((left, top, left + bw, top + bh))
    canvas.alpha_composite(im2, (x0, y0))

def paste_cp(canvas, im, cx, cy, size):
    """nanDECK 'CP': centered box of given size, keep aspect (icons)."""
    s = min(size / im.width, size / im.height)
    nw, nh = max(1, round(im.width * s)), max(1, round(im.height * s))
    im2 = im.resize((nw, nh), Image.LANCZOS).convert("RGBA")
    canvas.alpha_composite(im2, (cx - nw // 2, cy - nh // 2))

def wrap(text, fnt, maxw):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if fnt.getlength(t) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines

def draw_fit(draw, text, box, kind, pt_start, pt_min, fill, anchor="la",
             align="left", spacing_k=1.16, stroke=0, stroke_fill=None, valign="top"):
    """Auto-fit: start at pt_start, shrink until wrapped block fits box.
    valign: 'top' (default), 'center', or 'bottom' — vertical centering of the
    wrapped block inside the box."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    pad = 6
    for pt in range(pt_start, pt_min - 1, -2):
        fnt = font(kind, pt)
        lines = wrap(text, fnt, bw - 2 * pad)
        lh = int(pt * DPI / 72 * spacing_k)
        if len(lines) * lh <= bh and max(fnt.getlength(l) for l in lines) <= bw - 2 * pad:
            break
    total = len(lines) * lh
    if valign == "center":
        y = y0 + max(pad, (bh - total) // 2)
    elif valign == "bottom":
        y = y1 - pad - total
    else:
        y = y0 + pad
    for ln in lines:
        if align == "left":
            draw.text((x0 + pad, y), ln, font=fnt, fill=fill, anchor="la",
                      stroke_width=stroke, stroke_fill=stroke_fill)
        else:
            draw.text(((x0 + x1) // 2, y), ln, font=fnt, fill=fill, anchor="ma",
                      stroke_width=stroke, stroke_fill=stroke_fill)
        y += lh
    return pt

def draw_one(draw, text, box, kind, pt, fill, anchor, stroke=0, stroke_fill=None):
    x0, y0, x1, y1 = box
    fnt = font(kind, pt)
    cx, cy = {  # anchor shortcuts
        "lt": (x0, y0), "lm": (x0, (y0 + y1) // 2),
        "mm": ((x0 + x1) // 2, (y0 + y1) // 2),
        "mt": ((x0 + x1) // 2, y0),
    }[anchor]
    draw.text((cx, cy), text, font=fnt, fill=fill, anchor=anchor,
              stroke_width=stroke, stroke_fill=stroke_fill)

def frame_for(ptype):
    return {"Basic": "frame_basic", "Rare": "frame_rare",
            "Instant": "frame_instant", "Rare-Instant": "frame_rare"}.get(ptype, "frame_basic")

# Per-art zoom anchors (filename -> (fx, fy) source-relative focus point).
# None/missing = plain center crop. Set fy low to keep a top subject visible.
ART_FOCUS = {
    "sword_of_inspiration.png": (0.5, 0.15),  # soldier's face stays near the top
}

def label_for(ptype):
    return {"Basic": "Basic Item", "Rare": "Rare Item", "Instant": "Instant Item",
            "Rare-Instant": "Rare Instant Item"}.get(ptype, ptype + " Item")

def norm_tag(t):
    if not t:
        return None
    t = str(t).strip().lower().replace("-", "_").replace(" ", "_")
    return t if t in ICON_NAMES else None

# ---------- sheet readers ----------
def read_sheet(ws):
    hdr = [str(c.value).strip() if c.value is not None else "" for c in ws[1]]
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if all(v is None for v in r):
            continue
        rows.append({hdr[i]: ("" if v is None else str(v).strip()) for i, v in enumerate(r) if i < len(hdr) and hdr[i]})
    return rows

def s(v):
    return (v or "").strip()

# ---------- card renderers ----------
# Icons: right-aligned inside the navy plate, centered vertically on it.
# Plate face (on-card, 300dpi px): x 52..771, y 52..145 (measured from frame PNGs).
PLATE_X1 = 771
PLATE_CY = 99            # plate vertical center
ICON_SIZE = 96           # ~0.32 in; pokes above/below plate per design intent
ICON_GAP_OLD = 10          # spacing used to anchor the LEFT icon (kept fixed)
ICON_GAP = 2               # reduced padding between symbols (Curtis 2026-09-09)
def icon_xs(n):
    """Icon centers, ordered by tag (index 0 = Tag1). The RIGHTMOST slot is Tag1
    (same order as the old right-aligned render), so the left symbol never moves
    and the right symbol sits left of the plate edge with reduced gap."""
    leftmost = PLATE_X1 - ICON_SIZE // 2 - (ICON_SIZE + ICON_GAP_OLD) * (n - 1)
    return [leftmost + (ICON_SIZE + ICON_GAP) * (n - 1 - i) for i in range(n)]

def render_item(row, idx):
    c = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(c)
    # art: zoom-crop to fill (no bars); per-art anchor exceptions in ART_FOCUS
    ref = s(row.get("Hyperlink"))
    if ref:
        paste_zoom(c, open_real(ref).convert("RGBA"),
                   (IN(0.175), IN(0.475), IN(0.175) + IN(2.4), IN(0.475) + IN(1.75)),
                   focus=ART_FOCUS.get(ref.split("/")[-1].lower()))
    # frame over art
    paste_stretch(c, open_real(frame_for(s(row.get("Type"))) + ".png").convert("RGBA"),
                  (IN(0.125), IN(0.125), IN(0.125) + IN(2.5), IN(0.125) + IN(3.5)))
    # icons: LEFT-anchored (left symbol stays put), pasted BEFORE title so title can dodge
    tags = [norm_tag(row.get(f"Tag {i}")) for i in (1, 2, 3, 4)]
    icon_lefts = []
    active = [t for t in tags if t]
    for t, x in zip(active, icon_xs(len(active))):
        paste_cp(c, open_real(t + ".png").convert("RGBA"), x, PLATE_CY, ICON_SIZE)
        icon_lefts.append(x - ICON_SIZE // 2)
    # title: single line on the plate, shrink to fit available width (icon-aware)
    title_right = min([624] + [il - 8 for il in icon_lefts])
    title_right = max(title_right, 380)  # floor for 3-4-icon cards
    tx = s(row.get("Name"))
    tpt = 13.0
    tfnt = font("bold", int(tpt))
    while tpt > 7 and tfnt.getlength(tx) > title_right - IN(0.325) - 12:
        tpt -= 0.5
        tfnt = font("bold", int(tpt))
    d.text((IN(0.325), IN(0.35)), tx, font=tfnt, fill="#FFFFFF", anchor="lm")
    # game text: white directly on the navy panel — no box.
    # zone ends above flavor line when flavor exists, else above the divider notch
    fl = s(row.get("Flavor Text"))
    gt_y1 = IN(2.92) if fl else IN(3.10)
    draw_fit(d, s(row.get("Game Text")), (IN(0.425), IN(2.275), IN(0.425) + IN(2.0), gt_y1),
             "reg", 12, 10, "#FFFFFF")
    # flavor
    if fl:
        draw_fit(d, fl, (IN(0.305), IN(2.955), IN(0.305) + IN(2.14), IN(2.955) + IN(0.30)),
                 "ital", 10, 8, "#CCCCCC")
    # type label
    draw_one(d, label_for(s(row.get("Type"))), (IN(0.125), IN(3.19), IN(0.125) + IN(2.5), IN(3.19) + IN(0.30)),
             "bold", 10, "#FFFFFF", "mm")
    return c

def black_border():
    im = Image.open(ROOT / "diplomacy_black_border.png").convert("RGBA")
    a = np.asarray(im)[..., 3]
    return im, float((a < 50).mean())

def render_text_card(title, body_blocks, label, title_pt=17, body_kind="reg",
                     label_top=False):
    """Prompts / Diplomacy style: white card, black decorative border, dark text.
    Border window (inner clear area) spans x 0.37..2.92in, y 0.37..3.38in.
    label_top=True puts the type label at the top of the window (above body text)."""
    c = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(c)
    if title:
        draw_fit(d, title, (IN(0.37), IN(0.40), IN(0.37) + IN(2.01), IN(0.40) + IN(0.60)),
                 "bold", title_pt, 10, "#111111", align="center")
    y = IN(1.12)
    for txt, kind, pt, col, align, h_in in body_blocks:
        if not txt:
            continue
        draw_fit(d, txt, (IN(0.42), y, IN(0.42) + IN(1.91), y + IN(h_in)), kind, pt, 9, col,
                 align=align)
        y += IN(h_in) + IN(0.12)
    if label:
        if label_top:  # top of the border window (title-less cards only)
            draw_one(d, label, (IN(0.37), IN(0.38), IN(0.37) + IN(2.01), IN(0.38) + IN(0.24)),
                     "bold", 10, "#111111", "mm")
        else:
            draw_one(d, label, (IN(0.37), IN(3.14), IN(0.37) + IN(2.01), IN(3.14) + IN(0.22)),
                     "bold", 9, "#111111", "mm")
    return c

PROMPT_BG = (252, 255, 216)  # #fcffd8 — prompts card background (Curtis 2026-09-09)
import re as _re
def _titlecase(t):
    """Capitalize word-initial letters only (letters after ' or ’ stay lowercase)."""
    return _re.sub(r"[A-Za-z]+('|\u2019)?[A-Za-z]*",
                   lambda m: m.group(0)[0].upper() + m.group(0)[1:].lower(), t)
def render_prompts(rows):
    """Prompts: flat #fcffd8 background + Prompts-Frame (top banner, side borders).
    Title = the 2nd column ("Text", e.g. "A favor that backfired") centered in the
    dark top pill, WHITE serif; the internal Title field is NOT shown. Body
    (First + Second fill-in lines) is italicized."""
    out = []
    frame = open_real("Prompts-Frame.png").convert("RGBA")
    for i, row in enumerate(rows, 1):
        c = Image.new("RGBA", (W, H), PROMPT_BG + (255,))
        paste_stretch(c, frame, (0, 0, W, H))
        d = ImageDraw.Draw(c)
        # Title: card's "Text" value, Title-Case, white serif, vertically centered
        # in the dark top pill (card y33..111, center ~72).
        title = _titlecase(s(row.get("Text")))
        draw_fit(d, title, (58, 33, 767, 111),
                 "serifbold", 18, 11, "#FFFFFF", align="center", valign="center")
        # Body: both fill-in lines, italic, dark, left-aligned.
        draw_fit(d, s(row.get("First")), (84, 525, 741, 690),
                 "ital", 12, 9, "#222222", align="left")
        draw_fit(d, s(row.get("Second")), (84, 705, 741, 870),
                 "ital", 12, 9, "#222222", align="left")
        out.append((c, i))
    return out

def render_diplomacy(rows):
    """Diplomacy: green cloud (Player) / red helix (NPC) art background that shows
    through the unnamed.png frame's clear window; PLAYER/NPC label in the top pill."""
    out = []
    frame = open_real("unnamed.png").convert("RGBA")
    bg_cache = {}
    def bg(kind):
        if kind not in bg_cache:
            bg_cache[kind] = open_real("red helix.png" if kind == "npc" else "green cloud.png").convert("RGBA")
        return bg_cache[kind]
    for i, row in enumerate(rows, 1):
        kind = s(row.get("Background")).lower()
        c = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        paste_zoom(c, bg(kind), (0, 0, W, H))   # art fills the whole card
        paste_stretch(c, frame, (0, 0, W, H))    # white frame + top pill + bottom band
        d = ImageDraw.Draw(c)
        # Card type label, vertically centered in the dark top pill (card y42..97,
        # center ~70). Green/Player cards read DIPLOMACY; red/NPC cards stay NPC.
        label = "NPC" if kind == "npc" else "DIPLOMACY"
        draw_one(d, label, (150, 40, 675, 100), "serifbold", 13, "#FFFFFF", "mm")
        # Body: black SANS (not serif — Curtis 2026-09-10), no white halo,
        # centered in the frame's clear window.
        draw_fit(d, s(row.get("Text")), (62, 300, 763, 782),
                 "bold", 17, 11, "#000000", align="center", valign="center")
        out.append((c, i))
    return out

# Challenge text box: the opaque rounded panel in text-box.png, cropped out and
# stretched to a translucent reading panel in the lower art window of each card.
def textbox_panel():
    im = open_real("text-box.png").convert("RGBA")
    a = np.asarray(im)[..., 3]
    ys, xs = np.where(a > 40)
    return im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))

def render_challenges(rows):
    """Challenges: art fills the interior window, translucent text box over the
    lower art, Challenge-Frame on top. Title in the top green bar, flavor text in
    the text box, DIFFICULTY n centered in the bottom bar."""
    out = []
    frame = open_real("Challenge-Frame.png").convert("RGBA")
    panel = textbox_panel()
    for i, row in enumerate(rows, 1):
        c = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        ref = s(row.get("Image"))
        if ref:
            paste_zoom(c, open_real(ref).convert("RGBA"), (42, 111, 782, 986))
        paste_stretch(c, panel, (50, 758, 775, 976))   # translucent text panel
        paste_stretch(c, frame, (0, 0, W, H))           # opaque bars/border over edges
        d = ImageDraw.Draw(c)
        # Title: serif, ONE line (min 8pt so long titles shrink rather than wrap),
        # vertically centered in the green top pill (card y31..111, center ~71).
        draw_fit(d, s(row.get("Title")), (48, 31, 777, 111),
                 "serifbold", 15, 8, "#FFFFFF", align="center", valign="center")
        # Flavor text: italic ivory in the translucent box.
        draw_fit(d, s(row.get("Card Text")), (72, 775, 753, 962),
                 "ital", 13, 9, "#f5f2e8", align="center",
                 stroke=1, stroke_fill=(20, 20, 20))
        # Difficulty: white serif, vertically centered in the bottom green pill
        # (card y988..1070, center ~1029).
        draw_one(d, "Difficulty " + s(row.get("Difficulty")), (60, 990, 765, 1068),
                 "serifbold", 13, "#FFFFFF", "mm")
        out.append((c, i))
    return out

def render_art_cards(rows, arts, section):
    """Monsters & Challenges: art top, black border, dark text below."""
    out = []
    for i, row in enumerate(rows, 1):
        c = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        ref = s(row.get("image url") if section == "monsters" else row.get("Image"))
        if not ref:
            ref = arts.get(i)
        if ref:
            paste_zoom(c, open_real(ref).convert("RGBA"), (IN(0.18), IN(0.88), IN(0.18) + IN(2.39), IN(0.88) + IN(1.10)))
        paste_stretch(c, black_border()[0], (IN(0.10), IN(0.10), IN(0.10) + IN(2.55), IN(0.10) + IN(3.55)))
        d = ImageDraw.Draw(c)
        if section == "monsters":
            draw_fit(d, s(row.get("Name")), (IN(0.37), IN(0.40), IN(0.37) + IN(2.01), IN(0.40) + IN(0.42)),
                     "serifbold", 16, 10, "#111111", align="center")
            draw_one(d, s(row.get("Type")), (IN(0.37), IN(1.96), IN(0.37) + IN(2.01), IN(1.96) + IN(0.24)),
                     "bold", 11, "#333333", "mm")
            draw_one(d, s(row.get("HP text")), (IN(0.37), IN(2.20), IN(0.37) + IN(2.01), IN(2.20) + IN(0.24)),
                     "bold", 11, "#333333", "mm")
            for k, atk in enumerate(("Attack 1", "Attack 2", "Attack 3")):
                draw_fit(d, s(row.get(atk)), (IN(0.42), IN(2.52) + k * IN(0.26), IN(0.42) + IN(1.91), IN(2.52) + k * IN(0.26) + IN(0.25)),
                         "reg", 11, 9, "#111111")
        else:
            draw_fit(d, s(row.get("Title")), (IN(0.37), IN(0.40), IN(0.37) + IN(2.01), IN(0.40) + IN(0.56)),
                     "bold", 16, 10, "#111111", align="center")
            draw_fit(d, s(row.get("Card Text")), (IN(0.42), IN(2.16), IN(0.42) + IN(1.91), IN(2.16) + IN(0.98)),
                     "reg", 12, 10, "#111111")
            draw_one(d, "DIFFICULTY " + s(row.get("Difficulty")), (IN(0.37), IN(3.14), IN(0.37) + IN(2.01), IN(3.14) + IN(0.26)),
                     "bold", 11, "#111111", "mm")
        out.append((c, i))
    return out

# ---------- card backs ----------
BACKS_DIR = BASE / "backs"

def _cover_crop(im, focus_x=0.5, focus_y=0.5):
    """Scale to cover 825x1125, crop centered on the focus point (0..1)."""
    s = max(W / im.width, H / im.height)
    nw, nh = round(im.width * s), round(im.height * s)
    im2 = im.resize((nw, nh), Image.LANCZOS)
    cx, cy = focus_x * nw, focus_y * nh
    left = int(min(max(0, cx - W / 2), nw - W))
    top = int(min(max(0, cy - H / 2), nh - H))
    return im2.crop((left, top, left + W, top + H))

def build_backs():
    """Per-type backs: items=chest, prompts=party, monsters=cat+cube,
    challenges=elder, diplomacy=player sage / npc lizard (per-sheet column).
    All designs are 750x1050 with the frame pattern shifted ~14px left and
    ~24px up, so the focus point re-centers the design on the page."""
    BACKS_DIR.mkdir(exist_ok=True)

    # Measured frame-line offsets in each 750x1050 source (inner window edge
    # distance from each card edge, in source px). Designs are shifted ~10px
    # LEFT (right-side inner gap larger). We zoom slightly and re-center the
    # crop so the frame's inner window is equidistant on left/right.
    SRC_FRAME = {  # name -> (left_inner, right_inner) px from each edge
        "item back.png":        (13, 26),
        "prompt cards.png":     (13, 26),
        "challenge cards.png":  (13, 26),
        "player displomacy.png":(13, 26),
        "npc fixed.png":        (13, 26),
        "monster card.png":     (1, 13),
    }
    def make(src, out_name, fy=0.5):
        im = Image.open(BASE / src).convert("RGB")
        li, ri = SRC_FRAME[Path(src).name]
        s_min = max(W / im.width, H / im.height)
        # horizontal slack needed to re-center: (ri-li) scaled
        hz = abs(ri - li) * s_min + 4
        s = max((W + hz) / im.width, (H + hz * 0.5) / im.height)
        nw, nh = round(im.width * s), round(im.height * s)
        im2 = im.resize((nw, nh), Image.LANCZOS)
        # frame inner-window center x: li*s from left, ri*s from right
        cx_frame = (li * s + (nw - ri * s)) / 2
        left = int(min(max(0, cx_frame - W / 2), nw - W))
        # vertical: keep design centered (TB symmetric per edge scan)
        cy = fy * nh
        top = int(min(max(0, cy - H / 2), nh - H))
        back = im2.crop((left, top, left + W, top + H))
        back.save(BACKS_DIR / out_name)
        print(f"back {out_name:<16s} <- {src} (fy {fy}, crop_x0 {left}, zoom {s:.3f})")
        return back

    make("drive-assets/item back.png", "back_items.png", 0.476)
    make("drive-assets/prompt cards.png", "back_prompts.png", 0.483)
    make("drive-assets/challenge cards.png", "back_challenges.png", 0.481)
    make("drive-assets/player displomacy.png", "back_dip_player.png", 0.481)
    make("drive-assets/npc fixed.png", "back_dip_npc.png", 0.476)
    make("drive-assets/monster card.png", "back_monsters.png")  # square: center
    print(f"6 back designs built into {BACKS_DIR}/")

def back_for(section, row=None):
    """Back image for a card: per-section file; diplomacy splits Player/NPC."""
    if section == "diplomacy" and row is not None:
        kind = s(row.get("Background")).lower()
        return BACKS_DIR / ("back_dip_npc.png" if kind == "npc" else "back_dip_player.png")
    return {"items": "back_items.png", "prompts": "back_prompts.png",
            "monsters": "back_monsters.png", "diplomacy": "back_dip_player.png",
            "challenges": "back_challenges.png"}[section]

def dump(wb):
    items = read_sheet(wb["Items"])
    print(f"== dump: items {len(items)}, prompts {len(read_sheet(wb['Prompts']))}, "
          f"monsters {len(read_sheet(wb['Monsters']))}, diplomacy {len(read_sheet(wb['Diplomacy']))}, "
          f"challenges {len(read_sheet(wb['Challenges']))}")
    tag_census = {}
    for r in items:
        for i in (1, 2, 3, 4):
            t = norm_tag(r.get(f"Tag {i}"))
            raw = s(r.get(f"Tag {i}"))
            if raw:
                tag_census[raw] = tag_census.get(raw, 0) + (1 if t else 0)
    print("tag census (raw -> matched):", tag_census)
    gt = max(items, key=lambda r: len(s(r.get("Game Text"))))
    print(f"longest game text ({len(s(gt.get('Game Text')))} ch): {s(gt.get('Game Text'))[:80]}...")
    ttl = max(items, key=lambda r: len(s(r.get('Name'))))
    print(f"longest title: {s(ttl.get('Name'))}")
    print("types:", sorted({s(r.get('Type')) for r in items}))
    for r in items[:3]:
        print("sample:", {k: r[k] for k in ("Name", "Type", "Tag 1", "Tag 2", "Hyperlink") if k in r})

def main():
    dump_only = "--dump" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]  # e.g. "items:2"
    wb = openpyxl.load_workbook(BASE / "Unified-Cards-Sheet.xlsx", data_only=True)
    if dump_only:
        dump(wb)
        return
    OUT.mkdir(exist_ok=True)
    jobs = []  # (filename, image)
    items = read_sheet(wb["Items"])
    for i, row in enumerate(items, 1):
        jobs.append((f"full-items_{i:02d}.png", lambda r=row: render_item(r, i)))
    for img, i in render_prompts(read_sheet(wb["Prompts"])):
        jobs.append((f"full-prompts_{i:02d}.png", lambda im=img: im))
    for img, i in render_diplomacy(read_sheet(wb["Diplomacy"])):
        jobs.append((f"full-diplomacy_{i:02d}.png", lambda im=img: im))
    mon_rows = read_sheet(wb["Monsters"])
    # 128-card deck: filter monsters to the 8 keepers (1,2,4,5,8,9,10,11,12 minus cuts)
    KEEP_MONSTERS = {2, 4, 5, 8, 9, 10, 11, 12}
    mon_rows = [r for i, r in enumerate(mon_rows, 1) if i in KEEP_MONSTERS]
    for img, i in render_art_cards(mon_rows, {}, "monsters"):
        jobs.append((f"full-monsters_{i:02d}.png", lambda im=img: im))
    ch_rows = read_sheet(wb["Challenges"])
    for img, i in render_challenges(ch_rows):
        jobs.append((f"full-challenges_{i:02d}.png", lambda im=img: im))
    if only:
        sec, n = only.split(":")
        jobs = [j for j in jobs if j[0] == f"full-{sec}_{int(n):02d}.png"]
    for name, fn in jobs:
        im = fn()
        im.save(OUT / name)
        print("wrote", name)
    print(f"{len(jobs)} fronts written to {OUT}")
    if not only:
        build_backs()

if __name__ == "__main__":
    main()
