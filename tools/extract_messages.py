#!/usr/bin/env python3
"""Extract the messages you typed in Claude Code sessions, for local analysis.

Reads the transcripts Claude Code stores under ~/.claude/projects/*/*.jsonl and
writes your own messages to a text file, oldest first. A correction such as
"remove this" means little without the text it refers to, so each message comes
with the change Claude had just made to a text file (.tex, .md, ...) before it,
and the change Claude made in reply, when there are such changes:

    === [YYYY-MM-DD] <project>
    <message>
    --- before the message, Claude had changed paper.tex:
    - <removed text>
    + <added text>
    --- in reply, Claude changed paper.tex:
    - <removed text>
    + <added text>

Claude's chat replies and tool results are left out. Terminal output pasted
into the chat (shell prompts, tracebacks, job logs) is dropped, and long texts
are truncated, so the file stays focused on corrections. The output file stays
local: it contains passages of your texts, is raw material for
`tools/contribute.sh draft`, and must never be committed.

Usage:
    python3 tools/extract_messages.py [--out user_messages.txt]
                                      [--projects ~/.claude/projects]
                                      [--filter SUBSTRING ...]
                                      [--no-changes]
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
# Files whose changes are writing, not code.
TEXT_EXTENSIONS = (".tex", ".md", ".txt", ".bib", ".rst", ".typ", ".org", ".qmd", ".rmd")
MAX_CHANGE_CHARS = 400


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


def shorten(text, limit=MAX_CHANGE_CHARS):
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 100] + " [...] " + text[-90:]


def text_changes(entry):
    """Return the changes an assistant entry made to text files, as printable blocks."""
    if entry.get("type") != "assistant" or entry.get("isSidechain"):
        return []
    content = entry.get("message", {}).get("content")
    if not isinstance(content, list):
        return []
    changes = []
    for part in content:
        if not isinstance(part, dict) or part.get("type") != "tool_use":
            continue
        tool_input = part.get("input") or {}
        path = tool_input.get("file_path", "")
        if not path.lower().endswith(TEXT_EXTENSIONS):
            continue
        name = os.path.basename(path)  # never the full path: it can contain a username
        if part.get("name") == "Write":
            changes.append((name, f"(new version of the file)\n+ {shorten(tool_input.get('content', ''))}"))
            continue
        edits = tool_input.get("edits") or [tool_input]  # MultiEdit or Edit
        for edit in edits:
            if "new_string" in edit:
                changes.append((name, f"- {shorten(edit.get('old_string', ''))}\n+ {shorten(edit['new_string'])}"))
    return changes


# The home directory at the start of a transcript folder name: -Users-me- (macOS),
# -home-me- (Linux), C--Users-me- (Windows).
HOME_PREFIX = re.compile(r"^(?:[A-Za-z]-)?-(?:Users|home)-[^-]+-?")


def project_name(path):
    """Turn a transcript folder name like -Users-me-Desktop-Paper into Desktop-Paper."""
    folder = os.path.basename(os.path.dirname(path))
    return HOME_PREFIX.sub("", folder).lstrip("-") or "home"


def read_session(path):
    """Yield (timestamp, text, change before, change after) for each message of a transcript.

    The change before is the last change Claude made to a text file since the
    previous message; the change after is the first one it made in reply.
    """
    current = None  # the message waiting for Claude's reply
    last_change = None
    with open(path, errors="ignore") as handle:
        for line in handle:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            text = message_text(entry)
            if text is not None:
                if current:
                    yield current
                current = [entry.get("timestamp", ""), text, last_change, None]
                last_change = None
                continue
            for change in text_changes(entry):
                if current and current[3] is None:
                    current[3] = change
                last_change = change
    if current:
        yield current


def format_change(label, change):
    name, body = change
    return f"--- {label}, Claude {'had changed' if label.startswith('before') else 'changed'} {name}:\n{body}\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="user_messages.txt")
    parser.add_argument("--projects", default="~/.claude/projects")
    parser.add_argument("--filter", nargs="*", default=[],
                        help="keep only projects whose name contains one of these substrings")
    parser.add_argument("--no-changes", action="store_true",
                        help="leave out the changes Claude made to text files")
    args = parser.parse_args()

    seen, messages = set(), []
    for path in glob.glob(os.path.join(os.path.expanduser(args.projects), "*", "*.jsonl")):
        project = project_name(path)
        if args.filter and not any(f.lower() in project.lower() for f in args.filter):
            continue
        for timestamp, text, before, after in read_session(path):
            if len(text) < 12 or text in seen or len(NOISE.findall(text)) >= 2:
                continue
            seen.add(text)
            if len(text) > MAX_CHARS:
                text = text[:1200] + " [...] " + text[-300:]
            block = f"{text}\n"
            if not args.no_changes:
                if before:
                    block += format_change("before the message", before)
                if after:
                    block += format_change("in reply", after)
            messages.append((timestamp, project, block))

    messages.sort()
    with open(args.out, "w") as out:
        for timestamp, project, block in messages:
            out.write(f"=== [{timestamp[:10]}] {project}\n{block}")
    print(f"wrote {len(messages)} messages to {args.out}")


if __name__ == "__main__":
    main()
