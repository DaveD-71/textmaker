# Project Learning

Current durable project facts, constraints, and decisions for this workspace.

## Workspace

- Workspace root: `<repo-root>`
- Repository: Git repository on branch `main` with remote `origin` -> `git@github.com:DaveD-71/textmaker.git`
- Project memory status: repo-level memory scaffold created on `2026-03-24`; `project-learning.md` and `project-journal.md` are now the main source for ongoing project developments and durable decisions.

## Purpose

- `textmaker` is a textbook-content conversion toolkit centered on Markdown, DOCX, PDF, image OCR, PPTX packaging, and YAML-to-audio workflows.
- The primary publishing goal is converting Markdown textbook content into professionally styled Word documents using Pandoc plus a reusable `reference.docx`.
- The reverse-conversion goal is extracting DOCX content back into unit-level Markdown with assets and style references preserved.

## Core Workflows

- `generate-reference`: build `reference.docx` either from project defaults or from an existing source DOCX.
- `markdown-to-docx`: convert one Markdown file or a folder of Markdown files into a styled DOCX, optionally with a TOC.
- `docx-to-markdown`: convert a DOCX into split Markdown units plus extracted assets and a reference DOCX.
- `split-docx-units`: split a DOCX into per-unit DOCX files based on unit markers.
- `preprocess-docx`, `postprocess-docx`, and `postprocess-markdown`: preserve structural markers and restore DOCX/Markdown formatting details around the Pandoc pipeline.
- `pdf-to-markdown` and `image-to-markdown`: OCR-oriented extraction pipelines for PDFs and images.
- `pptx-to-package`: export PowerPoint decks into structured YAML/JSON packages with extracted assets.
- `yaml-to-audio`: synthesize MP3 assets from YAML dialogue/text fields via Piper.

## Tooling And Dependencies

- Python 3.9+ is required.
- `pandoc` must be installed separately and available on `PATH` for Markdown/DOCX conversions.
- `piper` and `ffmpeg` are required for YAML-to-audio MP3 generation.
- PDF extraction depends on Poppler tools (`pdftotext`, `pdfimages`, `pdftoppm`) and `tesseract` for OCR.
- `docs/requirements.txt` is the documented Python dependency entry point for the local virtual environment workflow.
- Optional document inspection/editing can use Microsoft Word or LibreOffice.

## Operational Conventions

- The Windows entry point is `textmaker.cmd`, which wraps the module CLI commands. It runs `python -m scripts` from the repo root and probes the active machine for common Pandoc, Poppler, and Tesseract install locations before launch.
- `c:\Dev\Code\textmaker` is on the system PATH as the canonical entry point on the primary PC. The OneDrive copy (`C:\Users\daved\OneDrive\Documents\Code\textmaker`) is a sync copy for the second PC; its `textmaker.cmd` uses `%~dp0` so it works regardless of clone location. Both `textmaker.cmd` and `scripts\__main__.py` should be kept in sync between both copies when scripts change.
- Markdown folders passed to `markdown-to-docx` are merged in sorted order, with section breaks inserted between files.
- When `--toc` is used for DOCX generation, the output gets a separate TOC section and page numbering restarts at 1 for the content.
- DOCX-to-Markdown defaults to Heading 1 unit splitting, extracts package media into assets folders, and writes numbered Markdown unit files such as `01-<slug>.md`.
- Shape extraction is a first-class part of the DOCX reverse-conversion workflow; shapes are emitted with stable markers plus XML and JSON sidecars.
- Split DOCX unit filenames follow ASCII lowercase slug conventions with numbered prefixes, and front matter becomes `00-front-matter.docx` unless disabled.
- PPTX package export uses stable per-slide object IDs and currently treats transitions/animations as MVP placeholders.

## Decisions

- Keep the bootstrap file pair synchronized between `%USERPROFILE%\.codex\AGENTS.md` and `<repo-root>\AGENTS.md`.
- Use `<repo-root>\instruction-read-log.csv` as the startup read audit log for this repository now that the local scaffold exists.
- Treat `%USERPROFILE%\.codex\memories\user-learning.md` as canonical user memory and `<repo-root>\user-learning-mirror.md` as the portable mirror copy.
- Use project memory files as the primary ongoing record for project progress, durable decisions, constraints, and roadmap changes, rather than relying on the README for development history.
- For Administrative Writing course DOCX output, map the `Call Out - Check` Quick Part to preparatory process cautions and `Before you write` prompts rather than to general review or checklist blocks.
- Treat the reference DOCX as the canonical source for document-level formatting defaults plus custom semantic styles and callout/table prototypes; apply textbook-specific custom formatting through a rule-based DOCX postprocess layer rather than manual cleanup.
- For the Administrative Writing books, keep Quick Parts only for unit title blocks; apply all other semantic emphasis through paragraph styles rather than callout tables so the page hierarchy stays quieter.
- Preserve the semantic markdown hierarchy as `## unit`, `### framework section`, `#### activity/task`, and avoid using headings for model-text labels such as `Original Version` / `Revised Version`.
- Apply `After List` both after actual list paragraphs and after short follow-on commentary blocks when the paragraph is a prompt-style line such as `Practice ...`, `Reflect:`, or `Example:`.
- When rewriting DOCX XML parts directly, preserve the original root namespace declarations and compatibility prefixes exactly; rewriting `word/styles.xml` without the declared `mc`/`w14+` namespaces corrupts the package for Word even if the visible style data looks valid.

## Constraints

- Preserve UTF-8 encoding for `<repo-root>\instruction-read-log.csv`; if mixed encoding is detected later, archive and recreate the log instead of appending.
- Several key features depend on external binaries, so repo functionality is not self-contained in Python alone.
- The README presents the current workflow as a prototype around Pandoc and generated reference DOCX styling; future changes should preserve that architecture unless intentionally revised.
- Before running Textmaker conversion commands, verify every referenced path with the shell first, including source, reference DOCX, Lua filters, output parent, and temporary copied filter paths. On Windows, do not pass paths containing shell metacharacters such as `&` through `cmd.exe` or fragile `Start-Process -ArgumentList` joins; either invoke through an argument-safe path or copy the referenced file to a no-spaces/no-metacharacters temp path before launching.
- For Advanced Administrative Writing DOCX generation, run the intended Textmaker CLI pipeline with `--reference` passed through to Pandoc as `--reference-doc` and the course Lua Div filter supplied with `--lua-filter`; do not repair generated DOCX style packages by copying XML parts from the reference after conversion.
- For Advanced Administrative Writing DOCX generation, pass `--no-pagebreak-filter`; the Advanced Lua filter suppresses standalone `---` separators, while Textmaker's built-in `pagebreak.lua` incorrectly turns them into page breaks.
- For Advanced Administrative Writing DOCX generation, output goes to `adv/md/working/` alongside the source markdown and reference DOCX — not to `adv/docx/`. The standard build command is: `textmaker.cmd markdown-to-docx --input adv\md\working\aw-adv-all_0516.md --reference adv\md\working\aw-adv-styleref.docx --lua-filter ..\textmaker\scripts\style_bridge.lua --output adv\md\working\aw-adv-all_MMDD.docx --no-pagebreak-filter --apply-semantic-labels` run from `book_administrative-writing\`.
- Treat Pandoc fallback styles such as `Compact` and `VerbatimChar` as cleanup targets in postprocess when they are not present in the reference DOCX; map them to approved reference styles rather than allowing generated-only styles to remain in output.
- For Advanced Administrative Writing alphabetic option lists, use the reference style `List Number 3`; after applying it in postprocess, remove literal source markers such as `A.` from the paragraph text so Word supplies the list label exactly once.
- For Advanced Administrative Writing semantic Div labels, preserve the semantic paragraph style on the label/title line; do not replace it with `Label Base Para`/`Label Para`. Set label paragraph spacing after to 4pt and moved content paragraph spacing before to 0pt.
- For semantic Divs that contain lists, keep the list paragraph style (`List Bullet 2`, `List Number 2`, or `List Number 3`) and copy Div block-level paragraph formatting such as borders/shading onto the list paragraphs as direct paragraph formatting. A Word paragraph cannot hold both the semantic paragraph style and the list paragraph style at once.

## Style-Safe DOCX Pipeline (added 2026-05-15)

The `markdown-to-docx` pipeline for content books now follows a strict style-safety model:

**Single source of truth**: the reference DOCX file is the canonical source for all style definitions. The build pipeline never creates or redefines styles.

**Responsibilities:**

- `style_bridge.lua` — generic Lua filter that reads `style_map` from Pandoc YAML front matter and maps fenced Div classes to `custom-style` attributes. No hardcoded style names.
- `postprocess_docx.py` — structural cleanup only by default. Semantic label rendering (emoji, character styles, unit title tables) requires `--apply-semantic-labels`.
- `manage_docx_styles.py` — explicit manual maintenance tool for updating reference DOCX styles from a YAML spec (`adv/style_specs/aw-div-label-styles.yaml`). **Not part of the automated build.**
- `audit_docx_styles.py` — read-only style inspector; reports style definitions, colors, linked-style pairs, and color-mismatch validation.
- `validate_docx_against_reference.py` — post-build validator; checks that all styles used in generated DOCX exist in the reference DOCX. Hard-fails on mismatch.

**Three-location color rule**: Div label paragraph styles must keep `w:rPr/w:color/@w:val`, `w:rPr/w14:srgbClr/@w14:val`, and the linked character style `w:rPr/w:color/@w:val` in sync. `manage_docx_styles.py` updates all three atomically.

**postprocess_docx.py `--apply-semantic-labels` flag**: added 2026-05-15. Previously `semantic_formatting=True` was the default. The old `--no-semantic-formatting` flag is kept as a deprecated no-op for backward compatibility.

**cli.py bug fixed 2026-05-15**: `insert_section_after_toc()` call was indented inside the `except ImportError` block and never ran when invoked as a package. Now correctly called after the try/except.

**postprocess_docx.py additions (2026-05-17)**:

- `apply_checklist_style()` — applies `Checklist` style to bullet items inside `Self-Editing Checklist` edit divs.
- `apply_example_block_styles()` — applies `AW Example Good`/`AW Example Bad`/`AW Example` to body paragraphs after matching Div Label paragraph.
- `apply_spacing_after_lists()` — adds 120-twip `w:spacing/@w:after` to prose paragraphs following list paragraphs (replaces deleted `After List` style).
- `apply_table_styles()` — applies `AW Standard Table` to all unstyled tables.
- `replace_unit_headings_with_title_tables()` ungated from `apply_semantic_labels` — now runs whenever `--reference-doc` is supplied.
- Duplicate `apply_semantic_div_labels` call removed from flow.

**Div style naming convention (2026-05-17)**: all Div paragraph styles in the reference DOCX are named `Div Label *` (10-char prefix). `style_bridge.lua` `is_div_label_style()` checks `style_name:sub(1, 10) == "Div Label "`. Any new Div styles must follow this prefix.

**Reference DOCX `Div Label Example Good/Bad` (2026-05-17)**: added paragraph styles (`2C9167` green for Good, `E36C0A` orange for Bad) and linked character styles. `apply_example_block_styles()` applies body text to content paragraphs after the label.

**`Body Text` style name**: reference DOCX uses `Body Text` (styleId `BodyText`). Any source that generates `Body Text1` or `AW Body Text` must be corrected; postprocessor maps normal paragraphs to this style by name.

**OOXML caps toggle property (2026-05-18)**: bare `<w:caps/>` in a character style is treated as "not set" by Word. Must be `<w:caps w:val="1"/>` to honour all-caps. This applies to all toggle properties in character styles — underline was unaffected because `<w:u>` already required `w:val="single"` by spec. Fix: patch reference DOCX char styles directly via XML.

**Section break page size (2026-05-18)**: any `sectPr` inserted by the postprocessor must copy `w:pgSz` and `w:pgMar` from the document-level `sectPr`. Without this, Word uses its application default (US Letter) for the new section regardless of the document's paper size. Both `_insert_section_break_before_paragraph()` and `_apply_next_page_section_to_paragraph()` now copy these elements.

**H1 section break skip (2026-05-18)**: `insert_section_breaks_before_h1()` must always use `skip_first=True`. The first H1 is the cover title — inserting a section break before it pushes the title onto a new page. The `skip_first=has_toc` logic was incorrect; when no TOC is present `has_toc=False` and the cover title was getting a spurious section break.

**Div label icon table layout (2026-05-18)**: `apply_semantic_div_labels()` now performs a single-pass replacement: each `DivLabel*` paragraph is replaced with a 2-column `<w:tbl>` (icon left, label text right) in one step. Table uses `TableGrid` style with explicit `none` borders (suppresses visible borders, preserves gridlines toggle). Left cell uses `DivTag` paragraph style (inherits spacing from `Div Label Base`) — never hardcode spacing values. Example divs (neutral/good/bad) are excluded from icon tables.

**Pandoc fenced div spacing rule (2026-05-18)**: a `:::` open fence must be preceded by a blank line when the preceding line is non-empty. Violations cause Pandoc to emit the fence as literal text. The systematic pattern to watch: bold label lines (`**Input N — ...**`) immediately followed by `:::` with no blank line. Also: a list must not immediately follow a `:::` open fence without a blank line gap.

**Nested div policy (2026-05-18)**: Pandoc does not support nested fenced divs — an inner `:::` close terminates the outer div. Thin nested divs (title-only, no body) that add no student learning value should be removed: confirmed removals are `learn "Functions"`, `language "Learn — Sentences"`, `language "Learn — Useful Language"`, `language "Learn — Patterns"`, `learn "Statements"`, `learn "Annotations"`, `learn "Discuss"`, `learn "Revision Checklist"`. Meaningful sub-labels (`Version A/B`, `Original`, `Proposed Changes`, `Scenario`) are kept. 233 substantive nested divs remain unresolved — full fix requires content-level decisions.

**Div Label style architecture (2026-05-18)**: linked paragraph+character style pairs have been replaced by paragraph-only styles. All 12 `DivLabel*Char` character styles and `w:link` references have been removed from the reference DOCX. `postprocess_docx.py` reads color directly from paragraph style `rPr` and applies color + `Noto Sans Condensed Medium` font directly to label runs. `Div Label Base` is the single source of truth for font, size, and spacing.

**DivTag style (2026-05-18)**: `DivTag` must be a character style (not paragraph) with `w:position w:val="-8"` so Word applies the 4pt baseline lowering to icon runs via `w:rStyle`. Defining it as a paragraph style causes `w:rStyle` references to be silently ignored.

**AW Table styles (2026-05-18)**: all 4 AW Table styles (`AWStandardTable`, `AWComparisonTable`, `AWPhraseBankTable`, `AWRubricTable`) use 100% width (`pct`), `autofit` layout, left-aligned paragraphs, `suppressAutoHyphens`, first-row bold/white/`2D4155` fill, and cell margins top/bottom=57 twips (0.1 cm), left/right=113 twips (0.2 cm). Width and layout must also be enforced directly on each table element by the postprocessor — Pandoc's generated `tblW` overrides style-level defaults.

**`autoRedefine` removed from DivLabel styles (2026-05-18)**: `w:autoRedefine` has been removed from all DivLabel paragraph styles. It is no longer needed now that child styles carry only `w:color` in their `rPr` — Word's normal inheritance cascades font/size/spacing from `Div Label Base` correctly. `autoRedefine` caused silent style corruption in output files.

**`--tag-style` CLI flag (2026-05-18)**: `markdown-to-docx` now accepts `--tag-style filled|outline` (default `filled`) to select the icon variant inserted before Div label text. Was previously only available when running `postprocess_docx.py` directly.

**Tag icon assets (2026-05-18)**: all `tag_filled_*` and `tag_outline_*` PNGs in the working assets folder are tight-cropped to content bounds + 1px padding. `tag_filled_*` was done in session 6; `tag_outline_*` cropped in session 9.

**Pipe table `<br>` tags (2026-05-18)**: `markdown+fancy_lists` does not process raw HTML in table cells. `<br>` renders as literal text. Use ` / ` as a visual separator for multi-item cells, or switch to grid table format (`+---+---+`) for multi-line cell content.

**AW Table styles — final architecture (2026-05-18 session 10)**: Word's table-style `rPr` is overridden by paragraph styles in cell content. The solution is two dedicated paragraph styles — `AW Table Header` (Roboto Condensed Medium 11pt, white, bold) and `AW Table Body` (Noto Sans Condensed Light 11pt, after=60, suppressAutoHyphens, keepLines) — applied by the postprocessor to header-row and body-row cells respectively. Table styles handle borders (single 1pt `sz=8`, auto color), cell margins (top/bottom=57, left/right=142 twips), 100% width, autofit, and tblLook firstRow=1. Header fill `31849B` is in the firstRow conditional `tcPr`. Direct `tblW`/`tblLayout` enforcement on each table element remains in `apply_table_styles()` to override Pandoc's generated values.

**`apply_example_block_styles()` `_seen_italic` rule (2026-05-19 session 15)**: uses `_seen_italic` flag to distinguish ADV-style examples (italic content) from INT-style examples (plain non-italic text). If no italic content has been seen yet when a non-italic `Body Text` paragraph appears, it is treated as INT-style example content and styled. Once italic content has been seen, the first non-italic `Body Text` paragraph is treated as the task instruction boundary and stops styling. This means INT examples (plain email-style text) are fully styled, while ADV examples (italic text followed by a task instruction) still stop at the task instruction boundary. Previously the function only styled italic body text and the `_example_seen_prose` (session 10) / plain-stop (session 11) approaches caused INT examples to produce only 14 styled paragraphs; after the fix: 179 (INT) and 234 (ADV).

**Misplaced div fence pattern (2026-05-18 session 10)**: two `rewrite` divs had their setup instruction + `example` sub-div inside the div instead of before it (L2143, L7323). Fixed by moving the setup line and example outside the `:::rewrite` open. The `notice` divs with "Read the following..." are correctly structured — those lines are task instructions that belong inside the div.

**HTML underline tags in markdown**: malformed `<uTEXT</u` tags (missing `>`) render as literal text in Pandoc. Correct form is `[TEXT]{.underline}` (Pandoc native span syntax). Fixed 5 instances at L2450–2454.

**Placeholder spacer (2026-05-18 session 10)**: `SPACER_HEIGHT` increased from `'140'` (7pt) to `'280'` (14pt) for clearer visual separation between consecutive placeholder tables.

## 2026-06-01 - INT Placeholder Tables And PDF Export

- Status: `active`
- Scope: project/tooling
- Decision: `apply_response_placeholders()` now honors explicit marker payloads such as `{{PH-1: id | rows=5}}`; `rows=N` overrides the PH fallback row count and is not treated as part of the display label.
- Decision: when a response placeholder follows a numbered/bulleted/checklist list, the postprocessor normalizes the whole contiguous preceding list run so list numbers sit at the left margin and list text uses a hanging indent at 357 twips. The placeholder table left border aligns to that list text indent and the table width is absolute, extending to the right margin.
- Update: the list-indent/table-indent rule applies only to Case 1, where each list item is followed by its own placeholder. Case 2, where one placeholder follows a complete multi-item list, keeps the list and table in their normal positions.
- Decision: `docx-to-pdf` no longer delegates to `docx2pdf.SaveAs(FileFormat=17)`. It uses Word COM `ExportAsFixedFormat`, matching Word's manual Export path more closely after the automated PDF showed list-numbering restarts that were not present in the DOCX or a manual Word-exported PDF.
- Preferred behavior: for print-readiness validation, treat DOCX numbering as source of truth first. If a generated PDF shows list numbering that differs from the DOCX and manual Word Export, debug the PDF export path before changing manuscript source.

## Roadmap From README

- Improve `reference.docx` to support running headers with chapter titles and page numbers.
- Add automated merging of multiple chapters plus front and back matter.
- Add automated image handling for placement, captions, and numbering.
