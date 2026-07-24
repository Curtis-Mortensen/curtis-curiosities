# DNDR Manual Dev Log

This file records implementation decisions, assumptions, and problems encountered while rebuilding the rulebook as LaTeX.

## 2026-07-21 - PDF recreation proof of concept

- The supplied source is an 11-page, US Letter PDF. Page 11 is blank; the recreated document intentionally targets the 10 content pages.
- `DND-5e-LaTeX-Template/example.tex` is retained unchanged as the requested reference.
- Missing logos, photos, character art, dice art, and product graphics are represented by clearly labeled framed placeholders.
- The source is divided into one file per major rules concept: quickstart, player reference, Architect guide, puzzle minigame, and monster manual.
- The bundled Poppler command wrappers failed with a missing-path error. Source pages were rendered for inspection with bundled Python and `pypdfium2` instead.
- No TeX engine was installed at the start of the task. Compilation and rendered QA therefore require a local engine to be installed or downloaded.
- A portable Tectonic 0.16.9 engine was downloaded from its official GitHub release for compilation. The first compile exposed a `geometry` option clash because `dndbook` already loads that package; the document now calls `\geometry{...}` without loading the package twice.
- The first successful render produced 7 pages with clean parchment backgrounds, but compressed the opening rules and monster references too aggressively. Explicit conceptual page breaks now target the source's 10 content pages, and monster table rows have been enlarged for table use.
- The 10-page render exposed excessive unused space caused by the initial 9.1 pt proof body. The body was increased to 10.5 pt with 12.4 pt leading, closer to the measured source typography, and the two major photo placeholders were enlarged.
- Final visual QA rendered all 10 output pages at 1.5x resolution. The parchment background and footer treatment appear on every page; text, placeholders, callouts, the puzzle grid, and monster tables show no clipping or overlap.
- The final compile succeeds. Remaining messages are non-fatal underfull/overfull line warnings plus UTF-8 warnings originating in the downloaded legacy `contour`/`kpfonts` package sources; no replacement-glyph defect was visible in the rendered document.

## 2026-07-24 - Remote integration and repository preservation

- Fast-forwarded the parent repository from `55c0d93` to `70de038`, incorporating four remote commits.
- The incoming Quick Cash Markdown was verified as the complete local transcript plus a new 26-line summary, so the remote version preserves all local content.
- The LaTeX template was a nested repository whose custom rulebook files existed only as untracked additions. A submodule would have referenced an unavailable local commit, so the template is being vendored into the parent repository instead.
- Temporary backups of the local Quick Cash file, the complete DNDR folder, and the nested repository metadata were retained until the parent commit was verified.
- The proof of concept prioritizes recognizable page hierarchy, typography, color, boxes, tables, and content flow over pixel-perfect replacement of unavailable artwork.
- The user explicitly requested the existing template's parchment background even though the supplied reference PDF is plain white. The build therefore enables the full D&D background and footer treatment on every page.
