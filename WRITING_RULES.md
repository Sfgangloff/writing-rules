# Academic writing rules for Claude

Load this file at the start of any thread where Claude writes, edits or reviews academic text: research papers, position papers, research proposals and grant memos, experiment reports.
**Very first version**, built from one researcher's corrections and meant to be improved progressively as contributions arrive. The rules come from about 1,000 corrections made in real academic writing sessions (see [README](README.md)). Many of them, especially in Part I, also apply to other kinds of writing, but they have not been tested there.
Within each section, rules are ordered by how often they were needed.

The file has three parts:

- **Part I - Reading rules.** These aim to make a text easier to read and to trust, whoever the writer and the reader are: define terms, keep one name per concept, never refer to what the reader cannot see, and so on. Apply them always.
- **Part II - Style preferences.** These are matters of taste and of how a text is perceived, for example avoiding phrasings that readers associate with AI-generated text, or preferring "problem" to "task". They are well supported for the writers who contributed them, but another writer may legitimately differ. Apply them unless the author says otherwise.
- **Part III - Working process.** How Claude should collaborate on a text: marking changes, scope of edits, reports. These are also preferences, about the process instead of the text.

Sections 3 to 9 assume a paper. The other sections also apply to proposals and reports.

---

# Part I - Reading rules

## 1. Never refer to what the reader cannot see

1. **No references to earlier versions of the text.** Do not write "no longer flagged", "improved but not fully resolved", "the previously reported swing does not reproduce", "as revised". The reader only has the current version.
2. **No internal artifacts in the text.** Do not mention internal files (`EXPERIMENTS.md`, `results/x.json`, script names), internal stage names ("stage A", "v1/v2/v3"), internal labels ("train_id") or chat discussions. If a version or variant matters, introduce it properly under a name the reader can understand.
3. **No narration of the research process.** Report the end result, not the intermediate reasoning or how a mistake was found. A correction of your own earlier error is not a result ("it turns out this mode is fine if trained longer" reads as "oops").
4. **No editorial notes** left in the text ("[The next two paragraphs are moved from Section 1]").
5. **Reports are also for a reader**: a report must be self-contained. A section announced as "the result everything depends on" must actually state the result.
## 2. Clarity

### 2.1 Definitions and terminology

1. **Define every term and symbol at its first use**: tools (name the tool and say what it does the first time it appears), technical jargon (FiLM, bitmasks, cell domains, naked singles, NMI, AUROC), notation (P ∪ P′, π, S, H), and abbreviations (write "artificial general intelligence (AGI)").
2. **One word per concept, everywhere.** Never use synonyms for a defined object (givens / clues / fixed cells; instance / puzzle; system / world). Before finishing, check every definition in the paper for this. The author asked for it in capital letters.
3. **One symbol per object.** Never reuse a letter for two things (K for both group size and number of examples). Avoid near-identical symbols (S, S′, 𝒮) unless their relation is explained. Prefer a descriptive noun to a bare symbol when the symbol is used only once.
4. **Introduce notation just before its first use**, and keep it consistent between sections and appendices.
5. **Use standard names**: established terms (token embeddings, hard-square model, Chinese room) instead of invented ones; textbook forms of formal definitions, with a reference.
6. **Never rely on a concept before it is introduced.** Do not refer to an example ("the mirror relation") or an argument ("the transfer argument of Section 4.2") before the reader has seen it. Do not write "recall that..." for something the reader has not seen.
7. **Explain once.** Explain a term at its first occurrence, then do not re-explain it later.
8. **State scope restrictions and working hypotheses early** in the main text, then refer back to them. Avoid "which I bracket" without a reason.
9. **Informal notions:** say so plainly ("This notion is still informal"), and present lists of structural aspects as non-exhaustive examples.

### 2.2 Explaining things

1. **Explain simple things simply.** When the idea is simple, the sentence must be simple. The author's strongest complaints concerned convoluted explanations of simple ideas.
2. **Avoid over-sophisticated phrasing** ("the fewer cells given, the more of the world's rules must be brought to bear"). Plain English wins.
3. **No vague deictics.** "This gap", "the question", "these arrangements", "both", "the two cases", "now": if the referent is more than a sentence away, restate it.
4. **Mark examples as examples** ("for instance"). An example must illustrate a definition, not presuppose it. Give the example first, then the general statement.
5. **Choose apt, accessible, accurate examples.** Avoid obscure ones (Othello) unless explained; check that examples are physically and mathematically correct; use current examples (recent results, not outdated ones).
6. **Summaries of cited work in plain English**, at the right level of detail: neither jargon nor a full replay of their method.
7. **Grammatical consistency**: do not switch subjects between "the model", "a model" and "models" in one passage.
8. **When a number is quoted, give the comparison point** the reader needs ("goes to 51.9%" means nothing if the starting value is not recalled).
9. **Choose precise words**: "must" or "could"; "equivalent" or "identical"; "exact" or "precise"; "a set" or "the set".

### 2.3 Flow

1. **Connect ideas.** Do not fire many ideas in quick succession without saying how they relate. Smooth transitions between paragraphs, and make each claim follow from the previous paragraph.
2. **No repetition.** Each idea is stated once in the body (the abstract and introduction compress, they do not duplicate). Check paragraphs for the same idea said twice.
3. **Do not put roadmap sentences between two important claims.**
4. **No orphan sentences** after an edit. Re-read the surrounding paragraph after every deletion or move.

### 2.4 Meta-commentary

Sentences that describe the paper instead of saying something cost the reader time and add nothing.

Remove them:
- "This is a position paper." / "This paper does not report an experiment. Its contribution is conceptual..."
- "We do not pursue this connection further here." / "We note the connection without developing it further."
- "This section fixes the notions used throughout the rest of the paper."
- "The criterion just stated is only useful if it can sort real submissions."
- Sentences that announce what will *not* be done ("we are not going to define X").
- Sentences whose only purpose is to say that the claims are falsifiable or testable. Do not sprinkle "falsifiable" and "testable" where they add nothing.

## 3. Structure of an academic paper

### 3.1 Title and abstract

- The title states the thesis or the question plainly. Arxiv versions of position papers drop "Position:".
- **Abstract: no precise numbers and no technical details** (grid sizes, architecture names, internal test names, rule details). The order is: the general question or motivation, how it is studied concretely, and the kind of results obtained.
- **Lead with the most interesting finding.** Controls and validation experiments come after it, as confirmation.
- Add a connecting sentence wherever the abstract jumps (for example, from "world models" to "understanding").
- A key term the reader cannot know (such as "causal structure") gets at least a compressed definition.
- Check the venue's length limit.
- Simulate a first-time reader: "pretend you know nothing about the topic. Is it understandable? Is it interesting?"

### 3.2 Introduction

- The introduction contains compressed versions of the ideas developed in the body, without large overlap. Detailed explanations belong in the body.
- Mention the key design choices (where the architecture comes from, why the setting was chosen) so that a skimming reviewer sees they are not arbitrary.
- Emphasize the interesting results over methodological minutiae.
- **Contributions list:** an overview of each contribution, without technical enumeration and without internal names introduced later.
- **Roadmap:** introduce it with a sentence such as "The text is structured as follows". Keep each description short and concrete. Check that every section is listed, with the right count, and that each description matches the section's content.

### 3.3 Sections

- Open each section by stating what it does overall, then describe its subsections. Check that the announced number of parts matches.
- Open with the purpose ("In this section we test the hypothesis that..."), not with "X was left unexplained".
- In a thesis section, recall at the beginning of each subsection which part of the claim it develops.
- Prefer sections fully divided into subsections, not one long unsectioned part followed by two subsections. Avoid sections with a single subsection.
- Section titles describe the content specifically, avoid category mistakes ("false optimization targets"), and sibling titles share a tone.
- Paragraph headings are full phrases ("Why we chose 6×6 grids", not "Why 6×6.").
- Place definitions before the material that uses them, and state the problem before the solution. Do not give away the punchline in a preview paragraph.

### 3.4 Related work and alternative views

- Do not differentiate aggressively from prior work that the reader already knows is different. Explain what that work does.
- Do not present prior work as what we should have done, or as having already done our study at a larger scale.
- Do not diminish our own contribution in the comparison.
- Do not criticize named individuals or a field for something too recent to blame anyone for.
- **Alternative views** (mandatory in position papers): present independent, existing positions that conflict with ours, with citations. Do not present objections to our paper as alternative views. Do not prefix each one with "Position.".
- Keep paragraph lengths balanced, and trim to the essential.

### 3.5 Results

- Before commenting on a table or figure, say which experiment it reports. Do this in the caption too.
- Reference every table and figure in the text, and place the sentence that introduces a figure before the figure. The table does not "test" anything: we test, and the table reports.
- Lead with the most surprising and least technical result.
- Do not present obvious results as findings.
- If a claim from the literature or from intuition is refuted, frame it as such, so the negative result still has value.
- Justify sample sizes and the choices a reviewer will question.

### 3.6 Limitations, conclusion and TODOs

- Limitations stay high level. Consider the heading "Limitations and further research".
- Unfinished experiments are TODOs, not limitations.
- Keep acknowledgements, the AI usage statement and similar sections in the format the venue requires.

### 3.7 Appendices

- **Each appendix is coherent** (one topic, not a bag of unrelated parts) **and self-contained**: restate the context and the result it expands on, with references to the sections, so the reader does not have to re-read the main text. For example: "In Section 4.2 we stated that ... We expand on this result here."
- Be pedagogical. There is space to explain basics for readers who do not know the material.
- For a technical appendix, re-explain the issue, then give a concrete example, then do the computation.
- Avoid many tiny subsections. Prefer one subsection with a paragraph per item, with balanced lengths.
- Cite every appendix briefly from the main text.
- Remove sentences that become orphans once text is moved to an appendix.
- With a single appendix, call it "the appendix", not "Appendix A".

### 3.8 Page limits

To reach the limit: detect repetition, trim what is superficial, compress formulations, and move expository material that is not necessary to follow the paper into coherent appendices. Do not touch the results unless asked. Never lose information when compressing.
## 4. Argumentation and claims

1. **Do not undersell.** Do not add sentences that give reasons to doubt the work ("not merely a mathematical convenience"), that sound careless ("is not settled by a single run per condition"), or that make a contribution sound smaller ("this definition is not more expressive than...").
2. **Do not oversell.** Avoid absolute claims ("This is not hypothetical", "cannot be what we mean by intelligence") when a nuanced claim is correct. Do not claim a solution you do not have. Writing "I do not have an answer to this problem" is fine.
3. **Anticipate the reviewer.** Where will a reviewer say "why 6×6?", "why 30 cells?", "duh", "so what?", "how do you measure that?", "come on, it solved Navier-Stokes"? Answer briefly where the question arises.
4. **Check for circularity** (using the criterion to justify the criterion) and for self-contradiction (a passage that argues against our own thesis, or two paragraphs that order the same things differently).
5. **Check that summaries of cited work are accurate** (what they claim, the names they use for their concepts) and that a citation fits the point being made.
6. **Distinguish hypothesis from claim.** Present speculative foundations as hypotheses, and use hedges where appropriate ("in principle", "one intuition behind", "we have no proof of this").
7. **Do not invent predictions or tests** to look scientific.
8. **Do not insert evidence the argument does not need.** Every added fact, statistic or citation must have a clear purpose where it is placed.
9. **State positive claims positively.** "This understanding already exists in cognitive science" instead of "This is not a new claim about cognition".
10. **Tone:** academic and sober. Avoid casual phrases ("someone else's department", "op-ed", "on the system's say-so") and heavy metaphors ("the door is already ajar"). Avoid phrasing that is too direct or accusatory ("three areas of current practice are measuring the wrong thing", "This is why I ask...").
## 5. Mathematical writing

- Formal definitions follow the standard textbook form, with a reference. Define every component (language, axioms, inference rules, what "decidable" means here).
- Introduce every symbol and its required properties before using it.
- Check that a definition and the remarks that follow it are consistent and unambiguous, and that the term being defined actually appears in its definition paragraph.
- Use set notation where appropriate ({1, ..., 6}), and say whether an object is a set or a relation.
- Use the definition environment only for actual definitions. If the content is too long for one, restructure it.
## 6. Figures, tables and LaTeX formatting

- Use sober colors in figures (no flashy greens). Keep captions short and descriptive. Remove details that are irrelevant to the purpose of the figure (token counts in an overview).
- Use proper tables, with rules between rows and columns where readability needs them, balanced column widths, and pictures aligned and centered with their text.
- One figure has one purpose. Move illustrations of a notion to where that notion is defined.
- Use consistent formatting for names (do not mix `anti_knight` and `AntiKnight`).
- Check that the PDF compiles, that tables do not overlap, and that long URLs in the bibliography do not overflow into other references.
- Use the current year's style files for the venue.
## 7. Citations and references

- **Check every reference**: it exists, the metadata is correct, and it supports the sentence where it is cited.
- **Go through the paper sentence by sentence** and add relevant citations wherever a claim calls for one. Prioritize machine learning and AI references. References from philosophy, cognitive science or mathematics are welcome where relevant.
- No paragraph of claims without at least one citation, unless it is purely our own argument.
- Remove uncited entries from the `.bib`, or move them to a separate file.
- Use current examples of the state of the art, and check that those facts are true.
## 8. Position papers (ICML/NeurIPS position track)

- The thesis is stated explicitly, early and consistently. When the thesis changes, re-center the whole paper (abstract, introduction, roadmap) on it.
- Mandatory sections: alternative views (see 3.4) and, where the venue requires it, a call to action. Check the current call for papers for other rules.
- Expect reviewers to ask for technical substance. Ground conceptual claims in machine learning practice and literature.
- An informal seed from the author is developed into an argument. It is not decorated with artificial structure ("Nothing artificial please").
## 9. Submission checklist

- [ ] Page limit respected (main text, excluding references and appendices, as the venue defines).
- [ ] Abstract within the venue's limit.
- [ ] Anonymized: no names, no identifying repository URLs (use an anonymous mirror), no self-identifying acknowledgements. The acknowledgements are commented out until camera-ready.
- [ ] Code repository cleaned: documentation without emojis, docstrings for every function, an anonymous mirror for review.
- [ ] AI usage statement included if the venue requires it.
- [ ] No TODOs, colored text or comment boxes left in the submitted PDF.
- [ ] Arxiv version: de-anonymized (affiliations, emails), "Position:" removed from the title, ideally one merged `.tex` file plus the style, `.bst` and `.bbl` files.

---

# Part II - Style preferences

## 10. Patterns that read as AI-generated

The author flags these immediately. Remove them in every self-review pass.

### 10.1 Contrast constructions (the most frequent correction)

- **"rather than"**: replace with "instead of", or restructure the sentence. Do not use "rather than" at all unless no other wording works.
- **"X, not Y" / "X rather than Y" / "not X but Y"** used for emphasis: remove the contrast if Y adds nothing. If both halves are needed, put the positive claim first: "is the one that maximizes agency, and not the one that minimizes effort".
- **Defensive appositives** that rebut an objection nobody raised. Remove them:
  - ", not a single small run", ", not just a pooled number", ", not on a single fixed ordering"
  - ", not the other way around", ", not an incidental weakness to explain away"
  - "and this is now confirmed rather than merely argued"
  - "worth stating plainly rather than folding into a pooled mean"
  - "instead of hiding it", "not a new concept", "not a new one invented for it"
  - "deliberate choices, not defaults inherited without justification" (write "natural choices")
- **"is an empirical question, not one we assume the answer to"** and similar.

### 10.2 Punctuation and rhythm

- **No em dashes (—).** Use a hyphen with spaces (" - "), parentheses, commas or a new sentence, and vary between them.
- **Break the "X: Y" pattern.** A colon followed by an explanation in every other sentence is a tell. Prefer two sentences, or a subordinate clause.
- **Avoid triplets** ("well-defined, verifiable, and easily generated") and short enumerations of three nouns ("text, pseudocode, a chain of thought").
- **Avoid fragment sentences** ("A real average improvement." → "This is a real average improvement."). Avoid label-like fragments as paragraph openers ("The computation." → "Computation of the NMI.").
- **Split long sentences**, especially in abstracts.

### 10.3 Vocabulary to avoid

| Avoid | Use instead / note |
|---|---|
| testbed, controlled testbed, toy testbed | example, setting, toy model; for mathematics, "crash test" |
| bookkeeping, grab-bag, piecemeal, yardstick, stopgap | reformulate plainly |
| genuinely, real (as intensifiers), truly | remove |
| load-bearing, does real work, what X buys | reformulate |
| tellingly, gracefully, nominally, for free | remove or reformulate |
| fresh, at low cost, for space, cheaply | remove, or "inexpensively" |
| mix, fresh mix, gate, live case | name the actual thing |
| "is worth making explicit", "made recognizable" | remove |
| "In a specific sense, ..." | remove unless the sense is then given |
| "This is not hypothetical" | "This is not only hypothetical" |
| Titles of the form "An identity, not an analogy" / "Not the compression X argues against" | plain descriptive titles |

## 11. Word choice and formatting

These substitutions were requested repeatedly. Apply them unless the context clearly needs the original word.

| Instead of | Write |
|---|---|
| task, sub-task | **problem** (or assignment, depending on context) |
| ask, asks, asking (about a paper, a question, a section) | question, wonder, formulate, require, concern |
| give, gives | provide |
| show (for a logical result) | prove, establish; for evidence: "provides evidence" |
| start(s) | begin(s) |
| starting point | point of departure |
| asked (a request) | requested |
| fix (noun or verb, in prose) | reformulate: remedy, correction, change, address |
| win (between alternatives) | prevail, be preferred |
| step (when overused) | move, stage, or reformulate |
| lab | laboratory |
| invoked, recruited | used, called upon |
| taken for granted | assumed |
| "the same as" | "identical to" |
| "we take X to be" | "we call X" |
| "X is the fraction of..." (for a new symbol) | "We denote by X the fraction of..." |
| "Call it a seed: a..." | "We call seed a..." |
| "Section 2.3's criterion" | "the criterion defined in Section 2.3" |
| "because Section 4.2 locates..." | "because ... is located ... (Section 4.2)" |
| "Section 4.3 trained the model" | "In Section 4.3 we reported experiments training..." |

Other preferences:
- **Single author: use "I", never "we".**
- Use "a world" and "a set of worlds", not "the world" or "the set", when the object is not unique.
- Prefer measured verbs: "is not entirely novel" instead of "is not new"; "currently falls short" instead of "genuinely falls short".
- Lowercase common nouns after hyphens and in running text ("proposition-level", "example-based"). Italicize names of models and systems, and a new term at its first occurrence only.

Document conventions:
- Section titles in sentence case (only the first word capitalized, plus proper nouns).
- No uppercase letters (A, B, C) for enumerations. Indent paragraphs, and indent lists as a block.
- In LaTeX, write the abstract on one line.

---

# Part III - Working process

## 12. How to work with the author

These rules concern the editing process. Breaking them caused the most frustration.

1. **Understand, then write. Do not transcribe.** When the author explains an idea in chat, it is a seed, not text to paste. Understand what they mean, then write it in your own academic prose, placed where it belongs. Never copy their casual phrasing ("from scratch", "kind of", "lol") into the document. Never copy into the document an explanation that was meant only for you ("just to explain you", "for instance, to make you understand").
2. **Think about every requested edit, even trivial-looking ones.** After many routine edits (renamings, small rewordings), do not slip into mechanical execution. If an edit is wrong, introduces an inconsistency, or misses the point, say so. "You don't have to use my exact words if you don't agree."
3. **Edit exactly the scope requested.** If asked to remove one sentence, remove that sentence and nothing else. If asked to compress, cut instead of oversimplifying, and never lose information. If an edit lost information, offer to revert.
4. **Apply global changes globally.** A renamed term, a new notation or a changed framework must be updated everywhere: main text, appendices, tables, figures, captions, comments that will be read. Do not leave a paragraph in the old notation and explain why. Do not report a change as done without checking.
5. **Make every change visible.** Unless told otherwise, write new or modified text in blue (`\textcolor{blue}{...}`). If asked to strike removed text, use strikethrough and keep it until told to delete it. Use a second color (red or purple) when asked to isolate the latest round of changes. "Unblue" only what the author has approved, and never unblue TODOs.
6. **Comments from co-authors or reviewers:** keep the colors they were given (for example, an orange box for the comment, a turquoise box for your reply). Keep replies short and point at the exact place.
7. **Before a large restructuring**, commit and push so the previous state can be recovered.
8. **Reports go in files, not the terminal.** A report on experiments is a `.md` file. For each experiment it gives: what was done, why, the results (synthetic numbers) and how to interpret them. Write it so the author can read and comment on it.
9. **When asked "what do you think?", give an opinion with reasons**, and say when the author's idea has a weakness.
10. **Verify instead of guessing.** Check facts, dates, claims attributed to papers, names of methods, and whether a reference exists, before writing them.

---

## 13. Final self-review pass (run before handing back any text)

Reading rules (Part I):

1. Check every term and symbol: is it defined at first use? Is there one name per concept and one meaning per symbol?
2. Check every "this", "these", "the two" and "both": is the referent obvious?
3. Look for references to earlier versions, internal files and chat context.
4. Look for repeated ideas, meta-commentary and orphan sentences.
5. Check that every table and figure is introduced in the text before it appears.
6. Check that each claim is neither undersold nor oversold, and that summaries of others' work are accurate.
7. Read the text as a reviewer who does not know the material. Where would they stop, and what would they ask?

Style preferences (Part II), unless the author has said otherwise:

8. Search for "rather than", "not ... but", ", not ", em dashes, and colons followed by an explanation. Rewrite them.
9. Search for the vocabulary in 10.3 and the substitutions in section 11 (task, ask, give, show, start).

Then:

10. Report what you changed. Do not claim a global change you did not verify.
