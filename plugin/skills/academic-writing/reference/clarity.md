# Clarity

Rules that make a text easier to read, whoever writes and reads it.

## Never refer to what the reader cannot see

1. **No references to earlier versions of the text.** Do not write "no longer flagged", "improved but not fully resolved", "the previously reported effect does not reproduce" or "as revised". The reader only has the current version.
2. **No internal artifacts.** Do not mention internal files (`EXPERIMENTS.md`, `results/run.json`, script names), internal stage names ("stage A", "v2"), code identifiers or chat discussions. If a version or variant matters, introduce it under a name the reader can understand.
3. **No narration of the research process.** Report the result, not the intermediate reasoning or how a mistake was found. A correction of your own earlier error is not a result ("it turns out this mode is fine if trained longer" reads as "oops").
4. **No editorial notes** left in the text ("[The next two paragraphs are moved from Section 1]").
5. **Reports are also written for a reader.** A report must be self-contained, and a section announced as "the key result" must state the result.

## Definitions and terminology

1. **Define every term and symbol at its first use.** This covers tools (name the tool and say what it does), technical jargon, notation and abbreviations ("artificial general intelligence (AGI)").
2. **One word per concept, everywhere.** Never use synonyms for a defined object ("instance" and "puzzle", "clues" and "givens"). Before finishing, check every defined term in the text for this.
3. **One symbol per object.** Never reuse a letter for two things (K for both a group size and a number of examples). Avoid near-identical symbols (S, S′, 𝒮) unless their relation is explained. When a symbol is used only once, prefer a descriptive noun.
4. **Introduce notation just before its first use**, and keep it consistent between sections and appendices.
5. **Use standard names**: established terms instead of invented ones, and textbook forms of formal definitions, with a reference.
6. **Never rely on a concept before it is introduced.** Do not refer to an example or an argument ("the transfer argument of Section 4.2") before the reader has seen it. Do not write "recall that..." for something the reader has not seen.
7. **Explain once.** Explain a term at its first occurrence, and do not explain it again later.
8. **State scope restrictions and working hypotheses early** in the main text, then refer back to them.
9. **Say when a notion is informal** ("This notion is still informal"), and present lists of aspects as non-exhaustive examples.

## Explaining

1. **Explain simple things simply.** When the idea is simple, the sentence must be simple. Convoluted explanations of simple ideas are the most frustrating kind of unclear writing.
2. **Avoid over-sophisticated phrasing** ("the fewer cells given, the more of the world's rules must be brought to bear"). Plain English is better.
3. **No vague deictics.** "This gap", "the question", "these arrangements", "both", "the two cases", "now": if the referent is more than a sentence away, restate it.
4. **Mark examples as examples** ("for instance"). An example illustrates a definition and must not presuppose it. Give the example first, then the general statement.
5. **Choose accessible and accurate examples.** Avoid obscure ones unless you explain them, check that they are physically and mathematically correct, and use current ones.
6. **Summarize cited work in plain English**, at the right level of detail: neither jargon nor a full replay of the method.
7. **Keep the grammatical subject consistent.** Do not switch between "the model", "a model" and "models" in one passage.
8. **When you quote a number, give the comparison point** ("goes to 51.9%" means nothing if the starting value is not recalled).
9. **Choose precise words**: "must" or "could", "equivalent" or "identical", "a set" or "the set" (use "the" only when the object is unique).

## Flow

1. **Connect ideas.** Do not fire ideas in quick succession without saying how they relate. Make each paragraph follow from the previous one.
2. **No repetition.** Each idea is stated once in the body. The abstract and introduction compress the body; they do not duplicate it.
3. **Do not put roadmap sentences between two important claims.**
4. **No orphan sentences** after an edit. Re-read the surrounding paragraph after every deletion or move.

## Meta-commentary

Sentences that describe the text instead of saying something cost the reader time. Remove:

- "This is a position paper." / "This paper does not report an experiment. Its contribution is conceptual..."
- "We do not pursue this connection further here."
- "This section fixes the notions used throughout the rest of the paper."
- "The criterion just stated is only useful if it can sort real cases."
- announcements of what will *not* be done ("we are not going to define X");
- sentences whose only purpose is to say that the claims are falsifiable or testable.
