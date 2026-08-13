# Plan 3 Phase 6 Repair Agent Review, Round 1

Date: 2026-08-13

Purpose: run a focused multi-agent review over Phase 6 repair issues, excluding visual/asset repair because that workstream has been paused for separate treatment.

Review order:

1. Agent 1: Control QA Analyst
2. Agent 2: Business/Government Presentation Specialist
3. Agent 4: Language Editor

Important sequencing rule: the Language Editor ran after the Business/Government Presentation Specialist because terminology and learner-language risks depend on the settled business/context wording.

## Agent 1: Control QA Analyst

### QA IDs in Scope

Repair rows in scope: `QA-001`, `QA-002`, `QA-003`, `QA-119`, `QA-120`, `QA-121`.

Adjacent but not Repair-row scope: `QA-122` is `Defer`, not Repair. Visual/asset repair rows are intentionally outside this review and should remain a later separate workstream.

### Missing

`books/Speaking with PowerPoint/plan3.md` is missing at the requested path. The current file appears to be `books/Speaking with PowerPoint/revision/control/plan3.md`.

`QA-001`: `plan3-traceability.md` still has planning dispositions like `Required`, `Reframed`, `Promoted`, and `Superseded by Plan 3`, but no implementation status column with `Pass/Repair/Defer/N/A`.

`QA-002`: consolidated task IDs `P0-01` through `P3-04` are mapped, but they do not yet have Phase 6 evidence, owner, repair/defer action, or recheck result.

`QA-003`: no final defer log exists. Existing defer-like notes are scattered across the QA checklist, traceability, image register, and `phase6-qa-review-2026-08-13.md`.

`QA-119`: significant external/current Phase 6 issues are not classified in one authoritative place by `scope`, `pedagogy`, `factual accuracy`, `accessibility`, `assessment`, `production`, or `style`.

`QA-120`: significant issues are not yet all resolved or formally deferred with reason and impact. For visual/asset issues, the correct control action is classification/deferral, not asset repair in this workstream.

`QA-121`: `plan3-traceability.md` has not been updated for the latest Phase 6 findings, especially example/model specificity, rejected/deferred assets, tiers, and export/production gates.

### Recommended File-Level Repairs

Update `books/Speaking with PowerPoint/revision/control/plan3-traceability.md` by adding Phase 6 execution columns: `Phase 6 Status`, `Evidence/File`, `Owner`, `Repair/Defer Action`, `Recheck Result`. Apply these row-by-row to all `P0-01` through `P3-04` and Plan 3-specific requirements.

Create a dedicated defer log, preferably `books/Speaking with PowerPoint/revision/control/plan3-phase6-defer-log.md`, with columns: `Item/QA ID`, `Deferred Work`, `Reason`, `Impact`, `Owner`, `Recommended Future Action`, `Recheck Trigger`. Include at minimum Essentials, Long, options-based decision model, final DOCX/PDF export checks, accessibility/export checks, release notes, and visual/asset workstream items.

Add a significant-issues classification table, either in `plan3-traceability.md` or a companion control file such as `plan3-phase6-external-issue-log.md`. It should include source record, issue summary, type, affected QA IDs, status, owner, disposition, and traceability row updated.

Update `books/Speaking with PowerPoint/revision/control/plan3-phase6-qa-checklist.md` only after the above repairs, so each row's status is backed by the traceability/defer/classification records rather than notes alone.

### Status Recommendations

Keep `QA-001` as `Repair` until traceability has row-level Phase 6 statuses. Move to `Pass` after every traceability row has a valid status and evidence.

Keep `QA-002` as `Repair` until every consolidated task ID has evidence or a formal defer entry. Then move to `Pass`.

Keep `QA-003` as `Repair` until the final defer log exists. Then move to `Pass`, assuming it includes reason, impact, and future action for each deferral.

Keep `QA-119` as `Repair` until significant issues are classified in one authoritative log/table. Then move to `Pass`.

Keep `QA-120` as `Repair` until all significant issues are either repaired or formally deferred. Visual/asset issues should be deferred to the separate visual/asset workstream, not repaired here.

Keep `QA-121` as `Repair` until `plan3-traceability.md` reflects the current Phase 6 findings. Then move to `Pass`.

## Agent 2: Business/Government Presentation Specialist

### QA IDs in Scope

Primary: `QA-011`, `QA-012`, `QA-019`, `QA-020`, `QA-021`, `QA-022`, `QA-023`, `QA-025`, `QA-026`, `QA-031`, `QA-033`, `QA-080`, `QA-086`, `QA-087`.

Related/dependent: `QA-003`, `QA-024`, `QA-053`, `QA-085`, `QA-091`, `QA-093`, `QA-104`, `QA-119`, `QA-120`, `QA-121`.

### Model-by-Model Findings

`process-improvement-briefing-models.md`

- Business model: broadly strong and now correctly reads as general trading-company operations, not securities trading. Import document handoff, exception log, shipment cutoff, and control-process language fit Marubeni/Itochu-style operational work. It demonstrates Units 1, 2, 3, 7, 10, and 12 reasonably well.
- Needed repair: add slightly more concrete operational realism: fictional location/team, document type, cutoff time, supplier or product category, and one short example of a typical exception. Example: "the Yokohama import documentation desk," "industrial parts from Supplier A," "3:00 p.m. shipping-document preparation cutoff."
- Government model: appropriate public-sector administrative process work. It is not just a business case with renamed actors, but it remains somewhat generic.
- Needed repair: specify one fictional application type and one service setting. Example: "housing support certificate application," "counter and online submissions," "temporary staff during the Monday morning peak." Keep it non-political and non-policy.

`product-service-program-launch-models.md`

- Business model: the supplier-status dashboard is a good general trading-company/service-operations launch case. Guardrails against securities trading are explicit and useful.
- Needed repair: "account managers" may sound financial to some learners. Add support that these are client/service account managers, not securities account managers. Add concrete business examples for each benefit: one shipment-reporting deadline, one unresolved supplier inquiry, one repeated status-check chain.
- Government model: strong administrative/service-delivery fit. The support desk is credible and clearly limited; it avoids policy advocacy.
- Needed repair: add one selected online form/process, pilot hours, and service channel detail. Example: "resident certificate support form," "Tuesday/Thursday morning desk," "counter and call-center handoff." This would make the staffing and counter-capacity Q&A more realistic.

`project-results-briefing-models.md`

- Business model: good results briefing structure and good caution language. It demonstrates Unit 6 chart/evidence skills better than the process models.
- Needed repair: the Q&A mentions volume adjustment, but the script does not give enough detail to support it. Add one fictional volume-adjusted number or backup-table example. Also name the two expansion desks fictionally.
- Government model: credible administrative results case with clear service metrics: returned applications, repeat inquiries, attachment-related returns, waiting time.
- Needed repair: add the two application types proposed for expansion and one realistic staff/workload detail. The model would then better justify the recommendation and Q&A.

`slide-design-checklist.md`

- Useful as a learner-facing support appendix for Units 5 and 7.
- Not a model script, so it does not need business/government pairing. It can remain general.

### Concrete Additions Needed

Add these kinds of fictional details:

- Business/process: fictional team names, import lane/product category, cutoff time, document type, one example exception, one pilot owner.
- Business/launch: dashboard users, supplier inquiry example, reporting deadline, two pilot teams, one sample field list.
- Business/results: before/after volume, volume-adjusted rate, two expansion desks, one duplicate-entry example.
- Government/process: application type, channel, staff role, peak time, one common missing item.
- Government/launch: selected online form, desk hours, staffing pattern, support limits, user access issue.
- Government/results: two expansion application types, waiting-time baseline/target, rotating-staff training note.

For main-point examples, each model should include at least one concrete example under the main teaching points: problem, evidence, recommendation, benefit/service impact, risk/limitation, next action.

### Terminology Needing Learner Support

Watch these for first-use support or glossary treatment after repairs: `handoff`, `exception`, `checkpoint`, `control process`, `cutoff`, `desk`, `account manager`, `account-service`, `supplier-status`, `dashboard`, `reporting cycle`, `status-check message`, `shipment reporting deadline`, `ownership`, `sanitized`, `rollout`, `pre-read`, `follow-up handout`, `data-field list`, `intake`, `formal review`, `repeat inquiry`, `counter capacity`, `public-facing`, `screen reader`, `alt text`, `metadata`, `PDF fallback`, `volume-adjusted`, `duplicate entries`, `high-volume application type`, `update owner`.

### Recommended Edit Sequence

1. Repair broken appendix image references or replace them with deck-only wording before any final QA.
2. Add concrete fictional details to the six model scenario briefs first.
3. Add one short example under each model's main spoken point where the script is still generic.
4. Strengthen parity checks pair by pair: process, launch, results.
5. Update vocabulary boxes after added details introduce new terms.
6. Update model-to-unit mapping/control notes only after the model scripts are stable.
7. Keep `QA-020` as an explicit defer unless a short options-based decision model or excerpt is added.
8. Run the final Language Editor pass last, focused on B1-B2 load, learner-facing clarity, terminology support, and spoken naturalness.

## Agent 4: Language Editor

### QA IDs in Scope

Primary Language Editor scope: `QA-011`, `QA-012`, `QA-019`, `QA-021`, `QA-022`, `QA-023`, `QA-027`-`QA-039`, `QA-055`, `QA-058`, `QA-063`-`QA-065`, `QA-071`, `QA-085`-`QA-087`, `QA-095`-`QA-100`, `QA-104`-`QA-106`, `QA-116`, `QA-119`-`QA-121`.

Production issues only noted, not repaired: `QA-066`, `QA-074`-`QA-081`, `QA-091`, `QA-093`.

### Main Findings

The Standard units are generally learner-facing, clear, and suitable for B1-B2 learners. The biggest language risk is not general difficulty; it is the load created by newly specific workplace compounds and process terms. This is especially visible in Units 5-7, Unit 10, Unit 12, and all six appendix scripts.

Broken image references remain in Units 5, 6, 7, 9 and appendix model files. These are production issues, not language repair, but they affect learner-facing clarity where tasks ask learners to inspect a missing visual.

Teacher/learner separation is mostly fixed, but the appendix files still include production-facing wording: "The deck is a draft planning asset. Images or final textbook screenshots can be added later after visual approval." This appears in all six model slide-set notes and should not be in learner-facing appendices.

### Learner-Facing Language Issues

- Unit 5 uses `accessibility` several times before the definition section. Define it at first use or move the definition earlier.
- Unit 2 uses `rollout` before it is taught later. Add a short first-use gloss or replace with "wider use" until Unit 4/5.
- Unit 3 uses `handoff` and `ownership` in examples, but Unit 3 itself does not support `ownership`. Add a small useful-terms box or simpler wording.
- Unit 6 introduces several terms through examples without a local support box: `checkpoint`, `rollout`, `dashboard`, `status-check messages`, `intake`. Add a short "Useful terms for this unit" table.
- Unit 7 defines several terms well, but `pre-read` and `dashboard` appear in the opening paragraph before the terms table. Add parenthetical support on first use or move the table earlier.
- Unit 12 has assessment categories but no B1/B2 descriptors. This is the clearest assessment-language gap.

### Terms Needing First-Use or Glossary Support

Already supported somewhere but still worth glossary inclusion because they recur: `handoff`, `exception`, `checkpoint`, `control process`, `dashboard`, `ownership`, `sanitized`, `rollout`, `pre-read`, `follow-up handout`, `intake`, `formal review`, `repeat inquiry`, `screen reader`, `alt text`, `PDF fallback`, `accessibility`, `confidentiality`.

Need stronger or more local support after the business/government specificity pass: `cutoff`, `desk`, `account manager`, `account-service`, `supplier-status`, `reporting cycle`, `status-check message`, `shipment reporting deadline`, `data-field list`, `counter capacity`, `public-facing`, `metadata`, `volume-adjusted`, `duplicate entries`, `high-volume application type`, `update owner`.

Teacher Notes line 28 currently lists only a shorter watchlist; it should be expanded to include the newer Business/Government terms.

### Model-Script Wording Risks

The six scripts now better reflect general trading-company operations rather than securities trading. That correction is good, but the scripts risk becoming noun-heavy.

High-load phrases to simplify or gloss:

- "same-day import document handoff delays"
- "daily shipping cutoff preparation window"
- "risk/control representative"
- "account-service representative"
- "supplier-status dashboard"
- "shipment reporting deadlines"
- "data-field list"
- "volume-adjusted view"
- "duplicate-entry ownership"
- "high-volume application types"
- "public-facing communication"

Recommended approach: keep the concrete fictional details, but split long compounds into shorter spoken sentences and add brief before-listening definitions. Avoid adding more disclaimer language inside the spoken scripts; securities/legal guardrails can mostly stay in notes or short learner cautions.

### Unit-Level Repairs Needed

Unit 3: add stronger evidence/example scaffolding. Learners need to know what counts as evidence, what counts as an example, and when a detail belongs in Q&A, an appendix, or the main flow. Also add a small options-based decision example or explicitly defer it, because the unit teaches `Situation - options - criteria - recommendation` but the appendix set still lacks a full model for that structure.

Unit 5: define `accessibility` before first use and repair broken image references.

Unit 6: add a useful-terms box and repair broken chart references. This unit is otherwise strong on cautious claims and fictional-data labeling.

Unit 7: move or repeat definitions for `pre-read`, `dashboard`, `PDF fallback`, and `sanitized` near first use. Repair broken workflow references.

Unit 9: broken setup-check image reference remains. Language is otherwise clear, and `asynchronous (async)` is defined well.

Unit 12: add explicit B1/B2 assessment descriptors. Suggested split: B1 = clear prepared structure, simple accurate phrases, expected Q&A with support; B2 = more flexible signposting, clearer evidence limits, better audience adaptation, and more independent Q&A handling.

### Teacher Notes Issues

Teacher Notes are useful and properly separated. Needed repair: expand the terminology watchlist and add Unit 12 B1/B2 descriptor guidance for assessors. No major teacher-facing leakage found in Standard units, but appendix production notes should be removed or rewritten for learners.

### Recommended Edit Sequence

1. Remove learner-facing appendix production notes about draft decks/visual approval.
2. Fix first-use terminology support across Units 2, 3, 5, 6, 7, 10, 12 and appendix scripts.
3. Repair Unit 3 evidence/example scaffolding and decide whether to add or defer an options-based model.
4. Add Unit 12 B1/B2 assessment descriptors in learner checklist and Teacher Notes.
5. Smooth appendix scripts for spoken naturalness after specificity additions.
6. Repair broken image references/deck references as a production pass.
7. Run final terminology, heading, learner-facing, and link/reference scans.

## Integrated Repair Sequence

1. Create or update the control evidence layer: traceability execution columns, defer log, and issue classification.
2. Repair model-script specificity in scenario briefs and spoken scripts while keeping scripts B1-B2 manageable.
3. Add first-use terminology support and update Teacher Notes terminology guidance.
4. Strengthen Unit 3 evidence/example scaffolding.
5. Add Unit 12 B1/B2 assessment descriptors in learner-facing material and Teacher Notes.
6. Remove production-facing appendix notes from learner-facing appendices.
7. Run final Language Editor recheck after the above repairs.

Visual/asset repair remains intentionally excluded from this round.
