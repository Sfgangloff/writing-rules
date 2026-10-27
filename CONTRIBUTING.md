# Contributing

## Adding your corrections

Run the two commands described in the [README](README.md#contribute-your-corrections):

```bash
tools/contribute.sh draft
tools/contribute.sh submit
```

A contribution pull request adds or updates exactly one file, `contributions/contributor-<id>.md`, and nothing else. A GitHub workflow checks this, and scans the file for identifying details.

## Proposing a change to the rules or the tools

Open an issue or a pull request. For a change to the rules (`plugin/skills/academic-writing/`), give one or two concrete before/after examples, and say whether the rule is a reading rule (it helps any reader) or a preference. For a new linter rule, add a test in `tests/test_lint_text.py`.

Run the tests before opening a pull request:

```bash
python3 -m unittest discover tests
claude plugin validate plugin
```

## Maintainers: merging contributions

When a few contributions have arrived, run the prompt in `tools/prompts/synthesis.md` in Claude Code at the repository root, review the diff of the skill, run the tests, and record the synthesis in `SYNTHESIS_LOG.md`. Raise the `version` in `plugin/.claude-plugin/plugin.json` so that installed plugins update.
