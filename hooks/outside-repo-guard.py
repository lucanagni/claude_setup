#!/usr/bin/env python3
"""PreToolUse (Edit|Write|NotebookEdit): edits outside the repo always reach the user.

Paths outside the session's git root (or cwd), temp dirs, Claude's memory and plans get
permissionDecision "ask", so auto mode's classifier cannot approve them."""
import json
import os
import subprocess
import sys
import tempfile

ev = json.load(sys.stdin)
inp = ev.get("tool_input") or {}
path = inp.get("file_path") or inp.get("notebook_path") or ""
if not path:
    sys.exit(0)
cwd = ev.get("cwd") or os.getcwd()
path = os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))

try:
    root = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True, timeout=5).stdout.strip()
except Exception:
    root = ""
free = [os.path.realpath(d) for d in
        (root or cwd, cwd, "/tmp/claude-%d" % os.getuid(), tempfile.gettempdir(),
         os.path.expanduser("~/.claude/projects"), os.path.expanduser("~/.claude/plans"))]
if any(path == d or path.startswith(d + os.sep) for d in free):
    sys.exit(0)

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": f"{path} is outside the repo ({root or cwd}); edits there need your approval."}}))
