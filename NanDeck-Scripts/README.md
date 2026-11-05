# NanDeck Scripts

Card pipeline for Curtis's DnDR card project: the original **nanDECK** workflow and the current **Python/PIL render pipeline** that replaced it.

## Current pipeline (Python/PIL)

The active production path. Renders all 128 cards deterministically and compiles a
print-ready CMYK PDF/X for DriveThruCards. Runs from the workspace
(`/home/fin/nandeck-test/drive-test/`) alongside `Unified-Cards-Sheet.xlsx` and
`drive-assets/` — keep that folder structure.

| Script | Purpose |
|---|---|
| `render_full_deck.py` | Renders all card fronts + per-type backs from the workbook. Entry point: `python render_full_deck.py`. Handles asset resolution (extensionless PNGs, placeholder-tile rejection), zoom-crop art, frame overlays, icon placement, per-section layouts. |
| `compile_cmyk_pdfx.py` | Compiles rendered PNGs into `drive-thru-ready-cmyk-pdfx.pdf`: FOGRA39 CMYK, TAC ≤ 240%, K-only darks, PDF/X-1a:2003 OutputIntent, 256 pages in (back, front) order. |
| `verify_order.py` | Verifies all 256 pages are in back-then-face order via raw stream SHA-256 against temp page JPEGs. |
| `audit_assets.py` | Audits the asset tree: finds placeholder tiles vs real art, extensionless PNGs. |
| `qa_sheets_all.py` | Builds QA contact sheets for visual review. |

### Build order

```bash
python render_full_deck.py     # 128 fronts + 6 backs
python verify_order.py         # after compile: 256-page order check
python compile_cmyk_pdfx.py    # final CMYK PDF/X
```

### Key conventions

- **Data source:** `Unified-Cards-Sheet.xlsx` (Google sheet is source of truth; sync before rendering).
- **128 cards** = 56 Items + 18 Prompts + 8 Monsters + 34 Diplomacy + 12 Challenges.
- **Never build 5-card proofs** (standing rule).
- **Card backs:** per-type PNGs in `backs/`, built by `render_full_deck.py build_backs()`.
  Designs are shifted ~10px left in source; the build re-centers by zooming slightly
  and cropping so the frame's inner window is equidistant left/right (frame features
  verified mirrored within 1px).
- **Item title plate:** face x 52..771, icons right-aligned inside the plate
  (ICON_SIZE 96, gap 2px), title pasted after icons and shrinks to dodge.
- **Diplomacy:** green cloud = Player bg, red helix = NPC bg; label at top
  (Player cards read DIPLOMACY, NPC cards read NPC); body text sans, black,
  no panel pasted.
- **Challenges:** art zoom-crop, title one line in top pill, "Difficulty n" above
  the bottom bar's watermark zone.

## Original nanDECK workflow

- `card-layout-workflow.html` — region picker / layout workflow
- `cards.nde`, `cards-drivethrucards.nde`, `diplomacy-margin-test.nde` — nanDECK templates
- `tools/pixels-to-nandeck.py` — convert pixel regions into nanDECK coordinates
- `tools/example-regions.json` — example region spec

The nanDECK path was superseded by the PIL pipeline after Wine rendering proved
unreliable (placeholder tiles, white boxes, hangs). The `.nde` scripts are kept
for reference and the 5-card proof workflow.
