#!/usr/bin/env python3
"""PreToolUse (Edit|Write|NotebookEdit): background jobs investigate only.

In a background job ($CLAUDE_JOB_DIR set), block edits to existing files outside the job dir, temp dirs
and Claude's memory; creating new files (reports, scratch scripts) stays allowed."""
import json
import os
import sys
import tempfile

job = os.environ.get("CLAUDE_JOB_DIR")
if not job:
    sys.exit(0)

ev = json.load(sys.stdin)
inp = ev.get("tool_input") or {}
path = inp.get("file_path") or inp.get("notebook_path") or ""
if not path:
    sys.exit(0)
path = os.path.realpath(os.path.join(ev.get("cwd") or ".", os.path.expanduser(path)))

writable = [os.path.realpath(d) for d in
            (job, "/tmp", tempfile.gettempdir(), os.path.expanduser("~/.claude/projects"))]
if any(path == d or path.startswith(d + os.sep) for d in writable):
    sys.exit(0)
if ev.get("tool_name") == "Write" and not os.path.exists(path):
    sys.exit(0)

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": (
        "Background sessions investigate only and leave existing files unchanged. Write new files "
        "(reports, scratch scripts) or work in $CLAUDE_JOB_DIR/tmp, and put proposed code changes "
        "as a plan in your final report.")}}))
