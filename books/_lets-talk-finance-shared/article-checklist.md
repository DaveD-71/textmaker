# Per-Article QA Checklist — minimum criteria

Applies to **both** books (*Let's Talk Finance*, *Let's Talk Finance 2*). Run this against **one article** every time it is drafted or substantively revised, before it is treated as done. It is the minimum gate; the full whole-book audit is each book's `drafts/control/qa-checklist-full.md` and is run once per book in Phase 5.

Every box must be checked, or the failure noted with a reason, before the article passes. Keep a filled copy (or a one-line "passed / failed on X" note) in the batch record.

Rules referenced by `§` are in `house-style.md`.

---

## 1. Structure — the template is complete and correct

- [ ] Six subsections present, in order, correctly numbered `X.Y.1.`–`X.Y.6.`: Goal, Reading, Vocabulary Focus, Reading Questions, Discussion Questions, Source Notes.
- [ ] Topic title is `## X.Y. Title`; each subsection heading is `### X.Y.n. Name`.
- [ ] Goal is exactly one sentence, stating the teaching aim.
- [ ] Reading Questions: exactly 5, numbered 1–5.
- [ ] Discussion Questions: exactly 5, numbered 1–5.
- [ ] Source Notes: numbered list; the count of distinct `[N]` markers in the Reading equals the count of Source Notes, with no gaps (1,2,3…).

## 2. Reading — length and page fit

- [ ] Reading body is **~440–475 words** (count the Reading prose only, not headings or markers). A value outside ~420–490 needs a written reason.
- [ ] Reading is **3–6 inline `[N]` markers**.
- [ ] It will plausibly fill **one A4 page as a 2-column article** under the Goal block without overflow (§5). Confirmed exactly in the Phase 7 PDF loop; at draft stage the word count is the proxy.

## 3. Facts and sources

- [ ] At least **one real anchor case** — a named company, regulator, central bank, standard-setter, market event, transaction, vote, law, or crisis.
- [ ] At least **two factual anchors** total (number, date, name, %, monetary value, rating, specific requirement).
- [ ] **Every** factual anchor has an inline `[N]` marker.
- [ ] **Every Source Note URL was opened and checked during this pass.** It resolves to a stable, public page — regulator / central bank / standard-setter / official statistics agency / company IR or press page / established news outlet. No blogs, aggregators, undated explainer pages, or guessed URLs.
- [ ] Each Source Note gives enough to verify the fact: publisher, title, date where relevant, then the URL.
- [ ] Every time-sensitive claim is dated in the prose ("in 2024", "as of mid-2026").
- [ ] Any fictional or composite example is visibly hypothetical and is **not** the primary evidence for a point.
- [ ] Currency/number style per §3: non-USD = ISO code + space + number; USD = `US$` no space; no spelled-out currency name as a code substitute; `3.8%`, "percentage points" spelled out on first use.

## 4. Level — B1+/B2

- [ ] Sentences are mostly 15–25 words. No sentence has three or more subordinate clauses.
- [ ] Connectives are mainly "because / so / but / for example / this means". "However" and "as a result" only for genuine contrast or consequence.
- [ ] Every specialist term is explained in plain English in the sentence it first does real work, or the sentence before.
- [ ] Active voice dominates. Passive only where the actor is genuinely unknown or unimportant.
- [ ] No opaque idiom, metaphor, or finance-desk slang.

## 5. Paragraph writing (§ "Paragraph writing")

- [ ] Every paragraph break marks a real shift (new stage, new country/case, problem→response). No break splits one continuing idea just to shorten a paragraph.
- [ ] The Reading does **not** end on a lone single-sentence "moral" or "kicker" paragraph. The final paragraph is full and carries a substantive point (a fact, a real trade-off, or a concrete open question).
- [ ] The body never refers to itself, the classroom, the source page, or the article's usefulness.
- [ ] Paragraphs are cohesive and self-contained; no filler sentences.

## 6. Framing — global topic, Japanese vantage point (§1a)

- [ ] The article is about the **financial topic**, not about any one country.
- [ ] At least **three regions** appear (some mix of US, EU/euro area, UK, Japan, other Asia, Latin America, emerging markets). No single country dominates the word count or the structure; Japan is not named far more often than the others.
- [ ] The topic is framed the way a reader **based in Japan** meets it. Where the topic has a distinct Japanese baseline that changes how the reader should understand it, that baseline is stated (it is fine for a topic to have no Japan paragraph if none is needed).
- [ ] Tone toward Japan is informed and matter-of-fact — not lecturing the reader about their own country, not implying Japan is behind.
- [ ] Jurisdiction-specific rules are labelled (§4), and any rule that also appears in another topic is labelled the **same way** here.

## 7. Article shape and opening (§6)

- [ ] The article uses the shape assigned to it in the batch plan (data-led explainer / short chronology / two-case comparison / problem → responses / scenario → principle → trade-off) — not defaulting to scenario → principle → trade-off → moral.
- [ ] The opening style matches the one assigned in the batch plan, and is not a style already used by ~3 other topics in the book.
- [ ] The ending is specific to this article.

## 8. Questions

- [ ] The 5 Reading Questions are each answerable **from the text alone**, and across the set cover a mix: main idea, specific detail, cause/effect, inference, meaning-in-context, writer's purpose.
- [ ] The 5 Discussion Questions require extended reasoning, not one-word answers, and progress roughly analysis → evaluation → application.
- [ ] At least **one** Discussion Question is task-style: rank / advise / compare / diagnose / rewrite / design / prepare.
- [ ] No Discussion Question requires confidential or personal financial disclosure.
- [ ] Question stems vary within the topic (not all "Should… / How… / What…").

## 9. Vocabulary

- [ ] Vocabulary Focus lists **4–6 New terms** and **3–5 Recycled terms** (`none yet` only for the first topic of the book).
- [ ] Each Recycled term actually appears, naturally, in this topic's Reading or questions.
- [ ] New terms are finance-specific and important to the topic — not general business vocabulary.
- [ ] Every New and Recycled term for this topic exists (or is added this pass) in `drafts/control/vocabulary-map.md`, and the map's row for this topic matches the article's Vocabulary Focus line exactly.
- [ ] If a teacher answer book entry for this topic exists yet, its `**Target vocabulary:**` line matches this article's `**New terms:**` line exactly (direct comparison, not from memory).

## 10. Ledger and consistency

- [ ] No real case or specific statistic used here as **primary** evidence is already primary evidence in another topic (check `_lets-talk-finance-shared/topic-ledger.md`). A recognisable company reused with a **different** fact is fine.
- [ ] This topic's primary-evidence cases are recorded in the topic ledger's evidence register.
- [ ] If a teacher answer book entry exists, its `**Aim:**` line === this article's Goal sentence, word for word, and its 5 Reading answers match the **final** wording of this article.

---

## Result

```
Article:        <P.T Title>
Book:           A / B
Batch:          <n>
Reading words:  <n>       [N] markers: <n>       Regions named: <list>
Checked by:     <who>     Date: <YYYY-MM-DD>
Result:         PASS  /  FAIL
Failures / notes:
  -
```
