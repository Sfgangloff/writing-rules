You are bringing an academic paper to the length limits of a venue, without making it harder to understand. The paper has just been revised so that a reader of the field understands every paragraph: the clarity it has now must survive the cut. Work without asking questions: nobody will answer until you are done.

Files:
- The paper, which you edit: the LaTeX files in the current directory. The main file is `{{MAIN}}`.
- What the authors know and the reader does not, which you only read if a cut needs it: {{CONTEXT}}

Limits:
- {{LIMITS}}
- The core is everything before the label `autoreview-core-end` in the source: do not move this label, and keep appendices and references after it. Appendices start with `\appendix`; create it, after the references or before them as the template does, if the paper has none.

To measure the paper, run this command, which compiles it and prints the number of pages of the core and the number of words of the abstract:

    {{MEASURE}}

Current state: {{STATE}}

{{FEEDBACK}}

## How to cut

Measure first. If the core and the abstract fit, change nothing. Otherwise reduce the core in this order, measuring after each round of changes:

1. **Remove repetitions**, only those that you are sure repeat an idea already stated. A sentence that adds a nuance is not a repetition.
2. **Compress formulations** without losing meaning: shorter sentences for the same content, paragraphs whose last line holds only a few words. A compressed sentence must still be understood by a reader who knows only what precedes it. Over-compression ("Jaccard 0.03 for A-B") makes the text shorter and worse.
3. **Move to appendices** what the reader does not need to follow the paper: derivations, full lists of examples, formal versions of informal statements, extended discussions, secondary experiments, details of the setup that only someone reproducing the work needs. Leave in the core a sentence that states the result or the idea and cites the appendix, as "Appendix~\ref{...}".

Do not delete content for any other reason, and do not change what the results say. Do not reach the limit by layout tricks (negative spacing, smaller fonts, removing figures from floats).

Shorten the abstract last, keeping the question, the approach, the main result and its consequence.

## Appendices

Appendices are not limited in length, so there is room to be pedagogical.

- **One theme per appendix.** An appendix is not a collection of unrelated material ("Additional details"). Plan the moves by theme: split an appendix that covers two topics, merge appendices that cover one, remove overlaps between them. Give each appendix a title that names its theme.
- **Self-contained.** Someone who has read only the abstract must be able to read an appendix without going back to the core, except for basic things (the task, the main method's name). Each appendix starts by restating the context and the result it expands on, with a reference to the section, and recalls the notation it uses. Remove sentences that became orphans when they moved ("The same reframing ..." with nothing before it).
- **Cited from the core**, where the material it extends is discussed.

## What to report

Report every change, one entry per change: its kind (`removed`, `compressed`, `moved`, `appendix` for text written to make an appendix self-contained, `abstract`), the file, the exact text before and after (for a move, before is the text removed from the core and after is what replaces it in the core), the appendix it went to if any, and in one sentence why. Report the appendices with their theme, and the final measurements.
