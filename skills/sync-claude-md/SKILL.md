---
name: sync-claude-md
description: Build or repair a project's CLAUDE.md as a terse map for agents.
disable-model-invocation: true
argument-hint: "[path to a nested CLAUDE.md]"
---

# Sync CLAUDE.md

Target: `$ARGUMENTS` if given, else `CLAUDE.md` at the repo root (`git rev-parse --show-toplevel`; outside git, the current directory).

Read [MAP-RULES.md](MAP-RULES.md) first: its template, content rules and checks govern everything you write here.

## 1. Gather
- **Map missing:** read the build manifests (package.json, pyproject.toml, requirements.txt, environment.yml, CMakeLists.txt, Makefile, MATLAB *.prj or buildfile.m, Cargo.toml, go.mod, or the stack's equivalent; in a monorepo, the workspace config first), the README, and `git ls-files | cut -d/ -f1-2 | sort -u`. Open source files only to confirm an entry point or convention.
- **Map exists:** read it, then take the sha from its `<!-- verified: <sha> <date> -->` line (fallback: `git log -1 --format=%h -- <target>`). Run `git diff --name-status <sha>` (committed and uncommitted changes since) and `git status --short`. When the map has no sha, the sha is missing from history (rebase, squash), or the project has no git, gather as for a missing map and keep the existing lines that still hold.
- **Fork:** when `git remote -v` shows the repo is someone else's project and an upstream remote exists, run `git log --oneline <upstream>/<default>..HEAD` and `git diff --stat <upstream>/<default>` for the Fork delta.
- When gathering means reading 5+ files, delegate it to an Explore subagent and ask for: purpose, non-obvious commands, entry points, dirs whose role the name hides, cross-file invariants and traps, each with its path.

## 2. Draft
Write the new map, or the changed lines of the existing one, and run every check in MAP-RULES.md.

## 3. Approve and write
Show the draft (the whole file when new, the changed lines otherwise) and wait for the user's OK; in plan mode the draft is the plan. Then write the target, show `git diff -- <target>` (the whole file when untracked) and stop; leave the commit to the user. When the sync changed commands, env vars or entry points that the README also documents, say so and suggest `/sync-readme`.
