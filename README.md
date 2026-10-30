<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo-light.svg" alt="writing-rules logo" width="112">
  </picture>
</p>

<h1 align="center">writing-rules</h1>

<p align="center">
  Academic writing rules for Claude, distilled from real paper-editing sessions.
</p>

<p align="center">
  <a href="LICENSE"><img alt="Rules: CC BY 4.0" src="https://img.shields.io/badge/rules-CC%20BY%204.0-1f2937"></a>
  <a href="LICENSE-CODE"><img alt="Code: MIT" src="https://img.shields.io/badge/code-MIT-1f2937"></a>
  <img alt="Requires Claude Code" src="https://img.shields.io/badge/requires-Claude%20Code-b91c1c">
</p>

---

When Claude drafts or edits a paper, researchers keep making the same corrections: define this term, this reads like AI, don't refer to the previous draft, "rather than" again. This repository collects those corrections into a Claude Code plugin, so that you don't have to repeat them.

The first version comes from about 1,000 corrections made by one researcher over one year of experimenting with academic writing using Claude Code. The goal is to grow it with corrections from many researchers, in two commands per contributor.

> **Status: very first version.** The rules currently reflect a single researcher's corrections. Rules that turned out to be one person's taste have been left out, and the rest will be improved progressively as contributions come in: rules that other researchers confirm will move up, and rules that turn out to be individual preferences will be scoped, made optional or moved out.

**Who this is for.** The rules are only as good as the reviewing behind them. They come from researchers who read what Claude writes line by line, push back, and ask for changes until the text says exactly what they mean. If you use Claude to write, these rules save you from repeating the same corrections. If you contribute, your history is useful only if it contains that kind of review. Someone who accepts drafts as they come has no corrections to share.

## What it does

| Without the rules | With the rules |
|---|---|
| Rather than a single pooled number, Table 2 reports per-world accuracy &mdash; a genuinely more informative view. As revised, the effect no longer depends on the seed. | Table 2 reports the accuracy of the model on each world separately. The effect is the same for the five random seeds we tried. |

The `writing-toolkit` plugin contains two things:

- **The `academic-writing` skill.** Claude loads it whenever it drafts, edits or reviews an academic text. It holds a short core of rules that apply to every text, and detailed rules in separate files (paper structure, argumentation, mathematics, citations, position papers, submission, style) that Claude opens one at a time, only when the task needs them. This keeps Claude's attention on the rules that matter for what it is doing.
- **A writing linter.** Every time Claude writes into a `.tex` file, the linter scans the new text for phrasings that read as AI-generated ("rather than", em dashes, ", not X" contrasts, "genuinely", "testbed", ...) and asks Claude to rewrite them. You can also run it yourself.

## Install

In Claude Code (version 2.1.275 or later):

```
/plugin install writing-toolkit --marketplace Sfgangloff/writing-rules
```

With an older version, add the marketplace first: `/plugin marketplace add Sfgangloff/writing-rules`, then `/plugin install writing-toolkit@writing-rules`.

The linter needs `python3`. To use the rules without Claude Code, in the Claude apps, zip the folder [`plugin/skills/academic-writing`](plugin/skills/academic-writing) and upload it as a skill in the settings (the linter does not run there). With another assistant, give it [`SKILL.md`](plugin/skills/academic-writing/SKILL.md) and the files in `reference/`.

## Make it yours

### Personal rules

Write your own rules in a Markdown file. Claude reads it before writing, and it takes precedence over the default rules:

- `~/.claude/writing-rules/personal.md` for all your projects;
- `.claude/writing-rules/personal.md` in a project, for that project only (it takes precedence over the first).

Write one instruction per line, as you would say it to Claude:

```markdown
- Single author: use "I".
- Write "problem" instead of "task".
- Section titles in sentence case.
- Track changes in color.
```

The last line turns on an **optional practice**. These are habits that help many authors without being good defaults, such as writing every change in blue for review and removing the color only after you approve it. The available practices, and the line that turns each one on, are listed in [`reference/optional-practices.md`](plugin/skills/academic-writing/reference/optional-practices.md).

### Linter rules

The default rules are in [`lint_rules.json`](plugin/skills/academic-writing/scripts/lint_rules.json). Each rule has a regular expression, a message, and optionally a default replacement. To change them, create `~/.claude/writing-rules/lint.json` (all projects) or `.claude/writing-rules/lint.json` (one project), in the same format. A rule with an existing `id` changes that rule, and a new `id` adds a rule:

```json
{
  "hook_extensions": [".tex", ".md"],
  "rules": [
    {"id": "rather-than", "enabled": false},
    {"id": "em-dash", "replace": " - "},
    {"id": "utilize", "pattern": "\\butiliz(e|es|ed|ing)\\b", "message": "write \"use\""}
  ]
}
```

`hook_extensions` sets the files the hook checks (`.tex` by default). To run the linter yourself, use the script in the installed plugin, or in a clone of this repository:

```bash
python3 plugin/skills/academic-writing/scripts/lint_text.py paper.tex         # report
python3 plugin/skills/academic-writing/scripts/lint_text.py --fix paper.tex   # apply the replacements
python3 plugin/skills/academic-writing/scripts/lint_text.py --list            # show the active rules
```

A replacement is applied only by `--fix`. When Claude gets a report, it treats the replacement as a suggestion and restructures the sentence if that reads better.

## Contribute your corrections

If you review Claude's academic writing closely, your Claude Code history already contains the corrections you make most often. Two commands turn it into a contribution. If `draft` finds few corrections in your history, that is a sign the contribution would add little: there is no need to submit it.

**Requirements:** [Claude Code](https://docs.claude.com/en/docs/claude-code) with a Claude subscription, `git`, `python3`, and the [GitHub CLI](https://cli.github.com) logged in (`gh auth login`). For now, only Claude Code sessions are supported. Conversations in the Claude web or desktop apps are not stored locally.

```bash
git clone https://github.com/Sfgangloff/writing-rules.git
cd writing-rules

tools/contribute.sh draft     # 1. Claude drafts your contribution
tools/contribute.sh submit    # 2. after your review: check, commit, open a pull request
```

**1. `draft`** extracts the messages you typed in Claude Code (`~/.claude/projects`), each with the change Claude had just made to your text and the change it made in reply, so that a correction such as "remove this" can be read with what it removed. Claude keeps only corrections to academic texts, works out the rule behind each one, groups them into rules and writes `contributions/contributor-<random id>.md`. It also writes a privacy report listing what it left out, in `.contribution/privacy_report.md`, which is never committed. Reading everything takes 10 to 40 minutes, depending on your history. To limit it to some projects, add `--filter <part of the project folder name>`.

**2. Review the file.** Read it, and edit or delete anything you like.

**3. `submit`** never modifies your file. It runs four checks and stops at the first failure:

1. The contribution file must be the only change in the repository.
2. A mechanical scan finds emails, URLs, file paths, phone numbers, ID-like strings, and your own name, git email and GitHub login.
3. Claude reviews the file in read-only mode for anything identifying: people, institutions, projects, unpublished work.
4. If everything passes, it commits the file under the identity "Anonymous contributor", pushes it to your fork, and opens a pull request with a one-line description.

If a check fails, fix the file and run `submit` again. If the push or the pull request is interrupted, running `submit` again picks up where it stopped.

**Contributing again.** Run the same two commands some months later. `draft` updates your existing file with your new corrections, and `submit` opens a pull request that updates it. The id of your contribution is stored in `.contribution/id` in your clone. In a new clone, restore it with `tools/contribute.sh draft --id contributor-<id>`.

## Anonymity

The **content** of a contribution is anonymous by design. The file name is random, the commit author is "Anonymous contributor", and two independent checks look for identifying details before anything is pushed. Every pull request is checked again by [a GitHub workflow](.github/workflows/check-contribution.yml).

The **pull request itself** is opened from your GitHub account, and GitHub shows that account publicly. If you want to stay completely anonymous, run `submit` while logged in to a separate GitHub account (`gh auth login`).

Your raw messages, the passages of your texts extracted with them, and the privacy report (`.contribution/`) are git-ignored and are never published. Examples in the contribution are rewritten generically, and both checks look for passages that would identify your work. Like any Claude Code session, `draft` and `submit` send what Claude reads to Anthropic for processing, under your usual Claude terms; only the contribution file you reviewed is pushed to GitHub.

## How contributions are merged

Contributions are merged into the skill with [`tools/prompts/synthesis.md`](tools/prompts/synthesis.md):

- Reading rules that several contributors share move up, and the most important ones go into the core of the skill.
- Preferences on which contributors disagree are kept with their scope ("in position papers", "for single-author papers"). The synthesis does not choose a side.
- Practices that help some authors but should not be defaults become optional practices.
- Taste specific to one person stays in that person's contribution file, and in their own `personal.md`.

Each synthesis is recorded in [`SYNTHESIS_LOG.md`](SYNTHESIS_LOG.md).

## Repository layout

```
.claude-plugin/marketplace.json     makes this repository a plugin marketplace
plugin/                             the writing-toolkit plugin
  skills/academic-writing/
    SKILL.md                        core rules, loaded when Claude writes academic text
    reference/                      detailed rules, opened one at a time when needed
    scripts/lint_text.py            the writing linter
    scripts/lint_rules.json         its default rules
  hooks/hooks.json                  runs the linter after Claude edits a .tex file
contributions/                      one file per contributor, plus TEMPLATE.md
                                    (sfgangloff.md is the maintainer's own, named file)
tools/contribute.sh                 the two contribution commands
tools/extract_messages.py           extracts your messages from Claude Code transcripts
tools/check_anonymity.py            mechanical anonymity scan
tools/prompts/                      prompts for drafting, reviewing and synthesizing
tests/                              tests of the scripts (python3 -m unittest discover tests)
```

## License

The rules and other texts are licensed under [CC BY 4.0](LICENSE). The code (`tools/`, `tests/` and the scripts and configuration of the plugin) is licensed under [MIT](LICENSE-CODE).
