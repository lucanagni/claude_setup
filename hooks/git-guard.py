#!/usr/bin/env python3
"""PreToolUse (Bash|Agent): force a permission prompt before Claude creates, moves or deletes a git branch or worktree.

Everything else passes through to the normal permission flow."""
import json
import shlex
import sys

GLOBAL_OPTS_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
BRANCH_MODIFY = {"-m", "-M", "--move", "-c", "-C", "--copy", "-d", "-D", "--delete", "-f", "--force",
                 "-u", "--set-upstream-to", "--unset-upstream", "--track", "--no-track"}
BRANCH_QUERY = {"-l", "--list", "--contains", "--no-contains", "--merged", "--no-merged", "--points-at",
                "--sort", "--format", "--color", "--column", "--abbrev"}
OPERATORS = {"&&", "||", ";", "|", "&", "(", ")"}


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason}}))
    sys.exit(0)


def check_git(args):
    """args: tokens after `git`, up to the next shell operator."""
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in GLOBAL_OPTS_WITH_ARG else 1
    if i >= len(args):
        return
    sub, rest = args[i], args[i + 1:]
    if sub == "worktree" and rest[:1] and rest[0] in {"add", "move", "remove"}:
        ask(f"git worktree {rest[0]}: changes where work happens")
    if sub == "checkout" and any(a in {"-b", "-B", "--orphan"} for a in rest):
        ask("git checkout creates a branch")
    if sub == "switch" and any(a in {"-c", "-C", "--create", "--force-create", "--orphan"} for a in rest):
        ask("git switch creates a branch")
    if sub == "branch":
        if any(a.split("=")[0] in BRANCH_MODIFY for a in rest):
            ask("git branch modifies branches")
        positional = [a for a in rest if not a.startswith("-")]
        if positional and not any(a.split("=")[0] in BRANCH_QUERY for a in rest):
            ask(f"git branch creates branch '{positional[0]}'")


def main():
    ev = json.load(sys.stdin)
    tool, inp = ev.get("tool_name"), ev.get("tool_input") or {}
    if tool == "Agent":
        if inp.get("isolation") == "worktree":
            ask("Subagent would run in a new git worktree")
        return
    cmd = inp.get("command", "")
    if "git" not in cmd:
        return
    try:
        lex = shlex.shlex(cmd.replace("\n", " ; "), posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        tokens = list(lex)
    except ValueError:
        tokens = cmd.replace("\n", " ; ").split()
    for i, tok in enumerate(tokens):
        if tok == "git" or tok.endswith("/git"):
            end = next((j for j in range(i + 1, len(tokens)) if tokens[j] in OPERATORS), len(tokens))
            check_git(tokens[i + 1:end])


main()
