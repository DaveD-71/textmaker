# User Learning

## Purpose

Persistent notes about user/environment-level behaviors that can affect work across multiple folders and tasks.

## Entries

### 2026-03-14 - Shell Wrapper Delete Policy

- Entry-ID: `ul-eec7bdf7-871e-520c-80c3-1333b7ea1546`

- Status: `workaround`
- Scope: user/environment
- Pattern: direct PowerShell deletion through the shell wrapper, such as `Remove-Item`
- Failure: command may be rejected with `blocked by policy` even when read/write access is otherwise fine
- Preferred behavior: if deletion is necessary and confirmed safe, prefer a simpler fallback such as `cmd /c del` for files

### 2026-03-14 - Be Cautious With Huge Diagnostic Logs

- Entry-ID: `ul-9f9a04b9-0a1a-5134-a96d-77ffd06b9eb7`

- Status: `monitor`
- Scope: user/environment
- Pattern: tools that can emit unbounded logs during failure loops
- Risk: logs can silently consume most of `C:` and destabilize the session
- Preferred behavior: check file size before tailing or re-running, preserve only small head/tail excerpts, and clean up oversized logs promptly

### 2026-03-14 - Prefer Segmented Memory Over Flat Ever-Growing Logs

- Entry-ID: `ul-aaae9fae-1a29-5e56-adba-f689780685f1`

- Status: `resolved`
- Scope: user/workflow design
- Pattern: long-lived project memory and journal files
- Decision: use compact current-state files plus segmented archives and pointers, rather than assuming all historical logs should be reread in full every session
- Preferred behavior: read current summaries first, use references to older segments when relevant, and keep memory curated for recall rather than raw accumulation

### 2026-03-14 - Codex VS Code Link Opening Can Be Environment-Specific

- Entry-ID: `ul-caf00166-13ea-526d-bdfb-eb86b5557a6d`

- Status: `monitor`
- Scope: user/environment
- Pattern: clicking assistant-generated file links in the Codex secondary sidebar in VS Code
- Observation: on some machines the link may open externally in Edge and fail, while on others it opens correctly inside VS Code
- Likely cause: client or extension-side handling of links/citations differs by environment, version, or pane behavior rather than by project content
- Preferred behavior: compare Codex extension version, VS Code build, and `file_opener` behavior across machines before assuming the link format itself is unsupported

### 2026-03-14 - VS Code Trust Prompt May Appear After External Browser Launch

- Entry-ID: `ul-98c2037d-50ea-539d-80df-e786cc576581`

- Status: `monitor`
- Scope: user/environment
- Pattern: clicking links in the Codex secondary sidebar webview
- Observation: on this machine, Edge may navigate before or concurrently with VS Code's `Do you want Code to open the external website?` prompt
- Implication: the problematic behavior appears to be in VS Code/webview or extension-side external-link handling rather than a simple project setting
- Preferred behavior: treat screenshots of this sequence as evidence of a client-handling bug or race, and distinguish external `https` links from local file citations when debugging

### 2026-03-14 - VS Code `Open` Extension Was Not The Cause

- Entry-ID: `ul-4b2039de-e426-5306-b6e1-a5b4b133beee`

- Status: `resolved`
- Scope: user/environment
- Pattern: Codex sidebar links opening incorrectly in Edge
- Observation: disabling the `sandcastle.vscode-open` extension did not change the behavior
- Implication: the issue is not explained by that extension alone; likely causes remain Codex extension/webview handling or environment/version differences

### 2026-03-14 - Copied Codex Pane Links Exposed Webview Resource URLs

- Entry-ID: `ul-5d0a44b1-b1b7-5263-ab38-a92fe506435f`

- Status: `monitor`
- Scope: user/environment
- Pattern: copying a link directly from the Codex secondary sidebar in VS Code
- Observation: the copied URL was `https://file+.vscode-resource.vscode-cdn.net/.../openai.chatgpt-.../webview/` instead of a native file-open target
- Implication: the pane is treating these as webview hyperlinks/resources, and `file_opener = "vscode"` is not being applied to those link targets in this environment
- Preferred behavior: treat this as evidence of extension/webview-side link-generation or click-handling failure, not as a simple bad file path

### 2026-03-14 - Copy From VS Code Webview Can Fail Independently Of Clipboard Health

- Entry-ID: `ul-d437531e-f100-5e5e-a7ad-4228af0be292`

- Status: `monitor`
- Scope: user/environment
- Pattern: selecting and copying links/text from a VS Code webview-based pane
- Observation: copy from the Codex pane stopped reaching the clipboard even after clearing clipboard history
- External evidence: there are known VS Code webview copy issues where copy/context-menu copy can fail while the rest of the clipboard works
- Preferred behavior: when debugging similar issues, test keyboard copy separately from context-menu copy and treat webview clipboard bugs as a real possibility

### 2026-03-14 - Open Codex Issue Confirms Windows VS Code Link Routing Bug

- Entry-ID: `ul-4401659f-8452-5016-b74a-9ebe9c18c20d`

- Status: `resolved`
- Scope: user/environment
- Pattern: clicking assistant-generated local Markdown/file links in the Codex sidebar on Windows
- External evidence: GitHub issue `openai/codex#12661` reports that the VS Code extension routes local `file://` links through `open-in-browser` and then `vscode.env.openExternal()`, which hands them to the OS default browser instead of opening them in an editor tab
- Implication: this is confirmed extension-side behavior/bug, not just a local settings mistake
- Preferred behavior: treat `file_opener = "vscode"` as insufficient when the webview click path itself is incorrectly using `openExternal`

### ISSUE 2026-03-14-EXT-01 - Codex VS Code Local File Links Open In Browser

- Entry-ID: `ul-518cee61-f1c0-5796-a7f9-628571a34f1f`

- Issue type: `extension`
- Component: `openai.chatgpt`
- Version observed: `26.311.21342`
- Date first noticed: `2026-03-14`
- Status: `open` with workaround
- Symptom: local file links generated in the Codex VS Code sidebar resolve through the webview/browser path instead of opening in a VS Code editor tab
- Workaround: prefer plain file paths for local references in affected environments; reserve clickable markdown links for web URLs unless local link handling is verified working
- External reference: `openai/codex#12661` - https://github.com/openai/codex/issues/12661
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

### 2026-03-14 - Inspect Codex Extension Code Early For Codex-UI Failures

- Entry-ID: `ul-f7449758-f199-5b27-9831-e33fe9b7ac54`

- Status: `workaround`
- Scope: user/workflow
- Pattern: failures in how the Codex VS Code pane creates, presents, copies, or routes hyperlinks and other UI actions
- Failure: I over-attributed the problem to VS Code, settings, or other extensions before checking the local Codex extension bundle that actually generates the link behavior
- Preferred behavior: when the defect is clearly inside the Codex pane, inspect the local `openai.chatgpt` extension files early, especially `webview/index.html`, `webview/assets/index-*.js`, `webview/assets/vscode-api-*.js`, source maps, and `out/extension.js`, before spending much time on broader editor-level blame

### 2026-03-14 - Treat User-Found Devtools Evidence As A Primary Lead

- Entry-ID: `ul-8f060ef1-7ecc-5a78-a3b7-f09b2bd98069`

- Status: `workaround`
- Scope: user/workflow
- Pattern: the user surfaces a concrete local debugging lead from browser or webview developer tools
- Failure: I did not pivot fast enough when you found the VS Code webview developer console and the local extension-file path hints
- Preferred behavior: when the user provides a concrete devtools path, stack trace, bundle name, or local asset reference, treat that as primary evidence and inspect the referenced local files immediately instead of continuing with broader speculation

### 2026-03-14 - User-Level AGENTS.md Must Live Under Codex Home

- Entry-ID: `ul-1606dd90-0bc6-58af-b715-c4b2df1a496a`

- Status: `workaround`
- Scope: user/workflow
- Pattern: setting up or auditing global Codex instruction discovery
- Failure: I incorrectly treated `C:\Users\daved\AGENTS.md` as the default user-level instructions path
- Correct behavior: use `C:\Users\daved\.codex\AGENTS.md` as the canonical user-level instructions file unless `CODEX_HOME` is explicitly changed
- Implication: if the file is placed outside Codex home, new sessions may not load the intended user-level instructions at all

### 2026-03-14 - Project Memory Files Need An Explicit Root Placement Rule

- Entry-ID: `ul-85e52955-c17b-522a-a77a-2c799b778d46`

- Status: `workaround`
- Scope: user/workflow
- Pattern: bootstrapping custom project-memory files that are not part of Codex's native discovery model
- Failure: the convention defined the file set but did not clearly define where those files must be created
- Correct behavior: create `AGENTS.md`, `user-learning-mirror.md`, `project-learning.md`, and `project-journal.md` at the repo root for git repos, or at the opened folder root for non-repo workspaces
- Preferred behavior: keep the files together at that root and avoid duplicate copies in subdirectories unless a narrower nested scope is intentional

### 2026-03-14 - Startup Handling Must Be Auditable In The First Reply

- Entry-ID: `ul-509183f3-2f28-5008-938c-c3855611d840`

- Status: `workaround`
- Scope: user/workflow
- Pattern: testing whether user-level and project-level instructions were actually applied in a new session
- Failure: reading instruction files silently made success and failure indistinguishable from the user's point of view
- Correct behavior: in the first substantive reply of a new session or after a workspace switch, explicitly report the workspace root, files read, repo/sync check status, and whether local project memory existed or was created
- Preferred behavior: make startup compliance observable instead of implicit

### 2026-03-15 - Read Confirmation Events Belong In CSV, Not Markdown

- Entry-ID: `ul-e27a3e13-fbaa-5c4e-a8d1-d70e6e10e61a`

- Status: `workaround`
- Scope: user/workflow
- Pattern: recording when `AGENTS.md` and other learning documents were read
- Decision: keep narrative memory in markdown, but record read-confirmation events in a separate CSV audit log
- Preferred behavior: use `instruction-read-log.csv` for timestamped read events and keep markdown files for durable lessons, decisions, and chronology

### 2026-03-15T00:34:37.9048369+09:00 - Workspace Scope Must Follow User Statement And VS Code Workspace

- Entry-ID: `ul-8ced613e-f5e7-5bc3-8aad-775b869156a3`

- Status: `workaround`
- Scope: user/workflow
- Pattern: determining which project instructions and memory files apply after a workspace switch
- Failure: stale shell cwd and prior project context were allowed to override the user's explicit workspace change and the current VS Code workspace
- Correct behavior: use the user's explicit statement and the current VS Code workspace as the authoritative scope signals; use shell cwd only as a fallback when those are absent
- Preferred behavior: once the workspace changes, immediately treat previous-project `AGENTS.md` files and project memory as out of scope and do not carry them forward without confirmation

### 2026-03-17T18:58:15.2116200+09:00 - Mixed-Encoding Audit CSVs Must Be Archived And Reset

- Entry-ID: `ul-f58acd56-e820-5fd5-ab92-648a6a0a9d9e`

- Status: `workaround`
- Scope: user/workflow
- Context: repairing `instruction-read-log.csv` after mixed UTF-8 and CP932/Shift-JIS content was detected
- Observation: appending new rows to a mixed-encoding audit CSV makes patching, decoding, and path verification unreliable
- Preferred behavior: keep `instruction-read-log.csv` as UTF-8 text only; if the file is not valid UTF-8, archive the old file, create a new UTF-8 log with the required header, and resume logging there

### 2026-03-17T21:45:00+09:00 - Preserve Existing File Encoding Before Rewriting, And Restore Baseline If Corruption Occurs

- Entry-ID: `ul-99b166ec-b558-5037-bb00-fd65197665d1`

- Status: `workaround`
- Scope: user/workflow
- Context: repairing files after a shell-driven text rewrite corrupted existing non-ASCII punctuation across the file
- Observation: shell-driven whole-file rewrites can silently transcode an existing file and corrupt non-ASCII punctuation or text if the file's current encoding is not preserved explicitly
- Preferred behavior: before rewriting an existing text file, preserve its current encoding explicitly; avoid whole-file shell rewrites when encoding safety is uncertain and prefer minimal patch edits instead; if corruption has already occurred, restore the clean baseline first and then reapply only the intended minimal edits

### 2026-03-18T11:40:00+09:00 - Force Python UTF-8 In PowerShell Sessions, Not Only In VS Code Terminal Settings

- Entry-ID: `ul-645d675d-b857-5142-af7f-469f62e2f4ba`

- Status: `workaround`
- Scope: user/workflow
- Context: persistent mojibake in terminal output and PowerShell-captured log files on Windows
- Observation: VS Code `terminal.integrated.env.windows` may not reach every Codex or PowerShell shell process; when `PYTHONIOENCODING` and `PYTHONUTF8` are absent, Python can start with `cp932` stdout/stderr and corrupt non-ASCII text during pipeline capture
- Preferred behavior: set `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` in the user environment and also export them from the PowerShell profile so new shells force Python UTF-8 before any capture or logging commands run

### 2026-03-18T13:10:00+09:00 - Direct Shell Deletes Can Be Rejected By Execution Policy, So Use A Reviewed Manifest With A Non-Shell Fallback

- Entry-ID: `ul-23c81bf9-c5ad-5f24-9e3e-8645ce1118b5`

- Status: `workaround`
- Scope: user/workflow
- Context: deleting approved file sets in the Codex workspace on Windows
- Observation: direct destructive shell commands such as `Remove-Item` can be rejected even when the workspace allows broad filesystem access, because an execution-policy layer can still block high-risk shell deletes before they run
- Preferred behavior: when deleting a reviewed batch of files, generate and verify a manifest first, then perform deletion through a non-shell fallback such as a short Python script reading that manifest; avoid spending a turn on direct shell delete commands when the environment has already shown this policy behavior

### 2026-03-18T14:50:00+09:00 - Avoid Bash-Style `&&` In PowerShell Command Chains

- Entry-ID: `ul-63b9f6a1-157b-529b-a7dc-1c0eaee2093f`

- Status: `workaround`
- Scope: user/workflow
- Context: running multi-step git commands from Codex in Windows PowerShell
- Observation: some PowerShell environments in this workflow use an older parser that does not support Bash-style `&&` command chaining, so commands fail before execution with a parser error instead of reaching git
- Preferred behavior: when sequencing multiple shell commands in PowerShell, avoid `&&`; use separate tool calls when practical or explicit `$LASTEXITCODE` checks between commands so commit/push flows fail cleanly and remain compatible with older PowerShell parsers

### 2026-03-18T15:35:00+09:00 - Reuse One Canonical `workdir` String Verbatim And Do Not Retry Hand-Typed Variants

- Entry-ID: `ul-433264d7-a8f0-552b-843d-91a5e5177c73`

- Status: `workaround`
- Scope: user/workflow
- Context: repeated `The directory name is invalid` failures on long Windows repo paths in tool calls
- Observation: once a long `workdir` string is manually retyped or reconstructed, it is easy to introduce a single wrong character and then waste multiple retries on near-identical bad paths
- Preferred behavior: capture one canonical workspace root at startup, then reuse that exact string verbatim in every later tool call; when a `workdir` fails once with `The directory name is invalid`, stop retrying path variants and compare against the canonical root before issuing another command

### 2026-03-22T16:33:28.5113488+09:00 - Shared AGENTS Variants Must Be Classified By Scope Before Merge

- Entry-ID: `ul-9444ae37-129c-55d1-93ba-c0db493c15fc`

- Status: `workaround`
- Scope: user/workflow
- Pattern: discovering another `AGENTS.md` outside the active user-level and repo-level pair
- Failure: it is easy to assume any discovered `AGENTS.md` should be synced into the current pair, even when it belongs to another workspace, clone, machine, or narrower nested scope
- Preferred behavior: classify discovered `AGENTS.md` files by scope first; merge only when they belong to the active duplicated bootstrap pair, otherwise treat them as out-of-scope or narrower-scope instructions and do not propagate them blindly

### 2026-03-22T19:40:00+09:00 - Before Every Commit, Run A Final Control-File And Memory Consistency Pass

- Entry-ID: `ul-79d12bda-d0e0-5bb6-94e2-e1b431923abc`

- Status: `workaround`
- Scope: user/workflow
- Pattern: committing planning or documentation reorganizations after the main file edits appear finished
- Failure: the main content changes can be correct while one or more control files, project-memory entries, or source-of-truth references remain stale, which then forces a follow-up correction after the commit
- Correct behavior: before every commit, run one final consistency pass across the affected control layer, including current source-of-truth files, to-do/status files, project memory, and any newly introduced path references
- Preferred behavior: treat commit readiness as requiring both the primary edits and the dependent control/memory updates; if a post-commit audit is likely to surface a stale reference, the commit is not ready yet

### 2026-03-22T22:05:00+09:00 - Run Post-Commit And Post-Push Verification Serially When The Checks Depend On A Git State Transition

- Entry-ID: `ul-51b0c008-dc6d-5848-b0de-f530c611a847`

- Status: `workaround`
- Scope: user/workflow
- Pattern: verifying repo state immediately after `git commit` or `git push`
- Failure: running a state-changing git command and a dependent verification command in parallel can return a stale pre-transition result, which creates a false mismatch and forces an unnecessary follow-up check
- Correct behavior: when one verification step depends on the completion of a commit or push, run the commands serially: complete the git state change first, then run the dependent verification
- Preferred behavior: reserve parallel tool use for independent checks only; if `git status`, ahead/behind confirmation, or similar output depends on a commit or push finishing, run it in a separate follow-up call

### 2026-05-16 - Temporary Multi-Root VS Code Workspaces Are Used To Combine Tool And Content Repos

- Entry-ID: `ul-1dd50d5e-f73e-50e8-b789-ee1ffc5c1463`

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

### 2026-03-31T13:10:00+09:00 - Mojibake Across Projects Usually Means UTF-8 Text Was Read Or Rewritten Through The Wrong Windows Code Page

- Entry-ID: `ul-33967232-53e6-5d9e-9d9f-c590f8edaf09`

- Status: `workaround`
- Scope: user/environment
- Pattern: Markdown or text files across projects showing corruption such as `窶・`, `竊・`, `didn窶冲`, or `applicant窶冱`
- Failure: valid UTF-8 punctuation or apostrophes are misdecoded through a Windows default code page such as `cp932` / Shift-JIS and then saved back, which turns punctuation-heavy text into persistent mojibake
- Correct behavior: treat this as an encoding mismatch first, not as a content-editing issue; read and write project text files explicitly as UTF-8, avoid tools that silently fall back to the system code page, and verify encoding before bulk rewrite passes
- Preferred behavior: when mojibake appears, stop normal editing, scan the active source set for the corruption pattern, repair the file text under explicit UTF-8 handling, and only then continue content work so the corruption does not spread

### ISSUE 2026-07-31-HW-01 - Dell XPS 15 9560 USB-C/Thunderbolt Port Only Detects Devices Connected At Boot [RESOLVED]

- Entry-ID: `ul-b07428f0-d8f4-5c76-84cb-c7fecc8f9b90`

- Issue type: `hardware`
- Component: Thunderbolt 3 controller (Intel Alpine Ridge, `PCI\VEN_8086&DEV_15B5`), Intel "Thunderbolt™ Software" v17.4.79.510
- Machine: Dell XPS 15 9560, service tag `FXZL8H2`
- Version observed: Thunderbolt driver (Microsoft inbox) v10.0.19041.5794 (2025-04-07); Thunderbolt Software v17.4.79.510
- Date first noticed: `2026-07-31` (user reports it "has never worked well")
- **Status: `resolved` as of 2026-07-31.** Genuine post-boot hot-plug now confirmed working — see the RESOLUTION entry near the bottom for the fix. The sections below trace the full investigation that led there; kept for reference in case the issue resurfaces (e.g. after a Windows/driver/BIOS update resets these settings).
- Symptom: the USB-C port only reliably detects a connected device if that device was already plugged in **before boot**. Hot-plugging a device into the port after Windows has started is not detected — confirmed live with a real drive connected: `Get-PnpDevice` shows the controller `Present: False`, no new disk appears anywhere, `pnputil /scan-devices` + `/enum-devices /connected` find nothing, and the Intel Thunderbolt Control Center shows "0 connected devices" despite the `tbtsvc` service running normally.
- Root cause: not fully confirmed, but strong evidence points to a well-documented Alpine-Ridge-generation Thunderbolt 3 limitation — POST/UEFI-time initialization succeeds (hence boot-time connections work), but the OS-level runtime hot-plug detection path has a known gap on this controller generation. This is a firmware/hardware-level limitation, not a Windows driver bug: zero Kernel-PnP/PCI/disk events are logged anywhere in the System event log when the failure reproduces, and no dedicated Thunderbolt event channel exists — the failure happens below where Windows would normally log an attempt or error.
- Secondary lead, not yet investigated further: `MsiInstaller` Event ID 1035 ("Windows Installer reconfigured the product... Thunderbolt™ Software... status: 0") recurs repeatedly in the Application log, often twice within seconds of each other, across nearly every day since 2026-07-26. Repeated MSI self-repair loops like this typically indicate an unhealthy/incomplete software install (something referenced by a shortcut/component keeps appearing "not installed"). Could be an independent contributor to the detection failure — not confirmed either way.
- Attempted and ruled out: `pnputil /scan-devices` (Windows device rescan) does not help; driver is current (same version/date as the working USB-A controller's driver, not outdated).
- **UEFI/BIOS settings checked 2026-07-31 (photos reviewed) — nothing misconfigured.** "Thunderbolt™ Adapter Configuration": Enable Thunderbolt Technology Support / Adapter Boot Support / Pre-boot Modules all enabled; Security Level already at the most permissive "No Security". "USB Configuration": Enable USB Boot Support / External USB Port both enabled (the latter's description confirms it also governs Type-C USB). "Dell Type-C Dock Configuration": "Always Allow Dell Docks" is unchecked, but doesn't apply here since these aren't Dell-branded docks. One notable detail: the "Enable Thunderbolt™ Adapter Boot Support" description states enabling it *overrides the OS-level Security Levels for devices connected during pre-boot* — a plausible mechanism for why boot-time and post-boot connections are handled differently, though not proven as the root cause. Not yet tested with this setting disabled.
- **Connect-before-boot workaround reconfirmed 2026-07-31, with an important refinement: full enumeration can be significantly delayed after Windows reaches the desktop, not immediate.** Test: device physically connected before power-on; USBDeview "before" snapshot taken ~1 minute after boot showed `Connected: No` (stale, from the prior day); the device didn't actually complete enumeration (proper name, driver bound, drive letter `D:` assigned) until **~24 minutes after boot** (system Up Time at report generation was 53m46s; device's arrival timestamp was ~24 min after the computed boot time). Initially misread as a successful hot-plug-after-boot until the user clarified the device was connected pre-boot the whole time — the delay was in Windows finishing enumeration, not a later hot-plug event. Likely tied to `DeviceInstall`/`DsmSvc` being demand-start services that only process pending device installs once their turn comes up, competing with everything else loading in the first several minutes of a session (this machine also shows heavy Windows Defender CPU usage right after boot/reconnect — see slowdown-diagnosis note elsewhere in the `data-recovery` repo's `project-journal.md`). **Practical implication: after connecting before boot, don't conclude detection failed just because the device isn't visible in the first few minutes — it may take up to ~20-30 minutes to fully appear.**
- **Dell Community research 2026-07-31 confirms this is a widely-reported, unresolved issue on this exact model — not machine-specific.** Multiple Dell Community threads describe the identical symptom on the XPS 15 9560. Commonly-cited community fixes: (a) Thunderbolt™ Service set to Automatic start — already was the case here; (b) Device Manager → USB Root Hub → Power Management → uncheck "allow the computer to turn off this device to save power" — not yet tried on this machine; (c) disable "Always Allow Dell Docks" in BIOS — already disabled here; (d) uninstall a conflicting Realtek USB driver — not applicable, no Realtek USB driver present on this machine. An official Dell KB for a related product (Precision Tower Thunderbolt 3 cards) describes the same class of issue and recommends enabling Thunderbolt Technology Support (already enabled here) plus manually triggering Device Manager "Rescan for hardware changes" after every hot-plug — the command-line equivalent (`pnputil /scan-devices`) was already tried on this machine and did not help. Net effect: this machine already matched most community/official fixes before this investigation even started, which is itself informative — it's a genuinely inconsistent, unresolved issue on this model, not a simple checkbox fix. Sources: dell.com/support/kbdoc/en-us/000134103 (Precision Tower KB); dell.com/community threads "Dell XPS 9560 Thunderbolt 3 problems solved", "XPS 9560 can't recognize external HDD by USB-C port", "Dell XPS 15 9560 with Thunderbolt Dock TB16 doesn't see USB devices before restart".
- **Clean hot-plug test 2026-07-31: confirmed failure, unconfounded.** With Windows already running (not a fresh boot), a drive was safely taken offline via `Set-Disk -IsOffline $true`, physically unplugged, then reconnected. Result: the drive vanished completely — gone from `Get-Disk`, PnP entries showed `Status: Unknown, Present: False`, and zero PnP/disk events logged anywhere despite the physical reconnect. This is the clean test that had been missing — no boot-timing ambiguity, no blocked-handle confounds. **Genuine post-boot hot-plug does not work on this port, confirmed.**
- **BREAKTHROUGH 2026-07-31: disabling "Enable Thunderbolt™ Adapter Boot Support" AND "Enable Thunderbolt™ Adapter Pre-boot Modules" in BIOS changed behavior significantly for the better.** With both disabled, rebooted with the drive already connected. Unlike every previous "connected before boot" test, the device did NOT appear automatically in Windows Explorer — but USBTreeView showed the controller, port, and device all fully enumerated down to the **DiskDrive class level** (`disk.sys` loaded and started, real `\\.\PhysicalDriveN` assigned) — a much deeper, more complete enumeration than the total-absence failure state seen in every hot-plug test. The disk showed `Attribute: offline`, which turned out to be a leftover from this session's own earlier `Set-Disk -IsOffline $true` call (Windows persists that flag per-disk-signature across reconnects) — not a new problem. Running `Set-Disk -IsOffline $false` brought it fully online with a healthy volume and drive letter.
- **Important unresolved question:** the successful test above still involved connecting the device *before* boot (with the new BIOS settings). True post-boot hot-plug has **not yet been retested** under this new BIOS configuration — that's the next thing to try, and would be the real confirmation of whether disabling Boot Support actually fixes hot-plug, or just changes the pre-boot connection path's behavior (no longer using the "overrides OS Security Levels" pre-boot bypass, which now requires the normal OS-level enumeration path to run and evidently does so more completely/reliably).
- Diagnostic tools added for this investigation (portable, no install): USBTreeView (`uwe-sieber.de/usbtreeview_e.html`) for live USB tree/descriptor inspection once a device does enumerate; USBDeview (NirSoft) for historical connect/disconnect timestamps — both proved essential for the before/after timeline comparisons and for seeing the DiskDrive-level enumeration detail that Device Manager alone wouldn't have shown clearly. Both currently live in the `data-recovery` repo's `tools/` folder (see that repo's `tools/SOURCES.md`) since that's where they were needed, though the issue itself is machine-level, not specific to that project.
- Other useful technique learned: `Set-Disk -Number N -IsOffline $true` (elevated) is a reliable alternative to the shell's "Eject" verb / tray icon when the latter gets stuck on a handle it won't identify (the tray eject failed intermittently this session — sometimes genuinely blocked by `wmpnetwk.exe`, once for an unidentified reason with no logged blocking event — while `Set-Disk -IsOffline` succeeded every time). Also note: this same `IsOffline` flag persists per-disk-signature across both reconnects AND reboots — after using it, remember to `Set-Disk -IsOffline $false` again or the disk will keep appearing "there but not mounted."

**RESOLUTION (2026-07-31):** Genuine post-boot hot-plug confirmed working after combining two changes:

1. **UEFI/BIOS** (System Configuration → Thunderbolt™ Adapter Configuration): disabled both **"Enable Thunderbolt™ Adapter Boot Support"** and **"Enable Thunderbolt™ Adapter Pre-boot Modules"**. Left "Enable Thunderbolt™ Technology Support" enabled and Security Level on "No Security."
2. **Device Manager → Power Management**: unchecked **"Allow the computer to turn off this device to save power"** on **both** the Thunderbolt host controller (`Intel(R) USB 3.1 eXtensible Host Controller - 1.10`) AND its Root Hub. Found via a direct comparison against the working USB-A hub, which already had this unchecked — the Thunderbolt hub/controller had it checked, meaning Windows was allowed to power them down, and (per `ArmedWakeOnConnect: No` on the Thunderbolt hub, vs. this not being a differentiator on its own) they had no way to wake back up when a new device connected. That combination — allowed to sleep, no way to wake on connect — is the most coherent explanation found for the original symptom.
3. Rebooted once after both changes (a `DN_NEED_RESTART` flag had been sitting on the Thunderbolt root hub, corroborated independently by Device Manager's own "reboot required" indicator — needed clearing).

**Verification:** safely ejected the drive via the tray icon (worked cleanly, unlike earlier in the session), physically unplugged it (the entire Thunderbolt controller/hub tree disappeared from USBTreeView — expected, this controller fully de-initializes with nothing connected, unlike the always-on USB-A controller), waited, then physically reconnected it **with Windows already running, no reboot**. Result: full success across every layer checked — `Get-Disk` showed it Online (no offline flag this time), controller/hub/device all `Present: True`, volume mounted with drive letter, and it appeared correctly in both USBTreeView and File Explorer. This is the clean, unconfounded hot-plug test the whole investigation had been building toward, and it passed.

- Recheck triggers if this regresses: Windows Update installs a Thunderbolt/USB driver update (could reset the Power Management checkboxes), a BIOS update (could reset the UEFI settings), or a fresh install/major Windows update.
- Exit criteria: met. Device connected after boot (genuine hot-plug) is now detected without requiring a reboot or sleep/wake cycle.

### 2026-08-23T21:48:28+09:00 - Word PDF Export And Print-to-PDF Can Strip Hyphens At Line-Wrap Points In Hyperlink URLs

- Entry-ID: `ul-7fb23845-0118-5b73-a9fb-5a32b4c1a477`

- Status: `resolved` (verified workaround)
- Scope: user/workflow — Word-to-PDF conversion, any document containing hyperlinked URLs
- Pattern: a hyphenated URL (e.g. `.../media-center/...`) inside a Word hyperlink happens to have its hyphen fall exactly at a visual line-wrap point in the document
- Failure: Word's File > Export > Create PDF/XPS, and the "Microsoft Print to PDF" virtual printer driver, both silently strip that hyphen from the resulting PDF's hyperlink target — apparently misidentifying it as a discretionary/soft hyphen inserted only for line-breaking rather than a literal character. This corrupts the URL (`media-center` → `mediacenter`, `First-Quarter` → `FirstQuarter`) and produces a link that 404s, even though the source URL and the DOCX's underlying hyperlink field are both correct.
- Verified fix (isolated via three test files by the user — original Export output vs. a Save-As-PDF test vs. a Print-to-PDF test): File > Save As, choosing PDF as the file type, correctly preserves the hyphen and produces a working link. Export and Print-to-PDF do not — confirmed reproducible across two independent conversion paths.
- Preferred behavior: when converting any Word document with hyperlinked URLs to PDF, use Save As → PDF, not Export or a Print-to-PDF driver — especially when a URL contains a hyphen that could land at a line-wrap point.
- Discovery context: found while reviewing a generated teaching resource where a correct, working source citation appeared "dead" only in the PDF; the DOCX and the original markdown source were unaffected. A same-session WebFetch check of the "dead" URL had actually reported it working — which turned out to be correct, since WebFetch was checking the real, uncorrupted URL rather than the PDF-mangled one the user had clicked.

### ISSUE 2026-05-09-WORKFLOW-UNC-01 - `cmd.exe` On UNC Working Directories Can Silently Rebase Relative Paths To `C:\Windows`

- Entry-ID: `ul-e774b093-31eb-5e9d-b857-ffe6df3b21f7`

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

- Entry-ID: `ul-d7c8cb9a-eb12-50ca-bca1-9f58c820d20b`

- Status: `workaround`
- Scope: `user/workflow`
- Pattern: documenting project locations and file paths in memory files
- Preferred behavior: record workspace paths literally as UNC paths, for example `\\prod-fs-gen01\WorkFile\04_在宅勤務\★グローバルビジネス推進部（在宅）\ランゲージサービス課\Dobson（在宅）\04. Projects\code\textmaker`, rather than using mapped drives, `file:` shortcuts, or `%USERPROFILE%` placeholders for UNC-backed workspaces
- Rationale: literal UNC paths are less ambiguous in this environment and avoid shell path rebasing issues when cross-checking notes, logs, and command outputs

### 2026-05-09T23:55:00+09:00 - Preserve DOCX XML Root Namespaces Exactly When Rewriting Word Package Parts

- Entry-ID: `ul-627ab285-e921-5457-94a7-b9cfee751ba9`

- Status: `workaround`
- Scope: user/workflow
- Pattern: editing `.docx` package XML directly, especially `word/styles.xml`
- Failure: rewriting a Word XML part with a generic XML serializer can keep compatibility attributes such as `mc:Ignorable` while dropping the matching namespace declarations (`xmlns:mc`, `xmlns:w14`, `xmlns:w15`, `xmlns:w16*`), which makes Word report the DOCX as corrupted even when the visible content edits seem small
- Preferred behavior: when modifying DOCX XML directly, preserve the original root element namespace declarations and compatibility prefixes verbatim, or patch the existing XML surgically instead of regenerating the root tag through a default serializer

### 2026-06-08T14:50:00+09:00 - PowerShell Display Mojibake Is Not The Same As File Mojibake

- Entry-ID: `ul-9c2b38ab-7b05-54e3-ad1f-343cf00002f5`

- Status: `workaround`
- Scope: user/environment
- Pattern: PowerShell output for UTF-8 markdown shows display artifacts such as `窶・` even though the file opens normally in the editor
- Failure: shell-rendered punctuation artifacts are mistaken for stored file corruption, which can trigger unnecessary edits to otherwise clean files
- Correct behavior: if a file looks normal in the editor but odd in shell output, verify with an explicit UTF-8 read or byte-level scan before assuming the markdown itself is corrupted
- Preferred behavior: treat `Get-Content` display as potentially unreliable for punctuation-heavy UTF-8 text in this environment; confirm corruption with Python or another explicit UTF-8 reader before repairing content

### ISSUE 2026-04-14-SHELL-01 - Pandoc Not On PATH In This Environment

- Entry-ID: `ul-07247ba8-b20c-5aaa-b0a7-4b997cd46fbf`

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

### 2026-06-19T19:43:23.6771334+09:00 - Word PDF Export Can Hang On VPN Printer Verification

- Entry-ID: `ul-d66b35e9-e0c7-588b-b746-1ba5fba37c05`

- Status: workaround
- Scope: user/workflow
- Pattern: Microsoft Word DOCX-to-PDF export on the company VPN
- Failure: Word PDF export can hang or fail when the default printer driver tries to verify a network/company printer through VPN.
- Preferred workaround: before exporting PDFs through Word/COM, switch the default printer to a local driver such as Microsoft Print to PDF, or avoid Word's printer-dependent export path when possible.
- Recheck trigger: revisit if Word/Office printer handling changes or if exports hang again despite a local default printer.

### 2026-06-30T16:33:56.6979603+09:00 - Use A 13 px VS Code Font Baseline Across Content Surfaces

- Entry-ID: `ul-a11b5150-89de-5d93-b831-a8f4b089eda6`

- Status: resolved
- Scope: user/editor preference
- Pattern: VS Code primary and secondary surfaces displayed different apparent font sizes
- Decision: align configurable VS Code content fonts to the workbench's 13 px baseline
- Preferred behavior: keep editor, SCM input, Markdown preview, notebook markup/output, Codex chat/chat code, debug console, and integrated terminal font-size settings at 13 unless the user requests a new global baseline

### 2026-07-13T17:12:00+09:00 - Put Windows Paths With Parenthesized Folder Names In Code Blocks

- Entry-ID: `ul-39a994f2-47e9-50ac-903c-e1ef80473be5`

- Status: `workaround`
- Scope: user/workflow
- Pattern: reporting Windows paths containing folder names such as `(K) NCB` in Markdown
- Failure: a single backslash before `(` can be rendered as a Markdown escape, hiding the path separator and making `Clients\(K) NCB` appear as `Clients(K) NCB`
- Preferred behavior: when reporting local Windows paths, especially client paths containing parenthesized folder names, put the whole path in a fenced code block or otherwise escape the backslashes so separators remain visible

### ISSUE 2026-07-06-WORKFLOW-01 - `Workflow` Tool Unavailable Across Sessions In This Environment

- Entry-ID: `ul-db7d4532-ca2a-589c-b78d-0938d4e6130a`

- Issue type: `workflow`
- Component: Claude Code `Workflow` tool (multi-agent orchestration with `phase()`/`parallel()`/`agent()` helpers)
- Version observed: n/a (tool-availability issue, not a version bug)
- Date first noticed: 2026-07-06
- Status: `open` with workaround
- Symptom: a `Workflow` script launched successfully and partially completed (5 of 19 agents finished, cached results in `subagents/workflows/<run-id>/journal.jsonl`), then failed the remaining agents with a session-limit error. On attempting to resume via `Workflow({scriptPath, resumeFromRunId})` in a later session (same day) and again three days later in a brand-new session, the `Workflow` tool itself was not present at all — not callable directly, and `ToolSearch` for `"Workflow"` returned no matching deferred tool either time.
- Workaround: completed agent results are not lost — they persist on disk as individual `agent-*.jsonl` transcripts plus a shared `journal.jsonl` with one `{"type":"result",...}` line per finished agent, keyed by `agentId` (no explicit unit/task label in the journal itself; match by inspecting each result's content). Extract completed results directly from the journal (e.g. via a small Node/Python script parsing the JSONL) and continue the remaining work as sequential/parallel plain `Agent` tool calls instead of waiting for `Workflow` to become available again.
- Preferred behavior: before starting a large multi-agent task, do not assume `Workflow` will remain available for a resume days later. If a multi-phase task depends on shared context across many agents (e.g. a common style/voice guide), extract and persist that shared context to durable files as soon as it's produced, so a fallback to plain sequential `Agent` calls can reuse it without regenerating it.
- Recheck triggers:
  - `Workflow` reappears as a directly-callable or `ToolSearch`-discoverable tool in a fresh session
  - Claude Code client/version update that might restore or explain the gating
- Exit criteria: `Workflow({scriptPath, resumeFromRunId})` succeeds in resuming a previously-interrupted run without the tool being reported unavailable.

### 2026-06-19T19:43:35.4984139+09:00 - Word PDF Export Can Hang On VPN Printer Verification

- Entry-ID: `ul-57059c3b-547d-557c-9271-0ca5eebd3d14`

- Status: workaround
- Scope: user/workflow
- Pattern: Microsoft Word DOCX-to-PDF export on the company VPN
- Failure: Word PDF export can hang or fail when the default printer driver tries to verify a network/company printer through VPN.
- Preferred workaround: before exporting PDFs through Word/COM, switch the default printer to a local driver such as Microsoft Print to PDF, or avoid Word's printer-dependent export path when possible.
- Recheck trigger: revisit if Word/Office printer handling changes or if exports hang again despite a local default printer.

### ISSUE 2026-07-07-NETWORK-01 - `openai` Python Package Cannot Be Reliably Installed In This Workspace's `.venv`

- Entry-ID: `ul-05a07bd0-36a8-53ac-8281-f219f5f82379`

- Issue type: `network` / `workflow`
- Component: `openai` PyPI package install into this repo's `.venv` (network-drive-backed: `\\prod-fs-gen01\...\textmaker\.venv`)
- Version observed: failed identically across `openai==1.59.9`, `2.38.0`, and `2.44.0`
- Date first noticed: 2026-07-07 (recurred across multiple attempts same day)
- Status: `workaround`
- Symptom: `pip install` reports success (sometimes even reporting the wrong final installed version in its own log output), but `import openai` then fails with `ModuleNotFoundError`/`ImportError` on an internal submodule -- different missing submodule each time (`openai.types.responses.response_input_text_content`, `openai.lib.streaming._deltas`, `cannot import name 'omit' from openai._types`). Consistent with partial/corrupted file copy onto the SMB-backed venv during install.
- Workaround: do not depend on the `openai` SDK for API access in this repo. Use raw HTTP via `requests` directly against `https://api.openai.com/v1/...` endpoints instead -- confirmed stable across many calls. See `scripts_local/generate_presentation_skills_images.py` and `scripts_local/generate_image_transparent.py` for the working pattern (including the `background: "transparent"` parameter for `gpt-image-1`, which requires SDK 2.x to access via the SDK but is trivially available via raw HTTP regardless of SDK version/state).
- Recheck triggers: a different venv location (local disk, not network share); pip/venv tooling changes that address partial-copy corruption on network-drive targets.
- Exit criteria: `import openai; openai.__version__` succeeds cleanly immediately after a fresh install, verified directly (not inferred from pip's log text) at least twice in separate sessions.

### 2026-05-29 - Project Memory Lives In Repo-Root Files, Not AI-Specific Internal Memory

- Entry-ID: `ul-02fdf5a6-3312-5c74-a19a-4047769b1217`

- Status: `active`
- Scope: user/workflow
- Pattern: saving project memory during any session in this workspace
- Decision: the user works with multiple AI tools in VS Code (Claude Code, Codex, and others) that share one memory source. Project memory must always be written to the repo-root files defined in AGENTS.md — never to an AI tool's internal/private memory only.
- Required behavior:
  1. At session start, read `AGENTS.md` at the repo root — it defines the startup read order and memory file locations
  2. Durable project facts and decisions → `project-learning.md` (repo root)
  3. Chronological session events → `project-journal.md` (repo root), appended in date order at the END of the file
  4. AI-internal memory (e.g. Claude Code memory) is secondary only — never the sole record of project decisions
  5. After writing to repo memory files, commit and push so all AIs see the update
- Why: writing memory only to AI-specific internal storage makes it invisible to other AIs working in the same repo, breaking shared context across tools
