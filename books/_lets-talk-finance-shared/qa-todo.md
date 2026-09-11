# Let's Talk Finance — QA Fix TODO

Source: Phase 5 whole-book QA audit, 2026-09-12 (two background agents, one per book, full read against `qa-checklist-full.md`). Findings-only pass — nothing below has been fixed yet. Full detail in `project-journal.md` 2026-09-12 entry. Re-run the whole-book audit once these are addressed.

Ordered by priority (most significant first).

---

## 1. Fix cross-topic evidence duplication — Silicon Valley Bank ✅ DONE 2026-09-12

- [x] **Book A** `drafts/articles/2-4_Stress_Testing_and_Risk_Management.md` used the same SVB "$40 billion in a single day" statistic as **Book B** `drafts/articles/2-5_Banks_What_They_Do_and_How_They_Fail.md`'s primary opening evidence. Confirmed by direct read.
- [x] Fixed: replaced the SVB case in Book A 2.4 with **Signature Bank** (failed 12 Mar 2023, ~US$110bn assets, well below the US$250bn mandatory-stress-test threshold, lost ~20% of deposits in hours on 10 Mar via contagion from SVB's collapse two days earlier) — a distinct, independently-sourced case making the same teaching point (a test only measures the risk it's designed to measure). Book B's SVB-anchored article was left untouched, since SVB is load-bearing there (Goal, Reading, both Reading Questions 1-2, and Discussion Question 2 all build on it).
- [x] Updated Reading Questions 3-4 (Silicon Valley Bank → Signature Bank), Source Note [3] (now FDIC's 27 Mar 2023 remarks on the 2023 bank failures), added Source Note [4] (BOJ Financial System Report, for the unrelated Japan joint-stress-test sentence that had been mis-piggybacking on the old [3]).
- [x] Updated the Book A teacher-answer-book 2.4 section (Reading answers 3-4, Discussion answers 2-5) to match — verified Goal==Aim, 5+5 answer counts, citation integrity, zero remaining SVB references.
- [x] Updated `topic-ledger.md`'s evidence register: Signature Bank now has its own primary-evidence row under A 2.4; the SVB row is annotated as B 2.5's sole primary use across both books.
- [ ] Not yet done: `company-and-geography-audit.md` backfill (item 2 below) should record Signature Bank under A 2.4 once that file is populated.

## 2. Backfill the company-and-geography-audit control files ✅ DONE 2026-09-12

- [x] `Let's Talk Finance/drafts/control/company-and-geography-audit.md` — backfilled from `topic-ledger.md`'s evidence register (all 20 topics, geographic-balance tally, company/case frequency cross-check against the ledger's own "Also referenced" column). Region tags are keyword-derived from the ledger text, not a fresh re-read — two topics (1.4, 2.4) flagged as reading thin (only 2 detected regions) for a manual double-check, not treated as confirmed gaps.
- [x] `Let's Talk Finance 2/drafts/control/company-and-geography-audit.md` — same treatment. Found and fixed a real gap while backfilling: **topic 1.1 (the book's own prototype topic) had never been added to `topic-ledger.md`'s evidence register at all** — added it now. Three topics (2.1, 3.2, 1.1) flagged thin for a manual double-check. Also flagged: Book B alone has zero Latin America primary topics (Book A covers it twice, so the two books together are fine, but Book B alone is thin there).
- [x] Both files now record Signature Bank (A 2.4) and confirm SVB is used as primary evidence only in B 2.5 — consistent with the item-1 fix.
- [ ] Not yet done: a full manual re-read to confirm the keyword-derived region tags on the ~5 flagged "thin" topics above (this was a data-driven backfill from the ledger, not a fresh close read of all 40 articles — the two QA audit agents already did that close read and found the geography solid in both books, so this is a low-priority follow-up, not a known defect).

## 3. Editorial pass: word count and sentence length in Parts 3–4 (both books)

- [ ] **Book A** — topics running over the ~490-word ceiling, worst first: `3.3` Trade Policies and Tariffs (537w), `3.5` Global Economic Recovery Post-COVID (527w), `4.4` Corporate Governance (512w), `3.4` Pension Reform (512w), `4.3` Wealth Inequality (500w), `3.2` Infrastructure Investment (500w), `4.2` Financial Literacy (499w), `4.5` Economic Diplomacy (509w), `2.1` How Companies Raise Money (490w).
- [ ] **Book A** — sentences at or above 40 words needing a split, worst first: `4.3` (47w), `4.4` (44w), `4.5` (43w), `4.2` (42w), `3.2` (42w), `4.1` (41w).
- [ ] **Book B** — topics over the ~490-word ceiling, worst first: `4.3` Business of Sport, Art and Culture (544w), `3.3` Commodities (531w), `4.5` Future of Money (530w), `4.1` Tax (519w), `4.4` Philanthropy (516w), `4.2` Government Debt (512w), `3.4` Currencies (510w), `3.2` Bubbles (506w), `3.1` What Moves Markets (497w), `3.5` Emerging Markets (497w).
- [ ] **Book B** — sentences at or above 40 words needing a split: `4.5` (44w), `3.2`/`3.3` (41w each), `3.5`/`4.1`/`4.4` (40w each).
- [ ] Note: this is a batch-level pattern (Parts 1–2 in both books sit close to target), not scattered outliers — do the whole Part 3–4 set together per book rather than topic by topic.

## 4. Fix currency-style violations — Book B only

- [ ] `1-1_The_Cost_of_Living_and_Inflation.md` — "¥4,260" → `JPY 4,260`.
- [ ] `1-2_Debt_Credit_Cards_Mortgages_and_Loans.md` — "under £0.1 billion... more than £13 billion" → `GBP 0.1 billion` / `GBP 13 billion`.
- [ ] `1-5_Scams_Fraud_and_Financial_Self_Defence.md` — "up to £85,000 per claim" → `GBP 85,000`; "a record ¥72 billion... a further ¥127 billion" → `JPY 72 billion` / `JPY 127 billion`.
- [ ] Check no other bare `¥`/`£`/`€` symbols were missed elsewhere in Book B (Book A had zero violations on the same check).

## 5. Resolve the recycled-vocabulary floor gap — Book A only

- [ ] `1.2` Central Bank Digital Currencies — only 2 recycled terms (*central bank, stablecoin*) against the checklist's 3–5 floor.
- [ ] `1.5` Financial Inclusion Initiatives — only 2 recycled terms (*central bank, payment system*).
- [ ] Decide: add one more genuinely-appearing recycled term to each, **or** formally document an accepted exception in `vocabulary-map.md` (it already self-notes this as a known limitation, but the rule itself is still technically unmet).

## 6. Build the missing Phase 5/6 deliverables (both books)

- [ ] `Let's Talk Finance/drafts/glossary.md` — does not exist yet.
- [ ] `Let's Talk Finance 2/drafts/glossary.md` — does not exist yet.
- [ ] `Let's Talk Finance/drafts/articles/00_How_This_Resource_Is_Organized.md` (front matter) — does not exist yet.
- [ ] `Let's Talk Finance 2/drafts/articles/00_How_This_Resource_Is_Organized.md` — does not exist yet.
- [ ] Once the glossaries exist, run the full three-way vocabulary check (article New/Recycled terms ↔ teacher-answer-book Target vocabulary ↔ glossary `[Part.Topic]` tags) — currently only the first two legs are checkable.
- [ ] Re-run the Phase 5 QA checklist's Glossary section and the front-matter line of the Whole-book section, both currently N/A for lack of these files.

## 7. Minor / cosmetic

- [ ] Book B — several topics cite Source Notes out of strict numeric order (e.g. `3-1_What_Moves_Stock_Markets.md` cites `[7]` before `[1]`). Every marker still resolves correctly and no note is orphaned — cosmetic only, renumber to sequential order if doing a pass on these files anyway.
- [ ] Book B `4.5. The Future of Money` — leans on essentially two countries (Sweden, Japan) for its comparative weight; not a violation but thinner than the "≥3 regions" spirit. Consider whether a third region needs slightly more presence at the next edit pass.

---

## After all of the above

- [ ] Re-run the full Phase 5 whole-book QA audit (`qa-checklist-full.md`) on both books to confirm all items above are resolved and nothing regressed.
- [ ] Only then proceed to Phase 6 (assemble: Part dividers, front matter, numbering) per `PROJECT-PLAN.md` §5.
