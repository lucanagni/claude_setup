# Sandbox: repo by default, prompt to go further

## Context
The current sandbox (handoff `2026-10-29-sandbox-hardening.md`) keeps Bash inside the repo plus the toolchain dirs. The only way to widen it is to edit `settings.json` by hand, which defeats the purpose. One hole is still open: sway-ipc and systemd/private give a way out of the sandbox.

Target agreed in the grilling session:
- The repo is free to use.
- Anything else in `~` needs your approval through a prompt, and Claude can act on it once you approve.
- Secrets and the escape sockets can never be reached, whatever you approve.

### Agreed requirements
| # | Decision |
|---|---|
| Q1 | Guard against both Claude's mistakes and hostile code it runs, so the socket hole must close |
| Q2 | Reads and writes outside the repo both need approval (toolchain dirs excepted) |
| Q3 | Never-allow list: ~/.ssh, ~/.gnupg, keyrings, credentials, browser/mail profiles, ~/pwd.txt, /run/user/1000 sockets, X11/ICE, system dbus. Only a manual settings edit can open them |
| Q4 | Out-of-repo file access is always approved by you, in auto mode too |
| Q6 | Directory grant first. The unsandboxed retry is a prompted last resort, and while it runs the never-allow list does not apply (accepted) |
| Q7/Q10 | Session grant = `/add-dir` typed by you. Permanent grant = Claude edits the repo's `.claude/settings.local.json` after your prompt |
| Q8 | Network unchanged: unknown hosts prompt in manual mode, and auto mode's classifier may approve them |
| Q9 | git push/pull/fetch over ssh = prompted unsandboxed retry |
| Q11 | File tools prompt outside the repo, toolchain reads are free, secrets are denied |
| Q12 | A SessionStart hook creates a repo's read grant automatically, if testing shows one is needed |
| Q13 | Conda installs = `/add-dir ~/miniconda3/envs/<env>` for the session |
| Q14 | Global CLAUDE.md rule for how Claude escalates when blocked |
| Q15 | If `/add-dir` doesn't grant reads, read grants go through the prompted settings edit |

## Where
`~/.claude`, which is not a git repo. No branches or commits. Changes are made with Edit (each one prompts you). Test sessions run in `~/repos/gram`.

## Phase 0: establish the facts (no edits; you start a session in ~/repos/gram)
These tests decide which steps below run:
- T1: can sandboxed Bash read the repo with no `.claude/settings.local.json`? Probe: `ls .` and `cat` a tracked file. Decides step 4.
- T2: after `/add-dir ~/repos/<other>`, can sandboxed Bash write to it and read it? Decides Q15 (whether session grants are write-only).
- T3: does an edit to `.claude/settings.local.json` mid-session (e.g. adding `allowRead`) take effect without a restart? This decides whether a permanent grant is usable immediately or only from the next session.
- T4: for the Read/Edit tools, which wins: an `ask` rule or an `allow` rule? Does auto mode honour `ask` rules for Read/Edit? Decides how step 2's rules are shaped.

## Phase 1: settings (1 file)
1. `~/.claude/settings.json` → sandbox block:
   - `denyRead` = `["~/", "~/.claude/.credentials.json", "/run/user/1000", "/tmp/.X11-unix", "/tmp/.ICE-unix", "/run/dbus/system_bus_socket"]`. Closes the sway/systemd socket hole (Q1, Q3).
   - `allowUnsandboxedCommands: true`. Enables the last-resort route (Q6, Q9).
2. `~/.claude/settings.json` → permissions:
   - Add an ask rule `Bash(dangerouslyDisableSandbox:true)`. Every unsandboxed retry then prompts, in auto and bypass modes too, and it beats any Bash allow rule (Q4, Q6).
   - Mirror the existing `Read(...)` denies as `Edit(...)` denies. Today secrets are blocked for Read only (Q3).
   - Outside-repo file access (Q11). The final rule shape depends on T4:
     - If ask beats allow: `ask` on `Read(~/**)` and `Edit(~/**)` would also catch the repo, so instead rely on the default prompt for paths outside the working dirs. Add `allow` for toolchain reads (`Read(~/miniconda3/**)`, `~/.matlab/**`, `~/Documents/MATLAB/**`, …, the same list as sandbox `allowRead`).
     - If auto mode skips that default prompt, add `ask` rules for the specific top-level trees (`~/repos/**`, `~/Documents/**`, `~/Downloads/**`, `~/Desktop/**`). Edits in the current repo are then expected to prompt in auto mode; T4 confirms this.

## Phase 2: automation and behaviour (2 files)
3. `~/.claude/CLAUDE.md` → new short `## Sandbox` section (Q14). On a sandbox block, Claude stops and names the path and the reason, then offers in order:
   1. the exact `/add-dir <path>` (session)
   2. a prompted edit to `.claude/settings.local.json` `sandbox.filesystem.allowRead/allowWrite` (permanent, or any read grant if T2 says so)
   3. an unsandboxed retry, only for git remote ops or as a last resort

   Claude never works around a block, e.g. by copying files into the repo.
4. Only if T1 fails: new `~/.claude/hooks/sandbox-bootstrap.sh` plus a SessionStart entry in `settings.json`. In a git repo whose `.claude/settings.local.json` lacks it, the hook merges in `{"sandbox":{"filesystem":{"allowRead":["."]}}}`, written in Python so existing keys are kept. It never touches `~/.claude`. The style follows the existing `hooks/map-status.sh`.

## Decisions
- Socket hole: deny all of `/run/user/1000` rather than enumerating sockets. The proxy sockets live in `/tmp`, so the network should survive this; the check verifies it.
- The git retry needs no git-specific rule. The `dangerouslyDisableSandbox` ask rule covers it, and the existing `Bash(ssh *)`/`Bash(scp *)` asks stay.
- Network: no change (Q8).
- Persistent grants live in the repo's `settings.local.json` (Claude Code keeps that file out of git), never in global `settings.json`.
- Known accepted gap: an approved unsandboxed retry can reach secrets and sockets. Read the command before clicking yes, and watch for git hooks.

## Check
Run in `~/repos/gram` after each phase:
- Socket probe: a Python `AF_UNIX` connect to `sway-ipc.*.sock`, `systemd/private`, `at-spi/bus_0` and pipewire-manager must all fail.
- `curl -sI https://pypi.org` works. `curl -sI https://example.com` prompts (manual mode).
- `matlab -batch "disp(1+1)"` and `wolframscript -code 1+1` both work.
- `cat ~/.ssh/id_*` from Bash fails, and the Read tool is denied on it. An Edit of `~/.bashrc` prompts.
- A blocked write to `~/repos/<other>` leads Claude to offer `/add-dir`. After you type it, the write succeeds.
- `git fetch` over ssh fails in the sandbox, then prompts as an unsandboxed retry and succeeds.
- A new repo with no `.claude/` works at the first session, after step 4 if it was needed.

## Docs
- `~/.claude/CLAUDE.md`: the new Sandbox section (step 3).
- The handoff note gets superseded; I write a fresh one when we stop.
