# Codex Correction Prompt — Step 11 Duplicate Requirements Blocks
## Project: *Administrative Writing, Advanced*

---

## Background

During Step 11 implementation, JPO scenario variants were correctly inserted into E (Freer Writing) sections as option 4. However, because the original prompt was insertion-only, the existing generic requirements block that followed the scenario list was preserved below the newly inserted JPO requirements block. This created a duplicate "Your [x] must include" block in six units.

This prompt authorises the deletion of those duplicate blocks. It is a **deletion-only** pass. No other content should be added, moved, or modified.

---

## Source files

All deletions are in the output files from the previous step:

- `md/revised_modules_step13/admin-writing-adv_mod2_revised.md`
- `md/revised_modules_step13/admin-writing-adv_mod3_revised.md`
- `md/revised_modules_step13/admin-writing-adv_mod4_revised.md`

No changes to `mod1`, `mod5`, or `mod6`.

---

## Deliverables

Edit the three files in place (or write corrected versions to a new folder `md/revised_modules_step13b` — your choice). The corrected files must be a complete, valid replacement for the previous output set.

---

## IMPORTANT: What is NOT a duplicate

Before deleting, note the following units where two requirements blocks are **correct** and should **not** be touched:

- **Unit 12 (mod4):** The E3 section contains two separate tasks — the original role-based task and the JPO "Alternatively" variant. Each has its own "Your inquiry must include" block. This is intentional. Do not delete either block.
- **Unit 17 (mod5):** No duplicate block exists. Do not touch this file.
- **Units 19 and 21 (mod6):** No duplicate blocks exist. Do not touch this file.

---

## Deletions

Each deletion is described with an exact string anchor. Delete the block that begins at the anchor and ends as indicated. The surrounding content (what comes immediately before and immediately after) is shown for verification.

---

### Deletion 1 — Unit 4, mod2

**What comes before (keep):**
```
- a next-step statement
```

**Delete this block exactly:**
```

Your email must include:

- a clear opening and statement of purpose
- an explanation of the relevant issue
- at least two distinct requests
- a next-step statement
- a diplomatic closing
```

**What comes after (keep):**
```

---

#### F1. Peer Review
```

---

### Deletion 2 — Unit 6, mod2

**What comes before (keep):**
```
- a next-step statement
```

**Delete this block exactly:**
```

Your message must include:

- diplomatic framing throughout
- specific references to sections, terms, or documents
- a neutral explanation of the issue
- an impact statement
- a clear correction request
- a next-step statement
```

**What comes after (keep):**
```

---

#### F1. Peer Review
```

---

### Deletion 3 — Unit 7, mod2

**What comes before (keep):**
```
- a next-step statement
```

**Delete this block exactly:**
```

Your message must include:

- three to four sequenced requests
- clear dependency logic between at least two of the requests
- a stated rationale for the sequence
- diplomatic phrasing throughout
- a next-step statement
```

**What comes after (keep):**
```

---

#### F1. Peer Review
```

---

### Deletion 4 — Unit 11, mod3

**What comes before (keep):**
```
**Word count: 200–230 words**
```

**Delete this block exactly:**
```

Your summary must include:

- all four sections: Overview, Key Points Discussed, Decisions / Action Items, Next Steps
- at least three bullet points in the Key Points section
- specific, attributed action items where relevant
- clear, formal, neutral tone

**Word count: 200–230 words**
```

**What comes after (keep):**
```

---

### F. Review & Self-Edit
```

---

### Deletion 5 — Unit 13, mod4

**What comes before (keep):**
```
- analytical, objective tone
```

**Delete this block exactly:**
```

Your assessment must include:

- 2–3 clearly identified risks
- causes and impacts for each
- mitigation proposals
- analytical, objective tone

**Word count: 180–220 words**
```

**What comes after (keep):**
```

---
```

---

### Deletion 6 — Unit 15, mod4

**What comes before (keep):**
```
- neutral, formal tone
```

**Delete this block exactly:**
```

Your rationale must include:

- a clear recommendation
- alignment with existing policy or guidelines
- objective reasoning and evidence of the problem
- benefits of the proposed change
- neutral, formal tone

**Word count: 180–220 words**
```

**What comes after (keep):**
```

---
```

---

## Verification checklist

After completing all deletions, confirm the following.

- [ ] Unit 4 (mod2): E section has exactly one "Your email must include" block — the JPO one, with five bullets ending in "a next-step statement"
- [ ] Unit 6 (mod2): E section has exactly one "Your message must include" block — the JPO one, with five bullets ending in "a next-step statement"
- [ ] Unit 7 (mod2): E section has exactly one "Your message must include" block — the JPO one, with five bullets ending in "a next-step statement"
- [ ] Unit 11 (mod3): E section has exactly one "Your summary must include" block and exactly one "Word count: 200–230 words" line
- [ ] Unit 13 (mod4): E section has exactly one "Your assessment must include" block and exactly one "Word count: 180–220 words" line
- [ ] Unit 15 (mod4): E section has exactly one "Your rationale must include" block and exactly one "Word count: 180–220 words" line
- [ ] Unit 12 (mod4): E3 section still has two requirements blocks (original task + JPO alternative) — both intact
- [ ] Unit 17 (mod5): E section unchanged
- [ ] mod1, mod5, mod6: files unchanged
- [ ] No other content has been removed from any file
- [ ] All files are valid Markdown with no broken separators or missing blank lines around headings
