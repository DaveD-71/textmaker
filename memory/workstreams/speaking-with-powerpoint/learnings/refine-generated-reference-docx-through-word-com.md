---
schema_version: 1
id: 01a0e328-4365-77dc-9d2a-d28bd4700ddf
record_type: learning
scope_ids:
  - speaking-with-powerpoint
  - shared-pipeline
status: active
created_at: 2026-09-27T22:57:09.3959493+09:00
created_device_id: dev-01a0e327-e642-7c35-9db6-66e47c562356
created_clone_id: clone-01a0e327-e642-79f5-afc9-cc04481cc1aa
created_session_id: ses-01a0e327-e642-75ed-ad0c-4725d0b48c30
historical_occurred_on: 2026-08-14
legacy_source_refs:
  - path: project-learning.md
    line: 399
tags: [docx, word-com, table-styles]
---

# Refine Generated Reference DOCX Files Through Word COM

## Learning

After generating `presentations_style.docx` from the YAML style source, run
`scripts/refine_presentations_reference_docx.py` with Word COM normalization. This supplies table
style conditions and package normalization that the base generator alone does not reliably retain.

## Reuse boundary

The technique belongs to both the Speaking with PowerPoint workstream and the shared pipeline, but
book-specific styling or page behavior must remain explicitly opt-in.
