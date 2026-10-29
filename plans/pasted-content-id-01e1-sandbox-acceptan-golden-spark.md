# Sandbox acceptance test

## Context
Run the 6-step sandbox acceptance test from the pasted request, report PASS/FAIL + one-line evidence per step, fix nothing, write nothing outside $TMPDIR (except the transient `sbx-test` touch/rm the test itself requires).

**Where**: `/home/luca/repos/gram`, branch `main`, no file changes, no commits.

## Steps
1. **Done in plan mode (read-only)**: `git check-ignore -v .claude/settings.local.json` → `/home/luca/.config/git/ignore:4:.claude/settings.local.json`, exit 0 → **PASS**.
2. Sandboxed `ls ~/repos` shows only `gram` (other entries masked), so I can't pick a sibling myself. I'll ask you to name one and type `/add-dir ~/repos/<sibling>`. Then:
   - sandboxed `touch <dir>/sbx-test && rm <dir>/sbx-test`
   - sandboxed `git -C <dir> ls-files | head -1`, then `cat` that file (`head -5`)
   - Expectation per CLAUDE.md: `/add-dir` grants Edit-tool access, not Bash reads/writes → both likely FAIL. That is the result to report, no workaround.
3. Sandboxed `git fetch` → expect ssh/proxy failure; retry with `dangerouslyDisableSandbox: true` (you approve). Note: a successful fetch updates `.git` remote refs (expected side effect of the test).
4. Edit/Write tool creating `~/repos/<sibling>/sbx-edit-test.txt` → expect permission prompt; you decline → PASS if declined/no file.
5. Sandboxed `cat ~/.ssh/id_ed25519.pub`, then Read tool on the same path → both must fail. No retry, no allowlist suggestion.
6. `matlab -batch "disp(1+1)"` twice, `timeout: 240000`, output to `$TMPDIR/matlab{1,2}.log`, report `2` + wall time each.

## Decisions
- Step 2 sibling: your choice (I can't see siblings).
- Step 2 tracked file: first entry of `git ls-files` there.
- Step 6 timeout: 240 s as specified; no sandbox bypass if it fails — report it.

## Check / output
Final 6-row table: Step | Result | Evidence.
**Docs**: none.
