

Run dashboard script then open view
No tasks in progress


I have this command in settings.json:

  "commands.commands": {
    "Open Dashboard": {
      "command": "livePreview.start.preview.atFileString",
      "args": "dashboard/dashboard.html",
    },

However, this is specific to the textmaker project only. Also, I want the command to first run the script that generates the dashboard and then open the .html output.

What should I do?


Worked for 1m 38s
Use a workspace-scoped command + a task.

Put this in project settings.json (not user settings), so it only applies to textmaker:
{
  "commands.workspaceCommands": {
    "Open Dashboard": {
      "sequence": [
        { "command": "workbench.action.tasks.runTask", "args": "Generate Dashboard" },
        { "command": "livePreview.start.preview.atFileString", "args": "dashboard/dashboard.html" }
      ]
    }
  }
}
Create tasks.json with your dashboard build script:
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Generate Dashboard",
      "type": "shell",
      "command": ".\\textmaker.cmd",
      "args": ["<your-dashboard-generate-subcommand>"],
      "options": { "cwd": "${workspaceFolder}" },
      "problemMatcher": []
    }
  ]
}
Remove the Open Dashboard entry from global settings.json.
If you want, I can wire this directly in your workspace now once you tell me the exact dashboard generation command.

Sources:

commands.workspaceCommands support: https://github.com/usernamehw/commands#workspace-commands
VS Code task command (workbench.action.tasks.runTask): https://code.visualstudio.com/docs/editor/tasks

please go ahead


Worked for 1m 23s
Implemented.

Changes made:

Added project-only dashboard command chain in settings.json (line 43).
Added project-only generator command setting in settings.json (line 42):
dashboard.generateCommand (currently placeholder).
Added task runner in tasks.json (line 1):
Task label Generate Dashboard runs ${config:dashboard.generateCommand}.
Removed global command from settings.json so it no longer applies to other projects.
What you need to set now:

Replace the placeholder at settings.json (line 42) with your real build command, for example:
.\textmaker.cmd <your-dashboard-command> ...
or build_dashboard.py
After that, run your Open Dashboard command as before. It will trigger generation first, then open dashboard.html.


3 files changed
+31
-8
Undo

Review
.vscode/settings.json
.vscode/tasks.json
C:/Users/d-dobson/AppData/Roaming/Code/User/settings.json
i'm sorry. I gave you the wrong information. the 'Open Dashboard' command is specific to the videocat project, not textmaker.


Worked for 32s
Understood. I’ve removed the dashboard command/task changes from textmaker:

Cleaned settings.json (no Open Dashboard wiring now)
Deleted tasks.json
Confirmed no commands.commands dashboard entry remains in user settings
If you open the videocat workspace, I can apply the same setup there with the correct dashboard build command.


2 files changed
+1
-30
Undo

Review
.vscode/settings.json
.vscode/tasks.json
that folder is on my home PC. I have Codex for VS Code installed on both. Can I access this thread when I change PCs?

Not automatically, in most setups.

Codex for VS Code chat history is usually local to each machine/VS Code profile unless you’re using a synced account feature that explicitly syncs conversation history.

Best practical options:

Copy this thread into a note/file now (or commit the config changes to git).
On home PC, open the videocat repo and start a new chat, then paste:
your intended Open Dashboard behavior
the exact dashboard generation command
I can recreate the exact setup there in one pass.
If you want, I can also give you a ready-to-paste snippet now for videocat so you can apply it quickly on the other PC.


yes, please. that would be helpful

Use this in settings.json:

{
  // ...your existing settings...
  "dashboard.generateCommand": "YOUR_DASHBOARD_BUILD_COMMAND_HERE",
  "commands.commands": {
    "Open Dashboard": {
      "sequence": [
        {
          "command": "workbench.action.tasks.runTask",
          "args": "Generate Dashboard"
        },
        {
          "command": "livePreview.start.preview.atFileString",
          "args": "dashboard/dashboard.html"
        }
      ]
    }
  }
}
Create tasks.json:

{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Generate Dashboard",
      "type": "shell",
      "command": "${config:dashboard.generateCommand}",
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "problemMatcher": []
    }
  ]
}
Example value for dashboard.generateCommand:

build_dashboard.py
or npm run build:dashboard
or build-dashboard.cmd
Notes:

Keep this in workspace .vscode (not user settings) so it stays project-specific.
The command will run generation first, then open dashboard.html in Live Preview.
