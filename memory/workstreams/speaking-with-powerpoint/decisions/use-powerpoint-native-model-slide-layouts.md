---
schema_version: 1
id: 01a0e328-4365-7ed6-9efe-931228adc890
record_type: decision
scope_ids:
  - speaking-with-powerpoint
status: accepted
created_at: 2026-09-27T22:57:09.3959493+09:00
created_device_id: dev-01a0e327-e642-7c35-9db6-66e47c562356
created_clone_id: clone-01a0e327-e642-79f5-afc9-cc04481cc1aa
created_session_id: ses-01a0e327-e642-75ed-ad0c-4725d0b48c30
historical_occurred_on: 2026-08-13
legacy_source_refs:
  - path: project-learning.md
    line: 74
  - path: project-journal.md
    line: 1145
relationships:
  - type: supersedes
    target_id: 01a0e328-4365-7864-8fe8-829c9386efaa
tags: [slides, powerpoint, approved-direction]
---

# Use PowerPoint-Native Model-Slide Layouts

## Decision

Build model-presentation slide sets with standard PowerPoint-native layouts and placeholders so
PowerPoint Designer can improve them. Use normal layout hierarchy to express one or two emphasis
points instead of bespoke boxes, arrows, and handmade graphic systems.

## Supersession

This replaces the rejected generated-PNG/custom-shape direction while preserving that earlier
decision as historical evidence.
