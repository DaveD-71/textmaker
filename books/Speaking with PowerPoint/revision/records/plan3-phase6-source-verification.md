# Plan 3 Phase 6 Source Verification

Created: 2026-08-13

Purpose: satisfy Phase 6 QA-085 for current Standard draft claims that depend on official or stable sources. This record covers accessibility, tool-check, metadata, confidentiality, copyright/licensing, and 2026 workplace/tool-neutral claims in the learner manuscript and control files.

## Sources Checked

| Source | URL | Used for |
|---|---|---|
| W3C WCAG 2.2 Understanding Success Criterion 1.4.3: Contrast (Minimum) | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | Contrast guidance: 4.5:1 for normal text and 3:1 for large text. |
| W3C WCAG 2.2 Recommendation | https://www.w3.org/TR/WCAG22/ | WCAG 2.2 as the current referenced accessibility standard. |
| W3C WAI Images Tutorial: Alt Decision Tree | https://www.w3.org/WAI/tutorials/images/decision-tree/ | Principle that meaningful images need text alternatives and decorative images may be treated differently. |
| Microsoft Support: Make Your PowerPoint Presentations Accessible to People with Disabilities | https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities | PowerPoint accessibility practices, including alt text and Accessibility Checker guidance. |
| Microsoft Support: Add Alternative Text to a Shape, Picture, Chart, SmartArt Graphic, or Other Object | https://support.microsoft.com/en-us/accessibility/office-accessibility/add-alternative-text-to-a-shape-picture-chart-smartart-graphic-or-other-object | Office alt-text tooling and AI-generated alt-text caution. |
| Microsoft Learn Answers: Remove Personal Information from Office Documents | https://learn.microsoft.com/en-us/answers/questions/5222553/how-do-i-remove-my-name-from-comments-and-from-the | Document Inspector/personal information removal guidance for metadata/privacy checks. |

## Verification Results

| Claim or Guidance Area | Current Manuscript/Control Treatment | Verification Result | Action |
|---|---|---|---|
| Contrast should be checked for readability and accessibility. | Units 5, 7, 9, 12 and the QA checklist teach contrast as part of presentation quality. | Supported. W3C WCAG 2.2 supports 4.5:1 normal-text and 3:1 large-text minimum contrast guidance. | Keep. |
| Color should not be the only signal in charts/visuals. | Units 5, 6, 7, appendices, and QA rows require labels/structure in addition to color. | Supported by accessibility principles in WCAG/WAI guidance and Microsoft PowerPoint accessibility guidance. | Keep. |
| Meaningful visuals need alt text or an equivalent explanation; decorative visuals can be handled differently. | Style sheet and QA rows require alt text or documented decorative status. Learner drafts discuss alt text awareness rather than technical production steps. | Supported by W3C WAI image guidance and Microsoft Office accessibility guidance. | Keep. |
| Captions or transcripts should be considered for recorded/async materials. | Units 5, 8, 9, 12 and appendices teach caption/transcript awareness. | Supported as ordinary accessibility practice; no unstable interface-specific instruction is used. | Keep. |
| PowerPoint Accessibility Checker can help find missing alt text/accessibility issues. | Control files require Word/PDF/PowerPoint accessibility checks where available; learner text does not give unstable step-by-step UI workflows. | Supported by Microsoft Support guidance. | Keep as production QA, not learner workflow. |
| Hidden comments, document properties, and metadata should be checked before sharing/exporting. | Appendices and QA rows mention metadata/hidden comments and final export metadata checks. | Supported by Microsoft Office Document Inspector guidance. | Keep. |
| Tool-neutral approach naming PowerPoint, Google Slides, Keynote, Canva, Figma Slides, Pitch, Gamma, PDFs, dashboards, and documents only as examples. | Style sheet and Unit 7 treat tools/formats as examples, not as required workflow. | No factual issue found; this is an editorial/course-scope decision rather than a technical claim. | Keep, but recheck specific tool names only if the final book makes claims about features, pricing, or availability. |
| AI should be used only for critique/checking in this textbook, not as a replacement for English development. | Style sheet and learner units frame AI as critical literacy and prohibit outsourcing final script/visuals. | This is a pedagogical policy decision aligned with the user's stated goal. It does not require external factual support unless specific AI product claims are added. | Keep. |
| Copyright/licensing caution should appear where learners use images, templates, AI outputs, or external data. | Units 5 and 7, appendices, style sheet, and QA rows include copyright/licensing/source caution. | Stable general risk guidance; no specific legal advice is given. | Keep wording general; do not add legal interpretation. |

## QA-085 Decision

QA-085 can move to `Pass` for the current Standard manuscript because the reviewed claims are either:

- supported by official/stable sources,
- explicitly framed as general caution rather than legal/technical instruction,
- or editorial/pedagogical policy choices set by the user.

Remaining source-sensitive checks after this point belong to production/export or future tool-specific additions. If later revisions add specific software feature steps, pricing, model names, accessibility tooling procedures, or legal/regulatory claims, re-run source verification for those exact claims.
