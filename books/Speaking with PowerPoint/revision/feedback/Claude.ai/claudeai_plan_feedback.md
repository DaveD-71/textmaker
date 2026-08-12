I read through both files carefully. Overall the consolidated list is thorough and well-sourced, and the plan has good guardrails (bounded agents, deterministic-first asset generation, no subagent file edits). But there's one significant structural gap and several smaller ones.

**The big one: the two documents don't agree on what you're actually building.**

The consolidated task list is written entirely as a revision of *the 39-page "Speaking with PowerPoint" book* — it talks about blank pages 2/3/20, PDF metadata, front/back matter, a "two-day sprint," and a "Minimum Viable 2026 Pass." It treats this as a standalone editing job on one document.

Plan.md then makes a quiet but major pivot: "Treat this as a rebuild of the existing Presentation Skills series units, not a standalone book." That's a completely different production target — tiered manuscripts (Essentials/Standard/Long) built from `units/*.json`, with its own asset register and build pipeline. Nothing in the plan explains:

- How the old book's content (Units 1–15, the Logic Tree, Sample A/B, the Ventura case) maps onto the series' existing unit structure. Agent 1 is *tasked* to produce that mapping, but the plan doesn't tell you what to do if the two structures don't line up cleanly — e.g., does "Speaking with PowerPoint" become one unit, several units, or get absorbed piecemeal?
- Whether the "two-day sprint" deadline from the task list still applies. Plan.md never mentions a timeframe at all. A 5-phase, 4-agent rebuild across three manuscript tiers is a plausibly larger job than a two-day sprint on one 39-page book — if the deadline still holds, the plan should say how it fits; if it doesn't, that's worth stating explicitly rather than dropping silently.
- Which acceptance criteria apply: the task list's per-item criteria are written against "the book" (page numbers, front matter, PDF metadata), which won't translate directly to a JSON/multi-tier build.

I'd flag this to whoever owns the project before execution starts — it's the kind of mismatch that causes rework if it's discovered mid-sprint instead of now.

**The four P0 decisions aren't actually closed.**

The task list is explicit that P0-01 through P0-04 must be decided *before* rewriting starts. Plan.md's "Default decisions" section addresses P0-04 (rename — deferred) and effectively overrides P0-02 (it's a series rebuild, not a book edit), but:

- **P0-01** (minimal Ventura update vs. full case replacement) is never decided.
- **P0-03** (explicit target-learner statement) is implied by "Japanese businesspeople" but never written as the one-sentence decision the task list calls for.

Worth pinning these down explicitly in the plan rather than leaving them for an agent to infer mid-execution.

**Other gaps worth adding:**

- **No definition of done / no rollback plan.** Nothing says what "ready to ship" means overall, and nothing mentions preserving/versioning the original book content before agents start rewriting units, in case a decision needs to be reversed.
- **No licensing check on existing assets.** The Asset Planning Agent classifies assets as keep/revise/redraw/regenerate/remove, but doesn't check whether the *existing* art (the clip art, the presenter silhouette, Sample A/B) is even licensed for reuse or modification.
- **No accessibility QA step for newly generated assets.** P1-12 requires an accessibility checklist in the content, but the Test Plan doesn't include verifying that the *deterministically generated diagrams/mockups themselves* meet contrast and color-blind-safe standards — easy to teach accessibility and still ship inaccessible diagrams.
- **No effort/time budget per phase.** The 5 Implementation Phases and 4 agents have no time allocation, so there's no way to check the plan against a deadline (see point above) or catch scope creep early.
- **The Day 1/Day 2 sprint plan and the 5-phase implementation plan are never merged.** Right now you have two different sequences of steps from two different documents, and it's not clear which one an executor actually follows on the day.

**Smaller things:** the plan doesn't say how many rounds of Claude.ai/ChatGPT external review are expected in QA (Phase 5), or what a "pass" looks like from that review; and P2-08/P2-04's Japan-specific ESL content isn't explicitly assigned to one of the four agents (it would fall to Pedagogy/QA Agent, but that's not stated).
