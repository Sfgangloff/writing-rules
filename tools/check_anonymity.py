#!/usr/bin/env python3
"""Mechanical anonymity check for contribution files.

Flags patterns that should never appear in a contribution: emails, URLs,
local file paths, phone numbers, IBAN-like and other long ID strings,
@handles, and any identity string passed with --forbid (the contributor's
name, git email, GitHub login, ...). Exits with status 1 if anything is found.

This complements the review by Claude in tools/contribute.sh; it is also run
on every pull request by .github/workflows/check-contribution.yml.

Usage:
    python3 tools/check_anonymity.py FILE [FILE ...] [--forbid STRING ...]
"""

import argparse
import re
import sys

PATTERNS = {
    "email": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "URL": r"https?://\S+|www\.\S+",
    "file path": r"(/Users/|/home/|[A-Za-z]:\\Users\\|~/)\S*",
    "phone number": r"\+\d[\d ().-]{7,}\d",
    "IBAN-like string": r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,}",
    "long ID string": r"\b(?=[A-Z0-9]*\d)(?=[A-Z0-9]*[A-Z])[A-Z0-9]{8,}\b",
    "@handle": r"(?<![\w.])@[A-Za-z0-9-]{2,}",
}


# Parts of email addresses that identify nobody.
GENERIC_PARTS = {"com", "org", "net", "edu", "gmail", "mail", "users", "noreply", "github"}


def forbidden_terms(values):
    """Split identity strings into searchable terms (full strings and name parts)."""
    terms = {}
    for value in values:
        value = value.strip()
        if not value:
            continue
        parts = [value] + re.split(r"[\s._@+-]+", value)
        for part in parts:
            if len(part) >= 3 and part.lower() not in GENERIC_PARTS:
                terms.setdefault(part.lower(), part)
    return sorted(terms.values())


def check(path, forbid):
    problems = []
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            for label, pattern in PATTERNS.items():
                for match in re.finditer(pattern, line):
                    problems.append((number, label, match.group(0)))
            for term in forbid:
                if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", line, re.I):
                    problems.append((number, "identity string", term))
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--forbid", nargs="*", default=[])
    args = parser.parse_args()

    forbid = forbidden_terms(args.forbid)
    found = False
    for path in args.files:
        for number, label, text in check(path, forbid):
            found = True
            print(f"{path}:{number}: {label}: {text}")
    if found:
        sys.exit(1)
    print("anonymity check: no issue found")


if __name__ == "__main__":
    main()
