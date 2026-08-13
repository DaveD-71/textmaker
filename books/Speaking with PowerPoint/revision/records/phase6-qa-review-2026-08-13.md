# Phase 6 QA Review

Date: 2026-08-13

Scope: current Standard unit drafts, appendix model scripts, teacher notes, Plan 3 control files, image register, and current model-deck assets under `books/Speaking with PowerPoint/revision/`.

Verdict: **Phase 6 is not passed.** The manuscript has a usable Standard-unit spine and several strong language/QA foundations, but it has release-blocking repairs in model specificity, examples pedagogy, asset/link integrity, and tier completion.

## Startup and Repository Context

- Workspace root: `\\prod-fs-gen01\WorkFile\04_在宅勤務\★グローバルビジネス推進部（在宅）\ランゲージサービス課\Dobson（在宅）\04. Projects\code\textmaker`
- Repository status at audit start: `main...origin/main`, clean.
- Instruction files and project memory were present. Read audit rows were appended to `instruction-read-log.csv`.

## High-Level Result

| QA Area | Status | Evidence / Note | Owner | Repair / Defer Action |
|---|---|---|---|---|
| Requirement coverage | Repair | Traceability exists, but Phase 6 execution status has not been applied row-by-row. Missing options-based decision model remains open. | Content Architect | Convert this review into row-level Pass/Repair/Defer log before final release. |
| Curriculum and unit QA | Repair | Standard has 12 units; all units have 3 learning outcomes. Most have deliverables, but Unit 12 lacks the exact `## Learner Deliverable` heading. Essentials and Long drafts do not exist. | Content Architect | Normalize Unit 12 deliverable heading; either defer Essentials/Long formally or create them later. |
| Example/model appendix QA | Repair | Unit 3 requires evidence/examples for each body section, but the textbook lacks a teaching block showing weak vs strong examples. Model scripts include numbers but often miss period, site/team, source, form/process name, and ownership detail. | Business Presentation Specialist, then Language Editor | Add “what makes a useful example” instruction and revise model scripts with concrete fictional/sanitized details. |
| ESL and Business English QA | Repair | Core language syllabus is broadly present. However, model scripts retain specialized terms and generic business/process references that need stronger first-use support and concrete context. | Language Editor | Run Language Editor after business-context repair. |
| AI policy QA | Pass with watch | AI appears as critical literacy and not as final-production outsourcing. | Language Editor | Keep as-is; recheck after later edits. |
| Visuals/documents/tool-neutral QA | Repair | Units teach tool-neutral workflow, but all deleted planned image references still appear in units/appendices. Model slide-deck direction is paused after rejected assets. | Asset and QA Specialist | Remove or replace broken image links; rebuild only after content is stable. |
| Delivery/Q&A/interaction QA | Pass with minor repair | Units 8-10 and Unit 12 cover delivery, online/async, and Q&A. Q&A is compulsory in Unit 12. | Language Editor | Recheck after model script specificity repair. |
| Accessibility QA | Repair | Accessibility is taught in Units 5, 7, 9, 12 and appendix notes. Production checks cannot pass because image assets are missing/rejected and no final DOCX/PDF exists. | Asset and QA Specialist | Recheck with final assets and exports; document manual accessibility limits. |
| Asset QA | Repair | `plan3_image_register.json` is valid JSON. Nine core assets are marked rejected and deleted. Six model-deck entries are draft. Several learner files still reference deleted PNGs. | Asset and QA Specialist | Update register paths/status and remove broken links from manuscript. |
| Factual/source/privacy/security QA | Repair | Fictional/sanitized labels and guardrails are present. But fictional examples are too generic; many claims use `last month`, `last reporting cycle`, `one high-volume application type`, etc., without enough scope/source detail. | Business Presentation Specialist | Add fictional but realistic source, period, scope, and process detail. |
| Assessment QA | Pass with minor repair | Unit 12 includes final task, rubric categories, required Q&A, self-review, and peer/formal distinction. | Content Architect | Rename/add exact learner deliverable heading for consistency. |
| Production/export QA | Defer | No final DOCX/PDF export exists. Metadata and page layout cannot be checked yet. | Asset and QA Specialist | Defer until manuscript and assets are stable. |
| Cross-series QA | Defer/Repair | Essentials and Long are planned but not drafted. | Content Architect | Formal deferral required if current deliverable is Standard only. |
| External review gate | Repair | Feedback files exist, but current Phase 6 findings show previous review agents missed material issues in examples/model specificity and asset quality. | Content Architect | Classify current findings as significant review failures and update repair plan. |

## Specific Blocking Findings

### 1. Broken Learner-Facing Image Links

The following deleted PNG references still appear in current learner-facing files:

- `standard-unit-05.md`: `p3-u05-visual-hierarchy-comparison.png`, `p3-u05-sample-ab-readability.png`
- `standard-unit-06.md`: `p3-u06-import-document-handoff-results-chart.png`, `p3-u06-application-intake-results-chart.png`
- `standard-unit-07.md`: `p3-u07-import-document-handoff-workflow.png`, `p3-u07-application-intake-workflow.png`
- `standard-unit-09.md`: `p3-u09-online-delivery-setup.png`
- `process-improvement-briefing-models.md`: import handoff workflow and application intake workflow PNGs
- `product-service-program-launch-models.md`: dashboard mockup and application support service-flow PNGs
- `project-results-briefing-models.md`: import handoff results chart and application intake results chart PNGs

Repair action: remove these image embeds for now, replace with placeholder instructions, or regenerate approved assets later.

### 2. Model Scripts Are Under-Specific

All six model scripts include some numbers, but none include enough realistic presentation detail. The scripts lack exact fictional dates/periods, desk/site/team names, source notes, sample scope, form/process names, owner names, and operational constraints.

Examples of under-specific phrasing:

- `last month`
- `last reporting cycle`
- `one high-volume application type`
- `two teams`
- `selected online form process`
- `some entries`
- `many forms`
- `common problems`

QA judgment: this fails the Unit 3 expectation that body sections include evidence or examples, because a model presentation should demonstrate what good examples look like.

Repair action: add concrete fictional/sanitized details to each main point and add a learner-facing teaching block on what makes an example useful.

### 3. The Textbook Does Not Teach “Examples of Examples”

Unit 3 requires:

- Main point 1 + evidence or example
- Main point 2 + evidence or example
- Main point 3 or next section + evidence or example

But the units do not explicitly teach the difference between weak and strong examples.

Repair action: add a small Unit 3 or Unit 6 teaching block:

| Main point | Weak example | Stronger example | Why it works |
|---|---|---|---|

The strong example should include at least some of: time period, team/place, number, process/item, source, and audience relevance.

### 4. Asset Direction Is Not Stable

The OpenAI/Pillow PNG asset batch was rejected. The custom PptxGenJS model-deck approach was also rejected as visually weak. One readable native PowerPoint 16:9 test deck exists, but the broader model-deck plan is paused.

Repair action: keep asset creation paused until the model scripts and example-detail standard are fixed.

### 5. Tier Scope Is Incomplete

Plan 3 defines Essentials, Standard, and Long, but only Standard exists as current unit drafts.

Repair action: either formally defer Essentials/Long or create those tiers after Standard passes QA.

## Pass / Strength Areas

- Standard 12-unit spine exists.
- All Standard units have three learning outcomes.
- Most units have learner deliverables and spoken tasks or spoken outputs.
- Tool-neutral framing is largely successful; PowerPoint is not the course concept.
- AI policy is aligned with the user decision: mention but do not promote.
- Teacher notes are separate from learner-facing units.
- Unit 12 includes required Q&A, rubric-style criteria, self-review, and a wrap-up quiz.
- Privacy/security guardrails are present in units and model appendices.
- Accessibility is taught as ordinary presentation quality in learner-facing material.

## Recommended Repair Order

1. Pause assets until content/model specificity is repaired.
2. Add an explicit “good examples” teaching block to Unit 3, with weak/strong examples.
3. Revise all six model scripts so every main point has a concrete fictional/sanitized example or evidence point.
4. Remove or replace all broken PNG image references.
5. Update `plan3_image_register.json` so path logic and statuses match the paused/rejected asset state.
6. Run Business Presentation Specialist review first over the repaired examples/models.
7. Integrate business/context findings.
8. Run Language Editor review last.
9. Rerun Phase 6 QA row by row.

## Current Release Decision

Do not proceed to final DOCX/PDF production. Phase 6 should remain open with multiple Repair and Defer items.
