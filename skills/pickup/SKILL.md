---
name: pickup
description: Resume work from a handoff note saved by /handoff.
argument-hint: "[slug or date of a handoff; default: newest]"
disable-model-invocation: true
---

# Pickup

1. List `<git root>/.claude/handoffs/*.md` (outside git: `./.claude/handoffs/`), newest first. Take the one matching `$ARGUMENTS`, else the newest.
2. Read it and the files under its Pointers.
3. Compare its header with now: `git branch --show-current`, `git rev-parse --short HEAD`, `git status --short`. Note the drift: another branch, new commits, uncommitted files that appeared or disappeared.
4. Report in at most 5 lines: the goal, where it stopped, the drift, and the next step. Name up to 3 other recent notes in one line. Then wait for the user; changes go through the usual plan.
