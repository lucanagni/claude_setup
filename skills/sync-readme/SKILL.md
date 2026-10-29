---
name: sync-readme
description: Build or refresh a project's README.md for human readers.
disable-model-invocation: true
argument-hint: "[path to a README]"
---

# Sync README

Target: `$ARGUMENTS` if given, else `README.md` at the repo root (`git rev-parse --show-toplevel`).

Write for a newcomer: a person who has not opened the code, the manifests or CLAUDE.md.

## 1. Gather
- **README missing:** read the build manifests (package.json, pyproject.toml, requirements.txt, environment.yml, CMakeLists.txt, Makefile, MATLAB *.prj or buildfile.m, Cargo.toml, go.mod, or the stack's equivalent), the project CLAUDE.md as a source of verified facts, the entry points, and `git ls-files | cut -d/ -f1-2 | sort -u`.
- **README exists:** read it, then take the commit that last touched it (`git log -1 --format=%h -- <target>`) and run `git diff --stat <sha>` and `git log --oneline <sha>..HEAD`. Treat the user-facing changes in that range (commands, flags, env vars, install steps, data, behaviour) as your worklist.
- **Fork of someone else's project:** the upstream README belongs to upstream. Ask before editing it; the fork's changes go in a short `## This fork` section or a `FORK.md`.

## 2. Draft
Use the sections that apply, in this order:

```markdown
# <project>
<what it is and why someone would use it, 1 to 3 sentences>

## Install
## Usage
<quickstart first, then common tasks with examples>
## Method & references
<papers, with the equations or sections the code implements>
## Data
<inputs not in git: what they are, where to get them, where they go>
## Reproducing results
<script or notebook -> figure or table it produces>
## Configuration
<env vars and config files, with defaults>
## Development
<setup, run tests, lint>
## Citing / License / Contributing
```

Rules:
- Confirm every path exists and every command is defined (manifest script, Makefile target, binary on PATH). Execute only fast, side-effect-free ones.
- Keep the owner's prose, voice, badges and custom sections; edit only the facts that went stale.
- Spell commands out in full, ready to copy, with an example wherever a flag or option needs one.
- Keep agent material in CLAUDE.md: the map, tool-owned blocks such as `## Agent skills`, agent-facing gotchas.

## 3. Approve and write
Show the draft (the whole file when new, the changed sections otherwise) and wait for the user's OK; in plan mode the draft is the plan. Then write the target, show `git diff -- <target>` (the whole file when untracked) and stop; leave the commit to the user.
