# Book Draft-and-Edit Process Guide

Written 2026-08-27, based on the "Let's Talk: Investor Relations" project in this repository. Intended as reusable guidance for running the same kind of draft-and-edit workflow on a different book/project.

## 1. Content foundation

- **Define scope up front**: N topics organized into parts (this project: 4 parts x 5/7/5/3 topics = 20), each topic with a fixed template — Goal, Reading, Vocabulary Focus, Reading Questions, Discussion Questions, Source Notes.
- **Company/example variety audit**: track which real-world companies/examples appear where, in a control doc (`company and geography audit.md`), to catch over-reliance on one company or one region before it becomes a rewrite.
- **Vocabulary tracking**: maintain a `vocabulary map.md` (topic -> New terms / Recycled terms) kept in lockstep with each article's own Vocabulary Focus section and a full glossary file. This paid off directly when an accessibility pass needed to add ~40 terms across many articles — having the map already meant each term could be placed correctly (New at first use, Recycled after) without re-deriving the whole sequence.
- **Source discipline**: every factual claim gets an inline `[N]` citation matched to a numbered Source Notes list, verified against primary sources.

## 2. The editing loop that mattered most

The most valuable pattern was: **make an editorial pass -> export to PDF -> programmatically check the actual result -> fix precisely what's wrong -> re-check.** Word count and "looks about right" were both misleading at different points:

- Word-count-based page-fit estimates were wrong in both directions (over- and under-counting overflow) until checked against a real rendered PDF.
- A naive full-topic-page-span heuristic over-flagged overflows that were actually just long Source Notes lists, not real Reading-section overflow. The fix was checking specifically "does the next heading appear within N pages," not "how many pages does this topic occupy total."

## 3. Being your own PDF generator

This environment had no LibreOffice or poppler-utils, which earlier sessions treated as a hard blocker. The unlock: **Microsoft Word itself is installed and fully scriptable via PowerShell COM automation** (`New-Object -ComObject Word.Application`). Pattern that worked reliably:

```
Documents.Open($path) -> Fields.Update() -> ExportAsFixedFormat($outPdf, 17) -> Close -> Quit
```

Pitfalls worth flagging in a new project too: `Resolve-Path` needs `.ProviderPath` before handing to COM; never kill a Word process mid-export (guaranteed corruption of that attempt, not a safe retry); a stuck-looking export is usually an invisible dialog, not genuine slowness — check CPU is actually advancing before waiting longer.

For genuinely visual review (not just text extraction), `pypdf` only gives text. Rendering an actual page image used the **Windows Runtime PDF API** (`Windows.Data.Pdf.PdfDocument`) via PowerShell reflection helpers — this is what made it possible to actually see a cover design and catch a font-sizing bug that text extraction alone would have missed.

## 4. DOCX structural traps (all cost real rework)

- **Section breaks are paragraph-attached, invisible, and easy to delete by accident.** Each topic's 2-column Reading layout is bounded by two empty paragraphs carrying `sectPr`. A naive "delete everything between heading A and B" script deleted them and collapsed 42 sections into 2. Always explicitly locate and protect `sectPr`-carrying paragraphs before any bulk paragraph deletion, and add a hard assertion on expected count.
- **Hyperlinks live in `w:hyperlink` elements that `paragraph.runs` doesn't see.** Editing a paragraph's runs directly leaves old hyperlink text concatenated with new. Fix pattern: locate and remove the `w:hyperlink` XML, drop the old relationship, create a new one, rebuild the hyperlink field explicitly.
- **List numbering that should restart per-section needs an explicit `startOverride`.** Giving each section its own `numId` isn't enough if they share an `abstractNum` — without `<w:lvlOverride><w:startOverride val="1"/></w:lvlOverride>` on each instance, Word treats them as one continuous counter.
- **Pandoc + Markdown formatting quirks carry through literally.** A missing blank line before a numbered list (present for one section, absent for another) caused Pandoc to merge one list into a single run-on paragraph while correctly splitting the other — the same Markdown *looked* equivalent but wasn't.
- **Style-reference conversion (`pandoc --reference-doc`) works well** for matching a new document's fonts/headings/list styles to an existing one — confirmed by comparing actual font/size values, not just style names.

## 5. Process/communication lessons

- **Confirm the audience calibration once, explicitly, and treat it as governing everything** — not just vocabulary. This project is for an upper-intermediate ESL learner, which should shape sentence complexity, idiom use, and length decisions throughout, not just glossary-term choices. Establish this before the first editorial pass, not partway through.
- **When trimming for length vs. preserving evidence are in tension, say so and ask rather than guessing the tradeoff** — a "fix all flagged terms" instruction and a "fit on one page" instruction can pull in opposite directions; better to flag the conflict than silently pick one.
- **Read files before distributing them**, even ones flagged as not worth worrying about — this caught a third-party client logo embedded in a template file before it was copied forward, which mattered for knowing what to leave untouched.
- **Keep a QA checklist and a project journal updated as you go**, dated, with what was checked and what passed/failed — this made every subsequent session (including compaction/context resets) able to pick up cleanly without re-deriving history.
