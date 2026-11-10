---
name: sync-setup-reports
description: Update the setup reports in ~/.claude/reports/ after changes to the Claude Code setup (settings, CLAUDE.md, hooks, skills, agents).
disable-model-invocation: true
---

# Sync setup reports

Runs in `~/.claude`. In plan mode, stop and say it needs normal mode: the report-sync agent inherits plan mode and could
not write.

## 1. Collect
Run `python3 ~/.claude/hooks/setup-changes.py --check`. No output: say the reports are up to date and stop. Otherwise
show the changed paths, one line each.

## 2. Update
Typing this command approves edits under `reports/` (git-reversible); nothing outside it changes. Spawn the
`report-sync` agent: "Update the reports from reports/.sync/pending.json." Wait for its summary.

## 3. Review
Show `git diff --stat -- reports/` and the agent's summary. Read the rebuilt PDF pages that changed and check the layout
yourself; fix what the agent got wrong. Then wait for the user's OK.

## 4. Stamp
On OK, run `python3 ~/.claude/hooks/setup-changes.py --stamp`: the snapshot now matches the reports and the status-line
flag clears. If the user rejects the update, don't stamp; the changes stay pending. Leave the commit to the user.
