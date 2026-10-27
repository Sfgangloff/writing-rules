#!/usr/bin/env python3
"""Mechanical writing linter: flags phrasings that read as AI-generated.

The default rules are in lint_rules.json, next to this script. Each rule has
an id, a regular expression (matched case-insensitively), a message, and
optionally a replacement that --fix applies. You can change them without
editing this file:

    ~/.claude/writing-rules/lint.json          for all your projects
    <project>/.claude/writing-rules/lint.json  for one project (searched upward
                                               from the linted file)

An override file has the same format as lint_rules.json. A rule whose id
already exists updates that rule ({"id": "rather-than", "enabled": false}
turns it off, {"id": "em-dash", "replace": " - "} makes it fixable); a new id
adds a rule. In .tex files, comments (after an unescaped %) are ignored.

Usage:
    lint_text.py FILE [FILE ...]   report matches; exits with status 1 if any
    lint_text.py --fix FILE ...    also apply the replacements, in place
    lint_text.py --list [FILE]     print the active rules
    lint_text.py --hook            Claude Code PostToolUse hook: reads the hook
                                   input on stdin and lints only the text that
                                   was just written
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = os.path.join(HERE, "lint_rules.json")
USER_CONFIG = os.path.join("~", ".claude", "writing-rules", "lint.json")
PROJECT_CONFIG = os.path.join(".claude", "writing-rules", "lint.json")
MAX_HOOK_REPORTS = 20


def project_config(start):
    """Return the nearest project override file above `start`, or None."""
    directory = os.path.abspath(start)
    while True:
        candidate = os.path.join(directory, PROJECT_CONFIG)
        if os.path.isfile(candidate):
            return candidate
        parent = os.path.dirname(directory)
        if parent == directory:
            return None
        directory = parent


def load_config(start="."):
    """Merge the default rules with the user and project overrides."""
    with open(DEFAULTS, encoding="utf-8") as handle:
        config = json.load(handle)
    rules = {rule["id"]: dict(rule) for rule in config["rules"]}
    for path in (os.path.expanduser(USER_CONFIG), project_config(start)):
        if not path or not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as handle:
                override = json.load(handle)
        except (OSError, json.JSONDecodeError) as error:
            print(f"warning: ignoring {path}: {error}", file=sys.stderr)
            continue
        if "hook_extensions" in override:
            config["hook_extensions"] = override["hook_extensions"]
        for rule in override.get("rules", []):
            if "id" in rule:
                rules.setdefault(rule["id"], {}).update(rule)

    active = []
    for rule in rules.values():
        if not rule.get("enabled", True):
            continue
        try:
            rule["regex"] = re.compile(rule["pattern"], re.IGNORECASE)
        except (KeyError, re.error) as error:
            print(f"warning: skipping rule {rule['id']}: {error}", file=sys.stderr)
            continue
        active.append(rule)
    config["rules"] = active
    return config


def split_comment(line, tex):
    """Split a line into (text, comment); only .tex files have comments."""
    if tex:
        match = re.search(r"(?<!\\)%", line)
        if match:
            return line[: match.start()], line[match.start():]
    return line, ""


def keep_case(replacement, matched):
    if matched[:1].isupper() and replacement:
        return replacement[0].upper() + replacement[1:]
    return replacement


def find(text, rules, tex):
    """Yield (line number, column, rule, matched text, line) for every match."""
    for number, line in enumerate(text.splitlines(), 1):
        body, _ = split_comment(line, tex)
        for rule in rules:
            for match in rule["regex"].finditer(body):
                yield number, match.start() + 1, rule, match.group(0), line


def fix(text, rules, tex):
    """Apply every rule that has a replacement, outside comments."""
    lines = []
    for line in text.splitlines(keepends=True):
        body, comment = split_comment(line, tex)
        for rule in rules:
            if "replace" in rule:
                body = rule["regex"].sub(lambda m, r=rule: keep_case(r["replace"], m.group(0)), body)
        lines.append(body + comment)
    return "".join(lines)


def describe(rule, matched):
    note = f"[{rule['id']}] {rule['message']}: \"{matched.strip()}\""
    if "replace" in rule:
        note += f" -> \"{keep_case(rule['replace'], matched)}\""
    return note


def lint_files(paths, apply_fix):
    found = 0
    for path in paths:
        config = load_config(os.path.dirname(os.path.abspath(path)))
        tex = path.endswith(".tex")
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        matches = sorted(find(text, config["rules"], tex), key=lambda match: match[:2])
        for number, column, rule, matched, _ in matches:
            found += 1
            print(f"{path}:{number}:{column}: {describe(rule, matched)}")
        if apply_fix:
            fixed = fix(text, config["rules"], tex)
            if fixed != text:
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(fixed)
                print(f"{path}: replacements applied")
    return found


def written_text(tool_input):
    """The text an Edit, MultiEdit or Write call just put in the file."""
    if "content" in tool_input:
        return [tool_input["content"]]
    if "new_string" in tool_input:
        return [tool_input["new_string"]]
    return [edit.get("new_string", "") for edit in tool_input.get("edits", [])]


def run_hook():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    tool_input = event.get("tool_input") or {}
    path = tool_input.get("file_path", "")
    config = load_config(os.path.dirname(path) or event.get("cwd", "."))
    if not path or not path.endswith(tuple(config.get("hook_extensions", []))):
        return 0

    tex = path.endswith(".tex")
    reports = []
    for text in written_text(tool_input):
        for _, _, rule, matched, line in find(text, config["rules"], tex):
            reports.append(f"- {describe(rule, matched)}\n  in: {line.strip()[:160]}")
    if not reports:
        return 0
    shown = reports[:MAX_HOOK_REPORTS]
    if len(reports) > len(shown):
        shown.append(f"- ... and {len(reports) - len(shown)} more")
    print(
        f"The writing linter found {len(reports)} pattern(s) in the text you just wrote in {path}.\n"
        "Rewrite these passages (a replacement is only a default: restructure the sentence if it "
        "reads better), unless the author has asked to keep them:\n" + "\n".join(shown),
        file=sys.stderr,
    )
    return 2  # exit status 2 shows the report to Claude


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*")
    parser.add_argument("--fix", action="store_true", help="apply the replacements in place")
    parser.add_argument("--list", action="store_true", help="print the active rules")
    parser.add_argument("--hook", action="store_true", help="run as a Claude Code PostToolUse hook")
    args = parser.parse_args()

    if args.hook:
        sys.exit(run_hook())
    if args.list:
        start = os.path.dirname(os.path.abspath(args.files[0])) if args.files else "."
        for rule in load_config(start)["rules"]:
            replacement = f" -> \"{rule['replace']}\"" if "replace" in rule else ""
            print(f"{rule['id']}: /{rule['pattern']}/{replacement}\n    {rule['message']}")
        return
    if not args.files:
        parser.error("give at least one file")
    found = lint_files(args.files, args.fix)
    if found:
        print(f"{found} match(es)")
        sys.exit(0 if args.fix else 1)
    print("writing linter: no match")


if __name__ == "__main__":
    main()
