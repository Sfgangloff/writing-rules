---
name: academic-writing
description: Rules for writing, editing and reviewing academic text (research papers, position papers, research proposals, grant memos, experiment reports, theses), distilled from researchers' corrections of Claude's drafts. Use whenever you draft, edit, compress, restructure or review such a text, in LaTeX, Markdown or plain prose.
---

# Academic writing

These rules come from corrections that researchers made to Claude's academic writing, again and again. The core rules below apply to every academic text. Detailed rules are in the `reference/` files next to this one: read a file only when the task needs it (see the table at the end).

## 1. The author's own rules come first

Before writing, check for personal rules and read the ones that exist:

1. `.claude/writing-rules/personal.md` in the current project or one of its parent directories
2. `~/.claude/writing-rules/personal.md`

A personal rule overrides any rule of this skill, and a project rule overrides a user rule. An instruction the author gives in the conversation overrides both. If a personal file turns on an optional practice (for example "track changes in color"), read `reference/optional-practices.md` for how to apply it.

## 2. Core rules

These are ordered by how often authors needed them.

**What the reader sees**

1. **Never refer to what the reader cannot see.** The reader has only the current version of the text. Do not mention earlier drafts ("no longer", "as revised"), internal files, scripts, stage names or chat discussions, and do not narrate how a result was found or how an error was corrected. Remove editorial notes.
2. **Define every term and symbol at its first use**, just before it is needed. Use one name per concept and one meaning per symbol, everywhere, including appendices and captions. Never rely on an example or argument the reader has not seen yet.
3. **Explain simple things simply.** If the idea is simple, the sentence must be simple. Prefer plain words to sophisticated ones.
4. **Remove what does not help the reader**: repeated ideas, sentences that describe the paper instead of saying something ("This section fixes the notions used throughout"), announcements of what will not be done, and evidence the argument does not need.
5. **No vague references.** If the referent of "this", "these", "the two" or "both" is more than a sentence away, name it again.
6. **Connect ideas.** Say how each paragraph follows from the previous one. Re-read the surrounding paragraph after every deletion or move, so that no sentence is left orphaned.

**Claims and evidence**

7. **Neither undersell nor oversell.** Do not add sentences that give reasons to doubt the work or make it sound smaller. Do not make absolute claims when a nuanced one is correct, and do not claim a solution you do not have.
8. **Introduce every table and figure** in the text before it appears, and say which experiment it reports. When you quote a number, give the point of comparison.
9. **Verify instead of guessing.** Check that every reference exists, has correct metadata and supports the sentence where it is cited. Check facts, dates and summaries of other people's work before writing them.

**Style**

10. **Avoid patterns that read as AI-generated**: "X, not Y" contrasts and defensive appositives, "rather than", em dashes, a colon followed by an explanation in sentence after sentence, triplets, fragment sentences, and words such as "genuinely", "testbed" or "load-bearing". `reference/style.md` lists them with rewrites.

**Working with the author**

11. **Understand, then write. Do not transcribe.** An idea the author explains in chat is a seed. Write it in your own academic prose, where it belongs, without their casual phrasing and without explanations that were meant only for you.
12. **Edit exactly the requested scope, and apply global changes globally.** Removing one sentence means removing that sentence only. Compressing must never lose information. A renamed term or new notation is updated everywhere, and you verify it before reporting it done.
13. **Think about every edit, even trivial ones.** If a requested edit is wrong, introduces an inconsistency or misses the point, say so. When asked for your opinion, give one with reasons.

## 3. Detailed rules

Read a file when the task calls for it, not before.

| File | Read it when |
|---|---|
| `reference/clarity.md` | drafting or rewriting prose, defining terms and notation, giving examples, removing repetition |
| `reference/paper-structure.md` | writing or reorganizing a title, abstract, introduction, section, related work, results, limitations or appendix, or cutting to a page limit |
| `reference/argumentation.md` | writing claims, hedges, answers to reviewers, or a section that argues for a thesis |
| `reference/math.md` | writing definitions, theorems, proofs or notation |
| `reference/figures-and-latex.md` | making figures or tables, or fixing LaTeX layout |
| `reference/citations.md` | adding, checking or cleaning references |
| `reference/position-papers.md` | writing a position paper |
| `reference/submission.md` | preparing a submission or a camera-ready or arXiv version |
| `reference/style.md` | writing any prose (the AI-generated patterns, with rewrites), and during the self-review |
| `reference/collaboration.md` | editing a text with the author over several rounds, or writing a report |
| `reference/optional-practices.md` | a personal rule or the author turns on an optional practice (tracked changes in color, replies to co-author comments) |

## 4. Self-review before handing text back

1. Check every term and symbol: defined at first use, one name per concept, one meaning per symbol.
2. Check every "this", "these", "the two" and "both".
3. Look for references to earlier versions, internal files and the conversation.
4. Look for repeated ideas, meta-commentary and orphan sentences.
5. Check that every table and figure is introduced before it appears.
6. Check that no claim is undersold or oversold, and that summaries of others' work are accurate.
7. Read the text as a reviewer who does not know the material. Where would they stop, and what would they ask?
8. Run the linter on the files you changed, from this skill's directory: `python3 scripts/lint_text.py <file>`. Rewrite what it flags (restructure the sentence if the default replacement reads badly), unless the author's rules allow it.
9. Report what you changed. Do not claim a global change you did not verify.
