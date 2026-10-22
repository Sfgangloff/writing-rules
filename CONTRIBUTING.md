# Contributing

## Adding your corrections

Run the two commands described in the [README](README.md#contribute-your-corrections):

```bash
tools/contribute.sh draft
tools/contribute.sh submit
```

A contribution pull request adds exactly one file, `contributions/contributor-<id>.md`, and nothing else. A GitHub workflow checks this, and scans the file for identifying details.

## Proposing a change to the rules or the tools

Open an issue or a pull request. For a change to `WRITING_RULES.md`, give one or two concrete before/after examples, and say whether the rule is a reading rule (Part I) or a preference (Parts II and III).

## Maintainers: merging contributions

When a few contributions have arrived, run the prompt in `tools/prompts/synthesis.md` in Claude Code at the repository root, review the diff of `WRITING_RULES.md`, and record the synthesis in `SYNTHESIS_LOG.md`.
