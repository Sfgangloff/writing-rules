# Writing rules for Claude

A rules file to load into any Claude thread where you write, built from what writers actually correct when Claude drafts for them, and open to contributions.

**Use it:** attach [`WRITING_RULES.md`](WRITING_RULES.md) at the start of a thread, or reference it from a `CLAUDE.md`:

```markdown
When writing or editing any text, follow /path/to/WRITING_RULES.md.
```

## Reading rules and preferences

The file separates two kinds of rules:

- **Part I - Reading rules** make a text easier to read and to trust, whoever writes it and whoever reads it. Examples: define a term before using it, use one name per concept, introduce a table before commenting on it, never refer to a draft the reader never saw.
- **Part II - Style preferences** and **Part III - Working process** are matters of taste. Examples: avoiding phrasings associated with AI-generated text (em dashes, "rather than"), preferring "problem" to "task", marking edits in blue for review.

Reading rules should converge as more writers contribute. Preferences are expected to vary, and the synthesis records the disagreements instead of hiding them.

## How it was built

Claude Code keeps a transcript of every session under `~/.claude/projects/`. The first version of the rules was extracted from one researcher's transcripts:

1. [`tools/extract_messages.py`](tools/extract_messages.py) pulled only the messages the user typed (about 2,650 messages, over three months and 49 projects: ML papers, position papers, a grant memo, experiment reports), dropping pasted terminal output.
2. Claude read all of them and kept the ones that correct a text: rewordings ("rather than -> instead of"), complaints ("this reads like AI", "I don't understand"), structural requests, and process instructions ("make the modifications in blue").
3. The corrections were grouped into rules, ordered by frequency, and written as instructions addressed to Claude.

The most frequent corrections were, in order: removing unnecessary sentences, making explanations understandable to a newcomer, marking every change for review, replacing "rather than" and "X, not Y" constructions, adding and checking citations, and a small set of word substitutions ("task" -> "problem", "ask" -> "question", "give" -> "provide"). The per-writer summary is in [`contributions/sfgangloff.md`](contributions/sfgangloff.md).

## Contribute your own

One writer's corrections are one point of view. The goal is a shared file that reflects many writers, so that it captures what reliably improves Claude's writing, and shows where preferences differ.

1. Fork and clone this repository.
2. Start Claude Code at the repository root and paste the prompt in [`tools/CONTRIBUTOR_PROMPT.md`](tools/CONTRIBUTOR_PROMPT.md). Claude extracts your messages **locally**, reads them, and drafts `contributions/<your-handle>.md` from [`contributions/TEMPLATE.md`](contributions/TEMPLATE.md).
3. Review the draft yourself, especially for privacy (see below), then open a pull request that adds only that file.

Maintainers periodically run [`tools/SYNTHESIS_PROMPT.md`](tools/SYNTHESIS_PROMPT.md) to merge all contributions into `WRITING_RULES.md`. Rules that several writers share move up. Rules that conflict are kept with their scope ("in position papers", "for single-author papers"), and personal taste stays in the contributor's own file. Each synthesis is recorded in `SYNTHESIS_LOG.md`.

## Privacy

Your transcripts contain much more than writing feedback: credentials pasted by mistake, personal documents, collaborators' names, unpublished work. Therefore:

- the raw extraction (`user_messages.txt`) is git-ignored and must never be committed;
- the contributor prompt includes a privacy pass, but **you** are responsible for reading your contribution before you push it;
- contributions contain rules and short, generic examples, never transcripts.

## Layout

```
WRITING_RULES.md            the synthesized rules (load this)
contributions/TEMPLATE.md   format for a contribution
contributions/<handle>.md   one file per writer
tools/extract_messages.py   local extraction of your Claude Code messages
tools/CONTRIBUTOR_PROMPT.md prompt to draft your contribution
tools/SYNTHESIS_PROMPT.md   prompt to merge contributions
```
