# Project Journal

## 2026-03-24

- Startup bootstrap executed for the `textmaker` workspace.
- Confirmed the workspace is a Git repository rooted at `<repo-root>`.
- Checked remote sync state non-destructively with `git fetch --prune origin`; local `main` and `origin/main` were even at the time of bootstrap.
- Created missing repo-level bootstrap files: `AGENTS.md`, `user-learning-mirror.md`, `project-learning.md`, `project-journal.md`, and `instruction-read-log.csv`.
- Read `README.md` and promoted its durable content into `project-learning.md`.
- Established repo project memory as the main source for recording project developments, durable decisions, constraints, and roadmap changes going forward.

## 2026-04-14

- Ran `textmaker.cmd markdown-to-docx` against the AME course summary markdown and produced `AME_course_summary_report.docm` in the client report folder; command required an in-session PATH prepend for local Pandoc (`C:\Users\d-dobson\AppData\Local\Pandoc`).

## 2026-05-09

- Updated `textmaker.cmd` to prepend the common local Pandoc install directory automatically when present.
- Updated `scripts/cli.py` so `markdown-to-docx` resolves relative input, reference, and output paths more robustly when launched through `cmd.exe` from a UNC-backed workspace.
- Verified the UNC case by running `..\..\textmaker\textmaker.cmd markdown-to-docx --input .\md\final\modules\aw-adv_mod1_n10.md --reference .\aw-adv-styleref.docx --output .\md\final\modules\aw-adv_mod1_from_relative.docx` from `book_administrative-writing\adv`, which completed successfully.
- Updated `scripts/cli.py` to normalize markdown before Pandoc by inserting blank lines before lists that directly follow prose, preventing list collapse in generated DOCX output.
- Added `--ignore-horizontal-rules` to drop standalone markdown separator lines such as `---` before conversion, avoiding unwanted page breaks when the pagebreak Lua filter is active.
- Added a semantic DOCX postprocessing layer driven by the reference DOCX. `markdown-to-docx` now applies custom styles and cloned prototype callout tables consistently for repeating textbook patterns such as `Why this works`, `Before you write`, teaching-point notes, model good/bad text blocks, homework word-count prompts, and post-list follow-on prompts.
- Verified the semantic pass on Module 1 by generating a temporary DOCX and confirming inserted `Why?` / `Check` / `Learn` / `Note` tables plus applied `Block Text Good`, `Block Text Bad`, `Homework Words`, and `After List` styles.
- Replaced the cloned-prototype-table approach with Word COM Quick Part insertion for unit title blocks only; the converter now launches a dedicated `DispatchEx` Word instance, inserts the real building block from `Normal.dotm`, and avoids touching unrelated `WINWORD.exe` processes.
- Reworked the Administrative Writing semantic formatting so only unit title tables remain as Quick Parts; `Why this works`, `Before you write`, `Teaching point`, `Note`, and related cues now stay paragraph-based to reduce visual dominance.
- Repaired the Module 1 demoted markdown hierarchy by keeping framework sections at `###`, activities at `####`, turning model labels into plain content labels, and converting the “Clarity Patterns” sequence away from a heading stack.
- Expanded `After List` styling so prompt-style lines such as `Practice ...`, `Reflect:`, and `Example:` can inherit the style after short commentary blocks, not only after literal list paragraphs.
- Removed all `*Tok` styles from `book_administrative-writing\adv\aw-adv-styleref.docx`, then repaired the resulting `word/styles.xml` corruption after an initial rewrite dropped the required compatibility namespace declarations from the root element.
- Regenerated the final Module 1 production candidate as `book_administrative-writing\adv\md\final\modules\aw-adv_mod1_n10_demoted_fixed.docx` and verified it contains three unit title Quick Part tables (`U1`, `U2`, `U3`) plus the broadened `After List` styling.

## 2026-05-12

- Added a repeatable Markdown style-audit utility for Advanced Administrative Writing source cleanup.
- Tightened `markdown-to-docx` so postprocess failures surface instead of being silently swallowed.
- Updated DOCX postprocessing to use only reference styles, remove `Strong`/direct bold output, color emoji labels from matching label styles, apply 6pt semantic label spacing, strip activity-code suffixes from headings, and broaden post-list spacing.
- Added a functional Markdown/DOCX paragraph audit report for Advanced Administrative Writing that groups by structural role rather than literal CSV text.
- Regenerated `aw-adv-all_0510.docx` through `textmaker.cmd markdown-to-docx` with `aw-adv-styleref.docx` as Pandoc `--reference-doc` and the Advanced Writing Lua Div filter enabled; validation confirmed no missing reference styles, no `Strong` run style, no direct bold, no remaining heading activity codes, and emoji runs without direct bold/italic markers.
- Regenerated `aw-adv-all_0510.pdf` from the validated DOCX with LibreOffice.
- Updated the Advanced Writing cleanup pipeline so DOCX postprocess purges generated style usage and style definitions not present in the reference DOCX; replaced `annotation` Divs in the working Markdown with `learn-note` and removed the `annotation` Lua mapping. No conversion was run for this change batch.

## 2026-05-13

- Regenerated the Advanced Administrative Writing DOCX through `textmaker.cmd markdown-to-docx --input ... --reference ... --lua-filter ...`, with `aw-adv-styleref.docx` passed through to Pandoc as `--reference-doc`.
- Added a postprocess cleanup for alphabetic option lists: `List Number 3` is applied to A/B/C option items and literal source markers are removed afterward to prevent doubled labels in PDF output.
- Validated the generated DOCX against the reference style set: no missing used styles, no extra style definitions, no `Strong` or `Emphasis` run styles, no direct bold tags, no activity-code suffix hits, and no literal alphabetic markers inside `List Number 3` paragraphs.
- Exported the validated DOCX to PDF with LibreOffice.
- Corrected the Advanced conversion command to use `--no-pagebreak-filter`; this keeps Textmaker from applying `pagebreak.lua` to standalone `---` separators and restores the PDF to the expected 186-page length.
- Updated semantic Div title postprocessing so title lines retain their semantic paragraph styles, with 4pt space after on the label paragraph and 0pt space before on the moved content paragraph.
- Updated unit-title table postprocessing so the original unit heading text is cleared after the reference table is inserted, preventing visible duplicate unit headings.
- Added a nested-list semantic Div pass so list paragraphs inside semantic Div blocks keep their list style while receiving the Div's block-level paragraph formatting. Regenerated the Advanced DOCX/PDF and validated that the nested list items have both list styling and Div border formatting.
- Simplified `scripts/postprocess_docx.py` by rolling back two recent postprocess behaviors:
  - removed the run-level cleanup pass that stripped `Strong`/`Emphasis` styles and rewrote bold handling through heavier font substitution
  - removed the nested-list semantic Div formatting pass that copied Div block formatting directly onto list paragraphs
- Kept the broader semantic paragraph formatting, unit-title handling, heading cleanup, and fallback-style cleanup intact.
- Updated the Learn semantic-style model to support a reduced reference-style set:
  - keep the emoji insertion and per-label Learn label styles
  - stop relying on multiple `Learn XXX` paragraph styles surviving postprocess
  - convert Learn semantic paragraphs to `Learn Base` during postprocess

## 2026-05-15

- Implemented the full style-safe DOCX pipeline for the Administrative Writing advanced book, based on a ChatGPT-authored plan at `book_administrative-writing/adv/edits & guides/style edits/step2-stylereference/Instructions_from_ChatGPT_0515.md`. GitHub CoPilot began the work but lost context mid-task; Claude Code completed all 10 tasks.
- Added `scripts/style_bridge.lua` — generic Pandoc Lua filter that reads `style_map` from YAML front matter and maps fenced Div classes to Word `custom-style` attributes. Replaces the hardcoded `aw_textbook_div_styles.lua`.
- Added `scripts/audit_docx_styles.py` — read-only DOCX style inspector with linked-style color-mismatch validation.
- Added `scripts/manage_docx_styles.py` — explicit manual-only tool for updating reference DOCX styles from a YAML spec. Updates all three color locations (`w:color`, `w14:srgbClr`, linked char style `w:color`) atomically. Has `--in-place` safety (auto-creates `.bak`) and post-write validation. **Must not be added to the automated build pipeline.**
- Added `scripts/validate_docx_against_reference.py` — post-build validation script with 5 checks (used para styles in reference, used char styles in reference, no extra style definitions, YAML style_map styles in reference, linked styles valid and reciprocal).
- Refactored `scripts/postprocess_docx.py`: default changed from `semantic_formatting=True` to `apply_semantic_labels=False`. Semantic label rendering now requires `--apply-semantic-labels`. Kept `--no-semantic-formatting` as a deprecated no-op. Updated docstring to remove misleading "semantic course formatting is applied consistently" language.
- Fixed long-standing bug in `scripts/cli.py`: `insert_section_after_toc()` call was indented inside the `except ImportError` block and never executed when running as a package. Added `--apply-semantic-labels` to cli.py parser.
- Added `tests/test_docx_styles.py` — 13 tests covering RGB→hex conversion, all three color-location updates, color-mismatch detection, `Div Label Base` next-style fix, and style audit failure on missing expected styles. All 13 pass.
- Fixed `scripts/style_bridge.lua`: `PANDOC_STATE.meta` does not exist in current Pandoc versions. Rewrote as a two-pass filter (array of filter tables) so `Meta` populates `style_map`/flags in pass 1 before `Div` and `HorizontalRule` run in pass 2. Single-pass filters process `Div` before `Meta` (bottom-up traversal), so the map was always empty.
- Ran first full production conversion of `book_administrative-writing/adv/md/final/aw-adv-all_0514.md` → `adv/docx/aw-adv-all_0514.docx` using direct Pandoc (not textmaker CLI) with `style_bridge.lua` and `aw-adv-styleref.docx`. Postprocess: 1680 list paragraphs styled, 521 fallback styles replaced, 1729 non-reference style instances cleaned, 29 page breaks applied. Validation: exit 0, all styles consistent with reference DOCX.
## 2026-05-16 (session 1 — bootstrap and pipeline setup)

- Set up Claude Code (claude-sonnet-4-6) to use the shared Codex memory bootstrap system.
- Created `C:\Users\daved\.claude\CLAUDE.md` (global) — imports `%USERPROFILE%\.codex\AGENTS.md` and `%USERPROFILE%\.codex\memories\user-learning.md` at every session start via `@filepath` directives.
- Created `c:\Dev\Code\textmaker\CLAUDE.md` (project) — imports `AGENTS.md`, `user-learning-mirror.md`, `project-learning.md`, and `project-journal.md` via relative `@filepath` directives.
- Decision: Claude Code will write durable decisions and events to the shared repo-level memory files rather than the Claude-specific `~/.claude/projects/` memory system, so memory remains shared with Codex and any other AI assistant.

## 2026-05-16 (session 2 — div cleanup and reclassification)

### Work completed

- Fixed 52 missing blank lines between consecutive `:::` close / `:::` open fences (Pandoc parse risk)
- Removed BOM character (U+FEFF) that was on its own line after the YAML front matter
- Stripped all `rubric-assessment` and `course-meta` div wrappers (8 total) — no distinctive rendering, content preserved as plain prose
- Removed 4 stale style_map entries: `guidance-step`, `annotation`, `example`, `placeholder`
- Removed `reference-support` div at Unit 9 D (template content absorbed into surrounding `activity-draft`)
- Removed `reference-support` div at line ~7267 (continuation of model report, absorbed as plain prose)
- Restructured Unit 23 B section (lines 8036–8089): removed empty `activity-analysis` shell, removed `reference-support` scenario wrapper, replaced `model-bad`/`model-good` with neutral `model` divs labelled "Response A" / "Response B"
- Completed initial div reclassification: all 595 div open fences renamed from 18 old classes to 9 new classes per the reclassification guide
- Updated YAML `style_map` to the 9 new classes with `Div Label *` Word style targets

## 2026-05-16 (session 3 — content-based div reclassification pass)

### Completed this session

- Generated a full 595-row content-based reclassification review (`div_reclassification_full_0516.md`) with an explicit one-sentence reason for every div classification.
- Reviewed all 595 rows independently (not label-swapping — reading actual content against the 9-class guide).
- Applied 74 reclassifications to `aw-adv-all_0516.md` via Python script; 0 skipped.
- Verified div balance: 595 open, 595 close, 0 unclosed, 0 orphan closes.
- Verified total count: 595 divs (unchanged — no divs added or removed).

### Key reclassification decisions and reasons

- **edit → rewrite (18 cases):** Tasks labelled `edit` whose instruction was to transform/rewrite given text, not to find errors or apply checklists. The `edit` class is reserved for error-finding, peer review, and self-editing checklists.
- **language → rewrite (8 cases):** Divs where the learner performs a sentence-transformation, completion, or expansion task on given text — not a reference list of language forms.
- **notice → write (9 cases):** Prediction, data-interpretation, and reflection tasks where the learner produces original text from given scenario information.
- **language → learn (6 cases):** Teaching explanation divs (notes on but/however, thematic progression panels, section wrappers) — no task, pure explanation, not a reference list.
- **language → structure (3 cases):** Phrase-bank sorting tasks where the learner classifies given phrases under headings — no new text produced.
- **notice → learn (4 cases):** Outer wrapper divs containing explanatory content or reference panels — no observation task.
- **rewrite → structure (4 cases):** Tasks where the learner orders/sequences given jumbled sentences into a paragraph, not rewrites prose.
- **notice → structure (2 cases):** Sorting/sequencing tasks on given items.
- **rewrite → learn (2 cases):** Outer wrapper divs containing teaching explanation with no rewrite task in the wrapper itself.
- **write → structure (3 cases):** Template-guided tasks where the learner fills a given structural framework — not original production from scratch.
- **edit → revise (4 cases):** Revision chains where learner improves their OWN previously drafted text from an earlier unit.
- **edit → notice (2 cases):** Track-change simulation tasks where learner evaluates proposed edits and decides accept/reject.
- **write → rewrite (1 case):** Two-audience adaptation task with given source text to transform.
- **write → revise (1 case):** Self-revision of own earlier writing using self-diagnosis questions.

### Final div class distribution (session 3 result)

| Class | Before | After | Delta | Word style |
| --- | --- | --- | --- | --- |
| `example` | 127 | 127 | 0 | Div Label Example |
| `learn` | 114 | 126 | +12 | Div Label Learn |
| `write` | 89 | 95 | +6 | Div Label Write |
| `rewrite` | 57 | 83 | +26 | Div Label Rewrite |
| `notice` | 79 | 65 | −14 | Div Label Notice |
| `edit` | 75 | 48 | −27 | Div Label Edit |
| `language` | 54 | 34 | −20 | Div Label Language |
| `structure` | 0 | 13 | +13 | Div Label Structure |
| `revise` | 0 | 4 | +4 | Div Label Revise |
| **Total** | **595** | **595** | **0** | |

### Remaining work (pending)

All items completed in session 4 and session 5 — see below.

## 2026-05-17 (session 4 — overnight fix batch)

### Reference DOCX style repairs

- Renamed all 22 `Div *` styles to `Div Label *` in `aw-adv-styleref.docx` via direct XML edit (`rename_div_styles.py`). Required for `style_bridge.lua` `is_div_label_style()` prefix check (`"Div Label "`, 10 chars).
- Added `Div Label Example Good` / `Div Label Example Good Char` (color `2C9167`) and `Div Label Example Bad` / `Div Label Example Bad Char` (color `E36C0A`) to reference DOCX.
- Updated `Div Label Example` color from `9CCF78` to `4F81BD` (steel blue, matching AW Example body style border).
- Renamed `Body Text1` → `Body Text` (styleId `BodyText`) in reference DOCX; postprocessor and Word both require the canonical name.
- Updated `aw-div-label-styles.yaml` to match all 9 new `Div Label *` names and add `example-good`/`example-bad` entries.

### Source markdown fixes (`aw-adv-all_0516.md`)

- Replaced 44 `model` → `example` occurrences, 23 heading renames (`### B. Model Text` → `### B. Example Text`), 59 div title renames (`Model Text` → `Example Text`).
- Fixed arrow paragraph: instructional note ("The arrow (→)…") moved outside `learn` div and given heading "Clarity Patterns".
- Fixed "Tone by Audience" section: added title to Internal/Interagency/International wrapper div.
- Wrapped Unit 4 Useful Phrases table in a `language` div.
- Renamed 28 "Extension Task" div titles → "Homework Task".
- Updated YAML `style_map` to 9 new `Div Label *` style names.

### Postprocessor additions (`postprocess_docx.py`)

- Added `apply_checklist_style()`: applies `Checklist` style to bullet items inside `Self-Editing Checklist` edit divs.
- Added `apply_example_block_styles()`: applies `AW Example Good` / `AW Example Bad` / `AW Example` body styles after matching Div Label paragraphs.
- Added `apply_spacing_after_lists()`: adds 120-twip space-after to prose paragraphs that follow list paragraphs (replaces deleted `After List` style).
- Added `apply_table_styles()`: applies `AW Standard Table` style to all unstyled tables.
- Moved `replace_unit_headings_with_title_tables()` outside the `apply_semantic_labels` gate — now always runs when reference_doc is available.
- Fixed duplicate `apply_semantic_div_labels` call (was called twice in the updated flow; second call removed).

### Build result (2026-05-17)

- Pandoc: clean, no warnings.
- Postprocess: 1666 list styles, 19 alpha markers stripped, 10 checklist items, 85 example block paragraphs, 179 post-list spacing, 41 table styles, 241 body text, 529 Pandoc fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings restored.
- Validation: exit 0, all styles consistent with reference DOCX.
- PDF: exported via LibreOffice soffice, 3.3 MB.

## 2026-05-17 (session 5 — checklist consistency and example-good/bad reclassification)

### Checklist consistency

- Converted all 151 plain `- ` (dash-space) bullet items inside edit divs to `- [ ]` for source consistency across all edit div types.
- Discovered that Pandoc with `--reference-doc` renders `- [ ]` as `List Bullet 2` (not `Compact` + checkbox glyph) — the checkbox is stripped when a reference DOCX defines the list style.
- Fixed `apply_checklist_style()`: now matches `List Bullet 2` inside any `DivLabelEdit` div (not just "Self-Editing Checklist" divs). 145 items converted in this build.
- Fixed `_apply_style_if_available()`: was calling `_require_style` (hard-fail on missing style). Changed to `_get_style_by_name_or_id` so legacy style references in `apply_semantic_styles()` (Model Bad, Homework Target, After List) degrade gracefully instead of crashing.

### Reference DOCX Body Text name regression

- Discovered `Body Text1`/`BodyText1` had regressed (the w14 strip script from session 4 serialized an older XML state). Fixed by direct XML patch — 17 cross-references updated. Style is now `Body Text` / `BodyText`.

### Example div reclassification

- Audited all 127 `example` divs by their title lines. Pattern confirmed 100%:
  - "Original Text" titles (23) → `example-bad`
  - "Revised Text" / "Worked Example" titles (43 total) → `example-good`
  - "Example Text" and others (61) → remain neutral `example`
- Added `example-good` and `example-bad` to YAML `style_map` targeting `Div Label Example Good` and `Div Label Example Bad`.
- Applied `apply_example_block_styles()` in postprocessor — 85 body paragraphs styled as `AW Example Good` / `AW Example Bad` / `AW Example`.

### Build result (session 5)

- Pandoc: clean, no warnings.
- Postprocess: 1666 list styles, 19 alpha markers, 145 checklist items, 85 example block paragraphs, 179 post-list spacing, 41 table styles, 267 div labels, 241 body text, 529 Pandoc fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings.
- Validation: exit 0.
- PDF: 3.3 MB. Both repos committed and pushed.

## 2026-05-18 (session 7 — icon table layout, caps fix, section break fix, div structure audit)

### Context and starting state

Continuing from session 6. The div label icon table layout (2-column borderless table with icon left, label text right) had been partially implemented but not yet verified against a clean build. Several issues were outstanding from the previous session: all-caps not rendering on div label char styles, page 1 rendering as Letter size with a spurious section break after the H1, and a file lock preventing the final rebuild.

### Reference DOCX patch: all-caps on DivLabel char styles

- All 12 `DivLabel*Char` styles in `aw-adv-styleref.docx` had bare `<w:caps/>` (no `w:val` attribute). Per OOXML spec, toggle properties in character styles require explicit `w:val="1"` to be honoured; bare elements are treated as "not set".
- Patched all 12 char styles to `<w:caps w:val="1"/>` using `C:\Temp\fix_caps_val.py`. Backup saved as `aw-adv-styleref.bak_caps` (moved to `adv/md/bak/` after session).
- Note: underline worked because `<w:u>` requires `w:val="single"` by spec and was already present; caps was the only property affected.
- Confirmed caps rendering in PDF output after patch.

### Postprocessor fixes (`postprocess_docx.py`)

**Section break / page size fixes:**

- `_insert_section_break_before_paragraph()`: added copy of `w:pgSz` and `w:pgMar` from document-level `sectPr` into every inserted `sectPr`, so section breaks inherit correct paper size (A4) instead of defaulting to Word's application default (US Letter).
- `insert_section_breaks_before_h1()` call site: changed `skip_first=has_toc` to `skip_first=True` so the first H1 (the cover title) is always skipped. Previously, when `has_toc=False`, the first H1 got a section break attached to the preceding YAML front-matter paragraph, effectively pushing the H1 off page 1.
- Confirmed via PDF MediaBox inspection that all pages are A4 (210×297mm) after fixes.

**Div label icon table layout (single-pass rewrite):**

- Rewrote `apply_semantic_div_labels()` as a single-pass function: builds the 2-column borderless table and inserts the icon in the same step, replacing each `DivLabel*` paragraph with a `<w:tbl>` in-place.
- Table config: `tblStyle=TableGrid`, `tblW type=auto` (autofit), explicit `tblBorders` with all sides `none`/`sz=0` to suppress visible borders while preserving gridlines toggle. `TableNormal` was tried but rejected because it has no border definition and the gridlines toggle couldn't be controlled.
- Left cell uses `DivTag` paragraph style (user-created, based on `Div Label Base`) so spacing inherits from the style rather than being hardcoded.
- Icon height changed to 190500 EMU (15pt) for inline rendering; `distR=114300` EMU (9pt) gap to label text.
- Example divs (neutral/good/bad) excluded from icon table — they use a different visual treatment.
- Fixed `AttributeError: 'CT_Body' object has no attribute 'part'` by using `Paragraph(child, doc._body)` instead of `Paragraph(child, body)`.

**`_apply_next_page_section_to_paragraph()` fix:**

- Added copy of `w:pgSz` and `w:pgMar` from document-level `sectPr` (same fix as `_insert_section_break_before_paragraph`).

### Working folder cleanup

- Moved `aw-adv-styleref.bak_caps` to `adv/md/bak/`.
- Removed stale `.tmp` file.
- Working folder now contains only: `aw-adv-all_0516.md`, `aw-adv-styleref.docx`, `aw-adv-all_0518.docx`, `aw-adv-all_0518.pdf`, `div-tags-icons-2_assets/`.

### Source markdown fixes (`aw-adv-all_0516.md`)

**Div spacing fixes (Pandoc compatibility):**

- Fixed 7 missing blank lines before `:::` open fences: all were bold `**Input N / Source N**` label lines immediately followed by `:::` with no blank line. Pandoc requires a blank line before a fenced div when preceded by non-empty content.
- Fixed 1 missing blank line between `:::` open fence and an immediately-following numbered list (`edit` div at L7317).
- Fixed 1 spurious extra `:::` close fence (triple `:::` at lines 2997–2999 reduced to double).
- Fixed unclosed `notice` div at L2951: inner `example-bad`/`example-good` divs were terminating the outer `notice` early; added explicit `:::` close before the sibling `learn "Why This Works"` block.

**Nested div audit and cleanup:**

- Audited all 244 nested div instances across the file. Two categories identified:
  - **Thin nested divs** (title-only, no body): 16 total, all nested. 11 removed as pure sub-labels adding no student learning value: `learn "Functions"` (×2), `language "Learn — Sentences"`, `language "Learn — Useful Language"` (×3), `language "Learn — Patterns"`, `learn "Statements"`, `learn "Annotations"`, `learn "Discuss"`, `learn "Revision Checklist"`.
  - **Kept** (meaningful labels): `learn "Version A"`, `learn "Version B"`, `learn "Original"`, `learn "Proposed Changes"`, `learn "Scenario"` — these label distinct content sections within the outer div.
- Remaining nested divs (233) are structural patterns where sub-divs are genuinely separate content blocks (e.g. `example-bad`/`example-good`/`learn "Why This Works"` sequences inside `notice` wrappers). These are known to cause early termination of the outer div in Pandoc; full resolution is pending — see decisions below.

**Table cell `<br>` tag fixes:**

- Replaced malformed `<br*` and `<br>` tags in pipe table cells with ` / ` separator. Pandoc's `markdown+fancy_lists` format does not process raw HTML in table cells without the `+raw_html` extension, so these were rendering as literal text.
- Affected: "Useful Phrases" language table (L1102–1106) and "Clarity Patterns" table (L196–198).

### Build results (session 7 final)

- Pandoc: clean, no warnings.
- Postprocess: 1678 list styles, 21 alpha markers, 145 checklist items, 92 example block paragraphs, 180 post-list spacing, 39 table styles, 458 icon tables + 61 emoji labels, 1113 div label updates, 243 body text, 513 fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings.
- PDF: 201 pages, all A4 (210×297mm confirmed via MediaBox). 3.9 MB.

### Outstanding issues

- **All-caps on div labels**: Caps patch applied to reference DOCX and confirmed in PDF. LibreOffice may render caps differently from Word — to be verified in Word.
- **Nested divs**: 233 remaining nested div instances. Most are `example-bad`/`example-good`/`learn` blocks inside `notice` wrappers — a deep structural issue requiring content-level decisions about which blocks are genuinely inside the outer activity vs. siblings. Not addressed this session.
- **Page 1 H1 visibility**: H1 "Administrative Writing, Advanced" is present in the DOCX body (confirmed via XML) but uses a white-text style in the reference DOCX (designed for use inside colored module title tables). The cover page layout is a placeholder ("Textbook description goes here") — not a pipeline issue.

## 2026-05-17 (session 6 — icon colors, alignment, and pipeline fixes)

### Reference DOCX color updates

- Updated `w:color/@w:val` on all 8 non-Example Div Label paragraph styles and their linked character styles to match the dominant fill color of each tag icon PNG:
  - Learn=`541F69`, Language=`722566`, Structure=`A72D61`, Notice=`DB4351`
  - Write=`CA7032`, Rewrite=`E09F1E`, Revise=`75B04C`, Edit=`0BA286`
- Example Div Label styles left at their original colors (no icon, no color change needed).

### Postprocessor changes (`postprocess_docx.py`)

- Removed `DivLabelExample`, `DivLabelExampleGood`, `DivLabelExampleBad` from `DIV_TAG_ICON_STEMS` — Example divs get no tag icon.
- Reduced `DIV_TAG_ICON_HEIGHT_EMU` from 152400 (12pt) to 133350 (10.5pt) to match font height exactly.
- Added `DIV_TAG_ICON_DIST_T_EMU = 38100` (3pt) and applied `distT` on `wp:inline` element to shift icon bottom toward text baseline.
- Increased NBSP after icon from 1 to 2 non-breaking spaces.
- Fixed intermediate save+reload: replaced `doc.save(path); doc = Document(path)` with a temp-file save+move to prevent corrupt DOCX on large icon-embedded files.

### CLI fix (`cli.py`)

- Fixed critical bug: `pandoc_input_fmt` had `-yaml_metadata_block` which disabled YAML front matter parsing, causing `style_bridge.lua` to never receive the `style_map` and silently produce zero Div Label styles. Restored to `markdown+fancy_lists`.

### Build result (session 6)

- Pandoc: clean, no warnings.
- Postprocess: 1676 list styles, 21 alpha markers, 145 checklist items, 85 example block paragraphs, 180 post-list spacing, 39 table styles, 589 div labels (469 with icons), 243 body text, 513 Pandoc fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings.
- Validation: exit 0.
- Both repos committed and pushed. PDF not exported (LibreOffice not installed on current machine).

## 2026-05-18 (session 8 — style architecture simplification and reference DOCX cleanup)

### DivTag character style fix

- Diagnosed root cause of div label icon misalignment: `DivTag` was defined as a paragraph style, so `w:rStyle` references to it on icon runs were silently ignored by Word (rStyle only resolves character styles). Icon inherited raw paragraph style properties with no baseline lowering.
- Changed `DivTag` from paragraph type to character type in reference DOCX with `w:position w:val="-8"` (4pt lower) and `w:u val="none"`. Removed `basedOn` and `next` (not valid on character styles).
- Icon run now correctly receives the 4pt baseline lowering via the character style.

### Icon height

- Changed `DIV_TAG_ICON_HEIGHT_EMU` from 152400 (12pt) to 198000 (0.55 cm) to account for internal PNG padding and baseline repositioning, keeping icon label text legible.

### Div Label style architecture — dropped linked char styles

- Removed all 12 `DivLabel*Char` character styles from reference DOCX.
- Removed `w:link` from all 12 `DivLabel*` paragraph styles.
- Replaced `build_semantic_div_label_styles()` in `postprocess_docx.py`: now reads color directly from paragraph style `rPr` instead of looking up linked char styles.
- Updated `apply_semantic_div_labels()`: applies color and `Noto Sans Condensed Medium` font directly to label runs via `_set_run_color` / `_set_run_font` — no char style assignment.
- Result: reference DOCX reduced from 24 DivLabel styles to 12 (paragraph only); single source of truth for font/size/spacing in `Div Label Base`.

### Reference DOCX — font update

- Set `Noto Sans Condensed Medium` (ascii + hAnsi) on all 12 `DivLabel*Char` styles before they were removed. Font is now applied directly by postprocessor.

### Reference DOCX — AW Table style updates

- All 4 AW Table styles (`AWStandardTable`, `AWComparisonTable`, `AWPhraseBankTable`, `AWRubricTable`) updated:
  - Width: 100% (`pct` type) — fit to text column
  - Layout: `autofit`
  - Paragraph alignment: left (was centered)
  - Paragraph hyphenation: `suppressAutoHyphens` = 1
  - First row: bold, white text, `2D4155` dark blue fill (was already present on AWStandardTable; applied consistently to all four)

### Build result (session 8)

- Pandoc: clean, no warnings.
- Postprocess: 1678 list styles, 21 alpha markers, 145 checklist items, 244 example block paragraphs, 395 post-list spacing, 39 table styles, 127 placeholders, 458 icon labels + 61 emoji labels, 595 div label updates, 219 body text, 513 fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings.

