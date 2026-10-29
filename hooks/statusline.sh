#!/bin/bash
# Status line: model · context used · git branch, flagged when the session sits in a linked worktree.
IFS=$'\x1f' read -r model pct dir < <(jq -r '[.model.display_name // "?", (.context_window.used_percentage // "" | tostring), .workspace.current_dir // .cwd // "."] | join("\u001f")')
out="$model"
[ -n "$pct" ] && out+=" · ctx ${pct%.*}%"
if top=$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null); then
  branch=$(git -C "$dir" branch --show-current)
  out+=" · ${branch:-detached@$(git -C "$dir" rev-parse --short HEAD)}"
  # A linked worktree has its own git dir, distinct from the shared common dir.
  [ "$(git -C "$dir" rev-parse --absolute-git-dir)" != "$(git -C "$dir" rev-parse --path-format=absolute --git-common-dir)" ] \
    && out+=" · ⚠ worktree $(basename "$top")"
fi
printf '%s' "$out"
