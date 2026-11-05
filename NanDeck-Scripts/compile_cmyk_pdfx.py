#!/usr/bin/env python3
"""
compile_cmyk_pdfx.py - Build a CMYK PDF/X-1a:2003 candidate for DriveThruCards.

Pipeline (per 825x1125 page image):
  1. Flatten RGBA onto white.
  2. sRGB -> CMYK via real ICC Coated FOGRA39 profile (ArgyllCMS colprof from
     FOGRA39L CGATS measurement data), relative colorimetric + BPC.
  3. Out-of-gamut pixels: re-take from a perceptual-intent transform.
  4. Dark neutral pixels (text / frame cores) -> K-only black (0,0,0,255).
  5. Total-ink clamp to 240% (scale CMY, preserve K).
  6. Save as CMYK JPEG (quality 95, 4:4:4 no chroma subsampling, 300 dpi).
  7. Assemble back-then-face page order with img2pdf; post-process with
     pikepdf: OutputIntent (the ICC), XMP GTS_PDFXVersion, Trapped=false,
     force PDF 1.4.

Usage:
  python3 compile_cmyk_pdfx.py --test     # 2 pages only (back + first item)
  python3 compile_cmyk_pdfx.py            # full 256-page build
"""
import argparse
import io
import json
import time
from pathlib import Path

import numpy as np
import openpyxl
import img2pdf
import pikepdf
from PIL import Image, ImageCms

BASE = Path("/home/fin/nandeck-test/drive-test")
FRONT_DIR = BASE / "full-output"
OUT_DIR = BASE / "full-deck-output"
OUT_PDF = OUT_DIR / "drive-thru-ready-cmyk-pdfx.pdf"
TMP_JPEG_DIR = BASE / "full-deck-output" / "cmyk-jpeg-tmp"
ICC_PATH = BASE / "icc-work" / "coated_fogra39_lut.icc"
STATS_PATH = OUT_DIR / "cmyk-compile-stats.json"

PAGE_W_PX, PAGE_H_PX = 825, 1125
DPI = 300
TAC_LIMIT_PCT = 240.0
JPEG_QUALITY = 95

# K-only forcing: dark neutral detection (text / frame cores).
DARK_MAX_C = 80     # max(R,G,B) <= this  (~<= 31% brightness)
DARK_CHROMA = 20    # max-min <= this    (near neutral)

# Section order (same as previous compile), monsters filtered to keepers.
SECTIONS = {
    "items": range(1, 57),
    "prompts": range(1, 19),
    "monsters": [2, 4, 5, 8, 9, 10, 11, 12],  # cut: 1,3,6,7,13
    "diplomacy": range(1, 35),
    "challenges": range(1, 13),
}
BACK_PATH = BASE / "card_back.png"


def build_transforms():
    srgb = ImageCms.createProfile("sRGB")
    cmyk = ImageCms.ImageCmsProfile(str(ICC_PATH))
    common = dict(renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC)
    t_rel = ImageCms.buildTransform(
        srgb, cmyk, "RGB", "CMYK",
        flags=ImageCms.Flags.BLACKPOINTCOMPENSATION, **common)
    t_inv = ImageCms.buildTransform(
        cmyk, srgb, "CMYK", "RGB",
        renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC)
    t_per = ImageCms.buildTransform(
        srgb, cmyk, "RGB", "CMYK",
        renderingIntent=ImageCms.Intent.PERCEPTUAL)
    return t_rel, t_inv, t_per


def to_cmyk(rgb: Image.Image, tf):
    """rgb: RGB PIL image -> (cmyk uint8 HxWx4, oog_count, k_only_count, max_tac_pct)

    OOG detection via round trip: pixels whose color visibly changes after
    CMYK->RGB inversion are clipped by the relative transform; those get the
    perceptual-intent result instead (smooth compression, no hard clipping).
    """
    t_rel, t_inv, t_per = tf
    c_rel = np.array(ImageCms.applyTransform(rgb, t_rel), dtype=np.uint8, copy=True)
    rgb_rt = ImageCms.applyTransform(Image.fromarray(c_rel, mode="CMYK"), t_inv)
    diff = np.abs(np.asarray(rgb).astype(np.int16) - np.asarray(rgb_rt).astype(np.int16)).sum(axis=2)
    oog_mask = diff > 45
    oog = int(oog_mask.sum())
    if oog:
        c_per = np.asarray(ImageCms.applyTransform(rgb, t_per), dtype=np.uint8)
        c_rel[oog_mask] = c_per[oog_mask]
    cmyk = c_rel.copy()

    # dark-neutral -> K-only black
    rgb_np = np.asarray(rgb)
    mx = rgb_np.max(axis=2).astype(np.int32)
    chroma = (rgb_np.max(axis=2).astype(np.int32) - rgb_np.min(axis=2).astype(np.int32))
    dark = (mx <= DARK_MAX_C) & (chroma <= DARK_CHROMA)
    k_only = int(dark.sum())

    # TAC clamp: sum of bytes <= 240/100*255 = 612.
    # Budget approach: allowed CMY sum = 612 - K; scale CMY down to that budget,
    # keep K untouched (K carries detail; new total lands exactly at 612).
    k_arr = cmyk[..., 3].astype(np.float64)
    cmy_sum = cmyk[..., 0:3].astype(np.float64).sum(axis=2)
    total = cmy_sum + k_arr
    over = total > 612.0
    if over.any():
        scale = np.ones_like(total)
        nz = over & (cmy_sum > 0)
        scale[nz] = (612.0 - k_arr[nz]) / cmy_sum[nz]
        for ch in range(3):
            ch_scaled = np.floor(cmyk[..., ch].astype(np.float64) * scale)
            ch_final = np.where(over, ch_scaled, cmyk[..., ch].astype(np.float64))
            cmyk[..., ch] = np.clip(ch_final, 0, 255).astype(np.uint8)
    cmyk[dark] = (0, 0, 0, 255)

    total_after = cmyk.astype(np.int32).sum(axis=2)
    max_tac = float(total_after.max() / 255.0 * 100.0)
    return cmyk, oog, k_only, max_tac


def page_jpeg(cmyk: np.ndarray) -> bytes:
    im = Image.fromarray(cmyk, mode="CMYK")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_QUALITY, subsampling=0, dpi=(DPI, DPI))
    return buf.getvalue()


def collect_pages():
    """Pages in DTC order: (back, front) repeating = 2N pages for N cards.
    Backs are PER-TYPE: each section uses its own back design; diplomacy
    splits Player/NPC per the sheet's Background column."""
    pages = []
    BACKS = BASE / "backs"
    back_files = {"items": "back_items.png", "prompts": "back_prompts.png",
                  "monsters": "back_monsters.png", "challenges": "back_challenges.png"}
    for sec, back_name in back_files.items():
        p = BACKS / back_name
        if not p.exists():
            raise SystemExit(f"per-type back missing: {p}")
    wb = openpyxl.load_workbook(BASE / "Unified-Cards-Sheet.xlsx", data_only=True)
    dip = wb["Diplomacy"]
    hdr = [str(c.value).strip() if c.value else "" for c in dip[1]]
    bi = hdr.index("Background")
    dip_kinds = {}
    for i, r in enumerate(dip.iter_rows(min_row=2, values_only=True), 1):
        if r and any(v is not None and str(v).strip() for v in r):
            dip_kinds[i] = "npc" if (bi < len(r) and r[bi] and str(r[bi]).strip().lower() == "npc") else "player"
    for sec, idxs in SECTIONS.items():
        for i in idxs:
            p = FRONT_DIR / f"full-{sec}_{i:02d}.png"
            if not p.exists():
                raise SystemExit(f"missing front: {p}")
            if sec == "diplomacy":
                kind = dip_kinds.get(i, "player")
                back = BACKS / ("back_dip_npc.png" if kind == "npc" else "back_dip_player.png")
                if not back.exists():
                    raise SystemExit(f"diplomacy back missing: {back}")
            else:
                back = BACKS / back_files[sec]
            pages.append(("back", back))
            pages.append((f"{sec}-{i:02d}", p))
    assert len(pages) % 2 == 0, f"page count must be even (back-then-face pairs), got {len(pages)}"
    # structural check: even index = back, odd index = front
    for i, (lbl, _) in enumerate(pages):
        if i % 2 == 0 and lbl != "back":
            raise SystemExit(f"page {i+1} should be a back, got {lbl}")
        if i % 2 == 1 and lbl == "back":
            raise SystemExit(f"page {i+1} should be a front, got back")
    # back census: confirm every back file exists and count which sections use which
    from collections import Counter
    census = Counter(str(p.name) for lbl, p in pages if lbl == "back")
    print("back design census:", dict(census))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="back + first item only")
    ap.add_argument("--limit", type=int, default=0, help="cap page count")
    args = ap.parse_args()

    assert ICC_PATH.exists(), f"missing ICC profile: {ICC_PATH}"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_JPEG_DIR.mkdir(parents=True, exist_ok=True)

    entries = collect_pages()
    if args.test:
        # first card pair only: back + front
        entries = entries[:2]
    if args.limit:
        entries = entries[: args.limit]
    n_fronts = sum(1 for lbl, _ in entries if lbl != "back")
    print(f"pages to compile: {len(entries)} ({n_fronts} fronts, {len(entries)-n_fronts} backs)")

    tf = build_transforms()
    stats = []
    jpeg_paths = []
    t0 = time.time()
    for idx, (label, path) in enumerate(entries, 1):
        im = Image.open(path).convert("RGBA")
        if im.size != (PAGE_W_PX, PAGE_H_PX):
            raise SystemExit(f"{path}: wrong size {im.size}")
        white = Image.new("RGBA", im.size, (255, 255, 255, 255))
        rgb = Image.alpha_composite(white, im).convert("RGB")
        cmyk, oog, k_only, max_tac = to_cmyk(rgb, tf)
        jp = TMP_JPEG_DIR / f"page_{idx:03d}_{label}.jpg"
        jp.write_bytes(page_jpeg(cmyk))
        jpeg_paths.append(jp)
        stats.append(dict(page=idx, label=label, oog=oog, k_only=k_only, max_tac_pct=round(max_tac, 1)))
        if idx % 20 == 0 or idx == len(entries) or args.test:
            print(f"  {idx}/{len(entries)}  {label:18s} oog={oog:6d} konly={k_only:6d} tac={max_tac:5.1f}%  ({time.time()-t0:.0f}s)")

    oog_total = sum(s["oog"] for s in stats)
    tac_max = max(s["max_tac_pct"] for s in stats)
    tac_pages_over = sum(1 for s in stats if s["max_tac_pct"] > TAC_LIMIT_PCT + 0.01)
    print(f"conversion done in {time.time()-t0:.0f}s | OOG px total={oog_total} | global max TAC={tac_max}% | pages>240%={tac_pages_over}")

    # ---- assemble PDF with img2pdf (DCT CMYK) ----
    layout = img2pdf.get_fixed_dpi_layout_fun((DPI, DPI))
    pdf_bytes = img2pdf.convert(
        [str(p) for p in jpeg_paths],
        layout_fun=layout,
        title="Throwing Starfish Studios - 128 Card Deck (DTC print)",
        author="Throwing Starfish Studios",
        creator="nanDECK 1.28.1 + Fin CMYK PDF/X pipeline",
    )
    raw_pdf = OUT_DIR / "_raw_img2pdf.pdf"
    raw_pdf.write_bytes(pdf_bytes)
    print(f"img2pdf base written: {raw_pdf.stat().st_size/1e6:.1f} MB")

    # ---- post-process to PDF/X-1a:2003 ----
    icc_bytes = ICC_PATH.read_bytes()
    with pikepdf.open(raw_pdf) as pdf:
        icc_stream = pdf.make_stream(icc_bytes)
        icc_stream.Type = pikepdf.Name("/ICCProfile")
        icc_stream.N = 4
        out_intent = pikepdf.Dictionary(
            Type=pikepdf.Name("/OutputIntent"),
            S=pikepdf.Name("/GTS_PDFX"),
            OutputConditionIdentifier="Coated FOGRA39 (FOGRA39L, argyll colprof)",
            Info="Coated FOGRA39 CMYK profile built from FOGRA39L CGATS data",
            RegistryName="http://www.color.org",
            DestOutputProfile=icc_stream,
        )
        pdf.Root.OutputIntents = pikepdf.Array([out_intent])
        with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
            meta["dc:title"] = "Throwing Starfish Studios - 128 Card Deck (DTC print)"
            meta["xmp:CreatorTool"] = "nanDECK 1.28.1 + Fin CMYK PDF/X pipeline"
            meta["pdfxid:GTS_PDFXVersion"] = "PDF/X-1a:2003"
            meta["pdf:Trapped"] = "False"
        pdf.docinfo[pikepdf.Name("/Trapped")] = pikepdf.Name("/False")
        pdf.save(OUT_PDF, force_version="1.4")
    raw_pdf.unlink()
    print(f"final PDF: {OUT_PDF}  ({OUT_PDF.stat().st_size/1e6:.1f} MB)")

    summary = dict(
        pages=len(entries), fronts=n_fronts, backs=len(entries) - n_fronts,
        order="back-then-face",
        icc_profile="Coated FOGRA39 (colprof from FOGRA39L.ti3, argyll 3.1.0)",
        intent="relative colorimetric + BPC, perceptual for OOG",
        k_only_policy=f"dark neutral (max<= {DARK_MAX_C}, chroma<= {DARK_CHROMA}) -> 0/0/0/100",
        tac_limit_pct=TAC_LIMIT_PCT,
        global_max_tac_pct=tac_max,
        pages_over_tac=tac_pages_over,
        oog_pixels_total=oog_total,
        jpeg_quality=JPEG_QUALITY, jpeg_subsampling=0,
        output=str(OUT_PDF),
    )
    STATS_PATH.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
