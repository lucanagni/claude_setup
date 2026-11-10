#!/usr/bin/env python3
"""PreToolUse (Edit|Write|NotebookEdit): edits outside the repo, and edits that can run code
outside the sandbox, always reach the user.

Paths inside a .git dir or in Claude's own hooks/settings/skills/agents/CLAUDE.md get
permissionDecision "ask" anywhere. So do paths outside the session's git root (or cwd),
Claude's temp dir, memory and plans. Auto mode's classifier cannot approve either."""
import json
import os
import subprocess
import sys


def under(p, d):
    return p == d or p.startswith(d + os.sep)


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason}}))
    sys.exit(0)


ev = json.load(sys.stdin)
inp = ev.get("tool_input") or {}
path = inp.get("file_path") or inp.get("notebook_path") or ""
if not path:
    sys.exit(0)
cwd = ev.get("cwd") or os.getcwd()
path = os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))

# git hooks/config and Claude's hooks run unsandboxed (e.g. on a prompted `git push` retry).
claude = os.path.realpath(os.path.expanduser("~/.claude"))
runs_code = [os.path.join(claude, p) for p in
             ("settings.json", "settings.local.json", "hooks", "skills", "agents", "CLAUDE.md")]
if ".git" in path.split(os.sep) or any(under(path, d) for d in runs_code):
    ask(f"{path} can run code outside the sandbox (git hooks/config, Claude hooks/settings); "
        "edits there need your approval.")

try:
    root = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True, timeout=5).stdout.strip()
except Exception:
    root = ""
free = [os.path.realpath(d) for d in
        (root or cwd, cwd, "/tmp/claude-%d" % os.getuid(),
         os.path.expanduser("~/.claude/projects"), os.path.expanduser("~/.claude/plans"))]
if any(under(path, d) for d in free):
    sys.exit(0)

ask(f"{path} is outside the repo ({root or cwd}); edits there need your approval.")
