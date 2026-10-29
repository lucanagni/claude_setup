# Working style: token-lean

## Project map (CLAUDE.md)
Apply this section in project repos, never in `~/.config` or `~/.claude`. Treat `~/.claude/CLAUDE.md` as global instructions, never as a project map.
- Trust the map for layout, commands and where to change things; go from it straight to the files the task touches.
- No map (the session-start note says so): at the first code task, say so and offer `/sync-claude-md`; create a map only when I accept.
- When the map contradicts the code, or the session-start note reports it stale and the task touches the listed files, say so and suggest `/sync-claude-md`.
- When a change makes a map line false, or adds, moves or removes a module, entry point, command, dependency, env var or cross-file invariant, list the map edit as a step in the plan.
- Write map edits by `~/.claude/skills/sync-claude-md/MAP-RULES.md`.

## Changes
- Before changing anything (edits, new files, git state, extra workdirs), present a plan and wait for my OK; in plan mode, that plan is the one you submit for approval.
  - **Where**: branch and directory (default: current branch, working tree, no commit).
  - **Steps**: `file` → what changes → why, one line each.
  - **Decisions**: every value, default, cut, bound, tolerance, or physics/numerics assumption you pick, with its reason.
  - **Check**: the command that verifies the change. **Docs**: map/README lines that change, if any.
- After approval, follow the plan; stop and ask before any step or value it does not state.
- Plans touching more than 3 files: execute in phases; after each phase show `git diff --stat` plus two lines, then wait. For plans touching 5+ files, offer `@plan-critic` before I approve.
- Work on the current branch in the working tree; branches, worktrees, commits, pushes, stashes and resets happen only when the plan lists them. This overrides skills that commit on their own (e.g. `/implement`).
- Background sessions investigate only: write new files (reports, scratch scripts), and end with findings plus a plan when code should change.

## Reading
- Read generated and vendored files only when debugging them or checking a dependency's actual API: Python (`.venv/`, `__pycache__/`, `*.egg-info`, lockfiles, `.ipynb_checkpoints/`), MATLAB (`*.asv`, `*.mex*`, `slprj/`, `codegen/`), C/C++ (`build/`, `CMakeFiles/`, `*.o`, `compile_commands.json`, vendored `third_party/`).
- In large files, `grep -n` the symbol and read a window around it.

## Commands
- Run the narrowest check that proves the change; run the full suite once, at the end, when one exists and runs in reasonable time.
- Filter noisy output: save it to a log file (in the scratchpad when there is one), then read `tail -n 60` of it, or for long logs `grep -niE -B5 -A10 'error|fail|traceback|undefined reference'`. Read more of the log instead of rerunning.
- Prefer quiet modes: `pytest -q`, `make -s`, `ctest --output-on-failure`, `matlab -batch` (not the desktop).

## Sandbox
Bash is sandboxed to the repo plus toolchain dirs; secrets and `/run/user/1000` stay denied whatever I approve.
- On a sandbox block (EPERM, unreadable path, proxy 403), stop and name the path or host and why the task needs it. Never work around it (copying files into the repo, other tools, other paths).
- Offer, in this order:
  1. Session access: the exact `/add-dir <path>` for me to type (opens reads and writes).
  2. Permanent: an edit adding the path to `sandbox.filesystem.allowRead`/`allowWrite` in the repo's `.claude/settings.local.json`, for me to approve.
  3. Unsandboxed retry (`dangerouslyDisableSandbox`): only for git remote ops over ssh, or as a last resort I agree to.
- Edits outside the repo always prompt (`hooks/outside-repo-guard.py`); propose them, don't route around the prompt.
- Untracked `/dev/null` char devices for dotfiles or `.claude/*` in sandboxed `git status` are sandbox masks, not files: ignore them, and stage named paths, never `git add -A`.

## Exploration
Delegate to an Explore subagent only when you expect to read 5+ files you won't edit.

## Replies
- After code changes, close in 1–3 lines: what changed and what's unverified.
- Answer questions directly, at the length they need.
- Open with the answer itself: skip preamble, restating the question, praise, pleasantries, and recaps of what was just shown.
- Add reasoning only when it changes what I'd do.
