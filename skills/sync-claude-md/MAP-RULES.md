# Map rules

A project map (CLAUDE.md) caches what an agent cannot find by looking: where things live, how pieces connect, what must stay consistent, and the traps. Everything else lives in the environment or next to the code.

## Template

```markdown
<!-- verified: <short sha> <YYYY-MM-DD> -->
# <project>
<one-line purpose>

## Commands
<non-obvious commands only; how to run a single test, when tests exist>

## Layout
<only dirs whose role the name hides>: `path/ - role (key file)`

## Where to change X
<the 3 to 5 most common edits: "add a prior: bilby/core/prior/ + register in __init__.py">

## Conventions
<rule - reason>

## Gotchas
<code or tool behaviour that costs a session if unknown>

## Fork delta
<forks of someone else's project only: what diverges from upstream - where - why>
```

## Content
- Record navigation facts: locations, connections, cross-file invariants, how to run things.
- Implementation details, parameter values, numerical results and history belong in code comments, docstrings, notebook text cells, or a doc beside the code (e.g. `benchmarks.md`); the map holds at most a one-line pointer to that doc.
- Leave out what one command or one file read reveals (standard scripts, self-describing directories).
- Keep each fact in one place; point to it instead of copying it.
- Describe the present: edit or delete a stale line rather than adding a correction.
- Phrase each rule as the action to take.
- Keep a line only if it changes what an agent would do without it.
- Omit any section with nothing to say.

## When to update
A map edit is due when a map line becomes false, or a module, entry point, command, dependency, env var or cross-file invariant appears, moves or goes. New functions, parameter changes, bug fixes and refactors inside a file leave the map as it is.

## Checks
- Confirm every path exists and every command is defined (manifest script, Makefile target, binary on PATH). Execute only fast, side-effect-free ones, such as a single test.
- Preserve verbatim any section owned by another tool or marked as generated (e.g. an `## Agent skills` block).
- Keep the map under 150 lines. Past that, move a subsystem's detail into `<dir>/CLAUDE.md`, leave a one-line pointer, and confirm every such pointer resolves.
- Bump the `verified` line to the current short sha (or `no-git`) and today's date.
- Fork of someone else's project: keep the map out of upstream commits by offering to add `CLAUDE.md` to `.git/info/exclude`.
