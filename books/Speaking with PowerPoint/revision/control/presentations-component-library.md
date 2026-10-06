# Presentations Textbook Component Library

Purpose: define the repeatable components needed to build the learner textbook, teacher notes, and DOCX production system for the presentation-skills textbook.

This library is intentionally broader than the Markdown manuscript. The Markdown files supply the content structure, but final DOCX production must also create page-level, navigation, layout, and print components that do not naturally exist in Markdown.

Working reference files:

- `books/Speaking with PowerPoint/revision/control/presentations-style-set.md`
- `books/Speaking with PowerPoint/revision/control/presentations_style.yaml`
- `books/Speaking with PowerPoint/revision/control/plan3.md`
- `books/Speaking with PowerPoint/revision/control/plan3-phase6-qa-checklist.md`

## Component Groups

### Text-Use Categories

Every component table below now carries a **Type** column — a reductive set of categories describing how the text is actually used in the book, independent of which of the 16 structural groups it sits in. These categories are the basis for the font/weight/color style system (see `presentations-style-set.md`): each learner-facing Type gets its own typographic treatment, while `Production/Layout` marks page-, paragraph-, and list-level mechanics that carry no distinct text-use identity of their own.

| Type | Description | Font Family | Weight | Size |
|---|---|---|---|---|
| Headings & Navigation | Titles, unit/section headings, cross-references, contents/course-map entries, appendix reference tags | Noto Sans | SemiBold | 12–34 pt (varies by heading level; see Section B/C detailed specs) |
| Body Prose | Ordinary running explanation: core-skill/concept boxes, scenario briefs, unit outcomes, data explanation | Noto Serif | Regular | 11 pt |
| Instruction/Direction | Task/practice instructions, activity directions, presenter-action notes | Noto Sans | Medium | 11 pt |
| Language Sample/Model | Spoken models, scripts, weak/improved/worked examples, Q&A model answers, model-support tables | Noto Serif | Regular | 11 pt |
| Target Vocabulary | Vocabulary tables, phrase banks, key-vocabulary/language-notes, glossary markers | Noto Sans | Regular (Medium for headwords) | 10.5–11 pt |
| Advice | Tips, cautions, AI-literacy, accessibility, privacy, pronunciation, and other forward-looking guidance the learner applies while preparing or presenting | Noto Serif | Regular | 11 pt |
| Reflection | Self-assessment, goal-setting, and other backward-looking review prompts the learner completes after an activity or presentation | Noto Serif | Regular | 11 pt |
| Reference Table | Checklists, rubrics, quizzes, comparison tables, review/assessment forms | Noto Sans | Regular | 10.5–11 pt |
| Learner Writing | Fill-in lines, writing areas, notes columns, planning tables, peer/self-review areas | Noto Sans | Regular | 10.5–11 pt |
| Captions/Metadata | Copyright/production lines, source/provenance notes, figure captions, model metadata panels | Noto Sans | Regular | 9–9.5 pt |
| Teacher-Facing | Content that lives only in the separate Teacher Notes document | Noto Serif | Regular | 10.5–11 pt |
| Production/Layout | Page/paragraph/list mechanics with no distinct text-use category of their own (page setup, section breaks, list spacing, style specimens) | N/A | N/A | N/A |

**Font policy logic:** follows the same discipline confirmed in the Business Result 2e style system (`br2e_data.py`) — two core families carry nearly all the hierarchy. **Noto Sans** is used for structural/label text that is scanned rather than read continuously (headings, instructions, vocabulary headwords, table content, captions). **Noto Serif** is used for continuous reading prose (body explanation, spoken models/scripts, callout body text, teacher notes). Weight and, later, color are what distinguish Types that share a family — e.g. Headings & Navigation (Sans/SemiBold) vs. Instruction/Direction (Sans/Medium) vs. Reference Table (Sans/Regular). `Production/Layout` has no text-use identity, so it carries no font policy; its rows stay `N/A`. Per-heading-level sizes and any Type-specific exceptions remain in the Detailed Component Family Specifications below. Font **color**, plus any other remaining style settings, will be added to the 16 component-group tables below in a follow-up pass.

**Manuscript Count columns added 2026-09-22.** Counts come from a mechanical scan of all 12 Standard unit files, the 3 appendix model-script files, the appendix slide-design checklist, and `Teacher Notes.md` (scanned separately), using heading text, blockquote/label pattern matching, table-header pattern matching, and list-block detection — the same trigger logic `--swp-style-tags` uses in `scripts/cli.py`. See "Manuscript Frequency Findings" at the end of this file for methodology, caveats, and the long-tail content the current 16-group taxonomy does not cleanly capture. Component IDs are a many-to-one/one-to-many mapping onto scanner categories, not a 1:1 map — a single scanner category (e.g. a script's "Visual Notes" table) can satisfy two or three catalog IDs at once, and several catalog IDs (page/book/style-system rules) describe DOCX production behavior that has no Markdown-detectable footprint at all and is correctly `0`.

### 1. Book-Level Production Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| B-001 | Front cover | Production/Layout | Learner textbook cover, final PDF/DOCX package | 0 |
| B-002 | Back cover | Production/Layout | Learner textbook back cover | 0 |
| B-003 | Half-title or title page | Production/Layout | Front matter | 0 |
| B-004 | Copyright and production line | Captions/Metadata | Front matter | 0 |
| B-005 | Revision/version line | Captions/Metadata | Print tracking and update control | 0 |
| B-006 | Learner introduction | Body Prose | Short learner-facing orientation | 0 |
| B-007 | How to use this book | Instruction/Direction | Learner navigation | 0 |
| B-008 | Course map / unit overview | Headings & Navigation | Front matter course planning | 0 |
| B-009 | Table of contents | Headings & Navigation | Navigation | 0 |
| B-010 | Appendix opener | Headings & Navigation | Appendix section division | 4 |
| B-011 | Credits/source notes page | Captions/Metadata | Image, template, tool, and source provenance | 0 |
| B-012 | Back matter opener | Headings & Navigation | Optional separation before glossary/checklists | 0 |

Front-matter items (B-001–B-009, B-011, B-012) do not exist yet as manuscript content — they are page/production objects to be built directly in DOCX, not inferred from Markdown. B-010 (4) is the 4 appendix files, each opening with one H1.

### 2. Page-Level Layout Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| P-001 | A4 page setup | Production/Layout | Base print format | 0 |
| P-002 | Margin system | Production/Layout | Office printing and possible binding | 0 |
| P-003 | Section breaks | Production/Layout | Cover, front matter, TOC, units, appendices, teacher notes | 0 |
| P-004 | Running header | Production/Layout | Unit and appendix navigation | 0 |
| P-005 | Footer | Production/Layout | Page number and optional short title | 0 |
| P-006 | Page number style | Production/Layout | Roman/Arabic or continuous numbering | 0 |
| P-007 | Header/footer separator rule | Production/Layout | Navigation without visual clutter | 0 |
| P-008 | Unit page start rule | Production/Layout | New-page behavior for units | 0 |
| P-009 | Appendix page start rule | Production/Layout | New-page behavior for major appendices | 0 |
| P-010 | Keep-with-next rule | Production/Layout | Prevent headings separated from content | 0 |
| P-011 | Widow/orphan control rule | Production/Layout | Body text and scripts | 0 |
| P-012 | Snap-to-grid disabled rule | Production/Layout | Whole document paragraph behavior | 0 |
| P-013 | Hyphenation rule | Production/Layout | English prose readability | 0 |
| P-014 | List hyphenation exception | Production/Layout | Lists left-aligned and not hyphenated | 0 |
| P-015 | Print-safe color theme | Production/Layout | Shared DOCX, slide, and Canva direction | 0 |

All of Group 2 is `0` by definition: these are page/paragraph production rules with no Markdown representation. They already exist as DOCX/postprocess behavior (see `presentations_style.yaml` and `postprocess_docx.py`), not as manuscript content to count.

### 3. Unit Opening Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| U-001 | Unit number block | Headings & Navigation | Clear unit navigation | 12 |
| U-002 | Unit title band | Headings & Navigation | Major unit opener | 12 |
| U-003 | Unit subtitle / focus line | Headings & Navigation | Optional unit summary | 0 |
| U-004 | Unit learning outcomes box | Body Prose | Start-of-unit objectives | 12 |
| U-005 | Unit context starter | Body Prose | Role-agnostic workplace entry point | 0 |
| U-006 | Unit deliverable tracker | Instruction/Direction | End goal for the unit | 12 |
| U-007 | Unit wrap-up block | Advice | Final consolidation | 12 |

12 units, so every genuinely-used unit-opener component scores exactly 12 (one per unit) — U-001/U-002 are one H1 each, U-004 is the "by the end of this unit" outcomes intro, U-006 is the Learner Deliverable heading, U-007 is the unit's closing block. U-003 and U-005 are not distinct Markdown-detectable elements in the current drafts (folded into the unit opener prose).

### 4. Section and Heading Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| H-001 | Main section heading | Headings & Navigation | Major sections inside units | 16 |
| H-002 | Section heading rule | Production/Layout | Visual hierarchy and scanning | 0 |
| H-003 | Subsection heading | Headings & Navigation | Local content blocks | 33 |
| H-004 | Script section heading | Headings & Navigation | Model script internal sections | 27 |
| H-005 | Practice task heading | Headings & Navigation | Numbered learner activities | 40 |
| H-006 | Speaking task heading | Headings & Navigation | Spoken-output tasks | 9 |
| H-007 | Learner deliverable heading | Headings & Navigation | Final unit output | 12 |
| H-008 | Appendix model heading | Headings & Navigation | Model presentations | 6 |
| H-009 | Teacher notes heading | Teacher-Facing | Separate teacher notes file | 17 |

H-009 (17) is from the separate `Teacher Notes.md` scan. H-002 is a rule/underline style, not manuscript content, so `0`.

### 5. Activity and Task Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| A-001 | Practice number marker | Instruction/Direction | Numbered activity identity | 40 |
| A-002 | Practice title | Headings & Navigation | Task purpose | 40 |
| A-003 | Practice instruction paragraph | Instruction/Direction | Learner-facing task direction | 40 |
| A-004 | Activity number + instruction pairing | Instruction/Direction | BR2e-style activity clarity | 40 |
| A-005 | Speaking task instruction | Instruction/Direction | Oral production tasks | 9 |
| A-006 | Pair/group task variant | Instruction/Direction | Optional classroom format | 5 |
| A-007 | One-to-one lesson variant | Teacher-Facing | Private-lesson usability | 2 |
| A-008 | Reflection prompt | Reflection | Self-review | 1 |
| A-009 | Learner notes area | Learner Writing | Written planning and reflection | 2 |
| A-010 | Final task checklist | Reference Table | Unit 12 and final presentation preparation | 1 |

A-001/A-002/A-003/A-004 all key off the same 40 "Practice N" headings — every practice head carries a number, a title, and an instruction paragraph, so all four legitimately share one count. A-006 (5) and A-007 (2, from Teacher Notes) are explicit textual mentions of the classroom-format variant, not a count of every activity that could theoretically be run that way. A-008/A-009's low counts (1–2) are a real finding: reflection and personal-notes prompts appear as one-off blocks, mostly folded into unit wrap-ups (U-007) and the standalone-label long tail (see Findings), not as a separately tagged, repeatable component.

### 6. Callout Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| C-001 | Core skill box | Body Prose | Main presentation skill explanation | 4 |
| C-002 | Core concept box | Body Prose | Conceptual foundation | 9 |
| C-003 | Useful language box | Target Vocabulary | Phrase banks and spoken patterns | 22 |
| C-004 | Model box | Language Sample/Model | Worked examples and short models | 13 |
| C-005 | Tip box | Advice | Short learner guidance | 0 |
| C-006 | Caution box | Advice | Confidentiality, overclaiming, accessibility, risk | 5 |
| C-007 | AI critical-literacy box | Advice | Neutral AI-checking tasks, not AI promotion | 3 |
| C-008 | Reflection box | Reflection | Self-assessment and goal-setting | 1 |
| C-009 | Accessibility note box | Advice | Visual/audio accessibility guidance | 5 |
| C-010 | Privacy/security note box | Advice | Confidentiality and data handling | 4 |
| C-011 | Bilingual planning note | Advice | Japanese-to-English planning awareness | 1 |
| C-012 | Pronunciation/intelligibility note | Advice | Spoken clarity support | 6 |

C-005 Tip Box never occurs as a distinctly labeled component in the current manuscript — `0`, a real candidate for dropping or merging into C-002. C-008 and C-011 are also singletons.

### 7. Cross-Reference and Navigation Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| X-001 | Cross-reference line | Headings & Navigation | References to appendices and model presentations | 8 |
| X-002 | Unit connection note | Headings & Navigation | Show how appendix models connect to units | 5 |
| X-003 | See-also reference | Headings & Navigation | Internal navigation | 0 |
| X-004 | Appendix reference tag | Headings & Navigation | Model-set references | 15 |
| X-005 | Source/provenance note | Captions/Metadata | Credits and traceability | 0 |
| X-006 | Glossary reference marker | Target Vocabulary | First-use or review support | 0 |

X-002's count (5) overlaps with X-001's (8) in the scan data — both key off the same cross-reference sentences, so treat these two as one behavior counted twice rather than 13 independent instances.

### 8. Example and Model Text Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| M-001 | Short spoken model | Language Sample/Model | Unit-level example | 3 |
| M-002 | Full spoken presentation script | Language Sample/Model | Appendix model presentations | 6 |
| M-003 | Script section label | Headings & Navigation | Opening, body, close, Q&A | 27 |
| M-004 | Weak example block | Language Sample/Model | Contrastive learning | 1 |
| M-005 | Improved example block | Language Sample/Model | Repair model | 0 |
| M-006 | Worked example block | Language Sample/Model | Guided learning | 7 |
| M-007 | Q&A model answer | Language Sample/Model | Question-response practice | 6 |
| M-008 | Language notes block | Target Vocabulary | Learner-facing phrase/function notes | 6 |
| M-009 | Pronunciation notes block | Advice | Stress, pausing, emphasis | 6 |
| M-010 | Visual notes block | Instruction/Direction | Slide/visual purpose and presenter action | 6 |

M-004/M-005 (weak/improved) as dedicated blockquote-style divs are nearly absent (1 and 0) — the real weak/improved teaching pattern lives almost entirely in ad hoc comparison tables instead (see T-004 and the T-other tail in Findings), not in M-004/M-005-shaped blocks. This is a genuine mismatch between how the catalog models this pattern and how the manuscript actually implements it.

### 9. Table Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| T-001 | Phrase bank table | Target Vocabulary | Functions and useful language | 5 |
| T-002 | Vocabulary table | Target Vocabulary | Terms, meanings, examples | 16 |
| T-003 | Planning table | Learner Writing | Learner writing and presentation planning | 2 |
| T-004 | Comparison table | Reference Table | Weak/improved, option comparison, repair work | 2 |
| T-005 | Checklist table | Reference Table | Readiness and quality checks | 11 |
| T-006 | Rubric table | Reference Table | B1/B2 descriptors and final assessment | 1 |
| T-007 | Model support table | Language Sample/Model | Appendix visual sequence, Q&A, skill maps | 3 |
| T-008 | Quiz table | Reference Table | Unit 12 wrap-up quiz | 1 |
| T-009 | Answer key table | Teacher-Facing | Teacher notes | 0 |
| T-010 | Course map table | Headings & Navigation | Front matter overview | 0 |
| T-011 | Data explanation table | Body Prose | Results/reporting presentation work | 0 |
| T-012 | Writable table row | Learner Writing | Handwriting space inside tables | 0 |

**Important caveat:** the manuscript contains 113 real Markdown tables total. Only 45 matched one of the fixed header patterns above (T-001–T-008); the other **68 tables each have a unique, unmatched header combination** (e.g. "weak visual / clearer visual," "purpose / best format / reason," "situation / possible format choices"). Most of these are genuinely planning tables (T-003) or comparison tables (T-004) in spirit but with bespoke column headers per activity, which is why T-003/T-004's matched counts (2 each) look implausibly low next to T-002/T-005. See Findings for the recommended fix (broaden the header-pattern match, don't read T-003/T-004 as true low-frequency components).

### 10. List Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| L-001 | Standard bullet list | Production/Layout | Non-sequential points | 564 items / 77 lists |
| L-002 | Nested bullet list | Production/Layout | Supporting details | 18 |
| L-003 | Numbered list | Production/Layout | Chronology, sequence, ranked steps | 133 items / 31 lists |
| L-004 | Nested numbered list | Production/Layout | Substeps under a numbered process | 0 |
| L-005 | Checklist list | Production/Layout | Readiness and review | 0 |
| L-006 | Sequence list with emphasized numbers | Production/Layout | Important process sequences | 0 |
| L-007 | List-block spacing before | Production/Layout | Space before first list item | 0 |
| L-008 | List-block spacing after | Production/Layout | Space after last list item | 0 |
| L-009 | List continuation paragraph | Production/Layout | Prose continuing after a list item | 0 |
| L-010 | List-to-table conversion rule | Production/Layout | When lists are too dense for prose | 0 |

L-001/L-003 are reported as both item count and distinct-list count (a list of 14 bullets is 1 list, not 14) — see Findings for why this distinction matters. L-004–L-006 are genuinely absent as separate Markdown constructs: nested numbering and true "checklist" (`- [ ]`) syntax are not used anywhere in the current drafts (checklists are built as plain tables — see T-005's 11). L-007–L-010 are spacing/production rules, not content, so `0`.

### 11. Learner Writing Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| W-001 | Single fill-in line | Learner Writing | Short learner response | 0 |
| W-002 | Multi-line writing area | Learner Writing | Planning and reflection | 0 |
| W-003 | Notes column | Learner Writing | Planning/checklist tables | 0 |
| W-004 | Drafting space | Learner Writing | Slide text or script drafting | 0 |
| W-005 | Peer feedback area | Learner Writing | Review tasks | 0 |
| W-006 | Self-review area | Learner Writing | Reflection and Unit 12 | 2 |

W-001–W-005 have no dedicated Markdown marker distinguishing them from an ordinary blank table cell or list item — they are physical writing-space allowances that must be built at DOCX production time (row height, ruled lines), not detected from source text, so `0` is correct rather than a scan gap. W-006 (2) is the same "learner notes area" mentions counted under A-009.

### 12. Visual and Figure Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| V-001 | Full-width figure | Production/Layout | Major visual examples | 0 |
| V-002 | Half-width figure | Production/Layout | Smaller supporting visuals | 0 |
| V-003 | Inline icon or symbol | Production/Layout | Functional navigation only | 0 |
| V-004 | Screenshot/mockup frame | Production/Layout | Tool-neutral visual examples | 0 |
| V-005 | Slide image placeholder | Production/Layout | Appendix model slide sets | 0 |
| V-006 | Diagram/process figure | Production/Layout | Workflow and structure examples | 0 |
| V-007 | Chart/data figure | Production/Layout | Results and evidence examples | 0 |
| V-008 | Figure caption | Captions/Metadata | Learner-facing caption | 0 |
| V-009 | Figure source note | Captions/Metadata | Provenance and license note | 0 |
| V-010 | Decorative image rule | Production/Layout | Mark decorative assets as decorative in accessibility | 0 |
| V-011 | Alt-text placeholder | Production/Layout | Meaningful image accessibility | 0 |

Every V-family component is `0`: a scan for Markdown image references (`![...](...)`) across all scanned files found none. This matches project history — the earlier generated PNG asset batches were rejected on visual-quality grounds and removed, and appendix slide content now lives in the separate slide-text plan files under `revision/assets/model-slide-text/`, not as embedded images in the manuscript. All 11 V-family rows are real `0`s, not a scan miss.

### 13. Appendix Model Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| AM-001 | Model presentation opener | Headings & Navigation | Appendix model start | 6 |
| AM-002 | Scenario brief | Body Prose | Learner context | 6 |
| AM-003 | Model metadata panel | Captions/Metadata | Purpose, audience, timing | 5 |
| AM-004 | Visual sequence table | Reference Table | Slide/visual plan | 6 |
| AM-005 | Key vocabulary table | Target Vocabulary | B1-B2 terminology support | 6 |
| AM-006 | Full script section | Language Sample/Model | Learner-facing model script | 6 |
| AM-007 | Language notes section | Target Vocabulary | Presentation phrase/function study | 6 |
| AM-008 | Pronunciation notes section | Advice | Delivery support | 6 |
| AM-009 | Q&A practice section | Language Sample/Model | Model responses | 6 |
| AM-010 | Skills practised map | Headings & Navigation | Unit-to-model connection | 6 |
| AM-011 | Security/privacy/accessibility note | Advice | Responsible presentation practice | 6 |
| AM-012 | Model slide deck reference | Captions/Metadata | Link/reference to editable PPTX or final slide images | 6 |

Clean and consistent: 3 appendix files x 2 model scripts each = 6, and every AM-family component appears exactly once per model script, confirming the 3 appendix files are structurally uniform. AM-003 is 5/6 (one script states timing without the fuller metadata panel wording).

### 14. Assessment and Review Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| R-001 | Unit review checklist | Reference Table | Unit wrap-up | 0 |
| R-002 | Final presentation checklist | Reference Table | Unit 12 and appendix | 1 |
| R-003 | Peer feedback form | Learner Writing | Class review | 0 |
| R-004 | Self-review form | Reflection | Individual reflection | 1 |
| R-005 | Final rubric | Reference Table | B1/B2 performance expectations | 1 + 2 (Teacher Notes mentions) |
| R-006 | Textbook wrap-up quiz | Reference Table | Unit 12 timing and consolidation | 1 |
| R-007 | Quiz answer key | Teacher-Facing | Teacher notes | 0 |
| R-008 | Error-correction key | Teacher-Facing | Teacher notes or self-study if approved | 0 |

R-001 (unit review checklist) is folded into U-007 Unit Wrap-Up Block rather than existing as its own tagged element — `0` here reflects a naming/overlap issue in the catalog, not a missing component. R-003 and R-007/R-008 do not exist as separate manuscript elements yet.

### 15. Teacher Notes Components

| ID | Component | Type | Needed for | Count |
|---|---|---|---|---:|
| TN-001 | Teacher notes cover/title | Teacher-Facing | Separate printable document | 1 |
| TN-002 | Teaching duration summary | Teacher-Facing | Course planning | 1 |
| TN-003 | Unit teacher note block | Teacher-Facing | Unit-specific guidance | 12 |
| TN-004 | Appendix teacher note block | Teacher-Facing | Model-use guidance | 3 |
| TN-005 | Answer key block | Teacher-Facing | Quiz and controlled practice | 1 |
| TN-006 | Client-specific adaptation note | Teacher-Facing | Business/government/private-class adaptation | 1 |
| TN-007 | One-to-one timing note | Teacher-Facing | Private lesson planning | 2 |
| TN-008 | Terminology watchlist | Teacher-Facing | B1-B2 support | 1 |
| TN-009 | Review sequence note | Teacher-Facing | Business specialist before language editor | 1 |

Counts for TN-001–TN-009 are structural (one per document/section in `Teacher Notes.md`, per the 2026-08-13 memory record of that file's contents) rather than scanner-pattern counts, since `Teacher Notes.md` has one of most of these by design. TN-007 (2) matches the A-007 one-to-one mentions found in the same file.

### 16. Style-System and QA Components

| ID | Component | Needed for | Count |
|---|---|---|---:|
| S-001 | Theme token sheet | Colors, fonts, rule weights, spacing | 0 |
| S-002 | Font specimen | Typeface and fallback QA | 0 |
| S-003 | Color swatch specimen | Print and contrast QA | 0 |
| S-004 | Rule/line specimen | Standard rule weights | 0 |
| S-005 | Callout specimen page | Visual consistency QA | 0 |
| S-006 | Table specimen page | Overflow and readability QA | 0 |
| S-007 | List specimen page | Numbering, nesting, spacing QA | 0 |
| S-008 | Unit opener specimen | Shape/header treatment QA | 0 |
| S-009 | Appendix specimen | Model presentation layout QA | 0 |
| S-010 | Teacher notes specimen | Separate document QA | 0 |
| S-011 | Accessibility QA marker | Alt text, heading order, color contrast | 0 |
| S-012 | Source/provenance register link | Asset traceability | 0 |

All of Group 16 is `0` by definition: these live in `presentations_style.yaml`/`presentations_style.docx` and the QA checklist, never in the learner manuscript.

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

## Manuscript Frequency Findings (2026-09-22)

### Method

Counts above come from a script-based scan (not a manual read) of all 12 `standard-unit-*.md` files, the 3 appendix model-script files, `slide-design-checklist.md`, and `Teacher Notes.md` (scanned separately). It replicates the same detection logic `apply_swp_style_tags()` uses in `scripts/cli.py`: heading level + text pattern, blockquote + preceding label, standalone colon-ending label pattern, and Markdown table header pattern. List counts report both item count and distinct-list-block count (a contiguous run of bullets/numbers), since these answer different questions — item count measures reading volume, block count measures how many separate list components must be styled.

### High-frequency components (clearly need dedicated styled treatment)

- **L-001 Standard bullet list** (564 items / 77 lists) and **L-003 Numbered list** (133 items / 31 lists) — by far the most common structural element; list-block spacing (L-007/L-008) and the bullet/numbered paragraph styles are the single highest-leverage styling investment in the whole build.
- **H-005 Practice task heading / A-001–A-004** (40) — every unit's core activity structure; this cluster of components appears far more than any other heading family and should stay a first-class styled component.
- **H-003 Subsection heading** (33), **H-004/M-003 Script section heading** (27), **C-003 Useful language box** (22) — solid mid-to-high frequency, worth their own styles.
- **T-002 Vocabulary table** (16) and **X-004 Appendix reference tag** (15) — recurring enough to justify a dedicated table family and a consistent cross-reference phrase style.
- **AM-001 through AM-012** (5–6 each, uniform) — low raw counts but each occurs in a fixed, guaranteed 1-per-model-script pattern across all 6 model scripts; these should stay fully specified components regardless of the small count, since the appendix is a small but structurally complete section of the book.

### Genuine long tail: 68 uncatalogued tables, 143 uncatalogued standalone labels

The scan found **113 real tables** in the manuscript but only matched 45 of them to one of the 8 defined `T-00x` header patterns (T-001–T-008). The other **68 tables** each have a unique, unmatched header combination that never repeats verbatim elsewhere (examples: "weak visual | clearer visual", "situation | possible format choices", "purpose | best format | reason", "audience question | weak response | stronger response"). Likewise, **143 standalone colon-ending labels** (e.g. "Useful terms:", "Vocabulary:", one-off "weak X:"/"improved X:" inline labels not written as blockquotes) did not match any of the 12 defined label classes in `_swp_label_class()`.

This is not evidence that the manuscript is disorganized — nearly every one of the 68 unmatched tables is recognizably a planning table (T-003) or comparison table (T-004) in *function*, just with bespoke column headers written per-activity rather than from a fixed small set of header strings. **Recommendation: broaden `_swp_label_class()`/table-header matching to classify by semantic pattern (2-column "before/after" or "weak/improved" shape, "question + notes" shape) rather than exact header text**, before concluding T-003/T-004 are truly low-frequency. As currently measured, their counts (2 and 2) badly understate real usage and should not be used to justify dropping those two table families.

### Low-count components (candidates for de-prioritizing or merging, pending sign-off — not deleted)

These appear once, or not at all, and are reasonable candidates to simplify from a dedicated styled/graphical component down to a plain paragraph-style approximation, or to merge into a sibling component:

- **C-005 Tip box (0)** — never occurs as its own labeled component; merge into C-002 Core Concept Box or drop.
- **C-008 Reflection box (1)**, **C-011 Bilingual planning note (1)**, **M-004 Weak example block (1)**, **M-005 Improved example block (0)**, **A-008 Reflection prompt (1)**, **R-002 Final presentation checklist (1)**, **R-006 Textbook wrap-up quiz (1)**, **T-006 Rubric table (1)**, **T-008 Quiz table (1)** — each a true singleton or near-singleton. Several of these (R-002, R-006, T-006, T-008) are singletons *because they are Unit-12-only, once-per-book components by design*, not because the component is unimportant — a quiz table only ever needs to exist once. These should keep a defined style even at count 1, since "low count" here means "rare by design," not "unnecessary."
- **M-004/M-005 Weak/Improved example block** are the one case where low count likely does mean the cataloged component doesn't match how the content is actually written — see the T-other finding above; the weak/improved pattern is realized as ad hoc comparison tables, not as M-004/M-005 blockquote divs.
- **A-006 Pair/group task variant (5)**, **A-007 One-to-one lesson variant (2)**, **X-002 Unit connection note (5)** — low counts here reflect that these are explicit textual call-outs of an alternate delivery mode, not a count of every activity that could be run that way; treat as correctly rare, not as evidence to drop.

### Zero-count groups (correctly zero, not a scan gap)

Groups 2 (Page-Level Layout), 12 (Visual/Figure), and 16 (Style-System/QA) are entirely `0`. This is expected: Group 2 and 16 describe DOCX/production rules with no Markdown representation at all (they already live in `presentations_style.yaml`/`postprocess_docx.py`), and Group 12 is zero because no Markdown image references exist anywhere in the current manuscript — the earlier generated image batches were rejected and removed, and appendix visuals now live only as separate slide-text plan files, not embedded images. None of these three groups should be cut from the library on count evidence; they are simply not yet built, not unneeded.

### What to focus on next

1. Fix the T-003/T-004 undercount by broadening the table-header match to a semantic pattern rather than exact text, then re-run the scan before making any final call on table-family scope.
2. Prioritize DOCX styling work on L-001/L-003 (lists), H-005/A-001–A-004 (practice tasks), H-003/H-004 (subsections/script sections), and T-002 (vocabulary tables) — these carry the visible bulk of the book.
3. Bring a proposal to the user for C-005 (drop/merge), and confirm M-004/M-005 should be re-modeled as comparison-table content rather than a separate blockquote-div component, before editing `presentations_style.yaml` or the Phase 6 QA rows that reference these IDs.
4. Leave Groups 2, 12, and 16 as planned/future work, not as candidates for removal.

## Manuscript Label Inventory (2026-09-22)

The tables and frequency findings above describe **categories** of text (e.g. "H-005 Practice task heading, count 40") but never listed the **literal strings** actually used in the manuscript. This section is that literal inventory — every real heading, standalone cue label, and table header row found by a fresh scan of all 12 `standard-unit-*.md` files, the 3 appendix model-script files, `slide-design-checklist.md`, and `Teacher Notes.md`. Source scan script and raw JSON are scratch artifacts (not kept in the repo); this section is the durable record.

### Unit and appendix H1 titles (17)

- Unit 1: Audience, Purpose, and Workplace Context
- Unit 2: Message, Objective, and Relevance
- Unit 3: Structure and Flow
- Unit 4: Business English for Signposting
- Unit 5: Clear Visual Communication
- Unit 6: Data, Charts, and Evidence
- Unit 7: Tool-Neutral Slide and Document Workflow
- Unit 8: Delivery: Voice, Presence, Movement, and Notes
- Unit 9: Online, Hybrid, and Asynchronous (Async) Delivery
- Unit 10: Q&A, Challenge Handling, and Interaction
- Unit 11: Final Rehearsal and Peer Feedback
- Unit 12: Final Presentation and Reflection
- Process Improvement Briefing Models *(appendix)*
- Product, Service, or Program Launch Models *(appendix)*
- Project Results Briefing Models *(appendix)*
- Appendix: Slide Design Checklist
- Teacher Notes

### Recurring H2 section headings (same literal label, every unit — H-001/H-005 through H-007)

These appear once per unit (12×, unless noted) and are the backbone of every unit's H2 structure:

- `Learning Outcomes`
- `Presentation English Focus`
- `Unit Wrap-Up`
- `Learner Deliverable` (10 units — Units 10 and 11 use a unit-specific variant instead: `Learner Deliverable: Q&A Response Bank`, `Learner Deliverable: Revised Full Presentation`)
- `Speaking Task` (6 units — Units 4, 10, 11 use a unit-specific variant: `Speaking Task: Signposting Rehearsal`, `Speaking Task: Q&A Rehearsal`, `Speaking Task: Timed Rehearsal`)
- `Optional Model References` (Units 10, 11, 12)
- `How This Helps Your Final Presentation` (Units 10, 11)

Per-appendix-model-file recurring H2s (each appears twice — once per model — in all 3 appendix files): `How to Use These Models`, `Compare the Two Models`.

### Per-unit unique H2 headings (one occurrence each — the "Core Concept" / "Core Skill" / "Model" family, H-001/H-004)

| Unit | Core Concept / Core Skill heading | Model heading |
| --- | --- | --- |
| 1 | Core Skill: Plan from the Audience Outcome | Worked Example |
| 2 | Core Skill: Turn a Topic into a Message | Worked Example: From Brief to Opening |
| 3 | Core Skill: Choose the Structure That Fits the Job / Core Skill: Use Examples and Evidence Well | Worked Example: Structure for a Process Improvement Briefing |
| 4 | Core Concept: Guide the Listener | Model: Adding Signposting to an Outline |
| 5 | Core Concept: One Visual, One Main Message | Model: Visual Redesign |
| 6 | Core Concept: Takeaway Before Detail | Model: Before/After Chart Explanation |
| 7 | Core Concept: Choose the Medium from the Purpose | Model: Choosing the Right Material |
| 8 | Core Concept: Delivery Makes Structure Audible | Model: Marked Delivery Segment |
| 9 | Core Concept: Design for Attention and Access | Model: Adapting a Results Briefing |
| 10 | Core Concept: Answer the Real Question | Model: Improving Weak Q&A Responses |
| 11 | Core Concept: Rehearsal Is a Repair Process | Model: Rehearsal Notes After One Run-Through |
| 12 | Core Concept: Complete the Communication Cycle | Model: Final Task Checklist *(also: Final Presentation Requirements, Final Presentation Task, Final Presentation Checklist)* |

Also unique to their unit: `AI Critical Literacy: Check a Generic Opening` (Unit 2), `Bilingual Planning Note` (Unit 2), `Visual Design Principles` / `Optional AI Critical-Literacy Task` (Unit 5), `Evidence Challenge` (Unit 6), `Register Choices` / `Role and Responsibility Vocabulary` (Unit 4), `Notes, Not a Reading Script` (Unit 8), `Self-Review` / `Next-Step Goals` / `Language-Level Check: B1 and B2` (Unit 12).

### Practice / Speaking Task literal titles (H-005/H-006, 49 total — this is the answer to "Practice X, Useful Terms, etc.")

| Unit | Titles in order |
| --- | --- |
| 1 | Practice 1: Identify the Real Purpose · Practice 2: Rewrite Topic-Only Goals · Practice 3: Draft Your Presentation Brief |
| 2 | Practice 1: Topic or Message? · Practice 2: Use the "So What?" Test · Practice 3: Improve a Weak Opening |
| 3 | Practice 1: Match Purpose and Structure · Practice 2: Convert a Weak List into an Outline · Practice 3: Build a Planning Map |
| 4 | Practice 1: Replace Stiff Phrases · Practice 2: Add Signposting to Your Outline · Practice 3: Choose the Register · Speaking Task: Signposting Rehearsal |
| 5 | Practice 1: Diagnose the Weak Visual · Practice 2: Rewrite the Visual Title · Practice 3: Rebuild a Readability Comparison · Practice 4: Explain Your Revised Visual Aloud |
| 6 | Practice 1: Match the Chart Type · Practice 2: Improve a Weak Chart · Practice 3: Write a Takeaway Title · Practice 4: Explain a Chart in 60-90 Seconds |
| 7 | Practice 1: Choose the Format · Practice 2: Plan Your Visual Pack · Practice 3: Backup and Security Check · Speaking Task |
| 8 | Practice 1: Mark Thought Groups · Practice 2: Reduce a Script to Notes · Practice 3: Presence in Different Settings · Speaking Task |
| 9 | Practice 1: Online and Hybrid Checklist · Practice 2: Adapt the Opening · Practice 3: Plan a Short Async Version · Practice 4: Remote Q&A Language · Speaking Task |
| 10 | Practice Task 1: Classify the Question · Practice Task 2: Build a Response Bank · Practice Task 3: Skeptical-Question Role Play · Speaking Task: Q&A Rehearsal |
| 11 | Practice Task 1: Prepare Your Rehearsal Target · Practice Task 2: Peer Feedback Cycle · Practice Task 3: Revise Your English · Practice Task 4: Final Q&A Check · Speaking Task: Timed Rehearsal |
| 12 | Practice Task 1: Final Preparation Review · Practice Task 2: One-Minute Readiness Check · Practice Task 3: Textbook Wrap-Up Quiz |

Note the naming split: Units 1–9 use `Practice N: ...`; Units 10–12 switch to `Practice Task N: ...`. This inconsistency is worth a normalization decision at DOCX-style time (both map to the same H-005 component today).

### Standalone cue labels (119 distinct strings; C-series/T-series boxes)

The original inventory lumped all 119 colon-ending standalone lines together. They actually split into two grammatically distinct groups that need different treatment (and different punctuation), plus a third pattern worth naming separately:

**Test:** does the string stand alone as a name for the box that follows (a noun phrase — "a box with a name"), or is it a clause/sentence with its own verb that only parses as a lead-in to what follows? Noun phrases are headings once styled and must drop the colon (matching sibling headings like `Learning Outcomes` or `Model`, which carry none). Verb-bearing directive/instruction sentences remain sentence fragments continuing into a list and keep the colon.

**Group 1 — heading-style labels (colon removed once styled; ~71 of 119).** These name the box/table/list that follows and read as complete titles on their own:

- Cross-file repeats: `Useful terms` (Units 1, 4, 5, 6, 7, 9), `Partner feedback` (Units 4, 5, 6, 8), `Core message` (Unit 2, appendix models), `Title` / `Data` (Units 5, 6 — as a scenario-example heading, not the appendix form-field usage), `Structure` (Units 7, 8), `Script`, `Presenter notes`.
- One-off/two-off labels: `Accessibility check`, `Accessibility`, `Action box`, `Async adaptation`, `Async version`, `Audience outcome`, `Audience`, `Bare outline`, `Cautious claim language`, `Checklist`, `Check`, `Comparison task`, `Contingency`, `Example` / `Example start` / `Example visual messages`, `Expected delivery time`, `First-use vocabulary`, `Improved visual`, `In-person opening`, `Katakana risk`, `Language focus`, `Minimum submission`, `One language goal`, `One presentation-skill goal`, `Online adaptation`, `Online or hybrid version`, `Options`, `Pointer and cursor control`, `Possible structure`, `Practice 3, Part A/B/C` (Teacher Notes.md), `Presentation brief`, `Privacy and security`, `Purpose`, `Questions`, `Rehearsal result`, `Sample explanation`, `Sample preview`, `Sample transition`, `Sentence frame`, `Short opening`, `Spoken drill`, `Spoken explanation`, `Spoken version`, `Strong hierarchy` / `Weak hierarchy`, `Suggested quick feedback codes` (Teacher Notes.md), `Text for rehearsal`, `Textbook wrap-up quiz answer key` (Teacher Notes.md), `Thought groups for the core message`, `Thought groups for the opening`, `Three-step flow`, `Useful launch phrases`, `Useful note format`, `Useful phrases`, `Visual notes`, `Vocabulary`, `Weak chart description`, `Weak list`, `Weak opening`, `Weak visual text`, `Weak visual`, `Why it is stronger` (idiomatic heading, matches project-wide "Why This Works" callout convention), `Word stress`.
- All of these lose the trailing colon in the source manuscript (e.g. `Useful terms:` → `Useful terms`, `Language focus:` → `Language focus`) since it is a heading/section marker, not a sentence continuation.

**Group 2 — directive-stem sentences/imperatives (colon kept; ~48 of 119).** These have their own finite verb and only make sense as prose continuing directly into the list/block that follows: `By the end of this unit, you can:` (all 12 units), `Include:`, `Use this sequence:` (Units 1, 2, 3, 5), `Use this frame:`, `Use this order:`, `Use this tool-choice checklist:`, `Use these options if you need support:`, `Use these frames if helpful:`, `Use these models when you need to practise:`, `Use one of these role-agnostic topics:`, `Use pauses to separate limits:`, `Use signposting when you need to:`, `Submit:` / `Submit or complete:` and all the longer `Submit a/one ... :` variants, `Discuss:`, `Check your map with these questions:`, `Compare these planning notes:`, `Place details carefully:`, `Rewrite the list as a structured outline. Choose one structure:`, `Adapt your delivery by checking three things:`, `Improve it by adding:`, `After marking, practice each sentence twice:`, `Then write a one-paragraph presentation brief:`, `Prepare a short explanation using these questions:` (slide-design-checklist.md), `Prepare your explanation with this frame:`, `Chunk key sentences into short thought groups:`, `Stress these key words:`, `A strong core message usually has three parts:`, `You may use this structure:`, `Your final presentation should show these qualities:`, `Your partner gives feedback using two questions:`, `Your partner listens and asks one clarification question:`, `Your partner listens for flow and asks one question:`, `Review this flawed generated slide text:`, `Instead of:` (a preposition, not a name — "instead of what?" only resolves in context, so it stays a fragment even though it's short). These keep the colon exactly as written.

**Group 3 — appendix form-field pairs (not part of this inventory's colon fix).** `Title:`/`Data:` inline scenario examples and the appendix "Scenario Brief" fields (`Audience:`, `Purpose:`, `Core message:` when used as a same-line label+value, e.g. `Core message: The pilot reduced...`) are context-dependent — the identical string can be a Group 1 heading in one file and a Group 3 inline label+value pair in another (confirmed for `Core message`, `Title`, `Data`). Each occurrence was checked individually rather than blind find-and-replaced; only the standalone heading-style occurrences (preceding a separate table/blockquote/list on their own line) had the colon removed.

Full per-occurrence classification with file/line references was done manually against the manuscript rather than kept as a static list here; regenerate the raw candidate list via a short script scanning `HEADING_RE`/`STANDALONE_LABEL_RE` patterns over the same file set (`utf-8-sig` encoding — the BOM in these source files silently drops H1 matches under plain `utf-8`) if auditing this again.

### Similarly-named label groups (8 groups — near-synonym naming drift, not exact-string repeats)

Distinct from the cross-file *exact* repeats already tracked above (`Useful terms`, `Partner feedback`, `Core message`, etc. reused verbatim), these 8 groups are cases where the **same functional role** was given **different literal wording** unit to unit. Worth a normalization decision at DOCX-style time, same as the Practice/Practice Task split already flagged. None of these have been changed yet — this is an inventory, not a fix.

1. **Vocabulary/language-support labels** — pre-teach terms before a task: `Useful terms` (Units 1, 4, 5, 6, 7, 9), `Useful phrases` (all 3 appendix files, ×2 models each), `Useful launch phrases` (launch appendix, ×2), `First-use vocabulary` (launch appendix, ×2), `Vocabulary` (process-improvement & results appendices), `Language focus` (process-improvement appendix), `Word stress` (process-improvement appendix). `Useful note format` (Unit 8) is a one-off that may be a different concept, not a vocabulary list — worth confirming before folding it in.
2. **Practice-activity numbering scheme** — `Practice N: ...` (Units 1–9) vs. `Practice Task N: ...` (Units 10–12). Same H-005 component, two competing patterns (already flagged above, line 736).
3. **Model/Worked-Example heading** — `Worked Example` / `Worked Example: ...` (Units 1–3) vs. `Model: ...` (Units 4–12). Same H-004 slot, two different labels depending on drafting order.
4. **Weak/Strong/Improved diagnostic-example labels** — `Weak opening`, `Weak list`, `Weak hierarchy` / `Strong hierarchy`, `Weak visual`, `Weak visual text`, `Weak chart description`, `Improved visual` — all "before/after example" labels, worded differently per unit instead of a fixed `Weak Example` / `Strong Example` pair.
5. **Sample/Spoken script-text labels** — `Sample preview`, `Sample explanation`, `Sample transition`, `Spoken version`, `Spoken drill`, `Spoken explanation`, `Text for rehearsal` — all label "text to read aloud/practise," worded differently unit to unit.
6. **Delivery-mode adaptation labels (Unit 9 only)** — `Online adaptation`, `Async adaptation`, `In-person opening`, `Online or hybrid version`, `Async version` — same "adapted version of the model for mode X" role, five phrasings within one unit.
7. **Partner feedback vs. Peer feedback** — `Partner feedback` (label in Units 4, 5, 6, 8) vs. "peer feedback" (prose/heading term in Unit 11's "Peer Feedback Cycle" and Unit 12's closing note). Same concept, two different words.
8. **Check vs. Checklist** (Unit 5 only) — two different verification-box labels for functionally the same kind of component.

### Table header row patterns (65 distinct headers; T-series families)

Most-repeated (the real T-00x families, appear in ≥4 files):

- `| Term | Simple meaning |` (7 units + appendices) — T-002 Vocabulary table
- `| Function | Useful phrases |` (7 occurrences, Units 4–6) and `| Function | Useful language |` (5 units) — Useful Language box
- `| Function | Question | Model answer |` (all 3 appendix files ×2 models) — Q&A Model Answers table
- `| Unit connection | Skill shown in this model |` (all 3 appendix files ×2 models) — X-002 Unit connection note

Everything else is a bespoke 2–4 column header unique to one practice/model (e.g. `| Weak visual | Clearer visual |`, `| Situation | Possible format choices |`, `| Rehearsal focus | What to check | Repair action |`) — consistent with the "68 uncatalogued tables" finding above; these are functionally before/after, planning, or comparison tables with custom column names rather than a fixed label set.
