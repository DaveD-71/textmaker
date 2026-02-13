# Situations YAML Export Requirements

This document captures the current requirements for generating and maintaining `Situations_all.yaml` from the DOCM source, so the output can be replicated consistently.

## Source of Truth
- Input: `Situations - All.docm`
- Output: `Situations_all.yaml`
- Schema: `situations_schema_1.0.yml`

## Output Structure (Schema 1.0)
Top-level:
- `schema_version: 1.0`
- `situations:` map keyed by situation code (e.g., `H01`)

Each map entry:
- `<code>:`
  - `details`:
    - `cefr` (CEFR level, e.g., A2)
    - `function`:
      - `en`, `ja` (first line of Purpose & Objectives)
    - `purpose_objectives`:
      - `en`, `ja` (remaining lines of Purpose & Objectives)
  - `instructions`:
    - `roleplays`: list of 2 items
      - `id` (1 or 2)
      - `prompt.en`, `prompt.ja`
    - `writing_task`:
      - `prompt.en`, `prompt.ja`
  - `language`:
    - `roleplay_1`:
      - `key_expressions`: list of entries
        - `function.en`, `function.ja`
        - `example` (string)
      - `target_vocabulary`: list of `{term, cefr}`
      - `model.dialogue` (multiline string)
    - `writing_task`:
      - `key_expressions`: list of entries
        - `function.en`, `function.ja`
        - `example` (string)
      - `target_vocabulary`: list of `{term, cefr}`
      - `model.text` (multiline string)

## Parsing Rules
1. **Situation boundaries**
   - New situation starts at `Heading2` containing `SITUATION <ID>`.
   - Extract `code` from `SITUATION <ID>`.
   - Extract `cefr` from the same heading (A1–C2).

2. **Purpose & Objectives**
   - First EN line → `details.function.en`.
   - First JA line → `details.function.ja`.
   - Remaining EN lines → `details.purpose_objectives.en`.
   - Remaining JA lines → `details.purpose_objectives.ja`.

3. **Roleplays / Writing Task**
   - `Roleplay 1` and `Roleplay 2` each map to `instructions.roleplays` (id 1/2).
   - `Writing Task` maps to `instructions.writing_task.prompt`.

4. **Key Expressions**
   - Two Key Expressions blocks per situation:
     - First → `language.roleplay_1.key_expressions`
     - Second → `language.writing_task.key_expressions`
   - Each Key Expression entry:
     - Function header (`English / Japanese`) → `function.en`, `function.ja`
     - Each quoted example line → `example`
     - Strip wrapping quotes from examples.

5. **Target Vocabulary**
   - Two Target Vocabulary blocks per situation:
     - First → `language.roleplay_1.target_vocabulary`
     - Second → `language.writing_task.target_vocabulary`
   - Parse `term (CEFR)` into `{term, cefr}`.

6. **Models**
   - `Roleplay 1 Model` → `language.roleplay_1.model.dialogue`.
     - Use dialogue lines as-is, but prefix roles as `S:` and `T:`.
   - `Writing Task Model` → `language.writing_task.model.text`.
     - Include `Subject:` line if present; otherwise omit.

## Text Normalization Rules
1. **Remove mid-sentence line breaks**
   - Join lines unless:
     - Previous line ends with punctuation (`. ! ? ; : , …` and JP equivalents), or
     - Next line is part of a list.

2. **Lists**
   - Convert list items to dash-prefixed lines (`- `) when:
     - The line already begins with a list marker (`-`, `*`, `1.`, `a)`), or
     - The previous line ends with `:` or full-width `\uFF1A` (Japanese colon `：`).

3. **Quotes**
   - Strip wrapping quotes around Key Expression examples.

4. **Line spacing**
   - Collapse multiple blank lines into a single line break.
   - No blank lines between vocabulary terms.

## YAML Formatting
- `language.roleplay_1.model.dialogue` must be a literal block scalar (`|`).
- `language.writing_task.model.text` must be a literal block scalar (`|`).
- `instructions.writing_task.prompt.en/ja` must be literal block scalars (`|`).
- Use wide line width to avoid automatic wrapping for plain scalars.
- Keep schema-style blank lines:
  - Blank line after `cefr`.
  - Blank line before `function`, `purpose_objectives`, `instructions`, `writing_task`, `language`, `target_vocabulary`, `model`.
  - Blank line between each situation.

## Validation Checks
- 60 situations expected.
- All situations contain EN + JA for:
  - `details.function`
  - `details.purpose_objectives`
  - `instructions.roleplays[*].prompt`
  - `instructions.writing_task.prompt`
- Empty `Subject:` lines are allowed if absent in DOCM.

## Output File
- `Situations_all.yaml`

