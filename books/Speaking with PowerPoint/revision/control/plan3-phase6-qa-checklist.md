# Plan 3 Phase 6 QA Checklist

Prepared: 2026-08-12

Purpose: provide the operational QA checklist for Phase 6 of Plan 3: "Run QA, repair, and final consistency passes." This file is used after unit content, assets, and tier adaptations exist. It complements `plan3-traceability.md`, which maps requirements before implementation.

Execution updated: 2026-08-13 by Codex. Every checklist row below was assigned a Phase 6 status from the current Standard drafts, appendices, control files, asset register, and generated-asset state. Statuses are evidence of audit only, not final approval.


## QA Status Legend

- Pass: requirement is complete and verified
- Repair: issue found and must be fixed before release
- Defer: intentionally postponed with reason and owner
- N/A: not applicable to this tier or deliverable

Every Repair and Defer item must include a note, file/location, owner, and next action.

When Phase 6 is executed, each checklist row must be tracked with this evidence format:

| ID | Check | Tier/Deliverable | Status | Evidence/File | Owner | Repair/Defer Action | Recheck Result |
| --- | --- | --- | --- | --- | --- | --- | --- |

The simplified tables below define the checks. The execution log must add the evidence, owner, action, and recheck fields.

## 1. Requirement Coverage QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-001 | Every row in `plan3-traceability.md` is marked Pass, Repair, Defer, or N/A after implementation | Pass | `plan3-traceability.md` now includes a Phase 6 execution tracking section with row-level status, evidence, owner, action, and recheck result. |
| QA-002 | Every consolidated task ID from P0-01 through P3-04 has evidence of completion, reframing, promotion, supersession, or deferral | Pass | All consolidated task IDs are covered in the Phase 6 execution tracking section of `plan3-traceability.md`; open repairs and deferred items are explicitly marked. |
| QA-003 | Deferred items are listed in a final defer log with reason, impact, and recommended future action | Pass | `plan3-phase6-defer-log.md` now lists deferred tier, export, release-note, options-model, and visual/asset work with reason, impact, owner, future action, and recheck trigger. |
| QA-004 | No Plan 3 requirement was dropped because it was absent from the old two-day task list | Pass | Plan 3-specific requirements beyond the two-day list are present in traceability and QA sections. |
| QA-005 | The final books still match the Plan 3 scope: tool-neutral business presentation skills for B1-B2 learners | Pass | Current Standard draft is tool-neutral B1-B2 business presentation material, though assets/models need repair. |

## 2. Curriculum and unit QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-006 | Standard has 12 Units matching the approved spine | Pass | Twelve Standard unit draft files exist and match the approved spine. |
| QA-007 | Essentials has 8 Units and compresses Standard without contradicting it | Defer | Essentials 8-unit manuscript has not been drafted. |
| QA-008 | Long has 15 Units and expands Standard without adding conflicting pedagogy | Defer | Long 15-unit manuscript has not been drafted. |
| QA-009 | Each unit has 1-3 measurable learner outcomes | Pass | All 12 Standard units contain three learning outcomes. |
| QA-010 | Each unit includes a clear learner deliverable or cumulative portfolio step | Pass | All 12 Standard units now include a learner deliverable heading or cumulative portfolio step; Unit 12 has an explicit Learner Deliverable section. |
| QA-011 | Each major teaching point has a learner task, not only explanation | Pass | Unit 3 now includes explicit example/evidence scaffolding and checks that every main point has an example, evidence, or explanation; model scripts now include more concrete examples. |
| QA-012 | Model presentations are mapped to Units, language points, visual-design points, delivery behaviors, and assessment criteria | Repair | Appendix skill maps exist, but model visuals are draft/rejected and model scripts need stronger mapping to example quality and visual principles. |
| QA-013 | The three recurring business cases are used consistently: process improvement, product/service launch, project results briefing | Pass | Process improvement, launch, and results cases recur in units and appendix model sets. |
| QA-014 | Final presentation task is clearly connected to earlier unit outputs | Pass | Unit 12 explicitly draws together audience, message, structure, visuals, evidence, tool choice, delivery, Q&A, and reflection. |
| QA-015 | Unit 12 includes a textbook wrap-up task for consolidation, especially for 1-to-1 classes where final presentation time is short | Pass | Unit 12 includes a textbook wrap-up quiz and teacher notes explain its 1-to-1 use. |
| QA-016 | Teacher notes, answer keys, or sample answers exist where learners or instructors need them | Pass | Teacher Notes includes timing guidance and answer keys for the Unit 12 wrap-up quiz; further sample answers may be added after repairs. |

## 2a. Example, Model, and Appendix Audience QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-017 | Main unit body is role-agnostic between government-agency clients and business clients | Pass | Main Standard unit body is generally role-agnostic; role-specific material is mostly in model references and teacher notes. |
| QA-018 | Government-agency and business-client specificity appears in examples, models, appendices, teacher notes, or optional variants rather than changing the core unit sequence | Pass | Business/government specificity is concentrated in appendices, teacher notes, and optional model references rather than changing the unit sequence. |
| QA-019 | Appendix models are referenced from the main unit body where they support the taught skill | Pass | Appendix model references exist where relevant; broken deleted-image embeds were removed from learner-facing unit and appendix drafts. |
| QA-020 | Missing options-based decision presentation model is tracked for deferral or future repair | Defer | Missing options-based decision model is explicitly tracked in QA notes; no model has been added yet. Existing note: Unit 3 teaches `Situation - options - criteria - recommendation`, but the current appendix model set does not yet include a full model presentation for that structure. Defer or add a short model/excerpt before final release. |
| QA-021 | Business-client and government-agency variants teach the same underlying skill with comparable quality and depth | Pass | Process, launch, and results model pairs now include parallel skill coverage with concrete business-client and government-agency details. |
| QA-022 | Government-agency examples are genuinely public-sector appropriate, not business examples with names swapped | Pass | Government models now include administrative/service details such as housing support certificates, resident certificate support, counter/online channels, support-desk hours, and specific application types. |
| QA-023 | Business-client examples are genuinely business appropriate, not public-sector examples with names swapped | Pass | Business models now include general trading-company/client-service operations details such as imported industrial parts, Supplier A packing-list issues, Team North/West, shipment-reporting deadlines, and named fictional expansion desks. |
| QA-024 | Government-facing visuals avoid real national flags, seals, emblems, crests, and country-specific iconography unless intentionally required and verified | Repair | Text guardrails exist, but final government visuals are missing/rejected so visual compliance cannot pass. |
| QA-025 | Business-client banking/leasing or general trading-company examples allow fictional or sanitized procurement, supplier-status, shipment, order, workflow, and reporting contexts, while avoiding investment advice, securities-market prediction, real identifying customer/account/order/shipment/transaction data, regulatory/legal advice, real firm names, securities exchange names, and stock ticker symbols | Pass | Guardrails against securities, investment advice, real identifiers, legal/regulatory advice, and real firm names are present. |
| QA-026 | Government-agency examples stay within administrative tasks, service delivery, reporting, coordination, process improvement, and service communication unless explicitly approved | Pass | Government examples stay in administrative/service/process contexts in current drafts. |

## 3. ESL and Business English QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-027 | Language level is appropriate for B1-B2 business English learners | Pass | Standard units are generally clear B1-B2 business English; final Language Editor pass still needed after repairs. |
| QA-028 | Instructions are clear, direct, and not overloaded with advanced vocabulary | Pass | Instructions are mostly direct and task-oriented; no major overload found in Standard units. |
| QA-029 | Presentation English syllabus is explicit: openings, relevance, previews, transitions, references, emphasis, summaries, recommendations, action closes | Pass | Units 2, 4, 6, 10, and 12 make the presentation-English syllabus explicit. |
| QA-030 | Q&A language includes clarifying, answering directly, structuring, checking satisfaction, deferring, disagreement, and follow-up | Pass | Unit 10 covers clarifying, direct answering, structuring, satisfaction checks, deferral, disagreement, and follow-up. |
| QA-031 | Business Presentation Specialist review is completed and integrated before the final Language Editor review | Pass | Business/context model repairs were completed first, then the final Language Editor recheck passed with no blocking language issues. |
| QA-032 | Agent 2 and Agent 3 are not run concurrently for final content review because the language review depends on the settled business/context wording | Pass | Plan 3 and QA specify non-concurrent final review order; recorded sequential review followed that order. |
| QA-033 | Specialized business/process terms are defined before learner use, with glossary or before-listening support where needed | Pass | Specialized terms now have adequate first-use, useful-terms, before-listening, or Teacher Notes support; final Language Editor recheck passed. |
| QA-034 | Register notes distinguish formal, neutral, and conversational business expressions | Pass | Unit 4 includes formal, neutral, and conversational register notes. |
| QA-035 | False absolute language rules from the old book have been corrected | Pass | Unit 4 corrects false absolutes about At first, then, Let us, That is all, and in charge of. |
| QA-036 | Role/responsibility vocabulary is accurate, including responsible for, manage, lead, take care of, and in charge of | Pass | Unit 4 defines responsible for, manage, lead, take care of, and in charge of. |
| QA-037 | Japanese-learner notes are useful, accurate, and not overgeneralized | Pass | Japanese-learner notes are practical and limited; no broad stereotyping found in current scan. |
| QA-038 | Pronunciation/intelligibility work covers thought groups, stress, prominence, pauses, chunking, pace, and recovery phrases | Pass | Units and appendix notes cover thought groups, stress, prominence, pauses, chunking, pace, and recovery guidance. |
| QA-039 | Preparation guidance supports learner-owned English and avoids sentence-by-sentence translation dependency | Pass | Unit 2 supports bilingual planning while discouraging sentence-by-sentence translation. |

## 4. AI Policy QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-040 | AI is mentioned only as critical literacy, checking, critique, ethics, confidentiality, copyright, and limitation awareness | Pass | AI appears as critique/checking/confidentiality/copyright/limitations content, not as a productivity pitch. |
| QA-041 | AI is not promoted as a replacement for English language development | Pass | AI is not promoted as a replacement for English development. |
| QA-042 | Learners are not instructed to outsource final language, message structure, or delivery preparation to AI | Pass | Learners are told not to use AI for final script or final visuals. |
| QA-043 | Any AI-output activity uses flawed material for critique, fact-checking, rewriting, or improvement | Pass | AI activities use flawed material for critique and rewriting awareness. |
| QA-044 | AI guidance includes human responsibility, company policy, confidentiality, source checking, and copyright/licensing caution | Pass | AI guidance includes responsibility, policy, confidentiality, checking, and copyright/licensing caution. |
| QA-045 | The final assessment requires learner-owned spoken performance and Q&A | Pass | Unit 12 requires learner-owned final presentation, Q&A, and reflection. |

## 5. Visuals, Documents, and Tool-Neutral Workflow QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-046 | PowerPoint is treated as one example tool, not the organizing concept | Pass | PowerPoint appears as an example/tool issue, not the organizing concept; Unit 12 even critiques PowerPoint dependency. |
| QA-047 | Tool mentions are practical and business-appropriate for Japanese business learners | Pass | Tool mentions are practical and limited to workplace material choices. |
| QA-048 | Tool-choice guidance covers audience, collaboration, data source, visual complexity, accessibility, export, and confidentiality | Pass | Unit 7 covers audience, collaboration/access, data source, visual complexity, accessibility, export, and confidentiality. |
| QA-049 | Format-choice guidance includes slides, PDF, document walkthroughs, dashboards, handouts, and screen sharing where relevant | Pass | Unit 7 covers slides, PDFs, documents, dashboards, worksheets, pre-reads, follow-up handouts, appendices/backup slides, and screen sharing. |
| QA-050 | Visual-design Units teach message-led visuals, hierarchy, alignment, contrast, whitespace, consistency, branding, and delivery environment | Pass | Unit 5 teaches message-led visuals, hierarchy, contrast, spacing/whitespace, consistency, accessibility, and delivery environment. |
| QA-051 | Old 7x7-style slide-text rules are replaced with better readability and hierarchy guidance | Pass | Unit 5 replaces 7x7-style thinking with one-message, hierarchy, brevity, and readability guidance. |
| QA-052 | Font guidance is current, screen-appropriate, and spells "sans serif" correctly | Pass | Style sheet and Unit 5 use current sans serif guidance; scan found no bad sans-serif wording in learner drafts. |
| QA-053 | Visual types include charts, tables, diagrams, timelines, photos, screenshots, process visuals, and unsuitable-use cases | Repair | Visual-type teaching exists, but final visual examples are missing/rejected so use cases cannot be fully validated. |
| QA-054 | Animation, transition, audio, and video guidance distinguishes purposeful use from decoration | Pass | Unit 9 and workflow guidance distinguish useful media/recording support from decoration. |
| QA-055 | Document-role guidance covers live slides, presenter notes, pre-reads, worksheets, follow-up handouts, appendices/backup slides, and PDF fallback | Pass | Unit 7 covers document roles including live slides, notes, pre-reads, worksheets, handouts, backup material, and PDF fallback. |

## 6. Delivery, Q&A, and Interaction QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-056 | In-person delivery covers voice, posture, eye contact, notes, movement, natural gesture, room setup, and cultural context | Pass | Unit 8 covers voice, posture, eye contact, notes, gesture, room setup, online, and async variations. |
| QA-057 | Pointer/cursor guidance removes outdated "infrared pointer" language | Pass | Scan found no outdated infrared pointer language in current learner drafts. |
| QA-058 | Pointer/cursor guidance covers safe laser use, cursor highlight, digital pointer/pen/highlighter tools, zooming, annotation, and avoiding pointing at people | Pass | Unit 8 now covers laser safety, cursor highlight, digital pen/highlighter, annotation, zoom, avoiding pointing at people, and avoiding constant cursor movement. |
| QA-059 | Online/hybrid delivery covers camera, microphone, lighting, screen sharing, presenter notes/view modes, chat/reactions, captions, timing, remote Q&A, and contingency planning | Pass | Unit 9 covers camera, microphone, lighting, screen sharing, notes, chat/reactions, captions, timing, remote Q&A, and contingency. |
| QA-060 | Async delivery includes recording, pacing, scripting, captions, and visual clarity where appropriate | Pass | Units 8 and 9 include recorded/async delivery, pacing, captions/transcripts, and visual clarity. |
| QA-061 | Q&A is compulsory in Standard and Long final assessment | Defer | Standard final assessment requires Q&A; Long is not drafted and is tracked in the Phase 6 defer log. |
| QA-062 | Peer feedback and formal assessment are clearly separate | Pass | Unit 11 and Unit 12 separate peer feedback from final assessment. |

## 7. Accessibility QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-063 | Accessibility is taught as ordinary presentation quality, not only a production concern | Pass | Accessibility is taught as ordinary visual/presentation quality in Units 5, 7, 9, and 12. |
| QA-064 | Learner materials cover readable text, contrast, color not as the only signal, chart clarity, alt-text awareness, cognitive load, captions, and inclusive delivery | Pass | Learner materials cover readable text, contrast, color not alone, chart clarity, alt-text awareness, cognitive load, captions/transcripts, and inclusive delivery. |
| QA-065 | Final rubric includes accessibility-related visual communication criteria | Pass | Unit 12 rubric/checklist includes accessibility and visual/material readability. |
| QA-066 | Images and diagrams have alt text or a documented reason if decorative | Repair | Asset alt text cannot pass because current final image assets are rejected/deleted and broken links remain. |
| QA-067 | Charts and visuals do not rely on color alone to communicate meaning | Repair | Curriculum teaches this, but final charts/visuals are missing/rejected so production compliance cannot pass. |
| QA-068 | Exported PDF receives a minimum accessibility/tool check where available | Defer | No final exported PDF exists for the textbook. |
| QA-069 | Accessibility limitations that tooling cannot verify are documented for manual review | Defer | Manual accessibility limitations cannot be documented until final exports/assets exist. |
| QA-070 | Text/background contrast is checked against WCAG 2.2 AA target of at least 4.5:1 for normal text and 3:1 for large text where practical | Defer | No final designed pages/assets exist for contrast checking. |
| QA-071 | Every chart has a takeaway title or clear chart title, readable labels, and does not depend on color alone | Repair | Chart-title rule is taught, but referenced chart assets are deleted and model visuals are not approved. |
| QA-072 | Recorded or async materials have caption, transcript, or transcript-awareness guidance | Pass | Units 8 and 9 include captions/transcript awareness for recorded/async materials. |
| QA-073 | Word accessibility check and PDF accessibility check are run where available, with manual limitations documented | Defer | No final DOCX/PDF exists for Word/PDF accessibility checks. |

## 8. Asset QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-074 | Every final asset appears in the asset or image register | Repair | Image register exists, but current final asset set is unsettled; one v2 test deck is not registered as final and deleted PNG links remain. |
| QA-075 | Every asset has file path, source, license status, generated/original status, alt text, decorative flag, caption where needed, unit/tier use, replacement rationale, visual-restriction check, and approval owner | Repair | Register contains many fields, but rejected/deleted assets and draft decks mean final asset metadata is incomplete/not final. |
| QA-076 | Generated images or mockups are marked as generated/original where applicable | Pass | Generated image/mockup entries are marked as generated/original or rejected in the register. |
| QA-077 | Stock or third-party assets are not used unless licensing is clear | Pass | No stock or third-party assets are currently used in the accepted final set. |
| QA-078 | Old dated clip art and repeated male presenter imagery are removed or intentionally replaced | Pass | Old generated PNG/clip-art-like assets were removed from active planned/model-slide folders. |
| QA-079 | Sample A/B or equivalent readability examples are editable and legible | Repair | Sample A/B readability asset was rejected/deleted and is not currently replaced. |
| QA-080 | Model visuals demonstrate the visual principles being taught | Repair | Model visuals are draft/rejected and do not yet demonstrate taught visual principles. |
| QA-081 | Generated images are visually inspected for text accuracy, element count, label placement, stray readable text, logos, watermarks, flags, seals, crests, and representation issues | Repair | Generated images were inspected and rejected; replacement assets still need inspection. |
| QA-082 | Transparent-background assets are checked for unwanted background artifacts or hidden RGB ghosting where applicable | N/A | No transparent-background final assets are currently in use. |
| QA-083 | Existing Presentation Skills assets are not reused for Plan 3 unless their prompts/register entries are revised or the asset is visually reapproved against Plan 3 restrictions | Pass | No existing Presentation Skills assets are currently reused as approved Plan 3 finals. |
| QA-084 | Any image defect has a regenerate-versus-edit decision; precise text/count/layout repairs should prefer editable/PIL overlay where feasible | Pass | Image defects have an explicit decision: rejected assets removed; future precise text/layout should use editable/native methods. |

## 9. Factual, Source, Privacy, and Security QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-085 | Real business data, tool references, accessibility guidance, and 2026 workplace claims are checked against official or stable sources | Pass | Source verification is recorded in `revision/records/plan3-phase6-source-verification.md`; current claims are supported, general cautions, or user-approved pedagogical/editorial policy choices. |
| QA-086 | Fictional teaching data is clearly labeled as fictional | Pass | Fictional data labels are present in units and appendices. |
| QA-087 | Case examples do not imply unsupported real-company claims | Pass | Repaired model examples use clearly fictional organizations, teams, desks, forms, suppliers, and data; no real-company operational claims are introduced. |
| QA-088 | Tool-specific guidance avoids unstable step-by-step UI instructions unless verified | Pass | Tool-specific step-by-step UI instructions are avoided. |
| QA-089 | Confidentiality and company security policy are mentioned in AI, tool-choice, export, and sharing guidance | Pass | Confidentiality and company policy appear in AI, tool-choice, export, and sharing guidance. |
| QA-090 | Copyright/licensing caution appears where learners use images, templates, AI outputs, or external data | Pass | Copyright/licensing caution appears in AI/tool/image/template contexts. |
| QA-091 | Dashboard mockups, screenshots, filenames, and metadata contain no real client, company, person, account, ticket, or trade identifiers | Repair | Mockup image files were deleted/rejected; current draft PPTX metadata/screenshots not fully checked. |
| QA-092 | No real screenshots are used unless they are current, permission-cleared, and necessary | Pass | No real screenshots are used in current accepted materials. |
| QA-093 | All dashboard/mockup data is fictional or sanitized and labeled appropriately | Repair | Dashboard/mockup examples are labeled fictional/sanitized, but deleted mockups mean final data labeling cannot pass. |
| QA-094 | Final DOCX/PDF metadata contains no legacy title, client-confidential residue, authoring comments, or unintended hidden data | Defer | No final DOCX/PDF export exists for metadata inspection. |

## 10. Assessment QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-095 | Final rubric includes message clarity, audience fit, structure, evidence, visual effectiveness, spoken English, delivery, Q&A, timing, and professionalism | Pass | Unit 12 final rubric/evidence table includes required categories including message, audience, structure, evidence, visuals, English, delivery, Q&A, timing, professionalism, accessibility, and reflection. |
| QA-096 | Rubric separates language accuracy/intelligibility from presentation effectiveness | Pass | Teacher Notes says to separate English control from presentation effectiveness. |
| QA-097 | B1/B2 descriptors are used where language is assessed | Pass | Unit 12 now includes a learner-facing B1/B2 language-level check, and Teacher Notes includes assessor guidance for B1/B2 performance. |
| QA-098 | Q&A performance is assessed, not optional | Pass | Q&A is required in Unit 12. |
| QA-099 | Self-review and peer feedback are included before final submission where appropriate | Pass | Unit 11 peer feedback and Unit 12 self-review are included before/with final submission. |
| QA-100 | Assessment evidence is clear: final deck/visuals, speaking performance, Q&A, reflection, and/or teacher notes | Pass | Unit 12 defines final presentation, materials, Q&A, and self-review evidence. |

## 11. Production and Export QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-101 | Title, front matter, back matter, revision date, credits, and copyright/production lines are current | Defer | Front/back matter, final title, credits, revision date, and production lines are not yet finalized. |
| QA-102 | DOCX/PDF metadata matches the final title and no longer says "Making Speeches" | Defer | No final DOCX/PDF metadata exists to inspect. |
| QA-103 | Old PowerPoint-prescriptive headings and metadata are removed unless referring to PowerPoint as an example | Pass | Current learner source drafts are tool-neutral; PowerPoint appears only as an example or in an intentional flawed quiz sentence. Final DOCX/PDF metadata remains separately deferred under QA-102. |
| QA-104 | Internal unit, unit, page, figure, and activity references are correct | Pass | Deleted-image embeds were removed from current learner-facing unit and appendix drafts; remaining model/deck references point to existing draft PPTX files or named appendix model sets. |
| QA-105 | Known typo list is cleared: deliver your message, sans serif, after a while, at least 16, Ventura/Venture, spacing and punctuation | Pass | Targeted typo/stale-term scan passed for current learner drafts and control files; remaining Ventura/Making Speeches hits are intentional control/defer references. |
| QA-106 | Capitalization, bullets, indentation, punctuation, table style, and heading levels are consistent | Pass | Final source-level heading/style scan passed after manuscript repairs; remaining layout-level checks belong to final DOCX/PDF production. |
| QA-107 | No accidental blank or near-blank pages remain | Defer | No final laid-out DOCX/PDF pages exist. |
| QA-108 | Text-dense pages are reflowed into workbook-style chunks where practical | Pass | Current markdown is mostly workbook-style chunks, tables, checklists, examples, and tasks. |
| QA-109 | Final DOCX exports open correctly | Defer | No final DOCX export exists. |
| QA-110 | Final PDF exports open correctly and visual layout is checked page by page or with contact sheets | Defer | No final PDF export exists. |

## 11a. DOCX Style Creation QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-123 | `presentations_style.docx` is generated from a reusable YAML style source and documented style set rather than built only by manual Word formatting | Defer | YAML source and style-set notes exist, but the final reference DOCX has not yet been approved for production. |
| QA-124 | A formal component library defines how styles combine into repeatable textbook elements such as running headers, unit openings, practice tasks, language boxes, model boxes, cross-reference lines, contents/course-map blocks, and review/checklist areas | Defer | Component-library requirements have been added to Plan 3; final component specimens still need to be created and checked. |
| QA-125 | Practice-task layout includes a consistent activity number plus instruction pairing system with task number, task title, short instruction text, and learner response space | Defer | The requirement is now tracked; final DOCX component styling and postprocess behavior remain to be built. |
| QA-126 | Cross-reference lines for appendix/model references have a defined style, placement rule, visible marker/rule treatment, and consistent learner-facing wording | Defer | `PS Cross Reference` exists, but final cross-reference component behavior has not been validated in DOCX. |
| QA-127 | Contents, course-map, and unit-overview styling are defined separately from the automatic TOC styles | Defer | TOC styles exist; course-map and unit-overview component specs still need final specimens. |
| QA-128 | Section-family accent logic distinguishes core skill, language, visual/tool workflow, delivery, model/appendix, and assessment/review material without creating an inconsistent palette | Defer | Accent roles are partly defined; final component specimens and theme-token validation remain. |
| QA-129 | Image placement specifications cover full-width figures, half-width figures, screenshots/mockups, diagrams, cover images, and appendix slide images, including caption and register requirements | Defer | Image placement rules are noted in the style set; final image/register integration has not been completed. |
| QA-130 | Standard rule weights are defined for section underlines, callout rules, table borders, table grids, learner-writing lines, and cross-reference rules | Defer | Rule-weight requirements are now tracked; final DOCX style values and rendered-page checks remain. |
| QA-131 | Fill-in and learner-writing line treatment is defined and checked for printed workbook tasks and planning tables | Defer | Planning-table styles exist, but final writable-line treatment has not been validated in rendered output. |
| QA-132 | Source/provenance and shared theme-token discipline is applied across DOCX, slide decks, and any Canva/template work, including source, license, generation prompt/tool where applicable, edit history, final path, and approval state | Defer | Asset registers and theme colors exist, but final cross-tool token/provenance QA remains incomplete. |

## 12. Cross-Series Consistency QA

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-111 | Essentials, Standard, and Long use consistent terminology and case names | Defer | Essentials and Long are not drafted, so cross-tier consistency cannot be checked. |
| QA-112 | Essentials does not omit any minimum viable 2026 requirement that is essential to credibility | Defer | Essentials is not drafted. |
| QA-113 | Long extensions deepen the course rather than changing the core pedagogy | Defer | Long is not drafted. |
| QA-114 | Shared assets are reused consistently or intentionally varied | Repair | Shared asset strategy is unsettled because assets were rejected/deleted. |
| QA-115 | Rubrics are tier-appropriate but aligned across the series | Defer | Tier rubrics cannot be checked because Essentials and Long are not drafted. |
| QA-116 | Teacher notes and answer keys do not contradict learner-facing pages | Pass | Current Teacher Notes align with learner-facing pages on role-agnostic textbook and client-specific classroom adaptation. |

## 13. External Review Gate

| ID | Check | Status | Notes |
| --- | --- | --- | --- |
| QA-117 | Claude.ai review feedback is saved in the project folder | Pass | Claude.ai feedback files are saved under the project feedback folders. |
| QA-118 | ChatGPT review feedback is saved in the project folder | Pass | ChatGPT feedback files are saved under the project feedback folders. |
| QA-119 | Every significant external issue is classified by type: scope, pedagogy, factual accuracy, accessibility, assessment, production, or style | Pass | `plan3-phase6-issue-classification-log.md` now classifies significant current issues by source, type, affected QA IDs, status, owner, disposition, and traceability update. |
| QA-120 | Significant issues are either repaired or deferred with reason and impact | Repair | Non-visual manuscript/source/proof issues have been repaired or deferred. QA-120 remains Repair because visual/asset issues remain open in the paused visual/deck-production workstream. |
| QA-121 | `plan3-traceability.md` is updated if review feedback changes requirement coverage | Pass | `plan3-traceability.md` now records current Phase 6 findings, including model specificity, terminology, options-model, tier, export, and paused visual/asset issues. |
| QA-122 | Final release notes mention any known limitations or deferred work | Defer | Final release notes do not exist yet. |

## Final Release Decision

Do not treat Phase 6 as complete until:

1. All required QA rows are Pass or N/A.
2. All Repair rows are fixed and rechecked.
3. All Defer rows have a reason, impact statement, and future action.
4. Final exports have been opened and visually checked.
5. External review issues have been classified and resolved or deferred.
6. DOCX style creation rows `QA-123` through `QA-132` have been completed, repaired, or explicitly deferred before final DOCX/PDF release.
