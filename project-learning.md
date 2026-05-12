# Project Learning

Current durable project facts, constraints, and decisions for this workspace.

## Workspace

- Workspace root: `<repo-root>`
- Repository: Git repository on branch `main` with remote `origin` -> `git@github.com:DaveD-71/textmaker.git`
- Project memory status: repo-level memory scaffold created on `2026-03-24`; `project-learning.md` and `project-journal.md` are now the main source for ongoing project developments and durable decisions.

## Purpose

- `textmaker` is a textbook-content conversion toolkit centered on Markdown, DOCX, PDF, image OCR, PPTX packaging, and YAML-to-audio workflows.
- The primary publishing goal is converting Markdown textbook content into professionally styled Word documents using Pandoc plus a reusable `reference.docx`.
- The reverse-conversion goal is extracting DOCX content back into unit-level Markdown with assets and style references preserved.

## Core Workflows

- `generate-reference`: build `reference.docx` either from project defaults or from an existing source DOCX.
- `markdown-to-docx`: convert one Markdown file or a folder of Markdown files into a styled DOCX, optionally with a TOC.
- `docx-to-markdown`: convert a DOCX into split Markdown units plus extracted assets and a reference DOCX.
- `split-docx-units`: split a DOCX into per-unit DOCX files based on unit markers.
- `preprocess-docx`, `postprocess-docx`, and `postprocess-markdown`: preserve structural markers and restore DOCX/Markdown formatting details around the Pandoc pipeline.
- `pdf-to-markdown` and `image-to-markdown`: OCR-oriented extraction pipelines for PDFs and images.
- `pptx-to-package`: export PowerPoint decks into structured YAML/JSON packages with extracted assets.
- `yaml-to-audio`: synthesize MP3 assets from YAML dialogue/text fields via Piper.

## Tooling And Dependencies

- Python 3.9+ is required.
- `pandoc` must be installed separately and available on `PATH` for Markdown/DOCX conversions.
- `piper` and `ffmpeg` are required for YAML-to-audio MP3 generation.
- PDF extraction depends on Poppler tools (`pdftotext`, `pdfimages`, `pdftoppm`) and `tesseract` for OCR.
- `docs/requirements.txt` is the documented Python dependency entry point for the local virtual environment workflow.
- Optional document inspection/editing can use Microsoft Word or LibreOffice.

## Operational Conventions

- The Windows entry point is `textmaker.cmd`, which wraps the module CLI commands.
- Markdown folders passed to `markdown-to-docx` are merged in sorted order, with section breaks inserted between files.
- When `--toc` is used for DOCX generation, the output gets a separate TOC section and page numbering restarts at 1 for the content.
- DOCX-to-Markdown defaults to Heading 1 unit splitting, extracts package media into assets folders, and writes numbered Markdown unit files such as `01-<slug>.md`.
- Shape extraction is a first-class part of the DOCX reverse-conversion workflow; shapes are emitted with stable markers plus XML and JSON sidecars.
- Split DOCX unit filenames follow ASCII lowercase slug conventions with numbered prefixes, and front matter becomes `00-front-matter.docx` unless disabled.
- PPTX package export uses stable per-slide object IDs and currently treats transitions/animations as MVP placeholders.

## Decisions

- Keep the bootstrap file pair synchronized between `%USERPROFILE%\.codex\AGENTS.md` and `<repo-root>\AGENTS.md`.
- Use `<repo-root>\instruction-read-log.csv` as the startup read audit log for this repository now that the local scaffold exists.
- Treat `%USERPROFILE%\.codex\memories\user-learning.md` as canonical user memory and `<repo-root>\user-learning-mirror.md` as the portable mirror copy.
- Use project memory files as the primary ongoing record for project progress, durable decisions, constraints, and roadmap changes, rather than relying on the README for development history.
- For Administrative Writing course DOCX output, map the `Call Out - Check` Quick Part to preparatory process cautions and `Before you write` prompts rather than to general review or checklist blocks.
- Treat the reference DOCX as the canonical source for document-level formatting defaults plus custom semantic styles and callout/table prototypes; apply textbook-specific custom formatting through a rule-based DOCX postprocess layer rather than manual cleanup.
- For the Administrative Writing books, keep Quick Parts only for unit title blocks; apply all other semantic emphasis through paragraph styles rather than callout tables so the page hierarchy stays quieter.
- Preserve the semantic markdown hierarchy as `## unit`, `### framework section`, `#### activity/task`, and avoid using headings for model-text labels such as `Original Version` / `Revised Version`.
- Apply `After List` both after actual list paragraphs and after short follow-on commentary blocks when the paragraph is a prompt-style line such as `Practice ...`, `Reflect:`, or `Example:`.
- When rewriting DOCX XML parts directly, preserve the original root namespace declarations and compatibility prefixes exactly; rewriting `word/styles.xml` without the declared `mc`/`w14+` namespaces corrupts the package for Word even if the visible style data looks valid.

## Constraints

- Preserve UTF-8 encoding for `<repo-root>\instruction-read-log.csv`; if mixed encoding is detected later, archive and recreate the log instead of appending.
- Several key features depend on external binaries, so repo functionality is not self-contained in Python alone.
- The README presents the current workflow as a prototype around Pandoc and generated reference DOCX styling; future changes should preserve that architecture unless intentionally revised.
- Before running Textmaker conversion commands, verify every referenced path with the shell first, including source, reference DOCX, Lua filters, output parent, and temporary copied filter paths. On Windows, do not pass paths containing shell metacharacters such as `&` through `cmd.exe` or fragile `Start-Process -ArgumentList` joins; either invoke through an argument-safe path or copy the referenced file to a no-spaces/no-metacharacters temp path before launching.
- For Advanced Administrative Writing DOCX generation, run the intended Textmaker CLI pipeline with `--reference` passed through to Pandoc as `--reference-doc` and the course Lua Div filter supplied with `--lua-filter`; do not repair generated DOCX style packages by copying XML parts from the reference after conversion.
- For Advanced Administrative Writing DOCX generation, pass `--no-pagebreak-filter`; the Advanced Lua filter suppresses standalone `---` separators, while Textmaker's built-in `pagebreak.lua` incorrectly turns them into page breaks.
- Treat Pandoc fallback styles such as `Compact` and `VerbatimChar` as cleanup targets in postprocess when they are not present in the reference DOCX; map them to approved reference styles rather than allowing generated-only styles to remain in output.
- For Advanced Administrative Writing alphabetic option lists, use the reference style `List Number 3`; after applying it in postprocess, remove literal source markers such as `A. ` from the paragraph text so Word supplies the list label exactly once.
- For Advanced Administrative Writing semantic Div labels, preserve the semantic paragraph style on the label/title line; do not replace it with `Label Base Para`/`Label Para`. Set label paragraph spacing after to 4pt and moved content paragraph spacing before to 0pt.

## Roadmap From README

- Improve `reference.docx` to support running headers with chapter titles and page numbers.
- Add automated merging of multiple chapters plus front and back matter.
- Add automated image handling for placement, captions, and numbering.
