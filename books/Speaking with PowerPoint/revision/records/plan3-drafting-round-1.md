# Plan 3 Drafting Round 1

Date: 2026-08-12

Purpose: durable record for the first concurrent drafting round for Standard Unit drafts.

## Drafting Scope

Tier: Standard only.

Output folder:

- `books/Speaking with PowerPoint/revision/drafts/standard/`

Source control files:

- `books/Speaking with PowerPoint/revision/control/plan3.md`
- `books/Speaking with PowerPoint/revision/control/standard-12-unit-curriculum-spec.md`
- `books/Speaking with PowerPoint/revision/control/plan3-style-sheet.md`
- `books/Speaking with PowerPoint/revision/control/plan3-case-model-brief.md`
- `books/Speaking with PowerPoint/revision/control/plan3-traceability.md`
- `books/Speaking with PowerPoint/revision/control/plan3-phase6-qa-checklist.md`
- `books/Speaking with PowerPoint/revision/control/standard-unit-1-drafting-package.md`

## Shared Drafting Rules

- Write learner-facing Standard-tier material unless teacher notes are explicitly requested.
- Follow the Standard tier voice guide from `books/Presentation Skills/canon/voice-S.md`.
- Keep the main unit body role-agnostic between business-client and government-agency contexts.
- Put role-specific references in short model references, appendix references, or optional examples.
- Do not promote AI as a replacement for English development.
- Do not create trade recommendations, market predictions, regulatory advice, client/account examples, or confidential data.
- Use fictional data only unless the final Content Architect later adds a verified source.
- Include spoken English output in visual/tool/data Units.
- Keep Units B1-B2 appropriate with scaffolding, sentence frames, and constrained tasks.

## Agent Assignments

| Agent Role | Units | Output Files | Status |
|---|---|---|---|
| Drafting Agent A / Hegel | 1-3 | `standard-unit-01.md`, `standard-unit-02.md`, `standard-unit-03.md` | completed |
| Drafting Agent B / Hume | 4-6 | `standard-unit-04.md`, `standard-unit-05.md`, `standard-unit-06.md` | completed |
| Drafting Agent C / Faraday | 7-9 | `standard-unit-07.md`, `standard-unit-08.md`, `standard-unit-09.md` | completed |
| Drafting Agent D / Heisenberg | 10-12 | `standard-unit-10.md`, `standard-unit-11.md`, `standard-unit-12.md` | completed |

## Agent Run Log

| Agent | Agent ID | Assignment | Result | Files Changed |
|---|---|---|---|---|
| Drafting Agent A | `019ff4c5-1709-78c1-8969-957af43f6265` | Initial Unit 1-3 draft assignment was sent before the terminology correction was complete. | Interrupted and stopped. Agent reported: "Stopped. I have not created or edited any files in this turn. No drafting will continue until you reassign the task with corrected `Unit` terminology." | None |
| Drafting Agent A / Hegel | `019ff4ce-ac89-7111-9c16-2914fada02c6` | Draft Standard Units 1-3 using corrected Unit terminology and shared drafting brief. | Completed. Noted that Units 1-3 need later cross-unit consistency review after Units 4-12 exist; appendix/model references are intentionally short; Unit 2 keeps AI as critical literacy only. | `standard-unit-01.md`, `standard-unit-02.md`, `standard-unit-03.md` |
| Drafting Agent B / Hume | `019ff4ce-d241-7631-9f90-14afc73f5509` | Draft Standard Units 4-6 using corrected Unit terminology and shared drafting brief. | Completed. Noted that Unit 5 includes AI only as optional critical-literacy critique; Unit 6 uses fictional data and explicit finance/trading guardrails. | `standard-unit-04.md`, `standard-unit-05.md`, `standard-unit-06.md` |
| Drafting Agent C / Faraday | `019ff4cf-0010-7fa2-8416-c79d0b721404` | Draft Standard Units 7-9 using corrected Unit terminology and shared drafting brief. | Completed. Noted that Units 7 and 9 are content-rich and may need later compression; Unit 9 keeps async feasible for Standard and leaves deeper production practice for Long. | `standard-unit-07.md`, `standard-unit-08.md`, `standard-unit-09.md` |
| Drafting Agent D / Heisenberg | `019ff4cf-25cb-7e30-8e8b-6779d308ea5c` | Draft Standard Units 10-12 using corrected Unit terminology and shared drafting brief. | Completed. Noted that Unit 12 needed a fixed final presentation time; Content Architect set Standard default to 5-7 minutes plus required Q&A, unless locally adjusted. | `standard-unit-10.md`, `standard-unit-11.md`, `standard-unit-12.md` |

## Content Architect Integration Notes

- Added `standard-unit-drafting-brief.md` as the shared drafting-control artifact for this and future rounds.
- Removed obsolete terminology policing from future-facing agent brief after the Unit terminology cleanup was locked in.
- Set the Standard final delivery target at 5-7 minutes plus required Q&A in the curriculum spec and Units 11-12.

## Integration Plan

After agents return:

1. Save or merge draft outputs into the listed files.
2. Record returned agent findings and changed files in this record.
3. Run AI-policy, role-agnostic, and finance/government guardrail checks.
4. Run a Content Architect pass before any specialist review.
