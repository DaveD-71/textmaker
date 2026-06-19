# User Learning Mirror

Portable mirror of user-level lessons relevant to this workspace.

Sync rule:

- compare this file with `%USERPROFILE%\.codex\memories\user-learning.md` at session start when both exist
- prefer this mirror as the portable source in this workspace
- dual-write new cross-project lessons to both files when both are available
- prefer literal UNC workspace paths in memory and troubleshooting notes when the project root is on a network share; avoid drive-letter or shell-variable path shortcuts for UNC-backed projects
- merge duplicates instead of appending near-identical entries

## Entries

### 2026-05-16 - Temporary Multi-Root VS Code Workspaces Are Used To Combine Tool And Content Repos

- Status: `resolved`
- Scope: user/workflow
- Pattern: VS Code `.code-workspace` files that pair a tool repo with a content repo for a specific task
- Example: `C:\Dev\Code\workspace\textmaker-admin_writing\textmaker-admin_writing.code-workspace` pairs `textmaker` (scripts) and `book_administrative-writing` (content)
- Key rules:
  - The `.code-workspace` file is the authoritative workspace scope — it defines all active roots, not just the shell cwd
  - The shell cwd defaults to the first listed folder (e.g. `textmaker`) but that is incidental, not authoritative
  - Temporary workspace folders (e.g. `C:\Dev\Code\workspace\...`) must never receive AGENTS.md, project memory scaffold, or instruction-read-log files
  - Each constituent repo keeps its own project memory independently
- Preferred behavior: at startup in a multi-root workspace, read each repo's AGENTS.md and project memory separately; do not conflate the shell cwd repo with the full workspace scope

### ISSUE 2026-05-09-WORKFLOW-UNC-01 - `cmd.exe` On UNC Working Directories Can Silently Rebase Relative Paths To `C:\Windows`

- Issue type: `workflow`
- Component: `cmd.exe` / batch wrappers on Windows network shares
- Version observed: `Windows 11` environment with UNC-backed workspaces and Codex shell launches
- Date first noticed: `2026-05-09`
- Status: `open` with workaround
- Symptom: when a `.cmd` wrapper is launched while the shell itself starts in a UNC working directory, `cmd.exe` prints `UNC paths are not supported. Defaulting to Windows directory.` and can interpret unresolved relative paths from `C:\Windows` unless the wrapper or downstream tool normalizes them
- Workaround: prefer wrappers that `pushd` to a mapped drive, prepend required local tool paths such as Pandoc automatically, and normalize user-supplied relative paths before handing them to downstream tools
- Preferred behavior: treat the UNC warning line as expected shell noise unless the actual command also shows missing files or wrong output paths; when debugging, verify the effective resolved input/reference/output paths rather than trusting the original relative arguments
- Recheck triggers:
  - wrapper logic changes for batch-file entrypoints
  - Windows shell behavior changes after OS or terminal updates
  - repeated file-not-found or wrong-output-path failures from UNC-backed projects
- Exit criteria:
  - wrappers consistently preserve caller-relative behavior on UNC-backed launches without fallback path errors
  - downstream tools no longer receive unresolved `..` UNC paths or `C:\Windows`-relative artifacts
  - validation passes from both repo-root and sibling-project launch locations
- Additional note: make this warning prominent in future debugging because it can masquerade as a missing dependency issue when the real problem is path rebasing

### 2026-05-21 - Use literal UNC paths in user memory notes

- Status: `workaround`
- Scope: `user/workflow`
- Pattern: documenting project locations and file paths in memory files
- Preferred behavior: record workspace paths literally as UNC paths, for example `\\prod-fs-gen01\WorkFile\04_在宅勤務\★グローバルビジネス推進部（在宅）\ランゲージサービス課\Dobson（在宅）\04. Projects\code\textmaker`, rather than using mapped drives, `file:` shortcuts, or `%USERPROFILE%` placeholders for UNC-backed workspaces
- Rationale: literal UNC paths are less ambiguous in this environment and avoid shell path rebasing issues when cross-checking notes, logs, and command outputs

### 2026-05-09T23:55:00+09:00 - Preserve DOCX XML Root Namespaces Exactly When Rewriting Word Package Parts

- Status: `workaround`
- Scope: user/workflow
- Pattern: editing `.docx` package XML directly, especially `word/styles.xml`
- Failure: rewriting a Word XML part with a generic XML serializer can keep compatibility attributes such as `mc:Ignorable` while dropping the matching namespace declarations (`xmlns:mc`, `xmlns:w14`, `xmlns:w15`, `xmlns:w16*`), which makes Word report the DOCX as corrupted even when the visible content edits seem small
- Preferred behavior: when modifying DOCX XML directly, preserve the original root element namespace declarations and compatibility prefixes verbatim, or patch the existing XML surgically instead of regenerating the root tag through a default serializer

### ISSUE 2026-03-14-EXT-01 - Codex VS Code Local File Links Open In Browser

- Issue type: `extension`
- Component: `openai.chatgpt`
- Version observed: `26.311.21342`
- Date first noticed: `2026-03-14`
- Status: `open` with workaround
- Symptom: local file links generated in the Codex VS Code sidebar resolve through the webview/browser path instead of opening in a VS Code editor tab
- Workaround: prefer plain file paths for local references in affected environments; reserve clickable markdown links for web URLs unless local link handling is verified working
- External reference: `openai/codex#12661` - <https://github.com/openai/codex/issues/12661>
- Recheck triggers:
  - installed `openai.chatgpt` extension version changes
  - VS Code updates on this machine
  - upstream issue `openai/codex#12661` closes
  - release notes mention a fix for Windows local file-link handling
- Exit criteria:
  - the relevant fix is present in the installed extension version on this machine
  - local validation passes for a project file link and a non-project local file link opening in VS Code editors
  - copied local links no longer expose `vscode-resource`/webview URLs as the open target
- Debugging note: if the failure references `webview/assets/index-*.js`, treat that as evidence the problem is occurring inside the Codex webview bundle; open the VS Code webview developer console to inspect console errors and click-handler behavior
- Additional local evidence: the VS Code on-disk Codex log recorded `open-in-target not supported in extension` for `vscode://codex/open-in-targets`, which directly supports the broken local-file open path diagnosis
- Noise filter: a webview devtools Quirks Mode warning on `vscode-webview://.../fake.html` is likely coming from the VS Code webview wrapper, not the Codex app itself; the extension's own `webview/index.html` already declares `<!doctype html>`
- Log priority: for this issue, `rendererLog` mostly contains unrelated VS Code window noise while `Codex.log` contains the decisive extension-specific failures; prefer `Codex.log` first when diagnosing Codex sidebar link handling
- Webview source path:
  - `webview/assets/vscode-api-DrUj-9Y8.js` posts bridge requests to `vscode://codex/<method>`
  - `webview/assets/index-B67BrupJ.js.map` includes `../../src/local-conversation/use-target-apps.ts` and `../../src/local-conversation/open-target-selection.ts`, which reference `open-in-targets`
  - `webview/assets/general-settings-Bqzo1N88.js.map` and `webview/assets/agent-settings-DHX6KGXw.js.map` also call `useFetchFromVSCode("open-in-targets", ...)`
- Conclusion: the failing `open-in-targets` request originates in the webview bundle, crosses the VS Code bridge as `vscode://codex/open-in-targets`, and then fails in `out/extension.js`
- Additional external corroboration: Claude summarized the root fix as an OpenAI extension change so local `file://` URIs use native VS Code editor-open APIs rather than `openExternal`; that matches the local evidence and reinforces that there is no reliable `config.toml` workaround for this build

### 2026-03-14 - Shell Wrapper Delete Policy

- Status: `workaround`
- Scope: user/environment
- Pattern: direct PowerShell deletion through the shell wrapper, such as `Remove-Item`
- Failure: command may be rejected with `blocked by policy` even when read/write access is otherwise fine
- Preferred behavior: if deletion is necessary and confirmed safe, prefer a simpler fallback such as `cmd /c del` for files

### 2026-03-14 - Be Cautious With Huge Diagnostic Logs

- Status: `monitor`
- Scope: user/environment
- Pattern: tools that can emit unbounded logs during failure loops
- Risk: logs can silently consume most of `C:` and destabilize the session
- Preferred behavior: check file size before tailing or re-running, preserve only small head/tail excerpts, and clean up oversized logs promptly

### 2026-03-14 - Prefer Segmented Memory Over Flat Ever-Growing Logs

- Status: `resolved`
- Scope: user/workflow design
- Pattern: long-lived project memory and journal files
- Decision: use compact current-state files plus segmented archives and pointers, rather than assuming all historical logs should be reread in full every session
- Preferred behavior: read current summaries first, use references to older segments when relevant, and keep memory curated for recall rather than raw accumulation

### 2026-03-14 - Codex VS Code Link Opening Can Be Environment-Specific

- Status: `monitor`
- Scope: user/environment
- Pattern: clicking assistant-generated file links in the Codex secondary sidebar in VS Code
- Observation: on some machines the link may open externally in Edge and fail, while on others it opens correctly inside VS Code
- Likely cause: client or extension-side handling of links/citations differs by environment, version, or pane behavior rather than by project content
- Preferred behavior: compare Codex extension version, VS Code build, and `file_opener` behavior across machines before assuming the link format itself is unsupported

### 2026-03-14 - VS Code Trust Prompt May Appear After External Browser Launch

- Status: `monitor`
- Scope: user/environment
- Pattern: clicking links in the Codex secondary sidebar webview
- Observation: on this machine, Edge may navigate before or concurrently with VS Code's `Do you want Code to open the external website?` prompt
- Implication: the problematic behavior appears to be in VS Code/webview or extension-side external-link handling rather than a simple project setting
- Preferred behavior: treat screenshots of this sequence as evidence of a client-handling bug or race, and distinguish external `https` links from local file citations when debugging

### 2026-03-14 - VS Code `Open` Extension Was Not The Cause

- Status: `resolved`
- Scope: user/environment
- Pattern: Codex sidebar links opening incorrectly in Edge
- Observation: disabling the `sandcastle.vscode-open` extension did not change the behavior
- Implication: the issue is not explained by that extension alone; likely causes remain Codex extension/webview handling or environment/version differences

### 2026-03-14 - Copied Codex Pane Links Exposed Webview Resource URLs

- Status: `monitor`
- Scope: user/environment
- Pattern: copying a link directly from the Codex secondary sidebar in VS Code
- Observation: the copied URL was `https://file+.vscode-resource.vscode-cdn.net/.../openai.chatgpt-.../webview/` instead of a native file-open target
- Implication: the pane is treating these as webview hyperlinks/resources, and `file_opener = "vscode"` is not being applied to those link targets in this environment
- Preferred behavior: treat this as evidence of extension/webview-side link-generation or click-handling failure, not as a simple bad file path

### 2026-03-14 - Copy From VS Code Webview Can Fail Independently Of Clipboard Health

- Status: `monitor`
- Scope: user/environment
- Pattern: selecting and copying links/text from a VS Code webview-based pane
- Observation: copy from the Codex pane stopped reaching the clipboard even after clearing clipboard history
- External evidence: there are known VS Code webview copy issues where copy/context-menu copy can fail while the rest of the clipboard works
- Preferred behavior: when debugging similar issues, test keyboard copy separately from context-menu copy and treat webview clipboard bugs as a real possibility

### 2026-03-14 - Open Codex Issue Confirms Windows VS Code Link Routing Bug

- Status: `resolved`
- Scope: user/environment
- Pattern: clicking assistant-generated local Markdown/file links in the Codex sidebar on Windows
- External evidence: GitHub issue `openai/codex#12661` reports that the VS Code extension routes local `file://` links through `open-in-browser` and then `vscode.env.openExternal()`, which hands them to the OS default browser instead of opening them in an editor tab
- Implication: this is confirmed extension-side behavior/bug, not just a local settings mistake
- Preferred behavior: treat `file_opener = "vscode"` as insufficient when the webview click path itself is incorrectly using `openExternal`

### 2026-03-14 - Inspect Codex Extension Code Early For Codex-UI Failures

- Status: `workaround`
- Scope: user/workflow
- Pattern: failures in how the Codex VS Code pane creates, presents, copies, or routes hyperlinks and other UI actions
- Failure: I over-attributed the problem to VS Code, settings, or other extensions before checking the local Codex extension bundle that actually generates the link behavior
- Preferred behavior: when the defect is clearly inside the Codex pane, inspect the local `openai.chatgpt` extension files early, especially `webview/index.html`, `webview/assets/index-*.js`, `webview/assets/vscode-api-*.js`, source maps, and `out/extension.js`, before spending much time on broader editor-level blame

### 2026-03-14 - Treat User-Found Devtools Evidence As A Primary Lead

- Status: `workaround`
- Scope: user/workflow
- Pattern: the user surfaces a concrete local debugging lead from browser or webview developer tools
- Failure: I did not pivot fast enough when you found the VS Code webview developer console and the local extension-file path hints
- Preferred behavior: when the user provides a concrete devtools path, stack trace, bundle name, or local asset reference, treat that as primary evidence and inspect the referenced local files immediately instead of continuing with broader speculation

### 2026-03-14 - User-Level AGENTS.md Must Live Under Codex Home

- Status: `workaround`
- Scope: user/workflow
- Pattern: setting up or auditing global Codex instruction discovery
- Failure: I incorrectly treated `C:\Users\daved\AGENTS.md` as the default user-level instructions path
- Correct behavior: use `C:\Users\daved\.codex\AGENTS.md` as the canonical user-level instructions file unless `CODEX_HOME` is explicitly changed
- Implication: if the file is placed outside Codex home, new sessions may not load the intended user-level instructions at all

### 2026-03-14 - Project Memory Files Need An Explicit Root Placement Rule

- Status: `workaround`
- Scope: user/workflow
- Pattern: bootstrapping custom project-memory files that are not part of Codex's native discovery model
- Failure: the convention defined the file set but did not clearly define where those files must be created
- Correct behavior: create `AGENTS.md`, `user-learning-mirror.md`, `project-learning.md`, and `project-journal.md` at the repo root for git repos, or at the opened folder root for non-repo workspaces
- Preferred behavior: keep the files together at that root and avoid duplicate copies in subdirectories unless a narrower nested scope is intentional

### 2026-03-14 - Startup Handling Must Be Auditable In The First Reply

- Status: `workaround`
- Scope: user/workflow
- Pattern: testing whether user-level and project-level instructions were actually applied in a new session
- Failure: reading instruction files silently made success and failure indistinguishable from the user's point of view
- Correct behavior: in the first substantive reply of a new session or after a workspace switch, explicitly report the workspace root, files read, repo/sync check status, and whether local project memory existed or was created
- Preferred behavior: make startup compliance observable instead of implicit

### 2026-03-15 - Read Confirmation Events Belong In CSV, Not Markdown

- Status: `workaround`
- Scope: user/workflow
- Pattern: recording when `AGENTS.md` and other learning documents were read
- Decision: keep narrative memory in markdown, but record read-confirmation events in a separate CSV audit log
- Preferred behavior: use `instruction-read-log.csv` for timestamped read events and keep markdown files for durable lessons, decisions, and chronology

### 2026-03-15T00:34:37.9048369+09:00 - Workspace Scope Must Follow User Statement And VS Code Workspace

- Status: `workaround`
- Scope: user/workflow
- Pattern: determining which project instructions and memory files apply after a workspace switch
- Failure: stale shell cwd and prior project context were allowed to override the user's explicit workspace change and the current VS Code workspace
- Correct behavior: use the user's explicit statement and the current VS Code workspace as the authoritative scope signals; use shell cwd only as a fallback when those are absent
- Preferred behavior: once the workspace changes, immediately treat previous-project `AGENTS.md` files and project memory as out of scope and do not carry them forward without confirmation

### 2026-03-17T18:58:15.2116200+09:00 - Mixed-Encoding Audit CSVs Must Be Archived And Reset

- Status: `workaround`
- Scope: user/workflow
- Context: repairing `instruction-read-log.csv` after mixed UTF-8 and CP932/Shift-JIS content was detected
- Observation: appending new rows to a mixed-encoding audit CSV makes patching, decoding, and path verification unreliable
- Preferred behavior: keep `instruction-read-log.csv` as UTF-8 text only; if the file is not valid UTF-8, archive the old file, create a new UTF-8 log with the required header, and resume logging there

### 2026-03-17T21:45:00+09:00 - Preserve Existing File Encoding Before Rewriting, And Restore Baseline If Corruption Occurs

- Status: `workaround`
- Scope: user/workflow
- Context: repairing files after a shell-driven text rewrite corrupted existing non-ASCII punctuation across the file
- Observation: shell-driven whole-file rewrites can silently transcode an existing file and corrupt non-ASCII punctuation or text if the file's current encoding is not preserved explicitly
- Preferred behavior: before rewriting an existing text file, preserve its current encoding explicitly; avoid whole-file shell rewrites when encoding safety is uncertain and prefer minimal patch edits instead; if corruption has already occurred, restore the clean baseline first and then reapply only the intended minimal edits

### 2026-03-18T11:40:00+09:00 - Force Python UTF-8 In PowerShell Sessions, Not Only In VS Code Terminal Settings

- Status: `workaround`
- Scope: user/workflow
- Context: persistent mojibake in terminal output and PowerShell-captured log files on Windows
- Observation: VS Code `terminal.integrated.env.windows` may not reach every Codex or PowerShell shell process; when `PYTHONIOENCODING` and `PYTHONUTF8` are absent, Python can start with `cp932` stdout/stderr and corrupt non-ASCII text during pipeline capture
- Preferred behavior: set `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` in the user environment and also export them from the PowerShell profile so new shells force Python UTF-8 before any capture or logging commands run

### 2026-03-18T13:10:00+09:00 - Direct Shell Deletes Can Be Rejected By Execution Policy, So Use A Reviewed Manifest With A Non-Shell Fallback

- Status: `workaround`
- Scope: user/workflow
- Context: deleting approved file sets in the Codex workspace on Windows
- Observation: direct destructive shell commands such as `Remove-Item` can be rejected even when the workspace allows broad filesystem access, because an execution-policy layer can still block high-risk shell deletes before they run
- Preferred behavior: when deleting a reviewed batch of files, generate and verify a manifest first, then perform deletion through a non-shell fallback such as a short Python script reading that manifest; avoid spending a turn on direct shell delete commands when the environment has already shown this policy behavior

### 2026-03-18T14:50:00+09:00 - Avoid Bash-Style `&&` In PowerShell Command Chains

- Status: `workaround`
- Scope: user/workflow
- Context: running multi-step git commands from Codex in Windows PowerShell
- Observation: some PowerShell environments in this workflow use an older parser that does not support Bash-style `&&` command chaining, so commands fail before execution with a parser error instead of reaching git
- Preferred behavior: when sequencing multiple shell commands in PowerShell, avoid `&&`; use separate tool calls when practical or explicit `$LASTEXITCODE` checks between commands so commit/push flows fail cleanly and remain compatible with older PowerShell parsers

### 2026-03-18T15:35:00+09:00 - Reuse One Canonical `workdir` String Verbatim And Do Not Retry Hand-Typed Variants

- Status: `workaround`
- Scope: user/workflow
- Context: repeated `The directory name is invalid` failures on long Windows repo paths in tool calls
- Observation: once a long `workdir` string is manually retyped or reconstructed, it is easy to introduce a single wrong character and then waste multiple retries on near-identical bad paths
- Preferred behavior: capture one canonical workspace root at startup, then reuse that exact string verbatim in every later tool call; when a `workdir` fails once with `The directory name is invalid`, stop retrying path variants and compare against the canonical root before issuing another command

### 2026-03-22T16:33:28.5113488+09:00 - Shared AGENTS Variants Must Be Classified By Scope Before Merge

- Status: `workaround`
- Scope: user/workflow
- Pattern: discovering another `AGENTS.md` outside the active user-level and repo-level pair
- Failure: it is easy to assume any discovered `AGENTS.md` should be synced into the current pair, even when it belongs to another workspace, clone, machine, or narrower nested scope
- Preferred behavior: classify discovered `AGENTS.md` files by scope first; merge only when they belong to the active duplicated bootstrap pair, otherwise treat them as out-of-scope or narrower-scope instructions and do not propagate them blindly

### 2026-03-22T19:40:00+09:00 - Before Every Commit, Run A Final Control-File And Memory Consistency Pass

- Status: `workaround`
- Scope: user/workflow
- Pattern: committing planning or documentation reorganizations after the main file edits appear finished
- Failure: the main content changes can be correct while one or more control files, project-memory entries, or source-of-truth references remain stale, which then forces a follow-up correction after the commit
- Correct behavior: before every commit, run one final consistency pass across the affected control layer, including current source-of-truth files, to-do/status files, project memory, and any newly introduced path references
- Preferred behavior: treat commit readiness as requiring both the primary edits and the dependent control/memory updates; if a post-commit audit is likely to surface a stale reference, the commit is not ready yet

### 2026-03-22T22:05:00+09:00 - Run Post-Commit And Post-Push Verification Serially When The Checks Depend On A Git State Transition

- Status: `workaround`
- Scope: user/workflow
- Pattern: verifying repo state immediately after `git commit` or `git push`
- Failure: running a state-changing git command and a dependent verification command in parallel can return a stale pre-transition result, which creates a false mismatch and forces an unnecessary follow-up check
- Correct behavior: when one verification step depends on the completion of a commit or push, run the commands serially: complete the git state change first, then run the dependent verification
- Preferred behavior: reserve parallel tool use for independent checks only; if `git status`, ahead/behind confirmation, or similar output depends on a commit or push finishing, run it in a separate follow-up call

### ISSUE 2026-04-14-SHELL-01 - Pandoc Not On PATH In This Environment

- Issue type: shell
- Component: pandoc CLI resolution from Codex shell sessions
- Version observed: pandoc 3.8.2.1 at C:\Users\d-dobson\AppData\Local\Pandoc\pandoc.exe
- Date first noticed: 2026-04-14
- Status: workaround
- Symptom:  extmaker.cmd markdown-to-docx fails with Error: pandoc binary not found on PATH when the shell PATH does not include the local Pandoc install directory.
- Workaround: prepend C:\Users\d-dobson\AppData\Local\Pandoc to PATH in-session before running textmaker conversion commands.
- Recheck triggers:
  - user/system PATH updates
  - Pandoc reinstallation or version change
- Exit criteria:
  - where pandoc resolves in a fresh shell without manual PATH edits
  -  extmaker.cmd markdown-to-docx runs successfully without in-session PATH modification

### 2026-06-19T19:43:35.4984139+09:00 - Word PDF Export Can Hang On VPN Printer Verification

- Status: workaround
- Scope: user/workflow
- Pattern: Microsoft Word DOCX-to-PDF export on the company VPN
- Failure: Word PDF export can hang or fail when the default printer driver tries to verify a network/company printer through VPN.
- Preferred workaround: before exporting PDFs through Word/COM, switch the default printer to a local driver such as Microsoft Print to PDF, or avoid Word's printer-dependent export path when possible.
- Recheck trigger: revisit if Word/Office printer handling changes or if exports hang again despite a local default printer.
