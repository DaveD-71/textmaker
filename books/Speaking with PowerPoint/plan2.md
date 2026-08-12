# Plan 2: Presentation Skills 2026 Curriculum Rebuild and Asset Plan

## Summary

Replace `books/Speaking with PowerPoint/plan.md` with a production-ready Plan 2 for rebuilding the existing `books/Presentation Skills` series from the 2026 revision requirements.

This is not a standalone edit of the 39-page *Speaking with PowerPoint* PDF. It is a rebuild of the existing Presentation Skills series, using *Speaking with PowerPoint* as the main modernization trigger and source of visual-presentation content.

Default decisions:
- Product target: `books/Presentation Skills` tiered series.
- Main design anchor: Standard tier = 12 lessons.
- Target learner: B1-B2 adult business ESL learners in Japan.
- Final title: defer until content architecture is stable.
- Model strategy: use three recurring model strands, not one Ventura replacement.
- Tool stance: teach visual communication principles; PowerPoint is one common example, not the course concept.
- Asset stance: instructional assets first; decorative illustration only when it teaches something.

Core tool examples, subject to final verification from official sources:
- Microsoft 365 / PowerPoint
- Google Slides / Google Workspace
- Canva
- Apple Keynote
- Generic PDF, dashboard, spreadsheet, and document walkthroughs

## Product Specification

Deliver three tiered manuscripts from the same rebuilt curriculum:

1. Essentials
   - Short-course version derived from the Standard curriculum.
   - Focus: planning, structure, clear visuals, delivery basics, Q&A basics.
   - Output: learner can deliver a short business update with one or two clear visuals.

2. Standard
   - Canonical 12-lesson course.
   - Focus: one progressively developed business presentation.
   - Output: learner can plan, design, deliver, and discuss a 5-7 minute business presentation with visuals.

3. Long
   - Standard course plus extension work.
   - Focus: persuasion, recommendation defense, more advanced data/evidence, team presentation.
   - Output: learner can deliver a fuller recommendation or briefing and handle discussion.

The old two-day sprint framing is retired for this series rebuild. Use it only as a fallback editorial triage lens, not as the production schedule.

## Curriculum Map

Standard tier is the canonical 12-lesson map.

| # | Lesson | Learner outcome | Business task | Language / skill focus | Key activity | Asset needed |
|---|---|---|---|---|---|---|
| 1 | Presentations as Business Decisions | Define audience, purpose, and desired outcome | Diagnose a weak brief | purpose, audience, decision/action | Rewrite weak briefs into audience-outcome briefs | planning form |
| 2 | Message and Evidence | State a key message supported by evidence | Build a claim from facts | key message, claim/evidence, concise wording | Turn raw notes into a message-evidence chain | message map |
| 3 | Structures for Business Presentations | Choose a structure that fits purpose | Organize update/proposal/briefing | signposting, agenda language | Match cases to structures | structure cards |
| 4 | Storyboard Before Visuals | Plan flow before making slides | Build a visual storyboard | sequencing, transitions | Create a storyboard for one model case | storyboard template |
| 5 | Designing Visual Support | Make visuals simple, readable, and useful | Improve weak visuals | visual hierarchy, contrast, one-message visuals | Redesign a cluttered visual | before/after mockups |
| 6 | Data and Evidence Visuals | Explain data accurately and ethically | Present trends/comparisons | numbers, trends, sources, uncertainty | Fix a misleading chart and explain it | chart set |
| 7 | Tool and Format Choice | Choose the right format/tool for the audience | Decide slides vs PDF vs dashboard vs document | tool-neutral preparation language | Select a format for different situations | tool-choice matrix |
| 8 | Speaking with Visuals | Deliver without reading visual content | Explain and point to visuals clearly | referring to visuals, highlighting, pacing | Practice “show, pause, explain” | delivery sequence diagram |
| 9 | Online and Hybrid Delivery | Adapt delivery for screen sharing and remote audiences | Run a remote presentation setup | camera, mic, chat, Q&A, captions | Remote setup checklist and mini-delivery | online setup mockup |
| 10 | Interaction and Q&A | Move from presentation to discussion | Handle questions and interruptions | clarifying, deferring, checking, next steps | Answer skeptical questions from a model case | Q&A flowchart |
| 11 | Rehearsal and Feedback | Improve timing, clarity, and confidence | Rehearse with peer feedback | feedback language, self-checking | Record, review, revise | peer-feedback form |
| 12 | Final Presentation | Deliver and discuss a complete presentation | Present final business case | integrated performance | Final presentation and Q&A | rubric/checklist |

Long-tier extensions:
- Persuasion and stakeholder buy-in.
- Recommendation defense and counterarguments.
- Team presentations and handoffs.
- More complex data/evidence tasks.

Essentials compression:
- Combine Lessons 1-2, 3-4, 5-7, 8-10, then finish with a short presentation task.
- Keep only core model examples and the simplest visuals.

## Model Case Strategy

Replace Ventura with three recurring model strands. These appear at different points in the curriculum to show how purpose changes design.

1. Process Improvement
   - Primary spine.
   - Example: reduce approval delays, improve onboarding, reduce rework, or shorten reporting time.
   - Best for: audience outcome, message/evidence, process visuals, recommendation, Q&A.

2. Product or Service Launch
   - Secondary model.
   - Example: launch a new internal tool, client service, or support program.
   - Best for: audience interest, benefit framing, visual hierarchy, feature-to-value language.

3. Project Results Briefing
   - Secondary model.
   - Example: quarterly results, pilot results, customer-feedback findings, cost-saving report.
   - Best for: charts, trend language, evidence quality, conclusions, next steps.

Each model gets:
- audience and presenter role
- business problem
- source data pack
- desired decision/action
- presentation outline
- visual sequence
- model language
- likely Q&A
- trainer notes / suggested answers

No 2014 Ventura material carries forward except as an internal example of what not to do.

## Deliverables

Plan execution should produce these files or artifacts:

1. Product specification and decision log.
2. 12-lesson curriculum map.
3. Three model-case packs.
4. Updated unit JSON for `books/Presentation Skills`.
5. Regenerated Essentials, Standard, and Long manuscripts.
6. Answer key / trainer notes.
7. Final presentation task and rubric.
8. Asset register with source, license/status, accessibility notes, and editability.
9. Editable deterministic assets where possible.
10. Updated image-generation prompts only after asset register approval.
11. Style and terminology sheet.
12. Built DOCX/PDF files after content and assets pass QA.

## Asset Strategy

Create assets only after curriculum and model cases are approved.

Use deterministic local creation for:
- planning maps
- structure cards
- storyboards
- tool-choice matrix
- UI mockups
- slide/PDF/dashboard before-after examples
- charts, tables, and accessibility comparisons
- rubrics and forms

Use OpenAI Images API for:
- cohesive icon sheets
- selected scenario illustrations
- high-quality cover concepts
- visuals where illustration quality matters and deterministic drawing would look weak

Use Canva only if:
- the template/output is business-appropriate for Japanese learners
- licensing/export terms are clear
- the asset can be reproduced or replaced later

Avoid:
- real tool screenshots in learner-facing materials unless explicitly approved
- logos and product UI details
- decorative scenario art that does not teach
- AI-rendered diagrams with exact text/count requirements
- inaccessible color-only examples

Every asset must include:
- teaching purpose
- location in course
- exact content/labels/data
- generation method
- source/licensing status
- alt text
- contrast/color-blind check
- editability requirement

## Multi-Agent Workflow

Use lean concurrent development: 4 bounded agents, then main-agent consolidation.

1. Curriculum Architecture Agent
   - Audits existing units against the 12-lesson map.
   - Outputs: keep/rewrite/merge/remove table and tier impact.

2. Model Case Agent
   - Designs the three model strands.
   - Outputs: case packs, data needs, visual sequence, Q&A prompts.

3. Asset Register Agent
   - Audits existing image register and generated assets.
   - Outputs: keep/revise/redraw/regenerate/remove decision per asset.

4. Pedagogy and QA Agent
   - Checks CEFR fit, learner journey, answerability, activities, rubric alignment.
   - Outputs: issues list and pass/fail acceptance checks.

Rules:
- Subagents do not edit repo files.
- Subagents do not call image APIs.
- Subagents cite source files and line references where possible.
- Main agent resolves conflicts and writes final implementation documents.

## Implementation Phases

1. Lock specification
   - Confirm target level, duration, series target, tier policy, and model-case strategy.
   - Outcome: decision log.

2. Build curriculum map
   - Convert the 12-lesson table into final tier mapping.
   - Outcome: approved unit architecture.

3. Build model cases
   - Create the three model-case packs before drafting units.
   - Outcome: reusable course spine.

4. Draft/rebuild units
   - Rewrite unit JSON in curriculum order.
   - Regenerate tier manuscripts after unit edits.
   - Outcome: coherent learner manuscripts.

5. Create answer/support materials
   - Add suggested answers, trainer notes, peer-feedback instructions, and rubric.
   - Outcome: teachable course, not just learner text.

6. Plan and create assets
   - Update asset register first.
   - Create deterministic assets.
   - Generate API images only after approval.
   - Outcome: complete visual package.

7. Production build
   - Update style map/reference DOCX if needed.
   - Build DOCX and export PDFs.
   - Outcome: publishable files.

8. QA and external review
   - Run internal checks.
   - Send final draft to Claude.ai and ChatGPT for one structured review round.
   - Outcome: issue log and final corrections.

## QA Checklist

Content:
- Standard tier has exactly 12 lessons.
- Each lesson has outcome, business task, model/example, practice, application, and assessment evidence.
- Learners build toward one final presentation.
- Three model strands are used intentionally, not randomly.
- B1-B2 language support is visible.
- Answer key/trainer notes exist for all non-obvious tasks.

Tool stance:
- PowerPoint appears as a common example, not as the course concept.
- Tool comparison does not become a software survey.
- Tool claims are checked against official sources or removed.

ESL language:
- Data language covers trends, comparison, approximation, percentages, percentage points, large numbers, decimals, currency, and source language.
- Q&A language covers clarifying, answering, deferring, disagreeing, checking satisfaction, and next steps.
- Japanese learner notes are included only where useful and accurate.

Accessibility:
- Textbook uses real heading structure.
- Tables are accessible.
- Instructional images have alt text.
- Diagrams meet contrast requirements.
- No meaning depends on color alone.
- Final PDF accessibility is checked as far as tooling allows.

Assets:
- Exact diagrams are deterministic.
- Generated people/scenario images follow Japan/East Asian representation requirements.
- No flags, emblems, seals, logos, or accidental product branding.
- Existing assets have reuse/licensing decisions.
- Every asset has editability and source notes.

Production:
- DOCX validates against reference styles.
- PDFs export cleanly via Word COM.
- Cross-references resolve.
- Metadata and title are updated only after final title decision.
- Essentials, Standard, and Long remain distinct.

## Assumptions and Defaults

- The implementation target is `books/Presentation Skills`, not the old standalone PDF.
- The old *Speaking with PowerPoint* file remains an archival source unless separately requested.
- Standard tier is the design spine; Essentials and Long are derived from it.
- B1-B2 is the default level.
- Twelve lessons means twelve Standard-tier lessons, not necessarily twelve files.
- Final title is intentionally deferred.
- OpenAI Images API is available but used after asset approval only.
- Official sources should be used for current tool claims; do not rely on memory for software features.
