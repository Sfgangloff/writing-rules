#!/usr/bin/env bash
# Contribute your academic writing rules, anonymously.
#
#   tools/contribute.sh draft    extract your Claude Code messages and let Claude
#                                draft contributions/contributor-<id>.md
#   tools/contribute.sh submit   check the file is the only change and is anonymous,
#                                then commit it under an anonymous identity, push it
#                                and open a pull request. It never modifies the file.
#
# Requirements: Claude Code (logged in, with a subscription), git, python3,
# and the GitHub CLI (gh) logged in.

set -euo pipefail

UPSTREAM="${WRITING_RULES_UPSTREAM:-Sfgangloff/writing-rules}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$ROOT/.contribution"          # local only, git-ignored
ID_FILE="$WORK/id"

cd "$ROOT"

die() { echo "error: $*" >&2; exit 1; }

require() {
  for cmd in "$@"; do
    command -v "$cmd" >/dev/null 2>&1 || die "'$cmd' is required but not installed"
  done
}

fill() {  # fill PROMPT_FILE KEY=VALUE...: substitute {{KEY}} placeholders
  python3 -c '
import sys
text = open(sys.argv[1]).read()
for pair in sys.argv[2:]:
    key, _, value = pair.partition("=")
    text = text.replace("{{" + key + "}}", value)
sys.stdout.write(text)' "$@"
}

contribution_id() {
  [[ -f "$ID_FILE" ]] || die "no draft found, run 'tools/contribute.sh draft' first"
  cat "$ID_FILE"
}

identity_strings() {  # strings that would identify the contributor
  git config user.name 2>/dev/null || true
  git config user.email 2>/dev/null || true
  gh api user -q .login 2>/dev/null || true
  gh api user -q .name 2>/dev/null || true
  id -un 2>/dev/null || true
}

changed_files() {  # every path that differs from HEAD, untracked included
  git status --porcelain --untracked-files=all | cut -c4-
}

draft() {
  require claude python3 git
  mkdir -p "$WORK"
  [[ -f "$ID_FILE" ]] || echo "contributor-$(python3 -c 'import secrets; print(secrets.token_hex(3))')" > "$ID_FILE"
  local id; id="$(contribution_id)"
  local output="contributions/$id.md"

  echo "1/3 Extracting your messages from ~/.claude/projects (stays on this machine)..."
  python3 tools/extract_messages.py --out "$WORK/user_messages.txt" "$@"

  echo "2/3 Claude is reading them and drafting $output."
  echo "    This reads every message and can take 10 to 40 minutes."
  claude -p "$(fill tools/prompts/draft.md \
      "MESSAGES=.contribution/user_messages.txt" "NOTES=.contribution/notes.md" \
      "OUTPUT=$output" "REPORT=.contribution/privacy_report.md" "ID=$id")" \
    --tools "Read,Write,Edit,Grep" --permission-mode acceptEdits \
    --no-session-persistence >/dev/null

  [[ -f "$output" ]] || die "Claude did not write $output; run 'tools/contribute.sh draft' again"

  echo "3/3 Mechanical anonymity check:"
  local identity=()
  while IFS= read -r line; do [[ -n "$line" ]] && identity+=("$line"); done < <(identity_strings)
  python3 tools/check_anonymity.py "$output" --forbid ${identity[@]+"${identity[@]}"} || true

  cat <<EOF

Done. Please review and edit, if needed:
    $output
What Claude left out for anonymity:
    .contribution/privacy_report.md

When you are happy with it, run:
    tools/contribute.sh submit
EOF
}

submit() {
  require claude python3 git gh
  gh auth status >/dev/null 2>&1 || die "run 'gh auth login' first"
  local id; id="$(contribution_id)"
  local output="contributions/$id.md"
  [[ -f "$output" ]] || die "$output not found"

  echo "1/4 Checking that $output is the only change..."
  local changes; changes="$(changed_files)"
  [[ "$changes" == "$output" ]] || die "only $output may differ from the repository. Found:
$changes
Revert the other changes (git checkout -- <file>) and run submit again."

  local before; before="$(shasum -a 256 "$output")"

  echo "2/4 Mechanical anonymity check..."
  local identity=()
  while IFS= read -r line; do [[ -n "$line" ]] && identity+=("$line"); done < <(identity_strings)
  python3 tools/check_anonymity.py "$output" --forbid ${identity[@]+"${identity[@]}"} \
    || die "fix the lines above in $output, then run submit again"

  echo "3/4 Claude reviews the file for anonymity (read-only)..."
  local identity_text review
  identity_text="$(printf -- '- %s\n' ${identity[@]+"${identity[@]}"})"
  review="$(claude -p "$(fill tools/prompts/review.md "FILE=$output" "IDENTITY=$identity_text")" \
    --tools "Read" --no-session-persistence)"
  echo "$review"
  [[ "$(shasum -a 256 "$output")" == "$before" ]] || die "$output changed during the review; aborting"
  [[ "$(echo "$review" | grep -E '^VERDICT: (PASS|FAIL)$' | tail -1)" == "VERDICT: PASS" ]] \
    || die "the review found issues (see above). Fix them in $output, then run submit again."

  echo "4/4 Committing anonymously, pushing and opening the pull request..."
  local login branch remote head
  if [[ -n "${WRITING_RULES_DRY_RUN:-}" ]]; then  # for testing: stop before touching git
    echo "dry run: would commit $output anonymously, push it and open a pull request on $UPSTREAM"
    return
  fi
  login="$(gh api user -q .login)"
  branch="contribution/$id"
  git checkout -q -b "$branch"
  git add -- "$output"
  GIT_AUTHOR_NAME="Anonymous contributor" GIT_AUTHOR_EMAIL="anonymous@users.noreply.github.com" \
  GIT_COMMITTER_NAME="Anonymous contributor" GIT_COMMITTER_EMAIL="anonymous@users.noreply.github.com" \
    git commit -q -m "Add $id"

  if [[ "$login" == "${UPSTREAM%%/*}" ]]; then
    remote="origin"; head="$branch"
  else
    gh repo fork "$UPSTREAM" --clone=false >/dev/null 2>&1 || true
    local fork_url="https://github.com/$login/${UPSTREAM##*/}.git"
    git remote get-url fork >/dev/null 2>&1 || git remote add fork "$fork_url"
    remote="fork"; head="$login:$branch"
  fi
  for attempt in 1 2 3 4 5; do  # a new fork can take a few seconds to be ready
    git push -q -u "$remote" "$branch" && break
    [[ $attempt == 5 ]] && die "push failed"
    sleep 5
  done

  gh pr create --repo "$UPSTREAM" --base main --head "$head" \
    --title "Add $id" \
    --body "Anonymous academic writing rules contribution, generated with \`tools/contribute.sh\`."
}

case "${1:-}" in
  draft)  shift; draft "$@" ;;
  submit) submit ;;
  *) echo "usage: tools/contribute.sh draft [--filter PROJECT ...] | submit" >&2; exit 2 ;;
esac
