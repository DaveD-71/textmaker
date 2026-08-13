# Plan 3 Traceability Matrix

Prepared: 2026-08-12

Purpose: map every item in `Speaking with PowerPoint - 2026 Consolidated Revision Task List.md` to the Plan 3 rebuild before rewriting units or manuscripts. This matrix covers Units, deliverables, QA checks, and deferred or reframed items.

## Baseline and Rollback Note

The original *Speaking with PowerPoint* source has already been exported and committed.

- Baseline export folder: `books/Speaking with PowerPoint/out`
- Source export contents: `reference.docx`, 14 chapter `.docx` files, 14 chapter `.md` files, and extracted media assets
- Export baseline commit: `34235c5` - `added new ref.docx files for each teactbook`
- Plan 3 baseline commit: `f8127e9` - `'Speaking with Powerpoint' Plan3 added`

Commit messages above are recorded verbatim for rollback lookup.

Rollback rule: before changing unit JSON, manuscripts, or generated assets, preserve the current committed state. If a rewrite path fails, restore from the committed source export in `out` and the Plan 3 baseline commit rather than reconstructing from memory.

## Scope Translation

The consolidated task list was written for a two-day modernization sprint. Plan 3 supersedes that sprint by authorizing a fuller three-tier rebuild:

- Essentials: 8-unit compressed course
- Standard: 12-unit master course
- Long: 15-unit expanded course

The old priorities remain source requirements, but the acceptance target is now the Plan 3 series architecture rather than a patched 39-page PDF.

## unit Spine and Cumulative Deliverables

| Standard Unit | Plan 3 Focus | Cumulative Learner Deliverable |
|---|---|---|
| 1 | Audience, purpose, business context | Presentation brief |
| 2 | Message, objective, relevance | Core message and opening |
| 3 | Structure and flow | Full presentation outline |
| 4 | Business English for signposting | Preview, transitions, references |
| 5 | Clear visual communication | Accessible slide or visual draft |
| 6 | Data, charts, and evidence | One chart explanation |
| 7 | Tool-neutral slide/document workflow | Visual pack plus notes |
| 8 | Delivery: voice, posture, movement, notes | Rehearsed 3-minute segment |
| 9 | Online, hybrid, and async delivery | Adapted online or recorded version |
| 10 | Q&A, challenge handling, and interaction | Q&A response bank |
| 11 | Final rehearsal and peer feedback | Revised full presentation |
| 12 | Final presentation, textbook wrap-up, and reflection | Delivered presentation plus wrap-up quiz and self-review |

## Full Task Traceability

| ID | Plan 3 Placement | Deliverable | QA Check | Disposition |
|---|---|---|---|---|
| P0-01 | Units 2, 6, 7; model case bank | Three recurring model cases: process improvement, product/service launch, project results briefing | Ventura is not the dominant spine unless deliberately reused; no outdated 2013/2014 framing remains | Reframed |
| P0-02 | Scope note; tier strategy | Three-tier rebuild plan with Essentials, Standard, Long | Final outline is not constrained to the old 39-page/two-day update model | Superseded by Plan 3 |
| P0-03 | Unit 1; front matter | Target learner statement and business-use scenarios | Audience is adult B1-B2 business ESL learners in international, in-person, online, or hybrid contexts | Required |
| P0-04 | Title/front matter/metadata; Unit 7 terminology | Tool-neutral title and terminology | PowerPoint appears only as an example tool, not the course concept | Required |
| P1-01 | All Units; style sheet | Terminology rewrite from speech frame to business presentation frame | Headings, instructions, models, and rubrics use presentation/briefing/proposal/update language appropriately | Required |
| P1-02 | Units 1, 2, 12 | Audience-outcome planning box | Learners answer what the audience should know, decide, or do; this is referenced again in final reflection | Required |
| P1-03 | Units 2, 3 | Flexible business structure toolkit | Includes opening/development/close plus problem-solution, situation-analysis-recommendation, options-recommendation, project update, and data story | Required |
| P1-04 | Units 2, 3; planning templates | Presentation planning map | No template implies every presentation needs exactly three points; audience, outcome, evidence, and action are included; Unit 3 planning map uses Introduction, Body, and Conclusion with summary before action/close | Required |
| P1-05 | All Units | Unit-level learner outcomes | Each unit has 1-3 measurable "can do" outcomes aligned to the deliverable | Required |
| P1-06 | Units 10-12; teacher notes | Final presentation rubric | Rubric covers message, audience, structure, evidence, visuals, English, delivery, interaction/Q&A, timing, professionalism | Required |
| P1-07 | All Units | Noticing, editing, planning, speaking, and peer-feedback tasks | No major teaching point is explanation-only; each has a learner action | Required |
| P1-08 | Units 6, 7; case bank; asset register | Modernized or replaced business case data and visuals | Fictional data is labeled; real/current claims are sourced; old Ventura assumptions are removed or retired | Required |
| P1-09 | Units 2, 6, 12; model scripts | Decision-oriented model presentations | At least one model recommends, reports, requests approval, or supports a decision rather than only describing a product | Required |
| P1-10 | Unit 6; final rubric | Data storytelling section and chart explanation task | Learners choose chart type, simplify, title with takeaway, cite/source, and explain trends aloud | Required |
| P1-11 | Units 2, 5, 7; teacher notes | AI critical-literacy checklist and optional flawed-output critique | AI is framed as checking, critique, ethics, confidentiality, copyright, and learner-owned rewriting; it is not promoted as skill replacement | Reframed |
| P1-12 | Units 5, 7, 12; final rubric | Accessibility checklist and learner task | Contrast, readable text, color dependence, alt-text awareness, captions, and inclusive delivery appear in curriculum and assessment | Required |
| P1-13 | Unit 5 | Modern visual-design principles unit | Teaches message-led visuals, hierarchy, alignment, contrast, whitespace, consistency, brand, accessibility, and environment | Required |
| P1-14 | Unit 7 | Format-choice checklist | Learners choose slides, PDF, document, dashboard, handout, or other format by purpose/context; no single format is prescribed | Required |
| P1-15 | Unit 7; style sheet | Tool-choice and template guidance | Mentions tools only as examples; checks brand, accessibility, data integrity, confidentiality, export, and collaboration needs | Required |
| P1-16 | Unit 5; style sheet | Updated font guidance | "Sans serif" is spelled correctly; serif body text is not recommended for screen slides; Aptos is example only | Required |
| P1-17 | Unit 5 | Replacement for Rule of 7 | Uses one-message-per-slide, hierarchy, brevity, and real-viewing-environment readability instead of 7x7 | Required |
| P1-18 | Units 5, 6, 7; asset plan | Visual-types section | Covers charts, tables, diagrams, timelines, photos, screenshots, process visuals, and unsuitable-use cases | Required |
| P1-19 | Units 5-7; asset register | Rebuilt model visuals | Old olive/tan and dated screenshots are replaced or retired; new visuals demonstrate taught principles and have source/alt text | Required |
| P1-20 | Unit 7 or 9 | Purposeful movement/media note | Distinguishes useful builds, transitions, audio, and video from decorative effects | Required |
| P1-21 | Unit 9 | Online/hybrid delivery checklist and practice task | Covers camera, mic, lighting, screen share, presenter notes, chat/reactions, captions, timing, Q&A, contingency | Required |
| P1-22 | Unit 8 | Modern in-person delivery section | Covers room size, hybrid audiences, cultural context, movement, natural body language, voice, notes, and eye contact | Required |
| P1-23 | Units 8, 9 | Pointer/cursor guidance | Removes "infrared pointer"; covers laser safety, cursor highlight, annotation, zooming, and not pointing at people | Required |
| P1-24 | Units 7, 9; preparation checklist | Backup/export/security checklist | Covers approved cloud, offline copy, PDF fallback, export tests, fonts/media/links, venue/platform test, company security | Required |
| P1-25 | Unit 7 | Document role decision task | Learners choose pre-read, live slides, worksheet, follow-up handout, appendix/backup slides, or detailed handout by purpose/timing | Required |
| P2-01 | Unit 4; teacher notes | Updated phrase bank with register notes | Expressions include current neutral, formal, and conversational business options | Required |
| P2-02 | Units 3, 4, 10; style sheet | Contextual language-warning notes | No false absolutes about "Let's," "That is all," "At first," or "then" remain | Required |
| P2-03 | Unit 4 | Role/responsibility vocabulary note | Explains responsible for, manage, lead, take care of, and in charge of with business examples | Required |
| P2-04 | Unit 2 or 8; teacher notes | Bilingual planning guidance | Allows efficient idea planning while discouraging sentence-by-sentence translation into unnatural English | Required |
| P2-05 | Units 4, 8 | Pronunciation/intelligibility practice | Teaches thought groups, prominence, pauses, stress, pace, chunking, and recovery phrases; removes unclear vowel-lengthening advice | Required |
| P2-06 | Unit 8 | Notes and memorization guidance | Distinguishes prepared openings/transitions/close from word-for-word memorization | Required |
| P2-07 | Unit 10 | Expanded Q&A strategy and practice | Includes clarifying, answering directly, structuring, checking satisfaction, deferring, disagreement, and follow-up | Required |
| P2-08 | Units 4, 8; teacher notes | Japan-specific learner support | Keeps useful pronunciation/register cautions while modernizing examples and avoiding inaccurate advice | Required |
| P2-09 | Asset plan; final production pass | Refreshed workbook visual system | Pages use clean hierarchy, spacing, diagrams/icons, and modern workbook design | Required |
| P2-10 | Asset plan; image register | Replacement for repeated male presenter imagery | Old repeated silhouette is removed or no longer dominant; imagery is neutral or inclusive | Required |
| P2-11 | Unit 5 or 7; asset register | Recreated Sample A/B | Examples are editable, legible, and demonstrate readability clearly | Required |
| P2-12 | Layout QA | Page-flow decision for old blank/low-value pages | No accidental blank or near-blank pages remain unless intentionally required for print layout | Required |
| P2-13 | All Units; layout QA | Workbook-style reflow | Dense explanation is broken into chunks, tables, checklists, examples, and learner tasks | Required |
| P2-14 | Front/back matter; metadata QA | Updated title, date, credits, copyright/production lines, document properties | PDF/DOCX metadata matches final title and no longer says "Making Speeches" or old revision date | Required |
| P2-15 | Proofreading QA | Known typo correction list | Confirms "deliver your message," "sans serif," "after a while," spacing, Ventura/Venture, and punctuation are fixed | Required |
| P2-16 | Cross-reference QA | Corrected unit/page references | All unit/page references match final Essentials, Standard, and Long structures | Required |
| P2-17 | Style sheet; all Units | Terminology list | Terms are consistent: presentation, visuals, deck/slides, handout, follow-up handout, agenda/overview, presenter notes, screen share, dashboard, document walkthrough | Required |
| P2-18 | Final editorial QA | Formatting/style pass | Capitalization, bullets, indentation, punctuation, spacing, headings, and tables follow one style | Required |
| P3-01 | Standard Unit spine | 12-unit master course | The future-edition idea is promoted into Plan 3 Standard, then adapted to Essentials and Long | Promoted |
| P3-02 | Unit 1; Long expansion | Audience adaptation task | Learners adapt message for at least one audience/time-limit variation; Long expands stakeholder variation | Required |
| P3-03 | Units 5 or 7; teacher notes | Optional flawed AI-output critique activity | Activity is optional and framed as critique/rewrite/fact-checking, not AI productivity promotion | Reframed optional |
| P3-04 | Unit 9; Long expansion | Async delivery component | Standard includes a short recorded/async adaptation; Long expands it into deeper practice | Required |

## Plan 3 Specific Requirements Not Separately Numbered in the Consolidated List

| Requirement | Placement | Deliverable | QA Check |
|---|---|---|---|
| Three recurring business cases | Model case bank; Units 1-12 | Process improvement, product/service launch, and project results briefing cases | Each model maps to Units, language points, visual points, delivery behaviors, and rubric criteria |
| Audience-variant rule | Main Units, appendix models, QA | Main unit body stays role-agnostic between business-client and government-agency contexts | Role-specific content appears in models, appendices, teacher notes, or optional variants rather than changing the core sequence |
| Business-client model focus | Appendix models and examples | Banking/leasing or general trading-company operations, reporting, workflow, client service, service quality, procurement, supplier coordination, shipment reporting, or control escalation examples | Fictional or sanitized shipment/order/procurement/supplier-status examples are allowed; no investment advice, securities-market prediction, real identifying customer/account/order/shipment/transaction data, legal or regulatory advice, real firm logos, securities exchange names, or stock ticker symbols |
| Government-agency model focus | Appendix models and examples | Administrative task, service delivery, reporting, coordination, or process improvement examples | No superficial relabeling of business examples; no political advocacy, legislation, budget campaigning, flags, seals, emblems, or crests unless approved |
| Appendix model parity | Appendix model sets and QA | Paired business-client and government-agency models for each case family | Each pair teaches the same underlying skill with comparable depth and quality |
| Three-tier series | Tier strategy and manuscripts | Essentials 8, Standard 12, Long 15 | Essentials compresses, Standard is source of truth, Long expands without contradiction |
| Four-role production workflow | Project workflow notes | Content Architect, Language Editor, Business Presentation Specialist, Asset and QA Specialist role briefs | Every task has an owner during implementation |
| Style sheet before drafting | QA and Acceptance | Style sheet covering title, level, terminology, AI policy, accessibility, citations, file naming, tone, case names | No unit rewrite begins before the style sheet exists |
| Asset creation policy | Asset register | Source, license status, alt text, captions, and replacement rationale for every asset | No unexplained stock/AI/extracted asset enters the final books |
| External review gate | QA workflow | Claude.ai/ChatGPT feedback log after implementation | Significant issues are classified, traced, and repaired before finalization |

## Tier Mapping

| Requirement Group | Essentials | Standard | Long |
|---|---|---|---|
| Audience, purpose, message | Keep | Keep as full spine | Expand with stakeholder adaptation |
| Structure and signposting | Keep | Keep | Add executive/deck structures |
| Visual principles and accessibility | Keep core checklist | Keep full unit sequence | Expand with advanced document and data formats |
| Data and evidence | Basic chart explanation | Full chart/evidence unit | Add data storytelling and decision-deck depth |
| Tool-neutral workflow | Condense | Full unit | Expand with collaboration, templates, and governance |
| Delivery and Q&A | Keep essentials | Full live/online/Q&A sequence | Add facilitation and difficult stakeholder scenarios |
| Async delivery | Mention briefly if space allows | Short Unit 9 component | Full extension unit |
| Final assessment | One final presentation | Final presentation plus reflection | Two assessed presentation cycles |

## Deferred, Superseded, Reframed, and Promoted Items

| Item | Decision |
|---|---|
| P0-01 Ventura strategy | Reframed as case-bank decision; Ventura is not the default spine |
| P0-02 two-day update versus shorter rebuild | Superseded by Plan 3 three-tier rebuild |
| P1-11 AI-assisted presentation guidance | Reframed as cautious AI literacy, checking, ethics, confidentiality, and learner-owned rewriting |
| P3-01 full 10-12 unit 2026 course | Promoted into the Standard 12-unit master course |
| P3-03 AI-generated-slide critique | Reframed as optional critique only |

## Phase 6 Execution Tracking

Updated: 2026-08-13

Purpose: record implementation status, evidence, owner, repair or defer action, and recheck result for every consolidated task ID and Plan 3-specific requirement. This section is the Phase 6 execution layer for the planning matrix above.

Status meanings: `Pass` = implemented and verified for the current Standard draft; `Repair` = must be fixed before current Standard release; `Defer` = intentionally postponed with reason in `plan3-phase6-defer-log.md`; `N/A` = not applicable to the current tier/deliverable.

| ID | Phase 6 Status | Evidence/File | Owner | Repair/Defer Action | Recheck Result |
|---|---|---|---|---|---|
| P0-01 | Repair | Standard units and appendix model files; Phase 6 agent review round 1 | Content Architect, Business/Government Presentation Specialist, Language Editor | Repair model specificity and role/context realism; keep visual/asset replacement separate | Open |
| P0-02 | Pass | `revision/control/plan3.md`; Standard 12-unit draft set | Content Architect | None | Verified in Phase 6 checklist |
| P0-03 | Pass | Unit 1; style sheet; teacher notes | Content Architect | None | Verified in Phase 6 checklist |
| P0-04 | Pass | Units 7 and 12; style sheet; Phase 6 checklist | Content Architect, Production QA | Current learner source is tool-neutral; final metadata/front matter checks remain separately deferred under export QA | Verified for current source |
| P1-01 | Pass | Standard unit drafts; Phase 6 checklist; final Language Editor recheck | Language Editor | Final terminology/proof pass completed for current source | Verified |
| P1-02 | Pass | Units 1, 2, and 12 | Content Architect | None | Verified in Phase 6 checklist |
| P1-03 | Pass | Units 2 and 3; defer log | Content Architect | Unit 3 now includes an options-based mini example; full appendix model remains tracked separately in defer log | Verified for Standard toolkit |
| P1-04 | Pass | Unit 3 planning map | Content Architect | None | Verified after Introduction/Body/Conclusion planning map revision |
| P1-05 | Pass | Units 1-12 | Content Architect | None | Verified in Phase 6 checklist |
| P1-06 | Pass | Unit 12; Teacher Notes | Language Editor | B1/B2 language assessment descriptors added | Verified |
| P1-07 | Pass | Units 1-12; Unit 3; Phase 6 manuscript repair | Content Architect, Language Editor | Unit 3 example/evidence learner support added | Verified |
| P1-08 | Repair | Units 6 and 7; appendix models; image register | Content Architect, Business/Government Presentation Specialist | Add concrete fictional data/details to examples; visual assets deferred separately | Open |
| P1-09 | Pass | Appendix model scripts; Phase 6 manuscript repair | Business/Government Presentation Specialist | Decision-oriented models now include concrete fictional details and clearer examples | Verified |
| P1-10 | Pass | Unit 6; Project Results Briefing Models | Content Architect, Language Editor | Unit 6 useful terms added; results models strengthened with volume-adjusted and specific expansion examples | Verified |
| P1-11 | Pass | Units 2, 5, 7, and 12; style sheet | Content Architect | None | Verified in Phase 6 checklist |
| P1-12 | Repair | Units 5, 7, 9, and 12; Phase 6 checklist | Content Architect, Production QA | Curriculum passes; final asset/export accessibility checks deferred or open | Open |
| P1-13 | Pass | Unit 5 | Content Architect | None | Verified in Phase 6 checklist |
| P1-14 | Pass | Unit 7 | Content Architect | None | Verified in Phase 6 checklist |
| P1-15 | Pass | Unit 7; style sheet | Content Architect | None | Verified in Phase 6 checklist |
| P1-16 | Pass | Unit 5; style sheet | Language Editor | None | Verified in Phase 6 checklist |
| P1-17 | Pass | Unit 5 | Content Architect | None | Verified in Phase 6 checklist |
| P1-18 | Repair | Units 5-7; slide-design checklist; image register | Asset and QA Specialist | Visual examples/assets are paused for separate workstream | Deferred/paused |
| P1-19 | Repair | Image register; Phase 5 rejection notes; Phase 6 checklist | Asset and QA Specialist | Visual/asset replacement workstream paused for separate treatment | Deferred/paused |
| P1-20 | Pass | Unit 9; tool-neutral workflow content | Content Architect | None | Verified in Phase 6 checklist |
| P1-21 | Pass | Unit 9 | Content Architect | None | Verified in Phase 6 checklist |
| P1-22 | Pass | Unit 8 | Content Architect | None | Verified in Phase 6 checklist |
| P1-23 | Pass | Unit 8 | Content Architect, Language Editor | Expanded pointer/cursor guidance covers laser safety, digital pen/highlighter, annotation, zoom, and cursor movement | Verified |
| P1-24 | Pass | Unit 7; Unit 9; preparation checklists | Content Architect | None | Verified in Phase 6 checklist |
| P1-25 | Pass | Unit 7 | Content Architect | None | Verified in Phase 6 checklist |
| P2-01 | Pass | Unit 4; Teacher Notes | Language Editor | None | Verified in Phase 6 checklist |
| P2-02 | Pass | Units 3, 4, and 10; style sheet | Language Editor | None | Verified in Phase 6 checklist |
| P2-03 | Pass | Unit 4 | Language Editor | None | Verified in Phase 6 checklist |
| P2-04 | Pass | Unit 2; Teacher Notes | Language Editor | None | Verified in Phase 6 checklist |
| P2-05 | Pass | Units 4 and 8 | Language Editor | None | Verified in Phase 6 checklist |
| P2-06 | Pass | Unit 8 | Language Editor | None | Verified in Phase 6 checklist |
| P2-07 | Pass | Unit 10 | Content Architect, Language Editor | None | Verified in Phase 6 checklist |
| P2-08 | Pass | Units 4 and 8; Teacher Notes | Language Editor | None | Verified in Phase 6 checklist |
| P2-09 | Repair | Standard drafts; style sheet; visual asset notes | Production QA | Workbook chunking is acceptable; final designed pages not yet exported | Open until layout/export |
| P2-10 | Pass | Image register; asset cleanup notes | Asset and QA Specialist | None for current text round | Verified in Phase 6 checklist |
| P2-11 | Repair | Image register; Phase 6 checklist | Asset and QA Specialist | Sample A/B replacement paused with visual/asset workstream | Deferred/paused |
| P2-12 | Defer | Phase 6 defer log | Production QA | Check after final DOCX/PDF layout | Deferred |
| P2-13 | Pass | Standard draft files | Content Architect | None | Verified in Phase 6 checklist |
| P2-14 | Defer | Phase 6 defer log | Production QA | Check after final title/front matter/export exist | Deferred |
| P2-15 | Pass | Standard drafts; appendices; Phase 6 checklist | Language Editor | Targeted typo/stale-term scan passed for current source | Verified |
| P2-16 | Pass | Standard drafts; appendix references; Phase 6 checklist | Content Architect, Production QA | Deleted-image embeds removed; current learner-facing references point to existing decks or named appendix model sets | Verified for current Standard source |
| P2-17 | Pass | Style sheet; Standard drafts; appendices | Language Editor | Final terminology scan after model specificity repairs passed for current source | Verified |
| P2-18 | Pass | Standard drafts; appendices; Teacher Notes | Language Editor, Production QA | Source-level heading/table/punctuation pass completed; layout checks remain in export QA | Verified |
| P3-01 | Defer | Phase 6 defer log | Content Architect | Essentials and Long are not drafted in current round | Deferred |
| P3-02 | Pass | Unit 1; curriculum spec | Content Architect | None | Verified in Phase 6 checklist |
| P3-03 | Pass | Units 2, 5, and 7; style sheet | Content Architect | None | Verified in Phase 6 checklist |
| P3-04 | Defer | Unit 9; tier strategy; defer log | Content Architect | Standard async content passes; Long expansion is deferred with Long manuscript | Deferred by tier |

## Phase 6 Plan 3-Specific Requirement Tracking

| Requirement | Phase 6 Status | Evidence/File | Owner | Repair/Defer Action | Recheck Result |
|---|---|---|---|---|---|
| Three recurring business cases | Pass | Appendix model sets; Phase 6 manuscript repair | Business/Government Presentation Specialist | All six model scripts now include more concrete fictional detail | Verified |
| Audience-variant rule | Pass | Standard units; appendices; Teacher Notes | Content Architect | None | Verified in Phase 6 checklist |
| Business-client model focus | Pass | Appendix model sets; Phase 6 manuscript repair | Business/Government Presentation Specialist | Business-client models now focus on general trading-company/client-service operations and avoid securities-trading assumptions | Verified |
| Government-agency model focus | Pass | Appendix model sets; Phase 6 manuscript repair | Business/Government Presentation Specialist | Government-agency models now include administrative/service-process detail without policy advocacy or sensitive operational detail | Verified |
| Appendix model parity | Pass | Appendix model sets; Phase 6 manuscript repair | Business/Government Presentation Specialist, Language Editor | Paired business/government models demonstrate comparable skills with different role-appropriate contexts | Verified pending final Language Editor recheck |
| Three-tier series | Defer | Phase 6 defer log | Content Architect | Essentials and Long are outside current Standard repair round | Deferred |
| Four-role production workflow | Pass | Plan 3; recorded agent reviews | Content Architect | None | Sequential Business Specialist then Language Editor rule recorded |
| Style sheet before drafting | Pass | `plan3-style-sheet.md`; Phase 4 records | Content Architect | None | Verified |
| Asset creation policy | Repair | Image register; Phase 5 rejection notes | Asset and QA Specialist | Visual/asset workstream paused for separate treatment | Deferred/paused |
| External review gate | Pass | Claude.ai and ChatGPT feedback folders; Phase 6 issue classification log | Content Architect | Continue updating issue log as new external reviews arrive | Verified for current feedback set |

## Next Gate

Before final release, every row in the Phase 6 execution tracking sections above must be `Pass`, `N/A`, or linked to a defer-log entry with reason, impact, future action, and recheck trigger. Current text-repair work should proceed in this order: model-script specificity, terminology support, Unit 3 evidence/example scaffolding, Unit 12 B1/B2 descriptors, final Language Editor recheck. Visual/asset repair remains paused for separate treatment.
