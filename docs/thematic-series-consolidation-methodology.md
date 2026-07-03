# Thematic Series Consolidation Methodology

Reusable process for merging a set of thematically related textbooks (a "series") into a
new unified book offered at multiple course-length tiers (e.g. Essentials / Standard / Long).

First applied to: **Presentation Skills** (2026-07), consolidating *Speaking with PowerPoint*,
*Making Speeches*, *Business Presentations Essentials for Businesspeople*, and *Business
Presentations Essentials for Government Officials*. See
[presentation-skills-consolidation-plan.md](presentation-skills-consolidation-plan.md) for the
applied instance.

Next planned application: **Meeting Skills** series.

## Why this exists

This company holds several small clusters of thematically overlapping books, often split by
audience (businesspeople vs. government officials) or by delivery medium (with/without slides),
written by the same authors over time and sharing near-identical frameworks under slightly
different names. Left alone, each new course request forces a from-scratch rewrite or a
audience-forked duplicate book. This methodology replaces that with a repeatable content-audit →
design-decision → build pipeline, so the outcome is consistent across series and connects to a
single brand voice rather than reading as N independently-authored books stitched together.

## Process

### Step 1 — Inventory the source books
List every book in the thematic cluster, confirm which already have `docx-to-markdown` output
(check each book's `out/.md/` folder before reconverting anything — do not regenerate what
already exists).

### Step 2 — Parallel content mapping (one agent per book)
Read every real content unit of every book (skip image-only placeholder files) and produce a
structured per-unit report covering:
1. Unit title and core topic/skill
2. Named frameworks/models introduced (quote the actual names used in-book)
3. Language/expression content categories taught
4. Practice activities and model speeches/scenarios, with their audience/context
5. Audience-specific vs. generic-skill flag — for any audience-forked book pair, explicitly
   separate "the skill being taught" from "the scenario dressing it's wrapped in"
6. Dated or modernization-flagged content
7. A tier judgement: does this unit's content feel like essentials/short-course material, or
   does it belong to a standard/long extended treatment?

Run these as parallel background agents (one per book) so mapping scales with series size
without consuming the main conversation's context on raw reading.

### Step 3 — Cross-book synthesis (main thread)
Once all book reports are back, build a cross-reference table of shared frameworks (which books
have which named model, and how the naming/depth differs between them) plus a list of each
book's genuinely distinctive, non-duplicated content. This surfaces:
- Which frameworks need a single canonical "best-of" synthesis (the common case — see Step 4)
- Which content is unique to one book and must be preserved deliberately rather than dropped
  during consolidation
- Where audience-specific content actually concentrates (in this series and the prior one,
  it concentrated almost entirely in model speeches/scenarios, not in skill instruction — verify
  this empirically per-series rather than assuming it, but expect the same pattern)
- Cross-cutting gaps no source book addresses (e.g. virtual/hybrid delivery was absent from
  all four Presentation Skills books) — these become explicit "new content" line items, not
  something to leave implicit

### Step 4 — Design decisions (require explicit user sign-off, do not assume)
Always raise these as decisions, not defaults:
1. **Framework naming/synthesis** — when multiple books name the same concept differently
   (e.g. "Four Keys" vs. "6 Keys"), default recommendation is a best-of synthesis into one
   canonical name/version, but confirm with the user rather than picking silently.
2. **Audience-fork handling** — if the series has an audience-split book pair, confirm whether
   to eliminate the split at book level (folding audience variants into paired models/examples
   within one unit) as was done here, or keep some other split structure. Don't assume the
   same resolution applies to every series without asking.
3. **Modernization scope** — confirm whether flagged gaps (e.g. new delivery-mode content) get
   built as new material in this pass or explicitly deferred as future work.
4. **Tier-inclusion granularity** — this is the one most likely to need real back-and-forth
   rather than a single clean rule. Do not assume "cut whole units for Essentials, keep whole
   units for Standard/Long." In practice content splits three ways per unit:
   - Essentials-only or Long-only content (some units genuinely don't belong in every tier)
   - Abridged/standard/extended depth of the *same* unit across all three tiers (most units)
   - Reference/appendix material that simply grows across tiers rather than being taught
   Design this per-unit, in a table, and get sign-off on the table before drafting.
5. **Manuscript structure** — one master source with tier tags/filtering, or separate
   per-tier manuscripts built from shared source units. This has real tooling implications
   (affects how `markdown-to-docx` / unit-splitting conventions get used) and should be
   decided before drafting starts, not discovered mid-build.

### Step 5 — Record the plan
Every consolidation project gets a project-specific plan file in `docs/`
(`docs/<series-name>-consolidation-plan.md`) capturing: the source inventory, the cross-book
synthesis table, the proposed unified unit list with tier mapping, and the resolved design
decisions from Step 4. This file is the durable record — it's what a future session (or a
different series' consolidation) should be able to read to understand not just what was
decided, but why, so the same decisions don't need to be re-litigated from scratch and the
methodology itself can be refined based on what worked.

## Standing conventions across series

- **Model speeches/scenarios are the audience-fork point, not units or books.** Confirmed
  independently across the Presentation Skills business/government pair: skill instruction was
  ~85% audience-agnostic, with audience flavor concentrated in worked examples. Treat this as
  the working hypothesis for the next series, but verify per-series in Step 3 rather than
  assuming.
- **Tiering is a depth/selection design problem per unit, not a single global rule.** Resist
  collapsing this to "short course = fewer units." Some units are tier-exclusive, most are
  depth-scaled, reference material accretes.
- **Flag modernization gaps explicitly, don't silently fix or silently ignore them.** Dated
  software UI references, pre-cloud backup advice, and — recurring across this series — no
  virtual/hybrid delivery content at all, should surface as named decisions in Step 4, not
  disappear into either an unreviewed rewrite or an unreviewed omission.
- **Reuse existing `out/.md/` conversions before reconverting anything.** Check book folders for
  prior `docx-to-markdown` output first; do not regenerate from DOCX unless no split markdown
  exists yet.

## Revision history

- 2026-07-03: Initial methodology written during Presentation Skills consolidation planning.
