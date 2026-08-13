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
- For Speaking with PowerPoint appendix model slide decks, do not continue the custom PptxGenJS shape/template approach unless the user explicitly reverses this decision. The user wants standard PowerPoint-native layouts/placeholders so PowerPoint Designer can improve the slides; slide content should identify one or two emphasis points and represent emphasis through standard layout hierarchy, not bespoke boxes, arrows, or handmade graphic systems.

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
- Decision: when a response placeholder follows a numbered list item in Case 1, the postprocessor normalizes that item so the list number sits at the left margin and the list text uses a hanging indent at 357 twips. The placeholder table left border aligns to that list text indent and the table width is absolute, extending to the right margin.
- Update: the list-indent/table-indent rule applies only to Case 1, where each list item is followed by its own placeholder. Case 2, where one placeholder follows a complete multi-item list, keeps the list and table in their normal positions.
- Update: bullet lists and checklist listws are excluded from the special Case 1 placeholder-alignment rule. Pandoc/Word may assign separate numbering IDs to checklist rows, which can make the final checkbox look like a one-item list; forcing the Case 1 indent on that final checkbox causes visible misalignment.
- Decision: `docx-to-pdf` no longer delegates to `docx2pdf.SaveAs(FileFormat=17)`. It uses Word COM `ExportAsFixedFormat`, matching Word's manual Export path more closely after the automated PDF showed list-numbering restarts that were not present in the DOCX or a manual Word-exported PDF.
- Preferred behavior: for print-readiness validation, treat DOCX numbering as source of truth first. If a generated PDF shows list numbering that differs from the DOCX and manual Word Export, debug the PDF export path before changing manuscript source.

## 2026-06-02 - Section-Based Running Headers Replace Hidden Heading Anchors

- Status: `active`
- Scope: project/tooling
- Decision: running headers should not depend on hidden `Heading 2` paragraphs kept only for `STYLEREF`. Hidden heading anchors interact badly with `Heading 2` styles that have `pageBreakBefore`, causing blank pages before units.
- Implementation: `postprocess_docx.py` now removes `pageBreakBefore` from generated Heading 1/2 styles, inserts real section breaks before module/unit boundaries, writes literal module/unit header text into each section header, and removes the original Unit Heading 2 paragraph after inserting the unit title table.
- Validation: targeted DOCX test produced separate module/unit sections, no hidden body paragraphs, no remaining Heading 2 body anchors after unit-title replacement, no direct heading page breaks, and literal module/unit text in section headers.
- Preferred behavior: use section context for running headers. Do not reintroduce hidden heading text as a header anchor unless section-based headers are proven impossible.

## 2026-06-02 - DOCX Conversion Profiling And Source-Driven Div Content Styles

- Status: `active`
- Scope: project/tooling
- Decision: `markdown-to-docx` and `postprocess-docx` now emit routine `[progress]` start/end logs, watchdog `[warn]` messages for long stages, and optional `[profile]` timing summaries. Use `--progress-warn-seconds N` to tune warning cadence.
- Decision: example/model paragraph styling must be driven by explicit Markdown div classification. `style_bridge.lua` supports `div_content_style_map` in YAML front matter so `example`, `example-good`, and `example-bad` content can receive `AW Example`, `AW Example Good`, and `AW Example Bad` during Pandoc conversion.
- Decision: phrase/quotation-based semantic style inference is retired for the INT source-driven path. `apply_example_block_styles` and the old semantic paragraph style inference are skipped in the postprocess pipeline; do not reintroduce model styling based only on text such as `Original Version`, quotation marks, or incidental Word quote styles.
- Performance note: measured INT temp DOCX conversion improved from ~258s total to ~117s total after adding source-driven example styles, skipping heuristic semantic passes, optimizing list-spacing traversal, and converting body-text normalization to direct XML style assignment.
- Preferred behavior: if content needs a semantic style, add the correct div class and `div_content_style_map` entry in source front matter instead of adding another postprocessor guess.

## 2026-06-02 - List Spacing And Alphabetic List Regression Check

- Status: `active`
- Scope: project/tooling
- Decision: `_is_list_paragraph()` must treat `Checklist` styles as list paragraphs for spacing and placeholder-adjacent policy decisions; otherwise checkbox/checklist runs can miss post-list spacing.
- Decision: alphabetic option conversion must accept both `A.` and `A)` literal source markers. Pandoc may emit `UpperAlpha/OneParen` lists for `A)` source text, but the postprocessor should still support literal-marker fallback and marker stripping for both forms.
- Validation: targeted temporary DOCX probe confirmed `list styles`, `post-list spacing`, and `response placeholders` passes still run after the profiling/source-driven refactor; repo tests passed afterward.
- Constraint: Pandoc DOCX output may strip `- [ ]` task-list checkbox markers before postprocessing, leaving ordinary bullet paragraphs. Do not rely on postprocess-only text inspection to recover checkbox intent; preserve checkbox intent earlier in the pipeline if true `Checklist` styling is required beyond contextual edit-div inference.

## 2026-06-09 - Hidden Example Label Marker

- Status: `active`
- Scope: project/tooling
- Decision: example divs may use a visible label paragraph containing exactly `No Title` as a hidden control marker. `apply_example_block_styles()` removes that `DivLabelExample*` paragraph from the DOCX output while preserving the active `AW Example` / `AW Example Good` / `AW Example Bad` styling state for the following example content.
- Preferred behavior: use `No Title` only for neutral/good/bad example divs where the example formatting should remain but the visible label is redundant. Do not rely on blank-line count in Markdown as a control signal; Pandoc does not preserve it at the block-structure level needed here.

## 2026-06-10 - Hidden Example Label Pass Moved Out Of Skipped Heuristic Path

- Status: `active`
- Scope: project/tooling
- Decision: in the source-driven INT pipeline, `apply_example_block_styles()` remains intentionally skipped, so `No Title` suppression must not live only inside that function.
- Implementation: added a separate active `strip_hidden_example_labels()` pass in `postprocess_docx.py`. It removes `DivLabelExample`, `DivLabelExampleGood`, and `DivLabelExampleBad` paragraphs whose normalized text is exactly `No Title`, without re-enabling the retired heuristic example-styling pass.
- Preferred behavior: keep example body styling source-driven via div classification and `div_content_style_map`; use the dedicated hidden-label pass only to suppress redundant visible labels.

## 2026-06-19 - PPTX Generation Requires Source-Verified Object Construction

- Status: `active`
- Scope: project/tooling
- Decision: before making non-trivial PPTX edits, especially for animation-ready objects, research and confirm the correct PowerPoint/PptxGenJS construction method from official docs, local library source, or a minimal generated-file probe.
- Lesson: avoid quick visual fixes that create the wrong PowerPoint object model. For example, a tag that must animate as one object should be created as a single text-bearing shape with `slide.addText("label", { shape: pptx.ShapeType.roundRect, ... })`, not as `addShape()` plus a separate overlaid `addText()`.
- Preferred behavior: validate generated PPTX files by opening/exporting with PowerPoint COM when Office compatibility matters, and inspect the generated XML or object count when object structure matters for animation/editing.

## 2026-07-03 - Thematic Series Consolidation Methodology Established

- Status: `active`
- Scope: project/tooling
- Decision: created a reusable, LLM-agnostic methodology for consolidating a cluster of thematically related textbooks (e.g. audience-forked or medium-forked book pairs) into a single unified book offered at multiple course-length tiers. Documented at `docs/thematic-series-consolidation-methodology.md`.
- Process summary: (1) inventory source books and reuse existing `docx-to-markdown` `out/.md/` conversions rather than reconverting; (2) map each book's content in parallel via one background agent per book, producing per-unit reports on frameworks, language content, model scenarios, audience-specificity, and tier judgment; (3) synthesize a cross-book framework table plus a list of each book's distinctive non-duplicated content; (4) raise explicit design decisions for user sign-off (framework naming/synthesis, audience-fork handling, modernization scope, tier-inclusion granularity, manuscript structure) rather than assuming defaults; (5) record the resolved plan in a project-specific `docs/<series-name>-consolidation-plan.md`.
- First applied instance: Presentation Skills series (`Speaking with PowerPoint`, `Making Speeches`, `Business Presentations Essentials for Businesspeople`, `Business Presentations Essentials for Government Officials`) being consolidated into a single "Presentation Skills" book with Essentials/Standard/Long tiers. Plan recorded at `docs/presentation-skills-consolidation-plan.md`.
- Key empirical finding (Presentation Skills instance, expected to generalize but must be re-verified per series): in audience-forked book pairs, only ~2 of 7-8 units per book carried genuine audience-specific content, and even then mostly just scenario/employer dressing on an otherwise identical skill — audience distinction should fold into paired model speeches/examples within shared units, not separate books.
- Next planned application: Meeting Skills book series, using the same methodology.
- Preferred behavior: this methodology document and any per-series plan files are project memory, not Claude-specific memory — keep them in `docs/` as plain markdown so they remain usable by any LLM or human working in this repo, and update `project-learning.md`/`project-journal.md` (not a tool-specific memory store) when durable decisions are made during this kind of project.

## 2026-07-07 - Presentation Skills Visual Asset Generation: Techniques And Representation Requirements

- Status: `active`
- Scope: project/tooling
- Context: pre-Stage-3 visual asset generation for "Presentation Skills," using `books/Presentation Skills/images/image_register.json` (36 images total: diagram/process/scenario/icon_set types) as the driving register, generated via `scripts_local/generate_presentation_skills_images.py`. See `openai` SDK unavailability workaround in `user-learning-mirror.md` issue `2026-07-07-NETWORK-01` -- all generation goes through raw HTTP, never the SDK.
- Decision: split technique by task -- use OpenAI (`gpt-image-1`) for organic/illustrative content and icon art; use PIL for precise text placement, exact element counting, and geometric layout. Empirically validated: the model could not reliably produce an 8-box connected flowchart with correct box count across 3 attempts (more explicit prompt wording made box count worse, not better), but reliably produced a clean 2x4 icon grid sheet (isolated icons, no connecting structure) on the first attempt. Working pattern for precision diagrams: generate icons as an isolated grid sheet, visually verify actual cell order by inspection (never assume it matches the request), slice with an alpha-threshold crop (ignore stray pixels below alpha ~40) inset ~6% per cell to avoid cross-cell bleed artifacts, then composite into a deterministically-drawn PIL layout. Reference implementation: `scripts_local/build_three_phases_final.py`.
- Decision: use the native `background: "transparent"` parameter on `gpt-image-1` (raw HTTP only) for true transparency, not prompt wording -- prompt-based attempts ("flat, texture-free background", "100% transparent background") caused vignette/gradient artifacts and color drift. After generating, zero RGB wherever alpha==0 (transparent pixels can carry hidden non-zero RGB that ghosts through in some renderers). Diagram/process/icon_set image types get transparent backgrounds; scenario type images stay full opaque rectangles (confirmed preference).
- Decision: all people depicted in scenario/photo-style images must read as Japanese/East Asian (textbook is for students/professionals in Japan), and no real national flags/emblems/seals/crests may appear anywhere. Generic "diverse" wording in the prompt was NOT sufficient -- an early batch defaulted to non-Asian skin tones/hair across most images despite that wording, and a government-scenario prompt saying "flags... optional" produced a literal US flag. Fix required forceful, explicit, early-in-prompt wording naming both the desired appearance and the specifically excluded groups/imagery (see current `style_lock.photo_style` in `image_register.json` for the working wording). Vague government/civic-setting descriptions ("government or civic auditorium", "seal/banner subtly visible") also defaulted to American iconography -- replaced with explicit "plain walls, no podium seal, no emblem, no crest, no flag, no signage" wording. Preferred behavior: never reintroduce the word "diverse" into these prompts, and visually check skin tone/hair plus scan for any flag-like/crest-like element on every people-containing image before approving, since this has failed silently more than once.
- Status as of 2026-07-07 (end of day): all 36 images generated and reviewed, none outstanding. Final 3 (`05-2-logic-tree-worked-budgetapp`, `appD-1-tree-stipend-pitch`, `appD-2-tree-intersection-pitch`) were produced with zero additional OpenAI API calls by reusing the already-approved `05-1-logic-tree-blank.png` art and overlaying worked-example text via a new generalized script `scripts_local/draw_logic_tree_worked_example.py` (parameterized version of `draw_logic_tree_labels.py`, takes `--trunk/--branches/--fruit` args, dynamically sizes the side margin from actual rendered text width rather than a fixed guess -- an early attempt with a fixed 320px margin silently truncated the longest trunk phrase, "This app gives you your evenings back" -> "This app gives you"). Final image, `04-3-delivery-icon-set`, generated directly via the standard batch script with no issues. Presentation Skills visual asset generation is complete; next step for this project is Stage 3 (style infrastructure / per-tier DOCX build) per the production checklist in `docs/presentation-skills-consolidation-plan.md`.
- Constraint: user received an OpenAI API spend alert during this work and asked explicitly not to waste credits. Preferred behavior going forward: write prompts to get representation/composition right on the first or second attempt (not iterative trial-and-error rounds), only regenerate an image when a confirmed real defect exists (not for speculative improvement), batch generation calls rather than one-off single-image calls when generating multiple images in the same session, and reuse already-generated source art via PIL post-processing instead of paying for a fresh API generation whenever the only thing that actually changes is text content (proven effective for the 3 worked-example trees above).

## Roadmap From README

- Improve `reference.docx` to support running headers with chapter titles and page numbers.
- Add automated merging of multiple chapters plus front and back matter.
- Add automated image handling for placement, captions, and numbering.

## 2026-08-12 - Speaking with PowerPoint Component Terminology

- Status: `active`
- Scope: project/content
- Decision: textbook components in the Speaking with PowerPoint / Presentation Skills rebuild are `Units`, not `Lessons`.
- Preferred behavior: use `Unit`, `unit`, `units`, `standard-12-unit-curriculum-spec.md`, `standard-unit-*`, `unit_use`, and `p3-uNN-*` asset IDs/filenames in authored planning, drafting, QA, and asset-register documents. Do not use `Lesson` for course components unless quoting or preserving external/source feedback.

## 2026-08-12 - Speaking with PowerPoint Appendix Model Teaching-Point Fit

- Status: `active`
- Scope: project/content
- Decision: appendix presentation models must demonstrate only teaching points that logically belong to the model topic. Do not add data, charts, visuals, document roles, or Q&A pressure just to satisfy a unit reference.
- Preferred behavior: use project results models for measured outcomes/data explanation; process improvement models for workflow, audience outcome, problem-solution structure, document roles, and implementation-risk Q&A; launch models for value-focused openings, visual hierarchy, rollout timelines, adoption questions, and next-step language. If a unit needs a skill that does not fit the appendix model, create a short role-agnostic practice item in the unit instead of distorting the model.

## 2026-08-12 - Speaking with PowerPoint Folder Layout

- Status: `active`
- Scope: project/files
- Decision: the book folder is organized into `books/Speaking with PowerPoint/revision/` for current 2026 revision work and `books/Speaking with PowerPoint/old/` for preserved original-source material.
- Preferred behavior: place current plans, control files, draft units, appendix model source packs, AI feedback, archived revision plans, and agent/review records under `revision/`. Keep original PDF/DOCX source files and extracted conversion output under `old/`.

## 2026-08-12 - Speaking with PowerPoint Model Script Timing

- Status: `active`
- Scope: project/content
- Decision: use about 115-125 words per minute as the working timing range for practiced B1-B2 model presentation scripts, including pauses and visual handling.
- Preferred behavior: do not label model scripts with timings that require rushed reading. If a timing target is important, check script-only word count and adjust the label or trim the script.

## 2026-08-12 - Speaking with PowerPoint Model Variety and Parity

- Status: `active`
- Scope: project/content
- Decision: appendix model scripts must demonstrate varied presentation structures and phrase families; they must not imply that every business presentation follows one rigid template.
- Preferred behavior: use the `Model Structure and Phrase Variety Map` in `books/Speaking with PowerPoint/revision/control/plan3-case-model-brief.md` before drafting or repairing model scripts. Preserve government/non-government teaching-point parity inside each model family: comparable core skill, visual/document role where relevant, Q&A challenge level, and final action request, while varying opening style, transition patterns, and close.

## 2026-08-12 - Speaking with PowerPoint Client Contexts

- Status: `active`
- Scope: project/content
- Decision: client examples should reflect a broad Japanese professional client base, including banking/leasing, general trading companies, manufacturing/industrial companies, and government/public-safety agencies. Named examples from the user include Mizuho Bank, Mizuho Leasing, Marubeni, Bosch, NRA, PSIA, and the Tokyo Metropolitan Police.
- Preferred behavior: business-client examples may include banking, leasing, general trading-company/import-export, manufacturing, operations, reporting, client service, supply chain, procurement, compliance-support, and internal process contexts. Do not treat `trading` as financial-market trading by default. Avoid stock/securities trading, investment advice, market predictions, ticker symbols, exchange names, financial trading desks, real client/account data, regulatory/legal advice, or real-company claims unless explicitly approved and sourced. Government examples should remain administrative, service-delivery, coordination, reporting, training, public-safety administration, or process-improvement focused, without political advocacy or sensitive operational/security detail.

## 2026-08-13 - Speaking with PowerPoint Handoff Discipline

- Status: `active`
- Scope: project/workflow
- Decision: because the user reported limited remaining weekly Codex token capacity, Speaking with PowerPoint work needs frequent durable handoff updates in both repo memory and `books/Speaking with PowerPoint/README.md`.
- Preferred behavior: after each meaningful content/control-file step, update the book README with current status, touched files, validation results, unrelated dirty-worktree warnings, and the next recommended step. Use project journal for chronology and project learning for durable decisions.

## 2026-08-13 - Speaking with PowerPoint Review Sequencing

- Status: `active`
- Scope: project/workflow
- Decision: Agent 2 and Agent 3 must not run concurrently for final content review. English language development is the textbook's highest priority, and business/context revisions can introduce specialized terms that the Language Editor needs to catch after the wording is settled.
- Preferred behavior: run Agent 3, the Business Presentation Specialist, first; integrate business/context findings; then run Agent 2, the Language Editor, as the final specialist pass. The final language pass must check first-use definitions, glossary needs, B1-B2 load, Japanese-learner support, spoken naturalness, and specialized terms such as `handoff`, `exception`, `pre-read`, `follow-up handout`, `takeaway document`, `fallback option`, `asynchronous`, `sanitized`, `accessibility`, and `confidentiality`.

## 2026-08-13 - Speaking with PowerPoint Learner-Facing Manuscript Rule

- Status: `active`
- Scope: project/content
- Decision: the textbook manuscript, including appendices, must be completely learner-facing. Teacher-facing notes should not appear inside learner unit or appendix drafts.
- Preferred behavior: keep teacher-facing guidance in the separate printable file `books/Speaking with PowerPoint/revision/drafts/Teacher Notes.md`, with clear Unit or Appendix references. If a note belongs in the learner manuscript, rewrite it directly to the learner; otherwise move it to the teacher-notes file.

## 2026-08-13 - Speaking with PowerPoint Role-Agnostic Manuscript vs Client-Specific Teaching

- Status: `active`
- Scope: project/content
- Decision: the printed textbook should be role-agnostic, but classroom delivery does not need to be role-agnostic. The user's classes are not mixed-client classes, so it is acceptable and often preferable for teachers to focus examples and practice on the specific learners' work roles, company, organization, and communication needs.
- Preferred behavior: keep learner manuscript units transferable across business and government clients, but write teacher notes that invite client-specific adaptation. For business clients, adapt toward banking/leasing, general trading-company/import-export, manufacturing, operations, reporting, service, procurement, or coordination contexts as appropriate. For government clients, adapt toward administrative service, reporting, coordination, training, and process-improvement contexts while respecting confidentiality and avoiding political advocacy or sensitive operational/security detail.

## 2026-08-13 - Speaking with PowerPoint Learner Terminology

- Status: `active`
- Scope: project/content
- Decision: do not rely on the workplace compound noun `leave-behind` in learner-facing text. `Leave behind` without a hyphen is the phrasal verb; `leave-behind` as a noun is style-dependent and opaque for many B1-B2 learners.
- Preferred behavior: use `follow-up handout`, `takeaway document`, or `supporting document` in learner-facing manuscript unless explicitly teaching the industry noun. Teacher notes may mention the distinction when checking terminology.

## 2026-08-13 - Speaking with PowerPoint Unit 12 Private-Lesson Timing

- Status: `active`
- Scope: project/content
- Decision: many classes are 1-to-1 private lessons, so Unit 12 should not rely only on final-presentation delivery time. A single learner's 5-7 minute final presentation plus Q&A can make the unit too short.
- Preferred behavior: Unit 12 should include a textbook wrap-up quiz or equivalent consolidation task covering major course learning points, with an answer key in `books/Speaking with PowerPoint/revision/drafts/Teacher Notes.md`. Use the quiz to extend 1-to-1 Unit 12 lessons and consolidate learning before or after the final presentation.

## 2026-08-13 - Speaking with PowerPoint Heading Capitalization

- Status: `active`
- Scope: project/style
- Decision: current draft titles, headings, and subheadings should use Chicago-style title case, not sentence case.
- Preferred behavior: capitalize the first and last word, major words, and the first word after a colon when the colon introduces a subtitle/subheading. Following CMOS 18, capitalize prepositions of five letters or more and lowercase articles, coordinating conjunctions, `to`, and prepositions of four letters or fewer unless first or last.

## 2026-08-13 - Speaking with PowerPoint Phase 4 Completion

- Status: `active`
- Scope: project/milestone
- Decision: Phase 4 Standard manuscript rewrite/integration is complete enough to move to Phase 5 asset creation/replacement.
- Preferred behavior: start Phase 5 from `books/Speaking with PowerPoint/revision/control/plan3_image_register.json`. Do not create or replace assets outside the register without updating the register. Keep the missing options-based decision model as a tracked Phase 6 QA/defer item unless the user decides to add that model before asset work.

## 2026-08-13 - Speaking with PowerPoint Asset Generation Workflow

- Status: `active`
- Scope: project/assets
- Decision: use OpenAI-generated images only as sparse, text-free source-panel art for this textbook. Compose all final readable text, chart numbers, headings, labels, and slide layouts deterministically in local code, currently Pillow, so visual assets remain editable/checkable and do not depend on image-model text accuracy.
- Preferred behavior: run OpenAI SDK generation from a local `%TEMP%` staging folder, then copy final source panels into the repo. This avoids recurring UNC/network-path issues. Record prompts/source panels under `books/Speaking with PowerPoint/images/source/`, final core assets under `books/Speaking with PowerPoint/images/planned/`, model slide sets under `books/Speaking with PowerPoint/images/model-slides/`, and update `books/Speaking with PowerPoint/revision/control/plan3_image_register.json` whenever assets are created, superseded, or approved.

## 2026-08-13 - OpenAI SDK UNC Path Workaround

- Status: `active`
- Scope: project/environment
- Decision: when using the OpenAI Python SDK from this network-drive workspace, avoid reading/writing live API inputs and outputs directly on the UNC repo path.
- Preferred behavior: create a local staging directory under `%TEMP%`, run SDK generation there, write manifests/prompts/outputs locally, validate locally, then copy only durable approved outputs back into the repo. Use .NET/PowerShell full-path normalization such as `[System.IO.Path]::GetFullPath(...)` when safety-checking UNC paths before cleanup because `Resolve-Path` may add provider prefixes or formatting that breaks simple string comparisons.
