---
schema_version: 1
id: 01a0e328-4365-7693-8a90-ec9ca65dd94d
record_type: decision
scope_ids:
  - shared-pipeline
  - speaking-with-powerpoint
status: accepted
created_at: 2026-09-27T22:57:09.3959493+09:00
created_device_id: dev-01a0e327-e642-7c35-9db6-66e47c562356
created_clone_id: clone-01a0e327-e642-79f5-afc9-cc04481cc1aa
created_session_id: ses-01a0e327-e642-75ed-ad0c-4725d0b48c30
historical_occurred_on: 2026-09-14
legacy_source_refs:
  - path: project-journal.md
    line: 41
tags: [pipeline, cli, isolation]
---

# Keep Speaking with PowerPoint Pipeline Behavior Opt-In

## Decision

Speaking with PowerPoint page setup, heading-page-break handling, and list-style behavior must be
activated by explicit SWP flags. Shared Textmaker defaults must remain neutral for other projects.

## Rationale

Textmaker serves multiple books. Requiring every non-SWP project to opt out of SWP behavior reverses
the correct ownership boundary and risks invisible layout changes elsewhere.
