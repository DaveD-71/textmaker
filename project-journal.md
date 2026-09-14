# Project Journal

## 2026-09-14 (even later) - Isolated SWP-specific pipeline behavior behind opt-in flags

User flagged that the previous session's fix (`--no-presentation-page-setup`, `--keep-heading-page-breaks`) had the polarity backwards: SWP-specific behavior was running by default for every project using `markdown-to-docx`, requiring non-SWP projects (like LTF) to opt out, when it should be the reverse — SWP is one project among several sharing this tool, so its specific behavior should require an explicit opt-in.

**Inverted three defaults in `scripts/postprocess_docx.py` / `scripts/cli.py`:**
- `apply_presentation_page_setup` (A4 mirror-margin override): was always-on with a `--no-presentation-page-setup` opt-out; now always-off with a `--swp-presentation-page-setup` opt-in.
- `disable_heading_style_page_breaks` (strips `pageBreakBefore` from Heading 1/2 in favor of explicit section breaks): was always-on with `--keep-heading-page-breaks`; now always-off with `--swp-disable-heading-page-breaks`.
- `apply_list_styles` / `strip_literal_alpha_markers` (remaps lists to `PS Bullet List` / `PS Numbered List` / `PS Numbered List 2`): was always-on (silently no-op for reference docs without those styles); now always-off with a new `--swp-list-styles` opt-in, consistent with the existing `--swp-style-tags` flag's naming.

**Verified the inversion is behaviorally neutral for LTF**: rebuilt all 6 deliverables (student edition, glossary, teacher answer book x 2 books) using the simplified command (no longer needs any opt-out flags) and confirmed identical paragraph-restyling counts to the previous build (101/99 article_body_text, 20/20 First Paragraph, 299/302 Compact, 40/40 section breaks, 133/121 glossary entries, 40+200 teacher-book paragraphs) — same result, cleaner command line.

**Updated `books/Speaking with PowerPoint/README.md`** (the only place SWP's build invocation is documented — there is no committed build script) to note the three new required opt-in flags alongside the existing `--swp-style-tags`, so a future SWP build doesn't silently lose its page setup/list styling/heading-page-break behavior.

Regenerated both books' student-edition PDFs from the rebuilt DOCX files.

## 2026-09-14 (later) - LTF Phase 6 extended: DOCX build matching the IR project's actual style, both books

User provided the three real "Let's Talk: Investor Relations" output DOCX files as the style reference for the LTF DOCX build (student edition, glossary, teacher answer book), rather than starting from scratch. Built all 6 deliverables for both books using `textmaker.cmd markdown-to-docx --reference <IR docx>`.

**Shared-pipeline bugs found and fixed** (`scripts/postprocess_docx.py`, `scripts/cli.py`): the pipeline was built for the Speaking with PowerPoint (SWP) project and had several passes that unconditionally assumed SWP-specific reference-doc styles or SWP-specific page setup, with no way to opt out. Four fixes: (1) `apply_list_styles`/`strip_literal_alpha_markers` now warn-and-skip instead of hard-crashing when the reference DOCX lacks `PS Bullet List`/`List Number 3`-style styles; (2) `remove_pandoc_generated_styles` made its `Body Text Char` requirement optional; (3) added `--no-presentation-page-setup` to skip the SWP page-margin override; (4) added `--keep-heading-page-breaks` to skip stripping `pageBreakBefore` from Heading 1/2 (needed because the IR reference relies on that style flag directly, not on explicit section breaks, to start new pages).

**Discovered the IR document's actual structure by direct OOXML inspection**, not by guessing: read the real `Investor Relations Resource - Articles.docx`/`- Glossary.docx`/`IR Teacher Answer Book.docx` files with python-docx to find (a) the exact per-topic section-break pattern (single-column title+Goal, then a 2-column CONTINUOUS section around just the Reading body, then single-column again for Vocabulary Focus onward); (b) the specific content paragraph styles used positionally (`article_body_text` for Reading, `First Paragraph` for the line right after certain headings, `Compact` for numbered Reading/Discussion Questions, Source Notes, and teacher-book answers); (c) the glossary's single continuous 2-column section spanning every entry; (d) the centered "p. [PAGE]" footer starting one section after the title page; (e) that Source Note URLs are real `w:hyperlink` elements, not plain text.

**New LTF-specific tooling in `scripts_local/`** (kept separate from the shared pipeline since this logic is specific to matching one reference document's exact layout, not general-purpose): `build_ltf_student_edition_md.py` (strips Recycled-terms line + New-terms label from the build-only merged markdown, confirmed by direct inspection that the IR reference shows one plain unlabeled term list with no recycled terms at all; also converts trailing Source Note URLs into markdown links so Pandoc emits real hyperlinks), `apply_ir_content_styles.py` and `apply_ir_teacher_book_styles.py` (position-based paragraph restyling, since the LTF markdown has no fenced Div classes to drive the existing `style_bridge.lua` mapping), `add_two_column_reading_sections.py` (per-topic section breaks, with a hard assertion on expected topic count and exact break count before saving, per the process guide's own section-break-corruption warning), `fix_part_heading_page_breaks.py`, `add_page_number_footer.py`, `style_glossary_docx.py`.

**Bugs caught and fixed during the build, not before:**
- A regex in the markdown transformer used `\s*$` under `re.MULTILINE` to trim trailing whitespace after a linkified URL, which also ate the blank line separating that topic from the next one's `## X.Y. Title` heading — silently merging topics 1.2 onward into their preceding topic with no Heading 2 at all. Caught by the section-break script's own hard assertion (`expected 20 topics, found 4`) refusing to proceed on the malformed structure, not by visual inspection. Fixed by restricting the trim to `[ \t]*` (no newlines).
- The existing `pagebreak.lua` filter (unrelated to this session's other bugs, a pre-existing repo feature) converts every `---` HorizontalRule into a literal hard page break. The Phase-6 merge script's Part-divider `---` markers were each producing a wasted, near-blank "Part N" page. Fixed with the pipeline's own existing `--ignore-horizontal-rules` flag, not new code.

**Verified for both books:** each topic's Reading fits one A4 page in the 2-column layout (confirmed by direct PDF render, not just structural inspection); topics start on fresh pages, Parts share a page with their first topic (matching the IR pattern exactly); Source Note URLs are real hyperlinks; Vocabulary Focus renders as the plain unlabeled list.

**Open question, not resolved:** whether the full topic (Goal through Source Notes) needs to fit one page, versus just the Reading section (house-style's literal wording is about the Reading specifically). Every topic's Reading fits one page; the full topic with all 10 questions plus Source Notes spans 2-3 pages. Asked the user; they chose to pause and continue the remaining polish manually rather than resolve this in-session.

**Also installed this session:** poppler (pdftoppm) at `%LOCALAPPDATA%\Poppler`, added to user PATH, so PDF pages can be rendered to PNG for visual verification going forward (this machine had no poppler/pdftoppm previously, only Pandoc).

## 2026-09-14 - LTF Phase 6: assembled student edition for both books

Started Phase 6 (assemble) per `PROJECT-PLAN.md`. The glossary and teacher-answer-book deliverables it calls for already existed (built during the QA-fix pass's item 6), so the remaining work was the student edition itself.

**Scoping question resolved first.** The plan's Phase 6 description ("consistent layout, Part.Topic numbering, section structure") is vague about the concrete deliverable, and the IR project's own process guide confirmed a DOCX build did happen there (Pandoc + `--reference-doc` + Word COM PDF export), but that work maps to our own Phase 7, not Phase 6 — and no 2-column reference DOCX exists yet for the rebuilt LTF drafts (only archived ones from the pre-rebuild old Book A). Asked the user to confirm scope rather than assume; agreed Phase 6 today is the merged-markdown step only, with the reference-DOCX build and PDF loop left as a separate Phase 7.

**Built:** a Python merge script that, per book, sorts all 20 topic files by Part.Topic order, inserts a `# Part N: Title` divider heading (with the Part's own one-line description) before each Part's first topic, and prepends the front-matter file's content under a `## How This Resource Is Organized` heading below the book's own H1 title. Output: `drafts/output/<Book Title> - Student Edition.md` for each book.

**Verified:** both files have exactly 20 `## X.Y. Title` topic headings and 4 `# Part N` headings, in correct order, with no truncation and no stray/duplicate top-level headings. Book A: 16,818 words total across all 20 Readings plus front matter. Book B: 16,704 words. Both files end cleanly at topic 4.5's Source Notes.

**Not yet done:** the reference DOCX (2-column A4 layout) and the Pandoc/Word-COM PDF-check loop are Phase 7, not started. The student-edition markdown built today is exactly the input Phase 7 will consume.

## 2026-09-12 (absolute final) - LTF: full Phase 5 whole-book re-audit, both books clean

Ran the "After all of the above" re-audit from `qa-todo.md` — a fresh full Phase 5 whole-book QA pass on both books, to confirm all 7 numbered fix items actually hold and catch anything missed, before moving to Phase 6 assembly.

**First attempt failed on cost, not content.** Launched two background agents (one per book). Both hit this session's monthly spend limit mid-run (`rate_limit`, HTTP 429) and were terminated — one of them had also spawned 4 further sub-agents splitting its own work by Part, none of which finished either, all failing the same way. No files were touched (these were read-only audits), so nothing was corrupted, but no report was produced. Waited for the spend-limit reset (7:50pm Asia/Tokyo per the error message), then relaunched both agents with explicit instructions to work in a single lean pass — read all 20 articles directly, no sub-agent splitting, no elaborate scripted sentence-counting — to avoid repeating the same budget exhaustion. Both completed successfully on the retry.

**Result: both books' whole-book audits are clean.** All 7 previously-fixed items (SVB/Signature Bank swap, company-and-geography-audit backfill, Parts 3-4 word-count/sentence-length trim, currency-style fixes, recycled-vocabulary floor, glossary/front-matter creation, citation renumbering) confirmed PASS in both books with zero regressions.

**Three new minor findings, all fixed immediately:**

1. **Book A — stale vocabulary-map.md row.** `vocabulary-map.md`'s 2.4 (Stress Testing) row still listed "bank run" as a recycled term, left over from before the Signature Bank rewrite (item 1) and never re-synced after. The article's own Vocabulary Focus line was already correct (3 terms, no "bank run" — confirmed the term doesn't appear anywhere in 2.4's current text); only the control file had drifted. Fixed the map row to match. Also retagged the glossary's "Bank run" entry from `[2.4]` to `[2.3, 2.4]`, since the term itself is genuinely used in 2.3 (Insurance Market Regulation)'s Reading and Discussion Question 1 ("Unlike a bank run, an insurer's trouble usually builds slowly...") even though 2.3's own Vocabulary Focus line doesn't list it as a tracked term either — the glossary entry's actual content (the Signature Bank case) is specifically anchored to 2.4, so both topics are now credited.

2. **Book B — genuine new run-on sentence.** A 55-word run-on in `1-5_Scams_Fraud_and_Financial_Self_Defence.md`, introduced when the "consumer protection" phrase was added during item 6 earlier this session and never re-checked for sentence length afterward (a gap in that fix's own verification — word count and citation integrity were checked then, but not sentence length, since the edit looked like a small insertion). Split the sentence at its colon into two clean sentences ("...not just the victim's problem. It now requires them to reimburse..."). Verified: longest sentence in the article dropped from 55 to 32 words, word count unaffected (469), citations still sequential and correct.

3. **Book B — duplicate glossary entry.** `"this time is different" thinking` had been added to `glossary.md` twice independently: once by the background glossary-drafting agent's own internal completeness self-check (during item 6), and again by me during item 6's verification pass when I found the same apparent gap without checking whether the agent had already closed it in a spot I hadn't re-read. Both entries were tagged `[3.2]` with different wording. Removed the weaker duplicate, kept the version better anchored to the article's specific "three forces" framing and named historical examples (tulip mania, the 2022 Luna crash).

**Checklist correction, not a content fix.** Both books' `qa-checklist-full.md` had a line requiring glossary letter-headers (A, B, C...), citing a different, superseded draft glossary attempt as the reason for the rule. Checked the actual house-style precedent directly — the IR project's own `IR industry glossary.md` — and confirmed it uses a flat alphabetical list with no letter headers at all. Asked the user whether to add headers to match the checklist as written, or correct the checklist to match the real precedent; user chose the latter. Marked the line N/A in both books' checklist copies, with an explanatory note, rather than silently deleting it.

**One item deliberately left as a soft note, not fixed:** Book A has 5 of 20 topics (1.4, 2.1, 2.3, 3.4, 3.5) opening with a dated-event first clause, against the house-style guideline of roughly 3 per book. The audit judged each opening independently well-written and not verbatim-similar to the others — not the severity the original rule was written to catch (an 8/20 case in the IR project) — so this was logged as worth a look at a future revision pass rather than forced into a rewrite now.

**All 7 `qa-todo.md` items plus this final re-audit are now complete.** Per `qa-todo.md`'s own closing note, the project is ready to proceed to Phase 6 (assembly: Part dividers, front matter, numbering) per `PROJECT-PLAN.md` §5, whenever the user chooses to start that phase.

## 2026-09-12 (final) - LTF QA TODO item 7 fixed: citation renumbering + Book B 4.5 third region

Fixed item 7, the last item on `qa-todo.md`'s numbered list, closing out the full QA-fix pass that started with item 1 (SVB duplication) earlier this session.

**Citation renumbering — scope grew on inspection.** The original audit flag named only Book B `3-1_What_Moves_Stock_Markets.md`. Before fixing just that one, ran a mechanical sweep of all 40 articles in both books checking whether inline `[N]` markers appear in strict first-appearance sequential order, and found 7 more affected: Book A `3-4` (Pension Reform), `3-5` (Global Economic Recovery), `4-3` (Wealth Inequality); Book B `1-5` (Scams and Fraud), `3-2` (Bubbles, Crashes and Manias), `3-3` (Commodities), `4-2` (Government Debt and Deficits). Confirmed with the user this was purely cosmetic (every marker still resolved to a correct Source Note, nothing orphaned) and got explicit sign-off before fixing all 8 rather than just the one named in the audit.

**Process correction caught mid-fix.** On the first file (Book A `3-4`), I edited only the inline markers to their new sequential numbers and was interrupted by the user before touching the Source Notes list itself — leaving the two halves temporarily mismatched (e.g. text `[1]` pointed to what was still labelled Source Note `5` in the list). The user asked directly whether the fact each citation references still matches after renumbering, which was exactly the right question given the file was mid-edit. Re-read the file, found the mismatch, fixed the Source Notes list to match, and verified by direct content comparison (not just count-matching) that all 6 fact/source pairs were correctly bound. Changed method for the remaining 7 files: build the full old->new number map first, apply it to inline markers and the Source Notes list together in the same edit pass per file, then verify — for every marker — that the specific claim next to it still matches the specific source described at that number, not just that the counts and ranges line up. Re-ran the full 40-article sweep after finishing: 100% sequential in both books.

**Book B 4.5 (The Future of Money) — added genuine third-region weight.** The article's comparative core (Sweden vs. Japan, cashless vs. cash-heavy) already mentioned Germany, China and India in passing, but only Sweden and Japan carried real detail. User chose to add substance to a third region rather than leave it as-is. Added a Germany data point sourced from Deutsche Bundesbank's "Payment behaviour in Germany in 2023."

**Caught my own citation error before it went into the file.** First draft cited a Bundesbank URL and claimed cash covers "about half of spending by value" in Germany, without live-verifying either. WebFetch on the URL showed it actually resolved to an unrelated 2022 speech transcript about fintech competition — not a real citation. A second guessed URL redirected to a completely different, unrelated domain. Used WebSearch properly instead of guessing further, found the real Bundesbank press release, and discovered the actual figures are more specific and more interesting than what I'd drafted: 51% of transactions by *count* were cash in 2023, but only 26% of spending by *value* (cash dominates small purchases, cards take over larger ones) — not "about half by value" as first written. Corrected the article text to state both figures accurately and distinctly, fixed the source URL to the real press release, and re-verified word count (499, right at this session's ~500 ceiling), citation sequential order (now 7 markers after the insertion), and that all Recycled terms remained present. Left the Discussion Questions' Sweden/Japan comparison untouched, since that pairing is the article's deliberate teaching contrast, not an oversight to fix.

**Lesson for future citation work:** never write a specific figure or URL into an article from memory/inference and treat it as done — always live-verify via WebFetch/WebSearch before the citation is considered real, the same discipline already applied to every other source in this project. This session's own house rule (verify sources) almost got skipped for a small "just add one supporting fact" edit, which is exactly when that kind of shortcut is most tempting and most risky.

This closes all 7 items on `qa-todo.md`. Remaining work per that file's "After all of the above" section: re-run the full Phase 5 whole-book QA audit on both books to confirm everything above is resolved and nothing regressed, before proceeding to Phase 6 assembly.

## 2026-09-12 (newest) - LTF QA TODO item 6 fixed: glossaries and front-matter files, both books

Fixed item 6 from `qa-todo.md`: both books were missing `glossary.md` and `00_How_This_Resource_Is_Organized.md`, the two remaining Phase 5/6 deliverables.

**Front matter:** wrote both `00_How_This_Resource_Is_Organized.md` files directly, following the IR project's precedent format exactly (title, short intro explaining `Part.Topic` numbering, then one paragraph per Part naming its 5 topics' shared theme). Committed as `7ec72a5`.

**Glossaries:** given the scale (roughly 120 entries per book, each needing to be sourced from the actual article rather than guessed from the term name), delegated to two background agents running in parallel, one per book, each briefed to read the IR project's own glossary as the format precedent, read all 20 of their book's articles, and mechanically cross-check every New/Target term in `vocabulary-map.md` against their draft before finishing.

**Book A result:** 133 entries. Verified directly (not just trusting the agent's self-report): read a sample of entries for quality, ran an independent mechanical completeness check against `vocabulary-map.md` (two apparent gaps were false positives from my own check script's quote-handling, confirmed by direct grep). Spot-checked the agent's two flagged disambiguation calls — "claim" (insurance) vs "claim (on the central bank)", and "default" (credit rating) vs "default option" (behavioural) — both correctly kept as separate entries since they are genuinely different concepts sharing a headword.

**Book B result:** 122 entries (120 initial + 2 added by me after verification). My independent completeness check found two real gaps the agent's own self-check had missed: (1) `"this time is different" thinking` (3.2) existed only as a passing mention inside two other entries ("Herd behaviour", "Leverage (bubbles)"), not as its own headword — added it as a standalone entry. (2) `consumer protection`, listed as a Recycled term in `1-5_Scams_Fraud_and_Financial_Self_Defence.md`'s own Vocabulary Focus line, did not actually appear anywhere in the article's body text — a genuine pre-existing drift between the vocabulary line and the prose, most likely dating from the item-3 length-trim pass on this same file. Fixed at the source rather than papering over it in the glossary alone: added the phrase naturally into the article's UK bank-reimbursement sentence ("the United Kingdom has treated this as a consumer protection matter for banks to fix, not just the victim's problem"), re-verified word count (469, still in range) and citation integrity, then added the glossary entry.

**Three-way vocabulary check:** with both glossaries now existing, ran the full check (article New/Recycled terms <-> teacher-answer-book Target vocabulary <-> glossary coverage) across all 40 topics in both books. Found zero real defects beyond the one consumer-protection gap above (already fixed) — every apparent "mismatch" my check script flagged was a trailing-period parsing artifact in the script itself, confirmed by direct inspection before treating anything as a false alarm or a real defect.

**Shared term bank:** `shared-term-bank.md` had existed since project setup but was still empty. Cross-checked all headwords across both new glossaries and found exactly 7 exact collisions (bank run, central bank, consumer protection, exchange rate, progressive/regressive tax, stablecoin, stock index). Verified all 7 consistent in meaning, scope and register between the two books — each book illustrates with its own real example (e.g. Book A's Signature Bank vs Book B's Silicon Valley Bank for "bank run", correctly kept as distinct cases per the item-1 fix, but the *definition* of the shared concept itself matches) — and added aligned reference entries for all 7.

**Not yet done:** the Phase 5 QA checklist's Glossary section and front-matter line of the Whole-book section were N/A for lack of these files; now that they exist, a fresh checklist pass could evaluate them, but this is deferred to the "After all of the above" full re-audit once items 4-7 are complete, consistent with this session's one-item-at-a-time pacing.

## 2026-09-12 (very latest) - LTF QA TODO item 5 fixed: recycled-vocabulary floor gap, Book A

Fixed item 5 from `qa-todo.md`: Book A topics 1.2 and 1.5 each had only 2 recycled terms against the checklist's 3-5 floor.

**User decision (asked directly, since the two topics warranted different treatment):** fix 1.5 by adding a genuine term; document 1.2 as an accepted exception rather than force an unrelated term into the prose.

**1.5 Financial Inclusion Initiatives - fixed.** Had a real 4-topic pool to draw from (1.1-1.4's cumulative term set). Added "regulator" to the Brazil/Pix sentence — "In Brazil, the central bank acted as regulator and infrastructure builder at once, launching an instant-payment system called Pix in 2020" — a genuine, non-forced addition that fits the sentence's own point about a government-built payment system. Now 3 recycled terms (*central bank, payment system, regulator*). Updated the article's Vocabulary Focus line and `vocabulary-map.md`'s Topic Map row. Verified: word count 467 (still in range), citation markers == Source Notes, all 3 recycled terms present verbatim in the Reading.

**1.2 Central Bank Digital Currencies - documented as an exception, not edited.** It is the book's second topic, so its only possible recycling source is 1.1 (Cryptocurrency Regulation), whose term set (cryptocurrency, blockchain, crypto exchange, stablecoin, issuer, supervision) has almost no genuine overlap with 1.2's CBDC-mechanics content beyond the one term already recycled (*stablecoin*). Forcing a third term in would have been padding, not real recycling. Added a formal "Accepted exception" note to `vocabulary-map.md` (distinct from the pre-existing general "Known limitation" note) so future QA passes treat this as resolved-by-decision rather than re-flagging it.

## 2026-09-12 (latest) - LTF QA TODO item 4 fixed: currency-style violations, both books

Fixed item 4 from `qa-todo.md`: bare `¥`/`£` symbols in prose instead of the required ISO-code format (`house-style.md` §3: ISO 4217 code + space + number, e.g. `JPY 45,095.3 billion`).

**Book B (3 topics, as originally flagged):** `1-1_The_Cost_of_Living_and_Inflation.md` ("¥4,260" -> "JPY 4,260"), `1-2_Debt_Credit_Cards_Mortgages_and_Loans.md` ("£0.1 billion"/"£13 billion" -> "GBP 0.1 billion"/"GBP 13 billion"), `1-5_Scams_Fraud_and_Financial_Self_Defence.md` ("£85,000" -> "GBP 85,000"; "¥72 billion"/"¥127 billion" -> "JPY 72 billion"/"JPY 127 billion").

**Extra violation caught by re-running the check rather than trusting the earlier audit finding:** the 2026-09-12 QA audit had reported Book A as having zero currency-style violations. A full sweep for this fix found that was wrong — Book A `1-4_Data_Privacy_and_Protection.md` has bare "€1.2 billion" and "€6 billion" in prose. Fixed to "EUR 1.2 billion" / "EUR 6 billion". Lesson: re-verify a prior audit's negative findings mechanically when doing the actual fix pass, don't just carry them forward.

**Correctly left alone:** two more bare-symbol hits (Book A `3-2_Infrastructure_Investment.md`, Book B `4-3_The_Business_of_Sport_Art_and_Culture.md`) are inside Source Note citation titles quoting the original article headline verbatim — not a style violation, since those are direct quotations of external source titles, not our own prose.

**Verified:** all 4 edited articles — citation markers == Source Notes (both books), word counts unaffected (439-451w, unchanged from before this fix since these were in-place symbol swaps not trims), zero bare `¥`/`£`/`€` remaining in any Reading body across either book.

## 2026-09-12 (even later) - LTF QA TODO item 3 fixed: Parts 3-4 word-count/sentence-length editorial pass, both books

Fixed item 3 from `qa-todo.md`: Parts 3-4 Readings in both books had drifted up to 497-544 words against the ~440-475 target (soft ~490 ceiling in practice), with several sentences running 40-62 words.

**Method (established this pass, reused for every article):** for each article, trim the Reading body toward ~485-498 words, then re-verify by script: word count (Reading-body-minus-`[N]`-markers), citation-marker-to-Source-Note integrity (set comparison), every Recycled term still present verbatim in the Reading+Questions text, and a naive sentence-boundary split to flag anything >=40 words for manual read-through (the naive splitter has known false positives at quote-mark/em-dash boundaries, so every flagged "long sentence" was read manually before deciding whether it was a real defect).

**Book A (10 topics touched, committed as `f083bd1`):** `3.2` Infrastructure Investment 500->466w, `3.3` Trade Policies and Tariffs 537->474w, `3.4` Pension Reform 512->472w, `3.5` Global Economic Recovery Post-COVID 527->473w, `4.2` Financial Literacy Programs 499->485w, `4.3` Wealth Inequality 500->484w, `4.4` Corporate Governance 512->495w, `4.5` Economic Diplomacy 509->497w. (`3.1` at 484w and `4.1` at 479w were already in range, left untouched.)

**Book B (10 topics touched, committed as `499c94e`):** `3.1` What Moves Stock Markets 497->483w, `3.2` Bubbles, Crashes and Manias 506->492w, `3.3` Commodities 531->488w, `3.4` Currencies and Exchange Rates 510->498w, `3.5` Emerging Markets and Development Finance 497->483w, `4.1` Tax 519->498w, `4.2` Government Debt and Deficits 512->498w, `4.3` Business of Sport, Art and Culture 544->496w, `4.4` Philanthropy, Foundations and Impact 516->480w, `4.5` The Future of Money 530->491w.

**Sentence-length fixes:** several over-long sentences (up to 62 words - Book B 4.3's Saudi PIF sentence, Book B 4.4's "three things explain this" sentence, Book A 4.3/4.4/4.5 in the 44-47w range) were split back into two clean sentences rather than trimmed in place, even where that cost a few extra words, to stay within the "two subordinate clauses is the ceiling" guideline. A handful of em-dash sentences in the low-40s were judged acceptable as single clean sentences and left as-is (precedent set with Book A's first pass, applied consistently to Book B).

**Content-consistency catches during trimming (same failure pattern recurred across both books - always re-verify after every trim, never assume a shortening edit is safe):**
- Book A `4.5`: dropped the "12.5% and 10%" stake figures mid-trim; restored.
- Book B `3.3`: dropped "purchasing power" (a Recycled term) and the exact phrase "revealing exception" (Reading Question 5's wording depends on it); both restored.
- Book B `4.5`: dropped the Swedish "legal duty for essential-goods shops to accept cash" fact mid-trim; restored.
- Book B `4.4`: deliberately dropped "the first rewrite of the relevant law in over a century" (Japan philanthropy-law aside) to control length - confirmed via `qa-todo.md`/checklist that no question or cross-reference depends on this clause, so this one drop was kept rather than restored.

**Verified on every one of the 20 edited articles:** final word count in target range, citation markers == Source Notes (set comparison, both books), all Recycled terms present verbatim, longest sentence 35-45 words with each manually confirmed as a single genuine sentence (not a splitter false positive).

**Not yet done:** re-run the full Phase 5 whole-book audit to confirm items 1-3 collectively resolved the checklist findings and nothing regressed (see qa-todo.md's "After all of the above" section) - deferred until items 4-7 are also addressed, per the user's one-item-at-a-time pacing this session.

## 2026-09-12 (later still) - LTF QA TODO item 2 fixed: backfilled both company-and-geography-audit files

Fixed item 2 from `qa-todo.md`: both books' `drafts/control/company-and-geography-audit.md` were still the blank Phase-3 template through all four drafting batches.

**Method:** rather than re-reading all 40 articles from scratch, built both files from `topic-ledger.md`'s cross-topic evidence register (already comprehensive and current, 184 entries covering all 40 topics) plus a keyword-based region tagger, cross-checked the resulting company/case frequency against the ledger's own "Also referenced (light)" column to confirm no undocumented duplication beyond what item 1 already fixed.

**Real gap found and fixed while backfilling:** Book B topic **1.1 (The Cost of Living and Inflation)** - the book's own prototype topic, drafted 2026-08-28 - had never been added to `topic-ledger.md`'s evidence register at all (only listed in the topic-name table, not the evidence register). Added its primary evidence (US CPI 9.1% June 2022, Argentina 211% inflation 2023, Japan's ~25-year near-zero-inflation baseline + 2024 BOJ move, Japan's 2025 rice-price shock, ECB/BoE/Fed 2% target) to the ledger now.

**Both audit files now record:** per-topic primary/secondary evidence and region tags (all 20 topics, both books); a company/case frequency table flagging only genuine multi-topic repeats (cross-checked against the ledger, all found to be already-documented distinct-angle callbacks, e.g. TSE's two separate actions, Sri Lanka's two separate facts, Japan-debt's precise-vs-rounded figure split); a geographic-balance tally per region.

**Findings flagged (not fixed, since they're read-only audit content, not article defects requiring a rewrite):**
- Book A: US/Americas (13 topics) and Europe (15 topics) both exceed the ~6-topic "no region dominates" guideline in the audit template - flagged as expected given the book's systemic/regulatory subject matter (US/EU regulators are the natural primary source for many global-standard topics), not treated as a violation, since Japan is never the *sole* dominant region in any topic and the actual "no country dominates" checklist intent is about Japan specifically, per house-style §1a.
- Book B: same pattern (Americas 17, Europe 14) for the same reason (personal-finance/market-mechanics topics naturally draw on US/UK/EU cases and data). Book B alone has **zero Latin America primary topics** - a real, if minor, gap; Book A covers Latin America twice (1.5, 3.1) so the two books together are not thin on the region, but Book B alone is.
- Five topics across both books (A: 1.4, 2.4; B: 1.1, 2.1, 3.2) read thin on region count from the keyword-derived tagging (2 or fewer detected regions) - flagged for a manual double-check rather than treated as confirmed defects, since this was a data-driven backfill from the ledger's text, not a fresh close read of the 40 articles. Both 2026-09-12 QA audit agents already did that close read and independently found the geography solid in both books, so this is a low-priority follow-up, not a known problem.

**Verified:** both files have exactly 20 topic rows (mechanical count), and both correctly reflect item 1's SVB/Signature Bank fix (Signature Bank now under A 2.4; SVB confirmed as B 2.5's sole primary use across both books).

## 2026-09-12 (later) - LTF QA TODO item 1 fixed: SVB cross-topic duplication

Fixed the first item from `books/_lets-talk-finance-shared/qa-todo.md` (from the 2026-09-12 whole-book QA audit): Book A `2-4_Stress_Testing_and_Risk_Management.md` and Book B `2-5_Banks_What_They_Do_and_How_They_Fail.md` both used the identical SVB "$40 billion in a single day" statistic as primary evidence.

**Decision:** fix Book A, not Book B. SVB is load-bearing in Book B 2.5 (the Goal, the whole Reading, Reading Questions 1-2, and Discussion Question 2 all build on it directly) but only illustrative in Book A 2.4 (supporting the "a test only measures what it's designed to measure" point). Replaced Book A's case with **Signature Bank** (failed 12 Mar 2023, ~US$110bn assets, well below the US$250bn mandatory-annual-stress-test threshold, lost ~20% of deposits in a matter of hours on 10 Mar via contagion from SVB's collapse two days earlier - confirmed via FDIC Chairman Gruenberg's 27 Mar 2023 remarks) - a distinct, independently-sourced case that makes the same teaching point without reusing Book B's evidence.

**Also fixed while editing:** Reading Questions 3-4 (renamed SVB->Signature Bank), Source Note [3] (now the FDIC speech, replacing the old Fed SVB-supervision-review link), added Source Note [4] for the article's separate, unrelated BOJ/FSA joint-stress-test sentence (which had been mis-piggybacking on the old [3] even before this fix - a pre-existing minor citation slip caught in passing). Updated the Book A teacher-answer-book 2.4 section (Reading answers 3-4, Discussion answers 2, 3, 4, 5) to match the new case. Updated `topic-ledger.md`'s evidence register: new Signature Bank row under A 2.4; SVB row annotated as B 2.5's sole primary use across both books as of this fix.

**Verified after editing** (script, not inspection): word count 463 (was 456, negligible change), citation markers [1-4] match Source Notes [1-4] exactly, 5+5 questions intact, Book A teacher-book Aim==Goal still exact match, Reading/Discussion answer counts still 5+5, zero remaining "Silicon Valley"/"SVB" references in either file, Target vocabulary and confidentiality note untouched.

**Not yet done:** `company-and-geography-audit.md` backfill (qa-todo.md item 2) should record Signature Bank under A 2.4 once that file is populated - deferred to that item rather than done piecemeal here.

## 2026-09-12 - LTF Phase 5: whole-book QA audit run on both books (findings, not yet fixed)

Ran the Phase 5 whole-book audit (`<book>/drafts/control/qa-checklist-full.md`, 89 lines) on both books via two parallel background agents, one per book, each reading all 20 articles in full against the checklist + `house-style.md` + `topic-ledger.md` + `vocabulary-map.md` + `teacher-answer-book.md`. This followed the textinspector.com side-investigation (see below) and precedes any fix work — **nothing has been changed yet**, this is a findings-only pass.

**Clean across all 40 topics, both books, no exceptions:** file presence/naming/numbering, `[N]` marker <-> Source Note correspondence (no gaps/orphans), exactly 5+5 questions per topic, >=1 task-style discussion verb per topic, teacher-answer-book Aim == article Goal word-for-word (all 40), vocabulary three-way match article<->vocabulary-map.md (all 40), confidentiality notes present (all 40), teacher-book Reading answers vs final article wording (16-topic spread sample, zero drift), no single-sentence "moral" endings, no verbatim-duplicate openings.

**Defects found, prioritized:**

1. **Cross-topic evidence duplication, confirmed by direct read, not yet fixed.** Book A `2-4_Stress_Testing_and_Risk_Management.md` and Book B `2-5_Banks_What_They_Do_and_How_They_Fail.md` both use Silicon Valley Bank's "more than US$40 billion in a single day" as **primary opening evidence** in each topic - same fact, same role, different surrounding argument. `topic-ledger.md` flagged this as "borderline" during Batch 2 drafting but the flag was never acted on. Fix: swap one book's opening anchor to a different bank-failure case, or demote one occurrence to an explicit light callback to the other topic.
2. **`company-and-geography-audit.md` was never populated, in either book** - both are still the blank Phase-3 template (`_(draft)_` placeholders) despite being the explicit Phase-4 guard against exactly defect #1. Both audit agents independently rebuilt the geography picture by hand from the 40 articles and found the underlying geographic spread is actually fine in both books (Japan appears frequently per house-style §1a's intent but never structurally dominates; no other single country dominates); the control mechanism itself simply never ran. Process gap, not a content problem - but it's why #1 slipped through uncaught.
3. **Systematic word-count and sentence-length drift in Parts 3-4, both books.** Parts 1-2 sit close to the 440-475 target in both books; Parts 3-4 drift up consistently - Book A up to 537 words (3.3 Trade Policies and Tariffs), Book B up to 544 (4.3 Business of Sport, Art and Culture), most Part 3/4 topics in both books now 500-540 words. The longest sentences (40-47 words) in both books are also concentrated in these same later-batch topics. Matches the length-editing session's known state (2026-09-11) but the agents' read confirms it as a genuine batch-level pattern, not scattered outliers. Recommend one more targeted editorial pass on Parts 3-4 specifically, both books, before the Phase 7 PDF page-fit check.
4. **Currency-style violations - Book B only, 3 topics.** `1-1`, `1-2`, `1-5` use bare `¥`/`£` symbols ("¥4,260," "£13 billion," "£85,000") instead of the required `JPY`/`GBP` ISO-code format (house-style.md §3) - inconsistent with `4-3`/`4-4` in the same book, which format currency correctly. Book A has zero violations. Mechanical, easy fix.
5. **Recycled-vocabulary floor violated - Book A only, 2 topics.** `1.2` Central Bank Digital Currencies and `1.5` Financial Inclusion Initiatives each have only 2 recycled terms against the checklist's 3-5 floor (the "none yet" exemption applies only to topic 1.1). Already self-documented as a known limitation in Book A's own `vocabulary-map.md`, but the rule itself remains technically unmet for these two topics - needs either a formal documented exception or one more genuinely-appearing recycled term added to each.
6. **Missing deliverables, both books:** no `glossary.md`, no `00_How_This_Resource_Is_Organized.md` (front matter), for either book. Not a defect in the 40 articles, but both checklist sections that depend on them (Glossary section; the front-matter line of Whole-book) can't be evaluated yet, and the vocabulary three-way match is currently only checkable on 2 of its 3 legs (article <-> map; article/map <-> glossary tags still pending).
7. **Minor/cosmetic:** Book B has several topics citing Source Notes out of strict numeric order (e.g. `[7]` before `[1]` in `3-1`) - every marker still resolves correctly, no functional break, just doesn't match the checklist's implicit sequential-citation convention. Book B `4.5. The Future of Money` leans on essentially two countries (Sweden, Japan) for its comparative weight - not a violation but thinner than the "≥3 regions" spirit; worth a look at the same editorial pass as #3.

**To resume:** fix #1 (SVB duplication) and #4 (currency style) first - both mechanical and fast; then the targeted Parts 3-4 length/sentence pass (#3, folds into the already-planned length-editing follow-up); then decide #5 (accept as documented exception, or patch); then build the glossary and front-matter file, which are needed regardless and required before the Glossary checklist section and the third leg of the vocabulary three-way match can run. After all of that, this whole-book audit should be re-run once (per the standing three-way cross-check practice established for the teacher answer books).

## 2026-09-11/12 - textinspector.com readability analysis: markdown/file-upload period-stripping bug found

Explored running the manuscript through textinspector.com (CEFR/readability scorer) per user request. Produced several rounds of prose-only extract files (`books/<book>/drafts/output/snapshots/0911/`) before getting a usable analysis - each round surfaced a real, separate artifact:

- **Round 1** (full articles incl. headings/questions/Source-Note URLs, `---` delimiter): CEFR C2+/D1, Flesch-Kincaid Grade ~181-182, "Average Sentence Length" ~458 words. Root cause: the "Split documents at this character" field appears to ALSO serve as textinspector's sentence-boundary delimiter when set, so with `---` (or later `~`) in that field it split only on the delimiter and ignored `.`/`?`/`!` entirely - each 20-article file scored as if it had exactly 20 "sentences" (one per article).
- **Round 2** (Reading-prose-only extract, citation markers `[N]` stripped, `~` delimiter): same delimiter-swallows-periods bug, confirmed by "Sentence count" = 20 exactly in both books' CSVs.
- **Round 3** (no delimiter at all, `.md` file upload): user found via a screenshot of textinspector's own preview that periods were being stripped on import - not a delimiter issue this time, a markdown-file-import cleaning bug. Saved plain `.txt` copies (verified UTF-8, no BOM, ASCII periods confirmed present in the raw bytes) - user reported periods were STILL stripped on `.txt` upload too, confirming the bug is in textinspector's file-upload import path generally (both `.md` and `.txt`), not encoding and not extension-specific.
- **Round 4 (working):** user pasted the text directly into textinspector's input box instead of uploading a file, bypassing the import imports's cleaning step entirely. This produced believable results: Book A 449 sentences avg 20.8 words/sentence, Book B 476 sentences avg 19.6 words/sentence (both within the B1+/B2 house-style 15-25 word target), Flesch-Kincaid Grade 11.2/10.2, but **CEFR level C1+ both books** (Percentage 68.00/64.44) against a B1+/B2 target - driven by vocabulary sophistication (AWL academic-word coverage ~14-15%, EVP A1-type-count only ~33%), not sentence mechanics. CSVs saved as `textinspector_ltf_book1_all_prose-only2.csv` / `..._book2_all_prose-only2.csv` in each book's `output/snapshots/0911/` folder.
- **Preferred behavior going forward:** textinspector.com's file-upload path (any extension) cannot currently be trusted to preserve periods - always paste text directly into their input box instead of uploading a file, until/unless this is confirmed fixed on their end.
- **Follow-up in progress:** built a combined known-finance-words list for textinspector's "known words list" feature, extracted from all 40 articles' New+Recycled vocabulary terms (`books/_lets-talk-finance-shared/textinspector-known-words.txt`, 349 words; `...-acronyms.txt`, 13 acronyms both cases; `...-combined.txt`, both merged) - intended to let the CEFR scorer stop penalizing deliberately-taught finance vocabulary, isolating the C1+ signal to genuinely incidental difficulty. Not yet re-run through textinspector with the known-words list applied.

## 2026-09-11 (latest) - LTF: both teacher answer books drafted (40 topics)

User asked where teacher answer books fit in the schedule. Investigated the model this whole project is based on -- `IR teacher answer book.md` in the Marubeni/Ishida repo -- and its own revision-audit history (`IR revision audit report.md`). Finding: the IR answer book was NOT a Phase-6/assembly deliverable. It was created 2026-08-18, close to when the articles themselves were drafted, went through its own revision passes (mismatches found/fixed 2026-08-20) and an expansion (2026-08-24), and from then on a **three-way vocabulary cross-check (articles / answer book / glossary)** became a standing audit re-run after every structural change to the articles. The answer book is a first-class artifact kept in permanent lockstep with the articles, not something built once at the end. This resolved an inconsistency in `PROJECT-PLAN.md` §4 (Phase 5's QA checklist item checks the answer book against articles, implying it exists by then, but Phase 6 "Assemble" lists it as being built there) -- the correct reading is Phase 5, not Phase 6.

Conclusion: since all 40 topics (both books) are now drafted with no `teacher-answer-book.md` for either book, this was a real gap. User asked to draft both now. Commits `1a5190a` (Book A) and `8a3d7f7` (Book B).

**Both `<book>/drafts/teacher-answer-book.md` files are now complete** (per PROJECT-PLAN.md D6 repo layout). Per topic, each contains: `**Aim:**` (must match the article's Goal sentence word-for-word), `**Target vocabulary:**` (must match the article's New terms line exactly), 5 Reading answers verified against final article text and question wording, 5 Discussion answers in the IR model's style -- what a strong response covers and why, naming the legitimate alternative view where a question is genuinely open, not a single fixed answer -- and a per-topic confidentiality note.

**Verification method:** wrote a script (not inspection) to check, for every one of the 40 topics: Aim == article Goal sentence exactly; Target vocabulary set-equal to New terms (punctuation-normalized); Reading-answer count == 5 Reading Questions; Discussion-answer count == 5 Discussion Questions; confidentiality note present. All 40 topics pass clean in both books.

**To resume:** per the IR precedent, treat the three-way cross-check (articles / answer book / glossary) as a standing audit to re-run after any future article edit -- most immediately relevant once DDobson's editorial read of Batches 1-4 produces article changes, since those would need propagating into the just-written Aim/Target-vocabulary lines and Reading answers. No glossary exists yet for either book (also a D5/D6 deliverable, not yet started) -- the three-way check can only run in full once that exists too.

## 2026-09-11 (later still) - LTF Batch 3-4: length trim and long-sentence splits complete

Followed up the checklist run with the editorial length/sentence pass it had flagged as outstanding. Commit `3b2880f`.

**Result:** all 20 Batch-3/4 Readings edited except the 6 already in range (A 3-1, A 4-1, B 3-4, B 3-5, plus B 3-1 and A 3-4 which only needed light trims). Word-count range is now 479-544 (mean 511), down from 479-589 (mean ~530). Longest sentence per article is now <=47 words everywhere, most <=44, down from as high as 76 words (A 4-3) and 63 words (A 4-5).

**Method:** split every 3+-clause sentence the checklist run flagged, then trimmed adjectives/restated clauses to bring word counts down further, always re-checking that (1) every cited factual anchor survived with its marker, (2) every Recycled/New vocabulary term for that topic still appears literally in the body, and (3) citation markers stayed distinct/sequential/gap-free and matching the Source Note count. Caught two cases where a first cut had accidentally dropped a Recycled term or a cited figure (B 3-3 "purchasing power", A 4-3 the JPY 100m-wall figure) and restored them before moving on.

**Two pre-existing content slips fixed while editing (not part of the original checklist findings):**
- B 3-3 Discussion Q4 asked to compare an oil shock with "the slow rise in copper demand," but the Reading never mentions copper - reworded to the rare-earth/critical-minerals case the Reading actually makes.
- B 3-2's tulip-mania opening claimed a bulb traded for "the price of a canal house in Amsterdam," which the cited NY Fed source doesn't support (it describes an earlier 1633 house-for-tulips exchange, not a crash-time canal-house price) - reworded to match the source.

**Verification:** wrote a script to re-check all 20 articles after editing (vocab-map exact match, Recycled terms present, 5+5 questions, citation integrity) rather than trusting inspection alone - all 20 pass clean.

**Not pushed further:** most articles still sit at 497-544 words, above the ~490 D3 target, but cutting further risks losing factual anchors from articles that are already dense with 3-4 regions of evidence. Per the existing decision record, the real gate is the Phase-7 rendered-PDF page-fit check once a 2-column A4 reference DOCX exists for this series - word count at draft stage is a proxy, and Batch 2's own shipped range (428-490) already showed 490 was aspirational, not hard.

**To resume:** DDobson's editorial read of Batches 1-4 (prose quality, paragraph rules, question quality - this pass only checked mechanics); then Phase 5 (whole-book QA), per below.

**Correction (caught next session):** there is no Batch 5. Both books are exactly 4 Parts x 5 topics = 20 topics each (PROJECT-PLAN.md D2, D8, §3), and Batches 1-4 cover Parts 1-4 in full for both books. **All 40 topics across both books are now drafted.** "Batch 5" above wrongly extrapolated the batch pattern without checking the plan. Per PROJECT-PLAN.md §5, what actually follows Phase 4 (drafting, now complete) is: Phase 5 - full whole-book QA per book against `control/qa-checklist-full.md` (plus DDobson's editorial read, not yet done for any batch); Phase 6 - assemble each book (Part dividers, front matter, numbering); Phase 7 - build the 2-column A4 reference DOCX (does not exist yet) and run the PDF page-fit loop; Phase 8 - sign-off and delivery.

## 2026-09-11 (later) - LTF Batch 3-4: article-checklist + URL verification pass run

Ran the deferred checks on all 20 Batch-3/4 Readings (Books A + B, Parts 3-4): `_lets-talk-finance-shared/article-checklist.md` mechanically, plus a WebFetch/WebSearch verification pass over prose and every Source Note URL. Commit `1f79710`.

**Checklist - all 20 pass on:** 6-subsection template + numbering, exactly 5+5 questions, citation-marker integrity (distinct `[N]` == Source Note count, no gaps), >=1 anchor case + >=2 factual anchors, >=3 regions with no country dominant, 6 New terms, all Recycled terms verified present in the Reading/questions, vocab-map rows match the articles exactly (all 20), article shape + opening match the batch shape-plans, endings article-specific, no self-reference, no kicker endings.

**Checklist - issues found:**
- **Word count over the D3 ~490 ceiling in 14 of 20 Readings; 6 are 540-590** (worst: A 4-5 = 586, B 3-3 = 589 [594 after edits], B 3-5-COVID recovery A 3-5 = 547; also B 4-2 552, B 4-5 561, B 4-1 542, B 4-3 576, B 4-4 546, A 4-3 538, A 4-4 527). In range: A 3-1 484, A 4-1 479, A 4-2 496, B 3-5 497. Real gate is the Phase-7 rendered-PDF page-fit check (no 2-column A4 reference DOCX exists yet); at draft stage this is the main failure. **Not fixed this pass** - folds into DDobson's editorial read of Batches 1-4.
- **Over-long sentences** (house-style: mostly 15-25 words; Batch-2 working ceiling <=38). Genuine offenders, worst first: A 4-5 (63w Sakhalin sentence + four more 47-54w), A 4-3 (69w Zucman sentence + 47w Japan-tax + 47w toolkit), B 3-3 (51w), A 3-5 (47w QE sentence + 42w output-gap), B 4-4 (60w + 55w), B 4-1 (53w revenue-mix chain-list). Several have 3+ subordinate clauses - need splitting, not just trimming. **Not fixed this pass.**
- **Recycled-term lists at the floor (3)** in A 3-1, A 4-2, A 4-3, B 3-2, B 4-3, B 4-4 - checklist minimum is 3 so they pass. Extended the "known limitation" note in both `vocabulary-map.md` files to cover Parts 3-4.

**URL verification - the 4 journal-flagged items all resolved:** A 3-4 [4] (SSA International Update June 2023 confirmed at that URL, covers France 62->64), B 3-2 [6] (Princeton UP - exact title/subtitle confirmed), B 3-1 [4] (CNBC `decpoint18` slug is real, content matches), B 4-4 Rob Reich *Just Giving* (already reworded - text names Reich as a critic, no book title, no citation needed).

**URL verification - 6 real citation defects found and fixed (commit `1f79710`):**
1. **A 3-3 [1]** - "foreign exporters absorbed nearly half" was cited to NY Fed Source [1], which found the OPPOSITE (~90% on US firms). The "nearly half" is Caroline Freund's study (CEPR/VoxEU, DP 21798, 2026). Added as a distinct source; renumbered markers 2-7 to keep first-appearance order (7 sources now, integrity re-verified).
2. **B 3-3 [1]** - cited DOE page was a *2026* SPR release of 172m barrels ("President Trump authorized..."), not the March 2022 release of 180m. Swapped to DOE "History of SPR Releases"; reworded sentence ("largest drawdown in the reserve's history", released over six months).
3. **B 3-2 [4]** - nippon.com "Heisei Blues" URL 404'd (stored URL had a plain apostrophe; live URL uses `%E2%80%99s`). Fixed. Content fully verified (six cities, 87% peak-to-trough, 15 years, 2005 upturn).
4. **B 3-2 [5]** - the Luna figures ("~$87 -> fraction of a cent, >$40bn erased") were not in cited Source [5] (Richmond Fed, which says "$31 -> $0.01"). Reworded to the sourced range ("near US$120 in early April 2022 ... from about US$80 to almost nothing over three days") and added Harvard Law CorpGov "Anatomy of a Run" as [7]. Topic-ledger row updated.
5. **B 3-1 [1]** - RBC "Great Narrowing" supports the 40.7% concentration figure but NOT the "2025 S&P 500 ~18%, mostly from earnings" claim also cited to it. Added First Trust "S&P 500 Index 2025 Recap" (8 Jan 2026: ~17.9% total return, >75% from EPS) as [7]. Also softened "passing 70,000 for the first time" -> "in intraday trading" (Nikkei closed ~69,404 on 16 June 2026).
6. **B 4-4 [5]** - Alliance Magazine URL (slug "29-billion") didn't support the article's GBP 37.6bn Wellcome endowment figure. Swapped to Wellcome's own 2024/25 annual report page (endowment ~GBP 37.6bn at 30 Sep 2025 - current, correct).

**URL verification - minor / accepted as context (not changed):**
- B 3-2 [1] - NY Fed tulip page supports the Feb 1637 Haarlem crash but not the "rarest bulb ~ price of an Amsterdam canal house" trope (page cites a 1633 Hoorn house-for-tulips exchange). Left as widely-attested context.
- B 4-4 [1] - Regulatory Review page supports the DAF-vs-foundation payout contrast but doesn't state "5%" explicitly (standard IRC §4942). Could add an IRS source later.
- B 3-1 [5] - Japan Times slug `nikkei-70000-first-time-june` unverifiable (402 paywall); the confirmed Japan Times article on the same event is at `.../2026/06/16/markets/boj-meeting-june-2026/`. Consider switching.
- First-appearance marker order is loose in the original B 3-1 / B 3-2 / B 3-3 drafts (e.g. B 3-1 had `[3]` before `[2]` from the start). Checklist "no gaps 1,2,3..." is satisfied; strict reordering deferred to the editorial pass.

**URL verification - confirmed good (spot-checks):** A 3-3 [1] (NY Fed, exact), A 3-4 [3] & [5] (SSA press release, Korea Herald - exact), B 3-1 [6] (CNBC BOJ - exact), B 3-2 [2] [3] (Fed History 1929, nippon.com Nikkei - exact), B 4-4 [1] [3] (Regulatory Review, CEP - confirmed). Known 403 bot-blocks (not defects, per the standing memory note): congress.gov, IMF, BLS, OECD, mof.go.jp / mhlw PDFs, SEC, Bloomberg, Japan Times, France24, Alliance/Wellcome; Reuters is fully tool-blocked (B 3-4 [1] [4] unverifiable by tool, events well documented).

**To resume:** (1) DDobson editorial read of Batches 1-4 (`books/*/drafts/articles/*.md`), which should absorb the word-count trim (heaviest on A 4-5, A 4-3, B 3-3, A 3-5, B 4-4) and the long-sentence splits; (2) apply feedback; (3) Batch 5 = Part 5 of both books.

## 2026-09-11 - LTF Batch 3 + Batch 4 Readings drafted from the research briefs

Picked up a step that had been missed: Batch 3 (2026-09-10) and Batch 4 (2026-09-11) had only reached step 1 of the per-batch pipeline — research briefs on disk, no article Readings. Drafted all 20 outstanding Readings from the briefs, following `_batch3-shape-plan.md` / `_batch4-shape-plan.md` and `house-style.md`, committing per book-part.

**Batch 3 (Part 3 of both books):**
- Book A: 3.1 Green Finance Initiatives, 3.2 Infrastructure Investment, 3.3 Trade Policies and Tariffs, 3.4 Pension Reform, 3.5 Global Economic Recovery Post-COVID. Commit `962667d`.
- Book B: 3.1 What Moves Stock Markets, 3.2 Bubbles, Crashes and Manias, 3.3 Commodities: Oil, Metals and Food, 3.4 Currencies and Exchange Rates, 3.5 Emerging Markets and Development Finance. Commit `df64b2d`.

**Batch 4 (Part 4 of both books):**
- Book A: 4.1 Anti-Money Laundering (AML) Regulations, 4.2 Financial Literacy Programs, 4.3 Wealth Inequality and Redistribution Policies, 4.4 Corporate Governance and Accountability, 4.5 Economic Diplomacy and International Cooperation. Commit `8129276`.
- Book B: 4.1 Tax: How Governments Raise Money, 4.2 Government Debt and Deficits, 4.3 The Business of Sport, Art and Culture, 4.4 Philanthropy, Foundations and Impact, 4.5 The Future of Money. (This commit.)

Each Reading: six-subsection template matched to `2-5_Sovereign_Debt_Management.md`; assigned article shape + opening style + lead regions + Japan placement from the batch shape plan; ~440–475 words; 4–6 `[N]` markers, each to a URL from the brief's verified "Suggested source list"; New terms drawn from the brief candidates and confirmed to appear; Recycled terms confirmed to genuinely appear (short lists kept short, per the vocab-map known-limitation note — Book A/B Part 4 topics are policy pieces with thin carry-over from Parts 1–3).

**Source-note discipline where the briefs lacked a verified deep URL:** substituted a different verified anchor, dropped the figure, or named the case without a citation as pattern context. Examples: A 4.4 names Sarbanes-Oxley and Satyam as dated context without their own markers; A 4.5 leans on the CFR frozen-assets explainer and AIIB's own About page; B 4.1 gives the EU high-VAT point qualitatively (no uncited 27%-Hungary anchor); B 4.3 gives the Germany-vs-US arts-funding contrast qualitatively (no uncited NEA budget figure).

**Vocab maps + topic ledger updated.** Book A and Book B `vocabulary-map.md` Part-3 and Part-4 rows populated and the "populated" header lines extended. `topic-ledger.md` cross-topic evidence register got ~28 rows for Batch 3 Book A, ~24 for Batch 3 Book B, ~28 for Batch 4 Book A, ~30 for Batch 4 Book B, each cross-referencing where a case is light-referenced in another topic (e.g. Japan debt "well over 200%" in B 4.2 vs the precise ~206%/BOJ-48%/foreign-8% figures reserved to A 2.5; TSE March 2023 cost-of-capital push in A 4.4 vs TSE April 2022 market restructuring in B 2.1; Kenya 2024 finance bill framed as domestic politics in B 4.2 vs IMF mechanics in B 3.5).

**Still to do for all 20:** run `article-checklist.md` on each Reading (deferred, noted in each commit message); a WebFetch verification pass over the new prose and Source Note URLs. Flagged for that pass: A-3-4 Source Note [4] cited for the France pension-age suspension; B-3-2 Source Note [6] Princeton UP URL slug; B-3-1 Source Note [4] CNBC URL segment; B-4-4 the Rob Reich *Just Giving* reference (named, uncited).

**To resume:** DDobson editorial read of Batches 1–4 (`books/*/drafts/articles/*.md`); then apply feedback; then the checklist + URL verification pass on Batches 3–4.

## 2026-09-10 - Let's Talk Finance Batch 2 drafted and mechanically checked

Resumed Batch 2 (Part 2 of both books). The 8 missing research briefs from the 2026-08-31 session were re-run and delivered; combined with the 2 already on disk, all 10 Batch-2 briefs are in `books/_lets-talk-finance-shared/research-briefs/` and committed.

**All 10 Batch-2 Readings drafted** from the briefs, per `_batch2-shape-plan.md`:
- Book A: 2.1 Regulatory Responses to Market Volatility, 2.2 Credit Rating Agencies Oversight, 2.3 Insurance Market Regulation, 2.4 Stress Testing and Risk Management, 2.5 Sovereign Debt Management (leads with Japan — ~206% debt/GDP per IMF WEO Apr 2026, BOJ holds ~48% of JGBs, foreigners ~8%).
- Book B: 2.1 How Companies Raise Money, 2.2 Startups, Venture Capital and Failure, 2.3 The Gig Economy and Income Security, 2.4 Executive Pay and Inequality Inside Firms, 2.5 Banks: What They Do and How They Fail.

**Mechanical checklist — all 10 pass:** Readings 435–490 words (slightly above Batch 1's 428–457 but within the D3 ~490 ceiling); longest sentence ≤38 words in every article; citations sequential and in order-of-first-appearance, marker count == Source Note count; 5 Reading + 5 Discussion questions each; 6 New terms + 3–4 Recycled (all Recycled terms verified to appear in the Reading/questions text).

**URL verification — all 31 Source Note URLs checked this pass.** Fixes made:
- A 2.1: JPX page corrected to the circuit-breaker rules page; Brady report -> SEC Historical Society PDF; SEC trading-halts page (404) -> investor.gov circuit-breakers glossary.
- A 2.2: SEC OCR report -> OCR reports-and-studies index (specific PDF URL kept 404ing); DOJ release -> `/archives/` path; ESMA -> CRA activities page.
- A 2.3: Japan FSA -> "Capital Requirements for Insurance Companies in Japan" page.
- A 2.4: EBA -> the dedicated 2025 stress-test results release.
- A 2.5: split into 4 sources — IMF WEO DataMapper now carries the 206% claim (was wrongly on CRS); CRS RS22331 moved to [4] for the US foreign-holdings numbers.
- B 2.1: India IPO sentence reworded to what DD News actually says (record 268 NSE IPOs / ~US$19.5bn, "among the busiest markets", not "second-largest").
- B 2.2: venture figure US$425bn -> US$440bn (Crunchbase 2025 recap); Crunchbase and IMF "Riding Unicorns" URLs corrected to live pages.
- B 2.3: ILO platform-count sentence softened to "about five-fold in the decade to 2020" (matches the cited release, which does not carry the 142/777 breakdown).
- B 2.5: added a DICJ source [3] for the Japan ¥10m limit (was leaning on the FDIC page, which only covers the US$250k figure).
- Known 403 bot-blocks left as canonical primaries (all cross-corroborated in the briefs): congress.gov, epi.org, imf.org, sechistorical.org, sec.gov press pages, mof.go.jp / dmo.gov.uk PDFs, dic.go.jp, jftc.go.jp.

**Vocab maps + topic ledger updated.** Both `vocabulary-map.md` Part-2 rows populated. Known-limitation notes extended to Parts 1–2: Book A's Part-2 opener 2.1 recycles only core-set terms (regulator/exchange/market) because a circuit-breaker mechanics piece shares little settled vocabulary with Part 1; Recycled lists list only terms that genuinely appear. `topic-ledger.md` evidence register got ~40 Batch-2 rows.

**Cross-topic overlap to flag at review:** Silicon Valley Bank (Mar 2023) is primary evidence in BOTH A 2.4 (below-threshold / interest-rate-losses angle — "the risk the test missed") and B 2.5 (one-day-run / maturity-transformation angle — opening dated event). Different facts/angle, so within the §10 "same company, different fact" allowance, but borderline — ledger rows now cross-reference each other.

**Also for the editorial read:** A 2.3 cites the EIOPA Solvency II landing page for the "1-in-200-year" capital calibration; that exact phrasing is in the Directive, not the landing page (standard Solvency II framing, but not on the cited page).

**Batch 2 still awaits DDobson's full editorial read** (prose quality, paragraph rules, question quality — only the mechanical checklist has run). Batch 1 also still awaits that read.

**To resume:** (1) DDobson reviews Batch 1 + Batch 2 (`books/*/drafts/articles/1-*.md` and `2-*.md`); (2) apply feedback; (3) Batch 3 = Part 3 of both books — Book A: 3.1 Green Finance, 3.2 Infrastructure Investment, 3.3 Trade Policies & Tariffs, 3.4 Pension Reform, 3.5 Global Economic Recovery Post-COVID; Book B: 3.1 What Moves Stock Markets, 3.2 Bubbles Crashes & Manias, 3.3 Commodities, 3.4 Currencies & Exchange Rates, 3.5 Emerging Markets & Development Finance. Same pipeline: research-brief agents (smaller waves — 10 at once burned a session in Batch 2's first attempt), then draft, expand, checklist, verify URLs, update maps + ledger.

## 2026-08-28 - Let's Talk Finance two-book rebuild: planning, prototypes, Batch 1 drafted

**Session summary.** Speaking with PowerPoint put on hold. Started the Let's Talk Finance track: two books to be produced to the standard of the completed "Let's Talk: Investor Relations" project (separate repo, `02. Clients/Marubeni/Ishida, Tetsuya`). See `project-learning.md` 2026-08-28 entry for the durable decision record; `books/Let's Talk Finance/PROJECT-PLAN.md` is the controlling document.

**What was done:**
- Read the whole IR project (process guide, project plan, QA checklist and its 6 audit passes, vocabulary map, glossary, teacher answer book, sample articles) to extract the standard. Measured the IR articles' actual shipped Reading length (422–487 words; the QA checklist's "450–550" was aspirational and not held to).
- Resolved all 8 project decisions (D1–D8) with the user across the session. Key ones: B1+/B2 level; write from a Japanese reader's vantage point but keep every topic genuinely global (≥3 regions, no country dominant); Reading fills one A4 2-column page under the Goal; every fact cited to a live URL; Book A keeps its 20 topics (fix the 3 defective ones); Book B's 20 new topics approved.
- Built the repo scaffold: `books/_lets-talk-finance-shared/` (house-style, per-article checklist, topic ledger, process guide, term bank), per-book `drafts/{articles,control,output}/`, archived old Book A material to `books/Let's Talk Finance/_archive/`, gitignored `Thumbs.db`.
- **Phase 2 — 2 calibration prototypes drafted, reviewed through several rounds, APPROVED by the user:** `Let's Talk Finance/drafts/articles/1-1_Cryptocurrency_Regulation.md` and `Let's Talk Finance 2/drafts/articles/1-1_The_Cost_of_Living_and_Inflation.md`. The review rounds fixed: dead/guessed URLs (3 of 4 in the first crypto draft were invalid), the Japanese-vantage-point framing (got it wrong twice — too non-Japanese, then over-corrected too Japan-centric), and the paragraph-writing rule (carried from IR: no mid-idea breaks, no single-sentence kicker endings).
- Added `books/_lets-talk-finance-shared/article-checklist.md` — a per-article minimum gate distinct from the whole-book `qa-checklist-full.md`.
- **Phase 4 Batch 1 started.** 8 background research agents delivered fact/source briefs (all URLs opened and verified) for A 1.2–1.5 and B 1.2–1.5, saved to `books/_lets-talk-finance-shared/research-briefs/`. 4 agents hit session/rate limits mid-run and were re-launched successfully after reset.
- Drafted all 8 Batch-1 Readings from the briefs, then did one revision pass. Committed as `0b7c65a` (briefs + first drafts) and `16b318c` (revision pass).

**State at session end — Batch 1 is NOT finished:**
- All 8 Readings: structure complete (6 subsections, 5+5 questions), citation integrity OK (marker count = Source Note count; fixed 4 attribution errors in the revision pass), all long sentences split (were 42–51 words, now ≤36), global spread and Japanese vantage point OK.
- **Outstanding: 7 of 8 Readings are ~60–90 words short of the ~440–475 target** (they sit at 357–381; A 1.2 is in range at 433). Each needs one short expansion from unused brief material (the briefs have plenty spare — SPIVA caveats, Pix scale figures, Japan "grey zone" detail, BIS global house-price context, UK APP-fraud numbers, etc.).
- **Not yet done for Batch 1:** run the full `article-checklist.md` on each of the 8; populate `vocabulary-map.md` (New/Recycled terms) in both books; record Batch-1 primary-evidence cases in `topic-ledger.md`'s cross-topic evidence register; hand the batch to the user for review.

**Batch-1 shape/opening plan** (for designed variety) is at `books/_lets-talk-finance-shared/research-briefs/_batch1-shape-plan.md`.

## 2026-08-31 (later) - Let's Talk Finance Batch 2 started; session limit hit early

- **Batch 1 fully committed and closed** — `7ac050f`, `b96e722`, `7e8a167`, `2e4f1df`. All 10 Batch-1 Readings pass the per-article mechanical checklist; all 48 Source Note URLs verified (4 are the known 403 bot-block on real primary pages — BLS, CFPB archive, IMF Fintech Note; RBA FSR was removed and its Australia sentence dropped from B 1.2). DDobson caught one phrasing error post-review: A 1.2 "nearly nine in ten" -> "more than nine in ten" (85/93 = 91.4%). **Batch 1 still awaits DDobson's full editorial read.**
- **Batch 2 = Part 2 of both books.** Shape/opening plan at `books/_lets-talk-finance-shared/research-briefs/_batch2-shape-plan.md` (committed `650da7f`). Topics — Book A: 2.1 Market Volatility, 2.2 Credit Rating Oversight, 2.3 Insurance Regulation, 2.4 Stress Testing, 2.5 Sovereign Debt Management (leads with Japan — highest debt/GDP, ~90% domestically held). Book B: 2.1 How Companies Raise Money, 2.2 Startups & VC, 2.3 Gig Economy, 2.4 Executive Pay (inside-firm inequality), 2.5 Banks & How They Fail.
- **10 Batch-2 research-brief agents launched.** As of session end, **2 of 10 delivered and committed** (`3df74f1`): `A-2-1_Market_Volatility.md`, `A-2-4_Stress_Testing.md`. The other 8 (A-2-2, A-2-3, A-2-5, B-2-1 … B-2-5) were still running when the 5-hour session limit was reached early (heavy agent use). Their transcripts are saved but partial-run agents are NOT cleanly resumable — **re-launch the 8 missing briefs with the same prompts** (agent prompts are in this session's history / reconstruct from `_batch2-shape-plan.md` + the Batch-1 brief prompt pattern).
- Also this session: Book A loose cover/description files were tidied into `books/Let's Talk Finance/cover/` (committed `3df74f1`).

**To resume Batch 2:** (1) re-launch the 8 missing research briefs (A 2.2, A 2.3, A 2.5, B 2.1, B 2.2, B 2.3, B 2.4, B 2.5); (2) when all 10 briefs are in, draft the 10 Readings from them; (3) expand to ~440–475 words; (4) run `_lets-talk-finance-shared/article-checklist.md` on each; (5) update both `vocabulary-map.md` Part-2 rows + the topic-ledger evidence register; (6) DDobson review. Same pipeline as Batch 1.

**Lesson for next time:** 10 parallel research agents per batch is too heavy for a 5-hour window — it burned the session before drafting could start. Next batch: run agents in smaller waves (e.g. 4–5 at a time), or accept that a batch spans two sessions (agents in session 1, drafting in session 2).

## 2026-08-31 - Let's Talk Finance Batch 1: expansion + checklist pass complete

Resumed Batch 1. Commits `7ac050f` (length expansion) and `b96e722` (checklist/vocab/ledger).

- **Expanded all 10 Batch-1 Readings to target length.** Were 357–433 words; now 428–457. Facts added from the research briefs (nothing new researched): GDPR cumulative fine total, India account-dormancy point, Japan grey-zone/multiple-debtor detail, 2000–24 return window + diversification, BIS global house-price level + Singapore HDB, UNODC SE-Asia scale + Japan SNS-fraud category. New sources added: DLA Piper GDPR survey, RBA FSR, FRBSF Asia Focus, BIS RPP, Cowles working paper (Auckland), gov.sg, UNODC. All sentences now ≤38 words.
- **URL verification pass.** Fixed 2 broken links in B 1.4 (BIS `pp_residential.htm` 404 → `data.bis.org/topics/RPP`; ScienceDirect 400/paywall → open Cowles PDF). Three 403s remain (CFPB archive, IMF Fintech Note, RBA FSR) — the known bot-block pattern on real primary pages; cite as-is.
- **Vocabulary Focus cleaned up.** All 10 trimmed to exactly 6 New terms (several were 8–10). Recycled lists set honestly (0–3 terms). **Design finding:** Book A Part 1 topics barely share vocabulary, so recycled lists are thin and drawn from a core-recurring set rather than the preceding topic. Documented in both `vocabulary-map.md` files; flagged for the Phase-1 Part-grouping review. Book B Part 1 shares a bit more (money-basics core).
- **Both `vocabulary-map.md` Part-1 rows populated**; Core Recurring Terms set for both books.
- **Topic-ledger cross-topic evidence register populated** with all ~44 Batch-1 primary-evidence cases. No collisions (India appears as primary evidence in A 1.3 / A 1.4 / A 1.5 but with a different fact each time — allowed).
- **All 10 Batch-1 Readings pass the per-article mechanical checklist** (`_lets-talk-finance-shared/article-checklist.md`): 428–457 words, longest sentence ≤38, citation markers sequential and = Source Note count, 5+5 questions, 6 New terms, ≥3 regions, no country dominant.

**Batch 1 = 10 Readings ready for DDobson review** (2 approved prototypes A 1.1 / B 1.1, + the 8 new). Not yet done: a close editorial read for prose quality / paragraph rules / question quality (only the mechanical checklist has run); teacher answer book entries; glossary. Those come after review or in Phase 5.

**To resume:** (1) DDobson reviews Batch 1 (all of `books/*/drafts/articles/1-*.md`); (2) apply review feedback; (3) Batch 2 = Part 2 of both books — Book A: 2.1 Market Volatility, 2.2 Credit Rating Oversight, 2.3 Insurance Regulation, 2.4 Stress Testing, 2.5 Sovereign Debt; Book B: 2.1 How Companies Raise Money, 2.2 Startups & VC, 2.3 Gig Economy, 2.4 Executive Pay, 2.5 Banks & How They Fail. Launch 10 research-brief agents first (same pattern as Batch 1), then draft, expand, checklist.

## 2026-07-07 - Presentation Skills Visual Generation: Representation Fixes And Batch Progress

- Continuing Stage-3-prep visual generation (36-image register at `books/Presentation Skills/images/image_register.json`). Prior work this week had already established the OpenAI-vs-PIL technique split, native transparency handling, and produced 9 approved images (8 scenarios + `01-1-three-phases` icon-sheet-composite diagram + the `05-1-logic-tree` pair) -- see `project-learning.md` entry same date for the durable technique/decision summary.
- User flagged a real representation problem after reviewing the approved scenario batch: every presenter was brown-skinned/dark-haired regardless of scene, and the government-scenario image (`appA-2`) contained a literal US flag -- inappropriate for a textbook aimed at Japan-based students, and geographically wrong for a generic government scene. Root cause: the shared `photo_style` prompt block used generic "diverse" wording with no ethnicity anchor, and per-image prompts described government settings vaguely ("civic auditorium", "seal/banner... optional") which let the model default to American iconography.
- First fix attempt (explicit "East Asian/Japanese in appearance" phrase added once, mid-paragraph, plus "no national flags of any specific real country") was insufficient: regenerating all 8 scenario images produced a mix of results -- 2 of 8 (`appA-1`, `15-2`) came out correctly Japanese-presenting, but 4 of 8 (`appB-1`, `appB-2`, `appC-1`, `appC-2`) still showed non-Asian (Black-presenting) figures, and `appA-2` still rendered a real US flag despite the added instruction.
- Second, stronger fix: rewrote `style_lock.photo_style` to lead with an emphatic, explicit instruction naming both the required appearance (Japanese/East Asian, straight black/dark brown hair, East Asian facial features) and the specifically excluded groups (not Black, not South Asian, not Middle Eastern, not White/Western), plus an explicit flag prohibition ("absolutely NO flags of any kind... no stars-and-stripes"). Also rewrote the two government-scenario prompts (`appA-2`, `appB-2`) to remove vague "government/civic auditorium" framing entirely in favor of "plain walls, no podium seal, no emblem, no crest, no flag, no signage," and to fix an unrelated but real composition defect the user caught in the same review pass: the presenter was standing directly against the front row with no floor gap, and the "screen" behind her had an oddly narrow tall aspect ratio that didn't read as a presentation screen at all. Regenerating all 5 affected images (`appA-2`, `appB-1`, `appB-2`, `appC-1`, `appC-2`) with the strengthened prompt produced correct results across the board: verified Japanese/East Asian presenters and audiences, no flags, no emblems, comfortable presenter-audience spacing.
- User raised a usage-limit constraint mid-session (17% of weekly limit remaining, cannot wait days for reset) and asked for more efficient working: batch image-generation calls together rather than one-at-a-time, avoid redundant iterative review rounds, be decisive rather than asking clarifying questions when a reasonable default exists. Applied immediately: batched all remaining low/medium-risk diagram-type images (21 of the remaining 26) into a single script invocation rather than generating and reviewing one at a time.
- User also caught a memory-hygiene error: an assistant (Claude Code) had started writing session memory into its own tool-specific store (`~/.claude/projects/.../memory/`) instead of this repo's shared, LLM-agnostic memory files as mandated by `AGENTS.md`'s "File Creation And Storage (All Assistants)" section. Deleted the wrongly-placed files immediately and recorded the same content in the correct locations (`user-learning-mirror.md` issue entry, `project-learning.md` decision entry, this journal entry) instead. Noted for future sessions across all assistants: always re-read `AGENTS.md` in full (not just grep for a location) before deciding where session memory belongs, especially early in a session after context compaction/summarization, since a summarized context can silently drop the instruction to check it first.
- Batch of 21 diagram/process images completed in background; all reviewed in one pass afterward (checked representation, element counts vs. register descriptions, composition) -- no defects found, no regenerations needed, confirming the earlier prompt fixes held up across the full set.
- User asked whether all prompts were prepared, intending to generate the rest manually if the weekly usage limit was hit before finishing -- confirmed yes, all 36 register entries have complete, ready-to-use prompts in `image_register.json`, generatable via `scripts_local/generate_presentation_skills_images.py --ids ...`, with the caveat that 4 entries (`01-1-three-phases`, `04-3-delivery-icon-set`, and the 3 tree worked-examples) need extra composite/overlay steps beyond the plain batch script.
- User then received an OpenAI spend-alert email mid-session and asked not to waste further credits. Finished the remaining work economically: reviewed the 22 already-generated-but-unreviewed images using existing files only (no new API cost) -- all passed; generated the final `04-3-delivery-icon-set` via one more small API call (clean result, no defects); and produced the last 3 tree worked-examples (`05-2`, `appD-1`, `appD-2`) with **zero** additional API cost by writing a new generalized overlay script (`scripts_local/draw_logic_tree_worked_example.py`) that reuses the already-approved blank tree art and overlays worked-example text via PIL, the same pattern already proven for the core Logic Tree's labels. Caught and fixed one real bug in the first pass of that script: a fixed 320px side margin silently truncated the longest trunk phrase ("This app gives you your evenings back" rendered as "This app gives you"); fixed by measuring actual rendered text width per image and sizing the margin dynamically instead of guessing a fixed constant.
- User also asked to leave for 3 hours and said not to ask further questions, to keep working autonomously until usage or spend limits are hit. Completed all remaining review and generation work solo under that instruction; no defects remained by the end.
- **Result: all 36 Presentation Skills images are now generated and reviewed. Visual asset generation for this book is complete.** Next stage for this project is Stage 3 (style infrastructure / per-tier DOCX build) per `docs/presentation-skills-consolidation-plan.md`'s production checklist.

## 2026-07-07 - Presentation Skills Content Review: 3 More Defects Found And Fixed

- User asked for a full content read-through of the assembled manuscripts (Long.md end-to-end first as the superset, then Standard.md and Essentials.md) before moving on to front matter/Stage 3, given that the prior session's word-count audit had already caught one real defect (Unit 12's thin Long-tier text).
- Found and fixed a cosmetic issue: a doubled `---` separator between consecutive units/appendices in all 3 manuscripts (14 in Long.md, 12 in Standard.md, 7 in Essentials.md), left over from the appendix-reordering script's join logic. Fixed via a small script that collapses `---\n\n---` down to a single `---`; verified word counts were unaffected (whitespace-only change).
- Found a real cross-reference defect in Unit 5 (The Logic Tree): its build-your-own-tree activity told learners in all three tiers to consult "Appendix B" for two additional worked examples, but Appendix B is paired with Units 10 & 11 per the plan's Section 5a, not Unit 5 -- confirmed via unit-5.json's own `notes` field, which showed this was a deliberate-but-mistaken choice by Unit 5's drafting agent (Appendix B genuinely does contain a business/government pair, just not one owned by this unit). In Essentials, Appendix B doesn't exist at all (Units 10/11 aren't in that tier); in Standard/Long, Unit 5 precedes Unit 10 in reading order, so the reference pointed at content not yet reached. User confirmed the same defect exists in all three tiers, not just Essentials, since Unit 5 is present in all three and always precedes Unit 10.
- Rather than simply removing the reference, user asked for a proper fix: wrote a new appendix, "Logic Tree Worked Models" (`books/Presentation Skills/units/appendix-d.json`), correctly paired with Unit 5, containing two freshly written worked Logic Tree examples (business: a remote-work stipend pitch; government: a pedestrian-safety intersection upgrade) in the correct filled-in Roots/Trunk/Branches/Leaves/Fruit template format -- confirmed distinct from Appendix B's flowing-speech format and from every other model-speech scenario already in the book.
- User then caught a follow-on naming problem: the new appendix's correct reading-order position (right after Self-Introduction Models, since it's paired with Unit 5) sorts before the original "Appendix B" and "Appendix C," making sequential lettering misleading. Resolved by dropping appendix letters entirely across all learner-facing text (unit JSONs, all 3 manuscripts, tables of contents) -- appendices are now referred to by name only ("the Self-Introduction Models appendix," "the Organizational/Product Presentation Models appendix," etc.). Production `notes` fields (not learner-facing) retain old lettered references as historical documentation and were not rewritten.
- Updated `docs/presentation-skills-consolidation-plan.md`: Section 5a addendum documenting the new appendix and the naming-scheme change; Stage 2 checklist note recording both this session's fixes and the prior session's (appendix ordering, Unit 12 depth).
- Full read-through of Long.md, Standard.md, and Essentials.md otherwise found the content solid: consistent per-tier voice, correct cross-unit callbacks throughout (Unit 3->2, Unit 4->2, Unit 7->3, Unit 8->5&7, Unit 9->2, Unit 10->appendix, Unit 11->10, Unit 12->appendix, Unit 13->12, Unit 14->6, Unit 15->2-4), and appropriate tier abridgment (Standard genuinely tighter than Long, not just truncated).

## 2026-07-06 - Presentation Skills Stage 2 Content Drafting Complete

- Drafted all 15 units of "Presentation Skills" per the fully-approved consolidation plan, using a multi-agent approach: attempted via the Claude Code `Workflow` tool first, then fell back to plain sequential/parallel `Agent` calls after `Workflow` became unavailable mid-run (see `user-learning-mirror.md` issue `2026-07-06-WORKFLOW-01`). 5 of 19 originally-launched workflow agents had already completed and cached results in `subagents/workflows/wf_0fe68fab-a09/journal.jsonl` before the interruption; these were extracted and reused rather than redrafted, preserving the 3 per-tier voice guides and 2 already-finished units.
- Established a per-tier shared voice-guide pattern to keep prose consistent across independently-drafted units at the same tier: `books/Presentation Skills/canon/voice-E.md`, `voice-S.md`, `voice-L.md`, each pasted verbatim into every unit-drafting agent's prompt for that tier.
- All 15 units persisted as `books/Presentation Skills/units/unit-N.json`, each containing per-tier content (only the tiers that unit belongs to) plus `appendixModels` for the 3 units that own an appendix (Unit 2 -> Appendix A, Unit 10 -> Appendix B, Unit 12 -> Appendix C), all freshly written per Decision 9.
- Assembled the 3 manuscript files (`Essentials.md` 8 units, `Standard.md` 12 units, `Long.md` all 15 units) via an assembly agent, verified all cross-unit callbacks resolve (Unit 3->2, Unit 4->2, Unit 7->3, Unit 8->5&7, Unit 9->2, Unit 10->Appendix B, Unit 11->10, Unit 12->Appendix C, Unit 13->12, Unit 14->6, Unit 15->2-4) and shared terminology stays consistent (6 Keys, Logic Tree parts, "M. Chair/Chairperson").
- User caught two real defects post-assembly: (1) appendices were interleaved mid-book (after their owning unit) rather than collected at the end -- fixed via a reordering script across all 3 files, with tables of contents corrected to match; (2) a word-count audit requested by the user surfaced that Unit 12's Long-tier text (319 words) was thinner than its own Standard-tier text (486 words) and a fraction of sibling Long units (1,300-2,800 words) -- redrafted Unit 12's Long tier only (now 1,621 words) to match Long voice/depth and correctly set up Unit 13's handoff, leaving Standard tier and both Appendix C speeches untouched.
- Committed and pushed to `origin/main` (`afed89e`): all 15 unit JSONs, 3 canon voice guides, 3 assembled manuscripts, plus the `user-learning-mirror.md` Workflow-tool issue entry. This completes Stage 2 (content drafting) of the plan's Section 7 production checklist; Stage 3 onward (style infrastructure, per-tier DOCX build, validation, pedagogy review, PDF export, sign-off) remains open.

## 2026-07-03 - Presentation Skills Consolidation Planning

- Began planning consolidation of four presentation-skills books (`Speaking with PowerPoint`, `Making Speeches`, `Business Presentations Essentials for Businesspeople`, `Business Presentations Essentials for Government Officials`) into a single "Presentation Skills" book offered at Essentials/Standard/Long tiers, eliminating the businessperson/government-officials split at book level in favor of paired audience-specific models within shared units.
- Established a reusable, LLM-agnostic thematic-series consolidation methodology (source inventory -> parallel per-book content mapping via background agents -> cross-book synthesis -> explicit design-decision sign-off -> recorded plan), intended for reuse on the upcoming Meeting Skills book series. Documented at `docs/thematic-series-consolidation-methodology.md`.
- Reused existing `docx-to-markdown` `out/.md/` unit conversions for all four source books rather than reconverting; ran four parallel background agents (one per book) to produce structured content maps (frameworks, language content, model scenarios, audience-specificity, dated-content flags, tier judgment).
- Resolved decisions: best-of framework synthesis across sources (not single-book-as-base or variant-preservation); eliminate business/government split at book level, folding audience variants into paired model speeches within shared units; build a new Virtual & Hybrid Delivery module as in-scope new content, since none of the four source books address virtual/hybrid presenting at all.
- Open decisions (recorded in `docs/presentation-skills-consolidation-plan.md`): per-unit tier-inclusion granularity (some units essentials/long-exclusive, most depth-scaled across all tiers, reference material accreting across tiers) needs further review; manuscript structure (single tagged source vs. separate per-tier manuscripts); "Keys" framework naming synthesis; whether to keep or generalize the Japanese-L1-learner-specific language framing; whether dated model-speech scenarios (Ventura car pitch, Cool Biz policy speech) get freshly written or refreshed in place.
- Full proposed unit list and tier mapping recorded in `docs/presentation-skills-consolidation-plan.md`.
- Revised plan per user feedback: online/hybrid delivery is now a cross-cutting consideration woven through nearly every unit (not a single bolt-on module), with a narrower dedicated unit retained for platform-specific mechanics; model speeches (previously standalone units) moved into a new Appendices section pairing business/government models per skill, directly serving the audience-split retirement goal from Decision 2.
- User caught a real error: the unit-list table's per-unit E/S/L marks did not match the illustrative summary counts below it. Reworked the table so Standard and Long are differentiated by depth (4 units abridged at Standard, full at Long) rather than Standard being a near-duplicate of Long, and corrected the counts to match the table exactly (Essentials 9/15, Standard 14/15, Long 15/15). Left open, within Decision 5, whether Standard also needs a content cut rather than just reduced depth.
- User judged the depth-only differentiation insufficient and set hard numeric tier caps: Essentials <= 8 taught units, Standard <= 12, Long = all. Retired the "abridged counts as present" convention entirely and rebuilt the unit table to enforce exclusion by count. Essentials rebuilt directly from the existing BPE Essentials books' actual unit set (Structure, Delivery, Flag Expressions, Logic Tree, Chairing, capstone) rather than a fresh guess, plus Slide Design since visual aids are now baseline expectation. Cut the standalone Online & Hybrid Delivery Mechanics unit entirely, folding its content into Delivery Skills, since Decision 3 already committed to weaving online considerations through every unit and a dedicated mechanics unit on top of that was redundant. Expressions Reference Appendix moved outside the unit-count cap. Renumbered all 13 taught units and corrected every cross-reference across the plan (decisions, appendix table, modernization flags). Final counts: Essentials 8/13, Standard 12/13, Long 13/13.
- User identified a significant scope gap: the source books are instructor/reference guides, not learner-facing textbooks with developmental activities built in. Designed a learning activity for every one of the 13 taught units, tier-scaled alongside content tiering rather than deferred to drafting. 7 of 13 activities extend a genuine source-book precedent (self-introduction critique exercise, Logic Tree build, annotated pronunciation practice, etc.); 6 of 13 are newly designed because no source activity existed for that content (orientation self-assessment, flag-expression drill, slide redesign critique, evidence-chain construction, slide/handout rehearsal, team-presentation group project). Added new resolved Decision 10 recording this addition; fixed section ordering so Appendices (5a) precede Activities (5b) since several activities reference appendix models.
- User split former Units 10-11 ("Description, Logic & Persuasion" and "Critical Thinking: Analyze & Propose / Argue & Defend") into four units -- Logic, Analyze (problem-solving/reporting focus), Persuasion, and Propose (recommended actions, folding in Argue & Defend) -- to give the Long course genuinely exclusive content instead of being "Standard plus one unit." Standard's unit count is unaffected: it keeps exactly the 2 units (Logic, Analyze) it always had from this cluster; Persuasion and Propose are new Long-exclusive units. User then caught an ordering error: the initial split grouped units by source book (Logic, Analyze, then Persuasion, Propose) rather than pairing each skill with its advanced extension. Corrected to topic-paired order: Logic (10) -> Persuasion (11, Long-exclusive) -> Analyze (12) -> Propose (13, Long-exclusive), with old Units 12-13 renumbered to 14-15. This makes Standard non-contiguous across Units 9-14 (present at 10, 12, 14; absent at 11, 13) -- a deliberate tradeoff for pedagogical ordering. Corrected every cross-reference: Appendix B now pairs with Units 10 & 11, Appendix C with Units 12 & 13; Section 5b activities renumbered and reworded so Units 11 and 13 explicitly build on Units 10 and 12's work rather than starting fresh. Final counts: Essentials 8/15, Standard 12/15, Long 15/15 -- directly resolves the remaining half of Decision 5 (Long now has 3 genuinely exclusive units instead of 1).
- Added Section 7 to the plan: an 8-stage production checklist (design sign-off, content drafting, style infrastructure, per-tier build, validation, content/pedagogy review, PDF export, sign-off/delivery) so production quality can be tracked stage by stage. Grounded in this repo's actual tooling (`markdown-to-docx`, `validate_docx_against_reference.py`, `audit_docx_styles.py`, `docx-to-pdf`) and cross-referenced against the plan's own section/decision numbers rather than generic textbook-production advice. Explicitly flags that this title needs a reference DOCX built from scratch, unlike the Administrative Writing books which had one to inherit. Mirrored into the HTML artifact as interactive checkboxes grouped by stage. Caught and fixed a self-introduced duplication bug during editing (the checklist block was accidentally duplicated at the end of the markdown file); verified clean via heading-structure grep before considering the edit complete.
- Resolved 4 of the 5 remaining open plan decisions. Decision 6 (manuscript structure): three separate manuscripts, one each for Essentials/Standard/Long, not a single tagged source -- content fixes now propagate to up to three files. Decision 7 (Keys framework naming): user explicitly rejected treating this as an A-or-B pick, asking whether the two source frameworks actually overlap in content. Read both source units word-for-word (`01-1-keys-to-successful-presentations.md` in Speaking with PowerPoint, `02-2-keys-to-successful-presentations.md` in Making Speeches) instead of assuming -- found they describe the same four ideas at different granularity (Making Speeches merges Purpose+Content into one item, Speaking with PowerPoint splits them into two) plus exactly one genuinely additional item (PowerPoint/Visual Aids, present only in Speaking with PowerPoint). A combined "10 Keys" would double-count the same ideas under different labels, so it was not adopted. Resolved: 6 keys at Speaking with PowerPoint's granularity (Purpose, Content, Structure, Language, Delivery, Visual Aids), canonical name "Keys to Successful Presentations" with the number dropped from the brand name. Decision 8 (learner-audience framing): resolved to generalize away from Japanese-L1-specific framing for a broader non-native-English audience. Decision 9 (model speech content): resolved that all appendix model speeches will be freshly written, not refreshed versions of the existing Ventura/Cool Biz speeches.
- User caught a mischaracterization in the Decision 5 write-up from the entry above: it conflated two distinct questions under one heading -- unit-*inclusion* (which units belong to which tier) and Section 5b's activity *tier-scaling* (how each activity's depth changes between tiers). The user's earlier "largely agree, pending drafts" answer was specifically about 5b's activity scaling, not unit-inclusion -- and unit-inclusion was never actually open, since the Section 5 table itself is the decision record for that question, requiring no separate sign-off. Corrected Decision 5's text to state plainly that unit-inclusion is resolved via the table, and narrowed the still-open item to 5b's tier-scaling specifics only, which await Stage 2 drafts for final review but do not block drafting from starting. Updated the Section 7 Stage 1 checklist and all status counts (plan header, HTML masthead, footer) to reflect this precisely: 10 of 10 decisions resolved, with one narrow sub-item pending drafted review.
- User approved Section 5b's activity tier-scaling design as written at the planning stage, without waiting for drafted activities -- closing the one remaining open sub-item under Decision 5. All 10 design decisions in the plan are now fully resolved. Noted in the plan that this is approval of design intent, not a guarantee drafted execution will match it -- Stage 6 (Content & pedagogy review) remains the checkpoint for verifying drafted activities actually deliver the described scaling. Updated the plan's top-of-file status line ("draft plan, design decisions not yet fully resolved" -> "all 10 design decisions resolved, ready for Stage 2 content drafting"), the Section 7 Stage 1 checklist item, and all status badges in the HTML artifact (masthead, Decision 05 card, footer). Plan is now ready to move into Stage 2 (content drafting) per its own production checklist.

## 2026-06-01

- Updated `textmaker.cmd` so Windows dependency discovery is environment-aware rather than tied to one machine. The wrapper now probes common active-machine install roots for Pandoc, Poppler, and Tesseract before launch, while keeping the existing UNC-safe `pushd` behavior.

## 2026-05-19 (session 15 — module introductions, example-bad restructuring, postprocessor fix)

### Work completed

**INT book (`aw-int-all_0519.md`)**
- Added per-unit description bullet list to all 6 `## Module Guide` introductions — new section inserted between opening paragraph and "By the end of this module" outcomes list.
- Detected 26 edit/rewrite/revise/notice divs containing untagged weak-example labels (`**Original:**`, `**Weak draft**`, `**Weak version**`, `**Original Email:**`); extracted all 26 as preceding `:::example-bad` divs using automated script (`tag_example_bad_blocks.py`).
- Manually fixed 4 cases where instruction text was incorrectly included in the example-bad block (revise, notice, and 2 rewrite cases).
- Div balance: 532 opens / 532 closes (Match: True, 0 unclosed). PH markers: 255.
- Final example-bad div count: 40 (was 14 before this session).

**ADV book (`aw-adv-all_0516.md`)**
- Converted prose unit-description paragraphs in Modules 2–6 to bullet lists (one bullet per unit), matching the reference format already established in Module 1.

**Postprocessor (`apply_example_block_styles()` in `postprocess_docx.py`)**
- Added `_seen_italic` tracking flag: if no italic content has been seen in the current example div, non-italic Body Text paragraphs are styled (INT-style); if italic content has been seen, the first non-italic paragraph acts as a task instruction boundary (ADV-style). Fixes the INT book example styling that was only producing 14 styled paragraphs (now 179).

### Build results

- INT: 2263 list styles, 179 example block paragraphs (was 14), 40 example-bad divs, 255 placeholders, 465 icon labels. Clean build.
- ADV: 1698 list styles, 234 example block paragraphs (was 148), clean build.
- Both PDFs exported and opened.
- Both repos committed and pushed.

## 2026-03-24

- Startup bootstrap executed for the `textmaker` workspace.
- Confirmed the workspace is a Git repository rooted at `<repo-root>`.
- Checked remote sync state non-destructively with `git fetch --prune origin`; local `main` and `origin/main` were even at the time of bootstrap.
- Created missing repo-level bootstrap files: `AGENTS.md`, `user-learning-mirror.md`, `project-learning.md`, `project-journal.md`, and `instruction-read-log.csv`.
- Read `README.md` and promoted its durable content into `project-learning.md`.
- Established repo project memory as the main source for recording project developments, durable decisions, constraints, and roadmap changes going forward.

## 2026-04-14

- Ran `textmaker.cmd markdown-to-docx` against the AME course summary markdown and produced `AME_course_summary_report.docm` in the client report folder; command required an in-session PATH prepend for local Pandoc (`C:\Users\d-dobson\AppData\Local\Pandoc`).

## 2026-05-09

- Updated `textmaker.cmd` to prepend the common local Pandoc install directory automatically when present.
- Updated `scripts/cli.py` so `markdown-to-docx` resolves relative input, reference, and output paths more robustly when launched through `cmd.exe` from a UNC-backed workspace.
- Verified the UNC case by running `..\..\textmaker\textmaker.cmd markdown-to-docx --input .\md\final\modules\aw-adv_mod1_n10.md --reference .\aw-adv-styleref.docx --output .\md\final\modules\aw-adv_mod1_from_relative.docx` from `book_administrative-writing\adv`, which completed successfully.
- Updated `scripts/cli.py` to normalize markdown before Pandoc by inserting blank lines before lists that directly follow prose, preventing list collapse in generated DOCX output.
- Added `--ignore-horizontal-rules` to drop standalone markdown separator lines such as `---` before conversion, avoiding unwanted page breaks when the pagebreak Lua filter is active.
- Added a semantic DOCX postprocessing layer driven by the reference DOCX. `markdown-to-docx` now applies custom styles and cloned prototype callout tables consistently for repeating textbook patterns such as `Why this works`, `Before you write`, teaching-point notes, model good/bad text blocks, homework word-count prompts, and post-list follow-on prompts.
- Verified the semantic pass on Module 1 by generating a temporary DOCX and confirming inserted `Why?` / `Check` / `Learn` / `Note` tables plus applied `Block Text Good`, `Block Text Bad`, `Homework Words`, and `After List` styles.
- Replaced the cloned-prototype-table approach with Word COM Quick Part insertion for unit title blocks only; the converter now launches a dedicated `DispatchEx` Word instance, inserts the real building block from `Normal.dotm`, and avoids touching unrelated `WINWORD.exe` processes.
- Reworked the Administrative Writing semantic formatting so only unit title tables remain as Quick Parts; `Why this works`, `Before you write`, `Teaching point`, `Note`, and related cues now stay paragraph-based to reduce visual dominance.
- Repaired the Module 1 demoted markdown hierarchy by keeping framework sections at `###`, activities at `####`, turning model labels into plain content labels, and converting the “Clarity Patterns” sequence away from a heading stack.
- Expanded `After List` styling so prompt-style lines such as `Practice ...`, `Reflect:`, and `Example:` can inherit the style after short commentary blocks, not only after literal list paragraphs.
- Removed all `*Tok` styles from `book_administrative-writing\adv\aw-adv-styleref.docx`, then repaired the resulting `word/styles.xml` corruption after an initial rewrite dropped the required compatibility namespace declarations from the root element.
- Regenerated the final Module 1 production candidate as `book_administrative-writing\adv\md\final\modules\aw-adv_mod1_n10_demoted_fixed.docx` and verified it contains three unit title Quick Part tables (`U1`, `U2`, `U3`) plus the broadened `After List` styling.

## 2026-05-12

- Added a repeatable Markdown style-audit utility for Advanced Administrative Writing source cleanup.
- Tightened `markdown-to-docx` so postprocess failures surface instead of being silently swallowed.
- Updated DOCX postprocessing to use only reference styles, remove `Strong`/direct bold output, color emoji labels from matching label styles, apply 6pt semantic label spacing, strip activity-code suffixes from headings, and broaden post-list spacing.
- Added a functional Markdown/DOCX paragraph audit report for Advanced Administrative Writing that groups by structural role rather than literal CSV text.
- Regenerated `aw-adv-all_0510.docx` through `textmaker.cmd markdown-to-docx` with `aw-adv-styleref.docx` as Pandoc `--reference-doc` and the Advanced Writing Lua Div filter enabled; validation confirmed no missing reference styles, no `Strong` run style, no direct bold, no remaining heading activity codes, and emoji runs without direct bold/italic markers.
- Regenerated `aw-adv-all_0510.pdf` from the validated DOCX with LibreOffice.
- Updated the Advanced Writing cleanup pipeline so DOCX postprocess purges generated style usage and style definitions not present in the reference DOCX; replaced `annotation` Divs in the working Markdown with `learn-note` and removed the `annotation` Lua mapping. No conversion was run for this change batch.

## 2026-05-13

- Regenerated the Advanced Administrative Writing DOCX through `textmaker.cmd markdown-to-docx --input ... --reference ... --lua-filter ...`, with `aw-adv-styleref.docx` passed through to Pandoc as `--reference-doc`.
- Added a postprocess cleanup for alphabetic option lists: `List Number 3` is applied to A/B/C option items and literal source markers are removed afterward to prevent doubled labels in PDF output.
- Validated the generated DOCX against the reference style set: no missing used styles, no extra style definitions, no `Strong` or `Emphasis` run styles, no direct bold tags, no activity-code suffix hits, and no literal alphabetic markers inside `List Number 3` paragraphs.
- Exported the validated DOCX to PDF with LibreOffice.
- Corrected the Advanced conversion command to use `--no-pagebreak-filter`; this keeps Textmaker from applying `pagebreak.lua` to standalone `---` separators and restores the PDF to the expected 186-page length.
- Updated semantic Div title postprocessing so title lines retain their semantic paragraph styles, with 4pt space after on the label paragraph and 0pt space before on the moved content paragraph.
- Updated unit-title table postprocessing so the original unit heading text is cleared after the reference table is inserted, preventing visible duplicate unit headings.
- Added a nested-list semantic Div pass so list paragraphs inside semantic Div blocks keep their list style while receiving the Div's block-level paragraph formatting. Regenerated the Advanced DOCX/PDF and validated that the nested list items have both list styling and Div border formatting.
- Simplified `scripts/postprocess_docx.py` by rolling back two recent postprocess behaviors:
  - removed the run-level cleanup pass that stripped `Strong`/`Emphasis` styles and rewrote bold handling through heavier font substitution
  - removed the nested-list semantic Div formatting pass that copied Div block formatting directly onto list paragraphs
- Kept the broader semantic paragraph formatting, unit-title handling, heading cleanup, and fallback-style cleanup intact.
- Updated the Learn semantic-style model to support a reduced reference-style set:
  - keep the emoji insertion and per-label Learn label styles
  - stop relying on multiple `Learn XXX` paragraph styles surviving postprocess
  - convert Learn semantic paragraphs to `Learn Base` during postprocess

## 2026-05-15

- Implemented the full style-safe DOCX pipeline for the Administrative Writing advanced book, based on a ChatGPT-authored plan at `book_administrative-writing/adv/edits & guides/style edits/step2-stylereference/Instructions_from_ChatGPT_0515.md`. GitHub CoPilot began the work but lost context mid-task; Claude Code completed all 10 tasks.
- Added `scripts/style_bridge.lua` — generic Pandoc Lua filter that reads `style_map` from YAML front matter and maps fenced Div classes to Word `custom-style` attributes. Replaces the hardcoded `aw_textbook_div_styles.lua`.
- Added `scripts/audit_docx_styles.py` — read-only DOCX style inspector with linked-style color-mismatch validation.
- Added `scripts/manage_docx_styles.py` — explicit manual-only tool for updating reference DOCX styles from a YAML spec. Updates all three color locations (`w:color`, `w14:srgbClr`, linked char style `w:color`) atomically. Has `--in-place` safety (auto-creates `.bak`) and post-write validation. **Must not be added to the automated build pipeline.**
- Added `scripts/validate_docx_against_reference.py` — post-build validation script with 5 checks (used para styles in reference, used char styles in reference, no extra style definitions, YAML style_map styles in reference, linked styles valid and reciprocal).
- Refactored `scripts/postprocess_docx.py`: default changed from `semantic_formatting=True` to `apply_semantic_labels=False`. Semantic label rendering now requires `--apply-semantic-labels`. Kept `--no-semantic-formatting` as a deprecated no-op. Updated docstring to remove misleading "semantic course formatting is applied consistently" language.
- Fixed long-standing bug in `scripts/cli.py`: `insert_section_after_toc()` call was indented inside the `except ImportError` block and never executed when running as a package. Added `--apply-semantic-labels` to cli.py parser.
- Added `tests/test_docx_styles.py` — 13 tests covering RGB→hex conversion, all three color-location updates, color-mismatch detection, `Div Label Base` next-style fix, and style audit failure on missing expected styles. All 13 pass.
- Fixed `scripts/style_bridge.lua`: `PANDOC_STATE.meta` does not exist in current Pandoc versions. Rewrote as a two-pass filter (array of filter tables) so `Meta` populates `style_map`/flags in pass 1 before `Div` and `HorizontalRule` run in pass 2. Single-pass filters process `Div` before `Meta` (bottom-up traversal), so the map was always empty.
- Ran first full production conversion of `book_administrative-writing/adv/md/final/aw-adv-all_0514.md` → `adv/docx/aw-adv-all_0514.docx` using direct Pandoc (not textmaker CLI) with `style_bridge.lua` and `aw-adv-styleref.docx`. Postprocess: 1680 list paragraphs styled, 521 fallback styles replaced, 1729 non-reference style instances cleaned, 29 page breaks applied. Validation: exit 0, all styles consistent with reference DOCX.
## 2026-05-16 (session 1 — bootstrap and pipeline setup)

- Set up Claude Code (claude-sonnet-4-6) to use the shared Codex memory bootstrap system.
- Created `C:\Users\daved\.claude\CLAUDE.md` (global) — imports `%USERPROFILE%\.codex\AGENTS.md` and `%USERPROFILE%\.codex\memories\user-learning.md` at every session start via `@filepath` directives.
- Created `c:\Dev\Code\textmaker\CLAUDE.md` (project) — imports `AGENTS.md`, `user-learning-mirror.md`, `project-learning.md`, and `project-journal.md` via relative `@filepath` directives.
- Decision: Claude Code will write durable decisions and events to the shared repo-level memory files rather than the Claude-specific `~/.claude/projects/` memory system, so memory remains shared with Codex and any other AI assistant.

## 2026-05-16 (session 2 — div cleanup and reclassification)

### Work completed

- Fixed 52 missing blank lines between consecutive `:::` close / `:::` open fences (Pandoc parse risk)
- Removed BOM character (U+FEFF) that was on its own line after the YAML front matter
- Stripped all `rubric-assessment` and `course-meta` div wrappers (8 total) — no distinctive rendering, content preserved as plain prose
- Removed 4 stale style_map entries: `guidance-step`, `annotation`, `example`, `placeholder`
- Removed `reference-support` div at Unit 9 D (template content absorbed into surrounding `activity-draft`)
- Removed `reference-support` div at line ~7267 (continuation of model report, absorbed as plain prose)
- Restructured Unit 23 B section (lines 8036–8089): removed empty `activity-analysis` shell, removed `reference-support` scenario wrapper, replaced `model-bad`/`model-good` with neutral `model` divs labelled "Response A" / "Response B"
- Completed initial div reclassification: all 595 div open fences renamed from 18 old classes to 9 new classes per the reclassification guide
- Updated YAML `style_map` to the 9 new classes with `Div Label *` Word style targets

## 2026-05-16 (session 3 — content-based div reclassification pass)

### Completed this session

- Generated a full 595-row content-based reclassification review (`div_reclassification_full_0516.md`) with an explicit one-sentence reason for every div classification.
- Reviewed all 595 rows independently (not label-swapping — reading actual content against the 9-class guide).
- Applied 74 reclassifications to `aw-adv-all_0516.md` via Python script; 0 skipped.
- Verified div balance: 595 open, 595 close, 0 unclosed, 0 orphan closes.
- Verified total count: 595 divs (unchanged — no divs added or removed).

### Key reclassification decisions and reasons

- **edit → rewrite (18 cases):** Tasks labelled `edit` whose instruction was to transform/rewrite given text, not to find errors or apply checklists. The `edit` class is reserved for error-finding, peer review, and self-editing checklists.
- **language → rewrite (8 cases):** Divs where the learner performs a sentence-transformation, completion, or expansion task on given text — not a reference list of language forms.
- **notice → write (9 cases):** Prediction, data-interpretation, and reflection tasks where the learner produces original text from given scenario information.
- **language → learn (6 cases):** Teaching explanation divs (notes on but/however, thematic progression panels, section wrappers) — no task, pure explanation, not a reference list.
- **language → structure (3 cases):** Phrase-bank sorting tasks where the learner classifies given phrases under headings — no new text produced.
- **notice → learn (4 cases):** Outer wrapper divs containing explanatory content or reference panels — no observation task.
- **rewrite → structure (4 cases):** Tasks where the learner orders/sequences given jumbled sentences into a paragraph, not rewrites prose.
- **notice → structure (2 cases):** Sorting/sequencing tasks on given items.
- **rewrite → learn (2 cases):** Outer wrapper divs containing teaching explanation with no rewrite task in the wrapper itself.
- **write → structure (3 cases):** Template-guided tasks where the learner fills a given structural framework — not original production from scratch.
- **edit → revise (4 cases):** Revision chains where learner improves their OWN previously drafted text from an earlier unit.
- **edit → notice (2 cases):** Track-change simulation tasks where learner evaluates proposed edits and decides accept/reject.
- **write → rewrite (1 case):** Two-audience adaptation task with given source text to transform.
- **write → revise (1 case):** Self-revision of own earlier writing using self-diagnosis questions.

### Final div class distribution (session 3 result)

| Class | Before | After | Delta | Word style |
| --- | --- | --- | --- | --- |
| `example` | 127 | 127 | 0 | Div Label Example |
| `learn` | 114 | 126 | +12 | Div Label Learn |
| `write` | 89 | 95 | +6 | Div Label Write |
| `rewrite` | 57 | 83 | +26 | Div Label Rewrite |
| `notice` | 79 | 65 | −14 | Div Label Notice |
| `edit` | 75 | 48 | −27 | Div Label Edit |
| `language` | 54 | 34 | −20 | Div Label Language |
| `structure` | 0 | 13 | +13 | Div Label Structure |
| `revise` | 0 | 4 | +4 | Div Label Revise |
| **Total** | **595** | **595** | **0** | |

### Remaining work (pending)

All items completed in session 4 and session 5 — see below.

## 2026-05-17 (session 4 — overnight fix batch)

### Reference DOCX style repairs

- Renamed all 22 `Div *` styles to `Div Label *` in `aw-adv-styleref.docx` via direct XML edit (`rename_div_styles.py`). Required for `style_bridge.lua` `is_div_label_style()` prefix check (`"Div Label "`, 10 chars).
- Added `Div Label Example Good` / `Div Label Example Good Char` (color `2C9167`) and `Div Label Example Bad` / `Div Label Example Bad Char` (color `E36C0A`) to reference DOCX.
- Updated `Div Label Example` color from `9CCF78` to `4F81BD` (steel blue, matching AW Example body style border).
- Renamed `Body Text1` → `Body Text` (styleId `BodyText`) in reference DOCX; postprocessor and Word both require the canonical name.
- Updated `aw-div-label-styles.yaml` to match all 9 new `Div Label *` names and add `example-good`/`example-bad` entries.

### Source markdown fixes (`aw-adv-all_0516.md`)

- Replaced 44 `model` → `example` occurrences, 23 heading renames (`### B. Model Text` → `### B. Example Text`), 59 div title renames (`Model Text` → `Example Text`).
- Fixed arrow paragraph: instructional note ("The arrow (→)…") moved outside `learn` div and given heading "Clarity Patterns".
- Fixed "Tone by Audience" section: added title to Internal/Interagency/International wrapper div.
- Wrapped Unit 4 Useful Phrases table in a `language` div.
- Renamed 28 "Extension Task" div titles → "Homework Task".
- Updated YAML `style_map` to 9 new `Div Label *` style names.

### Postprocessor additions (`postprocess_docx.py`)

- Added `apply_checklist_style()`: applies `Checklist` style to bullet items inside `Self-Editing Checklist` edit divs.
- Added `apply_example_block_styles()`: applies `AW Example Good` / `AW Example Bad` / `AW Example` body styles after matching Div Label paragraphs.
- Added `apply_spacing_after_lists()`: adds 120-twip space-after to prose paragraphs that follow list paragraphs (replaces deleted `After List` style).
- Added `apply_table_styles()`: applies `AW Standard Table` style to all unstyled tables.
- Moved `replace_unit_headings_with_title_tables()` outside the `apply_semantic_labels` gate — now always runs when reference_doc is available.
- Fixed duplicate `apply_semantic_div_labels` call (was called twice in the updated flow; second call removed).

### Build result (2026-05-17)

- Pandoc: clean, no warnings.
- Postprocess: 1666 list styles, 19 alpha markers stripped, 10 checklist items, 85 example block paragraphs, 179 post-list spacing, 41 table styles, 241 body text, 529 Pandoc fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings restored.
- Validation: exit 0, all styles consistent with reference DOCX.
- PDF: exported via LibreOffice soffice, 3.3 MB.

## 2026-05-17 (session 5 — checklist consistency and example-good/bad reclassification)

### Checklist consistency

- Converted all 151 plain `- ` (dash-space) bullet items inside edit divs to `- [ ]` for source consistency across all edit div types.
- Discovered that Pandoc with `--reference-doc` renders `- [ ]` as `List Bullet 2` (not `Compact` + checkbox glyph) — the checkbox is stripped when a reference DOCX defines the list style.
- Fixed `apply_checklist_style()`: now matches `List Bullet 2` inside any `DivLabelEdit` div (not just "Self-Editing Checklist" divs). 145 items converted in this build.
- Fixed `_apply_style_if_available()`: was calling `_require_style` (hard-fail on missing style). Changed to `_get_style_by_name_or_id` so legacy style references in `apply_semantic_styles()` (Model Bad, Homework Target, After List) degrade gracefully instead of crashing.

### Reference DOCX Body Text name regression

- Discovered `Body Text1`/`BodyText1` had regressed (the w14 strip script from session 4 serialized an older XML state). Fixed by direct XML patch — 17 cross-references updated. Style is now `Body Text` / `BodyText`.

### Example div reclassification

- Audited all 127 `example` divs by their title lines. Pattern confirmed 100%:
  - "Original Text" titles (23) → `example-bad`
  - "Revised Text" / "Worked Example" titles (43 total) → `example-good`
  - "Example Text" and others (61) → remain neutral `example`
- Added `example-good` and `example-bad` to YAML `style_map` targeting `Div Label Example Good` and `Div Label Example Bad`.
- Applied `apply_example_block_styles()` in postprocessor — 85 body paragraphs styled as `AW Example Good` / `AW Example Bad` / `AW Example`.

### Build result (session 5)

- Pandoc: clean, no warnings.
- Postprocess: 1666 list styles, 19 alpha markers, 145 checklist items, 85 example block paragraphs, 179 post-list spacing, 41 table styles, 267 div labels, 241 body text, 529 Pandoc fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings.
- Validation: exit 0.
- PDF: 3.3 MB. Both repos committed and pushed.

## 2026-05-18 (session 7 — icon table layout, caps fix, section break fix, div structure audit)

### Context and starting state

Continuing from session 6. The div label icon table layout (2-column borderless table with icon left, label text right) had been partially implemented but not yet verified against a clean build. Several issues were outstanding from the previous session: all-caps not rendering on div label char styles, page 1 rendering as Letter size with a spurious section break after the H1, and a file lock preventing the final rebuild.

### Reference DOCX patch: all-caps on DivLabel char styles

- All 12 `DivLabel*Char` styles in `aw-adv-styleref.docx` had bare `<w:caps/>` (no `w:val` attribute). Per OOXML spec, toggle properties in character styles require explicit `w:val="1"` to be honoured; bare elements are treated as "not set".
- Patched all 12 char styles to `<w:caps w:val="1"/>` using `C:\Temp\fix_caps_val.py`. Backup saved as `aw-adv-styleref.bak_caps` (moved to `adv/md/bak/` after session).
- Note: underline worked because `<w:u>` requires `w:val="single"` by spec and was already present; caps was the only property affected.
- Confirmed caps rendering in PDF output after patch.

### Postprocessor fixes (`postprocess_docx.py`)

**Section break / page size fixes:**

- `_insert_section_break_before_paragraph()`: added copy of `w:pgSz` and `w:pgMar` from document-level `sectPr` into every inserted `sectPr`, so section breaks inherit correct paper size (A4) instead of defaulting to Word's application default (US Letter).
- `insert_section_breaks_before_h1()` call site: changed `skip_first=has_toc` to `skip_first=True` so the first H1 (the cover title) is always skipped. Previously, when `has_toc=False`, the first H1 got a section break attached to the preceding YAML front-matter paragraph, effectively pushing the H1 off page 1.
- Confirmed via PDF MediaBox inspection that all pages are A4 (210×297mm) after fixes.

**Div label icon table layout (single-pass rewrite):**

- Rewrote `apply_semantic_div_labels()` as a single-pass function: builds the 2-column borderless table and inserts the icon in the same step, replacing each `DivLabel*` paragraph with a `<w:tbl>` in-place.
- Table config: `tblStyle=TableGrid`, `tblW type=auto` (autofit), explicit `tblBorders` with all sides `none`/`sz=0` to suppress visible borders while preserving gridlines toggle. `TableNormal` was tried but rejected because it has no border definition and the gridlines toggle couldn't be controlled.
- Left cell uses `DivTag` paragraph style (user-created, based on `Div Label Base`) so spacing inherits from the style rather than being hardcoded.
- Icon height changed to 190500 EMU (15pt) for inline rendering; `distR=114300` EMU (9pt) gap to label text.
- Example divs (neutral/good/bad) excluded from icon table — they use a different visual treatment.
- Fixed `AttributeError: 'CT_Body' object has no attribute 'part'` by using `Paragraph(child, doc._body)` instead of `Paragraph(child, body)`.

**`_apply_next_page_section_to_paragraph()` fix:**

- Added copy of `w:pgSz` and `w:pgMar` from document-level `sectPr` (same fix as `_insert_section_break_before_paragraph`).

### Working folder cleanup

- Moved `aw-adv-styleref.bak_caps` to `adv/md/bak/`.
- Removed stale `.tmp` file.
- Working folder now contains only: `aw-adv-all_0516.md`, `aw-adv-styleref.docx`, `aw-adv-all_0518.docx`, `aw-adv-all_0518.pdf`, `div-tags-icons-2_assets/`.

### Source markdown fixes (`aw-adv-all_0516.md`)

**Div spacing fixes (Pandoc compatibility):**

- Fixed 7 missing blank lines before `:::` open fences: all were bold `**Input N / Source N**` label lines immediately followed by `:::` with no blank line. Pandoc requires a blank line before a fenced div when preceded by non-empty content.
- Fixed 1 missing blank line between `:::` open fence and an immediately-following numbered list (`edit` div at L7317).
- Fixed 1 spurious extra `:::` close fence (triple `:::` at lines 2997–2999 reduced to double).
- Fixed unclosed `notice` div at L2951: inner `example-bad`/`example-good` divs were terminating the outer `notice` early; added explicit `:::` close before the sibling `learn "Why This Works"` block.

**Nested div audit and cleanup:**

- Audited all 244 nested div instances across the file. Two categories identified:
  - **Thin nested divs** (title-only, no body): 16 total, all nested. 11 removed as pure sub-labels adding no student learning value: `learn "Functions"` (×2), `language "Learn — Sentences"`, `language "Learn — Useful Language"` (×3), `language "Learn — Patterns"`, `learn "Statements"`, `learn "Annotations"`, `learn "Discuss"`, `learn "Revision Checklist"`.
  - **Kept** (meaningful labels): `learn "Version A"`, `learn "Version B"`, `learn "Original"`, `learn "Proposed Changes"`, `learn "Scenario"` — these label distinct content sections within the outer div.
- Remaining nested divs (233) are structural patterns where sub-divs are genuinely separate content blocks (e.g. `example-bad`/`example-good`/`learn "Why This Works"` sequences inside `notice` wrappers). These are known to cause early termination of the outer div in Pandoc; full resolution is pending — see decisions below.

**Table cell `<br>` tag fixes:**

- Replaced malformed `<br*` and `<br>` tags in pipe table cells with ` / ` separator. Pandoc's `markdown+fancy_lists` format does not process raw HTML in table cells without the `+raw_html` extension, so these were rendering as literal text.
- Affected: "Useful Phrases" language table (L1102–1106) and "Clarity Patterns" table (L196–198).

### Build results (session 7 final)

- Pandoc: clean, no warnings.
- Postprocess: 1678 list styles, 21 alpha markers, 145 checklist items, 92 example block paragraphs, 180 post-list spacing, 39 table styles, 458 icon tables + 61 emoji labels, 1113 div label updates, 243 body text, 513 fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings.
- PDF: 201 pages, all A4 (210×297mm confirmed via MediaBox). 3.9 MB.

### Outstanding issues

- **All-caps on div labels**: Caps patch applied to reference DOCX and confirmed in PDF. LibreOffice may render caps differently from Word — to be verified in Word.
- **Nested divs**: 233 remaining nested div instances. Most are `example-bad`/`example-good`/`learn` blocks inside `notice` wrappers — a deep structural issue requiring content-level decisions about which blocks are genuinely inside the outer activity vs. siblings. Not addressed this session.
- **Page 1 H1 visibility**: H1 "Administrative Writing, Advanced" is present in the DOCX body (confirmed via XML) but uses a white-text style in the reference DOCX (designed for use inside colored module title tables). The cover page layout is a placeholder ("Textbook description goes here") — not a pipeline issue.

## 2026-05-17 (session 6 — icon colors, alignment, and pipeline fixes)

### Reference DOCX color updates

- Updated `w:color/@w:val` on all 8 non-Example Div Label paragraph styles and their linked character styles to match the dominant fill color of each tag icon PNG:
  - Learn=`541F69`, Language=`722566`, Structure=`A72D61`, Notice=`DB4351`
  - Write=`CA7032`, Rewrite=`E09F1E`, Revise=`75B04C`, Edit=`0BA286`
- Example Div Label styles left at their original colors (no icon, no color change needed).

### Postprocessor changes (`postprocess_docx.py`)

- Removed `DivLabelExample`, `DivLabelExampleGood`, `DivLabelExampleBad` from `DIV_TAG_ICON_STEMS` — Example divs get no tag icon.
- Reduced `DIV_TAG_ICON_HEIGHT_EMU` from 152400 (12pt) to 133350 (10.5pt) to match font height exactly.
- Added `DIV_TAG_ICON_DIST_T_EMU = 38100` (3pt) and applied `distT` on `wp:inline` element to shift icon bottom toward text baseline.
- Increased NBSP after icon from 1 to 2 non-breaking spaces.
- Fixed intermediate save+reload: replaced `doc.save(path); doc = Document(path)` with a temp-file save+move to prevent corrupt DOCX on large icon-embedded files.

### CLI fix (`cli.py`)

- Fixed critical bug: `pandoc_input_fmt` had `-yaml_metadata_block` which disabled YAML front matter parsing, causing `style_bridge.lua` to never receive the `style_map` and silently produce zero Div Label styles. Restored to `markdown+fancy_lists`.

### Build result (session 6)

- Pandoc: clean, no warnings.
- Postprocess: 1676 list styles, 21 alpha markers, 145 checklist items, 85 example block paragraphs, 180 post-list spacing, 39 table styles, 589 div labels (469 with icons), 243 body text, 513 Pandoc fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings.
- Validation: exit 0.
- Both repos committed and pushed. PDF not exported (LibreOffice not installed on current machine).

## 2026-05-18 (session 8 — style architecture simplification and reference DOCX cleanup)

### DivTag character style fix

- Diagnosed root cause of div label icon misalignment: `DivTag` was defined as a paragraph style, so `w:rStyle` references to it on icon runs were silently ignored by Word (rStyle only resolves character styles). Icon inherited raw paragraph style properties with no baseline lowering.
- Changed `DivTag` from paragraph type to character type in reference DOCX with `w:position w:val="-8"` (4pt lower) and `w:u val="none"`. Removed `basedOn` and `next` (not valid on character styles).
- Icon run now correctly receives the 4pt baseline lowering via the character style.

### Icon height

- Changed `DIV_TAG_ICON_HEIGHT_EMU` from 152400 (12pt) to 198000 (0.55 cm) to account for internal PNG padding and baseline repositioning, keeping icon label text legible.

### Div Label style architecture — dropped linked char styles

- Removed all 12 `DivLabel*Char` character styles from reference DOCX.
- Removed `w:link` from all 12 `DivLabel*` paragraph styles.
- Replaced `build_semantic_div_label_styles()` in `postprocess_docx.py`: now reads color directly from paragraph style `rPr` instead of looking up linked char styles.
- Updated `apply_semantic_div_labels()`: applies color and `Noto Sans Condensed Medium` font directly to label runs via `_set_run_color` / `_set_run_font` — no char style assignment.
- Result: reference DOCX reduced from 24 DivLabel styles to 12 (paragraph only); single source of truth for font/size/spacing in `Div Label Base`.

### Reference DOCX — font update

- Set `Noto Sans Condensed Medium` (ascii + hAnsi) on all 12 `DivLabel*Char` styles before they were removed. Font is now applied directly by postprocessor.

### Reference DOCX — AW Table style updates

- All 4 AW Table styles (`AWStandardTable`, `AWComparisonTable`, `AWPhraseBankTable`, `AWRubricTable`) updated:
  - Width: 100% (`pct` type) — fit to text column
  - Layout: `autofit`
  - Paragraph alignment: left (was centered)
  - Paragraph hyphenation: `suppressAutoHyphens` = 1
  - First row: bold, white text, `2D4155` dark blue fill (was already present on AWStandardTable; applied consistently to all four)

### Build result (session 8)

- Pandoc: clean, no warnings.
- Postprocess: 1678 list styles, 21 alpha markers, 145 checklist items, 244 example block paragraphs, 395 post-list spacing, 39 table styles, 127 placeholders, 458 icon labels + 61 emoji labels, 595 div label updates, 219 body text, 513 fallback replacements, 31 non-reference styles purged, 29 page breaks, 3 running headers, 23 unit title tables, 23 Unit Overview headings.

## 2026-05-18 (session 9 — style cleanup, table fixes, icon crops, CLI fix)

### Reference DOCX changes

- Removed `w:autoRedefine` from all 10 DivLabel paragraph styles that had it (`DivLabelBase` + 9 child styles). Child styles now rely on normal Word style inheritance. `DivLabelExampleGood` and `DivLabelExampleBad` already lacked it.
- Set cell margins on all 4 AW Table styles: top/bottom = 57 twips (0.1 cm), left/right = 113 twips (0.2 cm).

### Postprocessor fixes (`postprocess_docx.py`)

- `apply_table_styles()`: added direct enforcement of `tblW` (5000 pct = 100%) and `tblLayout` (autofit) on each table element after applying the style. Pandoc writes explicit `tblW` on generated tables which overrides style-level defaults — direct element patching is required.

### CLI fix (`cli.py`)

- Added `--tag-style` argument (`filled`/`outline`, default `filled`) to the `markdown-to-docx` CLI parser and wired it through to the postprocess call. Was previously only available when running `postprocess_docx.py` directly.

### Icon assets

- Tight-cropped all 9 `tag_outline_*` PNGs in `adv/md/working/div-tags-icons-2_assets/` to content bounds + 1px padding (matching the existing `tag_filled_*` treatment). Height reduced from 59px to ~55px.

## 2026-05-18 (session 10 — AW Table redesign, example block fixes, div fence fixes)

### AW Table style redesign

- User deleted all 4 AW Table styles from reference DOCX after Word refused to apply font/color overrides — root cause: Word's style cascade means table-style `rPr` is always overridden by paragraph styles in cell content.
- New architecture: 4 table styles handle borders/width/margins/firstRow fill only; two new paragraph styles `AW Table Header` and `AW Table Body` carry the font/size/spacing and are applied by the postprocessor to header-row and body-row cells respectively.
- Specs read from sample table created by user in `adv/md/bak/aw-adv-styleref_0515.docx`: header fill `31849B`, header font Roboto Condensed Medium 11pt white bold; body font Noto Sans Condensed Light 11pt, after=60 (3pt), suppressAutoHyphens, keepLines; borders single sz=8 all sides; cell margins top/bottom=57, left/right=142 twips.
- `apply_table_styles()` updated: applies `AW Table Header` to first-row cells and `AW Table Body` to all other cells for any AW-styled table.

### `apply_example_block_styles()` refinement

- Added `_example_seen_prose` flag: first non-italic `Body Text` after a DivLabel is example body content (styled); subsequent non-italic `Body Text` is task instruction (stops styling).
- List paragraphs inside example divs always receive example style — fixes numbered/bullet lists inside `example-good` boxes not being styled.
- Correctly handles: procedure-body examples, numbered-list worked examples, and mixed italic/prose examples without pulling post-example task instructions into the styled box.

### Source markdown fixes

- Fixed 2 misplaced `rewrite` div fences (L2143, L7323): setup instruction + `example` sub-div moved outside the `:::rewrite` open. Div balance remains 585/585.
- Fixed 5 malformed HTML underline tags `<uTEXT</u` → `[TEXT]{.underline}` at L2450–2454.

### Other changes

- Placeholder spacer height increased from 140 (7pt) to 280 (14pt) twips for clearer visual separation between consecutive placeholder tables.
- Working folder cleaned: removed 4 stale backup files; now contains only `aw-adv-all_0516.md`, `aw-adv-all_0518.docx`, `aw-adv-styleref.docx`, `div-tags-icons-2_assets/`.

### Build result (session 10)

- Pandoc: clean, no warnings. 597 div labels (458 icon + 61 emoji + 78 example). 378 example block paragraphs. All other counts stable.
- Validation: exit 0.

## 2026-05-19 (session 11 — inline icon rewrite, emoji removal, example block refinement)

### `apply_semantic_div_labels()` rewrite — inline icon approach

- Replaced the session 7 single-pass 2-column table approach with direct inline icon insertion.
- Icon run and 2× NBSP spacer run are prepended before the first existing run in the `DivLabel*` paragraph — no table created.
- `DivTag` character style applied to icon run via `w:rStyle` for style-driven 4pt baseline lowering.
- Removed `SEMANTIC_DIV_EMOJI` dict and all emoji fallback logic (61 emoji labels from session 10 are gone; divs with no icon file are now skipped silently).

### `apply_example_block_styles()` rewrite — closing-quote boundary detection

- Added `_after_closing_quote` flag: when a styled paragraph ends with `"` or `"`, the next paragraph is treated as post-example task instruction and stops styling.
- Added `NEUTRAL_MODEL_SOURCE_STYLES` (`Block Text`, `Quote`, `Intense Quote`) — these are always styled regardless of italic state.
- Added `QUOTED_MODEL_RE` — matches paragraphs enclosed in curly/straight quotes as model content.
- Correctly handles: procedure-body examples, numbered-list worked examples, mixed italic/prose examples, and quoted model text without pulling post-example instructions into the styled block.

### `apply_table_styles()` — reference DOCX style copy

- Added `reference_doc_path` parameter.
- Calls `_ensure_styles_from_reference()` to copy `AW Table Header` and `AW Table Body` into output DOCX if missing — Pandoc never propagates these styles since they don't appear in source markdown.
- `reference_doc_path` wired through from `insert_section_after_toc()` call site.

### Other postprocessor fixes

- `replace_unit_headings_with_title_tables()`: removes the original heading paragraph entirely (was converting to a page-break paragraph). Page break is now handled by `w:pageBreakBefore` on `AWUnitNumber` style in reference DOCX — avoids a spurious empty paragraph above the title table.
- `apply_body_text_to_normal_paragraphs()`: checks `style_id.startswith('DivLabel')` instead of checking against the now-deleted emoji dict.

### New: `docx-to-pdf` CLI command

- Added `scripts/docx_to_pdf.py`: converts DOCX to PDF using `docx2pdf` (Word COM on Windows).
- Registered as `docx-to-pdf` in `__main__.py`.

### Operational notes

- `textmaker.cmd` path corrected: was pointing to an old location. Updated system PATH and documented the OneDrive sync copy convention in `project-learning.md`.
- Session ended mid-process after VS Code reload required for PATH change to take effect. No build run this session.

## 2026-05-19 (session 13 — Intermediate book scan corrections)

### Issues corrected (from full PDF scan of aw-int-all_0519_stage7a.pdf)

- **F. Reflection wrapping (Issue 2)**: wrapped 22 F. Reflection numbered lists in `:::write` divs with "Reflection" title (Units 2-23). Unit 1 was already wrapped. Pattern: `### F. Reflection` heading followed by bare numbered list — added `:::write\nReflection\n\n` before and `:::\n` after.
- **Lowercase div labels (Issue 3)**: fixed 5 labels with incorrect title case:
  - L2557: `Politeness Scale (from direct ->most polite)` → `Politeness Scale (From Direct to Most Polite)`
  - L4039: `Before you explain a problem, ask` → `Before You Explain a Problem, Ask`
  - L4749: `Module 3 self-edit routine` → `Module 3 Self-Edit Routine`
  - L5147: `Teaching point` → `Teaching Point`
  - L6183: `To keep email style consistent, check` → `To Keep Email Style Consistent, Check`
- **Module 6 Key Lessons (Issue 8)**: added `:::learn` wrapper around Module 6 Review "Key lessons to keep" bullet list — the only module review without a div wrapper.
- **Issues 1, 6 already resolved**: "Example (Part of...)" headings in A sections were already inside `example-good` divs (correct orange rendering). Unit 15 example split was already `example-bad` + `example-good`.
- **AW Table Header (Issue 4, previous session)**: added `AW Table Header` paragraph style (styleId `AWTableHeader`, Roboto Condensed Medium 11pt bold white) to `aw-adv-styleref.docx` — was completely absent, causing all planning/grid table headers to be invisible.

### Build result (session 13)

- Source: `int/md/working/aw-int-all.md` — 10403 lines (up from 10288; +115 from div fence insertions)
- Div balance: 480 opens / 480 closes (Match: True)
- Postprocess: 2291 list styles, 92 alpha markers, 68 checklist items, 8 example block paragraphs, 620 post-list spacing, 18 table styles, 163 placeholders, 465 icon labels, 377 body text, 33 fallback replacements, 31 non-reference styles purged, 23 page breaks, 3 running headers, 23 unit title tables.
- Validation: exit 0.
- Output: `int/md/working/aw-int-all_0519_stage7b.docx` and `.pdf`
- Both repos committed and pushed.

## 2026-05-19 (session 14 — placeholder insertion, example div splits, heading/div title cleanup)

### Work completed

- **Placeholder insertion**: ran `C:\Temp\insert_placeholders.py` to insert ~71 `{{PH-N: code}}` response markers. One NOT FOUND (M2 revision lab — actual div title was `Revision Lab` not `Module 2 Revision Lab`); fixed manually. Final total: 255 PH markers across the INT book.

- **Example div identification and splitting**: identified 13 `:::notice`/`:::learn` divs containing Email A/B, Version A/B, and Summary A/B comparison pairs embedded as plain text. Each split into: original div (intro instruction only) + `:::example-bad` (Version A) + `:::example-good` (Version B). Script: `C:\Temp\split_examples.py`. 12 splits automatic; Module 4 Reader-Trust Clinic required manual fix (was `:::notice` not `:::learn`).

- **Heading restoration and div title renames**: `fix_heading_duplication.py` was run in error — it removed 135 `###` structural headings (A–F letter-sections and module-review sections). User correctly rejected this approach: structural headings must remain. Wrote and ran `C:\Temp\restore_headings_rename_divs.py` which:
  - Restored 83 letter-prefix headings (`### F. Reflection`, etc.)
  - Restored 41 module-prefix headings (`### module 2 email control checklist`, etc.)
  - Restored 11 special headings (6× Key Lessons to Keep, 5 comparison review sections)
  - Renamed 123 div titles to describe activity purpose instead of repeating heading text (e.g., `Reflection` → `Reflect on This Unit`, `Homework` → `Homework Task`, `What Is a Paragraph?` → `Definition`, `Notice Control Board` → `Control Board`, etc.)
  - Module-prefix headings: heading retains module number + full name in lowercase; div title becomes the short type name (e.g., `Email Control Checklist`)
  - Comparison sections renamed: `Email Comparison Review` → heading `### Email comparison review` + div title `Email Comparison`

### Key decision: div titles should describe activity purpose, not repeat heading text

## 2026-09-10 - LTF Batch 3 research briefs: local handoff, verification pass + 3 new briefs

- Cloud session "Let's Talk Finance Batch 3" (branch `claude/compassionate-dirac-67bepn`) had WebFetch blocked by an org egress proxy and drafted all Batch 3 research briefs with facts verified from WebSearch snippets only. It committed through 25751eb, then handed off to a local session with working WebFetch.
- **Verification pass** over the 7 already-drafted briefs (A-3-1..A-3-5, B-3-1, B-3-2): re-checked against primary sources; added a dated "Live-fetch verification pass" note to each. No fabrications found — forward-dated 2025-26 anchors (Feb 2026 SCOTUS IEEPA ruling *Learning Resources v. Trump*, June 2026 BOJ hike to 1% + Nikkei ¥70,000, S&P 500 top-10 concentration 40.7%) all confirmed across multiple independent outlets.
  - Correction: A-3-2 anchor 1 — GI Hub's own figure is a ~US$18tn gap on a US$97tn need; the US$15tn figure is the narrower WEF framing off the US$94tn base.
  - A-3-2 anchor 6 and A-3-5 fact 10 upgraded from single-source caution.
  - Recorded which primary sites block automated fetch (congress.gov CRS, ssa.gov, oecd.org, adb.org, imf.org, bls.gov) but remain stable public pages; their facts corroborated via cited news co-sources.
- **Drafted the 3 missing Batch 3 briefs** with WebFetch-verified anchors, following the B-3-2 template and the `_batch3-shape-plan.md` shape/opening assignments:
  - `B-3-3_Commodities.md` — 2022 oil/food/nickel shocks, 2020 negative WTI, Black Sea Grain Initiative, copper/electrification, China critical-minerals concentration, Japan import dependence (energy 15.2% FY2023 self-sufficiency, food 38% calorie basis).
  - `B-3-4_Currencies_and_Exchange_Rates.md` — weak yen 2022-24 (~161/USD, 38-yr low), Japan FX interventions (JPY 2.8tn/6.3tn 2022, JPY 9.79tn Apr-May 2024), dollar reserve role (~58%), euro-dollar parity 2022, Argentina Dec-2023 devaluation, Swiss franc de-peg 2015. Lead per shape plan.
  - `B-3-5_Emerging_Markets_and_Development_Finance.md` — India as 4th-largest economy 2025 vs Egypt/Pakistan distress; sudden stops & the Fed; IMF EFF (Pakistan US$7bn Sep 2024); SDR US$650bn allocation Aug 2021; Egypt US$8bn IMF + UAE Ras El-Hekma US$35bn + pound float; World Bank IDA/IBRD; China ~US$1.1tn as top bilateral creditor / rescue lending; remittances US$685bn 2024; Japan/JICA/ADB as creditor.
  - Ledger checks done per brief: B-3-5 deliberately avoids Sri Lanka/Zambia/Ghana (A 2.5 primary evidence) and the WB/ADB FY2025 commitment figures (A 3.2 primary evidence); Argentina's Dec-2023 devaluation is used in B-3-4 only, and B-3-5 records it as excluded there to avoid double use within Book B; the weak yen is B-3-4's primary evidence and is kept to a one-sentence amplifier in B-3-3.
- Batch 3 research-brief set is now complete (10/10): A 3.1-3.5, B 3.1-3.5.

## 2026-09-11 - LTF Batch 4 research briefs (Part 4 of both books), WebFetch-verified

- Local session with working WebFetch drafted the full Batch 4 set on `claude/compassionate-dirac-67bepn`. First created `_batch4-shape-plan.md` (article shape + opening style + lead regions + Japan placement for all 10 Part-4 topics), checked against the Batch 1-3 opening ledger so no opening style exceeds ~3 per book; introduced a *scene* opening and a *plain-definition* opening to Book A for the first time.
- **Book A Part 4:**
  - `A-4-1_Anti_Money_Laundering.md` — FATF standard, Danske Bank (EUR 200bn / US$2bn 2022), TD Bank (~US$3bn, first US bank to plead guilty to a money-laundering conspiracy, Oct 2024), EU AMLA (Frankfurt, 2027 rulebook / 2028 supervision), Japan 2021 FATF "enhanced follow-up" + 2022 law changes.
  - `A-4-2_Financial_Literacy_Programs.md` — OECD/INFE 2023 survey (60/100 avg), the 2014 Fernandes vs 2022 Kaiser-Lusardi meta-analyses on whether financial education works, US state high-school mandates (25 -> ~30 states), UK MaPS, Japan J-FLEC (Aug 2024) + 2022 age-of-majority change.
  - `A-4-3_Wealth_Inequality.md` — global 76% / 2% wealth split (WIR 2022), US top-1% ~31% (Fed DFA), OECD annual wealth taxes 12 -> 3, G20/Zucman 2% billionaire minimum tax, Japan's "100 million yen wall" + 2025 minimum tax on top earners.
  - `A-4-4_Corporate_Governance.md` — chronology Cadbury 1992 -> Sarbanes-Oxley 2002 -> Satyam/India Companies Act 2013 -> Japan Stewardship+CG codes 2014-15 -> Wirecard 2020 -> Engine No. 1 vs ExxonMobil 2021 -> TSE March-2023 cost-of-capital / P/B-below-1 initiative.
  - `A-4-5_Economic_Diplomacy.md` — 2022 Russia sanctions (~US$300bn CBR reserves frozen, ~EUR 200bn at Euroclear, G7 US$50bn loan), dollar-system leverage / secondary sanctions, G20/IMF cooperative track + Common Framework (mechanism only), China's AIIB/CIPS, COP29 US$300bn/yr-by-2035 climate-finance goal, Japan's Sakhalin-2 carve-out.
- **Book B Part 4:**
  - `B-4-1_Tax.md` — OECD tax-to-GDP ~33.9% (2023), the tax mix, US (no federal VAT) vs EU (high VAT) models, UAE adding 5% VAT (2018) + 9% corporate tax (2023), the 15% global minimum tax (Pillar Two; US withdrew 2025), Japan consumption tax 3% (1989) -> 10% (2019) and reliance on social-security contributions.
  - `B-4-2_Government_Debt_and_Deficits.md` — deficit vs debt vs ratio; UK 23 Sep 2022 mini-budget + gilt crisis + BoE intervention + Truss 49 days; the three US downgrades (S&P 2011, Fitch 2023, Moody's 16 May 2025); reformed EU fiscal rules (2024); Kenya's withdrawn 2024 Finance Bill; Japan's high-debt/low-yield puzzle framed as political economy (distinct from A 2.5's issuer mechanics — uses rounded ">200% of GDP", not A 2.5's specific figures).
  - `B-4-3_Business_of_Sport_Art_and_Culture.md` — two-case comparison: self-funding (Premier League GBP 6.7bn TV deal, Real Madrid first EUR 1bn club, Saudi PIF in football/golf, top of the art market, Japanese anime JPY 3.3tn 2023 with overseas > domestic) vs subsidy/philanthropy-dependent (US orchestras ~43c/dollar from donations, Germany vs NEA, Baumol cost disease).
  - `B-4-4_Philanthropy_Foundations_and_Impact.md` — problem->responses: 5% payout rule + DAF payout gap; Gates Foundation US$200bn spend-down / close by 2045 (May 2025); MacKenzie Scott >US$19bn unrestricted; "plutocratic philanthropy" critique (Reich); impact investing ~US$1.57tn (GIIN 2024); UK Wellcome Trust ~GBP 37.6bn; Japan giving ~0.23% of GDP + 2008 public-interest-corporation reform.
  - `B-4-5_The_Future_of_Money.md` — short chronology of money's form; Sweden's cash decline (40% -> 8%) AND its 2024-25 reversal to protect cash as civil-defence; most money is already commercial-bank deposits; stablecoins ~US$250bn supply / ~US$33tn 2025 volume (flagged as trading-inflated); tokenised deposits / unified ledgers; UK ~50% branch loss; Japan cash demand ~19-20% of GDP (highest BIS tracks), new banknotes 3 Jul 2024.
- **Ledger discipline for Batch 4:** B-4-2 avoids A 2.5's specific Japan debt figures and the Sri Lanka/Zambia/Ghana restructurings; B-4-3 keeps philanthropy to a mention (B 4.4's territory); B-4-4 keeps wealth-tax policy detail in A 4.3; A-4-5 keeps tariffs out (A 3.3) and uses the Common Framework as a mechanism only (country cases are A 2.5 / B 3.5); B-4-5 deliberately avoids A 1.2's CBDC survey + China e-CNY + digital-euro timeline, A 1.1's GENIUS Act/MiCA/FTX, and A 1.3/A 1.5's UPI/Pix/M-Pesa/METI-43% figures.
- Batch 4 research-brief set complete (10/10): A 4.1-4.5, B 4.1-4.5. All four batches of research briefs (40 topics) now drafted.

- Confirmed user rule: "The structural headings (A–F) and above must remain. If the div title matches the heading, rewrite the div title based on the activity purpose."
- Addendum: "Headings can be shortened if they are long, and the specific detail removed from the heading can become the div title."

### Build result (session 14)

- Source: `int/md/working/aw-int-all_0519.md` — +671 lines net
- Div balance: 506 opens / 506 closes (confirmed via nesting stack check)
- Postprocess: 2240 list styles, 92 alpha markers, 68 checklist items, 14 example block paragraphs, 612 post-list spacing, 21 table styles, 255 placeholders, 465 icon labels, 369 body text, 33 fallback replacements, 31 non-reference styles purged, 23 page breaks, 3 running headers, 23 unit title tables.
- Output: `int/md/working/aw-int-all_0519.docx` and `.pdf` (outline tag style)
- Both repos committed and pushed.

### Outstanding issue: example block styling

- `apply_example_block_styles()` styled only 14 paragraphs — the `_example_seen_prose` boundary logic stops styling when it hits a non-italic `Body Text` paragraph after the first. INT book example bodies often use bold text (not italic), causing premature style cutoff. Pending fix.

## 2026-06-01 - INT Print-Readiness Tooling Fixes

- Scope: `scripts/postprocess_docx.py` and `scripts/docx_to_pdf.py`.
- Trigger: INT Unit 1 PDF/DOCX review found response tables after lists with inconsistent indentation, excessive gaps, narrow table width, and an automated-PDF-only numbered-list restart.
- Action: updated placeholder replacement to parse `rows=N`, remove the extra pre-table spacer, add small post-table spacing, normalize contiguous list runs before list-adjacent placeholders, align placeholder tables to the list text indent, and make list-adjacent placeholder tables extend to the right margin.
- Action: replaced the `docx-to-pdf` dependency on `docx2pdf.SaveAs(FileFormat=17)` with direct Word COM `ExportAsFixedFormat`.
- Verification: `python -m py_compile scripts/postprocess_docx.py scripts/docx_to_pdf.py` passes. A full temporary book build was started but stopped after it ran too long; Dave regenerated the DOCX/PDF manually afterward.

## 2026-06-01 - Case-Specific List Placeholder Policy

- Scope: `scripts/postprocess_docx.py`.
- Trigger: Dave clarified that list indentation should differ between one-placeholder-per-list-item activities and one-placeholder-after-the-whole-list activities.
- Action: changed placeholder replacement so the flush-number/hanging-indent/table-indent policy applies only when the placeholder follows a single-item list run. If the placeholder follows a contiguous multi-item list, the list and table retain normal positioning.
- Verification: `python -m py_compile scripts/postprocess_docx.py` passes.

## 2026-06-02 - List Spacing And Alphabetic List Regression Patch

- Scope: `scripts/postprocess_docx.py`.
- Trigger: Dave reported that list spacing edits appeared not to be applied and alphabetic lists were not being converted after the DOCX conversion refactor.
- Action: extended alphabetic marker detection/stripping from `A.` only to both `A.` and `A)`, and updated list detection so `Checklist` style paragraphs count as list paragraphs for spacing and placeholder policy checks.
- Verification: targeted temporary Markdown-to-DOCX probe showed `list styles`, `post-list spacing`, and `response placeholders` passes running with changed counts; `python -m compileall scripts` and `pytest -q` passed.
- Note: the probe also showed that Pandoc's DOCX writer can strip `- [ ]` checkbox markers before postprocess, leaving plain bullet paragraphs; true source-preserved checkbox styling needs an earlier pipeline marker rather than Word-stage guessing.

## 2026-06-09 - Hidden `No Title` Marker For Example Divs

- Scope: `scripts/postprocess_docx.py`.
- Trigger: Dave wanted neutral/good/bad example blocks to keep their semantic example styling while allowing selected visible example titles to be suppressed when redundant.
- Action: added `NO_TITLE_MARKER_RE` and updated `apply_example_block_styles()` so a `DivLabelExample`, `DivLabelExampleGood`, or `DivLabelExampleBad` paragraph containing exactly `No Title` is removed from the DOCX output but still activates the following example-content styling.
- Verification: `python -m py_compile scripts/postprocess_docx.py` passed.

## 2026-06-10 - `No Title` Regression Fix For Source-Driven Pipeline

- Scope: `scripts/postprocess_docx.py`.
- Trigger: Dave reported that all `No Title` labels were still visible in DOCX output. Diagnosis showed the suppression logic existed only inside `apply_example_block_styles()`, but that pass is intentionally skipped in the source-driven INT pipeline.
- Action: added a separate active `strip_hidden_example_labels()` pass and wired it into the main postprocess pipeline immediately after the skipped heuristic note. The new pass removes `DivLabelExample*` paragraphs whose text is exactly `No Title` while leaving source-driven `AW Example*` content styling untouched.
- Verification: `python -m py_compile scripts/postprocess_docx.py` passed.

## 2026-06-19 - Bosch Meeting 3a Evidence Holder Source Copy

- Created an editable revised DOCX copy of the Meeting 3a EV Dilemma simulation source with a new Evidence Summary holder column identifying which role had each item before the meeting.
- Cross-check result: most rows map directly to Roles A-F; Consumer behavior is a partial wording match to Role E, and Market competition has no exact matching role-sheet data point in the current source.
- Validation: Microsoft Word opened the revised DOCX and exported it to PDF; rendered evidence pages were visually checked for table readability.


## 2026-06-22 - Bosch PPTX Formatting Pass

- Updated the Bosch Logical Thinking & Discussion training slide deck in the client course folder using PowerPoint COM rather than regenerating the PPTX.
- Removed repeated footer text boxes from all slides, converted dense review/summary text to real PowerPoint bullet/numbered list structures, and increased body text sizes where appropriate.
- Preserved Slide 7 animation targets; XML validation found 60 Slide 7 animation targets and no missing shape IDs after the edit.
- Validation: exported 39 slide PNGs, created a contact sheet for layout review, and ran a PowerPoint text-bound overflow check with no remaining overflow issues.
- Backup created: Bosch 2026 - Logical Thinking & Discussion - Training Slides_bak20260622_before-formatting.pptx.


## 2026-06-22 - Bosch PPTX Bottom Bars And Typography Rebalance

- Removed remaining bottom blue bar shapes from the Bosch training PPTX after first deleting their text content.
- Rebalanced non-body text after body/list font enlargement: slide titles, top labels, section transition subtitles, framework labels, table headers, and Slide 7 labels.
- Validation: PowerPoint text-bound overflow check reports no issues; Slide 7 animation target XML still has 60 targets with no missing shape IDs; rendered contact sheet and spot-checked Slide 7 and a transition slide.


## 2026-06-22 - Bosch PPTX Reduced To Slide 7

- Per user request, deleted all slides from the Bosch training PPTX except the former Slide 7 mini logic puzzle slide.
- Backup created before deletion: Bosch 2026 - Logical Thinking & Discussion - Training Slides_bak20260622_before-delete-all-but-slide7.pptx.
- Validation: current one-slide deck contains the former Slide 7 as slide1.xml; animation target IDs and timing node count match the immediate pre-deletion backup, with no missing target shapes.


## 2026-06-22 - Bosch PPTX Argument Model Slides Added

- Added three slides after the preserved mini logic puzzle slide: ORE puzzle explanation, PBSR puzzle process explanation, and PCAF discussion question slide.
- Textbook references used on slides: ORE pp. 1-3, PBSR p. 16, PCAF p. 19.
- PCAF slide is framed as a discussion prompt rather than an applied solution model because the puzzle resolves logically to one outcome rather than two debatable sides.
- Validation: deck now has 4 slides; preserved puzzle slide animation targets remain valid with no missing target shapes; PowerPoint text overflow check reports no issues; rendered slides were visually checked.

## 2026-07-16 - In Company Meetings A3 Cover Sheet

- Created `output/pdf/In Company - Meetings A3 Cover.pdf` as a one-page A3 landscape cover sheet for booklet printing, with the back cover on the left and front cover on the right.
- Used the source A4 page size from `books/In Company/In Company - Meetings (AS Online).pdf` so each half is 595.32 x 841.92 pt and the full sheet is 1190.64 x 841.92 pt.
- Removed revision-date content from the redesigned cover; validation confirmed no `Revised`, `revision`, or `2016` text in the generated PDF.
- Follow-up correction: user rejected the geometric A3 design and requested two separate A4 covers using OpenAI image generation, no logo, no revision dates. Generated new OpenAI art assets and created `output/pdf/In Company - Meetings Front Cover A4.pdf` and `output/pdf/In Company - Meetings Back Cover A4.pdf`. Validation confirmed both are A4 portrait, one page each, with no revision-date or logo-placeholder text.
- Second layout correction: rebuilt the two A4 PDFs with stronger textbook hierarchy, larger main title, one-line subtitle `Skills and Language for Successful Staff Meetings`, no ampersand, and a simplified back-cover hierarchy. The standard front/back filenames now contain the corrected layout; intermediate `redesigned` PDFs and previews were also left in `output/pdf/` and `output/imagegen/`.
- Final direction for this session: user provided a stronger OpenAI Playground front-cover concept. Standard front-cover PDF now uses that Playground image directly as a full-page A4 cover. Generated a matching full-page OpenAI back-cover concept in the same large-type blue/white style and packaged it as the standard back-cover A4 PDF. Avoid manual small-text reconstruction for this cover direction; preserve the large textbook-cover hierarchy shown in the Playground concept.

## 2026-08-12 - Speaking with PowerPoint 2026 Audit Consolidation

- Reviewed `books/Speaking with PowerPoint/old/source/Speaking with PowerPoint.pdf`, rendered a PDF contact sheet via PyMuPDF for visual/layout inspection, and read the Claude.ai and ChatGPT revision audits saved under the book folder.
- Created `books/Speaking with PowerPoint/revision/Speaking with PowerPoint - 2026 Consolidated Revision Task List.md` as the durable consolidated task list for a two-day modernization sprint.
- Consolidation resolves the main audit tension by keeping both a minimum viable two-day update path and future-edition rebuild tasks: immediate priorities are reframing "speech" as business presentation, modernizing/replacing the Ventura case, rewriting slide-design guidance, and adding online/hybrid, accessibility, AI, and data-storytelling coverage.
- Scope update from user: the 2026 revision should move away from a PowerPoint-prescriptive concept and teach broader visual presentation skills across tools. Updated the consolidated task list with a P0 rename/tool-scope decision and reframed the design/delivery tasks around tool choice, format choice, and presenting with visuals rather than one software product.
# 2026-08-12 - Speaking with PowerPoint Plan 3 Review Round

- Ran the first concurrent Plan 3 specialist review round using the defined roles: Language Editor, Business Presentation Specialist, and Asset and QA Specialist. Review was read-only; agents did not draft units or edit files.
- Integrated review findings into the Plan 3 control files: cleaned `plan3.md`, tightened `standard-12-unit-curriculum-spec.md`, expanded `plan3-style-sheet.md`, added audience-variant traceability, hardened Phase 6 QA criteria, and expanded `plan3-case-model-brief.md`.
- Durable decisions: main unit body remains role-agnostic between business clients and government agencies; business-client examples focus on finance/trading operations, reporting, workflow, client service, and control contexts; government examples focus on administrative tasks, service delivery, reporting, coordination, and process improvement; role-specific detail belongs in appendix examples/models and QA, not separate unit tracks.
- Review findings also reinforced that AI content must remain critical-literacy only, visual/tool units need spoken English outputs, and asset QA must enforce source, license, alt text, accessibility, privacy/security, and generated-image inspection fields.
- Record-keeping correction: saved the raw specialist review round output and integration notes to `books/Speaking with PowerPoint/revision/records/plan3-specialist-review-round-1.md`. Going forward, every multi-agent round should have a durable record file with assignments, agent IDs, returned findings, and integration actions.
- Created a Plan 3-specific image register at `books/Speaking with PowerPoint/revision/control/plan3_image_register.json` with 9 planned assets and the stricter asset QA schema. This is separate from the older shared `books/Presentation Skills/images/image_register.json`; future Plan 3 asset work should use the new register unless the user explicitly decides to merge registers.
- Terminology correction: retroactively normalized authored Speaking with PowerPoint planning/control documents from `Lesson` terminology to `Unit` terminology, including filenames, `unit_use` asset schema, `p3-uNN-*` asset IDs, Plan 3 DOCX text, and drafting-round records. External Claude.ai/ChatGPT feedback files were left unchanged as source records. The initial Drafting Agent A run (`019ff4c5-1709-78c1-8969-957af43f6265`) was interrupted before file edits because the assignment used old terminology; this is recorded in `plan3-drafting-round-1.md`.
- Standard first-draft review round: ran Plan 3 Agent 2 (Language Editor, `019ff4d5-6699-7812-a7be-a3fab57532da`) and Agent 3 (Business Presentation Specialist, `019ff4d5-8f09-7472-856b-c906900e576f`) as read-only reviewers over all 12 Standard unit drafts. Findings are recorded in `books/Speaking with PowerPoint/revision/records/plan3-standard-draft-review-round-1.md`. Main integration priorities: create six appendix model stubs, tighten Unit 12 business-purpose requirements, normalize headings, add specialist-term definitions, strengthen pronunciation/intelligibility scaffolding, add learner-facing finance/trading guardrails, improve course-case continuity, and add physical room setup / sector-specific Q&A checks.
- Appendix model drafting started with the Project Results Briefing Models appendix at `books/Speaking with PowerPoint/revision/drafts/appendices/project-results-briefing-models.md`. The paired models cover Seika Capital Operations exception resolution pilot results and Midori Ward intake checklist trial results, using fictional data and parallel teaching points: results-evidence-next steps structure, chart/data explanation, cautious claims, online/async adaptation, evidence-based Q&A, and final recommendation. The drafting round record is `books/Speaking with PowerPoint/revision/records/plan3-appendix-model-drafting-round-1.md`.
- Appendix model drafting round 1 completed all three Standard model files: `process-improvement-briefing-models.md`, `product-service-program-launch-models.md`, and `project-results-briefing-models.md`. The six paired variants now exist as draft infrastructure for revising Units 1-12; next integration pass should normalize appendix heading style, confirm teaching-point fit, and repair unit cross-references to the exact model-set names.
- Appendix model review round 1 completed with Plan 3 Agent 2 / Language Editor and Agent 3 / Business Presentation Specialist as read-only role reviews over the three appendix model draft files. Findings are recorded in `books/Speaking with PowerPoint/revision/records/plan3-appendix-model-review-round-1.md`. Main integration priorities: normalize the six model names, add an appendix timing note, add first-use vocabulary glosses, add Q&A answer frames, add brief pronunciation/intelligibility notes, add delivery/contingency notes, make privacy/security/accessibility checks consistent, and preserve the Teaching-Point Fit Rule.
- Correction: user clarified that appendix presentation models should be complete model presentation scripts, not structured model packs. The current appendix files should be treated as source packs/briefs for script drafting, and `plan3-appendix-model-review-round-1.md` is marked superseded/invalid for final appendix-model approval.
- Folder cleanup: reorganized `books/Speaking with PowerPoint/` into `revision/` and `old/`. Current Plan 3 work, draft units, appendix model source packs, feedback records, archived revision plans, and agent/review logs are under `revision/`; original source files and extracted conversion output are under `old/`. Updated project references to the new paths and added `books/Speaking with PowerPoint/README.md`.
- Appendix full-script drafting round 1 completed with three drafting agents: Tesla (`019ff52b-6ca4-7620-ac07-aeb07c9a21f6`) for process improvement, Sagan (`019ff52b-9796-7233-8ebf-6ce79a88098f`) for launch models, and Averroes (`019ff52b-c18d-71a3-a67a-3b32457532b0`) for project-results models. All three appendix files now contain two complete spoken model scripts. Drafting record: `books/Speaking with PowerPoint/revision/records/plan3-appendix-full-script-drafting-round-1.md`.
- Appendix full-script review round 1 completed with Plan 3 Agent 2 / Language Editor Mencius (`019ff52f-b45d-70a0-93c4-8009aba5c6af`) and Plan 3 Agent 3 / Business Presentation Specialist Carver (`019ff52f-dc7f-7f23-b706-8226b2819e50`) as read-only reviewers. Findings are recorded in `books/Speaking with PowerPoint/revision/records/plan3-appendix-full-script-review-round-1.md`. Main repair priorities: timing-label realism, remove teaching/safeguard metalanguage from spoken scripts, separate script text from teaching notes, add first-use vocabulary support, standardize Q&A function labels, and decide on shared appendix-level AI guidance.
- Timing standard decision: use about 115-125 words per minute as the working timing range for practiced B1-B2 model presentation scripts, with pauses and visual handling included. Updated appendix timing labels and removed the most obvious fictional/practice and teaching-metalanguage wording from spoken script sections.
- Model variety correction: added a `Model Structure and Phrase Variety Map` to `books/Speaking with PowerPoint/revision/control/plan3-case-model-brief.md` because the first full-script draft overused one rigid structure and repeated phrase frames. Updated the six appendix scripts to vary opening styles, transition patterns, and closes while preserving government/non-government teaching-point parity inside each model family.
- Client-context correction: user clarified that the client base is broad, including Mizuho Bank, Mizuho Leasing, Marubeni, NRA, Bosch, PSIA, and the Tokyo Metropolitan Police. Business examples should mainly fit banking/leasing and general trading-company contexts such as Marubeni, not financial-market trading by default. Government/public-safety examples should remain administrative, service-delivery, coordination, reporting, training, or process-improvement focused without political advocacy or sensitive operational/security detail. Current control files, appendix models, asset plans, and Standard unit drafts contain financial-trading assumptions and need a focused repair pass before model approval or unit integration.

## 2026-08-13 - Speaking with PowerPoint Continuation

- User noted limited remaining weekly Codex token capacity and asked for regular project-memory updates, including `books/Speaking with PowerPoint/README.md`, so Claude/Codex can take over if needed.
- Unit 3 `Practice 3: Build a Planning Map` was revised: the table now groups planning items under `Introduction`, `Body`, and `Conclusion`; items under each heading are numbered; `Backup detail that may not belong in the main flow` was replaced with `Summary of key points`.
- Appendix script repair pass started after the 2026-08-12 model review findings. Added explicit script/support-material boundaries and before-listening vocabulary to the three appendix model files, normalized headings in launch/results appendices, removed one teaching-only fictional-data phrase from process language notes, replaced spoken `practice case` with `scenario`, and removed a securities/investment guardrail sentence from a spoken results script.
- Timing check after the pass: process scripts 811/779 words, launch scripts 911/843 words, results scripts 663/682 words; all remain broadly consistent with the approved 115-125 wpm B1-B2 timing standard and current labels.
- Standard unit cross-reference cleanup: tightened references in Units 1, 7, 8, 9, 10, 11, and 12 so they use the exact appendix model-set names and business-client/government-agency variant language. Scan afterward found no stale `lesson` component terminology, old `backup detail` wording, or vague administrative-example references in the current Standard drafts and appendix model files; remaining stock/securities/ticker hits are guardrail notes.
- Control-layer update: `plan3-case-model-brief.md`, `plan3-traceability.md`, and `standard-12-unit-curriculum-spec.md` now reflect exact appendix model-set reference wording and the revised Unit 3 planning map with Introduction, Body, Conclusion, summary of key points, and action/close.
- Unit 4 update: added limitation/risk signposting phrases and a short spoken drill after phrase-repair practice, addressing the recorded review requests for a data/risk signposting example and more controlled spoken drilling.
- Unit 5 update: added an `accessibility` definition before the checklist and a corrected-title table showing article/plural/noun-phrase repairs. Also corrected the stale `Trade confirmation workflow before and after` image-register asset title to `Import document handoff workflow before and after`.
- Validation: `plan3_image_register.json` passes `python -m json.tool`; targeted stale-term scan found no `trade confirmation`, `financial trading`, `market data`, `backup detail`, `main flow`, stale `lesson` component terminology, or vague administrative-example references in current control files, Standard drafts, and appendix model files.
- Current next recommended step: continue deeper Standard unit revision with Unit 6 data/chart language unless the user wants another appendix-script review first.
- Review-sequencing correction: user clarified that Agent 2 and Agent 3 should not run concurrently for final content review. The required order is Agent 3 Business Presentation Specialist first, integrate business/context findings, then Agent 2 Language Editor last because English language development is the highest-priority goal. This is especially important for specialized terminology such as `document handoff`.
- Learner-facing manuscript correction: user clarified that the textbook, including appendices, should be completely learner-facing. Created `books/Speaking with PowerPoint/revision/drafts/Teacher Notes.md` as a separate printable teacher-notes document with Unit and Appendix references; removed embedded teacher-note sections from Standard Units 1-12; converted appendix teacher/editor-facing labels into learner-facing instructions/headings. Scan confirmed no teacher/editor-facing labels remain in learner draft files under `revision/drafts/standard/` or `revision/drafts/appendices/`.
- Teacher-notes update: renamed the teacher-notes file to title-neutral `Teacher Notes.md` and updated it with general teaching notes, the sequential specialist-review rule, terminology/glossary watchlist, and specific notes for the revised Unit 3 planning map, Unit 4 risk signposting drill, and Unit 5 accessibility/title-language content. Current learner-facing scan only returns Unit 7 uses of `support material(s)`, where the term refers to presentation materials for learners.
- Teacher Notes Language Editor pass: confirmed `leave behind` without a hyphen is the phrasal verb, while `leave-behind` as a compound noun is style-dependent and not transparent for B1-B2 learners. Updated `books/Speaking with PowerPoint/revision/drafts/Teacher Notes.md` to recommend `follow-up handout`, `takeaway document`, or `supporting document`; also softened abrupt teacher-note wording and removed project-internal `Standard` labels from teacher instructions.
- Unit 1 teacher-note clarification: rewrote the example-scope note so it clearly says Unit 1 should stay focused on audience, purpose, and audience outcome. Brief business-client and government-agency examples are acceptable when helpful, but fuller workplace examples should come later through appendix models.
- Role-agnostic scope correction: user clarified that the textbook manuscript must be role-agnostic, but classroom lessons do not need to be. Because classes are not mixed-client groups, teacher delivery may and often should focus on the specific learners' roles, company/organization, industry context, and communication needs. Updated `Teacher Notes.md`, book README, and project learning accordingly.
- Sequential Plan 3 review round 2 completed. Agent 3 / Business Presentation Specialist Beauvoir (`019ff90d-6158-78f1-ab20-3dad8389c5f4`) reviewed first and returned `Pass with repairs`; required business/context repairs were integrated before Agent 2. Agent 2 / Language Editor Curie (`019ff911-7262-75a0-850e-9d82f3897508`) then reviewed and returned `Pass with repairs`. Full record saved at `books/Speaking with PowerPoint/revision/records/plan3-sequential-review-round-2.md`.
- Integrated Agent 3 repairs before Agent 2: business-client guardrails now allow fictional/sanitized shipment, order, procurement, supplier-status, workflow, and reporting examples; ambiguous Unit 12 `trade data` was replaced; Unit 1 was renamed `Audience, Purpose, and Workplace Context`; launch/results appendix model headings now identify Business Client or Government Agency variants.
- Open Agent 2 repair list before layout/DOCX production: add first-use vocabulary support in Units 1, 4, 5, 7, and 9; finish Unit 1 `business` to `workplace` wording alignment; define `asynchronous (async)` before use in Unit 9; add `rollout` and `pre-read` to launch-model vocabulary; normalize heading capitalization across Units 1-12; rewrite the launch appendix AI note as learner-facing classroom wording.
- Course-planning update: added expected unit teaching duration guidance to `books/Speaking with PowerPoint/revision/drafts/Teacher Notes.md`: Units 1-3 at 75-90 minutes each, Units 4-10 at 90-120 minutes each, Unit 11 at 90-120 minutes or longer for large classes, and Unit 12 at about 10-12 minutes per learner.
- QA deferral update: added a Phase 6 QA row for the missing options-based decision model. Unit 3 teaches `Situation - options - criteria - recommendation`, but the current appendix model set does not yet include a full model presentation for that structure; this should be deferred explicitly or repaired before final release.
- Unit 12 private-lesson timing update: user noted many classes are 1-to-1, where a final presentation alone can make Unit 12 too short. Added a learner-facing textbook wrap-up quiz to `standard-unit-12.md`, added the answer key and revised timing guidance in `Teacher Notes.md`, and updated curriculum/traceability/QA controls to treat the quiz as a consolidation deliverable.
- Chicago heading capitalization pass: verified Chicago guidance for title/headline-style headings and colon subtitles, updated `plan3-style-sheet.md` from sentence-style headings to Chicago-style title case, and normalized headings/subheadings across current Standard unit drafts, appendix drafts, and `Teacher Notes.md`. Validation scans found no remaining heading lines with lowercase text immediately after a colon.
- Phase 4 completion pass: integrated remaining Agent 2 Language Editor repairs by adding first-use `Useful terms` support in Units 1, 4, 5, 7, and 9; aligning Unit 1 stale `business` context wording to role-agnostic `workplace` wording; defining `asynchronous (async)` before use in Unit 9; adding `pre-read` and `rollout` to Product, Service, or Program Launch Models vocabulary; and rewriting the launch appendix AI note as learner-facing classroom wording. Targeted validation scans passed, and the next recommended step is Phase 5 asset creation/replacement from `plan3_image_register.json`.
- Phase 5 asset repair pass: reran the visual-source batch through the OpenAI Python SDK using `gpt-image-2`, 2560x1440 high-quality opaque PNG, staged in local `%TEMP%` to avoid UNC path problems. Final visible slide/text/chart content was then composed locally with Pillow rather than relying on image-model text rendering. Created 9 final core assets in `books/Speaking with PowerPoint/images/planned/`, 9 SDK source panels plus prompts/manifest in `books/Speaking with PowerPoint/images/source/openai-sdk-2k-final/`, and 36 model sample slides across six folders in `books/Speaking with PowerPoint/images/model-slides/`.
- Phase 5 appendix integration: added learner-facing `Sample Slide Set` sections to the three appendix model files so all six model presentations include six sample slide images. Updated `plan3_image_register.json` to 15 entries: 9 core assets plus 6 model slide-set entries, all still `draft` pending user/editor approval.
- Phase 5 validation: PIL check confirmed all 9 core assets, 36 model slides, and 9 SDK source panels are 2560x1440 RGB PNGs with no embedded PNG text metadata. Contact sheets were visually checked; two result-model slides were corrected so the subtitle, body message, and highlighted key result all refer to the same measure. Appendix image-link validation found no missing image files.
- Phase 5 cleanup before commit: recorded the OpenAI SDK UNC-path workaround in project memory. Deleted superseded image batches `images/source/openai/`, `images/source/openai-platform-import/`, and `images/source/openai-platform-import-2k/`, plus repo-local scratch folder `tmp/imagegen/`. Kept the current SDK source panel batch in `images/source/openai-sdk-2k-final/`, final core assets in `images/planned/`, and model sample slide sets in `images/model-slides/`.
- Phase 5 visual direction correction: user rejected the generated PNG core/model-slide assets as visually unprofessional, with text alignment/readability/layout problems. Deleted the active PNG asset folders `images/planned/` and `images/model-slides/`, changed appendix model references to editable PPTX slide decks, and updated `plan3_image_register.json` to mark the nine core assets as rejected and the six model decks as draft editable PPTX entries.
- Created `books/Speaking with PowerPoint/revision/drafts/appendices/slide-design-checklist.md` as a learner-facing appendix checklist and recorded a three-agent model-slide content scan in `revision/records/plan3-model-slide-content-agent-scan.md`.
- New deck-production decision: build model presentation slide sets as standard PowerPoint-native layouts/placeholders so PowerPoint Designer can improve them. A first readable test deck was created at `books/Speaking with PowerPoint/revision/assets/model-slide-decks/process-business-standard-template-v2.pptx`, with PDF/contact-sheet exports. The earlier custom PptxGenJS shape decks are not approved as the final direction.
- Phase 6 repair-agent review round 1 completed with visual/asset work intentionally excluded for later treatment. Control QA Agent Hilbert (`019ffa96-869e-7263-b4d5-b7fe7c5f9566`) reviewed traceability/defer/evidence repairs; Business/Government Presentation Specialist Boyle (`019ffa96-af6a-7b12-aa75-269db7564f47`) reviewed model specificity, business/government parity, and terminology risk; Language Editor Laplace (`019ffa99-a6a2-7f42-9b0d-58c8a6b3a6d8`) reviewed after Boyle for B1-B2 load, first-use definitions, learner-facing consistency, and assessment descriptors. Record saved at `books/Speaking with PowerPoint/revision/records/plan3-phase6-repair-agent-review-round-1.md`.
- Canva tooling note: user set up a Canva account and wants to explore Canva MCP/connector access for later visual work before resuming Phase 6 text repairs. Official Canva documentation identifies `https://mcp.canva.com/mcp` as the remote MCP server and says popular tools including Codex may already have access, with each user authenticating individually. Phase 6 textual repair queue remains parked and should resume afterward: control evidence files, model-script specificity, terminology support/B1-B2 descriptors, and final language recheck.
- Tooling parking note: Canva plugin/MCP access has been authorized, and the `Default templates` plugin should also be revisited later for PowerPoint-native presentation templates. For now, both are pinned as later visual/deck-production options while the project returns to Phase 6 textbook repair.
- Phase 6 control-layer repair completed for the current Standard-draft review. Added Phase 6 execution tracking to `books/Speaking with PowerPoint/revision/control/plan3-traceability.md`, created `plan3-phase6-defer-log.md`, created `plan3-phase6-issue-classification-log.md`, and updated `plan3-phase6-qa-checklist.md` so QA-001, QA-002, QA-003, QA-119, and QA-121 now pass. QA count is now 71 Pass, 32 Repair, 18 Defer, 1 N/A. QA-120 remains Repair because active manuscript issues are not yet fixed or fully deferred.
- Phase 6 manuscript repair round 1 completed. Repaired model-script specificity, Unit 3 example/evidence scaffolding, Unit 6 terminology support, Unit 8 pointer/cursor guidance, Unit 12 Learner Deliverable/B1-B2 descriptors, Teacher Notes terminology/B1-B2 guidance, and removed deleted-image embeds plus production-facing draft-deck notes from learner-facing drafts. Final Language Editor recheck Agent Sartre (`019ffaca-6661-7613-af0c-cfd23d26d488`) returned Pass with no blocking language issues. Record saved at `books/Speaking with PowerPoint/revision/records/plan3-phase6-manuscript-repair-round-1.md`. QA count is now 83 Pass, 19 Repair, 19 Defer, 1 N/A.
- Phase 6 non-visual repair completion: source verification completed and saved at `books/Speaking with PowerPoint/revision/records/plan3-phase6-source-verification.md`; final source-level proof/style/reference scans passed for current Markdown source. QA count is now 87 Pass, 15 Repair, 19 Defer, 1 N/A. Remaining Repair rows are visual/asset-related except QA-120, which remains the summary open-significant-issues row until visual/asset issues are resolved or formally deferred.

## 2026-08-14 - Speaking with PowerPoint Slide-Text Reset

- Archived the old combined model-slide content scan to `books/Speaking with PowerPoint/revision/records/archive/plan3-model-slide-content-agent-scan-archived-2026-08-14.md`.
- Recreated `books/Speaking with PowerPoint/revision/records/plan3-model-slide-content-agent-scan.md` as an index to the current slide-text review files rather than as a full agent-scan record.
- Created six current slide-text planning files under `books/Speaking with PowerPoint/revision/assets/model-slide-text/`, one for each appendix model presentation. Each file includes exact on-slide text, one or two emphasis points, and visual direction based on the revised model scripts.
- Updated `books/Speaking with PowerPoint/revision/control/plan3_image_register.json` so model-deck source details point to the rebuilt slide-text plans and not the rejected PptxGenJS/generated-slide workflow. JSON validation passed after removing a PowerShell-introduced UTF-8 BOM.
- Began DOCX production planning by reading the Business Result 2e scalable style definition under `style_definitions/business_result_2/2026-08-13/`. Confirmed `br2e_data.py` is the authoritative style source and that it provides A4-scaled typography, geometry, colors, Word-style rows, and PowerPoint theme notes.
- User set the production type-size rule: commercial textbook sizes are too small; main body text should be `11 pt`, with other sizes scaled proportionally and rounded to Word-compatible half-point increments.
- Scanned the current `books/Speaking with PowerPoint/revision/drafts/` manuscript set and created `books/Speaking with PowerPoint/revision/control/presentations-style-set.md`. The file defines the planned `presentations_style.docx` style system, including print-safe colors, typography, unit/section/practice heading treatments, callouts, block text, model scripts, numbered-sequence backgrounds, and distinct table families for phrase banks, vocabulary, planning forms, comparisons, checklists, rubrics, model support, and quizzes.
- Extended `scripts/generate_reference_docx.py` with a new `--spec <styles.yaml>` mode so future reference DOCX files can be generated from structured YAML instead of a manually built source DOCX. The existing default and `--input source.docx` modes remain backward-compatible, and `--input`/`--spec` are mutually exclusive. Updated `README.md` with the minimal YAML schema and verified `tests/test_docx_styles.py` in the repo virtual environment: `14 passed`.
## 2026-08-14 - Presentations textbook DOCX style definition expanded

- Expanded `books/Speaking with PowerPoint/revision/control/presentations-style-set.md` beyond paragraph/table styling to include production layout decisions: A4 page setup, margins, header/footer rules, line spacing, heading spacing, page-break rules, TOC, front matter, back matter, covers, image/caption handling, table overflow, accessibility/export QA, metadata, and open build decisions.
- Added explicit list-style definitions for bullets, nested bullets, numbered lists, nested numbered lists, checklists, and sequence lists. Automatic numbering binding may still require Pandoc/Word numbering XML or postprocessing, but the named paragraph styles now exist in the YAML reference source.
- Added `books/Speaking with PowerPoint/revision/control/presentations_style.yaml` as the reusable YAML source for generating `presentations_style.docx`. Probe generation to `%TEMP%\presentations_style_probe.docx` succeeded with 64 styles.

## 2026-08-14 - BR2e-derived DOCX style creation requirements added to Plan 3

- Added a DOCX style creation workstream to `books/Speaking with PowerPoint/revision/control/plan3.md`.
- Added QA rows `QA-123` through `QA-132` under `## 11a. DOCX Style Creation QA` in `books/Speaking with PowerPoint/revision/control/plan3-phase6-qa-checklist.md`.
- The new rows track BR2e-derived requirements: component library, activity number/instruction pairing, cross-reference line style, contents/course-map styling, section-family accents, image placement specs, rule weights, learner-writing/fill-in lines, source/provenance discipline, and shared theme tokens across DOCX/slides/Canva/template work.

## 2026-08-14 - Speaking with PowerPoint component library expanded

- Created and expanded `books/Speaking with PowerPoint/revision/control/presentations-component-library.md` as the production component library for the textbook.
- The file now goes beyond the Markdown manuscript inventory and includes DOCX-only production components: page sections, margins, running heads, page numbers, unit opener shapes, heading rules, callouts, task blocks, table families, list-block spacing, learner writing areas, figure handling, appendix model components, teacher notes, style specimens, and QA requirements.
- User clarified that Markdown files provide only the bare minimum and cannot define page numbers, callout framing, unit header shapes, or other document-production behavior. The component library now records that distinction and identifies which components require reference DOCX styles, Pandoc mapping, Lua filters, DOCX postprocessing, or manual/design-tool handling.

## 2026-08-14 - Presentations style DOCX regenerated with Noto and table refinements

- User criticized the first `presentations_style.docx` as too harsh/generic: headings needed left alignment, Arial was undesirable, bold should be reduced in favor of Medium/SemiBold faces, heading spacing was too tight, and table styles looked default/undefined despite having different names.
- Checked installed fonts: system has `Noto Sans`, `Noto Serif`, `Noto Sans Display`, `Noto Serif Display`, `Noto Sans JP`, and `Noto Serif JP` variants available. Adopted a Noto-based style direction.
- Updated `books/Speaking with PowerPoint/revision/control/presentations_style.yaml` with Noto fonts, softer muted palette, left-aligned headings, increased heading spacing, wider body leading, and table-family metadata.
- Added `scripts/refine_presentations_reference_docx.py` to enrich Word table styles with first-row, first-column, and banded-row conditions, then normalize the package through Microsoft Word COM. Regenerated `books/Speaking with PowerPoint/revision/control/presentations_style.docx`; validation found required Noto font names, left alignment, auto-hyphenation, snap-to-grid disabled, list hyphen suppression, and conditional table-style XML in the DOCX.

## 2026-08-14 - Presentations palette changed to Wada-derived base colors

- User supplied three main textbook colors from Sanzo Wada's `A Dictionary of Color Combinations`: Eupatorium purple `(25,79,12,0)`, cream yellow `(0,28,68,0)`, and blue `(95,54,0,0)`.
- Updated `books/Speaking with PowerPoint/revision/control/presentations_style.yaml` to track these bases and all derived shades/tints under `color_system`, including the CMYK-to-RGB and RGB mix formulas.
- Regenerated `books/Speaking with PowerPoint/revision/control/presentations_style.docx` and reran `scripts/refine_presentations_reference_docx.py --word-com-save`. Package validation found Wada-derived visible colors and table conditional styles in `word/styles.xml`; base cream yellow and base blue are tracked in YAML but intentionally not directly used in visible styles because the document uses darker/tinted derivatives for print readability.

## 2026-08-14 - Presentations style DOCX follow-up repairs

- User reviewed the improved style DOCX and requested five fixes before moving to the next production step.
- Updated `presentations_style.yaml`: heading styles now suppress automatic hyphenation; `PS Heading 1` and `PS Unit Title Band` reduced from `32 pt` to `28 pt`; shaded task heads (`PS Practice Head`, `PS Speaking Task Head`, `PS Learner Deliverable Head`) retain their normal heading space before after user clarification, with any shading-over-gap issue deferred to DOCX cleanup if needed.
- Updated `scripts/refine_presentations_reference_docx.py`: table header-row conditional styles now force white text on dark fills and single-spaced paragraph settings.
- Regenerated `books/Speaking with PowerPoint/revision/control/presentations_style.docx` and reran Word COM normalization. Validation confirmed unit-title `28 pt`, heading hyphen suppression, retained task-heading spacing, and single-spaced/light table header rows in the DOCX XML.
- Follow-up sample-feedback pass: updated the style spec to top `20 mm`, bottom `25 mm`, left `40 mm`, right `25 mm`; added odd/even right-aligned page-number footer generation; tightened list-block spacing; removed table-header space after in marked tables; changed `PS Planning Table` to a darker Slate header with white text; increased inset on filled paragraph styles used in the sample; and documented the rule against ordinary back-to-back headings.
- Second follow-up sample-feedback pass: removed artificial Lua list-block spacer paragraphs from the sample metadata; changed DOCX postprocessing so post-list spacing normalizes to `0` by default; removed paragraph indents from task-heading styles so headings align with body text; standardized the filled callout/body box family to a shared `5 mm` inset; added direct visible borders to marked PS table families in `scripts/postprocess_docx.py`; regenerated `presentations_style.docx`, refined it through Word COM, rebuilt `presentations_style_sample.docx` through `textmaker.cmd markdown-to-docx` with `presentations_style.docx` and `scripts/style_bridge.lua`, and exported `presentations_style_sample.pdf`.
- Third follow-up sample-feedback pass: changed the fixed base palette to China Rose `#A24F71`, Geebung `#C98F21`, and Green Blue `#3366A8`; updated `presentations_style.yaml` so main headings use the base colors directly; normalized non-heading/non-table paragraph text styles to `1.2` line spacing; normalized list paragraphs to `1.1`, left alignment, and no automatic hyphenation; added table-body postprocessing so body cells are `1.1`, left aligned, and no-hyphenation while table header rows remain single-spaced. Regenerated `presentations_style.docx`, refined it through Word COM, rebuilt the sample DOCX through the Textmaker Markdown-to-DOCX route with `scripts/style_bridge.lua`, exported the PDF, and verified the generated DOCX XML.

## 2026-08-31 - SWP text-first DOCX draft readability pass

- Generated and committed the first text-first Standard DOCX/PDF draft under `books/Speaking with PowerPoint/revision/output/docx-draft/`.
- After PDF inspection, repaired style readability issues: reduced H1/unit-title styles from `28 pt` to `24 pt`, disabled global auto-hyphenation for learner readability, removed the draft-only `Visual Work Deferred` back-matter block from the learner-facing draft, and patched `scripts/refine_presentations_reference_docx.py` so reference/specimen table headers export with readable light text on dark fills.
- Regenerated `presentations_style.docx` via `textmaker.cmd generate-reference --spec`, refined through Word COM, rebuilt `swp-standard-text-first-draft.docx` with `scripts/style_bridge.lua`, validated the DOCX against the reference, exported updated PDFs, and spot-checked rendered pages.

## 2026-08-31 - SWP TOC depth adjustment

- Recorded the user's TOC decision: production DOCX/PDF builds should use Textmaker --toc --toc-depth 1 unless a later custom/manual contents page replaces the automatic TOC.

## 2026-08-31 - SWP DOCX style and page setup enforcement

- Updated the SWP style pipeline so `presentations_style.yaml` defines screenshot-matching mirror margins and explicit `PS Table Header Text` / `PS Table Body Text` styles. Updated reference generation and postprocessing so the generated DOCX applies PS body/list/table-cell paragraph styles programmatically after Pandoc conversion. Rebuilt `presentations_style.docx`, `presentations_style.pdf`, and the current text-first DOCX/PDF draft.

