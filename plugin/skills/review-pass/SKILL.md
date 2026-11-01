---
name: review-pass
description: A full review pass over an academic paper draft, the way a careful author does it - a simulated reader questions the text paragraph by paragraph and the text is rewritten until it is clear, then global consistency checks, then fitting the page limits by compressing and moving material to coherent, self-contained appendices, then a final polish. Use when the author asks to review, revise or polish a whole paper or section, or to bring a paper to a page limit.
---

# Review pass

This skill revises a paper draft in successive passes, before the author's own review. It applies the rules of the `academic-writing` skill, in the directory next to this one: read `../academic-writing/SKILL.md` first, and the reference files that each phase names.

The phases come in this order because each one needs the previous one to be done: the text must be clear before it is checked for global consistency, and consistent before it is cut, since cutting an unclear text loses meaning. The author may ask for one phase only ("just fit it to 8 pages"): then run that phase, with its checks.

## 0. Preparation

1. Find the paper: the main file, the files it includes, in reading order, and which parts are the main text (the "core"), the appendices, the abstract. Note sections that the author says belong to a co-author: do not change them without asking, but do not use this as a reason to leave a global change undone.
2. Compile the paper and note the page count of the core, the warnings, undefined references and citations.
3. Create `.review/log.md` next to the paper. In it, keep the list of passages done, the questions raised, what changed, and the open questions for the author. The pass is long: the log lets you resume after an interruption, and is what the author reads at the end.
4. If the author's rules turn on tracked changes (see `../academic-writing/reference/optional-practices.md`), mark every change that way.

## 1. Clarity pass, paragraph by paragraph (core of the text)

Go through the core in reading order, one paragraph at a time. Do not worry about length in this phase.

For each paragraph:

1. **Ask a reader.** Launch the `reader` agent of this plugin (`writing-toolkit:reader`) with the list of paper files in reading order, the paragraph to examine, and where its reading must stop (the end of the paragraph). The reader knows only the text that precedes the paragraph: this is what makes its questions those of the paper's audience, which you, who know the work, cannot ask yourself.
2. **Answer in the text.** For each question, decide where the answer belongs: in this paragraph, earlier (a definition that comes too late), later, in an appendix, or nowhere (a question that the text should not answer, a misreading the text cannot prevent). Answer with what the work actually contains, from the paper, the code, the results and the conversation. Never invent a motivation, a number or a claim. A question that only the author can answer goes to the open questions of the log, and the passage is marked with a short comment in the source.
3. **Apply the local rules** to the rewritten paragraph: the core rules of `academic-writing` on terms, references, vague "this", internal names, claims, style, and `../academic-writing/reference/clarity.md` and `style.md`. Run the linter on the file: `python3 ../academic-writing/scripts/lint_text.py <file>`.
4. **Ask again**, with the rewritten paragraph, until the reader answers `clear` or only questions for the author remain. Stop after three rounds and log what is left.
5. Log the paragraph as done, and move to the next one. A change may make earlier text inconsistent (a term defined twice, a sentence that now repeats): fix it right away.

Paragraphs that only list or summarize (a list of contributions, a roadmap) can be read together with what they announce, once that has been reviewed.

## 2. Global pass

Check the whole text, appendices and captions included, against the rules that only appear at the scale of the paper. Read `../academic-writing/reference/paper-structure.md` and `argumentation.md`.

1. **Terms and notation**: one name per concept and one meaning per symbol everywhere; no name left over from an earlier version of the work; the same spelling of names in text, tables and figures.
2. **Order**: every term is defined before it is used, and no argument relies on an example that comes later.
3. **Introduction and body**: the introduction gives compressed versions of the ideas the body develops, without large overlap; a detailed explanation that sits in the introduction moves to where the body first needs it.
4. **Promises**: the title, the abstract, the contributions and the conclusion claim what the results show, no more and no less.
5. **Structure**: each paragraph opens by saying what it is about or how it relates to the previous one; parallel items (contributions, tests, cases) get comparable space and detail; tables and figures are introduced before they appear; every appendix is cited from the core.
6. **Citations**: summaries of cited works match what the works say (check the sources you can access, list the others in the open questions); statements that call for a reference have one. Read `../academic-writing/reference/citations.md`.
7. **What the reader cannot see**: search the whole source for file names, run names, version labels and references to the conversation.
8. **A reader of the whole core**: launch the `reader` agent on the whole core and ask for the questions that remain at the scale of the paper (the question studied, the main result, whether the evidence supports the claims). Treat them as in phase 1.

## 3. Length

1. **Ask the author for the limits**, unless they are already given in the conversation or in the author's rules: the page limit of the core and what it excludes (references, appendices, impact statement), and the length limit of the abstract. If you cannot ask, take them from the venue's call for papers or style files, and say so in the log.
2. Compile and measure where the core ends. If it fits, skip to phase 4.
3. Reduce the core in this order, compiling after each round of changes:
   1. **Remove repetitions**, only those that you are sure repeat an idea already stated in the text. A sentence that adds a nuance is not a repetition.
   2. **Compress formulations** without losing meaning: shorter sentences for the same content, paragraphs that end with a few words on their last line. A compressed passage must still be understood by a reader: when in doubt, ask the `reader` agent about it. Over-compression ("Jaccard 0.03 for A-B") makes the text shorter and worse.
   3. **Move to appendices** what the reader does not need to follow the paper: derivations, full lists of examples, formal versions of informal statements, extended discussions, secondary experiments. Leave in the core a sentence that states the result or the idea and cites the appendix. Plan the moves by theme, so that each appendix stays coherent (phase 4).
4. Do not delete content for any other reason, and do not change the results section unless the author asks. Do not reach the limit by layout tricks (negative spacing, smaller fonts in the text) unless the author asks.
5. **Abstract** last: compress it to its limit, keeping the question, the approach, the main result and its consequence.

## 4. Appendices

Appendices are usually not limited in length, so there is room to be pedagogical.

1. **One theme per appendix.** An appendix is not a collection of unrelated parts. Split an appendix that covers two topics, merge appendices that cover one, remove overlaps between appendices.
2. **Self-contained.** Each appendix restates the context and the result it expands on, with a reference to the section, recalls the notation it uses, and can be read without going back and forth to the core. Remove sentences that became orphans when they moved ("The same reframing ..." with nothing before it).
3. **Cited from the core**, at the place where the material it extends is discussed, as "Appendix C", not "Section C". With a single appendix, call it "the appendix".
4. **A reader of each appendix**: launch the `reader` agent on the appendix alone, after the abstract, and ask what cannot be understood without the core. Fix what it finds.

## 5. Final polish

1. Typos, grammar, and the patterns of `../academic-writing/reference/style.md`; run the linter on every file of the paper.
2. Compile: no undefined references or citations, no overfull lines in the core, figures and tables near where they are cited, page limits met.

## 6. Handing over to the author

Report, briefly, and complete `.review/log.md`:

1. what changed in each phase, with the passages the author should check first: compressions, moved material, answers you added to the reader's questions;
2. the open questions that only the author can answer, each with its location;
3. what you did not do, and why.

The author then reviews the paper. Do not describe the paper as finished or ready to submit.
