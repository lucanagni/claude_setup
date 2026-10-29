# Finish sandbox check: Wolfram and MATLAB

## Context
Sandbox check from handoff `2026-10-28-claude-workflow-setup.md`. Results:
- `git ls-remote` over ssh (bitbucket): works in sandbox.
- `wolframscript -code 1+1`: exit 255, no output, in sandbox.
- `matlab -batch "disp(1)"`: error 5201 "Unable to communicate with required MathWorks services" in sandbox (MathWorks service host needs writes/sockets outside the allowlist).

## Where
`~/.claude` (no git), no commit.

## Steps
- `~/.claude/settings.json` → `sandbox.excludedCommands` += `"wolframscript *"`, `"matlab *"` → both fail inside bwrap; running them unsandboxed is what the handoff anticipated (via `update-config` skill).
- `~/.claude/settings.json` → `sandbox.allowUnsandboxedCommands: false` → stops Claude from running commands with `dangerouslyDisableSandbox`; `excludedCommands` becomes the only way out of the sandbox, and only you can change it.
- `~/.claude/.claude/handoffs/2026-10-28-claude-workflow-setup.md` → mark sandbox check done, drop the Wolfram/MATLAB open question.

## Decisions
- Exclude whole commands rather than chase extra allowWrite paths (`~/.MathWorks`, Wolfram licensing sockets): fewer guesses, licenses are local anyway.
- Leave `ssh/scp/rsync` exclusion as is (git-over-ssh already works; no change needed).
- Remove now-unneeded `~/.Mathematica`, `~/.Wolfram`, `~/.matlab` from allowWrite? No — keep them (harmless, still used if a kernel is launched another way, e.g. `math`).

- MATLAB unsandboxed also hung >150 s with no output (killed). So exclusion alone may not fix MATLAB; if `matlab -batch` still hangs outside the sandbox, that's a MATLAB/licensing issue to debug separately, not a sandbox one.

## Check
In a fresh session (settings reload): `wolframscript -code 1+1` → `2`; `matlab -batch "disp(1)"` → `1`; any Bash call with `dangerouslyDisableSandbox: true` still runs sandboxed (e.g. `touch ~/x` fails).

## Docs
None (no map in `~/.claude`).
