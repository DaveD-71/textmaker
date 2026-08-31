# Plan 3 DOCX Style-Tag Audit

Date: 2026-08-31

Scope: current text-first Speaking with PowerPoint DOCX draft generated from `revision/output/docx-draft/swp-standard-text-first-draft.md`.

## Source of Truth

The broad element inventory was already created in `revision/control/presentations-component-library.md`. The DOCX style system is defined in `revision/control/presentations_style.yaml` and summarized in `revision/control/presentations-style-set.md`.

The missing implementation layer was the style-tag bridge. The manuscript used ordinary Markdown headings, labels, blockquotes, lists, and tables, so Pandoc applied standard Word heading/body styles unless Textmaker or postprocessing remapped them.

## Current Build Mechanism

Use Textmaker, not direct Pandoc:

```powershell
textmaker.cmd markdown-to-docx `
  --input "books\Speaking with PowerPoint\revision\output\docx-draft\swp-standard-text-first-draft.md" `
  --output "books\Speaking with PowerPoint\revision\output\docx-draft\swp-standard-text-first-draft.docx" `
  --reference "books\Speaking with PowerPoint\revision\control\presentations_style.docx" `
  --lua-filter "scripts\style_bridge.lua" `
  --swp-style-tags
```

`--swp-style-tags` is a style-only preprocessing option. It converts Markdown headings, standalone component labels, and blockquote model/example blocks into silent Div classes before DOCX conversion. It does not insert visible labels.

## Applied Style Families

Latest generated DOCX paragraph-style counts:

| Style | Count |
|---|---:|
| `PS Bullet List` | 582 |
| `PS Body Text` | 542 |
| `PS Numbered List` | 137 |
| `PS Section Label` | 131 |
| `PS Section Head` | 105 |
| `PS Heading 3` | 93 |
| `PS Practice Head` | 40 |
| `PS Heading 4` | 27 |
| `PS Heading 1` | 12 |
| `PS Unit Outcomes Box` | 12 |
| `PS Learner Deliverable Head` | 12 |
| `PS Language Notes` | 10 |
| `PS Speaking Task Head` | 9 |
| `PS Block Example` | 7 |
| `PS Pronunciation Note Box` | 6 |
| `PS Caution Box` | 5 |
| `PS Accessibility Note Box` | 5 |
| `PS Appendix Title` | 5 |
| `PS Privacy Security Note Box` | 4 |
| `PS Spoken Model` | 3 |
| `PS Front Matter Title` | 2 |
| `PS Presenter Notes` | 2 |
| `PS Visual Notes` | 2 |
| `PS Weak Example` | 1 |
| `PS AI Literacy Box` | 1 |
| `PS Bilingual Planning Note` | 1 |

Non-PS styles with visible text:

| Style | Count | Reason |
|---|---:|---|
| `Title` | 1 | Pandoc metadata title |
| `Subtitle` | 1 | Pandoc metadata subtitle |

Blank structural paragraphs may still use `Normal`; no visible learner content was found in `Normal`.

Latest generated DOCX table-style counts:

| Style | Count |
|---|---:|
| `PS Comparison Table` | 47 |
| `PS Model Support Table` | 17 |
| `PS Vocabulary Table` | 16 |
| `PS Checklist Table` | 16 |
| `PS Phrase Bank Table` | 5 |
| `PS QA Model Table` | 5 |
| `PS Planning Table` | 4 |
| `PS Visual Sequence Table` | 3 |
| `PS Rubric Table` | 1 |

## Remaining Style-Tag Limits

- Page-only production objects still need separate generation rules: covers, custom contents page, unit opener shapes, final front/back matter, figure placement, and future visual assets.
- Some component families currently use paragraph-style approximations rather than full boxed/table prototypes. This is acceptable for the text-first draft but should be inspected in the rendered DOCX/PDF before final layout.
- The automatic Pandoc TOC is not required. A custom contents component can be built later.

## Validation

- Textmaker `markdown-to-docx` build completed with `--swp-style-tags`.
- `scripts/validate_docx_against_reference.py` passed against `presentations_style.docx`.
- Current generated DOCX has zero visible-body uses of standard Word `Heading 1`, `Heading 2`, `Heading 3`, or `Heading 4`.
- Current generated DOCX has 13 sections after unit boundary insertion.
