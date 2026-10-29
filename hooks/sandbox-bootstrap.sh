#!/bin/bash
# SessionStart: sandbox denyRead covers ~/, so give each repo read access to itself via its .claude/settings.local.json.
cwd=$(jq -r '.cwd // empty')
cd "${cwd:-.}" 2>/dev/null || exit 0
root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
[ "$(realpath "$root")" = "$(realpath ~/.claude)" ] && exit 0

python3 - "$root" <<'EOF'
import json, os, sys
root = sys.argv[1]
f = os.path.join(root, ".claude", "settings.local.json")
try:
    with open(f) as fh:
        s = json.load(fh)
except FileNotFoundError:
    s = {}
except ValueError:
    sys.exit(0)  # leave a hand-broken file alone
reads = s.setdefault("sandbox", {}).setdefault("filesystem", {}).setdefault("allowRead", [])
if root in reads:
    sys.exit(0)
reads.append(root)
os.makedirs(os.path.dirname(f), exist_ok=True)
with open(f, "w") as fh:
    json.dump(s, fh, indent=2)
    fh.write("\n")
print(f"Sandbox: added {root} to sandbox.filesystem.allowRead in .claude/settings.local.json.")
EOF

# Keep the personal settings file (it holds an absolute path) out of git.
git check-ignore -q .claude/settings.local.json 2>/dev/null \
  || echo ".claude/settings.local.json" >> "$(git rev-parse --git-path info/exclude)"
exit 0
