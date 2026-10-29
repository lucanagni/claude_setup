---
name: handoff
description: Save the current session as a handoff note in the repo, for a fresh session to resume with /pickup.
argument-hint: "[what the next session will focus on]"
disable-model-invocation: true
---

# Handoff

Write a handoff note so a fresh session can continue this work without the conversation. When `$ARGUMENTS` is given, it names the next session's focus: tailor the note to it.

## 1. Locate
Directory: `<git root>/.claude/handoffs/` (outside git: `./.claude/handoffs/`). File: `YYYY-MM-DD-<slug>.md`, where the slug is 2-4 words naming the task; append `-2`, `-3` when taken.

## 2. Gather git state
Run `git branch --show-current`, `git rev-parse --short HEAD`, `git status --short` and `git worktree list`; note when this session works in a linked worktree.

## 3. Write

```markdown
# <task>
<date> · branch <branch> @ <sha> [· worktree <path>]

## Goal
<what we are trying to achieve and why, 1-3 lines>

## State
- Done: <item - file paths, commits>
- In progress: <item - where it stopped>
- Uncommitted: <file - what changed>

## Decisions
- <choice: value, cut, method, assumption> - <reason>
- Rejected: <approach> - <why>, when the next session might retry it

## Open questions
- <question - who or what can answer it>

## Next step
<the single next action, concrete enough to start without rereading the session>

## Pointers
<plans, reports, specs, commits, memory files to read first; skills to call>
```

Rules:
- Reference specs, plans, reports, commits and diffs by path or sha instead of pasting them.
- Stay under 60 lines; omit empty sections.
- Redact secrets (API keys, passwords, tokens).

## 4. Finish
Print the note's path and suggest `/clear` followed by `/pickup`.
