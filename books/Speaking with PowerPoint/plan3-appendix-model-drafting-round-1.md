# Plan 3 Appendix Model Drafting Round 1

Date: 2026-08-12

Purpose: durable record for drafting the six Standard appendix presentation models.

## Drafting Scope

Output folder:

- `books/Speaking with PowerPoint/drafts/appendices/`

Required appendix model files:

- `process-improvement-briefing-models.md`
- `product-service-program-launch-models.md`
- `project-results-briefing-models.md`

Each file must contain:

- one business-client / non-government finance/trading variant
- one government-agency administrative variant
- comparable depth across variants
- scenario brief
- audience and purpose
- core message
- outline
- delivery context profile
- sample opening
- visual or data point only where the presentation topic naturally requires it
- short excerpt for language analysis
- 4-6 Q&A pairs tagged by function
- unit skills demonstrated

## Control Files

- `books/Speaking with PowerPoint/plan3.md`
- `books/Speaking with PowerPoint/plan3-case-model-brief.md`
- `books/Speaking with PowerPoint/plan3-traceability.md`
- `books/Speaking with PowerPoint/standard-12-unit-curriculum-spec.md`
- `books/Speaking with PowerPoint/plan3-style-sheet.md`
- `books/Speaking with PowerPoint/plan3-phase6-qa-checklist.md`
- `books/Presentation Skills/canon/voice-S.md`

## Shared Rules

- Follow the Teaching-Point Fit Rule in `plan3-case-model-brief.md`.
- Do not force data, charts, visuals, or Q&A patterns into a model where they do not logically belong.
- Business-client variants must focus on finance/trading operations, reporting, workflow, client service, service quality, control escalation, or internal service launch.
- Government-agency variants must focus on administrative tasks, service delivery, internal process improvement, reporting, coordination, public-facing administrative communication, or staff workflow.
- Do not create investment advice, market predictions, real client/account data, regulatory/legal advice, real firm names, exchange names, ticker symbols, proprietary systems, political advocacy, legislation, budget campaigning, policy argument, flags, seals, emblems, crests, party symbols, or country-specific government iconography.
- Use fictional data only and label it as fictional for practice.
- Keep models B1-B2 usable and aligned to Standard voice.
- AI should not be part of these model presentations unless a unit later uses a separate flawed-output critique; do not promote AI in the models.

## Agent Assignments

| Agent Role | Agent ID | Nickname | Output File | Status |
|---|---|---|---|---|
| Process Improvement Model Agent | `019ff4df-9a32-7610-b143-6b5745e5aa61` | Kierkegaard | `process-improvement-briefing-models.md` | complete |
| Launch Model Agent | `019ff4df-d234-7651-affa-362ae3030874` | Carson | `product-service-program-launch-models.md` | complete |
| Project Results Model Agent | `019ff4e0-0453-7f00-b610-ffef4a5cfa9c` | Avicenna | `project-results-briefing-models.md` | complete |

## Agent Run Log

| Agent | Agent ID | Assignment | Result | Files Changed |
|---|---|---|---|---|
| Process Improvement Model Agent / Kierkegaard | `019ff4df-9a32-7610-b143-6b5745e5aa61` | Draft paired business-client and government-agency process improvement briefing models. | Complete. Drafted two paired process improvement models: Seika Capital Operations trade confirmation delay workflow pilot and Midori Ward returned application forms intake checklist trial. Constraint scan found no unit terminology issue, no AI promotion, and restricted finance/government terms only in guardrail language. | `books/Speaking with PowerPoint/drafts/appendices/process-improvement-briefing-models.md` |
| Launch Model Agent / Carson | `019ff4df-d234-7651-affa-362ae3030874` | Draft paired business-client and government-agency launch briefing models. | Complete. Drafted two paired launch models: Koyo Markets Client Services reporting dashboard pilot and Aoba City Administrative Support Center application support desk pilot. Constraint scan found no unit terminology issue, no AI promotion, and restricted finance/government terms only in guardrail language. | `books/Speaking with PowerPoint/drafts/appendices/product-service-program-launch-models.md` |
| Project Results Model Agent / Avicenna | `019ff4e0-0453-7f00-b610-ffef4a5cfa9c` | Draft paired business-client and government-agency project results briefing models. | Complete. Drafted two paired project results models: Seika Capital Operations exception resolution pilot results and Midori Ward intake checklist trial results. Constraint checks found no `Lesson` terminology, no AI promotion, and all required sections present. Restriction terms appear only as guardrails. | `books/Speaking with PowerPoint/drafts/appendices/project-results-briefing-models.md` |

## Content Architect Integration Notes

- Project Results Briefing Models drafted first because the teaching-point fit is straightforward: project results naturally supports data/chart explanation, cautious claims, evidence-based Q&A, online or async adaptation, and final recommendation language.
- The two variants are intentionally parallel in structure and skill focus, but the operational pressures differ: finance/trading emphasizes control risk, duplicate log ownership, and volume effects; government administration emphasizes waiting time, rotating staff, update ownership, and service consistency.
- Process Improvement Briefing Models use evidence only to support a workflow pilot decision; they do not force chart teaching beyond simple process evidence.
- Launch Models use dashboard, service-flow, timeline, and document-role artifacts because those naturally fit launch presentations.
- Content Architect integration should normalize heading style across the three appendix files and check unit cross-references before the next unit revision pass.

## Initial QA

Checks run after agent return:

- Required-section check across all three appendix files: passed.
- Business-client and government-agency variant presence: passed.
- Fictional-data labeling presence: passed.
- Restricted-term scan: matches are guardrail language only.
- AI-promotion scan: no model content promotes AI.

Notes:

- Two agents exceeded the requested write scope by touching recordkeeping files. The useful recordkeeping content was retained, and a malformed `instruction-read-log.csv` append was repaired into separate CSV rows.
- The next integration pass should review the six variants side by side for parity, heading style, B1-B2 readability, and exact unit cross-reference wording.
