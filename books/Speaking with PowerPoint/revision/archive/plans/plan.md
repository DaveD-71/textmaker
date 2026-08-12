# Speaking with PowerPoint 2026 Rewrite and Asset Plan

## Summary

Create `books/Speaking with PowerPoint/Speaking with PowerPoint - 2026 Rewrite and Asset Plan.md` as a series-feeder implementation plan for rebuilding the existing `books/Presentation Skills` series units and assets using the consolidated 2026 task list.

Default decisions:

- Treat this as a rebuild of the existing Presentation Skills series units, not a standalone book.
- Defer final title until content decisions are complete.
- Use a lean multi-agent workflow: 4 bounded agents, no open-ended parallel drafting.
- Make the course tool-agnostic: “presenting with visuals,” not PowerPoint.
- Use only business-appropriate tools accessible to Japanese businesspeople as examples.

## Key Changes

- Rebuild affected `books/Presentation Skills` units around:
  - audience outcome, decision/action, and business purpose
  - tool/format choice across slides, PDFs, dashboards, documents, and screen shares
  - visual design principles independent of software
  - online/hybrid delivery as cross-cutting content
  - accessibility, AI use, data storytelling, and Q&A
- Recommended tool examples:
  - Core business tools: Microsoft 365/PowerPoint, Google Slides, Canva, Keynote
  - Specialist/team tools: Figma Slides for design/product teams
  - AI-first example: Gamma, with caution about company policy and confidentiality
  - Non-slide formats: PDF decks, dashboards, spreadsheet/chart walkthroughs, document walkthroughs
- Avoid real product screenshots/logos in learner-facing assets unless explicitly approved. Use clean generic UI mockups to reduce copyright, maintenance, and localization risk.

## Multi-Agent Workflow

Use 4 short-lived agents, each with a bounded brief and expected output:

1. Content Architecture Agent
   - Compare the consolidated task list against `books/Presentation Skills/units/*.json`.
   - Identify which units need full rewrite, partial rewrite, or no change.
   - Output a unit-by-unit rebuild map.

2. Tool-Agnostic Modernization Agent
   - Audit Units 1, 4, 6, 10-15 for PowerPoint-only assumptions.
   - Propose replacements using tool-neutral language and business-appropriate example tools.
   - Verify current tool claims from official sources only.

3. Asset Planning Agent
   - Audit `books/Presentation Skills/images/image_register.json` and generated assets.
   - Mark assets as reuse, revise, replace, or create new.
   - Produce an asset register update plan before any API calls.

4. Pedagogy and QA Agent
   - Check learner activities, rubrics, ESL usefulness, and final assessment flow.
   - Ensure the rebuild does not become a software tutorial.
   - Produce acceptance checks for each tier: Essentials, Standard, Long.

The main agent consolidates all outputs, resolves conflicts, and writes the final plan file. Do not allow subagents to generate images or edit files directly.

## Asset Creation Strategy

- Use deterministic local generation first:
  - Python/PIL or SVG for diagrams, framework maps, process flows, chart examples, UI mockups, accessibility examples, and before/after visuals.
  - HTML/CSS rendered via Playwright for polished generic screen mockups.
  - Open-source icon sets such as Lucide, Tabler, or Material Symbols for simple icons.
- Use OpenAI Images API when quality benefits justify cost:
  - scenario illustrations
  - cohesive icon sheets
  - cover/background concepts
  - high-polish visual metaphors
- Use Canva as a design/reference tool when free or already available:
  - business-appropriate layout inspiration
  - possible manually exported templates if licensing/export rights are clear
- Do not use paid/API generation until the asset register is approved.
- Batch OpenAI image calls by style and reuse existing art through deterministic compositing wherever possible.

## Implementation Phases

1. Discovery and Gap Map
   - Read consolidated task list, existing series plan, tier manuscripts, unit JSON, image register, and generated manifest.
   - Produce a gap matrix: task-list item -> current series status -> required action.

2. Content Rebuild Plan
   - Rewrite the unit map for the series.
   - Identify exact units needing replacement content, especially visual design, delivery, data storytelling, AI, accessibility, and tool choice.
   - Preserve useful existing frameworks only if they fit the tool-agnostic direction.

3. Asset Register Plan
   - Classify every existing asset:
     - keep
     - revise text/labels only
     - redraw deterministically
     - regenerate with OpenAI
     - remove
   - Add new required assets for tool/format choice, generic tool workflows, data storytelling, accessibility, AI critique, and online/hybrid presenting.

4. Drafting and Build Plan
   - Update unit JSON first, then regenerate tier manuscripts.
   - Keep Essentials/Standard/Long as separate manuscripts, consistent with the current series architecture.
   - Update style-map/reference-DOCX needs after content and asset scope are fixed.

5. QA and Review Plan
   - Run content review against the consolidated task list.
   - Run visual review against the asset register.
   - Build DOCX/PDF only after content and assets pass.
   - Have Claude.ai and ChatGPT review the final plan or rebuilt draft using the same acceptance criteria.

## Test Plan

- Static checks:
  - No learner-facing text treats PowerPoint as the default tool.
  - No 2014/2016/Ventura legacy material remains unless intentionally referenced as “old example.”
  - All tool claims are sourced from official docs or removed.
- Content checks:
  - Every unit has learning outcomes, guided practice, and clear acceptance criteria.
  - Essentials, Standard, and Long remain meaningfully distinct.
  - AI, accessibility, online/hybrid, and data-storytelling content appear where required.
- Asset checks:
  - Every asset has an ID, purpose, source method, licensing/status, and reuse/regenerate decision.
  - Generated people/scenario images follow the existing Japan/East Asian representation and no-flags/no-emblems constraints.
  - Diagrams with exact text/count requirements are deterministic, not model-rendered text.
- Build checks:
  - Validate DOCX styles against reference.
  - Export PDFs via Word COM.
  - Visually inspect PDFs for layout, image clarity, page flow, headings, and cross-references.

## Assumptions

- Final title will be chosen after the content architecture is stable.
- The existing `books/Presentation Skills` series is the implementation target.
- OpenAI Images API is acceptable for high-value assets, but usage should be batched and minimized.
- Canva may be considered, but only where output quality, business appropriateness, and licensing are clear.
- The plan file itself will be saved during execution mode, not while still in Plan Mode.

## Feedback and plan revision

Both ClaudeAI and ChatGPT were asked to review the two main files and provide feedback.

### Main files

'books\Speaking with PowerPoint\revision\Speaking with PowerPoint - 2026 Consolidated Revision Task List.md'

'books\Speaking with PowerPoint\revision\archive\plans\plan.md'

### ChatGPT says

'books\Speaking with PowerPoint\revision\feedback\ChatGPT\chatgpt_plan_feedback.md'

### ClaudeAI says

'books\Speaking with PowerPoint\revision\feedback\Claude.ai\claudeai_plan_feedback.md'

### Codex says

Both sets of feedback from the two AIs were shared with Codex. Here is the response.

Read both feedback files.

Main takeaway: Claude.ai and ChatGPT agree that `plan.md` is not execution-ready yet. The core issue is not asset generation or agents; it is that the plan does not yet define the actual textbook/curriculum product clearly enough.

Their shared criticisms:

- `plan.md` silently shifts scope from revising *Speaking with PowerPoint* to rebuilding the broader `Presentation Skills` series. That may be correct, but it needs to be explicit and reconciled with the task list.
- The plan lacks a real unit/curriculum map: outcomes, business task, language focus, activity, asset needs, and assessment evidence per unit.
- The original two-day sprint framing is incompatible with the current multi-tier series rebuild plan. The plan needs separate tracks for editorial rewrite vs. later production/build.
- P0 decisions are not closed, especially the new model/case strategy and target learner statement.
- Assets are too prominent too early. Instructional design should come first; asset creation should follow approved unit/case design.
- The plan needs target CEFR level, course duration, learner journey, model answers/trainer notes, final task, rubric, and accessibility QA for both textbook and assets.
- Tool-agnostic is right, but ChatGPT warns against turning the book into a software survey. Better principle: teach durable visual communication; PowerPoint is one common example, not the course concept.

My recommendation: revise `plan.md` substantially before implementation. The next version should start with a product specification and curriculum map, then define the model case, then plan assets and agent workflow around that. The current plan is useful as a production/agent workflow draft, but not yet as the master rewrite plan.
