# Codex Memory Bootstrap Instructions

Bootstrap-Version: 2026-03-22T16:33:28.5113488+09:00

Scope:

- this file is the shared startup and memory bootstrap specification for Codex
- the duplicated copies are expected at `%USERPROFILE%\.codex\AGENTS.md` and `<repo-root>\AGENTS.md` when the active workspace has a repository root
- resolve Codex home from `%USERPROFILE%\.codex` unless `CODEX_HOME` is explicitly changed

## Duplication Rule

- `%USERPROFILE%\.codex\AGENTS.md` and `<repo-root>\AGENTS.md` must carry the same file contents when both files exist
- do not rewrite, summarize, or manually reconstruct one file from the other
- when one `AGENTS.md` file is missing, create it by direct file copy from the existing one
- treat differences in line endings or filesystem metadata as incidental; the instruction content itself should remain the same

## Workspace Authority And Scope

When determining the active workspace and which instructions apply, use this authority order:

1. the user's explicit statement about the current workspace or workspace switch
2. the current VS Code workspace or IDE context
3. the repository-root `AGENTS.md` for the active workspace when a repository root exists
4. the user-level `AGENTS.md` at `%USERPROFILE%\.codex\AGENTS.md`
5. shell cwd only as a fallback when the higher-priority signals are absent

Do not let stale shell cwd, prior conversation context, or injected environment metadata override the current workspace.

When the workspace changes, immediately treat prior project-scoped `AGENTS.md` files, project memory files, and assumptions from the previous workspace as out of scope.

Ask for confirmation only if the current IDE workspace itself is ambiguous.

## Startup Read Order

At session start, read:

1. `%USERPROFILE%\.codex\AGENTS.md` if it exists
2. `<repo-root>\AGENTS.md` if it exists
3. `%USERPROFILE%\.codex\memories\user-learning.md` if it exists

Then, if the active workspace has a repository root, read the repo companion files in this order when they exist:

1. `<repo-root>\user-learning-mirror.md`
2. `<repo-root>\project-learning.md`
3. `<repo-root>\project-journal.md`

Use recent journal entries by default. Read older archive segments only when needed.

## Startup Audit

In the first substantive reply of a new session or after a workspace switch, explicitly report:

- the workspace root being used
- which user-level and project `AGENTS.md` / memory files were read
- whether the repository is a git repo
- whether repo or sync status was checked
- whether project memory already existed
- whether project memory was created or updated during startup handling

Do not make startup handling implicit when the session depends on project instructions or custom memory files.

For lightweight confirmation of instruction-file reads, append CSV rows for each file read:

- use `<repo-root>\instruction-read-log.csv` when the workspace has a project memory scaffold
- otherwise use `%USERPROFILE%\.codex\memories\instruction-read-log.csv`

CSV columns:

- `timestamp_iso`
- `workspace_root`
- `scope`
- `file_path`
- `reason`

CSV encoding rule:

- `<repo-root>\instruction-read-log.csv` must be maintained as UTF-8 text
- if the existing log is not valid UTF-8 or is mixed-encoding, do not keep appending to it
- archive the old log file as-is, create a new UTF-8 `instruction-read-log.csv` with the required header, and continue logging in the new file
- when repairing the log, note the rule in bootstrap memory so the encoding issue is not silently reintroduced

## Project Bootstrap Workflow

For each newly opened project or workspace, do the following before substantive work when feasible:

1. determine whether the workspace is inside a git repository
2. if it is a git repository, inspect remotes and check whether remote updates exist for the current branch
3. if remote updates exist, prefer a non-destructive sync check first
4. only update the local branch automatically when it is a safe fast-forward and there is no conflicting local work
5. after any successful sync, re-read `AGENTS.md` files and project memory files because the instructions may have changed
6. if the workspace is not a git repository, or if no project memory files exist yet, create the standard local project memory scaffold

## Sync Safety Rules

When the workspace is a git repository:

- prefer `git fetch` and status inspection before any pull
- do not auto-merge or overwrite local work
- if the branch cannot be updated safely, continue using local instructions and report the sync constraint
- treat updated instruction or memory files as higher priority than earlier assumptions once they are read

## Standard Project Memory Scaffold

If a project or workspace does not already contain project memory files, create:

- `AGENTS.md`
- `user-learning-mirror.md`
- `project-learning.md`
- `project-journal.md`
- `instruction-read-log.csv`

Create them in one place only:

- if the workspace is inside a git repository, create them at the repository root
- if the workspace is not inside a git repository, create them at the opened workspace root
- keep the five files together in that same root location
- do not create duplicate copies in subdirectories unless a narrower nested scope is intentional and explicitly needed

Use them as follows:

- `AGENTS.md`: shared local and project startup and read-order rules
- `user-learning-mirror.md`: portable mirror of user-level memory relevant to the workspace
- `project-learning.md`: durable project memory including goals, decisions, constraints, conventions, milestones, and preferred workarounds
- `project-journal.md`: key events, stage progress, outcomes, and timeline notes
- `instruction-read-log.csv`: lightweight CSV audit trail of instruction and memory file reads

Seed new files with the current known context when possible so the first session does not start from empty notes.

## Missing-File Bootstrap

At session start, do not treat missing memory files as a reason to skip the workflow. Create the missing files immediately when they are expected for the active workspace.

Create as needed:

- `%USERPROFILE%\.codex\AGENTS.md`
- `%USERPROFILE%\.codex\memories\user-learning.md`
- `<repo-root>\AGENTS.md`
- `<repo-root>\user-learning-mirror.md`
- `<repo-root>\project-learning.md`
- `<repo-root>\project-journal.md`
- `<repo-root>\instruction-read-log.csv` with the required CSV header

Bootstrap rule for `AGENTS.md`:

- if one `AGENTS.md` copy exists and the other does not, create the missing copy by direct file copy
- if both `AGENTS.md` files are missing, create the first copy from the latest approved version-controlled bootstrap source, then direct-copy it to the second location when needed

Bootstrap rule for user-learning:

- if one of `%USERPROFILE%\.codex\memories\user-learning.md` or `<repo-root>\user-learning-mirror.md` exists and the other does not, create the missing file by direct file copy

Bootstrap rule for repo companion files:

- if `<repo-root>\project-learning.md`, `<repo-root>\project-journal.md`, or `<repo-root>\instruction-read-log.csv` is missing, create it at startup before continuing the repo-level workflow

## AGENTS Versioning And Merge

`AGENTS.md` uses versioned merge rules because source authority depends on the situation.

Version rules:

- `Bootstrap-Version` is the required version field for `AGENTS.md`
- a file with no `Bootstrap-Version` is a legacy file
- if both `AGENTS.md` files exist, do not use direct overwrite as the default behavior
- read both `AGENTS.md` copies before deciding whether bootstrap, merge, or conflict handling is required

When both `AGENTS.md` files exist:

1. if one file is legacy and the other is versioned:
   merge the legacy content into the versioned file carefully, then write the resolved result back to both files with a current `Bootstrap-Version`
2. if both files are versioned and the versions differ:
   perform a two-way merge; do not overwrite one side blindly
3. if both files are versioned, the versions match, and the contents differ:
   treat that as drift and perform a two-way merge
4. after a successful merge:
   write the merged result back to both `AGENTS.md` locations so the duplicated instruction files are identical again
5. if the merge cannot be resolved confidently:
   stop and surface the conflict instead of guessing

Merge goal for `AGENTS.md`:

- preserve one shared bootstrap specification
- preserve the current `Bootstrap-Version` or advance it intentionally as part of the resolved merge
- do not keep divergent user-level and repo-level instruction text after merge

## Discovered AGENTS Variants Outside The Active Pair

When an `AGENTS.md` file is discovered outside the active duplicated pair, handle it explicitly instead of assuming it should overwrite the current pair.

Classify the discovered file as one of:

- the user-level copy for the current machine
- the repo-root copy for the active workspace
- a narrower nested-scope workspace file that intentionally applies only below its own directory
- a stale or out-of-scope copy from another workspace, clone, or machine

Rules for discovered variants:

- do not let an out-of-scope or stale `AGENTS.md` file override the active workspace instructions
- if the discovered file belongs to a different workspace or repository, treat it as scoped to that workspace only and do not propagate it into the active pair blindly
- if the discovered file appears to be another copy of the shared bootstrap spec, compare `Bootstrap-Version` and contents before acting
- if it contains unique bootstrap rules that are still valid, merge them intentionally and then restore identical paired copies for the relevant scope
- if it is legacy or stale and contains no unique rules that should survive, replace it only after the relevant scope is confirmed
- log the discovery, classification, and resolution in the relevant project memory or user-level memory when the outcome is likely to matter again
- when scope or intended ownership is ambiguous, stop and surface the ambiguity instead of guessing

## User-Learning Mirror Sync

Canonical user-level memory uses:

- machine-local canonical file: `%USERPROFILE%\.codex\memories\user-learning.md`

Portable workspace mirror uses:

- `<repo-root>\user-learning-mirror.md`

When both files exist:

- compare them at session start
- prefer a merge over blind overwrite when both sides contain unique entries
- dual-write new cross-project lessons to both files when both are available
- merge duplicates instead of appending near-identical entries

What must be synced and where:

- cross-project user lessons belong in both `%USERPROFILE%\.codex\memories\user-learning.md` and `<repo-root>\user-learning-mirror.md`
- `%USERPROFILE%\.codex\memories\user-learning.md` is the machine-local canonical working copy
- `<repo-root>\user-learning-mirror.md` is the repo-tracked transport and mirror copy

## Repo-Tracked Memory Files

These repo files are managed for cross-device propagation through Git rather than through a second Codex-level duplication protocol:

- `<repo-root>\project-learning.md`
- `<repo-root>\project-journal.md`
- `<repo-root>\instruction-read-log.csv`

Use them as follows:

- `<repo-root>\project-learning.md` for durable project facts, goals, constraints, decisions, conventions, and milestone state
- `<repo-root>\project-journal.md` for chronological events, actions, outcomes, and follow-up notes
- `<repo-root>\instruction-read-log.csv` for startup and read audit rows only

Automatically log:

- milestone or stage starts, completions, blocks, or abandonment
- goal or scope changes
- durable decisions about tasks, content, structure, tooling, or direction
- reusable constraints, risks, dependencies, or assumptions
- rejected or replaced approaches and why

## Event Logging Rubric

When working in a project or workspace, automatically record items that clearly match any of the following:

- a stage or milestone was completed, started, blocked, or abandoned
- project goals or scope changed
- a durable decision was made about tasks, content, structure, tooling, or direction
- a reusable constraint, risk, dependency, or assumption was discovered
- an approach was rejected or replaced and the reason is likely to matter later
- a failure pattern proved repeatable and has a preferred workaround

Use `<repo-root>\project-learning.md` for lasting project facts and decisions.
Use `<repo-root>\project-journal.md` for chronological events and timeline changes.

If an event is ambiguous, use judgment and favor brevity. If the user explicitly says `log this`, record it even if it would otherwise seem minor.

## Log Growth And Segmentation

Do not treat long project memory as a single forever-growing flat log.

When project memory becomes long, prefer:

- a compact current-state file for active durable facts and decisions
- segmented journal or archive files for older chronology
- stable references or IDs that point from current notes to older relevant entries
- short summaries in current files that preserve the relevance of older history without duplicating it

Default behavior:

- always read the current user-level memory file
- always read the current project summary or state files
- read recent project journal entries by default
- read older archive segments when a current note points to them or when the task clearly requires historical detail

The goal is not to replay every past token each session. The goal is fast, accurate recall through curated current state plus addressable history.

## User-Level Memory Policy

Use `%USERPROFILE%\.codex\memories\user-learning.md` as a persistent user and environment memory file.

Record only durable items that are likely to matter again across multiple folders or projects:

- shell wrapper quirks
- recurring permission or policy constraints
- preferred command substitutions
- device or environment behaviors that are not specific to one project folder

Do not add noisy one-off notes.

Before retrying a command pattern that previously failed, check whether `user-learning.md` already documents a known failure mode and preferred alternative.

## User-Level Issue Tracking

When a user-level problem is better treated as a tracked issue than a simple lesson, record it as a typed issue entry.

Use issue-type tags such as:

- `extension`
- `editor`
- `os`
- `shell`
- `workflow`
- `hardware`
- `network`

For typed issue entries include:

- issue type tag
- affected component or extension ID when applicable
- version observed when the issue was recorded
- date first noticed
- current status such as `open`, `monitor`, `workaround`, `resolved`, or `archived`
- concise symptom or failure description
- workaround or preferred behavior
- external references such as GitHub issues, release notes, or vendor docs
- recheck triggers such as version changes, issue closure, or release-note mentions
- exit criteria for removing the workaround

For extension-related issues:

- record the extension ID and version explicitly
- if there is an upstream issue, record its URL and current status
- recheck when the extension version changes, when VS Code updates, or when the upstream issue closes
- do not keep workarounds indefinitely without a revalidation trigger

## Temporary Workaround Rules

When a user-level issue entry defines a temporary workaround with recheck triggers and exit criteria:

- follow the workaround by default while the issue remains `open`, `workaround`, or `monitor`
- revalidate only on the recorded change triggers, not on every session
- return to the normal or default behavior only after the exit criteria are satisfied

While the Windows Codex sidebar local-link issue remains unresolved:

- prefer plain string file paths for local file references in this pane
- continue to use normal clickable links for web URLs unless a separate issue says otherwise
- retire this workaround only after the tracked extension issue is fixed and local validation passes

## Entry Format

Keep entries concise and operational. For each new durable memory entry include:

- timestamp with timezone offset in ISO format
- status
- scope
- pattern or context
- what failed or what was decided
- preferred workaround or next-time behavior

Status guidance:

- use `open` or `workaround` for active unresolved problems
- use `monitor` for items that are not failing now but should be revisited on a trigger
- use `resolved` when the issue or decision no longer requires active handling
- use `archived` only after the item has been moved out of the current active memory file

Archive guidance:

- keep active or monitor items in the current memory files
- resolved items may remain in the current file while still recent or useful
- move resolved items to an archive segment when they no longer need to be in the active working set

## Portability

- resolve user-level Codex paths from `%USERPROFILE%` on each machine rather than assuming a fixed Windows username
- resolve project memory files from the active repository root rather than assuming a fixed local clone path
- treat older absolute project-path references in memory as historical snapshots unless they explicitly claim to define the current workspace root
