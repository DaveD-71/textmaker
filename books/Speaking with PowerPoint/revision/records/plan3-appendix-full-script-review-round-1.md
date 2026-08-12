# Plan 3 Appendix Full-Script Review Round 1

Date: 2026-08-12

Purpose: run Plan 3 Agent 2 and Agent 3 as read-only reviewers over the completed appendix model scripts.

## Reviewed Files

- `books/Speaking with PowerPoint/revision/drafts/appendices/process-improvement-briefing-models.md`
- `books/Speaking with PowerPoint/revision/drafts/appendices/product-service-program-launch-models.md`
- `books/Speaking with PowerPoint/revision/drafts/appendices/project-results-briefing-models.md`

## Review Assignments

| Agent Role | Agent ID | Nickname | Scope | Result |
|---|---|---|---|---|
| Plan 3 Agent 2: Language Editor | `019ff52f-b45d-70a0-93c4-8009aba5c6af` | Mencius | B1-B2 level control, ESL pedagogy, spoken-script quality, language notes, Q&A language, pronunciation/intelligibility, Japanese-learner support, AI policy. | Complete. Found timing issues, some script lines that break role-play, teaching metalanguage inside launch scripts, and uneven vocabulary/Japanese-learner support. |
| Plan 3 Agent 3: Business Presentation Specialist | `019ff52f-dc7f-7f23-b706-8226b2819e50` | Carver | Business realism, finance/trading and government guardrails, teaching-point fit, visual/document/Q&A quality, privacy/security/accessibility/contingency notes, variant parity. | Complete. Timing-fit review raised the severity of timing issues and recommended relabeling or trimming scripts. |

## Agent 2 Findings: Language Editor

### High

1. Several timing labels encourage rushed B1-B2 delivery.

   Files and locations:
   - `books/Speaking with PowerPoint/revision/drafts/appendices/process-improvement-briefing-models.md`, timing labels for both models.
   - `books/Speaking with PowerPoint/revision/drafts/appendices/product-service-program-launch-models.md`, timing labels for both models.

   Summary: process and launch scripts are too long for their stated timings at realistic B1-B2 delivery speed. Suggested timing labels: process business 7.5-8.5 minutes, process government 7-8 minutes, launch business 8.5-9.5 minutes, launch government 8-9 minutes. Project results scripts fit better.

2. Some spoken-script lines break role-play by speaking as a textbook, not as a workplace presenter.

   Examples include lines such as "fictional practice data," "used for this presentation or practice," and "these figures are fictional for this practice model." These safeguards should usually be outside the spoken script or in teacher notes.

### Medium

3. Product launch scripts include teaching metalanguage inside the presentation.

   Phrases such as "The visual hierarchy is important here" and "we will use four document roles" teach useful points but do not sound like natural business presentation language. They should be rewritten as natural presenter phrases.

4. The appendix files still partly read as model packs, not clean complete scripts.

   The full scripts are present, but scenario briefs, visual tables, teaching maps, and notes surround them. The script and teaching notes should be visually separated so learners do not confuse support material with spoken content.

5. First-use vocabulary support comes after learners have already met difficult terms.

   Terms such as `exception`, `handoff`, `control process`, `visual hierarchy`, `document roles`, `controlled expansion`, and `volume-adjusted view` need a short before-reading/listening glossary or simpler language in the script.

6. Japanese-learner support is helpful but uneven across the set.

   The set could use more support for article/plural control in slide text, avoiding over-scripted delivery, and direct-but-polite recommendation language.

### Low

7. Q&A language is generally strong, but labels are not fully consistent.

   Standardize function labels such as clarify, answer directly, bridge to evidence, acknowledge risk/limitation, defer safely, and confirm next action.

8. AI policy passes, with one consistency note.

   The launch appendix includes a compliant AI note. Process and project results do not mention AI, which is acceptable. A shared appendix-level AI note may be cleaner than placing the note only in the launch file.

## Agent 3 Findings: Business Presentation Specialist

### High

1. Process-model timing labels are too short for realistic B1-B2 delivery.

   - Business process script: 841 words labeled as 6 minutes; realistic delivery is about 7.0-8.4 minutes before Q&A.
   - Government process script: 788 words labeled as 6 minutes; realistic delivery is about 6.6-7.9 minutes before Q&A.

   Recommendation: relabel process models as `7-8 minutes plus 4 minutes Q&A`, or cut about 180-240 words each for true 6-minute models.

2. Project-results timing labels may be slightly long for the script length.

   - Business results script: 718 words labeled as 7-8 minutes; realistic delivery is about 6.0-7.4 minutes.
   - Government results script: 735 words labeled as 7-8 minutes; realistic delivery is about 6.1-7.4 minutes.

   Recommendation: relabel as `about 6-7.5 minutes plus Q&A`, or add a short optional evidence/detail segment if the 7-8 minute slot must be filled.

### Medium

3. Launch-model timing labels are slightly short.

   - Business launch script: 915 words labeled as 6.5-7.5 minutes; realistic delivery is about 7.6-9.2 minutes.
   - Government launch script: 867 words labeled as 6.5-7.5 minutes; realistic delivery is about 7.2-8.7 minutes.

   Recommendation: relabel as `7.5-9 minutes plus 5 minutes Q&A`, or cut about 100-180 words each.

## Integrated Repair List

1. Repair timing labels across all six model scripts using realistic B1-B2 delivery speeds. User-approved working standard: about 115-125 words per minute for practiced B1-B2 model delivery, with pauses and visual handling included.
2. Move fictional-data and practice-safeguard wording out of the spoken script body where it sounds unnatural.
3. Rewrite teaching metalanguage inside launch scripts into natural business presenter language.
4. Visually separate script text from teaching notes/support materials.
5. Add short before-reading/listening vocabulary support for difficult recurring terms.
6. Standardize Q&A function labels across all model files.
7. Decide whether AI guidance belongs as one shared appendix-level note instead of inside only the launch appendix.
8. Repair over-rigid model structure and repeated phrase frames. User clarified that the models should demonstrate varied presentation structures and target phrases while preserving government/non-government teaching-point parity.

## Review Outcome

The appendix scripts are now the correct artifact type, but they are not yet approved. The next repair pass should fix timing, role-play realism, script/note separation, vocabulary support, and Q&A-label consistency before unit integration.

## Superseding Client-Context Correction

After this review round, the user clarified that `trading` means general trading-company/import-export contexts such as Marubeni-type businesses, not financial-market trading by default. Review findings that refer to finance/trading should be read as superseded where they imply securities, trading desks, trade confirmations, market data, ticker symbols, or investment contexts. Current repair work should use banking/leasing, general trading-company/import-export, manufacturing/industrial, operations, reporting, procurement, supply chain, and account-service contexts while preserving the government/non-government model split.
