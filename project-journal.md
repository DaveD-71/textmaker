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

## 2026-05-16 (session 2 — div cleanup and reclassification)

### Status at session end

Active working file: `book_administrative-writing/adv/md/working/aw-adv-all_0516.md` (8,361 lines, 595 div instances)

Reclassification review document: `book_administrative-writing/adv/edits & guides/style edits/div_reclassification_review_0516.md` (597-row detail table, verified totals)

Design reference: `book_administrative-writing/adv/edits & guides/style edits/div_class_reclassification_0515.md`

Build guide: `book_administrative-writing/adv/README-build.md`

### Completed this session

- Fixed 52 missing blank lines between consecutive `:::` close / `:::` open fences (Pandoc parse risk)
- Removed BOM character (U+FEFF) that was on its own line after the YAML front matter
- Stripped all `rubric-assessment` and `course-meta` div wrappers (8 total) — no distinctive rendering, content preserved as plain prose
- Removed 4 stale style_map entries: `guidance-step`, `annotation`, `example`, `placeholder`
- Removed `reference-support` div at Unit 9 D (template content absorbed into surrounding `activity-draft`)
- Removed `reference-support` div at line ~7267 (continuation of model report, absorbed as plain prose)
- Restructured Unit 23 B section (lines 8036–8089): removed empty `activity-analysis` shell, removed `reference-support` scenario wrapper, replaced `model-bad`/`model-good` with neutral `model` divs labelled "Response A" / "Response B"
- Completed full div reclassification: all 595 div open fences renamed from 18 old classes to 9 new classes per the reclassification guide
- Updated YAML `style_map` to the 9 new classes with `Div Label *` Word style targets

### New div class system (9 classes, 595 instances)

| Class | Count | Word style |
| --- | --- | --- |
| `example` | 127 | Div Label Example |
| `learn` | 114 | Div Label Learn |
| `write` | 89 | Div Label Write |
| `notice` | 79 | Div Label Notice |
| `edit` | 75 | Div Label Edit |
| `rewrite` | 57 | Div Label Rewrite |
| `language` | 54 | Div Label Language |
| `structure` | 0 | Div Label Structure |
| `revise` | 0 | Div Label Revise |

### Remaining work (pending)

- The reference DOCX (`adv/md/working/aw-adv-styleref.docx`) still has the OLD style names (e.g. `Div Label Activity Analysis`, `Div Label Process`, etc.) — it needs to be updated to define the 9 new `Div Label *` styles before a DOCX build can be run. Use `manage_docx_styles.py` with a YAML spec, or update manually.
- The `adv/style_specs/aw-div-label-styles.yaml` spec file will also need updating to match the new 9-class system before `manage_docx_styles.py` can be used.
- Review and update `aw-adv-all_0516_div_issues.md` to close out resolved items.
- Remaining div issues from the original to-do list that may still need attention: heading-to-div gap pattern review (24+ instances), heading/Focus redundancy pattern (8 cases) — these were deprioritised in favour of the reclassification pass.
- A full DOCX build and validation pass has not been run against the 0516 file yet.

## 2026-05-16 (session 1 — bootstrap and pipeline setup)

- Set up Claude Code (claude-sonnet-4-6) to use the shared Codex memory bootstrap system.
- Created `C:\Users\daved\.claude\CLAUDE.md` (global) — imports `%USERPROFILE%\.codex\AGENTS.md` and `%USERPROFILE%\.codex\memories\user-learning.md` at every session start via `@filepath` directives.
- Created `c:\Dev\Code\textmaker\CLAUDE.md` (project) — imports `AGENTS.md`, `user-learning-mirror.md`, `project-learning.md`, and `project-journal.md` via relative `@filepath` directives.
- Decision: Claude Code will write durable decisions and events to the shared repo-level memory files rather than the Claude-specific `~/.claude/projects/` memory system, so memory remains shared with Codex and any other AI assistant.

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
