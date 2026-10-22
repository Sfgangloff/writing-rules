#!/usr/bin/env python3
"""Extract the messages you typed in Claude Code sessions, for local analysis.

Reads the transcripts Claude Code stores under ~/.claude/projects/*/*.jsonl and
writes only your own messages (no assistant output, no tool results) to a text
file, oldest first, one block per message:

    === [YYYY-MM-DD] <project>
    <message>

Terminal output pasted into the chat (shell prompts, tracebacks, job logs) is
dropped, and long pastes are truncated, so the file stays focused on what you
asked for. The output file stays local: it is raw material for
`tools/contribute.sh draft` and must never be committed.

Usage:
    python3 tools/extract_messages.py [--out user_messages.txt]
                                      [--projects ~/.claude/projects]
                                      [--filter SUBSTRING ...]
"""

import argparse
import glob
import json
import os
import re

# Lines that indicate pasted terminal output rather than writing feedback.
NOISE = re.compile(
    r"Traceback|^\s*File \"|^\s*\$ |@[\w.-]+:[~/]|sbatch|squeue|sacct|Epoch \d"
    r"|pip install|Collecting |Downloading|Requirement already|npm (ERR|WARN)"
    r"|^\s*at [\w.$]+\(|error: |Error: ",
    re.M,
)
SKIP_PREFIXES = (
    "<command", "<local-command", "<task-notification", "<bash-",
    "Caveat:", "[Request interrupted",
)
MAX_CHARS = 1500


def message_text(entry):
    """Return the text typed by the user in a transcript entry, or None."""
    if entry.get("type") != "user" or entry.get("isMeta") or entry.get("isSidechain"):
        return None
    content = entry.get("message", {}).get("content")
    if isinstance(content, list):
        content = "\n".join(
            part.get("text", "")
            for part in content
            if isinstance(part, dict) and part.get("type") == "text"
        )
    if not isinstance(content, str):
        return None
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", content, flags=re.S).strip()
    if not text or text.startswith(SKIP_PREFIXES) or "This session is being continued" in text[:300]:
        return None
    return text


def project_name(path):
    """Turn a transcript folder name like -Users-me-Desktop-Paper into Desktop-Paper."""
    folder = os.path.basename(os.path.dirname(path))
    return re.sub(r"^-Users-[^-]+-", "", folder).lstrip("-") or folder


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="user_messages.txt")
    parser.add_argument("--projects", default="~/.claude/projects")
    parser.add_argument("--filter", nargs="*", default=[],
                        help="keep only projects whose name contains one of these substrings")
    args = parser.parse_args()

    seen, messages = set(), []
    for path in glob.glob(os.path.join(os.path.expanduser(args.projects), "*", "*.jsonl")):
        project = project_name(path)
        if args.filter and not any(f.lower() in project.lower() for f in args.filter):
            continue
        with open(path, errors="ignore") as handle:
            for line in handle:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                text = message_text(entry)
                if text is None or len(text) < 12 or text in seen:
                    continue
                if len(NOISE.findall(text)) >= 2:
                    continue
                seen.add(text)
                if len(text) > MAX_CHARS:
                    text = text[:1200] + " [...] " + text[-300:]
                messages.append((entry.get("timestamp", ""), project, text))

    messages.sort()
    with open(args.out, "w") as out:
        for timestamp, project, text in messages:
            out.write(f"=== [{timestamp[:10]}] {project}\n{text}\n")
    print(f"wrote {len(messages)} messages to {args.out}")


if __name__ == "__main__":
    main()
