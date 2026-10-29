# Plan: write handoff note

Plan mode blocks writing outside this file. On approval, write the note below to
`/home/luca/repos/gram/.claude/handoffs/2026-10-29-sandbox-t1-results.md` (new file, no other changes, no commit).

---

# Sandbox: T1 results in ~/repos/gram
2026-10-29 · branch main @ 7f840e24de · supersedes 2026-10-29-sandbox-prompted-access.md

## Goal
Claude works freely in the current repo. Out-of-repo access goes through the user's prompt, and secrets and escape sockets stay unreachable. This session started the Phase 0 tests (T1–6) from the previous handoff.

## State
- Done (earlier sessions, in `~/.claude`, which has no git): settings, `hooks/outside-repo-guard.py`, `hooks/sandbox-bootstrap.sh`, CLAUDE.md `## Sandbox`.
- T1, mostly passing:
  - The SessionStart bootstrap printed "Sandbox: added /home/luca/repos/gram…".
  - `.claude/settings.local.json` holds `allowRead: ["/home/luca/repos/gram"]`.
  - Sandboxed `ls`, `cat` and `git status` work.
- T1 bug: `.git/info/exclude` has no `.claude/settings.local.json` line, and `git check-ignore -v .claude/settings.local.json` exits 1.
- New finding: the sandbox creates placeholder files (`crw-rw-rw- nobody 1,3`, i.e. /dev/null bind mounts) for denied paths inside the repo. They show up in `git status` as untracked:
  - repo root: `.bashrc`, `.bash_profile`, `.profile`, `.zshrc`, `.zprofile`, `.gitconfig`, `.gitmodules`, `.mcp.json`, `.ripgreprc`
  - `.claude/`: `settings.json`, `hooks`, `skills`, `agents`, `commands`, …
- Oddity: the first `ls .claude/handoffs/*.md` this session found nothing, and a later one found the previous note.
- Not run yet: T2–T6.
- Uncommitted: nothing tracked. `.claude/` is untracked (handoffs plus settings.local.json).

## Open questions
- Why the bootstrap's exclude write didn't land. Possible causes:
  - the hook runs with a cwd other than the repo
  - `git rev-parse --git-path` returns a relative path
  - `.git/` isn't writable from the hook's context

  Answer by running the hook by hand: `echo '{"cwd":"/home/luca/repos/gram"}' | bash ~/.claude/hooks/sandbox-bootstrap.sh`, then inspect the exclude file.
- Should the placeholder files be hidden from `git status`, e.g. via exclude lines the bootstrap writes, or a global excludes file? The user decides.
- Carried over: does the guard's `ask` prompt in auto mode? Does MATLAB hang again?

## Next step
Debug the missing exclude line (see above) and propose a fix to `sandbox-bootstrap.sh`. Then run T2: `/add-dir ~/repos/<other>`, then sandboxed `touch` and `cat` there.

## Pointers
- Previous note: `.claude/handoffs/2026-10-29-sandbox-prompted-access.md` (the T1–T6 list)
- Plan: `~/.claude/plans/i-think-this-sandbox-shiny-planet.md`
- `~/.claude/hooks/sandbox-bootstrap.sh`, `~/.claude/settings.json`
