# Plan 3 Appendix Script Repair Round 2

Date: 2026-08-13

Purpose: continue repair work after `plan3-appendix-full-script-review-round-1.md`, with emphasis on learner-facing clarity, script/support-material separation, and handoff readiness.

## Files Edited

- `books/Speaking with PowerPoint/revision/drafts/appendices/process-improvement-briefing-models.md`
- `books/Speaking with PowerPoint/revision/drafts/appendices/product-service-program-launch-models.md`
- `books/Speaking with PowerPoint/revision/drafts/appendices/project-results-briefing-models.md`
- `books/Speaking with PowerPoint/revision/drafts/standard/standard-unit-03.md`
- `books/Speaking with PowerPoint/README.md`
- `project-learning.md`
- `project-journal.md`

## Repair Actions Completed

1. Added `How to Use These Models` notes to the appendix files to make clear that full spoken script sections are learner-facing scripts and the surrounding material is support material.
2. Added `Key Vocabulary Before Listening` sections before the full scripts so difficult terms are introduced before learners read or listen.
3. Normalized heading capitalization in the launch and results appendices.
4. Removed one teaching-only phrase from process language notes: `Use "fictional practice data" when numbers are invented for learning.`
5. Replaced one spoken-script phrase, `In this practice case`, with `In this scenario`.
6. Removed one securities/investment guardrail sentence from a spoken results script because it belonged in support material, not in presenter voice.
7. Revised Unit 3 Practice 3 planning map to group items under `Introduction`, `Body`, and `Conclusion`; numbered the items under each section; replaced the old backup-detail row with `Summary of key points`.
8. Tightened Standard unit cross-references in Units 1, 7, 8, 9, 10, 11, and 12 so they point to the named appendix model sets and their business-client/government-agency variants.
9. Replaced one ordinary spoken-script `lessons` phrase with `points` to keep terminology scans focused on `Unit` for textbook components.
10. Updated `plan3-case-model-brief.md`, `plan3-traceability.md`, and `standard-12-unit-curriculum-spec.md` so the control layer reflects exact appendix model-set reference wording and the revised Unit 3 planning map.
11. Updated Unit 4 with limitation/risk signposting phrases and a spoken drill after phrase-repair practice, addressing recorded review findings.
12. Updated Unit 5 by defining `accessibility` before the checklist and adding corrected slide-title examples for article/plural/noun-phrase problems.
13. Corrected the stale `Trade confirmation workflow before and after` asset title in `plan3_image_register.json` to `Import document handoff workflow before and after`.
14. Updated Plan 3 review sequencing in `plan3.md` and `plan3-phase6-qa-checklist.md`: Agent 3 Business Presentation Specialist must run first, its findings must be integrated, and Agent 2 Language Editor must run last because English language development is the highest-priority goal.
15. Created `books/Speaking with PowerPoint/revision/drafts/Teacher Notes.md` as a separate printable teacher-notes document with Unit and Appendix references.
16. Removed embedded teacher-note sections from `standard-unit-01.md` through `standard-unit-12.md`.
17. Converted appendix teacher/editor-facing wording into learner-facing instructions and headings.
18. Updated `Teacher Notes.md` with general teaching notes, the mandatory specialist-review sequence, terminology/glossary watchlist, and notes for the revised Unit 3, Unit 4, and Unit 5 learner content.

## Timing Check

Script-only word count after edits, using the approved 115-125 wpm B1-B2 timing range:

| Model file | Script 1 | Script 2 |
|---|---:|---:|
| Process Improvement Briefing Models | 811 words; about 6.5-7.1 minutes | 779 words; about 6.2-6.8 minutes |
| Product, Service, or Program Launch Models | 911 words; about 7.3-7.9 minutes | 843 words; about 6.7-7.3 minutes |
| Project Results Briefing Models | 663 words; about 5.3-5.8 minutes | 682 words; about 5.5-5.9 minutes |

## Remaining Work

1. Run the next specialist checks sequentially: Agent 3 Business Presentation Specialist first, integrate findings, then Agent 2 Language Editor last.
2. Continue deeper Standard unit revision with Unit 6 data/chart language after the sequencing-sensitive language/glossary pass is complete.

## Validation

- Script-only timing check completed against the approved 115-125 wpm B1-B2 timing range.
- Scan completed for stale `lesson` terminology, old `backup detail` wording, vague appendix-model references, and financial-trading terms in current Standard drafts and appendix model files.
- Remaining stock/securities/ticker hits are guardrail notes, not model contexts.
- `plan3_image_register.json` validated with `python -m json.tool`.
- Scan completed for teacher/editor-facing labels in learner draft files. No matches remain under `revision/drafts/standard/` or `revision/drafts/appendices/`; teacher-facing notes now live in the separate teacher-notes document.
- Latest learner-facing scan only returns Unit 7 uses of `support material(s)`, where the term refers to presentation materials for learners, not teacher/editor notes.

## Worktree Note

Unrelated uncommitted work exists under `br2e_styleguide/`. It was not edited or staged as part of this repair round.
