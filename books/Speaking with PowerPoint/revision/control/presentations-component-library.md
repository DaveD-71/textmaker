# Presentations Textbook Component Library

Purpose: define the repeatable components needed to build the learner textbook, teacher notes, and DOCX production system for the presentation-skills textbook.

This library is intentionally broader than the Markdown manuscript. The Markdown files supply the content structure, but final DOCX production must also create page-level, navigation, layout, and print components that do not naturally exist in Markdown.

Working reference files:

- `books/Speaking with PowerPoint/revision/control/presentations-style-set.md`
- `books/Speaking with PowerPoint/revision/control/presentations_style.yaml`
- `books/Speaking with PowerPoint/revision/control/plan3.md`
- `books/Speaking with PowerPoint/revision/control/plan3-phase6-qa-checklist.md`

## Component Groups

### 1. Book-Level Production Components

| ID | Component | Needed for |
|---|---|---|
| B-001 | Front cover | Learner textbook cover, final PDF/DOCX package |
| B-002 | Back cover | Learner textbook back cover |
| B-003 | Half-title or title page | Front matter |
| B-004 | Copyright and production line | Front matter |
| B-005 | Revision/version line | Print tracking and update control |
| B-006 | Learner introduction | Short learner-facing orientation |
| B-007 | How to use this book | Learner navigation |
| B-008 | Course map / unit overview | Front matter course planning |
| B-009 | Table of contents | Navigation |
| B-010 | Appendix opener | Appendix section division |
| B-011 | Credits/source notes page | Image, template, tool, and source provenance |
| B-012 | Back matter opener | Optional separation before glossary/checklists |

### 2. Page-Level Layout Components

| ID | Component | Needed for |
|---|---|---|
| P-001 | A4 page setup | Base print format |
| P-002 | Margin system | Office printing and possible binding |
| P-003 | Section breaks | Cover, front matter, TOC, units, appendices, teacher notes |
| P-004 | Running header | Unit and appendix navigation |
| P-005 | Footer | Page number and optional short title |
| P-006 | Page number style | Roman/Arabic or continuous numbering |
| P-007 | Header/footer separator rule | Navigation without visual clutter |
| P-008 | Unit page start rule | New-page behavior for units |
| P-009 | Appendix page start rule | New-page behavior for major appendices |
| P-010 | Keep-with-next rule | Prevent headings separated from content |
| P-011 | Widow/orphan control rule | Body text and scripts |
| P-012 | Snap-to-grid disabled rule | Whole document paragraph behavior |
| P-013 | Hyphenation rule | English prose readability |
| P-014 | List hyphenation exception | Lists left-aligned and not hyphenated |
| P-015 | Print-safe color theme | Shared DOCX, slide, and Canva direction |

### 3. Unit Opening Components

| ID | Component | Needed for |
|---|---|---|
| U-001 | Unit number block | Clear unit navigation |
| U-002 | Unit title band | Major unit opener |
| U-003 | Unit subtitle / focus line | Optional unit summary |
| U-004 | Unit learning outcomes box | Start-of-unit objectives |
| U-005 | Unit context starter | Role-agnostic workplace entry point |
| U-006 | Unit deliverable tracker | End goal for the unit |
| U-007 | Unit wrap-up block | Final consolidation |

### 4. Section and Heading Components

| ID | Component | Needed for |
|---|---|---|
| H-001 | Main section heading | Major sections inside units |
| H-002 | Section heading rule | Visual hierarchy and scanning |
| H-003 | Subsection heading | Local content blocks |
| H-004 | Script section heading | Model script internal sections |
| H-005 | Practice task heading | Numbered learner activities |
| H-006 | Speaking task heading | Spoken-output tasks |
| H-007 | Learner deliverable heading | Final unit output |
| H-008 | Appendix model heading | Model presentations |
| H-009 | Teacher notes heading | Separate teacher notes file |

### 5. Activity and Task Components

| ID | Component | Needed for |
|---|---|---|
| A-001 | Practice number marker | Numbered activity identity |
| A-002 | Practice title | Task purpose |
| A-003 | Practice instruction paragraph | Learner-facing task direction |
| A-004 | Activity number + instruction pairing | BR2e-style activity clarity |
| A-005 | Speaking task instruction | Oral production tasks |
| A-006 | Pair/group task variant | Optional classroom format |
| A-007 | One-to-one lesson variant | Private-lesson usability |
| A-008 | Reflection prompt | Self-review |
| A-009 | Learner notes area | Written planning and reflection |
| A-010 | Final task checklist | Unit 12 and final presentation preparation |

### 6. Callout Components

| ID | Component | Needed for |
|---|---|---|
| C-001 | Core skill box | Main presentation skill explanation |
| C-002 | Core concept box | Conceptual foundation |
| C-003 | Useful language box | Phrase banks and spoken patterns |
| C-004 | Model box | Worked examples and short models |
| C-005 | Tip box | Short learner guidance |
| C-006 | Caution box | Confidentiality, overclaiming, accessibility, risk |
| C-007 | AI critical-literacy box | Neutral AI-checking tasks, not AI promotion |
| C-008 | Reflection box | Self-assessment and goal-setting |
| C-009 | Accessibility note box | Visual/audio accessibility guidance |
| C-010 | Privacy/security note box | Confidentiality and data handling |
| C-011 | Bilingual planning note | Japanese-to-English planning awareness |
| C-012 | Pronunciation/intelligibility note | Spoken clarity support |

### 7. Cross-Reference and Navigation Components

| ID | Component | Needed for |
|---|---|---|
| X-001 | Cross-reference line | References to appendices and model presentations |
| X-002 | Unit connection note | Show how appendix models connect to units |
| X-003 | See-also reference | Internal navigation |
| X-004 | Appendix reference tag | Model-set references |
| X-005 | Source/provenance note | Credits and traceability |
| X-006 | Glossary reference marker | First-use or review support |

### 8. Example and Model Text Components

| ID | Component | Needed for |
|---|---|---|
| M-001 | Short spoken model | Unit-level example |
| M-002 | Full spoken presentation script | Appendix model presentations |
| M-003 | Script section label | Opening, body, close, Q&A |
| M-004 | Weak example block | Contrastive learning |
| M-005 | Improved example block | Repair model |
| M-006 | Worked example block | Guided learning |
| M-007 | Q&A model answer | Question-response practice |
| M-008 | Language notes block | Learner-facing phrase/function notes |
| M-009 | Pronunciation notes block | Stress, pausing, emphasis |
| M-010 | Visual notes block | Slide/visual purpose and presenter action |

### 9. Table Components

| ID | Component | Needed for |
|---|---|---|
| T-001 | Phrase bank table | Functions and useful language |
| T-002 | Vocabulary table | Terms, meanings, examples |
| T-003 | Planning table | Learner writing and presentation planning |
| T-004 | Comparison table | Weak/improved, option comparison, repair work |
| T-005 | Checklist table | Readiness and quality checks |
| T-006 | Rubric table | B1/B2 descriptors and final assessment |
| T-007 | Model support table | Appendix visual sequence, Q&A, skill maps |
| T-008 | Quiz table | Unit 12 wrap-up quiz |
| T-009 | Answer key table | Teacher notes |
| T-010 | Course map table | Front matter overview |
| T-011 | Data explanation table | Results/reporting presentation work |
| T-012 | Writable table row | Handwriting space inside tables |

### 10. List Components

| ID | Component | Needed for |
|---|---|---|
| L-001 | Standard bullet list | Non-sequential points |
| L-002 | Nested bullet list | Supporting details |
| L-003 | Numbered list | Chronology, sequence, ranked steps |
| L-004 | Nested numbered list | Substeps under a numbered process |
| L-005 | Checklist list | Readiness and review |
| L-006 | Sequence list with emphasized numbers | Important process sequences |
| L-007 | List-block spacing before | Space before first list item |
| L-008 | List-block spacing after | Space after last list item |
| L-009 | List continuation paragraph | Prose continuing after a list item |
| L-010 | List-to-table conversion rule | When lists are too dense for prose |

### 11. Learner Writing Components

| ID | Component | Needed for |
|---|---|---|
| W-001 | Single fill-in line | Short learner response |
| W-002 | Multi-line writing area | Planning and reflection |
| W-003 | Notes column | Planning/checklist tables |
| W-004 | Drafting space | Slide text or script drafting |
| W-005 | Peer feedback area | Review tasks |
| W-006 | Self-review area | Reflection and Unit 12 |

### 12. Visual and Figure Components

| ID | Component | Needed for |
|---|---|---|
| V-001 | Full-width figure | Major visual examples |
| V-002 | Half-width figure | Smaller supporting visuals |
| V-003 | Inline icon or symbol | Functional navigation only |
| V-004 | Screenshot/mockup frame | Tool-neutral visual examples |
| V-005 | Slide image placeholder | Appendix model slide sets |
| V-006 | Diagram/process figure | Workflow and structure examples |
| V-007 | Chart/data figure | Results and evidence examples |
| V-008 | Figure caption | Learner-facing caption |
| V-009 | Figure source note | Provenance and license note |
| V-010 | Decorative image rule | Mark decorative assets as decorative in accessibility |
| V-011 | Alt-text placeholder | Meaningful image accessibility |

### 13. Appendix Model Components

| ID | Component | Needed for |
|---|---|---|
| AM-001 | Model presentation opener | Appendix model start |
| AM-002 | Scenario brief | Learner context |
| AM-003 | Model metadata panel | Purpose, audience, timing |
| AM-004 | Visual sequence table | Slide/visual plan |
| AM-005 | Key vocabulary table | B1-B2 terminology support |
| AM-006 | Full script section | Learner-facing model script |
| AM-007 | Language notes section | Presentation phrase/function study |
| AM-008 | Pronunciation notes section | Delivery support |
| AM-009 | Q&A practice section | Model responses |
| AM-010 | Skills practised map | Unit-to-model connection |
| AM-011 | Security/privacy/accessibility note | Responsible presentation practice |
| AM-012 | Model slide deck reference | Link/reference to editable PPTX or final slide images |

### 14. Assessment and Review Components

| ID | Component | Needed for |
|---|---|---|
| R-001 | Unit review checklist | Unit wrap-up |
| R-002 | Final presentation checklist | Unit 12 and appendix |
| R-003 | Peer feedback form | Class review |
| R-004 | Self-review form | Individual reflection |
| R-005 | Final rubric | B1/B2 performance expectations |
| R-006 | Textbook wrap-up quiz | Unit 12 timing and consolidation |
| R-007 | Quiz answer key | Teacher notes |
| R-008 | Error-correction key | Teacher notes or self-study if approved |

### 15. Teacher Notes Components

| ID | Component | Needed for |
|---|---|---|
| TN-001 | Teacher notes cover/title | Separate printable document |
| TN-002 | Teaching duration summary | Course planning |
| TN-003 | Unit teacher note block | Unit-specific guidance |
| TN-004 | Appendix teacher note block | Model-use guidance |
| TN-005 | Answer key block | Quiz and controlled practice |
| TN-006 | Client-specific adaptation note | Business/government/private-class adaptation |
| TN-007 | One-to-one timing note | Private lesson planning |
| TN-008 | Terminology watchlist | B1-B2 support |
| TN-009 | Review sequence note | Business specialist before language editor |

### 16. Style-System and QA Components

| ID | Component | Needed for |
|---|---|---|
| S-001 | Theme token sheet | Colors, fonts, rule weights, spacing |
| S-002 | Font specimen | Typeface and fallback QA |
| S-003 | Color swatch specimen | Print and contrast QA |
| S-004 | Rule/line specimen | Standard rule weights |
| S-005 | Callout specimen page | Visual consistency QA |
| S-006 | Table specimen page | Overflow and readability QA |
| S-007 | List specimen page | Numbering, nesting, spacing QA |
| S-008 | Unit opener specimen | Shape/header treatment QA |
| S-009 | Appendix specimen | Model presentation layout QA |
| S-010 | Teacher notes specimen | Separate document QA |
| S-011 | Accessibility QA marker | Alt text, heading order, color contrast |
| S-012 | Source/provenance register link | Asset traceability |

## Priority Build Order

1. Define page-level layout components first: page size, margins, sections, headers, footers, page numbers, and global paragraph settings.
2. Define text hierarchy next: body, headings, unit openers, section heads, task heads, script heads.
3. Define task and callout components: activity number/instruction pairing, core skill boxes, useful language boxes, model boxes, caution/tip/AI/reflection boxes.
4. Define table families and list behavior because these will create most DOCX layout risk.
5. Define appendix model components, especially full script, vocabulary, visual sequence, Q&A, and skill-map treatment.
6. Define teacher notes components separately from learner textbook components.
7. Create specimen pages and run QA before full DOCX assembly.

## Key Production Implications

- The Markdown source cannot be the only guide. It must be mapped into these components during conversion.
- Some components can be represented by paragraph or table styles in `presentations_style.docx`.
- Some components require postprocessing, especially unit opener shapes, section breaks, headers/footers, automatic numbering, list-block spacing, page numbering, table overflow control, and figure placement.
- Some components may need explicit Markdown wrappers before conversion if inference from headings/table headers is too fragile.
- Teacher-facing components must stay in the separate teacher notes document, not in learner-facing units or appendices.
- The component library should remain aligned with `presentations_style.yaml` and the Phase 6 QA checklist.

## Required Specification Fields

Every component family should eventually carry these fields before final DOCX production:

| Field | Purpose |
|---|---|
| Component IDs | Links the detailed family spec to the inventory tables above |
| Source trigger | How the build system recognizes the component from Markdown, metadata, or postprocess rules |
| Target style/component | Word paragraph style, table style, character style, section rule, or generated object |
| Typography | Font family, size, weight, color, line spacing, and casing |
| Geometry | Width, height, padding, indentation, row height, or page placement |
| Spacing | Space before, space after, and keep rules |
| Rule/border/fill | Line weight, color, border side, shading, or background shape |
| Generation method | Reference DOCX style, Pandoc mapping, Lua filter, DOCX postprocess, manual final-layout pass, or external design tool |
| Accessibility | Heading structure, alt text, color contrast, color-not-alone, reading order |
| Specimen requirement | Whether a test/example must appear in the reference DOCX or specimen document |
| QA check | What must be inspected before final export |

## Detailed Component Family Specifications

### A. Page and Section System

Component IDs: `B-001` through `B-012`, `P-001` through `P-015`

| Field | Specification |
|---|---|
| Source trigger | Document metadata, build command options, and final assembly order |
| Target style/component | Word sections, page setup, headers, footers, page numbering fields |
| Typography | Running heads: sans, 10.5-11 pt, single-spaced; page numbers: 11-12 pt; front/back matter body follows `PS Body Text` unless a specific front-matter style is used |
| Geometry | A4 portrait; margins initially top/bottom 18 mm, left/right 17 mm; header/footer from edge 9-10 mm |
| Spacing | No body content should collide with header/footer; first content block on a page should have controlled top spacing |
| Rule/border/fill | Optional thin header/footer rule, 0.5-0.8 pt, Slate or Deep ink tint; avoid heavy color bands on ordinary pages |
| Generation method | DOCX section/postprocess layer; reference DOCX can define styles but cannot fully control section order alone |
| Accessibility | Correct heading order, page numbers outside reading-critical text, no production-only header text that confuses learners |
| Specimen requirement | Include a specimen with front matter, first unit page, interior unit page, appendix page, and teacher-notes page |
| QA check | Check section breaks, page numbering, running heads, margins, print preview, PDF export, and whether covers have no visible page number |

Open decisions:

- Final page-numbering scheme: Roman/front matter plus Arabic/main text, or simple continuous Arabic numbering.
- Cover production method: Word, Canva, or separate PDF artwork.
- Whether teacher notes use the same reference DOCX or a plainer variant generated from the same YAML tokens.

### B. Unit Opener System

Component IDs: `U-001` through `U-007`, `H-001`, `S-008`

| Field | Specification |
|---|---|
| Source trigger | `# Unit N: Title` plus immediately following unit opening material |
| Target style/component | `PS Heading 1`, `PS Unit Number Block`, `PS Unit Title Band`, `PS Unit Subtitle`, `PS Unit Outcomes Box` |
| Typography | Unit number: sans bold 16-18 pt; unit title: sans bold 30-34 pt, title case; subtitle/focus line: sans 12-13 pt; outcomes: body 11 pt with sans label |
| Geometry | Full-width or near-full-width unit title band within margins; number block at left or top-left; outcomes box below title band |
| Spacing | Unit opener starts a new page; 10-12 pt after title band before outcomes or first body block; keep opener components together where possible |
| Rule/border/fill | Deep ink or Professional teal title band; white title text; optional Amber or Business blue accent stripe; outcomes box Teal tint with visible teal top rule |
| Generation method | Likely DOCX postprocess or prototype table/object insertion; ordinary Word heading style alone is not enough |
| Accessibility | Unit title must remain a real Heading 1 in the document structure even if visually placed in a band |
| Specimen requirement | One complete unit opener specimen, including long and short title variants |
| QA check | Confirm title fits, title case is correct, unit starts on new page, outcomes do not split awkwardly, and the heading remains navigable |

### C. Section Heading System

Component IDs: `H-001` through `H-009`, `X-001` through `X-004`

| Field | Specification |
|---|---|
| Source trigger | Markdown `##`, `###`, appendix headings, teacher-notes headings |
| Target style/component | `PS Heading 2`, `PS Heading 3`, `PS Heading 4`, `PS Cross Reference`, appendix/teacher heading styles |
| Typography | Heading 2: sans bold 16 pt teal; Heading 3: sans bold 13.5 pt graphite; Heading 4: sans bold 12 pt slate; all heading styles single-spaced and title case |
| Geometry | Heading 2 receives a full text-column underline rule; lower headings rely on spacing and weight rather than large shapes |
| Spacing | Heading 2: 14-16 pt before, 6 pt after; Heading 3: 10-12 pt before, 4-5 pt after; Heading 4: 8 pt before, 3-4 pt after |
| Rule/border/fill | Heading 2 underline rule: 2-3 pt Professional teal; cross-reference line: 0.8 pt Slate or Business blue |
| Generation method | Reference DOCX styles plus possible postprocess rule for section underline/cross-reference rule |
| Accessibility | All heading-like components should map to real heading levels unless they are labels inside a callout/table |
| Specimen requirement | Heading hierarchy specimen with H1-H4, cross-reference, appendix heading, and teacher heading |
| QA check | Check title case, first word after colon in headings, keep-with-next, no orphaned headings, and TOC inclusion/exclusion |

### D. Activity and Practice Task System

Component IDs: `A-001` through `A-010`, `H-005`, `H-006`, `L-003`, `L-004`, `W-001` through `W-006`

| Field | Specification |
|---|---|
| Source trigger | Headings beginning `Practice`, `Speaking Task`, `Learner Deliverable`, numbered exercise labels, or explicit task wrappers |
| Target style/component | `PS Practice Head`, `PS Practice Number`, `PS Practice Instruction`, `PS Sequence List`, learner-writing components |
| Typography | Practice number: sans bold 11-12 pt; practice title: sans bold 12.5-13.5 pt; instruction: body 11 pt; task verbs may use `PS Task Verb` character style |
| Geometry | Number marker aligned to left edge of text column; instruction starts on same baseline or immediately below depending on length; writing areas must have minimum usable row height |
| Spacing | 10-12 pt before task heading, 5-6 pt after; list blocks get spacing before first item and after last item only |
| Rule/border/fill | Practice number may use small square/capsule in teal with white number; writing areas use white background and visible grey/slate rules |
| Generation method | Markdown heading inference plus DOCX postprocess for number marker/table prototype if needed |
| Accessibility | Activity number and task title must be readable as text, not only decorative shape text |
| Specimen requirement | Practice task specimen with normal instruction, numbered sequence, nested subpoints, writing area, and speaking task |
| QA check | Confirm task number/title/instruction relationship is clear; chronological tasks use numbered lists; subpoints are nested; writing space survives PDF print |

### E. Callout and Box System

Component IDs: `C-001` through `C-012`, `M-004` through `M-006`, `S-005`

| Field | Specification |
|---|---|
| Source trigger | Section labels such as `Core Skill`, `Core Concept`, `Useful Language`, `Tip`, `Caution`, `AI`, `Reflection`, `Accessibility`, `Privacy`, `Pronunciation`; explicit wrappers if inference is unreliable |
| Target style/component | `PS Core Skill Box`, `PS Useful Language Box`, `PS Model Box`, `PS Tip Box`, `PS Caution Box`, `PS AI Literacy Box`, `PS Reflection Box` |
| Typography | Label: sans bold 10.5-12 pt, title case or all caps only where intentional; body: 11 pt body font; dense callout text may use 10.5 pt |
| Geometry | Text-column width unless paired with a table; 3-4 mm internal padding; avoid nested boxes |
| Spacing | 6-8 pt before and after callout block; keep label with first body paragraph |
| Rule/border/fill | Core skill/useful language: Teal tint with teal rule; model: Blue tint/blue left rule; caution/tip: Amber tint/amber rule; AI: light grey/slate, neutral styling |
| Generation method | Reference styles for paragraph look; table/prototype insertion or postprocess may be needed for true boxed layouts |
| Accessibility | Do not rely on color alone; include visible text labels; maintain reading order inside the box |
| Specimen requirement | One page with all callout types, including long body text and a callout followed by a table/list |
| QA check | Check contrast in grayscale, no promotional AI styling, no callout split that leaves label alone at page bottom |

### F. Example and Model Text System

Component IDs: `M-001` through `M-010`, `AM-006` through `AM-009`

| Field | Specification |
|---|---|
| Source trigger | Blockquotes, model/example headings, appendix full-script sections, Q&A sections |
| Target style/component | `PS Block Example`, `PS Spoken Model`, `PS Weak Example`, `PS Improved Example`, `PS Script Text`, `PS Script Section Head`, `PS QA Model Table` |
| Typography | Short examples: body 11 pt; full scripts: body 11 pt with 1.15 line spacing; script section heads: sans bold 12 pt; weak/improved labels: sans bold |
| Geometry | Long scripts should be mostly white for readability; use subtle left rule or heading hierarchy instead of heavy colored boxes |
| Spacing | Script paragraphs need comfortable spacing but not paragraph-by-paragraph gaps; section heads keep with following script text |
| Rule/border/fill | Weak examples use amber cue; improved examples use teal cue; full scripts may use blue or slate left rule |
| Generation method | Markdown wrappers preferred for distinguishing weak/improved/model/script; inference from headings is possible but riskier |
| Accessibility | Preserve model scripts as selectable text; avoid embedding script text in images |
| Specimen requirement | Short model, weak/improved pair, full script excerpt, Q&A table |
| QA check | Check B1-B2 readability, first-use vocabulary support, script timing labels, and no teacher-facing notes in learner scripts |

### G. Table System

Component IDs: `T-001` through `T-012`, `S-006`

| Field | Specification |
|---|---|
| Source trigger | Markdown table header patterns, explicit table wrappers if needed |
| Target style/component | `PS Phrase Bank Table`, `PS Vocabulary Table`, `PS Planning Table`, `PS Comparison Table`, `PS Checklist Table`, `PS Rubric Table`, `PS Model Support Table`, `PS Quiz Table` |
| Typography | Header: sans bold 10.5-11 pt, white or deep ink depending on fill; body: 10.5-11 pt; writable tables should not drop below 10.5 pt unless unavoidable |
| Geometry | 100% text-column width by default; fixed or proportional column rules by table family; planning/writable rows need added height |
| Spacing | 6 pt before and after tables; captions/source notes use `PS Caption`; avoid tight table-to-heading collisions |
| Rule/border/fill | Header fills vary by family: teal for phrase banks, graphite/slate for vocabulary/quiz, blue for model support; body uses white/light grey alternating rows; hairline rules 0.5-0.8 pt |
| Generation method | Reference DOCX table styles plus postprocess to enforce width, header row, cell margins, and family mapping |
| Accessibility | Repeat header rows where tables split; avoid merged cells unless necessary; add text labels such as Weak/Improved rather than color-only status |
| Specimen requirement | One specimen table for each family, including a wide/overflow stress test |
| QA check | Check table fits portrait A4, header row formatting, no text below 10 pt, writable areas are usable, and long phrase-bank entries do not crowd |

Suggested table-family mapping:

| Header pattern | Target family |
|---|---|
| `Function | Useful language` | `PS Phrase Bank Table` |
| `Term | Simple meaning` | `PS Vocabulary Table` |
| `Question | Your notes` | `PS Planning Table` |
| `Weak... | Improved...` | `PS Comparison Table` |
| `Check | Status` / `Check | Yes / Not yet | Notes` | `PS Checklist Table` |
| `Area | B1 performance | B2 performance` | `PS Rubric Table` |
| `Visual | Purpose | Suggested content` | `PS Model Support Table` |
| `Question | A | B | C` | `PS Quiz Table` |

### H. List and Numbering System

Component IDs: `L-001` through `L-010`, `A-004`, `A-010`, `R-001` through `R-008`

| Field | Specification |
|---|---|
| Source trigger | Markdown bullets, numbered lists, nested list indentation, checklist patterns |
| Target style/component | `PS Bullet List`, `PS Bullet List 2`, `PS Numbered List`, `PS Numbered List 2`, `PS Checklist`, `PS Sequence List` |
| Typography | 11 pt body font for learner-facing lists; 10.5 pt acceptable in dense tables/teacher notes; lists left-aligned |
| Geometry | Level 1 hanging indent about 5 mm; Level 2 hanging indent about 10 mm; sequence list may use a larger emphasized number marker |
| Spacing | Middle list items: 0 pt before/after; list block: 4-6 pt before first item and 6 pt after last item |
| Rule/border/fill | Ordinary lists use simple markers; sequence lists may use teal number markers; checklists use visible box/status marker |
| Generation method | Pandoc list conversion plus Lua/DOCX postprocess for block boundary spacing and possibly numbering-style binding |
| Accessibility | Use real Word lists where possible; do not fake important ordered steps as plain text numbers unless unavoidable |
| Specimen requirement | Bullet, nested bullet, numbered sequence, nested numbered substeps, checklist, sequence list |
| QA check | Confirm chronological/process content is numbered, non-sequential content is bulleted, subpoints are nested, and list text is not justified/hyphenated |

### I. Learner Writing and Worksheet System

Component IDs: `W-001` through `W-006`, `T-003`, `T-005`, `T-012`

| Field | Specification |
|---|---|
| Source trigger | Planning tables, `Your notes`, `My answer`, checklist note columns, fill-in prompts |
| Target style/component | `PS Planning Table`, writable row component, fill-in line component, notes area component |
| Typography | Prompt text: sans/body 10.5-11 pt; learner writing areas usually blank or lightly ruled |
| Geometry | Minimum row height should support handwriting; notes columns wider than status columns; fill-in lines span usable width |
| Spacing | Add breathing room around writing areas; avoid placing a large writing area immediately under a page header |
| Rule/border/fill | White background; visible Slate/Grey rules; no heavy color fill in writing cells |
| Generation method | Table style plus postprocess for row height and cell margins |
| Accessibility | Prompt text must remain connected to the writing area; avoid unlabeled blank lines |
| Specimen requirement | Planning map, short-answer lines, checklist notes, peer-feedback area |
| QA check | Print a sample page and confirm handwriting space is practical |

### J. Figure, Image, and Slide-Asset System

Component IDs: `V-001` through `V-011`, `AM-012`, `X-005`, `S-012`

| Field | Specification |
|---|---|
| Source trigger | Markdown image links, asset register entries, appendix slide-deck references |
| Target style/component | Figure frame, `PS Caption`, source/provenance note, alt-text metadata |
| Typography | Captions/source notes: 9.5 pt body or sans, Slate; figure labels if used: sans bold 10.5-11 pt |
| Geometry | Full-width figures within margins; half-width figures only when text wrapping is controlled; slide images should preserve 16:9 ratio |
| Spacing | 6 pt before figure, 4 pt after image, 6 pt after caption/source note |
| Rule/border/fill | Optional 0.5 pt Slate frame for screenshots; avoid decorative heavy frames |
| Generation method | Markdown image handling plus postprocess for sizing/captions/alt text; editable PPTX decks tracked separately |
| Accessibility | Meaningful figures need alt text; decorative figures should be marked decorative; no important text should exist only inside an image unless separately readable |
| Specimen requirement | Full-width figure, screenshot frame, diagram, chart, slide image placeholder, caption/source note |
| QA check | Check image resolution, print sharpness, license/provenance, alt text, caption placement, and no missing files |

### K. Appendix Model System

Component IDs: `AM-001` through `AM-012`, `M-002`, `T-007`, `V-005`

| Field | Specification |
|---|---|
| Source trigger | Appendix model Markdown files and model-set headings |
| Target style/component | `PS Appendix Title`, `PS Model Title`, `PS Scenario Brief`, `PS Model Metadata`, `PS Visual Sequence Table`, `PS Full Script Text`, `PS QA Model Table` |
| Typography | Appendix title: sans bold 22-26 pt; model title: sans bold 16-18 pt; full script: body 11 pt; vocabulary/support tables: 10.5-11 pt |
| Geometry | Each model should open clearly; scenario/metadata should be compact; full script should not be trapped inside a dense colored box |
| Spacing | New page for major appendix; model-to-model spacing should be clear; script sections keep with following paragraph |
| Rule/border/fill | Business blue accent for appendix/model support; use teal only where tying back to core skill is useful |
| Generation method | Reference styles plus postprocess/table-family mapping |
| Accessibility | Models are learner-facing; all teacher/editor notes remain outside learner appendix |
| Specimen requirement | One complete model spread with scenario, vocabulary, visual sequence, full script, language notes, Q&A, skill map |
| QA check | Check model timing, vocabulary support, government/business parity, first-use terms, and no role-specific claims in main textbook cross-references |

### L. Teacher Notes System

Component IDs: `TN-001` through `TN-009`, `T-009`, `R-007`, `R-008`, `S-010`

| Field | Specification |
|---|---|
| Source trigger | `books/Speaking with PowerPoint/revision/drafts/Teacher Notes.md` |
| Target style/component | Teacher notes heading styles, teacher note boxes, answer key tables, timing summary |
| Typography | Plainer print-first styling; body 10.5-11 pt; headings sans bold; avoid decorative learner-textbook treatment |
| Geometry | A4 portrait; efficient density; answer keys should be scannable |
| Spacing | Clear separation between units; compact but not cramped |
| Rule/border/fill | Grey/Slate treatment; avoid learner callout colors unless needed for cross-reference clarity |
| Generation method | Same reference DOCX if feasible, or a teacher-notes variant from the same YAML tokens |
| Accessibility | Teacher notes may be denser but should still preserve heading order and readable tables |
| Specimen requirement | Unit note, answer key, timing summary, terminology watchlist |
| QA check | Confirm no teacher-only content appears in learner manuscript; answer keys match learner tasks |

### M. Style Specimen and QA System

Component IDs: `S-001` through `S-012`

| Field | Specification |
|---|---|
| Source trigger | Reference DOCX generation and specimen build command |
| Target style/component | `presentations_style.docx`, style specimen DOCX/PDF, QA checklist rows |
| Typography | Must demonstrate all defined font families, fallback behavior, heading styles, list styles, table styles, callouts, and captions |
| Geometry | Specimen pages should include realistic long text and overflow cases, not only short perfect examples |
| Spacing | Specimen must expose heading-to-body, list-block, table, figure, and callout spacing |
| Rule/border/fill | Include every rule weight and every major fill color in one controlled page |
| Generation method | YAML reference generation plus scripted specimen Markdown/DOCX conversion |
| Accessibility | Specimen should be checked with Word accessibility checker and visual PDF review |
| Specimen requirement | Required before full textbook DOCX build |
| QA check | Compare specimen output against `presentations-style-set.md`, component library, and QA-123 through QA-132 |

## Component-to-Implementation Matrix

| Component family | Reference DOCX style | Markdown/Pandoc mapping | Lua filter | DOCX postprocess | Manual/design-tool pass |
|---|---:|---:|---:|---:|---:|
| Page and section system | Partial | No | No | Yes | Possible for covers |
| Unit opener system | Partial | Partial | Possible | Yes | Possible |
| Section headings | Yes | Yes | Possible | Possible for rules | No |
| Practice tasks | Partial | Partial | Possible | Yes for markers | No |
| Callout boxes | Partial | Partial | Possible | Yes for true boxes | No |
| Example/model text | Yes | Partial | Possible | Possible | No |
| Table families | Yes | Partial | Possible | Yes | No |
| Lists and numbering | Partial | Yes | Yes for spacing | Yes for numbering/spacing | No |
| Learner writing areas | Partial | Partial | No | Yes | No |
| Figures and captions | Partial | Yes | Possible | Yes | Possible for covers/slides |
| Appendix models | Yes | Partial | Possible | Possible | No |
| Teacher notes | Yes or variant | Yes | Possible | Possible | No |
| Specimen/QA | Yes | Yes | Yes | Yes | No |

## Build-Ready Definition

The component library is build-ready only when:

1. Every component family above has at least one specimen.
2. Every required style exists in `presentations_style.yaml`.
3. Every component that cannot be represented by a Word style has a named postprocess or manual production rule.
4. Table-family mapping has been tested on real manuscript tables.
5. List-block spacing has been tested on ordinary lists, nested lists, and lists inside callouts or tables.
6. Unit opener and appendix opener treatments have been tested in rendered DOCX/PDF output.
7. The learner textbook and teacher notes can be generated without moving teacher-facing content into learner-facing pages.
8. QA rows `QA-123` through `QA-132` can be answered from concrete files, not assumptions.
