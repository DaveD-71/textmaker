# Textmaker Structured Memory

This directory is the repository-visible structured-memory layer for Textmaker. It supplements the
legacy root memory during a controlled migration; it does not replace or silently rewrite history.

## Authority during the pilot

- `../project-learning.md` remains authoritative legacy durable memory.
- `../project-journal.md` remains authoritative chronological evidence.
- `registry.yaml` declares sources, scope, lifecycle, and authority.
- `current-state.md` is the compact repository restart summary.
- `workstreams/<scope-id>/current-state.md` is the compact workstream restart summary.
- Significant durable records use Markdown with YAML front matter and stable UUIDv7 IDs.
- Material accountability events use bounded JSONL session streams under `events/<year>/<month>/`.
- SQLite/FTS5 output is generated outside this repository and is never authoritative.

When a durable record is promoted from legacy memory, retain a `derived_from` relationship or
source reference and identify which representation governs future updates. Do not edit two
authoritative copies of the same decision independently.

## Authoring boundary

Create a standalone Markdown/YAML record only when information needs stable identity,
relationships, supersession, synchronization, or an independent lifecycle. Routine actions remain
events or journal evidence. JSONL is for material events, not the explanatory body of a decision.

Do not store transcripts, hidden reasoning, credentials, routine commands, or large tool output.

## Validation

The implementation and validation tools live in the separate `memory` implementation repository.
During the pilot, validate structured records and events against the schemas in `schema/`, then
rebuild the disposable index from both legacy and structured sources.

## Pilot scope

The first full workstream pilot is `speaking-with-powerpoint`. Existing project content and control
artifacts remain in `books/Speaking with PowerPoint/`; this directory stores memory and references,
not duplicate manuscript or production files.
