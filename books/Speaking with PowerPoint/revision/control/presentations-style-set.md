# Presentations Style Set for `presentations_style.docx`

Purpose: define the Word reference style set for the presentation-skills textbook before DOCX production. This file is based on:

- `style_definitions/business_result_2/2026-08-13/br2e_data.py`
- `style_definitions/business_result_2/2026-08-13/BR2e_Design_System_v4.1.html`
- a scan of the current learner-facing drafts in `books/Speaking with PowerPoint/revision/drafts/`

The Business Result 2e system is used as a proportional design reference, not as a style-name source to copy directly. The final reference file should be named:

`books/Speaking with PowerPoint/revision/control/presentations_style.docx`

## Design Direction

The textbook should look contemporary, professional, and printable on mostly white office paper. It should not look like a PowerPoint manual, a marketing brochure, or a copied commercial textbook page.

Core principles:

- White page base with strong typographic hierarchy.
- Functional color, not decoration.
- Print-visible tints and rules.
- Tables and activity areas should be easy to scan.
- Learners should immediately recognize: core skill, useful language, model, practice, checklist, reflection, and final task.
- Use shape/background treatments consistently enough to support navigation, but not so heavily that the page becomes visually noisy.

## Page and Scaling Rules

Base page:

- A4 portrait.
- Primary output is printable DOCX/PDF for office printers and ordinary hardcopy use.
- Commercial textbook source sizes are too small for this project.
- Main body text must be `11 pt`.
- Scale other BR2e A4-derived type sizes proportionally from the BR2e A4 body size of `9.5 pt`.
- Scaling factor: `11 / 9.5 = 1.1579`.
- Round all font sizes to Word-safe half-point values.
- Use mirror-compatible margins where possible so the document can be printed single-sided or double-sided.
- Avoid bleed-dependent design because most copies will be printed on white office paper.

Initial margin specification:

| Area | Size | Rationale |
|---|---:|---|
| Top | `20 mm` | Allows a running header without crowding the unit title area |
| Bottom | `25 mm` | Allows page number/footer line and learner writing space |
| Inside/left | `40 mm` | Binding/annotation margin requested for the production sample |
| Outside/right | `25 mm` | Keeps a stable outside margin for office printing |
| Header from edge | `9-10 mm` | Keeps running head clear of body text |
| Footer from edge | `9-10 mm` | Keeps page number clear of body text |

Binding note:

- Current production sample uses asymmetric margins: top `20 mm`, bottom `25 mm`, left `40 mm`, right `25 mm`.
- Recheck margins after the first full-unit print proof because the left margin is intentionally generous.

Word-compatible font-size rule:

- DOCX stores font sizes in half-point units.
- Use whole or half-point sizes only.
- Do not use arbitrary decimals such as `11.3 pt`.
- Disable Word's `snap to grid` paragraph setting for the entire book. This applies to Normal and every paragraph style in the generated reference DOCX.
- Set proofing language to English (US), `en-US`, for the whole reference style set.
- Enable document hyphenation for prose-heavy pages.
- Body text and Normal-style prose use justified alignment.
- Body text and Normal-style prose must have widow/orphan control enabled.

Line spacing / leading:

- Main body: `11 pt` type with approximately `1.12-1.15` line spacing.
- Dense notes and table text: `10-10.5 pt` with `1.05-1.10` line spacing.
- Full spoken model scripts: `11 pt` with slightly more open leading, approximately `1.15`.
- All headings, running heads, cover titles, TOC headings, appendix/model headings, and other heading-like styles use single line spacing.
- All heading styles must have `Keep with next` enabled in Word paragraph settings.
- All heading styles must be left-aligned and suppress automatic hyphenation.
- Avoid fully justified text unless hyphenation and line breaks are checked in Word.

Spacing around headings:

| Style | Before | After | Rule |
|---|---:|---:|---|
| Unit title / `PS Heading 1` | `0 pt` | `16 pt` | Starts a new unit page or unit block |
| Main section / `PS Heading 2` | `20 pt` | `8 pt` | Keep with following paragraph/table |
| Local subhead / `PS Heading 3` | `16 pt` | `6 pt` | Keep with following paragraph/table |
| Script subhead / `PS Heading 4` | `12 pt` | `4 pt` | Keep with following script paragraph |
| Practice heading | `16 pt` | `6 pt` | Keep with task instruction |

Page-break and keep rules:

- Each unit should start on a new page unless final imposition later requires otherwise.
- Major appendices should start on a new page.
- Keep headings with the following paragraph or table.
- Keep short callout labels with their callout body.
- Avoid leaving a table header at the bottom of a page.
- Avoid widows and orphans in body text and model scripts.
- Do not split small two-row or three-row tables across pages.

## Print Color Scheme

Use a formula-derived palette based on three user-supplied colors from Sanzo Wada's *A Dictionary of Color Combinations* published by Seigensha. Tints are deliberately print-visible but should avoid the harsh, saturated look of screen-first palettes.

Base colors:

| Base | CMYK | RGB/Hex Conversion | Role |
|---|---:|---:|---|
| Eupatorium purple | `(25, 79, 12, 0)` | `#BF36E0` | Primary accent family |
| Cream yellow | `(0, 28, 68, 0)` | `#FFB852` | Warm support/caution/action family |
| Blue | `(95, 54, 0, 0)` | `#0D75FF` | Navigation/model/reference family |

Formula rules:

- CMYK-to-RGB conversion: `rgb_channel = round(255 * (1 - cmy_channel / 100) * (1 - k / 100))`.
- Shade/tint mixing: `mix(base, target, amount) = round(base * (1 - amount) + target * amount)` per RGB channel.
- Derivations must be tracked in `presentations_style.yaml` under `color_system` so the base colors can be changed after print testing and the palette recalculated.

| Role | Hex | Use |
|---|---:|---|
| Deep ink | `#031A38` | Main text, running headers, strong text; formula `mix(blue, black, 0.78)` |
| Graphite | `#052C61` | Secondary headings and strong neutral text; formula `mix(blue, black, 0.62)` |
| Slate | `#073D85` | Table rules, labels, secondary lines; formula `mix(blue, black, 0.48)` |
| Eupatorium purple | `#BF36E0` | Primary accent; base color |
| Purple dark | `#691E7B` | Core skill, section rules, key learning labels; formula `mix(eupatorium_purple, black, 0.45)` |
| Blue dark | `#084BA3` | Model/reference links and document-role accents; formula `mix(blue, black, 0.36)` |
| Yellow dark | `#996E31` | Cautions, timing, decision/action prompts; formula `mix(cream_yellow, black, 0.40)` |
| Purple tint | `#F5DFFA` | Core skill / language box background; formula `mix(eupatorium_purple, white, 0.84)` |
| Blue tint | `#E2EEFF` | Model/example background; formula `mix(blue, white, 0.88)` |
| Yellow tint | `#FFEBCF` | Tip/caution background; formula `mix(cream_yellow, white, 0.72)` |
| Grey tint | `#ECF4FF` | Table headers, worksheet rows; formula `mix(blue, white, 0.92)` |
| Light grey | `#F5F9FF` | Alternating rows and light planning areas; formula `mix(blue, white, 0.96)` |
| White | `#FFFFFF` | Page base and reversed text |

Do not rely on fill color alone. Any colored box must also use at least one structural cue: a top rule, left rule, medium/semibold label, border, icon/label text, or clear spacing.

Compatibility note: the current YAML still contains legacy semantic keys such as `teal`, `amber`, and `plum` because existing style rules reference them. These are now aliases to Wada-derived colors, not independent palette choices.

## Font Family Rules

Primary body:

- Word font: `Noto Serif`
- Medium/emphasis face: `Noto Serif Medium`
- Use for body text, activity instructions, model scripts, examples, and learner-facing prose.

Primary sans:

- Word font: `Noto Sans`
- Medium face: `Noto Sans Medium`
- Semibold face: `Noto Sans SemiBold`
- Use for headings, labels, activity numbers, table headers, running headers, callout labels, and navigation elements.

Display:

- Word font: `Noto Sans Display SemiBold`
- Use for cover and unit-title display treatment only.

Japanese support:

- Word font: `Noto Sans JP`
- Use for any Japanese glosses, bilingual planning support, or Japanese learner notes that remain in the final document.

Weight rule:

- Prefer real `Medium` or `SemiBold` font faces over synthetic Word bold.
- Avoid bold for routine hierarchy. Use spacing, size, color, rules, and Medium/SemiBold faces first.
- Reserve true bold for rare cover/display cases only if a Medium/SemiBold face is not strong enough.

## Book-Level Layout System

These rules sit above individual paragraph/table styles. Some can be stored in `presentations_style.docx`; others will need the DOCX build script, Word postprocessing, or manual final-layout QA.

### Sections and Page Numbering

Use separate Word sections for:

1. Front cover.
2. Front matter.
3. Table of contents.
4. Main units.
5. Appendices.
6. Back matter.
7. Back cover.

Page-number rules:

- Front cover: no visible page number.
- Front matter and table of contents: lowercase Roman numerals if numbering is needed; otherwise no visible page numbers.
- Main units: restart at Arabic page `1`, or continue from front matter if a single continuous scheme is preferred for printing.
- Appendices: continue Arabic page numbering from main units.
- Back cover: no visible page number.
- Each generated section should include odd/even footer references. Page numbers are right-aligned on both odd and even pages unless the final print layout changes.

Open decision: choose final page-numbering scheme after the final title, table of contents, and appendix count are fixed.

### Headers and Footers

Header/footer goals:

- Help navigation without making the page look crowded.
- Stay printable in black-and-white or color.
- Avoid confusing learners with production-only information.

Recommended header/footer treatment:

| Page type | Header | Footer |
|---|---|---|
| Front cover | None | None |
| Front matter | Book title or blank | Optional Roman page number |
| Table of contents | `Contents` | Optional Roman page number |
| Unit pages | Unit number/title or short book title | Arabic page number |
| Appendix pages | Appendix name or model family | Arabic page number |
| Teacher notes | `Teacher Notes` plus unit reference | Arabic page number |
| Back cover | None | None |

Visual treatment:

- Running heads use `PS Running Head` or a plainer dark-text variant.
- Page numbers use `PS Page Number`.
- `PS Page Number` is right-aligned in both odd and even footers.
- Use a thin rule or small color block only when it improves navigation.
- Keep header/footer text short enough to survive narrow margins.

### Table of Contents

The textbook should include a table of contents unless the final printed version is very short.

TOC requirements:

- Include front matter only if useful to the learner.
- Include all 12 units.
- Include appendices and model presentations.
- Include the slide design checklist and wrap-up quiz if kept as appendices.
- Do not include every practice task; the TOC should not become too long.
- Use leader dots only if they render cleanly in Word/PDF.
- Update the TOC in Word before final PDF export.

Style needs:

- `PS TOC Title`
- `PS TOC Level 1`
- `PS TOC Level 2`
- `PS TOC Page Number`

### Front Matter

Front matter should be learner-facing and concise.

Required front matter:

1. Half title or title page.
2. Copyright / production line.
3. Revision date and version line.
4. Short learner-facing introduction.
5. How to use this book.
6. Course map or unit overview.

Optional front matter:

- A short note on tools, explaining that PowerPoint, Canva, Google Slides, Keynote, PDFs, dashboards, and document walkthroughs are all possible visual-presentation tools.
- A short accessibility note for learners.
- A short AI note that mentions AI critically but does not promote it as a replacement for English development.

Avoid:

- Teacher-only explanations.
- Internal project history.
- Long methodological justification.
- Claims that the book is for only government or only business clients.

### Back Matter

Back matter should support learner review and practical reuse.

Required or likely back matter:

1. Full model presentation appendices.
2. Slide design checklist.
3. Final presentation checklist.
4. Textbook wrap-up quiz if not placed in Unit 12.
5. Phrase bank index or language review list.
6. Key business terms glossary, especially for terms used in models.
7. Credits and source/license notes for images, icons, generated assets, and templates.

Teacher-facing answer keys and teaching notes stay in `Teacher Notes.md` or a separate generated teacher-notes DOCX, not in the learner textbook unless the item is intentionally self-study.

### Covers

The book needs at least:

- Front cover.
- Back cover.

Optional:

- Inside front cover with course map or quick-use guide.
- Inside back cover with quick checklist or phrase-bank summary.

Front cover requirements:

- Final title must be tool-neutral; do not foreground `PowerPoint`.
- Include subtitle or descriptor that makes the learner audience clear.
- Include organization/production identity once confirmed.
- Use a contemporary professional visual style that connects to business presentations with visuals.
- Avoid stock-like presenter silhouettes, dated clip art, and software-specific UI mockups.
- Must print acceptably on white paper and remain legible in grayscale.

Back cover requirements:

- Short learner-facing description.
- Bullet list of skills covered.
- Revision/version line.
- Production/organization line.
- Optional QR/link space only if the final distribution plan needs it.

Cover production note:

- A cover can be generated separately from the DOCX reference style if needed.
- If the cover is built in Word, it needs dedicated cover styles and possibly full-page positioned elements.
- If the cover is built in Canva or another design tool, keep a PDF/PNG export plus the editable source link or file reference in the asset register.

### Images, Figures, and Captions

Style and production requirements:

- Every figure needs a placement decision: inline, full-width, half-width, or appendix-only.
- Every instructional image needs a caption or nearby task label unless the purpose is obvious.
- Avoid images with embedded AI-generated text unless manually checked.
- Keep figure width within page margins.
- Use `PS Caption` for captions and source notes.
- Record asset source, license, generation prompt/tool, edit history, and final file path in the asset register.

### Tables and Overflow

Tables are a major layout risk in this book.

Production rules:

- Prefer landscape only if a table cannot be made readable on portrait A4.
- Split very wide tables into two smaller tables before reducing text below `10 pt`.
- Planning tables need writable row height.
- Phrase-bank tables should prioritize readable language over fitting many phrases into one row.
- Rubric tables should be checked manually after conversion.

### Accessibility and Export QA

Final DOCX/PDF QA must include:

- Word accessibility checker.
- Heading-order check.
- Table header-row check.
- Color contrast and color-not-alone check.
- Alt text or decorative marking for meaningful images.
- PDF metadata title/author/subject check.
- Visible revision date check.
- Print test or rendered-page review for representative pages: cover, unit opening, dense table, callout page, appendix script page, quiz/checklist page.

## Core Paragraph Styles

| Style name | Basis | Size | Font | Color | Intended use |
|---|---|---:|---|---|---|
| `PS Body Text` | BR body scaled to 11 | 11 pt | Noto Serif | Deep ink | Default textbook prose |
| `PS Body Text Small` | BR key line scaled | 10 pt | Noto Serif | Deep ink | Dense notes, table body where space is tight |
| `PS Heading 1` | Unit title adapted | 28 pt | Noto Sans Display SemiBold | White | Unit-opening title on colored background |
| `PS Heading 2` | Section head scaled | 16 pt | Noto Sans SemiBold | Muted teal | Main section headings |
| `PS Heading 3` | Subhead adapted | 13.5 pt | Noto Sans SemiBold | Graphite | Local subheads |
| `PS Heading 4` | Script-section head | 12 pt | Noto Sans SemiBold | Slate | Model script sections such as Opening, Evidence, Close |
| `PS Running Head` | Running header | 10.5-11 pt | Noto Sans SemiBold | White | Header band text |
| `PS Page Number` | Page number | 12 pt | Noto Sans Medium | White or Deep ink | Page number in footer/header system |
| `PS Caption` | Caption | 9.5 pt | Noto Sans | Slate | Captions, figure notes, source notes |
| `PS Cross Reference` | Crossref | 12 pt | Noto Sans Medium | Soft business blue | Appendix/model references |

Note: The BR2e scaled unit-title size of `47.5 pt` is too large for this book unless used for a cover or part opener. Use a smaller, cleaner unit-opening title treatment for normal units.

## Heading and Background Shape System

### Unit Opening

Styles/elements:

- `PS Unit Number Block`
- `PS Unit Title Band`
- `PS Unit Subtitle`
- `PS Unit Outcomes Box`

Treatment:

- Top or side band in Deep ink or Professional teal.
- White unit title text.
- Current unit title size is `28 pt`; if titles still wrap badly in the specimen build, shorten unit titles rather than increasing compression.
- Small accent stripe in Amber or Business blue.
- Outcomes box below the title band using Teal tint with a visible teal top rule.
- Keep the unit-opening treatment clean enough for office printing.

### Section Headings

Styles/elements:

- `PS Section Head`
- `PS Section Head Rule`
- `PS Section Label`

Treatment:

- No full-width heavy color bars for every section.
- Use teal heading text with a 2-3 pt teal underline rule.
- For major recurring sections such as `Presentation English Focus`, allow a light background strip in `#E5E7EB` or `#CDEDEA`.

### Practice Headings

Styles/elements:

- `PS Practice Head`
- `PS Practice Number`
- `PS Practice Instruction`

Treatment:

- Numbered practice heading should be visually distinct from ordinary section heads.
- Use a small colored number capsule or square in Professional teal.
- Heading text remains black/graphite.
- Shaded task-heading styles retain normal heading space before. If Word paragraph shading visually fills the space above a heading in the produced DOCX, correct that during DOCX cleanup rather than removing the heading spacing from the style definition.
- Do not stack ordinary headings back to back in manuscript source. Put learner-facing text, an instruction, or a table between headings unless a designed component explicitly handles the spacing.
- Filled paragraph styles need visible internal breathing room; use at least `5 mm` left/right paragraph indent for box-style paragraphs, and at least `3 mm` for short shaded task heads.
- Do not use rounded decorative pill labels unless the shape has a clear functional role.

## Callout and Box Styles

| Style name | Visual treatment | Use |
|---|---|---|
| `PS Core Skill Box` | Teal tint background, teal top rule, bold sans label | Core skill/concept blocks |
| `PS Useful Language Box` | Teal tint or white with teal left rule | Presentation English phrase banks |
| `PS Model Box` | Blue tint background, blue left rule, model label | Worked examples, model excerpts |
| `PS Tip Box` | Amber tint background, amber top rule | Tips, reminders, short cautions |
| `PS Caution Box` | Amber tint, amber left rule, stronger label | Confidentiality, overclaiming, accessibility warnings |
| `PS AI Literacy Box` | Light grey background, slate border, no promotional styling | AI critical-literacy notes and critique tasks |
| `PS Reflection Box` | White or light grey background, slate border | Self-review and next-step goals |
| `PS Teacher Note Box` | Separate teacher-notes document only; grey background | Teacher-facing content in `Teacher Notes.md` |

AI boxes must remain neutral and critical. They should not visually promote AI as a shortcut or primary skill.

## Lists and Numbering

The manuscript contains ordinary bullets, chronological numbered tasks, nested subpoints, and checklist-like sequences.

Required list styles:

- `PS Bullet List`
- `PS Bullet List 2`
- `PS Numbered List`
- `PS Numbered List 2`
- `PS Checklist`
- `PS Sequence List`

List-level style definitions:

| Style | Level | Marker | Indent | Use |
|---|---:|---|---:|---|
| `PS Bullet List` | 1 | solid bullet | `5 mm` hanging | Non-sequential points, examples, short option lists |
| `PS Bullet List 2` | 2 | open bullet or dash | `10 mm` hanging | Supporting detail under a level-1 bullet |
| `PS Numbered List` | 1 | `1. 2. 3.` | `5 mm` hanging | Chronological steps, ordered procedures, ranked stages |
| `PS Numbered List 2` | 2 | `a. b. c.` or `i. ii. iii.` | `10 mm` hanging | Substeps under an ordered step |
| `PS Checklist` | 1 | checkbox/status marker | `5 mm` hanging | Completion checks and readiness checks |
| `PS Sequence List` | 1 | emphasized number marker | `6 mm` hanging | Important process sequences that may receive a background/number treatment |

Numbering implementation note:

- The paragraph styles must exist in `presentations_style.docx`.
- Actual automatic numbering and multilevel list binding may need Pandoc list mapping, Word numbering XML, or postprocessing.
- Chronological instructions should use numbered-list Markdown before conversion.
- Nested support points should be indented one level in Markdown so they can become level-2 list paragraphs.
- Do not flatten all lists into one hierarchy; list type must follow function.

List-block spacing rule:

- Do not add vertical spacing after every list paragraph.
- Middle list items should have `0 pt` before and `0 pt` after.
- Add space before the first item in a list block and after the last item in a list block.
- Target spacing: about `3 pt` before and `3 pt` after ordinary list blocks, adjusted by context.
- Do not add extra spacing between a parent list paragraph and child list paragraphs.
- List paragraphs should be left-aligned, not justified.
- List paragraphs should suppress automatic hyphenation, even when document-level hyphenation is enabled.
- This requires build/postprocess handling because a single Word paragraph style cannot know whether the paragraph is the first, middle, or final item in a list.
- Preferred implementation: detect list blocks after Pandoc conversion and assign first/last-item spacing or direct paragraph formatting at the block boundary.
- If separate first/last list styles are used, define them as variants of the base list style, not as separate list types.
- When using `scripts/style_bridge.lua`, enable `style_bridge.list_block_spacing` in Markdown metadata to add DOCX-only spacing before and after list blocks.

Numbered list background treatment:

- Use only for important process sequences, not every numbered list.
- Number marker: small square or circle with Professional teal fill and white number.
- Text sits on white or very light grey background.
- Use for steps such as planning sequences, delivery sequence, Q&A sequence, and final-preparation sequence.

Checklist treatment:

- Use visible boxes or status cells, not color alone.
- Checklist tables can use grey header and white/light-grey rows.
- Keep enough row height for learners to write by hand.

## Table Style Families

The current drafts contain 115 Markdown tables. They should not all receive the same table style.

The reference DOCX table styles must not look like default/undefined Word tables. The YAML generator creates the base table-style names, then `scripts/refine_presentations_reference_docx.py` applies richer table-style XML and saves the file through Microsoft Word COM. This is required because `python-docx` exposes only a limited part of Word's table-style model.

Required table-style differences:

- distinct header-row fill and text color by table family;
- white or light header-row text whenever the header fill is dark;
- single-spaced header-row text;
- first-column emphasis where the first column carries functional labels;
- banded-row treatment where it improves scanning;
- family-specific top rule color;
- consistent cell margins;
- visible but restrained internal rules;
- no reliance on color alone for weak/improved/status meanings.

### `PS Phrase Bank Table`

Detected examples:

- `Function | Useful language`
- `Function | Useful phrases`
- `Function | Neutral business English`
- `Function | More formal | Neutral | More conversational`

Treatment:

- Header row: Professional teal fill, white sans bold text.
- Body: white/light grey alternating rows.
- First column: sans bold, Graphite.
- Phrase columns: body font, 11 pt where possible.

### `PS Vocabulary Table`

Detected examples:

- `Term | Simple meaning`
- `Term | Simple meaning in this model`
- `Phrase | Meaning | Example`

Treatment:

- Header row: Graphite or Slate fill, white text.
- Term column: sans bold, Deep ink.
- Meaning column: body font.
- Use clear row rules; no dense decorative fill.

### `PS Planning Table`

Detected examples:

- `Question | Your notes`
- `Planning area | Your notes`
- `Question | My answer`
- `Area | Reflection question | My notes`

Treatment:

- Header row: Slate fill with white text.
- Blank response cells: white with visible Slate or Grey rules.
- Increase row height for handwriting.
- Avoid heavy color fills in learner-writing areas.

### `PS Comparison Table`

Detected examples:

- `Topic only | Stronger audience outcome`
- `Weak title | Improved title | Why it is clearer`
- `Weak visual | Clearer visual`
- `Too strong | More careful`
- `Audience question | Weak response | Stronger response`

Treatment:

- Neutral header.
- Use subtle status colors only where useful: weak/problem column may use very light amber tint; stronger/repair column may use light teal tint.
- Add text labels such as `Weak`, `Improved`, `Repair`, not color alone.

### `PS Checklist Table`

Detected examples:

- `Check | Yes / Not yet | Notes`
- `Check | Status`
- `Item | Ready? | Note`
- `Area | Check`

Treatment:

- Grey header.
- Alternating white/light grey rows.
- Short status columns centered.
- Notes columns wide and writable.

### `PS Rubric Table`

Detected examples:

- `Area | B1 performance | B2 performance`
- `Category | Evidence`
- final checklist and assessment tables

Treatment:

- Header row: Deep ink or Graphite fill, white text.
- First column: sans bold.
- Keep B1/B2 columns balanced.
- Use 10.5-11 pt text, not dense 8-9 pt commercial textbook text.

### `PS Model Support Table`

Detected examples:

- `Visual | Purpose | Suggested content`
- `Visual | Main message | Presenter action`
- `Unit connection | Skill shown in this model`
- `Function | Question | Model answer`

Treatment:

- Header row: Business blue fill, white text.
- Body rows: white/light blue alternating rows.
- Use for appendices and model support.

### `PS Quiz Table`

Detected examples:

- `Question | A | B | C`

Treatment:

- Header row: Graphite fill, white text.
- Question column wider than options.
- Option columns centered or left-aligned depending on length.
- Avoid very small text; split long quiz items if needed.

## Block Text and Model Script Styles

The manuscript uses blockquotes for frames, sample openings, flawed examples, and short spoken models.

Styles:

- `PS Block Example`
- `PS Spoken Model`
- `PS Weak Example`
- `PS Improved Example`
- `PS Script Text`
- `PS Script Section Head`
- `PS Presenter Notes`

Treatment:

- Ordinary examples: Blue tint background or blue left rule.
- Weak examples: Amber tint or amber left rule with label `Weak`.
- Improved examples: Teal tint or teal left rule with label `Improved`.
- Full spoken model scripts: mostly white background for readability; use section heads and a subtle left rule rather than placing long script passages inside heavy colored boxes.
- Presenter notes: light grey background, smaller sans/body mix, visibly different from full scripts.

## Appendix Model Styles

Appendix models require their own clear hierarchy because each model includes scenario, vocabulary, full script, language notes, pronunciation notes, Q&A, privacy/accessibility/contingency notes, and skill mapping.

Styles:

- `PS Appendix Title`
- `PS Model Title`
- `PS Scenario Brief`
- `PS Model Metadata`
- `PS Visual Sequence Table`
- `PS Key Vocabulary Table`
- `PS Full Script Head`
- `PS Full Script Text`
- `PS Language Notes`
- `PS Pronunciation Notes`
- `PS QA Model Table`
- `PS Security Notes`
- `PS Skills Practised Table`

Treatment:

- Use Business blue as the appendix/model accent, not the same teal used for core unit learning.
- Keep learner-facing support materials clear and printable.
- Do not visually bury vocabulary or Q&A; these are learner study material, not teacher notes.

## Special Elements from Current Manuscript

The scan identified these recurring or important elements that must be supported by the reference DOCX and/or postprocess rules:

- Learning outcomes list.
- Core concept / core skill block.
- Presentation English focus phrase bank.
- Useful terms / vocabulary table.
- Worked example.
- Practice tasks, numbered by task.
- Speaking task.
- Learner deliverable.
- Unit wrap-up.
- Optional model references.
- AI critical-literacy task.
- Bilingual planning note.
- Privacy/security/accessibility/contingency notes.
- Pronunciation and intelligibility notes.
- Word-stress examples.
- Q&A model answers.
- Final presentation checklist.
- Textbook wrap-up quiz.
- Teacher notes, in a separately printable document.

## Reference DOCX Build Requirements

`presentations_style.docx` must include, at minimum:

- A4 page setup.
- Margin, header, and footer settings suitable for office printing.
- Normal/body style based on `PS Body Text`.
- Heading 1-4 styles mapped to `PS Heading 1-4`.
- Front matter, TOC, cover, back cover, glossary, credits, and appendix styles.
- Bullet, numbered, nested bullet, nested numbered, checklist, and sequence list styles.
- Table styles for phrase bank, vocabulary, planning, comparison, checklist, rubric, model support, and quiz tables.
- Paragraph styles for all callout and block-text families.
- Character styles for key terms, task verbs, cross-reference targets, stress marks, and optional pronunciation emphasis.
- Running header/footer styles.
- Page-numbering and section-break behavior for cover, front matter, contents, units, appendices, and back matter.
- Sample prototype elements if postprocessing will insert unit title blocks or repeated callout tables.

## Markdown-to-DOCX Mapping Notes

The source Markdown currently uses standard Markdown headings, tables, lists, and blockquotes. To produce the intended DOCX styles reliably, the production source may need lightweight semantic wrappers or a prebuild mapping step.

Recommended mapping:

| Source pattern | Target style |
|---|---|
| `# Unit N...` | `PS Heading 1` plus unit-opening treatment |
| `## Learning Outcomes` | `PS Section Head` |
| `## Core Concept...` / `## Core Skill...` | `PS Core Skill Box` |
| `## Presentation English Focus` | `PS Section Head` plus `PS Phrase Bank Table` for following tables |
| `## Worked Example...` / `## Model...` | `PS Model Box` / model section styles |
| `## Practice...` | `PS Practice Head` |
| `## Speaking Task...` | `PS Practice Head` with speaking-task accent |
| `## Learner Deliverable` | `PS Reflection Box` or deliverable callout |
| blockquote examples | `PS Block Example`, `PS Weak Example`, or `PS Spoken Model` depending on nearby label |
| vocabulary tables | `PS Vocabulary Table` |
| phrase-bank tables | `PS Phrase Bank Table` |
| planning/writable tables | `PS Planning Table` |
| checklist tables | `PS Checklist Table` |
| rubric/assessment tables | `PS Rubric Table` |

If this mapping cannot be inferred safely from headings and table headers, add explicit Markdown div classes before final conversion rather than relying on manual Word cleanup.

## Open Build Decisions

1. Confirm whether `News Gothic MT` and `PMN Caecilia` are available on the production machine. If not, use the fallback stack.
2. Decide whether unit-opening title blocks will be inserted by postprocess prototype tables or created directly through Word styles.
3. Decide whether semantic Markdown divs will be added before build, or whether postprocess will infer style families from heading/table-header patterns.
4. Decide whether teacher notes use the same style set with reduced decoration or a plainer print-first variant.
5. Confirm final placement of the generated `presentations_style.docx`.
6. Choose final title before cover, metadata, running heads, and back cover are finalized.
7. Choose final page-numbering scheme: separate Roman/Arabic numbering or simple continuous numbering.
8. Decide whether the learner textbook includes answer keys for self-study items or whether answer keys stay only in teacher notes.
9. Decide whether cover production happens in Word, Canva, or another design tool.
10. Decide whether the final TOC is generated by Word fields, manually typeset, or generated by the build pipeline.
