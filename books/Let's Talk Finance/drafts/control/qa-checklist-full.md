# Let's Talk Finance (Book A) — Full QA Checklist (whole book, Phase 5)

**For the per-article minimum gate, use `../../_lets-talk-finance-shared/article-checklist.md` instead — run that on every article as it is drafted or revised.** This file is the whole-book audit, run once per book in Phase 5 (and re-run after any late change). Adapted from the *Let's Talk: Investor Relations* revision QA checklist; the IR project's six audit passes are the evidence that each line catches a real, recurring defect (bracketed notes say which).

Companion: `../../Let's Talk Finance 2/drafts/control/qa-checklist-full.md` (structurally identical).

---

## Article content

- [ ] The Reading uses at least one real company, regulator, central bank, standard-setter, market event, transaction, vote or crisis.
- [ ] The Reading has at least two factual anchors (numbers, dates, names, places, percentages, values, rating changes, reporting requirements).
- [ ] Every factual anchor has an inline `[N]` marker resolving to a Source Note.
- [ ] Every Source Note URL was checked live and resolves to a stable public page (regulator, central bank, standard-setter, company IR/press page, established news outlet). No blogs, aggregators, or undated explainer sites.
- [ ] Fictional or composite examples, if any, are visibly hypothetical and secondary — never the primary evidence for a point.
- [ ] The same real case / company event / statistic is not used as **primary** evidence in more than one topic. Check `../../_lets-talk-finance-shared/topic-ledger.md` evidence register. [IR had 5 substantial cross-topic duplications.] Light one-sentence callbacks are fine.
- [ ] The Reading is company-neutral: the topic does not require knowledge of one specific company.
- [ ] **Japanese vantage point:** the topic is framed the way a reader based in Japan meets it, then widened out — not written as a non-Japanese default with Japan as an aside. Where the topic has a distinct Japanese baseline that changes how the reader should understand it (deflation / lost decades, BOJ 2% target and 2024 rate lift-off, weak yen, early crypto rules, ageing & pensions, high cash savings, NISA, TSE governance reform, housing depreciation, consumption tax), that baseline is stated. Not every topic needs a Japan paragraph. [First prototype pass got the framing wrong: "People often ask why central banks do not aim for zero inflation" assumed a non-Japanese reader.]
- [ ] **Global perspective, no single country dominant.** The Reading covers the topic across at least three regions (some mix of US, EU/euro area, UK, Japan, other Asia, Latin America, emerging markets). No one country dominates the word count or the structure, and Japan is not named far more often than the others. [Prototype pass 2 over-corrected into a Japan-centred article — equally wrong.]
- [ ] Tone toward Japan is informed and matter-of-fact — not lecturing the reader about their own country, not implying Japan is behind.
- [ ] Jurisdiction-specific rules are labelled (`house-style.md` §4), and the **same rule is labelled the same way every time it appears across the book**. [IR: Topic 1 used a US rule without the "U.S.-specific" label that other topics used for the same rule.]
- [ ] The Reading is understandable with no outside reading.
- [ ] No unsupported claims, promotional language, or overgeneralization.
- [ ] Currency figures follow `house-style.md` §3 (ISO code + space for non-USD; `US$` no space for USD; no spelled-out currency name as a code substitute).

## Structure and style variety

- [ ] The opening style is not shared by more than ~3 topics in the book. Spread across: dated event, concrete scene, surprising number, short comparison, common misconception, direct question. [IR: 8 of 20 topics opened "On [date], X happened".]
- [ ] The topic uses its assigned article shape (data-led explainer / short chronology / two-case comparison / problem → responses / scenario → principle → trade-off). Shapes assigned per topic in the batch plan before drafting.
- [ ] The article does not follow only the pattern scenario → principle → trade-off → generic moral.
- [ ] Paragraphs have clear logical movement; they are not isolated sentences. 3–5 sentences each.
- [ ] The ending is specific to this article, not a generic "good regulation means…".
- [ ] The Reading is ~440–475 words. Outliers only if a shorter article is clearly stronger, and noted in writing.

## Level (B1+/B2)

- [ ] Sentences mostly 15–25 words; at most one subordinate clause is routine, two is the ceiling.
- [ ] Connectives are mostly "because / so / but / for example / this means"; "however" and "as a result" reserved for genuine contrast/consequence.
- [ ] Each new term is defined in plain English in the sentence it first does real work, or the sentence before.
- [ ] Active voice dominates; passive only where the actor is genuinely unknown/unimportant.
- [ ] No opaque idiom or finance-desk slang.

## Questions

- [ ] Exactly 5 reading questions and 5 discussion questions.
- [ ] Reading questions cover a mix: main idea, detail, cause/effect, inference, meaning-in-context, writer's purpose.
- [ ] Every reading question is answerable from the text alone.
- [ ] Discussion questions invite extended reasoning, not one-word answers.
- [ ] At least one discussion question is task-style: rank / advise / compare / diagnose / rewrite / design / prepare.
- [ ] No discussion question requires confidential or personal financial disclosure.
- [ ] Question stems are varied within the topic and across the book (not all "Should…/How…/What…").
- [ ] The teacher answer book's Reading answers match the **final** article wording — verified by direct comparison, not by trusting an earlier pass. [IR: 4 answer-book answers had drifted from the article after edits.]

## Vocabulary

- [ ] The topic lists 4–6 New terms and 3–5 Recycled terms (`none yet` only for topic 1.1).
- [ ] Recycled terms actually appear, naturally, in this topic's Reading or questions.
- [ ] New terms are finance-specific and important to the topic — not general business vocabulary.
- [ ] Terms with a jurisdiction limit carry a note in the glossary.
- [ ] `vocabulary-map.md` records this topic's first-introduction and recycling accurately; its Topic row matches the article's Vocabulary Focus section.
- [ ] **Three-way match, checked by direct comparison** [IR: 3 topics had a mismatch here]:
  - the Reading's `**New terms:**` line
  - the teacher answer book's `**Target vocabulary:**` line for this topic
  - the glossary's `[Part.Topic]` tags on those terms

## Source and teacher support

- [ ] Source Notes are complete enough for a teacher to verify each fact.
- [ ] The teacher answer book has, for this topic: a one-line Aim, the 5 Reading answers, and discussion angles (what a strong answer covers, plus the main alternative view where the question is open).
- [ ] The topic's `### Goal` sentence === the teacher book's `**Aim:**` line, word for word.
- [ ] A confidentiality/sensitivity reminder is present where the topic could invite personal or confidential disclosure.

## Glossary (whole-book, Phase 5)

- [ ] Every glossary entry's example matches the **current** article for that entry's `[Part.Topic]` tag(s) — checked entry by entry, not from a flagged subset. [IR: 11 stale examples found on full re-check vs 8 originally flagged.]
- [ ] No leftover company names from superseded drafts anywhere in the glossary (sweep for names dropped during rebalancing).
- [ ] Every term in any topic's Vocabulary Focus has a glossary entry.
- [ ] Glossary intro's claim ("terms found across all 20 topics") holds: every topic 1.1–4.5 has ≥1 glossary term tagged to it.
- [ ] Letter headers present and complete (A, B, C, … — no missing letters for letters that have entries). [The old flat LTF glossary was missing its `F` header.]

## Whole-book, Phase 5

- [ ] All 20 topics present, correctly numbered Part.Topic, in Part order.
- [ ] Front matter `00_How_This_Resource_Is_Organized.md` present and matches the final Part/topic structure.
- [ ] Cross-topic callbacks (light references) all resolve to a topic that exists and precedes or is clearly cross-referenced.
- [ ] No two topics' Readings share an opening sentence structure verbatim.
- [ ] Geographic spread: no single country dominates the book's real-world examples.
- [ ] The three content fixes are done: 1.3 Fintech (correct topic, not market-fragmentation filler), 4.1 AML (correct topic, not AI-in-finance filler), 1.4 Data Privacy (opening sentence repaired).
