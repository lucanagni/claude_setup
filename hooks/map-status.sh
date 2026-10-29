#!/bin/bash
# SessionStart: tell Claude when the repo has no project map, or when source files moved since the map was verified.
cwd=$(jq -r '.cwd // empty')
cd "${cwd:-.}" 2>/dev/null || exit 0
root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
map="$root/CLAUDE.md"

if [ ! -f "$map" ]; then
  echo "Project map: no CLAUDE.md at $root. At the first code task, tell the user and offer /sync-claude-md."
  exit 0
fi

sha=$(grep -oP '<!-- verified: \K[0-9a-f]+' "$map" | head -1)
if [ -z "$sha" ] || ! git cat-file -e "$sha^{commit}" 2>/dev/null; then
  echo "Project map: $map has no verified commit in this history; treat it as unverified and offer /sync-claude-md if it contradicts the code."
  exit 0
fi

# Source files added/removed/renamed since verification (committed or not); data and outputs don't count.
src='\.(py|pyx|m|wl|wls|nb|c|h|cc|cpp|hpp|f|f90|jl|sh|ipynb)$'
moved=$(git -C "$root" diff --name-status "$sha" | awk -F'\t' '$1 ~ /^[ADR]/ {print $NF}' \
  | grep -E "$src" | grep -v ipynb_checkpoints \
  | while read -r f; do
      d=$(dirname "$f")
      grep -qF "$f" "$map" || { [ "$d" != . ] && grep -qF "$d/" "$map"; } || echo "$f"
    done)
manifests=$(git -C "$root" diff --name-only "$sha" \
  | grep -E '(^|/)(pyproject\.toml|setup\.(py|cfg)|requirements[^/]*\.txt|environment\.ya?ml|CMakeLists\.txt|Makefile)$')
n=$(grep -c . <<<"$moved")

if [ "$n" -ge 3 ] || [ -n "$manifests" ]; then
  msg="Project map: $map verified at $sha."
  [ "$n" -ge 3 ] && msg+=" Since then $n source files the map doesn't mention were added, removed or renamed: $(head -5 <<<"$moved" | paste -sd, -)$([ "$n" -gt 5 ] && echo ", …")."
  [ -n "$manifests" ] && msg+=" Manifests changed: $(paste -sd, - <<<"$manifests")."
  echo "$msg If the task touches these, tell the user the map may be stale and offer /sync-claude-md."
fi
exit 0
