# Plan 3 Specialist Review Round 1

Date: 2026-08-12

Purpose: durable record of the first concurrent specialist review round for the Plan 3 rebuild. This preserves the agent work that was returned in chat before manuscript drafting began.

## Review Scope

The round used the Plan 3 roles that can work concurrently without changing the course architecture:

- Language Editor
- Business Presentation Specialist
- Asset and QA Specialist

Review mode: read-only. Agents were instructed not to edit files, create assets, or draft lessons.

Files under review:

- `books/Speaking with PowerPoint/plan3.md`
- `books/Speaking with PowerPoint/standard-12-lesson-curriculum-spec.md`
- `books/Speaking with PowerPoint/plan3-style-sheet.md`
- `books/Speaking with PowerPoint/plan3-case-model-brief.md`
- `books/Speaking with PowerPoint/plan3-traceability.md`
- `books/Speaking with PowerPoint/plan3-phase6-qa-checklist.md`
- `books/Presentation Skills/images/image_register.json` for the Asset and QA Specialist where useful

## Agent 1: Language Editor

Agent ID: `019ff4b1-3c6b-7323-92f5-e9cc81a45c63`

Nickname: `Lagrange`

Assignment:

Review for B1-B2 ESL fit, English language-development focus, presentation-English syllabus coverage, Japanese-learner support, and AI caution. Check whether any wording risks promoting AI as a replacement for language growth. Check whether tasks are feasible for adult business English learners. Return concise findings with file/section references and concrete proposed fixes. Do not rewrite the files and do not draft lessons.

Returned findings:

1. Medium: Lessons 5 and 7 could drift from English development into design/workflow training. `standard-12-lesson-curriculum-spec.md` has strong visual/tool content, but the learner deliverables are mainly artifacts. Proposed fix: add required spoken micro-outputs, such as explaining a visual choice in 45-60 seconds and justifying a format choice using target language for handouts, pre-reads, backup files, confidentiality, and follow-up.

2. Medium: Japanese-learner support is good in the style sheet but under-mapped in the lesson spine. Proposed fix: add placement notes for Lesson 2 bilingual planning, Lesson 5/6 article-plural slide text, Lesson 8 katakana/stress/thought groups, and Lesson 10 polite direct disagreement. Also expand traceability beyond Lessons 4 and 8.

3. Medium: Some Standard tasks are feasible for adult B1-B2 learners only if tightly scaffolded. Lesson 7 asks learners to choose among many formats and check export/security issues; Lesson 9 combines online, hybrid, and async delivery. Proposed fix: state that Standard uses constrained choice menus, short scenarios, sentence frames, and one chosen output per learner; reserve multi-format comparison and full async production for Long.

4. Low: AI caution is mostly strong, but "rewrite output into learner-owned English" could be misread as AI-assisted composition. Proposed fix: specify that AI tasks use short flawed sample outputs for critique only, not the learner's final presentation, and that learners must produce their own assessed message, slides, notes, rehearsal, and delivery.

5. Low: Presentation-English coverage is broad, but contingency language is missing from the explicit syllabus. Proposed fix: add categories for technical problems, screen-sharing transitions, audio/caption issues, timing recovery, and moving to a backup file.

6. Cleanup: `plan3.md` still contained `:codex-annotation{index="1"}`. Proposed fix: remove the annotation before approval.

Overall conclusion:

Plan 3 is suitable for adult B1-B2 business English learners and does not broadly promote AI as a replacement for language growth. The main implementation risk is drift: visual/tool lessons need mandatory spoken-English outputs and tighter B1-B2 scaffolding.

## Agent 2: Business Presentation Specialist

Agent ID: `019ff4b1-591c-7273-bb2b-12b54df2bb75`

Nickname: `Kuhn`

Assignment:

Review for business-presentation realism, finance/trading business-client fit, government-agency administrative-task fit, role-agnostic main-text strategy, appendix model usefulness, tool-neutral workflow, document roles, delivery contexts, and Q&A realism. Return concise findings with file/section references and concrete proposed fixes. Do not edit files and do not draft lessons.

Returned findings:

1. Traceability does not yet enforce the new business/government audience split. The case/model brief correctly says main text stays role-agnostic and variants carry finance/trading and government-agency specificity, but traceability only tracks recurring cases generally. Proposed fix: add explicit traceability rows for audience-variant rule, finance/trading operations fit, government administrative-task fit, appendix model parity, and main lesson body remaining role-agnostic.

2. The Standard spec still reads too generic in the case table. Proposed fix: keep the Standard table role-agnostic, but add a note that concrete model variants must follow the case/model brief: finance/trading operations, reporting, client-service, or control contexts for business-client examples; administrative service/process/reporting contexts for government examples.

3. Appendix model system is promising but not operational enough for drafting. What is missing is the promised trace from each model to language points, visual-design points, delivery behaviors, and assessment criteria. Proposed fix: add a compact matrix per model set with columns for lesson reference, excerpt to reuse, target language, visual principle, delivery behavior, Q&A skill, and rubric category.

4. Q&A realism is under-specified. The plan gives pressure points, but does not require model answers, follow-up moves, or realistic constraints such as lacking a number, needing policy confirmation, or requiring risk/control approval. Proposed fix: require each appendix model to include 4-6 Q&A pairs tagged by function: clarify, answer directly, bridge to evidence, defer safely, acknowledge risk, and confirm follow-up.

5. Finance/trading fit is mostly safe, but the curriculum should carry the boundary rules forward. Proposed fix: add task-level constraints: no trade recommendations, no client names, no real account data, no regulatory advice; focus on workflow, reporting, evidence, service quality, and control escalation.

6. Document roles are named, but delivery-context decisions need sharper scenario binding. Proposed fix: add a delivery context profile to each model brief: mode, audience, time limit, required materials, optional backup materials, confidentiality/accessibility checks, and expected interaction pattern.

7. Government-agency administrative fit is good, but avoid drifting into public-policy debate. Proposed fix: add a guardrail that government examples should not become political advocacy, legislation, budget campaigning, or public-policy argument unless explicitly approved; they should stay in administrative improvement, reporting, coordination, and service communication.

8. Minor cleanup item: remove `:codex-annotation{index="1"}` from `plan3.md`.

## Agent 3: Asset and QA Specialist

Agent ID: `019ff4b1-7685-7e81-8f31-f5f66396d50e`

Nickname: `Popper`

Assignment:

Review for asset feasibility, accessibility coverage, source/factual QA, privacy/security/copyright checks, visual restrictions for finance/trading and government examples, generated-image risk, and whether the Phase 6 checklist is operational enough. Return concise findings with file/section references and concrete proposed fixes. Do not edit files and do not create assets.

Returned findings:

1. Asset register is not release-ready against Plan 3 requirements. The style sheet and Phase 6 checklist require source, license status, alt text, captions, lesson/tier use, and replacement rationale, but the existing `books/Presentation Skills/images/image_register.json` currently has prompts/descriptions only. Proposed fix: define a required asset schema and add QA rows that fail any asset missing `file_path`, `source`, `license_status`, `generated_or_original`, `alt_text`, `decorative`, `caption`, `lesson_tier_use`, `replacement_rationale`, `visual_restriction_check`, and `approved_by`.

2. Phase 6 checklist is too thin operationally for QA execution. It says Repair/Defer items need file/location, owner, and next action, but the tables only have `Check | Status | Notes`. Proposed fix: use an execution format with `Check | Tier/Deliverable | Status | Evidence/File | Owner | Repair/Defer Action | Recheck Result`.

3. Accessibility coverage exists, but acceptance criteria are vague. Proposed fix: add concrete criteria: contrast target, color-not-alone confirmation, alt/decorative decision for every asset, chart label check, caption/transcript check for recorded/async material, Word accessibility check, PDF accessibility check, and manual limitations note.

4. Finance/trading visual restrictions are missing from Phase 6. Proposed fix: add a finance/trading visual QA row checking for no real firm names, logos, exchange names, ticker symbols, client data, proprietary UI, market predictions, trade recommendations, or compliance/legal advice.

5. Generated-image risk is under-controlled in the checklist. Proposed fix: add per-image visual inspection fields: text accuracy, element count, label placement, no stray readable text, no logos/watermarks, no flags/seals/crests, representation check for people, transparent-background check where applicable, and regenerate-versus-repair decision.

6. Existing image prompts are risky if reused for Plan 3. The style lock says people must read as Japanese/East Asian and no flags/emblems, but many older people-containing prompts do not repeat that constraint. Proposed fix: either do not reuse those assets for Plan 3, or require prompt/register revision and visual reapproval before reuse.

7. Privacy/security checks are present but not specific enough for mockups. Proposed fix: add rows for no real client/company/person/account names, no real screenshots unless current and permission-cleared, all dashboard/mockup data fictional and labeled, and DOCX/PDF metadata containing no legacy/client-confidential residue.

8. Plan 3 itself violates its own cleanup rules. `plan3.md` still contained the annotation marker and wording issues such as `QA And Acceptance`, `AI-use policy`, and `license/status`. Proposed fix: include these in Phase 6 Production QA or fix before drafting.

Overall conclusion:

The policy layer is strong, especially the AI, source, accessibility, finance/trading, and government-visual restrictions. The main weakness is operationalization: Phase 6 needs evidence fields, owners, pass thresholds, and asset-register schema enforcement.

## Integration Actions Taken

After the three reviews returned, the Content Architect integrated the findings into the planning/control files.

Updated files:

- `books/Speaking with PowerPoint/plan3.md`
- `books/Speaking with PowerPoint/standard-12-lesson-curriculum-spec.md`
- `books/Speaking with PowerPoint/plan3-style-sheet.md`
- `books/Speaking with PowerPoint/plan3-traceability.md`
- `books/Speaking with PowerPoint/plan3-phase6-qa-checklist.md`
- `books/Speaking with PowerPoint/plan3-case-model-brief.md`
- `project-journal.md`

Integrated changes:

- Removed the saved Codex annotation marker from `plan3.md`.
- Cleaned `QA and Acceptance`, `AI use policy`, `license status`, and `the OpenAI image generation API` wording.
- Added spoken micro-outputs to visual/tool lessons so they remain anchored in English development.
- Added B1-B2 scaffolding constraints for Standard, especially constrained choices and one chosen output per learner.
- Added Japanese-learner placement notes for bilingual planning, slide-text articles/plurals, thought groups/stress, and polite direct disagreement.
- Strengthened AI policy so AI tasks use short flawed samples for critique only and cannot become a drafting workflow for assessed work.
- Added contingency language categories for technical problems, screen sharing, audio/caption issues, timing recovery, and backup-file transitions.
- Added traceability rows for audience-variant rule, finance/trading business-client focus, government-agency administrative focus, and appendix model parity.
- Expanded the case/model brief with six concrete appendix model briefs, delivery context profiles, required Q&A functions, and a model-to-lesson trace matrix.
- Added finance/trading and government-agency guardrails to the curriculum spec, style sheet, traceability matrix, and QA checklist.
- Hardened Phase 6 QA with an execution evidence format, concrete accessibility checks, asset schema requirements, generated-image inspection, privacy/security mockup checks, and metadata checks.

Open follow-up:

- Create an asset/register schema or template before generating or reusing final assets.
- Decide whether to update the existing `books/Presentation Skills/images/image_register.json` or create a Plan 3-specific asset register.
- Next drafting phase should remain centralized until the updated planning package is reviewed and committed.
