# Project Journal

## 2026-07-06 - Presentation Skills Stage 2 Content Drafting Complete

- Drafted all 15 units of "Presentation Skills" per the fully-approved consolidation plan, using a multi-agent approach: attempted via the Claude Code `Workflow` tool first, then fell back to plain sequential/parallel `Agent` calls after `Workflow` became unavailable mid-run (see `user-learning-mirror.md` issue `2026-07-06-WORKFLOW-01`). 5 of 19 originally-launched workflow agents had already completed and cached results in `subagents/workflows/wf_0fe68fab-a09/journal.jsonl` before the interruption; these were extracted and reused rather than redrafted, preserving the 3 per-tier voice guides and 2 already-finished units.
- Established a per-tier shared voice-guide pattern to keep prose consistent across independently-drafted units at the same tier: `books/Presentation Skills/canon/voice-E.md`, `voice-S.md`, `voice-L.md`, each pasted verbatim into every unit-drafting agent's prompt for that tier.
- All 15 units persisted as `books/Presentation Skills/units/unit-N.json`, each containing per-tier content (only the tiers that unit belongs to) plus `appendixModels` for the 3 units that own an appendix (Unit 2 -> Appendix A, Unit 10 -> Appendix B, Unit 12 -> Appendix C), all freshly written per Decision 9.
- Assembled the 3 manuscript files (`Essentials.md` 8 units, `Standard.md` 12 units, `Long.md` all 15 units) via an assembly agent, verified all cross-unit callbacks resolve (Unit 3->2, Unit 4->2, Unit 7->3, Unit 8->5&7, Unit 9->2, Unit 10->Appendix B, Unit 11->10, Unit 12->Appendix C, Unit 13->12, Unit 14->6, Unit 15->2-4) and shared terminology stays consistent (6 Keys, Logic Tree parts, "M. Chair/Chairperson").
- User caught two real defects post-assembly: (1) appendices were interleaved mid-book (after their owning unit) rather than collected at the end -- fixed via a reordering script across all 3 files, with tables of contents corrected to match; (2) a word-count audit requested by the user surfaced that Unit 12's Long-tier text (319 words) was thinner than its own Standard-tier text (486 words) and a fraction of sibling Long units (1,300-2,800 words) -- redrafted Unit 12's Long tier only (now 1,621 words) to match Long voice/depth and correctly set up Unit 13's handoff, leaving Standard tier and both Appendix C speeches untouched.
- Committed and pushed to `origin/main` (`afed89e`): all 15 unit JSONs, 3 canon voice guides, 3 assembled manuscripts, plus the `user-learning-mirror.md` Workflow-tool issue entry. This completes Stage 2 (content drafting) of the plan's Section 7 production checklist; Stage 3 onward (style infrastructure, per-tier DOCX build, validation, pedagogy review, PDF export, sign-off) remains open.

## 2026-07-03 - Presentation Skills Consolidation Planning

- Began planning consolidation of four presentation-skills books (`Speaking with PowerPoint`, `Making Speeches`, `Business Presentations Essentials for Businesspeople`, `Business Presentations Essentials for Government Officials`) into a single "Presentation Skills" book offered at Essentials/Standard/Long tiers, eliminating the businessperson/government-officials split at book level in favor of paired audience-specific models within shared units.
- Established a reusable, LLM-agnostic thematic-series consolidation methodology (source inventory -> parallel per-book content mapping via background agents -> cross-book synthesis -> explicit design-decision sign-off -> recorded plan), intended for reuse on the upcoming Meeting Skills book series. Documented at `docs/thematic-series-consolidation-methodology.md`.
- Reused existing `docx-to-markdown` `out/.md/` unit conversions for all four source books rather than reconverting; ran four parallel background agents (one per book) to produce structured content maps (frameworks, language content, model scenarios, audience-specificity, dated-content flags, tier judgment).
- Resolved decisions: best-of framework synthesis across sources (not single-book-as-base or variant-preservation); eliminate business/government split at book level, folding audience variants into paired model speeches within shared units; build a new Virtual & Hybrid Delivery module as in-scope new content, since none of the four source books address virtual/hybrid presenting at all.
- Open decisions (recorded in `docs/presentation-skills-consolidation-plan.md`): per-unit tier-inclusion granularity (some units essentials/long-exclusive, most depth-scaled across all tiers, reference material accreting across tiers) needs further review; manuscript structure (single tagged source vs. separate per-tier manuscripts); "Keys" framework naming synthesis; whether to keep or generalize the Japanese-L1-learner-specific language framing; whether dated model-speech scenarios (Ventura car pitch, Cool Biz policy speech) get freshly written or refreshed in place.
- Full proposed unit list and tier mapping recorded in `docs/presentation-skills-consolidation-plan.md`.
- Revised plan per user feedback: online/hybrid delivery is now a cross-cutting consideration woven through nearly every unit (not a single bolt-on module), with a narrower dedicated unit retained for platform-specific mechanics; model speeches (previously standalone units) moved into a new Appendices section pairing business/government models per skill, directly serving the audience-split retirement goal from Decision 2.
- User caught a real error: the unit-list table's per-unit E/S/L marks did not match the illustrative summary counts below it. Reworked the table so Standard and Long are differentiated by depth (4 units abridged at Standard, full at Long) rather than Standard being a near-duplicate of Long, and corrected the counts to match the table exactly (Essentials 9/15, Standard 14/15, Long 15/15). Left open, within Decision 5, whether Standard also needs a content cut rather than just reduced depth.
- User judged the depth-only differentiation insufficient and set hard numeric tier caps: Essentials <= 8 taught units, Standard <= 12, Long = all. Retired the "abridged counts as present" convention entirely and rebuilt the unit table to enforce exclusion by count. Essentials rebuilt directly from the existing BPE Essentials books' actual unit set (Structure, Delivery, Flag Expressions, Logic Tree, Chairing, capstone) rather than a fresh guess, plus Slide Design since visual aids are now baseline expectation. Cut the standalone Online & Hybrid Delivery Mechanics unit entirely, folding its content into Delivery Skills, since Decision 3 already committed to weaving online considerations through every unit and a dedicated mechanics unit on top of that was redundant. Expressions Reference Appendix moved outside the unit-count cap. Renumbered all 13 taught units and corrected every cross-reference across the plan (decisions, appendix table, modernization flags). Final counts: Essentials 8/13, Standard 12/13, Long 13/13.
- User identified a significant scope gap: the source books are instructor/reference guides, not learner-facing textbooks with developmental activities built in. Designed a learning activity for every one of the 13 taught units, tier-scaled alongside content tiering rather than deferred to drafting. 7 of 13 activities extend a genuine source-book precedent (self-introduction critique exercise, Logic Tree build, annotated pronunciation practice, etc.); 6 of 13 are newly designed because no source activity existed for that content (orientation self-assessment, flag-expression drill, slide redesign critique, evidence-chain construction, slide/handout rehearsal, team-presentation group project). Added new resolved Decision 10 recording this addition; fixed section ordering so Appendices (5a) precede Activities (5b) since several activities reference appendix models.
- User split former Units 10-11 ("Description, Logic & Persuasion" and "Critical Thinking: Analyze & Propose / Argue & Defend") into four units -- Logic, Analyze (problem-solving/reporting focus), Persuasion, and Propose (recommended actions, folding in Argue & Defend) -- to give the Long course genuinely exclusive content instead of being "Standard plus one unit." Standard's unit count is unaffected: it keeps exactly the 2 units (Logic, Analyze) it always had from this cluster; Persuasion and Propose are new Long-exclusive units. User then caught an ordering error: the initial split grouped units by source book (Logic, Analyze, then Persuasion, Propose) rather than pairing each skill with its advanced extension. Corrected to topic-paired order: Logic (10) -> Persuasion (11, Long-exclusive) -> Analyze (12) -> Propose (13, Long-exclusive), with old Units 12-13 renumbered to 14-15. This makes Standard non-contiguous across Units 9-14 (present at 10, 12, 14; absent at 11, 13) -- a deliberate tradeoff for pedagogical ordering. Corrected every cross-reference: Appendix B now pairs with Units 10 & 11, Appendix C with Units 12 & 13; Section 5b activities renumbered and reworded so Units 11 and 13 explicitly build on Units 10 and 12's work rather than starting fresh. Final counts: Essentials 8/15, Standard 12/15, Long 15/15 -- directly resolves the remaining half of Decision 5 (Long now has 3 genuinely exclusive units instead of 1).
- Added Section 7 to the plan: an 8-stage production checklist (design sign-off, content drafting, style infrastructure, per-tier build, validation, content/pedagogy review, PDF export, sign-off/delivery) so production quality can be tracked stage by stage. Grounded in this repo's actual tooling (`markdown-to-docx`, `validate_docx_against_reference.py`, `audit_docx_styles.py`, `docx-to-pdf`) and cross-referenced against the plan's own section/decision numbers rather than generic textbook-production advice. Explicitly flags that this title needs a reference DOCX built from scratch, unlike the Administrative Writing books which had one to inherit. Mirrored into the HTML artifact as interactive checkboxes grouped by stage. Caught and fixed a self-introduced duplication bug during editing (the checklist block was accidentally duplicated at the end of the markdown file); verified clean via heading-structure grep before considering the edit complete.
- Resolved 4 of the 5 remaining open plan decisions. Decision 6 (manuscript structure): three separate manuscripts, one each for Essentials/Standard/Long, not a single tagged source -- content fixes now propagate to up to three files. Decision 7 (Keys framework naming): user explicitly rejected treating this as an A-or-B pick, asking whether the two source frameworks actually overlap in content. Read both source units word-for-word (`01-1-keys-to-successful-presentations.md` in Speaking with PowerPoint, `02-2-keys-to-successful-presentations.md` in Making Speeches) instead of assuming -- found they describe the same four ideas at different granularity (Making Speeches merges Purpose+Content into one item, Speaking with PowerPoint splits them into two) plus exactly one genuinely additional item (PowerPoint/Visual Aids, present only in Speaking with PowerPoint). A combined "10 Keys" would double-count the same ideas under different labels, so it was not adopted. Resolved: 6 keys at Speaking with PowerPoint's granularity (Purpose, Content, Structure, Language, Delivery, Visual Aids), canonical name "Keys to Successful Presentations" with the number dropped from the brand name. Decision 8 (learner-audience framing): resolved to generalize away from Japanese-L1-specific framing for a broader non-native-English audience. Decision 9 (model speech content): resolved that all appendix model speeches will be freshly written, not refreshed versions of the existing Ventura/Cool Biz speeches.
- User caught a mischaracterization in the Decision 5 write-up from the entry above: it conflated two distinct questions under one heading -- unit-*inclusion* (which units belong to which tier) and Section 5b's activity *tier-scaling* (how each activity's depth changes between tiers). The user's earlier "largely agree, pending drafts" answer was specifically about 5b's activity scaling, not unit-inclusion -- and unit-inclusion was never actually open, since the Section 5 table itself is the decision record for that question, requiring no separate sign-off. Corrected Decision 5's text to state plainly that unit-inclusion is resolved via the table, and narrowed the still-open item to 5b's tier-scaling specifics only, which await Stage 2 drafts for final review but do not block drafting from starting. Updated the Section 7 Stage 1 checklist and all status counts (plan header, HTML masthead, footer) to reflect this precisely: 10 of 10 decisions resolved, with one narrow sub-item pending drafted review.
- User approved Section 5b's activity tier-scaling design as written at the planning stage, without waiting for drafted activities -- closing the one remaining open sub-item under Decision 5. All 10 design decisions in the plan are now fully resolved. Noted in the plan that this is approval of design intent, not a guarantee drafted execution will match it -- Stage 6 (Content & pedagogy review) remains the checkpoint for verifying drafted activities actually deliver the described scaling. Updated the plan's top-of-file status line ("draft plan, design decisions not yet fully resolved" -> "all 10 design decisions resolved, ready for Stage 2 content drafting"), the Section 7 Stage 1 checklist item, and all status badges in the HTML artifact (masthead, Decision 05 card, footer). Plan is now ready to move into Stage 2 (content drafting) per its own production checklist.

## 2026-06-01

- Updated `textmaker.cmd` so Windows dependency discovery is environment-aware rather than tied to one machine. The wrapper now probes common active-machine install roots for Pandoc, Poppler, and Tesseract before launch, while keeping the existing UNC-safe `pushd` behavior.

## 2026-05-19 (session 15 — module introductions, example-bad restructuring, postprocessor fix)

### Work completed

**INT book (`aw-int-all_0519.md`)**
- Added per-unit description bullet list to all 6 `## Module Guide` introductions — new section inserted between opening paragraph and "By the end of this module" outcomes list.
- Detected 26 edit/rewrite/revise/notice divs containing untagged weak-example labels (`**Original:**`, `**Weak draft**`, `**Weak version**`, `**Original Email:**`); extracted all 26 as preceding `:::example-bad` divs using automated script (`tag_example_bad_blocks.py`).
- Manually fixed 4 cases where instruction text was incorrectly included in the example-bad block (revise, notice, and 2 rewrite cases).
- Div balance: 532 opens / 532 closes (Match: True, 0 unclosed). PH markers: 255.
- Final example-bad div count: 40 (was 14 before this session).

**ADV book (`aw-adv-all_0516.md`)**
- Converted prose unit-description paragraphs in Modules 2–6 to bullet lists (one bullet per unit), matching the reference format already established in Module 1.

**Postprocessor (`apply_example_block_styles()` in `postprocess_docx.py`)**
- Added `_seen_italic` tracking flag: if no italic content has been seen in the current example div, non-italic Body Text paragraphs are styled (INT-style); if italic content has been seen, the first non-italic paragraph acts as a task instruction boundary (ADV-style). Fixes the INT book example styling that was only producing 14 styled paragraphs (now 179).

### Build results

- INT: 2263 list styles, 179 example block paragraphs (was 14), 40 example-bad divs, 255 placeholders, 465 icon labels. Clean build.
- ADV: 1698 list styles, 234 example block paragraphs (was 148), clean build.
- Both PDFs exported and opened.
- Both repos committed and pushed.

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

## 2026-05-18 (session 9 — style cleanup, table fixes, icon crops, CLI fix)

### Reference DOCX changes

- Removed `w:autoRedefine` from all 10 DivLabel paragraph styles that had it (`DivLabelBase` + 9 child styles). Child styles now rely on normal Word style inheritance. `DivLabelExampleGood` and `DivLabelExampleBad` already lacked it.
- Set cell margins on all 4 AW Table styles: top/bottom = 57 twips (0.1 cm), left/right = 113 twips (0.2 cm).

### Postprocessor fixes (`postprocess_docx.py`)

- `apply_table_styles()`: added direct enforcement of `tblW` (5000 pct = 100%) and `tblLayout` (autofit) on each table element after applying the style. Pandoc writes explicit `tblW` on generated tables which overrides style-level defaults — direct element patching is required.

### CLI fix (`cli.py`)

- Added `--tag-style` argument (`filled`/`outline`, default `filled`) to the `markdown-to-docx` CLI parser and wired it through to the postprocess call. Was previously only available when running `postprocess_docx.py` directly.

### Icon assets

- Tight-cropped all 9 `tag_outline_*` PNGs in `adv/md/working/div-tags-icons-2_assets/` to content bounds + 1px padding (matching the existing `tag_filled_*` treatment). Height reduced from 59px to ~55px.

## 2026-05-18 (session 10 — AW Table redesign, example block fixes, div fence fixes)

### AW Table style redesign

- User deleted all 4 AW Table styles from reference DOCX after Word refused to apply font/color overrides — root cause: Word's style cascade means table-style `rPr` is always overridden by paragraph styles in cell content.
- New architecture: 4 table styles handle borders/width/margins/firstRow fill only; two new paragraph styles `AW Table Header` and `AW Table Body` carry the font/size/spacing and are applied by the postprocessor to header-row and body-row cells respectively.
- Specs read from sample table created by user in `adv/md/bak/aw-adv-styleref_0515.docx`: header fill `31849B`, header font Roboto Condensed Medium 11pt white bold; body font Noto Sans Condensed Light 11pt, after=60 (3pt), suppressAutoHyphens, keepLines; borders single sz=8 all sides; cell margins top/bottom=57, left/right=142 twips.
- `apply_table_styles()` updated: applies `AW Table Header` to first-row cells and `AW Table Body` to all other cells for any AW-styled table.

### `apply_example_block_styles()` refinement

- Added `_example_seen_prose` flag: first non-italic `Body Text` after a DivLabel is example body content (styled); subsequent non-italic `Body Text` is task instruction (stops styling).
- List paragraphs inside example divs always receive example style — fixes numbered/bullet lists inside `example-good` boxes not being styled.
- Correctly handles: procedure-body examples, numbered-list worked examples, and mixed italic/prose examples without pulling post-example task instructions into the styled box.

### Source markdown fixes

- Fixed 2 misplaced `rewrite` div fences (L2143, L7323): setup instruction + `example` sub-div moved outside the `:::rewrite` open. Div balance remains 585/585.
- Fixed 5 malformed HTML underline tags `<uTEXT</u` → `[TEXT]{.underline}` at L2450–2454.

### Other changes

- Placeholder spacer height increased from 140 (7pt) to 280 (14pt) twips for clearer visual separation between consecutive placeholder tables.
- Working folder cleaned: removed 4 stale backup files; now contains only `aw-adv-all_0516.md`, `aw-adv-all_0518.docx`, `aw-adv-styleref.docx`, `div-tags-icons-2_assets/`.

### Build result (session 10)

- Pandoc: clean, no warnings. 597 div labels (458 icon + 61 emoji + 78 example). 378 example block paragraphs. All other counts stable.
- Validation: exit 0.

## 2026-05-19 (session 11 — inline icon rewrite, emoji removal, example block refinement)

### `apply_semantic_div_labels()` rewrite — inline icon approach

- Replaced the session 7 single-pass 2-column table approach with direct inline icon insertion.
- Icon run and 2× NBSP spacer run are prepended before the first existing run in the `DivLabel*` paragraph — no table created.
- `DivTag` character style applied to icon run via `w:rStyle` for style-driven 4pt baseline lowering.
- Removed `SEMANTIC_DIV_EMOJI` dict and all emoji fallback logic (61 emoji labels from session 10 are gone; divs with no icon file are now skipped silently).

### `apply_example_block_styles()` rewrite — closing-quote boundary detection

- Added `_after_closing_quote` flag: when a styled paragraph ends with `"` or `"`, the next paragraph is treated as post-example task instruction and stops styling.
- Added `NEUTRAL_MODEL_SOURCE_STYLES` (`Block Text`, `Quote`, `Intense Quote`) — these are always styled regardless of italic state.
- Added `QUOTED_MODEL_RE` — matches paragraphs enclosed in curly/straight quotes as model content.
- Correctly handles: procedure-body examples, numbered-list worked examples, mixed italic/prose examples, and quoted model text without pulling post-example instructions into the styled block.

### `apply_table_styles()` — reference DOCX style copy

- Added `reference_doc_path` parameter.
- Calls `_ensure_styles_from_reference()` to copy `AW Table Header` and `AW Table Body` into output DOCX if missing — Pandoc never propagates these styles since they don't appear in source markdown.
- `reference_doc_path` wired through from `insert_section_after_toc()` call site.

### Other postprocessor fixes

- `replace_unit_headings_with_title_tables()`: removes the original heading paragraph entirely (was converting to a page-break paragraph). Page break is now handled by `w:pageBreakBefore` on `AWUnitNumber` style in reference DOCX — avoids a spurious empty paragraph above the title table.
- `apply_body_text_to_normal_paragraphs()`: checks `style_id.startswith('DivLabel')` instead of checking against the now-deleted emoji dict.

### New: `docx-to-pdf` CLI command

- Added `scripts/docx_to_pdf.py`: converts DOCX to PDF using `docx2pdf` (Word COM on Windows).
- Registered as `docx-to-pdf` in `__main__.py`.

### Operational notes

- `textmaker.cmd` path corrected: was pointing to an old location. Updated system PATH and documented the OneDrive sync copy convention in `project-learning.md`.
- Session ended mid-process after VS Code reload required for PATH change to take effect. No build run this session.

## 2026-05-19 (session 13 — Intermediate book scan corrections)

### Issues corrected (from full PDF scan of aw-int-all_0519_stage7a.pdf)

- **F. Reflection wrapping (Issue 2)**: wrapped 22 F. Reflection numbered lists in `:::write` divs with "Reflection" title (Units 2-23). Unit 1 was already wrapped. Pattern: `### F. Reflection` heading followed by bare numbered list — added `:::write\nReflection\n\n` before and `:::\n` after.
- **Lowercase div labels (Issue 3)**: fixed 5 labels with incorrect title case:
  - L2557: `Politeness Scale (from direct ->most polite)` → `Politeness Scale (From Direct to Most Polite)`
  - L4039: `Before you explain a problem, ask` → `Before You Explain a Problem, Ask`
  - L4749: `Module 3 self-edit routine` → `Module 3 Self-Edit Routine`
  - L5147: `Teaching point` → `Teaching Point`
  - L6183: `To keep email style consistent, check` → `To Keep Email Style Consistent, Check`
- **Module 6 Key Lessons (Issue 8)**: added `:::learn` wrapper around Module 6 Review "Key lessons to keep" bullet list — the only module review without a div wrapper.
- **Issues 1, 6 already resolved**: "Example (Part of...)" headings in A sections were already inside `example-good` divs (correct orange rendering). Unit 15 example split was already `example-bad` + `example-good`.
- **AW Table Header (Issue 4, previous session)**: added `AW Table Header` paragraph style (styleId `AWTableHeader`, Roboto Condensed Medium 11pt bold white) to `aw-adv-styleref.docx` — was completely absent, causing all planning/grid table headers to be invisible.

### Build result (session 13)

- Source: `int/md/working/aw-int-all.md` — 10403 lines (up from 10288; +115 from div fence insertions)
- Div balance: 480 opens / 480 closes (Match: True)
- Postprocess: 2291 list styles, 92 alpha markers, 68 checklist items, 8 example block paragraphs, 620 post-list spacing, 18 table styles, 163 placeholders, 465 icon labels, 377 body text, 33 fallback replacements, 31 non-reference styles purged, 23 page breaks, 3 running headers, 23 unit title tables.
- Validation: exit 0.
- Output: `int/md/working/aw-int-all_0519_stage7b.docx` and `.pdf`
- Both repos committed and pushed.

## 2026-05-19 (session 14 — placeholder insertion, example div splits, heading/div title cleanup)

### Work completed

- **Placeholder insertion**: ran `C:\Temp\insert_placeholders.py` to insert ~71 `{{PH-N: code}}` response markers. One NOT FOUND (M2 revision lab — actual div title was `Revision Lab` not `Module 2 Revision Lab`); fixed manually. Final total: 255 PH markers across the INT book.

- **Example div identification and splitting**: identified 13 `:::notice`/`:::learn` divs containing Email A/B, Version A/B, and Summary A/B comparison pairs embedded as plain text. Each split into: original div (intro instruction only) + `:::example-bad` (Version A) + `:::example-good` (Version B). Script: `C:\Temp\split_examples.py`. 12 splits automatic; Module 4 Reader-Trust Clinic required manual fix (was `:::notice` not `:::learn`).

- **Heading restoration and div title renames**: `fix_heading_duplication.py` was run in error — it removed 135 `###` structural headings (A–F letter-sections and module-review sections). User correctly rejected this approach: structural headings must remain. Wrote and ran `C:\Temp\restore_headings_rename_divs.py` which:
  - Restored 83 letter-prefix headings (`### F. Reflection`, etc.)
  - Restored 41 module-prefix headings (`### module 2 email control checklist`, etc.)
  - Restored 11 special headings (6× Key Lessons to Keep, 5 comparison review sections)
  - Renamed 123 div titles to describe activity purpose instead of repeating heading text (e.g., `Reflection` → `Reflect on This Unit`, `Homework` → `Homework Task`, `What Is a Paragraph?` → `Definition`, `Notice Control Board` → `Control Board`, etc.)
  - Module-prefix headings: heading retains module number + full name in lowercase; div title becomes the short type name (e.g., `Email Control Checklist`)
  - Comparison sections renamed: `Email Comparison Review` → heading `### Email comparison review` + div title `Email Comparison`

### Key decision: div titles should describe activity purpose, not repeat heading text

- Confirmed user rule: "The structural headings (A–F) and above must remain. If the div title matches the heading, rewrite the div title based on the activity purpose."
- Addendum: "Headings can be shortened if they are long, and the specific detail removed from the heading can become the div title."

### Build result (session 14)

- Source: `int/md/working/aw-int-all_0519.md` — +671 lines net
- Div balance: 506 opens / 506 closes (confirmed via nesting stack check)
- Postprocess: 2240 list styles, 92 alpha markers, 68 checklist items, 14 example block paragraphs, 612 post-list spacing, 21 table styles, 255 placeholders, 465 icon labels, 369 body text, 33 fallback replacements, 31 non-reference styles purged, 23 page breaks, 3 running headers, 23 unit title tables.
- Output: `int/md/working/aw-int-all_0519.docx` and `.pdf` (outline tag style)
- Both repos committed and pushed.

### Outstanding issue: example block styling

- `apply_example_block_styles()` styled only 14 paragraphs — the `_example_seen_prose` boundary logic stops styling when it hits a non-italic `Body Text` paragraph after the first. INT book example bodies often use bold text (not italic), causing premature style cutoff. Pending fix.

## 2026-06-01 - INT Print-Readiness Tooling Fixes

- Scope: `scripts/postprocess_docx.py` and `scripts/docx_to_pdf.py`.
- Trigger: INT Unit 1 PDF/DOCX review found response tables after lists with inconsistent indentation, excessive gaps, narrow table width, and an automated-PDF-only numbered-list restart.
- Action: updated placeholder replacement to parse `rows=N`, remove the extra pre-table spacer, add small post-table spacing, normalize contiguous list runs before list-adjacent placeholders, align placeholder tables to the list text indent, and make list-adjacent placeholder tables extend to the right margin.
- Action: replaced the `docx-to-pdf` dependency on `docx2pdf.SaveAs(FileFormat=17)` with direct Word COM `ExportAsFixedFormat`.
- Verification: `python -m py_compile scripts/postprocess_docx.py scripts/docx_to_pdf.py` passes. A full temporary book build was started but stopped after it ran too long; Dave regenerated the DOCX/PDF manually afterward.

## 2026-06-01 - Case-Specific List Placeholder Policy

- Scope: `scripts/postprocess_docx.py`.
- Trigger: Dave clarified that list indentation should differ between one-placeholder-per-list-item activities and one-placeholder-after-the-whole-list activities.
- Action: changed placeholder replacement so the flush-number/hanging-indent/table-indent policy applies only when the placeholder follows a single-item list run. If the placeholder follows a contiguous multi-item list, the list and table retain normal positioning.
- Verification: `python -m py_compile scripts/postprocess_docx.py` passes.

## 2026-06-02 - List Spacing And Alphabetic List Regression Patch

- Scope: `scripts/postprocess_docx.py`.
- Trigger: Dave reported that list spacing edits appeared not to be applied and alphabetic lists were not being converted after the DOCX conversion refactor.
- Action: extended alphabetic marker detection/stripping from `A.` only to both `A.` and `A)`, and updated list detection so `Checklist` style paragraphs count as list paragraphs for spacing and placeholder policy checks.
- Verification: targeted temporary Markdown-to-DOCX probe showed `list styles`, `post-list spacing`, and `response placeholders` passes running with changed counts; `python -m compileall scripts` and `pytest -q` passed.
- Note: the probe also showed that Pandoc's DOCX writer can strip `- [ ]` checkbox markers before postprocess, leaving plain bullet paragraphs; true source-preserved checkbox styling needs an earlier pipeline marker rather than Word-stage guessing.

## 2026-06-09 - Hidden `No Title` Marker For Example Divs

- Scope: `scripts/postprocess_docx.py`.
- Trigger: Dave wanted neutral/good/bad example blocks to keep their semantic example styling while allowing selected visible example titles to be suppressed when redundant.
- Action: added `NO_TITLE_MARKER_RE` and updated `apply_example_block_styles()` so a `DivLabelExample`, `DivLabelExampleGood`, or `DivLabelExampleBad` paragraph containing exactly `No Title` is removed from the DOCX output but still activates the following example-content styling.
- Verification: `python -m py_compile scripts/postprocess_docx.py` passed.

## 2026-06-10 - `No Title` Regression Fix For Source-Driven Pipeline

- Scope: `scripts/postprocess_docx.py`.
- Trigger: Dave reported that all `No Title` labels were still visible in DOCX output. Diagnosis showed the suppression logic existed only inside `apply_example_block_styles()`, but that pass is intentionally skipped in the source-driven INT pipeline.
- Action: added a separate active `strip_hidden_example_labels()` pass and wired it into the main postprocess pipeline immediately after the skipped heuristic note. The new pass removes `DivLabelExample*` paragraphs whose text is exactly `No Title` while leaving source-driven `AW Example*` content styling untouched.
- Verification: `python -m py_compile scripts/postprocess_docx.py` passed.

## 2026-06-19 - Bosch Meeting 3a Evidence Holder Source Copy

- Created an editable revised DOCX copy of the Meeting 3a EV Dilemma simulation source with a new Evidence Summary holder column identifying which role had each item before the meeting.
- Cross-check result: most rows map directly to Roles A-F; Consumer behavior is a partial wording match to Role E, and Market competition has no exact matching role-sheet data point in the current source.
- Validation: Microsoft Word opened the revised DOCX and exported it to PDF; rendered evidence pages were visually checked for table readability.


## 2026-06-22 - Bosch PPTX Formatting Pass

- Updated the Bosch Logical Thinking & Discussion training slide deck in the client course folder using PowerPoint COM rather than regenerating the PPTX.
- Removed repeated footer text boxes from all slides, converted dense review/summary text to real PowerPoint bullet/numbered list structures, and increased body text sizes where appropriate.
- Preserved Slide 7 animation targets; XML validation found 60 Slide 7 animation targets and no missing shape IDs after the edit.
- Validation: exported 39 slide PNGs, created a contact sheet for layout review, and ran a PowerPoint text-bound overflow check with no remaining overflow issues.
- Backup created: Bosch 2026 - Logical Thinking & Discussion - Training Slides_bak20260622_before-formatting.pptx.


## 2026-06-22 - Bosch PPTX Bottom Bars And Typography Rebalance

- Removed remaining bottom blue bar shapes from the Bosch training PPTX after first deleting their text content.
- Rebalanced non-body text after body/list font enlargement: slide titles, top labels, section transition subtitles, framework labels, table headers, and Slide 7 labels.
- Validation: PowerPoint text-bound overflow check reports no issues; Slide 7 animation target XML still has 60 targets with no missing shape IDs; rendered contact sheet and spot-checked Slide 7 and a transition slide.


## 2026-06-22 - Bosch PPTX Reduced To Slide 7

- Per user request, deleted all slides from the Bosch training PPTX except the former Slide 7 mini logic puzzle slide.
- Backup created before deletion: Bosch 2026 - Logical Thinking & Discussion - Training Slides_bak20260622_before-delete-all-but-slide7.pptx.
- Validation: current one-slide deck contains the former Slide 7 as slide1.xml; animation target IDs and timing node count match the immediate pre-deletion backup, with no missing target shapes.


## 2026-06-22 - Bosch PPTX Argument Model Slides Added

- Added three slides after the preserved mini logic puzzle slide: ORE puzzle explanation, PBSR puzzle process explanation, and PCAF discussion question slide.
- Textbook references used on slides: ORE pp. 1-3, PBSR p. 16, PCAF p. 19.
- PCAF slide is framed as a discussion prompt rather than an applied solution model because the puzzle resolves logically to one outcome rather than two debatable sides.
- Validation: deck now has 4 slides; preserved puzzle slide animation targets remain valid with no missing target shapes; PowerPoint text overflow check reports no issues; rendered slides were visually checked.

