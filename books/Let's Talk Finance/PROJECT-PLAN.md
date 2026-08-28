# Let's Talk Finance — Two-Book Project Plan

Written 2026-08-28. Supersedes `EDIT-LIST.md` (patch-in-place, abandoned) and the interim single-book `REBUILD-PLAN.md` (renamed to this file). Driven by review of the completed **Let's Talk: Investor Relations** project at
`\\prod-fs-gen01\WorkFile\04_在宅勤務\★グローバルビジネス推進部（在宅）\ランゲージサービス課\Dobson（在宅）\02. Clients\Marubeni\Ishida, Tetsuya\materials\drafts\`.

---

## Scope: two books

| | **Book A — Let's Talk Finance (new edition)** | **Book B — Let's Talk Finance 2** |
|---|---|---|
| Content | Rebuild of the existing 20 topics, from scratch | 20 **new** finance topics, not overlapping Book A |
| Status of current material | The ChatGPT-generated `Let's Talk Finance.docx` is a first draft: no citations, no vocabulary system, no control layer, unspecified level, 2 articles with the wrong reading text (04, 05), 1 malformed sentence (06), ~15 wrong glossary cross-refs. Discarded — subjects kept, prose not. | New — topic list proposed in §3 below, for approval |
| Standard | Both books built to the **IR resource standard** (see §1), following `Book_Draft_And_Edit_Process_Guide.md` | same |
| Format identity | `Let's Talk` reading-and-discussion, 6-subsection topic template | same |
| Relationship | Companion volumes: same format, same level, same glossary conventions, shared control layer. Each is a complete standalone book with its own glossary and teacher answer book; topic lists must not overlap. | same |
| Location | `books/Let's Talk Finance/` | `books/Let's Talk Finance 2/` (new folder, same repo) |

**Build order (agreed):** *prototype both, then parallel.* One calibration prototype covering both books → lock the shared spec → draft A and B in parallel Part-sized batches.

---

## 1. The IR standard (the target for both books)

Verified against the IR project's `Investor_Relations_Resource_Project_Plan.md`, `IR article revision QA checklist.md`, `IR resource vocabulary map.md`, `IR industry glossary.md`, `IR teacher answer book.md`, and the 20 shipped article files.

### 1.1 Per-topic template — six subsections, numbered under the topic

Topic numbering is **Part.Topic** (e.g. `2.4`); subsections numbered under it (`2.4.1. Goal`, `2.4.2. Reading`, …):

| # | Subsection | Spec |
|---|---|---|
| .1 | **Goal** | One sentence, teaching aim. Heading 3. Matches the teacher book's `**Aim:**` line word-for-word. |
| .2 | **Reading** | **Must fill exactly one A4 page as a 2-column article, under the Goal block, with no overflow to a second page.** This is the binding constraint (D3); word count is only a proxy for it. In the shipped IR book that meant **~440–475 words with 3–6 inline `[N]` citation markers** (all 20 IR Readings: 422–487 words, mean ~453, none reached 500). Short classroom paragraphs. ≥1 real company/regulator/event/transaction; ≥2 factual anchors (numbers, dates, names, %, values). Every anchor cited inline `[N]`. Company-neutral. Jurisdiction-specific rules explicitly labelled. Understandable with no external reading. No promotional language / overgeneralization. Ends specific to the article, not a generic moral. |
| .3 | **Vocabulary Focus** | `**New terms:**` 4–6 subject-specific terms · `**Recycled terms:**` 3–5 from earlier topics (none for the first topic of a book). Matches the vocabulary map and glossary tags exactly. |
| .4 | **Reading Questions** | Exactly 5. Mix of main-idea / detail / inference / cause-effect / vocabulary-in-context / writer's purpose. Answerable from the text. |
| .5 | **Discussion Questions** | Exactly 5. Extended professional reasoning: analysis → evaluation → application. ≥1 task-style (rank / advise / compare / diagnose / rewrite / design). No question requiring confidential info. |
| .6 | **Source Notes** | Numbered list matching the inline `[N]` markers. Each entry: publisher — title — URL. Complete enough for a teacher to verify. |

### 1.2 Currency / number style

- Non-USD: ISO 4217 code + space + number — `JPY 45,095.3 billion`, `DKK 290.403 billion`.
- USD: `US$` symbol, no space — `US$6.395 billion`.
- Spelled-out currency name as a plain noun is fine (`95 yen per share`); not as a code substitute.

### 1.3 Book structure

- 20 topics in **4 Parts**. Each Part gets a one-line purpose statement. (IR used 5/7/5/3.)
- A `00` front-matter piece: "How This Resource Is Organized" (per book).
- Outcomes of the subject area run across all Parts, not a separate Part.

### 1.4 Page layout — measured from the shipped IR Articles.docx/PDF (this is the D3 standard)

- **A4. Each topic = exactly 2 pages.**
- **Page 1 (Reading page):** single-column header zone — `X.Y. Title`, then `X.Y.1. Goal` + one-sentence goal, then the `X.Y.2. Reading` heading — followed by the Reading body in **2 columns** filling the rest of the page. Inline `[N]` markers, superscript.
- **Page 2 (Questions page):** single column throughout — `X.Y.3. Vocabulary Focus` (comma-separated term list), `X.Y.4. Reading Questions` (numbered 1–5), `X.Y.5. Discussion Questions` (numbered 1–5, ~1–2 lines each), `X.Y.6. Source Notes` (numbered; publisher + title, then the URL on its own indented line).
- **Part divider:** its own page — `Part N` / Part title / a ~180-word single-column intro paragraph, page-numbered `p.1` of that part's run.
- The Reading must not spill onto page 2; the questions page must not spill onto a third page. Both are enforced by the Phase 7 PDF page-fit check, not by word count alone.

### 1.5 Deliverables per book (final)

- `<Book> — Articles.docx` / `.pdf`
- `<Book> — Glossary.docx` / `.pdf`
- `<Book> — Teacher Answer Book.docx` / `.pdf`
- `<Book> — Cover.docx` / `.pdf` (Book A: cover art already in this folder — reuse/adapt; Book B: new)

---

## 2. Decisions — ALL RESOLVED 2026-08-28 (D1–D8)

### D1. Target learner and level — RESOLVED
**Learner: an educated adult based in Japan, primarily a Japanese first-language speaker.** **CEFR B1+/B2** for both books — one step easier than IR's B2–B2+.

**Japanese vantage point (added after prototype review 2026-08-28):** the reader's own context is the starting point, not one example among several. This is different from the IR resource, which uses Japanese companies freely but was directed to keep a *global focus* and stay off its client. Here, frame each topic the way a Japan-based reader meets it, then widen out. State the Japanese baseline where its absence would leave the reader with the wrong mental model (deflation / the "lost decades"; the BOJ's 2% target from 2013 and its 2024 exit from negative rates; the weak yen; the 2025 rice-price shock; early crypto rules after Mt. Gox and Coincheck; ageing and pensions; high cash savings; NISA; TSE governance reform). Still teach the international picture — every topic carries at least one clearly labelled non-Japan example. Not a quota for Japan content, not "make every topic about Japan". The first prototype pass got the *framing* wrong (e.g. "People often ask why central banks do not aim for zero inflation" — backwards for a reader whose normal experience was near-zero inflation). Full rule: `_lets-talk-finance-shared/house-style.md` §1a.

Level implications vs the IR articles:
- Shorter average sentences; fewer multi-clause "however / which is why / even as" chains.
- Concrete before abstract; define a term the first time it does real work in the sentence, not two sentences later.
- Keep the specialist finance terms the topic genuinely needs (they're the point), but carry more of the explanation in the surrounding plain-English sentence.
- Discussion questions still demand extended reasoning, but the stems are simpler and one task-style question per topic is enough. Questions may address the reader as someone in Japan ("Should the Bank of Japan…") where that is natural.

### D2. Book A topic list — RESOLVED
**Keep the current 20 topics unchanged.** No swap, no retitle, no additions. *Financial Literacy Programs* stays in; *AI in Finance* stays out (it is only present now as the mis-pasted filler text in topic 05 and will be removed).
The only content corrections to Book A's subject matter:
- **Topic 04 — Financial Technology (Fintech) Regulation:** current Reading is wrong-topic filler about financial-market fragmentation / MiFID II. Write a correct fintech-regulation Reading.
- **Topic 05 — Anti-Money Laundering (AML) Regulations:** current Reading is wrong-topic filler about AI in finance. Write a correct AML Reading.
- **Topic 06 — Data Privacy and Protection:** first sentence is malformed ("The of data privacy..."). Fix in the rebuild.
Because we are rebuilding all 20 from scratch to the IR standard anyway, these three are not special-cased — they just have no salvageable draft prose to lean on.

**Book A 4-Part grouping** — to be finalised in Phase 1 from the existing 20. Working proposal (5/5/5/5):
- **Part 1 — Money, Payments and Financial Technology:** Cryptocurrency Regulation · Central Bank Digital Currencies · Financial Technology Regulation · Data Privacy and Protection · Financial Inclusion Initiatives
- **Part 2 — Markets, Institutions and Financial Stability:** Regulatory Responses to Market Volatility · Credit Rating Agencies Oversight · Insurance Market Regulation · Stress Testing and Risk Management · Sovereign Debt Management
- **Part 3 — Capital, Investment and Public Policy:** Green Finance Initiatives · Infrastructure Investment · Trade Policies and Tariffs · Pension Reform · Global Economic Recovery Post-COVID
- **Part 4 — Finance, Fairness and Global Cooperation:** Anti-Money Laundering Regulations · Financial Literacy Programs · Wealth Inequality and Redistribution Policies · Corporate Governance and Accountability · Economic Diplomacy and International Cooperation

### D3. Reading length / page fit — RESOLVED
**The IR book sets the standard.** Each Reading must fill exactly one A4 page as a 2-column article beneath the Goal block, with no overflow. Measured from the shipped IR Articles PDF that is **~440–475 words with 3–6 inline `[N]` markers**; see §1.4 for the full measured layout. Word count is the working proxy; the Phase 7 rendered-PDF page-fit check is the real gate.

### D4. Sourcing — RESOLVED
**Yes — real, verifiable facts with accessible website links**, exactly as IR: every factual anchor carries an inline `[N]` marker resolving to a numbered Source Note (publisher — title — URL). ≥2 anchors per Reading. Links must be to a stable, publicly reachable page (regulator, company IR site, standard-setter, established news outlet), checked live during drafting. This is ~40+ verified citations per book.

### D5. House glossary — RESOLVED
**One glossary per book.** Each built from scratch from that book's final 20 Readings' Vocabulary Focus sections (as IR did): per entry — definition in plain English, why it matters, how it comes up in practice, `[Part.Topic]` tags. The old flat LTF glossary is discarded. Terms that recur in both books are defined **independently in each glossary**, with wording kept aligned via `_lets-talk-finance-shared/shared-term-bank.md`. No cross-book "see also".

### D6. Repo layout — RESOLVED
Mirror the IR `materials/drafts/` layout, one tree per book, plus a shared folder:
```
books/
  Let's Talk Finance/            ← Book A
    drafts/
      articles/                  00_*.md, 1-1_*.md …  (Part-Topic naming)
      control/                   project-plan.md, qa-checklist-full.md, vocabulary-map.md,
                                 company-and-geography-audit.md, revision-audit-report.md
      glossary.md
      teacher-answer-book.md
      output/                    final .docx / .pdf
  Let's Talk Finance 2/          ← Book B
    drafts/
      articles/  control/  glossary.md  teacher-answer-book.md  output/
  _lets-talk-finance-shared/     ← shared across A + B
    process-guide.md             (adapted from Book_Draft_And_Edit_Process_Guide.md)
    house-style.md               (level, register, currency/number rules, jurisdiction-labelling, [N] citation format)
    shared-term-bank.md          (aligned definitions of terms recurring across both books)
    topic-ledger.md              (master list of all 40 topics — guarantees no A/B overlap)
```
The old Book A `out/` conversions move to `_archive/` per D7 — not kept under the live tree.

### D7. Old Book A files — RESOLVED: ARCHIVE
Move to `books/Let's Talk Finance/_archive/` (not deleted, not under the live `drafts/` tree):
- `Let's Talk Finance.docx`, `Let's Talk Finance (AS Online).docx`, `Let's Talk Finance (Answers for Teachers).docx`
- the `out/` conversion folder and the two sub-`out/` folders
- the cover `.docx` / `.jpg` files stay in place for now (Book A cover art is reused)
- `Thumbs.db` → add `Thumbs.db` to repo `.gitignore`, then delete.

### D8. Book B topic list — RESOLVED
The 20 topics in §3 are approved as-is (DDobson, 2026-08-28). No changes.

---

## 3. Book B — proposed 20 new topics (for approval)

Design rules used: (a) no overlap with Book A's 20; (b) genuine 2026-current finance discussion topics with real cases and verifiable data; (c) same 4-Part shape; (d) advanced-adult / senior-professional interest; (e) company-neutral, jurisdiction-labelled. **All provisional — your call.**

### Part 1 — Personal Finance and Household Money
| # | Topic | Focus |
|---|---|---|
| 1.1 | The Cost of Living and Inflation | How households and economies experience sustained price rises; wage–price dynamics; central-bank targets. |
| 1.2 | Debt: Credit Cards, Mortgages and Loans | How consumer credit works, interest and compounding, over-indebtedness, buy-now-pay-later. |
| 1.3 | Saving and Investing for the Long Term | Compounding, diversification, index funds vs active, the role of time horizon. |
| 1.4 | Housing Markets and Affordability | What drives house prices, rent vs buy, housing as investment vs shelter, policy levers. |
| 1.5 | Scams, Fraud and Financial Self-Defence | Investment fraud, phishing, romance/APP scams, who bears the loss, prevention. |

### Part 2 — Companies, Work and Money
| # | Topic | Focus |
|---|---|---|
| 2.1 | How Companies Raise Money | Equity vs debt, IPOs, venture capital, private markets vs public listing. |
| 2.2 | Startups, Venture Capital and Failure | The funding ladder, why most startups fail, unicorns and down rounds. |
| 2.3 | The Gig Economy and Income Security | Platform work, irregular income, benefits and pensions gaps, classification disputes. |
| 2.4 | Executive Pay and Inequality Inside Firms | Pay ratios, stock-based compensation, say-on-pay, the justification debate. |
| 2.5 | Banks: What They Do and How They Fail | Maturity transformation, deposit runs, 2023 regional-bank failures, deposit insurance. |

### Part 3 — Markets, Risk and the Global Economy
| # | Topic | Focus |
|---|---|---|
| 3.1 | What Moves Stock Markets | Earnings, rates, sentiment, index concentration, why prices and news diverge. |
| 3.2 | Bubbles, Crashes and Manias | Historical and recent asset bubbles, leverage, herd behaviour, "this time is different." |
| 3.3 | Commodities: Oil, Metals and Food | Price formation, supply shocks, resource dependence, the energy transition's demand shift. |
| 3.4 | Currencies and Exchange Rates | What sets exchange rates, devaluation, the US dollar's global role, currency crises. |
| 3.5 | Emerging Markets and Development Finance | Capital flows, the "middle-income trap," IMF/World Bank roles, debt distress. |

### Part 4 — Money, Society and the Future
| # | Topic | Focus |
|---|---|---|
| 4.1 | Tax: How Governments Raise Money | Income vs consumption vs wealth taxes, avoidance vs evasion, the global minimum tax. |
| 4.2 | Government Debt and Deficits | Why states borrow, debt-to-GDP, who holds the debt, sustainability vs austerity debates. |
| 4.3 | The Business of Sport, Art and Culture | Valuation of clubs and artworks, sponsorship, media rights, cultural assets as investments. |
| 4.4 | Philanthropy, Foundations and Impact | How large-scale giving is structured and taxed, effectiveness debates, donor influence. |
| 4.5 | The Future of Money | Programmable money, tokenised assets, cash decline, financial privacy, what comes after cards. |

**Overlap check vs Book A:** Book A covers *systemic/regulatory* finance (CBDCs, AML, stress testing, credit-rating oversight, sovereign debt at the sovereign-issuer level). Book B covers *personal, corporate-finance, and market-mechanics* angles. Closest pairs to watch: A "Sovereign Debt Management" vs B 4.2 "Government Debt and Deficits" (A = issuer's debt-management operations; B = the political-economy of deficits) and A "CBDCs" vs B 4.5 "The Future of Money" (A = one instrument; B = the broader shift). Both are defensibly distinct; flag if you want tighter separation.

---

## 4. Production process (from `Book_Draft_And_Edit_Process_Guide.md`), adapted for two books

### Phase 1 — Confirm the working specification — COMPLETE

D1–D8 all resolved (§2). Spec locked: B1+/B2 level, the 6-subsection template, one-A4-page 2-column Reading fit (§1.4), inline `[N]` + URL Source Notes, ≥2 anchors/Reading, per-book glossary, the repo layout (§D6), Book A's 20 topics + working Part grouping, Book B's 20 topics (§3).

### Phase 2 — One calibration prototype covering both books
Draft **one complete topic from Book A and one from Book B** (Goal + Reading + Vocabulary Focus + Reading Qs + Discussion Qs + Source Notes each). Purpose: lock tone, density, vocabulary level, structure, question style — and confirm the two books read as companions, not as two different products. Review and calibrate before drafting the rest.
- Suggested prototypes: Book A **1.1 Cryptocurrency Regulation** (exists as broken draft — good rebuild test) and Book B **1.1 The Cost of Living and Inflation** (fresh write, high-interest, well-sourced).

### Phase 3 — Set up the shared + per-book control layer
- `_lets-talk-finance-shared/house-style.md`, `process-guide.md`, `shared-term-bank.md`, `topic-ledger.md`
- Shared: `_lets-talk-finance-shared/article-checklist.md` (per-article minimum gate). Per book: `control/project-plan.md`, `control/qa-checklist-full.md` (whole-book Phase-5 audit, adapted from IR's), `control/vocabulary-map.md`, `control/company-and-geography-audit.md`, `control/factual-data-insertion-guide.md`

### Phase 4 — Draft in parallel Part-sized batches
Alternate or interleave: Book A Part 1 → Book B Part 1 → check both → continue. After each batch, check terminology, tone, question design, vocabulary map. Maintain both company/geography audits and the shared topic ledger.

### Phase 5 — Quality assurance (per book)
Full QA checklist against every topic + teacher book + vocabulary map + glossary. Known IR-project failure modes to pre-empt:
- Opening-style repetition (IR: 8/20 topics opened "On [date], X happened") — assign varied structures up front.
- Cross-topic reuse of the same case/statistic as primary evidence (IR: 5 substantial duplications) — the company/geography audit + shared topic ledger are the guard, now across 40 topics.
- Answer-book Reading answers drifting from final article wording — re-verify against the *final* text.
- Teacher-book "Target vocabulary" vs article "New terms" vs glossary tags — must match exactly; check by direct comparison.
- Jurisdiction labels applied inconsistently to the same rule.
- Glossary going stale after any example-rebalancing pass.

### Phase 6 — Assemble (per book)
Consistent layout, Part.Topic numbering, section structure. Build student edition, glossary, teacher answer book.

### Phase 7 — PDF-check production loop (per book)
Editorial pass → export to PDF (Word COM: `Documents.Open → Fields.Update() → ExportAsFixedFormat($pdf, 17) → Close → Quit`) → programmatically check the rendered result (page-fit test: "does the next heading appear within N pages", not total span) → fix precisely → re-check.
DOCX traps: section breaks are paragraph-attached and invisible (assert expected count before bulk paragraph deletes); hyperlinks live in `w:hyperlink`, not `paragraph.runs`; per-section list restart needs explicit `<w:startOverride w:val="1"/>`; verify `--reference-doc` style matching by comparing actual font/size values.
Environment note: no LibreOffice/poppler, but Word is installed and scriptable via PowerShell COM; `Resolve-Path` needs `.ProviderPath` before COM; never kill Word mid-export (guaranteed corruption); a stuck export is usually an invisible dialog — check CPU is advancing.

### Phase 8 — Sign-off and delivery
Final review; deliver the four output pairs per book (eight pairs total).

---

## 5. Status & immediate next actions

**All decisions resolved 2026-08-28 (D1–D8, §2). Phases 1–3 complete. Phase 2 prototypes approved 2026-08-28.**

Done:
1. ✅ Old Book A material archived to `books/Let's Talk Finance/_archive/`. `Thumbs.db` removed and gitignored.
2. ✅ Repo layout created: `books/Let's Talk Finance/drafts/{articles,control,output}/`, `books/Let's Talk Finance 2/drafts/{articles,control,output}/`, `books/_lets-talk-finance-shared/`.
3. ✅ Shared layer: `house-style.md` (B1+/B2 register, currency/number style, jurisdiction labelling, `[N]` citation format, §1.4 page layout, §1a Japanese-vantage-point / global-perspective rule, paragraph-writing rule carried from IR), `topic-ledger.md` (all 40 topics + overlap-watch + cross-topic evidence register), `process-guide.md` (copy of the IR playbook), `shared-term-bank.md` (stub).
4. ✅ Per-book control layer: `project-plan.md`, `qa-checklist-full.md` (whole-book Phase-5 audit, adapted from IR's), `vocabulary-map.md` (20-row Topic Map, empty), `company-and-geography-audit.md`, `factual-data-insertion-guide.md` — for both books. Shared **`_lets-talk-finance-shared/article-checklist.md`** — the per-article minimum gate, run on every article.
5. ✅ Phase-2 prototypes drafted, revised through review (level, Japanese vantage point, global balance, paragraph writing), and **approved**:
   - Book A `drafts/articles/1-1_Cryptocurrency_Regulation.md` — 428-word Reading, 4 live sources
   - Book B `drafts/articles/1-1_The_Cost_of_Living_and_Inflation.md` — 439-word Reading, 5 live sources

**Next — Phase 4, parallel batch drafting.** Per Part-sized batch, interleaved A then B:
- **Batch 1:** Book A Part 1 (1.2–1.5) + Book B Part 1 (1.2–1.5). 1.1 of each is done.
- Before drafting each batch: assign an article shape and an opening style per topic (log in that book's `control/` — `house-style.md` §6), so the set has variety by design.
- During drafting: research and live-verify every fact and URL; keep `vocabulary-map.md`, `company-and-geography-audit.md`, and the shared `topic-ledger.md` evidence register current as each topic lands.
- Run `_lets-talk-finance-shared/article-checklist.md` on **every** article as it lands. After each batch: confirm no cross-topic evidence collision against the ledger; confirm global spread and Japanese vantage point across the batch.
- Then Batches 2–4 (Parts 2, 3, 4 of each book).

After Phase 4: Phase 5 full QA per book → Phase 6 assemble → Phase 7 PDF page-fit loop (needs a 2-column A4 reference DOCX built first — no inherited one) → Phase 8 sign-off.

## 6. Reference index

| Purpose | File (Ishida repo, `…/Marubeni/Ishida, Tetsuya/`) |
|---|---|
| Reusable process playbook | `Book_Draft_And_Edit_Process_Guide.md` |
| Book concept + spec | `materials/drafts/control/Investor_Relations_Resource_Project_Plan.md` |
| Topic org front-matter model | `materials/drafts/articles/00_How_This_Resource_Is_Organized.md` |
| Sample finished topic | `materials/drafts/articles/1-1_What_Is_Investor_Relations.md` |
| QA checklist to adapt | `materials/drafts/control/IR article revision QA checklist.md` |
| Vocabulary map model | `materials/drafts/control/IR resource vocabulary map.md` |
| Glossary model | `materials/drafts/IR industry glossary.md` |
| Teacher answer book model | `materials/drafts/IR teacher answer book.md` |
| Company/geography audit model | `materials/drafts/control/IR article company and geography audit.md` |
| Topic-candidate map (pre-selection) model | `materials/archive/Investor relations 20 topic map.md` |

Old Book A conversion (this repo, superseded): `books/Let's Talk Finance/out/.md/` — 20 split articles + glossary from the ChatGPT docx.
