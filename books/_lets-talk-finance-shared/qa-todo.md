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

## 3. Editorial pass: word count and sentence length in Parts 3–4 (both books) ✅ DONE 2026-09-12

- [x] **Book A** — all 8 over-ceiling topics trimmed to 466-497 words (from 499-537w). Committed as `f083bd1`. `3.2` 500→466, `3.3` 537→474, `3.4` 512→472, `3.5` 527→473, `4.2` 499→485, `4.3` 500→484, `4.4` 512→495, `4.5` 509→497. (`3.1` 484w and `4.1` 479w were already in range, untouched.)
- [x] **Book A** — over-long sentences split back to two clean sentences where needed; verified citation integrity and Recycled-term presence on every edited article.
- [x] **Book B** — all 10 Part 3-4 topics trimmed to 483-498 words (from 497-544w). Committed as `499c94e`. `3.1` 497→483, `3.2` 506→492, `3.3` 531→488, `3.4` 510→498, `3.5` 497→483, `4.1` 519→498, `4.2` 512→498, `4.3` 544→496, `4.4` 516→480, `4.5` 530→491.
- [x] **Book B** — split several over-long em-dash sentences (up to 62 words, e.g. the `4.3` Saudi PIF sentence and the `4.4` "three things explain this" sentence) back into two sentences; longest sentence across the batch is now 45 words (a single clean em-dash sentence, accepted as in-range per the same precedent used in Book A).
- [x] Caught and restored factual anchors accidentally dropped mid-trim: Book B `3.3`'s "revealing exception" phrase (needed for Reading Question 5's wording) and "purchasing power" (a Recycled term); Book B `4.5`'s Swedish legal-duty-for-essential-goods-shops detail.
- [x] Verified on every edited article in both books: word count in range, citation markers == Source Notes (set comparison), all Recycled terms still present verbatim, Reading/Discussion Question wording still matches the edited text.

## 4. Fix currency-style violations ✅ DONE 2026-09-12

- [x] Book B `1-1_The_Cost_of_Living_and_Inflation.md` — "¥4,260" → `JPY 4,260`.
- [x] Book B `1-2_Debt_Credit_Cards_Mortgages_and_Loans.md` — "under £0.1 billion... more than £13 billion" → `GBP 0.1 billion` / `GBP 13 billion`.
- [x] Book B `1-5_Scams_Fraud_and_Financial_Self_Defence.md` — "up to £85,000 per claim" → `GBP 85,000`; "a record ¥72 billion... a further ¥127 billion" → `JPY 72 billion` / `JPY 127 billion`.
- [x] Full sweep of both books' `drafts/articles/` for bare `¥`/`£`/`€` found one violation the original audit missed: **Book A** `1-4_Data_Privacy_and_Protection.md` had bare `€1.2 billion` and `€6 billion` in prose — fixed to `EUR 1.2 billion` / `EUR 6 billion`. (Book A's audit had wrongly reported zero violations; this was caught by re-running the check rather than trusting the earlier finding.)
- [x] Two remaining bare-symbol hits (Book A `3-2_Infrastructure_Investment.md`, Book B `4-3_The_Business_of_Sport_Art_and_Culture.md`) are inside Source Note citation titles quoting the original article headline verbatim ("EU Faces €481 Billion...", "...record UK£6.7bn...") — correctly left as-is, not house-style violations.
- [x] Verified all 4 edited articles: citation markers == Source Notes, word counts unaffected (439-451w, all in range), zero bare currency symbols remaining in any Reading body.

## 5. Resolve the recycled-vocabulary floor gap — Book A only ✅ DONE 2026-09-12

- [x] `1.5` Financial Inclusion Initiatives — had a genuine 4-topic pool to draw from (1.1–1.4). Added "regulator" to the Pix sentence ("the central bank acted as regulator and infrastructure builder at once") — a real, non-forced addition. Now 3 recycled terms (*central bank, payment system, regulator*), meeting the floor. Updated the article's Vocabulary Focus line and `vocabulary-map.md`'s Topic Map row to match. Verified: word count 467 (in range), citation markers == Source Notes, all 3 recycled terms present verbatim.
- [x] `1.2` Central Bank Digital Currencies — user-approved decision: **document as an accepted exception**, not fix by forcing an unrelated term. It is the book's second topic; its only prior topic (1.1)'s term set (cryptocurrency, blockchain, crypto exchange, stablecoin, issuer, supervision) has almost no genuine overlap with 1.2's CBDC-mechanics content beyond the one term already recycled (*stablecoin*). Documented in `vocabulary-map.md`'s "Known limitation" section as a formal accepted exception — future audits should not re-flag this as an unresolved defect.

## 6. Build the missing Phase 5/6 deliverables (both books) ✅ DONE 2026-09-12

- [x] `Let's Talk Finance/drafts/articles/00_How_This_Resource_Is_Organized.md` — created, following the IR project's precedent format (4-Part structure summary, `Part.Topic` numbering explanation).
- [x] `Let's Talk Finance 2/drafts/articles/00_How_This_Resource_Is_Organized.md` — created, same treatment.
- [x] `Let's Talk Finance/drafts/glossary.md` — created via background agent, 133 entries covering every New/Target term across all 20 topics (mechanically cross-checked against `vocabulary-map.md`, zero gaps). Sourced from the actual article text for every definition, not from term names alone. Follows the IR project's glossary format exactly (`# X Glossary` → purpose paragraph → `## Terms` → alphabetical entries with `[Part.Topic]` tags).
- [x] `Let's Talk Finance 2/drafts/glossary.md` — same treatment via a second background agent, 122 entries. Two real gaps found on verification and fixed: (1) `"this time is different" thinking` (3.2) existed only as a mention inside two other entries, not as its own headword — added as a standalone entry; (2) `consumer protection` (recycled in 1.5) was listed in the article's own Vocabulary Focus line but the phrase did not actually appear anywhere in the article body — a pre-existing drift, likely from the item-3 length-trim pass. Fixed at the source: added "consumer protection" naturally into the UK bank-reimbursement sentence in `1-5_Scams_Fraud_and_Financial_Self_Defence.md`, verified word count (469, in range) and citation integrity unaffected, then added the glossary entry.
- [x] Ran the full three-way vocabulary check (article New/Recycled terms ↔ teacher-answer-book Target vocabulary ↔ glossary coverage) across all 40 topics, both books. Zero real mismatches found (all initial "mismatches" were parsing artifacts in the check script itself, verified by direct inspection) other than the one consumer-protection gap above, now fixed.
- [x] Populated `shared-term-bank.md` (previously empty): cross-checked all headwords in both glossaries, found exactly 7 exact collisions (bank run, central bank, consumer protection, exchange rate, progressive/regressive tax, stablecoin, stock index), verified all 7 consistent in meaning/scope/register between the two books (each illustrates with its own examples, which is expected), and added aligned reference entries for all 7.
- [ ] Not yet done: re-run the Phase 5 QA checklist's Glossary section and the front-matter line of the Whole-book section — both were N/A for lack of these files; now that the files exist, a fresh checklist pass can evaluate them. Deferred to the "After all of the above" full re-audit rather than done piecemeal here.

## 7. Minor / cosmetic

- [ ] Book B — several topics cite Source Notes out of strict numeric order (e.g. `3-1_What_Moves_Stock_Markets.md` cites `[7]` before `[1]`). Every marker still resolves correctly and no note is orphaned — cosmetic only, renumber to sequential order if doing a pass on these files anyway.
- [ ] Book B `4.5. The Future of Money` — leans on essentially two countries (Sweden, Japan) for its comparative weight; not a violation but thinner than the "≥3 regions" spirit. Consider whether a third region needs slightly more presence at the next edit pass.
- [ ] **Deferred idea (2026-09-12):** consider adding a `**Recycled vocabulary:**` line to both books' `teacher-answer-book.md` files, alongside the existing `**Target vocabulary:**` line, so the teacher-book reflects the article's full Vocabulary Focus section rather than only New terms. Checked against the IR project's own teacher answer book as precedent — the IR file uses only a single `**Target vocabulary:**` line per topic (New/target terms only), no separate Recycled line, so this would be a new enhancement beyond the IR precedent, not something to bring into parity with it. Not needed to resolve item 5 above (that only touched the article's own Vocabulary Focus line and `vocabulary-map.md`). Revisit only if the user asks for it explicitly.

---

## After all of the above

- [ ] Re-run the full Phase 5 whole-book QA audit (`qa-checklist-full.md`) on both books to confirm all items above are resolved and nothing regressed.
- [ ] Only then proceed to Phase 6 (assemble: Part dividers, front matter, numbering) per `PROJECT-PLAN.md` §5.
