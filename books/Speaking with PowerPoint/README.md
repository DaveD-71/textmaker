# Speaking with PowerPoint Folder Layout

This folder is split into two working areas.

- `revision/` contains all current 2026 revision work: Plan 3 control files, draft units, appendix model source packs, review records, feedback records, and archived revision plans.
- `old/` contains preserved source/reference material from the original textbook: the original PDF/DOCX files and extracted conversion output.

Use `revision/control/plan3.md` as the current production plan. Use `revision/records/` for durable multi-agent work records and review logs.

The textbook manuscript drafts under `revision/drafts/standard/` and `revision/drafts/appendices/` should be completely learner-facing. Teacher-facing guidance belongs in the separate printable file `revision/drafts/Teacher Notes.md`.

## Current Handoff Status

Updated: 2026-08-13 20:15 JST

Latest Phase 6 control update:

- Phase 6 repair-agent review round 1 is recorded at `revision/records/plan3-phase6-repair-agent-review-round-1.md`.
- Phase 6 manuscript repair round 1 is recorded at `revision/records/plan3-phase6-manuscript-repair-round-1.md`.
- Phase 6 control-layer repair is now complete for traceability/defer/classification:
  - `revision/control/plan3-traceability.md` now has a Phase 6 execution tracking section covering all consolidated task IDs and Plan 3-specific requirements.
  - `revision/control/plan3-phase6-defer-log.md` now records deferred work with reason, impact, owner, future action, and recheck trigger.
  - `revision/control/plan3-phase6-issue-classification-log.md` now classifies significant current issues by type, affected QA IDs, status, owner, and disposition.
  - `revision/control/plan3-phase6-qa-checklist.md` now marks QA-001, QA-002, QA-003, QA-119, and QA-121 as Pass because the supporting control files exist.
- Phase 6 manuscript repair round 1 completed:
  - six appendix model scripts now include concrete fictional business-client and government-agency details;
  - deleted-image embeds and production-facing draft-deck notes were removed from learner-facing drafts;
  - Unit 3 now teaches examples/evidence/detail placement and includes an options-based decision mini example;
  - Unit 6 has useful-terms support;
  - Unit 8 has expanded pointer/cursor/laser/annotation/zoom guidance;
  - Unit 12 has an explicit Learner Deliverable section and B1/B2 language-level descriptors;
  - Teacher Notes has expanded terminology and B1/B2 assessor guidance.
- Final Language Editor recheck after manuscript repair passed with no blocking language issues.
- QA-085 source verification is recorded at `revision/records/plan3-phase6-source-verification.md`.
- Final source-level proof/style/reference scans are complete for current Markdown source.
- Current Phase 6 QA count after non-visual Phase 6 repair: 87 Pass, 15 Repair, 19 Defer, 1 N/A.
- Visual/asset repair remains intentionally paused. Canva plugin/MCP and the `Default templates` plugin are pinned for later visual/deck-production exploration.
- Remaining Repair rows: QA-012, QA-024, QA-053, QA-066, QA-067, QA-071, QA-074, QA-075, QA-079, QA-080, QA-081, QA-091, QA-093, QA-114, QA-120.
- Next step: resume the visual/deck-production workstream when ready. Remaining Repair rows are visual/asset-related, except QA-120, which stays Repair as the summary row until the visual/asset issues are repaired or formally deferred.

- Latest synced baseline before today's edits: commit `357ec3e Reframe appendix models for client context`.
- Current uncommitted Speaking with PowerPoint edits:
  - `revision/drafts/standard/standard-unit-03.md`: Practice 3 planning map now uses `Introduction`, `Body`, and `Conclusion`, with numbered items under each section. The old backup-detail row was replaced by `Summary of key points`.
  - `revision/drafts/appendices/process-improvement-briefing-models.md`: added clear script/support-material boundary and before-listening vocabulary; removed a teaching-only fictional-data phrase from language focus; replaced one spoken `practice case` phrase with `scenario`.
  - `revision/drafts/appendices/product-service-program-launch-models.md`: normalized headings, added clear script/support-material boundary, and added before-listening vocabulary for both model scripts.
  - `revision/drafts/appendices/project-results-briefing-models.md`: normalized headings, added clear script/support-material boundary, added before-listening vocabulary for both model scripts, and removed one securities/investment guardrail sentence from the spoken script.
  - Standard unit cross-references were tightened in Units 1, 7, 8, 9, 10, 11, and 12 so they point to the named appendix model sets and their business-client/government-agency variants.
  - `revision/control/plan3-case-model-brief.md`, `revision/control/plan3-traceability.md`, and `revision/control/standard-12-unit-curriculum-spec.md`: updated to reflect the revised Unit 3 planning map and exact appendix model-set reference wording.
  - `revision/control/plan3_image_register.json`: corrected the stale `Trade confirmation workflow before and after` asset title to `Import document handoff workflow before and after`.
  - `revision/drafts/standard/standard-unit-04.md`: added limitation/risk signposting phrases and a spoken drill after phrase-repair practice, addressing the recorded Agent 2/3 review findings for Unit 4.
  - `revision/drafts/standard/standard-unit-05.md`: defined `accessibility` before the checklist and added corrected slide-title examples for article/plural/noun-phrase problems.
  - `revision/control/plan3.md` and `revision/control/plan3-phase6-qa-checklist.md`: added a mandatory review-sequencing rule. Agent 3, the Business Presentation Specialist, runs first; its findings are integrated; then Agent 2, the Language Editor, runs last because English language development is the highest priority.
  - `revision/drafts/Teacher Notes.md`: created as a separate printable teacher-notes document with Unit and Appendix references.
  - `revision/drafts/Teacher Notes.md`: updated with general teaching notes, the sequential specialist-review rule, terminology/glossary watchlist, and specific notes for the revised Unit 3 planning map, Unit 4 risk signposting drill, and Unit 5 accessibility/title-language work. A Language Editor pass clarified `leave behind` versus the style-dependent noun `leave-behind`, recommends learner-facing alternatives such as `follow-up handout` and `takeaway document`, and softened/standardized several teacher-note instructions.
  - `revision/drafts/Teacher Notes.md`: clarified the Unit 1 note about example scope. Unit 1 should teach audience, purpose, and audience outcome; business-client and government-agency examples should be brief, with fuller workplace examples handled later through appendix models.
  - `revision/drafts/Teacher Notes.md`: clarified that the printed textbook should be role-agnostic, but classroom delivery can be client-specific. Teachers may adapt examples and practice contexts to the learners' company, organization, roles, and communication needs.
  - `revision/drafts/standard/standard-unit-07.md` and `revision/drafts/appendices/product-service-program-launch-models.md`: replaced learner-facing `leave-behind(s)` with `follow-up handout(s)` for clarity.
  - `revision/records/plan3-sequential-review-round-2.md`: saved the sequential Agent 3 then Agent 2 review record.
  - Agent 3 business repairs integrated before Agent 2: business-client guardrails now allow fictional/sanitized shipment, order, procurement, supplier-status, workflow, and reporting examples; Unit 12 `trade data` wording was replaced; Unit 1 was renamed to `Audience, Purpose, and Workplace Context`; launch/results model headings now identify Business Client or Government Agency variants.
  - `revision/drafts/Teacher Notes.md`: added course-planning teaching-time guidance for Units 1-12.
  - `revision/control/plan3-phase6-qa-checklist.md`: added a QA/defer check for the missing full model presentation demonstrating Unit 3's `Situation - options - criteria - recommendation` structure.
  - `revision/drafts/standard/standard-unit-12.md`: added `Practice task 3: textbook wrap-up quiz` to consolidate learning points across the textbook, especially for 1-to-1 classes where final-presentation delivery time is short.
  - `revision/drafts/Teacher Notes.md`: revised Unit 12 timing guidance for 1-to-1 lessons and added the wrap-up quiz answer key.
  - `revision/control/standard-12-unit-curriculum-spec.md`, `revision/control/plan3-traceability.md`, and `revision/control/plan3-phase6-qa-checklist.md`: updated Unit 12 deliverables/QA to include the textbook wrap-up quiz.
  - `revision/control/plan3-style-sheet.md`: changed heading convention from sentence-style headings to Chicago-style title case, including capitalization after colons for subtitles/subheadings.
  - Current Standard unit drafts, appendix drafts, and `Teacher Notes.md`: normalized Markdown headings and subheadings to Chicago-style title case.
  - `revision/drafts/standard/standard-unit-01.md` through `standard-unit-12.md`: removed embedded teacher-note sections so learner units remain learner-facing.
  - `revision/drafts/appendices/*.md`: converted teacher/editor-facing labels such as `learner-facing`, `support material`, `Teaching-Point Map`, and `Comparison Note for Teachers` into learner-facing instructions and headings.
  - Phase 4 Agent 2 repairs are now integrated: Units 1, 4, 5, 7, and 9 have first-use `Useful terms` support; Unit 1 now uses `workplace` wording instead of stale `business` context wording; Unit 9 defines `asynchronous (async)` before learner use; the launch appendix vocabulary now includes `pre-read` and `rollout`; the launch appendix AI note is learner-facing classroom wording.
  - Phase 5 asset creation was rerun through the OpenAI Python SDK, using `gpt-image-2` at 2560x1440 high-quality opaque PNG. To avoid the persistent UNC/network-path issue, generation was staged in local `%TEMP%` and copied back into the repo.
  - OpenAI output is now used only as sparse, text-free source-panel art. Final visible text, chart values, headings, and slide layouts are composed deterministically with Pillow so the textbook does not depend on image-model text rendering.
  - Correction after user review: the generated PNG assets in `images/planned/` and `images/model-slides/` were rejected as visually unprofessional and deleted from the active project tree. Keep `images/source/openai-sdk-2k-final/` only as source/provenance material unless the user decides otherwise.
  - The appendix model files now link to editable PPTX slide-deck drafts instead of embedding the rejected PNG slide images.
  - New slide-deck direction: use standard PowerPoint-native slide layouts/placeholders so PowerPoint Designer can improve the deck. Do not build bespoke PptxGenJS shape systems for these model decks unless the user explicitly changes this decision.
  - One readable test deck exists for inspection: `revision/assets/model-slide-decks/process-business-standard-template-v2.pptx`, with PDF/contact-sheet exports under `revision/assets/model-slide-decks/pdf/`.
  - `revision/control/plan3_image_register.json` records the rejected core image assets and draft editable model slide-deck entries. Status remains `draft` pending user/editor approval.
- Script timing check after edits:
  - Process model scripts: 811 and 779 words, about 6.2-7.1 minutes at 115-125 wpm.
  - Launch model scripts: 911 and 843 words, about 6.7-7.9 minutes at 115-125 wpm.
  - Results model scripts: 663 and 682 words, about 5.3-5.9 minutes at 115-125 wpm.
- Unrelated uncommitted work exists under `br2e_styleguide/`; do not stage or modify it as part of this textbook revision unless the user explicitly asks.

Validation completed in this pass:

- Script-only timing check against the approved 115-125 wpm range.
- Scan for stale `lesson` terminology, old `backup detail` wording, and vague appendix-model references in current control files, Standard drafts, and appendix model files.
- `plan3_image_register.json` validates with `python -m json.tool`.
- Earlier Phase 5 PNG validation was superseded by user review. The visible PNG slide/core assets were rejected and removed; the current acceptable direction is the readable native PowerPoint test deck.
- The current standard-template test deck has six slides using native PowerPoint layouts only: Title Slide, Title and Text, and Comparison.
- Remaining hits for stock/securities/ticker language are guardrail notes, not model contexts.
- Scan confirms no teacher/editor-facing labels remain in learner draft files under `revision/drafts/standard/` or `revision/drafts/appendices/`; the separate teacher-notes file is the only teacher-facing draft document.
- Teacher Notes Language Editor pass completed: `leave-behind` is not recommended for learner-facing text; use `follow-up handout`, `takeaway document`, or `supporting document` unless explicitly teaching the industry noun.
- Current learner drafts now have no `leave-behind` hits.
- Latest learner-facing scan only returns Unit 7 uses of `support material(s)`, where the term refers to presentation materials for learners, not teacher/editor notes.
- Sequential review round 2 verdict: Agent 3 and Agent 2 both returned `Pass with repairs`.
- Heading capitalization scan found no current draft/control Markdown headings with lowercase text immediately after a colon.
- Targeted Phase 4 repair scans found no remaining Unit 1 stale phrases: `business purpose`, `business reason`, `business problem`, `Main business context`, or `business relevance`.
- Launch appendix scan confirms `If your class discusses AI...` is now the active learner-facing AI note and the old `If AI is mentioned with these models...` wording is gone.

Next recommended step: inspect `revision/assets/model-slide-decks/process-business-standard-template-v2.pptx` in PowerPoint, try Designer on it, then decide the standard-template pattern before rebuilding the other five appendix model slide decks. Keep the missing options-based decision model as a tracked Phase 6 QA/defer item unless the user chooses to add that model before layout work.

