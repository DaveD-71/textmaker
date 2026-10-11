# Textmaker Repository Current State

Last verified: 2026-10-11T20:00:48.5906907+09:00  
Verified Git baseline: `e53f523703382f5858a8639927c5fab6c5c1e81d`

## Purpose

Textmaker contains shared document-production tooling and several substantial book/course
workstreams. Project-specific detail remains owned by the relevant workstream; shared pipeline
decisions remain repository or `shared-pipeline` scoped.

## Active state

- The root legacy memory remains authoritative during the structured-memory pilot.
- The approved scope vocabulary is in `memory-scopes.yaml`.
- The first structured-memory workstream pilot is `speaking-with-powerpoint`.
- Recent legacy chronology also includes active Let's Talk Finance production work; the pilot choice
  does not make that workstream inactive or subordinate.
- Shared DOCX behavior must remain opt-in when it is specific to one book. Speaking with PowerPoint
  flags must not silently change other Textmaker projects.

## Constraints

- Do not move, split, delete, or rewrite `project-learning.md` or `project-journal.md` during scaffold initialization.
- Do not duplicate authoritative manuscript, plan, QA, register, or implementation content into memory records.
- Use repository-relative artifact references and preserve historical absolute paths as evidence.
- Multi-scope decisions must remain retrievable through every co-owning scope.
- Generated SQLite is disposable and must remain outside Git authority.

## Restart point

Revalidate the structured-memory pilot for `speaking-with-powerpoint` against the refreshed Git
baseline, then rebuild and test the combined legacy/structured index. The representative record
set and first bounded JSONL event stream already exist.

See `workstreams/speaking-with-powerpoint/current-state.md` for the content-production state.
