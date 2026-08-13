# Plan 3 Phase 6 Issue Classification Log

Created: 2026-08-13

Purpose: classify significant Phase 6 issues by type, source, affected QA IDs, and disposition so external and internal review findings are traceable.

Issue types: `scope`, `pedagogy`, `factual accuracy`, `accessibility`, `assessment`, `production`, `style`.

## Significant Issues

| Issue ID | Source | Issue Summary | Type | Affected QA IDs | Status | Owner | Disposition / Next Action | Traceability Updated |
|---|---|---|---|---|---|---|---|---|
| P6-I01 | Phase 6 checklist; Agent 1 | Traceability matrix lacked row-level Phase 6 status/evidence. | production | QA-001, QA-002, QA-121 | Repaired in control layer | Content Architect | Added Phase 6 execution tracking to `plan3-traceability.md`. | Yes |
| P6-I02 | Phase 6 checklist; Agent 1 | Deferred work was scattered and lacked one authoritative defer log. | production | QA-003, QA-120, QA-122 | Repaired in control layer | Content Architect | Created `plan3-phase6-defer-log.md`; active repairs remain open. | Yes |
| P6-I03 | Phase 6 checklist; Agent 1 | Significant issues were not classified by type. | production | QA-119, QA-120 | Repaired in control layer | Content Architect | Created this issue classification log. | Yes |
| P6-I04 | User review; Agent 2; Agent 4 | Appendix model scripts are too generic and need concrete fictional details, examples, and workplace realism. | pedagogy | QA-011, QA-012, QA-021, QA-022, QA-023, QA-087 | Repaired | Business/Government Presentation Specialist, Language Editor | Six model scripts now include concrete fictional details and examples; final Language Editor recheck passed. | Yes |
| P6-I05 | User correction; project memory; Agent 2 | Business/trading examples must mean general trading-company operations, not securities/financial-market trading. | factual accuracy | QA-021, QA-023, QA-025, QA-085, QA-087 | Repaired | Business/Government Presentation Specialist | Business examples now use general trading-company/client-service operations; QA-085 source verification passed for current manuscript claims. | Yes |
| P6-I06 | Agent 2; Agent 4 | Government examples need concrete administrative/service-delivery detail without becoming business cases with agency labels. | pedagogy | QA-021, QA-022, QA-026, QA-087 | Repaired | Business/Government Presentation Specialist | Government models now include application types, channels, staffing/workload details, and service-process examples. | Yes |
| P6-I07 | Agent 4 | Specialized terms need first-use support or glossary/before-listening support. | pedagogy | QA-033, QA-027, QA-028 | Repaired | Language Editor | Local useful-terms boxes and Teacher Notes terminology watchlist were expanded; final Language Editor recheck passed. | Yes |
| P6-I08 | Agent 4; Phase 6 checklist | Unit 3 does not sufficiently explain what makes a good example/evidence item. | pedagogy | QA-011, QA-012 | Repaired | Content Architect, Language Editor | Unit 3 now explains examples, evidence, explanation, detail placement, and includes an options-based mini example. | Yes |
| P6-I09 | Phase 6 checklist; Agent 4 | Options-based decision model is missing although Unit 3 teaches that structure. | pedagogy | QA-020, QA-012 | Deferred or future repair | Content Architect | Listed in defer log; decide after model-script repair whether to add a short model/excerpt. | Yes |
| P6-I10 | Agent 4 | Unit 12 has assessment categories but lacks explicit B1/B2 descriptors where language is assessed. | assessment | QA-097, QA-095, QA-096 | Repaired | Language Editor | Added learner-facing B1/B2 descriptor guidance and teacher-note assessor guidance. | Yes |
| P6-I11 | Phase 6 checklist | Pointer/cursor guidance is too light. | pedagogy | QA-058, P1-23 | Repaired | Content Architect, Language Editor | Expanded safe laser/cursor/highlighter/annotation/zoom guidance. | Yes |
| P6-I12 | User review; Phase 5 notes | Generated visual assets and model-slide PNGs were rejected as visually unprofessional. | production | QA-024, QA-053, QA-066, QA-067, QA-071, QA-074, QA-075, QA-079, QA-080, QA-081, QA-091, QA-093, QA-114 | Deferred separate workstream | Asset and QA Specialist | Visual/asset repair paused; Canva and Default templates pinned for later. | Yes |
| P6-I13 | Agent 4 | Learner-facing appendices still contain production-facing wording about draft decks/visual approval. | style | QA-019, QA-104, QA-116 | Repaired | Language Editor | Removed production-facing notes from learner appendices. | Yes |
| P6-I14 | Phase 6 checklist; Agent 4 | Broken image/deck references remain after rejected asset deletion. | production | QA-019, QA-104 | Repaired for text; visual assets deferred | Production QA | Removed deleted-image embeds from learner drafts; visual asset replacement remains deferred. | Yes |
| P6-I15 | Phase 6 checklist | Official-source verification for tool/accessibility/2026 workplace claims is incomplete. | factual accuracy | QA-085 | Repaired | Content Architect, Language Editor | Source verification saved in `revision/records/plan3-phase6-source-verification.md`; re-run only if later revisions add specific software feature, pricing, legal/regulatory, or time-sensitive claims. | Yes |
| P6-I16 | Phase 6 checklist | Final title, metadata, exports, accessibility checks, page-flow checks, and release notes do not exist yet. | production | QA-068, QA-069, QA-070, QA-073, QA-094, QA-101, QA-102, QA-107, QA-109, QA-110, QA-122 | Deferred | Production QA | Listed in defer log; recheck after final DOCX/PDF exports. | Yes |
| P6-I17 | Phase 6 checklist | Essentials and Long tiers are not drafted, so cross-tier checks cannot pass. | scope | QA-007, QA-008, QA-061, QA-111, QA-112, QA-113, QA-115 | Deferred | Content Architect | Listed in defer log; recheck during tier adaptation phases. | Yes |
| P6-I18 | Phase 6 checklist | Final proof/style/reference checks remain open until text and asset references are settled. | style | QA-103, QA-104, QA-105, QA-106 | Repaired for current source | Language Editor, Production QA | Final source-level proof/style/reference scans passed; layout/export checks remain in production QA. | Yes |

## Current Priority Order

1. Keep visual/asset repair paused until the separate visual/deck-production workstream resumes.
2. After visual/assets are repaired, update the image register and re-run asset/accessibility/model-visual QA.
3. After final DOCX/PDF export, run metadata, accessibility, blank-page, and visual layout checks.

Visual/asset repair remains outside this sequence.
