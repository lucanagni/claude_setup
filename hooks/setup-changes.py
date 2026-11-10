#!/usr/bin/env python3
"""SessionStart/Stop (sessions in ~/.claude only): track setup changes the reports in reports/ don't cover yet.

Compares the setup files (CLAUDE.md, settings.json, .gitignore, hooks/, agents/, own skills/) with the snapshot
taken at the last report sync and writes the difference to reports/.sync/pending.json, for /sync-setup-reports.
  setup-changes.py           hook mode: reads the hook JSON on stdin
  setup-changes.py --check   refresh pending.json now, print the changed paths
  setup-changes.py --stamp   take a new snapshot (reports are current) and drop pending.json"""
import difflib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.home() / ".claude"
SYNC = ROOT / "reports" / ".sync"
SNAP = SYNC / "snapshot"
PENDING = SYNC / "pending.json"
FILES = ["CLAUDE.md", "settings.json", ".gitignore"]
DIRS = ["hooks", "agents", "skills"]
SKIP = {"skills/synced"}  # claude.ai syncs, not Luca's edits


def setup_files(base):
    out = {}
    for f in FILES:
        if (base / f).is_file():
            out[f] = base / f
    for d in DIRS:
        for p in sorted((base / d).rglob("*")):
            rel = p.relative_to(base).as_posix()
            if p.is_file() and not any(rel == s or rel.startswith(s + "/") for s in SKIP) \
                    and "__pycache__" not in p.parts:
                out[rel] = p
    return out


def read(p):
    try:
        return p.read_text().splitlines(keepends=True)
    except (UnicodeDecodeError, OSError):
        return [f"<binary {p.stat().st_size} bytes>\n"]


def refresh():
    """Write pending.json (or remove it when nothing changed); return the changed entries."""
    old, new = setup_files(SNAP), setup_files(ROOT)
    changed, diff = [], []
    for rel in sorted(old.keys() | new.keys()):
        a = read(old[rel]) if rel in old else []
        b = read(new[rel]) if rel in new else []
        if a == b:
            continue
        changed.append({"path": rel, "status": "added" if rel not in old else "removed" if rel not in new else "modified"})
        diff += difflib.unified_diff(a, b, f"snapshot/{rel}", rel)
    if changed:
        SYNC.mkdir(parents=True, exist_ok=True)
        PENDING.write_text(json.dumps({"generated": time.strftime("%Y-%m-%d %H:%M"), "changed": changed,
                                       "diff": "".join(diff)}, indent=1))
    else:
        PENDING.unlink(missing_ok=True)
    return changed


def stamp():
    shutil.rmtree(SNAP, ignore_errors=True)
    for rel, p in setup_files(ROOT).items():
        (SNAP / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, SNAP / rel)
    PENDING.unlink(missing_ok=True)


def in_setup_repo(cwd):
    try:
        top = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return False
    return os.path.realpath(top) == os.path.realpath(ROOT)


def main():
    if "--stamp" in sys.argv:
        stamp()
        return
    if "--check" in sys.argv:
        for c in refresh():
            print(f"{c['status']:9} {c['path']}")
        return
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    if not SNAP.is_dir() or not in_setup_repo(event.get("cwd") or "."):
        return
    changed = refresh()
    if changed and event.get("hook_event_name") == "SessionStart":
        print(f"Setup reports: {len(changed)} setup file(s) changed since the last report sync "
              f"({', '.join(c['path'] for c in changed[:5])}{', …' if len(changed) > 5 else ''}). "
              "Remind the user that /sync-setup-reports updates reports/ when they are done editing.")


if __name__ == "__main__":
    main()
