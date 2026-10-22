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

When Claude drafts or edits a paper, researchers keep making the same corrections: define this term, this reads like AI, don't refer to the previous draft, "rather than" again. This repository collects those corrections into one file, [`WRITING_RULES.md`](WRITING_RULES.md), that you load at the start of a writing session so that you don't have to repeat them.

The first version comes from about 1,000 corrections made by one researcher over three months of writing ML papers, position papers and a research proposal with Claude Code. The goal is to grow it with corrections from many researchers, in two commands per contributor.

> **Status: very first version.** The rules currently reflect a single researcher's corrections, and some of them are certainly personal taste. They will be improved progressively, based on the contributions that come in: rules that other researchers confirm will move up, and rules that turn out to be individual preferences will be scoped or moved out.

**Who this is for.** The rules are only as good as the reviewing behind them. They come from researchers who read what Claude writes line by line, push back, and ask for changes until the text says exactly what they mean. If you use Claude to write, these rules save you from repeating the same corrections. If you contribute, your history is useful only if it contains that kind of review. Someone who accepts drafts as they come has no corrections to share.

## Use the rules

Reference the file from the `CLAUDE.md` of your paper's project:

```markdown
When writing or editing academic text, follow /path/to/writing-rules/WRITING_RULES.md.
```

Or attach `WRITING_RULES.md` at the start of any Claude conversation.

The file has three parts:

| Part | What it contains | How to treat it |
|---|---|---|
| **I. Reading rules** | Rules that make a text easier to read and to trust, whoever writes and reads it: define terms at first use, one name per concept, never refer to drafts the reader never saw, introduce a table before commenting on it. | Apply always. |
| **II. Style preferences** | Matters of taste: avoiding phrasings associated with AI-generated text (em dashes, "rather than"), word choices such as "problem" over "task". | Apply unless the author says otherwise. |
| **III. Working process** | How Claude should collaborate: understand ideas before writing them down, edit exactly the requested scope, mark every change for review. | Apply unless the author says otherwise. |

It ends with a self-review checklist that Claude runs before handing text back.

## Contribute your corrections

If you review Claude's academic writing closely, your Claude Code history already contains the corrections you make most often. Two commands turn it into a contribution. If `draft` finds few corrections in your history, that is a sign the contribution would add little: there is no need to submit it.

**Requirements:** [Claude Code](https://docs.claude.com/en/docs/claude-code) with a Claude subscription, `git`, `python3`, and the [GitHub CLI](https://cli.github.com) logged in (`gh auth login`). For now, only Claude Code sessions are supported. Conversations in the Claude web or desktop apps are not stored locally.

```bash
git clone https://github.com/Sfgangloff/writing-rules.git
cd writing-rules

tools/contribute.sh draft     # 1. Claude drafts your contribution
tools/contribute.sh submit    # 2. after your review: check, commit, open a pull request
```

**1. `draft`** reads the messages you typed in Claude Code (`~/.claude/projects`) on your machine and keeps only corrections to academic texts. Claude groups them into rules and writes `contributions/contributor-<random id>.md`. It also writes a privacy report listing what it left out, in `.contribution/privacy_report.md`, which never leaves your machine. Reading everything takes 10 to 40 minutes, depending on your history. To limit it to some projects, add `--filter <part of the project folder name>`.

**2. Review the file.** Read it, and edit or delete anything you like.

**3. `submit`** never modifies your file. It runs four checks and stops at the first failure:

1. The contribution file must be the only change in the repository.
2. A mechanical scan finds emails, URLs, file paths, phone numbers, ID-like strings, and your own name, git email and GitHub login.
3. Claude reviews the file in read-only mode for anything identifying: people, institutions, projects, unpublished work.
4. If everything passes, it commits the file under the identity "Anonymous contributor", pushes it to your fork, and opens a pull request with a one-line description.

If a check fails, fix the file and run `submit` again. If the push or the pull request is interrupted, running `submit` again picks up where it stopped.

## Anonymity

The **content** of a contribution is anonymous by design. The file name is random, the commit author is "Anonymous contributor", and two independent checks look for identifying details before anything is pushed. Every pull request is checked again by [a GitHub workflow](.github/workflows/check-contribution.yml).

The **pull request itself** is opened from your GitHub account, and GitHub shows that account publicly. If you want to stay completely anonymous, run `submit` while logged in to a separate GitHub account (`gh auth login`).

Your raw messages (`.contribution/`) are git-ignored and never leave your machine.

## How contributions are merged

Contributions are merged into `WRITING_RULES.md` with [`tools/prompts/synthesis.md`](tools/prompts/synthesis.md):

- Reading rules that several contributors share move up.
- Preferences on which contributors disagree are kept with their scope ("in position papers", "for single-author papers"). The synthesis does not choose a side.
- Taste specific to one person stays in that person's contribution file.

Each synthesis is recorded in [`SYNTHESIS_LOG.md`](SYNTHESIS_LOG.md).

## Repository layout

```
WRITING_RULES.md              the rules: load this file
contributions/                one file per contributor, plus TEMPLATE.md
                              (sfgangloff.md is the maintainer's own, named file)
tools/contribute.sh           the two contribution commands
tools/extract_messages.py     extracts your messages from Claude Code transcripts
tools/check_anonymity.py      mechanical anonymity scan
tools/prompts/                prompts for drafting, reviewing and synthesizing
```

## License

The rules and other texts are licensed under [CC BY 4.0](LICENSE). The code in `tools/` is licensed under [MIT](LICENSE-CODE).
