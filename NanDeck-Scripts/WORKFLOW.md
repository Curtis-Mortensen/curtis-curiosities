# Pipeline Workflow

End-to-end procedure for the drive-thru cards deck. Companion to README.md (script
reference). The live session state also lives in the Hermes wiki
(`wiki/nandeck/drive-thru-cards-session-state.md`); this file mirrors the durable parts.

## 1. Data flow

```
Google Sheet "Unified-Cards-Sheet" (source of truth)
        │  sync: $GAPI sheets get/update, or re-download xlsx
        ▼
Unified-Cards-Sheet.xlsx  ──►  render_full_deck.py ──► full-output/full-<section>_<n>.png
                               build_backs()        ──► backs/back_<type>.png
        ▼
compile_cmyk_pdfx.py ──► full-deck-output/drive-thru-ready-cmyk-pdfx.pdf (256 pages)
        ▼
verify_order.py (stream-hash page order check)
```

- Google sheet ID: `1s0V1Ha4vOlgbLh5692gTPbKExTIa4lWNND4UQlvrcqA`
- Cell edits go to the Google sheet first, then the local xlsx (keep both in sync).
- Excel date-mangling trap: text like `3-4` / `4/5` becomes datetimes in xlsx —
  store as strings; diff local vs Google cell-by-cell after any sync.

## 2. Spell-check before rendering

pyspellchecker (installed in the Hermes venv; no aspell/hunspell on the server).
Real fixes so far: Warrent→Warrant, whos→whose, randmo→random. Intentional
non-words to whitelist: dmg, Lockpick, Cotion of Ponfusion, Owlbear, etc.
`Challenges!D2 = warrent.png` is an art filename — harmless, do not "fix".

## 3. Render + compile

```bash
python render_full_deck.py       # fronts + backs (backs re-center automatically)
python compile_cmyk_pdfx.py      # CMYK PDF/X-1a:2003, FOGRA39, TAC<=240%
python verify_order.py           # 256 pages, back-then-face, 0 mismatches expected
```

- Page order: (back, front) × 128. Page 1 = back. Never ship front-only.
- verify by raw stream SHA-256; pymupdf-decoded buffers differ ≤4 levels (decode
  quirk) — never pixel-compare pymupdf output.
- pikepdf embeds timestamps → PDF SHA changes every rebuild even with identical
  page content. Compare page hashes, not file SHA, when content shouldn't change.

## 4. Known quirks

- **Extensionless PNGs:** frames (`frame_basic`, `frame_instant`) and 12 tag icons
  exist without `.png` extensions in `drive-assets/`. `open_real()` in
  render_full_deck.py resolves this — don't re-copy.
- **Root-dir placeholder tiles:** copies of assets in the working-dir root can be
  literal red/green placeholder tiles. `open_real()` prefers real art and rejects
  flat tiles (std < 18). Audit with audit_assets.py.
- **`frame_rare`** never existed; a warm-tinted copy of frame_instant is the fallback.
- **Monsters:** only 8 keepers (Gnome, Minotaur, Owlbear, Werewolf, Dancing Armor cut).
  Overview sheet row 9 "Target: 130" is stale — final is 128.
- **Diplomacy backgrounds:** green cloud / red helix have bright glow regions that
  read panel-ish but are pure art (no baked-in text box; frame body window is ~95%
  transparent).

## 5. Delivery + preflight gates

- Stage deliverables: `install -m 644 <pdf> /tmp/` (server /home/fin is 700; scp in
  as fin is impossible). Curtis pulls:
  `scp curtis@192.168.1.83:/tmp/<file> $HOME\Downloads\` — /tmp wiped on reboot, verify first.
- **Curtis's manual gates:** 5-card DTC upload test (never build these as the agent),
  physical print proof (inspect all four edges).
- veraPDF preflight (PDF/A flavour only; PDF/X posture is by-construction):
  `sg docker -c "docker run --rm -v $PWD:/data ghcr.io/verapdf/cli:latest -f 1b --format json /data/file.pdf"`

## 6. Editing the scripts

- render_full_deck.py resolves paths relative to its own location (BASE) — keep the
  workspace folder structure (xlsx + drive-assets/ siblings).
- Layout constants worth knowing: plate face x 52..771 @300dpi; icon slots
  ICON_SIZE=96, rightmost = Tag1; prompt pill y 33..111; challenge pills y 31..111
  and y 988..1070; diplo label y 42..97; diplo body window (62,300)-(763,782).
- After any layout change: render → verify counts in Python → ONE QA contact sheet
  → fix → compile. Don't burn cycles on per-asset visual exploration; measure with
  numpy/PIL and decide from code.
