# Claude Code config

Personal Claude Code setup (`~/.claude`): global instructions, settings, guard hooks, custom skills and agents, plus reports that document how they fit together.

## Install
Clone into `~/.claude` (back up an existing one first):

    git clone <remote> ~/.claude

Requires `bash`, `python3` and `git`. To rebuild the reports you also need Graphviz (`dot`) and `latexmk`.

## What's here
| Path | Purpose |
|---|---|
| `CLAUDE.md` | Global working-style rules: plan before changing, token-lean reading and commands, sandbox etiquette, reply style |
| `settings.json` | Model, permissions, sandbox (filesystem/network), hook wiring, status line, plugins |
| `hooks/` | Scripts run by Claude Code (below) |
| `agents/` | Subagents: `explain` (explain existing code), `plan-critic` (fresh-eyes plan review), `report-sync` (used by `/sync-setup-reports`) |
| `skills/` | Slash commands (below) |
| `reports/setup/`, `reports/sandbox/` | PDF/SVG overviews of the setup and the sandbox, with `.tex`/`.dot` sources |
| `plans/` | Plans saved from plan-mode sessions |

### Hooks
| Hook | Event | Does |
|---|---|---|
| `map-status.sh` | SessionStart | Warns when a repo has no CLAUDE.md map, or source files moved since it was verified |
| `sandbox-bootstrap.sh` | SessionStart | Gives each repo sandbox read access to itself via `.claude/settings.local.json` |
| `setup-changes.py` | SessionStart, Stop | Tracks setup changes the reports don't cover yet |
| `git-guard.py` | PreToolUse (Bash, Agent) | Forces a prompt before creating, moving or deleting branches/worktrees |
| `bg-guard.py` | PreToolUse (Edit/Write) | Background jobs may only write new files, not edit existing ones |
| `outside-repo-guard.py` | PreToolUse (Edit/Write) | Prompts for edits outside the repo or to files that can run code |
| `statusline.sh` | status line | Model · context used · git branch (flags linked worktrees) |

### Skills
| Command | Does |
|---|---|
| `/sync-claude-md` | Build or repair a project's CLAUDE.md map for agents |
| `/sync-readme` | Build or refresh a project's README.md |
| `/sync-setup-reports` | Update `reports/` after setup changes |
| `/handoff` | Save the session as a note in `.claude/handoffs/` |
| `/pickup` | Resume from a handoff note |

## Keeping the reports current
After editing settings, hooks, skills, agents or CLAUDE.md, run `/sync-setup-reports` in a session started in `~/.claude` (normal mode, not plan mode). To list pending changes without updating:

    python3 ~/.claude/hooks/setup-changes.py --check

## What git tracks
`.gitignore` whitelists the files above. Runtime state (sessions, caches, `projects/`, `skills/synced/`, `.claude/settings.local.json`) stays untracked. Add new top-level files to the whitelist.
