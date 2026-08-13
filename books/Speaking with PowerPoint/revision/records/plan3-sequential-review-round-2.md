# Plan 3 Sequential Review Round 2

Date: 2026-08-13

Purpose: run the required sequential Plan 3 review order over the repaired Standard unit drafts, appendix model scripts, and Teacher Notes file.

Review order:

1. Agent 3 / Business Presentation Specialist
2. Integrate required business/context repairs
3. Agent 2 / Language Editor

Files reviewed:

- `books/Speaking with PowerPoint/revision/drafts/standard/standard-unit-01.md` through `standard-unit-12.md`
- `books/Speaking with PowerPoint/revision/drafts/appendices/process-improvement-briefing-models.md`
- `books/Speaking with PowerPoint/revision/drafts/appendices/product-service-program-launch-models.md`
- `books/Speaking with PowerPoint/revision/drafts/appendices/project-results-briefing-models.md`
- `books/Speaking with PowerPoint/revision/drafts/Teacher Notes.md`

## Agent 3: Business Presentation Specialist

Agent: Beauvoir

Agent ID: `019ff90d-6158-78f1-ab20-3dad8389c5f4`

Mode: read-only review

Verdict: Pass with repairs.

### Findings

1. `books/Speaking with PowerPoint/revision/drafts/Teacher Notes.md:85`, `:97`, `:161`; `standard-unit-10.md:138`; `standard-unit-12.md:153`

Issue: Some guardrails say to avoid `shipment`, `transaction`, or `account` details too broadly.

Why it matters: For general trading-company clients, sanitized shipment/order/procurement examples are highly relevant. The real problem is identifiable/confidential data, not the topic itself.

Recommended repair: Change the rule to allow fictional or sanitized shipment, order, procurement, supplier-status, and workflow examples, while banning real identifying details, real client/account/order numbers, and legal/regulatory advice.

Repair before Language Editor: Yes.

2. `standard-unit-12.md:38`

Issue: `trade data` is ambiguous after the clarification that `trading companies` means sogo shosha/import-export, not securities trading.

Why it matters: Learners or teachers may read `trade data` as either securities trades or import/export transactions.

Recommended repair: Replace with clearer wording such as `confidential company, client, account, order, shipment, transaction, staff, applicant, or personal data`.

Repair before Language Editor: Yes.

3. `product-service-program-launch-models.md:17`, `:218`; `project-results-briefing-models.md:20`, `:211`

Issue: Appendix model headings are not consistently labeled as business-client or government-agency variants.

Why it matters: Main units refer learners to business-client/government-agency models, so the appendix headings should make that distinction immediately clear.

Recommended repair: Rename headings consistently, e.g. `Model 1: Business Client - Launching a Supplier-Status Dashboard`; `Model 2: Government Agency - Launching an Application Support Desk`.

Repair before Language Editor: Yes.

4. `process-improvement-briefing-models.md:73-133` and `:318-378`; `project-results-briefing-models.md:78-136` and `:269-331`

Issue: The paired models still use very similar section architecture. The content contexts differ, but the visible model structures can still feel like clones.

Why it matters: The appendices should demonstrate comparable skills without implying one rigid presentation template.

Recommended repair: Keep teaching-point parity, but vary the visible structures more. For example, make one process model more decision-first and the other more service-question-led; make one results model use `result, limitation, recommendation` and the other `service change, evidence, next step`.

Repair before Language Editor: Yes, because structure affects language review.

5. `standard-unit-01.md:1` and `Teacher Notes.md:21`

Issue: Unit 1 is titled `Audience, Purpose, and Business Context`. This is understandable for a business-English book, but `workplace context` may fit the role-agnostic manuscript rule better.

Why it matters: Government-agency learners are still workplace presenters, but not always `business` presenters in the narrow company sense.

Recommended repair: Consider `Audience, Purpose, and Workplace Context` unless the final book title deliberately keeps `business presentation` as the umbrella term.

Repair before Language Editor: Optional, but useful.

### Terms for Language Editor Follow-up

`handoff`, `exception`, `pre-read`, `follow-up handout`, `takeaway document`, `fallback`, `asynchronous/async`, `sanitized`, `dashboard`, `status-check message`, `ownership`, `controlled expansion`, `rollout`, `volume-adjusted view`, `counter capacity`, `intake`, `formal review`, `update owner`, `shipment reporting deadline`.

### No-Issue Checks

- The revised meaning of `trading company` is mostly handled correctly; no remaining `same-day trade` or securities-trading scenario misuse was found.
- Government models stay administrative/service-delivery/process-focused and avoid political advocacy or sensitive operational/security detail.
- Fictional data is clearly marked in the appendix models and Unit 6.
- Q&A functions are present: clarification, direct answer, evidence bridge, risk/limitation, safe deferral, and follow-up.
- Tool-neutral workflow, PDF fallback, confidentiality, accessibility, and online/async contingency are present.
- AI is framed as critical literacy/checking, not as a replacement for learner-owned English.

## Integration Before Agent 2

The main blocking Agent 3 repairs were integrated before running Agent 2:

- Updated business-client guardrails in Teacher Notes, Units 10 and 12, and control files so fictional/sanitized shipment, order, procurement, supplier-status, workflow, and reporting examples are allowed for general trading-company contexts.
- Replaced ambiguous `trade data` wording in Unit 12.
- Renamed Unit 1 to `Audience, Purpose, and Workplace Context` in the unit draft, Teacher Notes, appendix references, and control files.
- Labeled launch and results appendix model headings as `Business Client` or `Government Agency`.
- Checked model variety: the current scripts already vary openings and transitions more than the earlier rigid draft; Agent 2 was asked to inspect phrase/template load again.

## Agent 2: Language Editor

Agent: Curie

Agent ID: `019ff911-7262-75a0-850e-9d82f3897508`

Mode: read-only review

Verdict: Pass with repairs.

This is not blocked, but it needs a focused Language Editor repair pass before layout/DOCX production.

### Findings

1. `books/Speaking with PowerPoint/revision/drafts/standard/standard-unit-01.md:51`, `standard-unit-02.md:21`, `standard-unit-04.md:52`, `standard-unit-05.md:28`, `standard-unit-07.md:3`, `standard-unit-09.md:1`

Issue: Specialist terms appear in main units before clear learner support: `handoff`, `ownership`, `rollout`, `dashboard`, `pre-read`, `fallback`, `async`.

Why it matters: B1-B2 learners may copy these terms without really understanding them.

Recommended repair: Add short `Useful terms` boxes in Units 1, 4, 5, 7, and 9, or define terms immediately before first practice use.

2. `standard-unit-01.md:11`, `:40`, `:50`, `:99`

Issue: Unit 1 title now says `Workplace Context`, but the unit still uses `business purpose`, `business reason`, `business problem`, and `Main business context`.

Why it matters: This weakens the role-agnostic manuscript rule for government/public-sector learners.

Recommended repair: Change to `workplace purpose`, `workplace reason`, `workplace problem`, and `Main workplace context`, unless the specific sentence is clearly about a company setting.

3. `standard-unit-09.md:1`, `:9`, `:36`, `:98`, `:139`, `:143`

Issue: `async` is used as a learner-facing term without first defining `asynchronous`.

Why it matters: `async` is common in tech/workplace English but not transparent for ESL learners.

Recommended repair: First use should be `asynchronous (async): recorded or prepared for people to use later, without live interaction`.

4. `product-service-program-launch-models.md:3`, `:50`, `:116`, `:315`

Issue: `rollout` and `pre-read` are central to the model but are not included in the model's `Key Vocabulary Before Listening`.

Why it matters: Learners need these terms before listening/reading the script.

Recommended repair: Add `rollout = introducing something in stages` and `pre-read = short material sent before a meeting`.

5. `standard-unit-01.md` through `standard-unit-12.md`

Issue: Heading capitalization is inconsistent: Units 1-3 use `Learning Outcomes`, `Speaking Task`, `Unit Wrap-Up`; later units use sentence-style headings.

Why it matters: Low language-development risk, but it will look inconsistent in production.

Recommended repair: Normalize to sentence-style headings, matching `plan3-style-sheet.md:308`.

6. `product-service-program-launch-models.md:433`

Issue: `If AI is mentioned with these models...` sounds slightly control/editorial rather than fully learner-facing.

Why it matters: The rule itself is correct, but the phrasing could feel like teacher guidance.

Recommended repair: Change to learner-facing wording such as: `If your class discusses AI, use it only for checking and critique...`

### Glossary / First-Use Terms

Add or check first-use support for:

`handoff`, `exception`, `ownership`, `pre-read`, `follow-up handout`, `fallback`, `asynchronous/async`, `sanitized`, `dashboard`, `status-check message`, `controlled expansion`, `rollout`, `volume-adjusted view`, `intake`, `formal review`, `update owner`.

`leave-behind`: handling is now correct. Learner text should not use it. `leave behind` without a hyphen is only the phrasal verb; the compound noun is style-dependent and too opaque here. Prefer `follow-up handout`, `takeaway document`, or `supporting document`.

### No-Issue Checks

- AI is framed as critique/checking, not as a replacement for learner-owned English.
- Learner-facing appendices no longer contain obvious teacher/editor-facing labels like `teacher notes` or `not part of the spoken presentation`.
- Business/government model labels are now clear.
- Securities/investment guardrails are present and no longer confuse `trading company` with financial trading in the main scenarios.
- Spoken model structures are more varied than the earlier draft; repeated closes are acceptable as normal presentation convention.

## Open Repair List After Round 2

Required before layout/DOCX production:

- Add or tighten first-use vocabulary support in Units 1, 4, 5, 7, and 9.
- Finish Unit 1 wording alignment from `business` context wording to `workplace` context wording where appropriate.
- Define `asynchronous (async)` before learner use in Unit 9.
- Add `rollout` and `pre-read` to the Product, Service, or Program Launch Models vocabulary support.
- Normalize heading capitalization across Units 1-12.
- Rewrite the launch appendix AI note as learner-facing classroom wording.

## Integration After Agent 2

Completed on 2026-08-13:

- Added first-use `Useful terms` support in Units 1, 4, 5, 7, and 9.
- Repaired Unit 1 stale `business` context wording to `workplace` wording where appropriate.
- Defined `asynchronous (async)` before learner use in Unit 9.
- Added `pre-read` and `rollout` to both launch-model vocabulary tables and first-use vocabulary tables.
- Rewrote the launch appendix AI note as learner-facing classroom wording: `If your class discusses AI...`
- Completed the heading capitalization pass separately using the updated Chicago-style heading rule in `plan3-style-sheet.md`.

Remaining/deferred:

- Unit 3 teaches the options-based decision structure `Situation - options - criteria - recommendation`, but no full appendix model currently demonstrates that structure. This is tracked in `revision/control/plan3-phase6-qa-checklist.md` as a QA/defer item.
- Full Phase 6 QA still needs to run after Phase 5 asset work.
