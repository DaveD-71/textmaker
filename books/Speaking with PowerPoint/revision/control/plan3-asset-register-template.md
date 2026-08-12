# Plan 3 Asset Register Template

Prepared: 2026-08-12

Purpose: define the required asset-register schema for the Plan 3 rebuild before creating, reusing, or approving final visuals. This template exists because Phase 6 QA requires asset-level evidence, not just a list of image prompts.

## Register Policy

Every final asset used in Essentials, Standard, or Long must appear in an asset register before release.

Assets include:
- generated illustrations
- edited/generated mockups
- charts
- diagrams
- icons
- screenshots
- photos
- extracted legacy images reused from the old textbook
- decorative visual elements if they appear in final output

Do not reuse existing `books/Presentation Skills/images/` assets for Plan 3 unless they are rechecked against this schema and approved for the new course.

## Required Fields

| Field | Required | Description |
|---|---|---|
| `asset_id` | Yes | Stable unique ID, e.g. `p3-u05-visual-hierarchy-01` |
| `asset_title` | Yes | Human-readable title |
| `file_path` | Yes | Final or planned repository path |
| `asset_type` | Yes | `diagram`, `chart`, `icon`, `mockup`, `screenshot`, `photo`, `illustration`, `decorative`, `other` |
| `status` | Yes | `planned`, `draft`, `approved`, `repair`, `rejected`, `deferred` |
| `tier_use` | Yes | `Essentials`, `Standard`, `Long`, or combined use |
| `unit_use` | Yes | Unit number/name, appendix model, front matter, or teacher notes |
| `source` | Yes | `original`, `OpenAI generated`, `PIL/editable generated`, `legacy textbook extract`, `third-party`, `screenshot`, or other |
| `source_detail` | Yes | Prompt file, source file, URL, generation note, or source explanation |
| `license_status` | Yes | Usage status and any restriction |
| `generated_or_original` | Yes | `generated`, `original`, `reused`, `edited`, `third-party` |
| `alt_text` | Yes, unless decorative | Concise functional alt text |
| `decorative` | Yes | `yes` or `no` |
| `caption` | If needed | Learner-facing caption or figure label |
| `replacement_rationale` | Yes | Why this asset exists or replaces an old one |
| `accessibility_check` | Yes | Contrast/readability/color/alt-text outcome |
| `visual_restriction_check` | Yes | Finance/trading, government-symbol, logo, privacy, and representation checks |
| `privacy_security_check` | Yes | Confirms no confidential, client, account, trade, or real personal data |
| `text_accuracy_check` | If asset contains text | Confirms text is correct, readable, and intentional |
| `element_count_check` | If diagram/process | Confirms count/order of boxes, icons, arrows, labels, etc. |
| `background_check` | If transparent or generated | Confirms no unwanted background artifact or ghosting |
| `approved_by` | Yes before release | Owner or reviewer approving final use |
| `approval_date` | Yes before release | Date approved |
| `repair_or_defer_note` | If not approved | Required for `repair`, `rejected`, or `deferred` status |
| `recheck_status` | If repaired | Result after repair |

## Markdown Register Row Template

Use this table format if the register is maintained in Markdown.

| Asset ID | Title | Type | Status | Tier/Unit Use | File Path | Source | License Status | Alt Text / Decorative | Caption | Key Checks | Approved By | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  | planned |  |  |  |  |  |  |  |  |  |

## JSON Object Template

Use this object shape if the register is maintained as JSON.

```json
{
  "asset_id": "",
  "asset_title": "",
  "file_path": "",
  "asset_type": "",
  "status": "planned",
  "tier_use": [],
  "unit_use": [],
  "source": "",
  "source_detail": "",
  "license_status": "",
  "generated_or_original": "",
  "alt_text": "",
  "decorative": false,
  "caption": "",
  "replacement_rationale": "",
  "accessibility_check": {
    "contrast_checked": "",
    "readability_checked": "",
    "color_not_alone_checked": "",
    "chart_label_checked": "",
    "notes": ""
  },
  "visual_restriction_check": {
    "finance_trading_clear": "",
    "government_symbols_clear": "",
    "logos_watermarks_clear": "",
    "representation_checked": "",
    "notes": ""
  },
  "privacy_security_check": {
    "no_real_client_data": "",
    "no_account_or_trade_ids": "",
    "no_real_personal_data": "",
    "metadata_checked": "",
    "notes": ""
  },
  "generated_image_check": {
    "text_accuracy": "",
    "element_count": "",
    "label_placement": "",
    "stray_text": "",
    "background_artifacts": "",
    "repair_or_regenerate_decision": ""
  },
  "approved_by": "",
  "approval_date": "",
  "repair_or_defer_note": "",
  "recheck_status": ""
}
```

## Required Checks by Asset Type

| Asset Type | Required Checks |
|---|---|
| Chart | source/fictional-data label, takeaway title, readable labels, color-not-alone, no misleading scale |
| Diagram/process | element count, arrow direction, label placement, readable text, color-not-alone |
| Icon | clear meaning, consistent style, no logo resemblance, alt/decorative decision |
| Mockup/dashboard | fictional/sanitized data, no real client/account/trade/person identifiers, no proprietary UI, readable labels |
| Screenshot | current, permission-cleared, no confidential data, no unstable UI dependency unless necessary |
| Illustration/photo | representation check, no logos/watermarks, no flags/seals/crests, no accidental text |
| Decorative element | decorative flag, no required meaning, no distracting or misleading symbolism |

## Finance/Trading Restrictions

Business-client finance/trading visuals must not contain:

- real firm names
- bank logos
- exchange names
- ticker symbols
- real client names
- account numbers
- trade IDs
- proprietary screens
- market predictions
- trade recommendations
- investment advice
- compliance/legal advice

Preferred finance/trading visuals:

- generic workflow diagrams
- reporting dashboards with fictional labels
- process charts
- before/after operational metrics
- service-quality or inquiry-volume charts
- control/escalation flow diagrams

## Government-Agency Restrictions

Government-agency visuals must not contain real or country-specific:

- national flags
- seals
- emblems
- crests
- official insignia
- political campaign symbols
- party symbols
- patriotic color schemes that imply a specific country

Preferred government-agency visuals:

- plain administrative offices
- meeting rooms
- counters
- forms
- workflow diagrams
- service-delivery diagrams
- internal reporting visuals

Avoid vague civic/government prompt wording that may cause generated imagery to default to another country's symbols.

## Accessibility Checks

Minimum asset accessibility checks:

- Meaningful image has alt text.
- Decorative image is marked decorative.
- Text is readable at final output size.
- Contrast target is checked where text/background colors matter.
- Color is not the only signal.
- Charts have labels and takeaway titles.
- Complex visuals have captions or surrounding explanation.
- Async/recorded visuals have caption/transcript awareness if used in recorded tasks.

Contrast target: aim for WCAG 2.2 AA, at least 4.5:1 for normal text and 3:1 for large text where practical.

## Generated Image Checks

Generated images must be visually inspected before approval.

Check:
- correct subject
- correct composition
- correct number of people/objects/boxes/arrows
- no broken hands/faces or distracting artifacts
- no accidental readable text
- no misspelled labels
- no logos or watermarks
- no prohibited flags/seals/crests
- Japanese/East Asian representation where people are shown for Japan-based learner material
- transparent-background quality where applicable

If only text, labels, counts, or simple layout are wrong, prefer editable/PIL repair over another paid generation call when practical.

## Approval Workflow

1. Add asset as `planned`.
2. Record source and intended unit/tier use.
3. Create or collect draft asset.
4. Complete accessibility, restriction, privacy/security, and generated-image checks.
5. Mark `repair` if any required check fails.
6. Repair or regenerate only when there is a confirmed defect.
7. Recheck repaired asset.
8. Mark `approved` only when all required fields and checks are complete.

## Open Decision

Before asset production begins, decide whether Plan 3 will:

1. update `books/Presentation Skills/images/image_register.json`, or
2. create a new Plan 3-specific asset register, such as `books/Speaking with PowerPoint/plan3-asset-register.md` or `books/Presentation Skills/images/plan3_image_register.json`.

Recommendation: create a Plan 3-specific register first, then merge into the final `books/Presentation Skills/images/` register only when the final source location is settled.
