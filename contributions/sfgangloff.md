# sfgangloff

## Profile

- **Writes mostly:** ML conference papers (ICLR, ICML main track), ICML position papers, a grant-programme memo, experiment reports
- **Field:** mathematics, machine learning (interpretability, reasoning, AI for mathematics), philosophy of ML
- **Language of writing / native language:** English / French
- **Period covered:** August to October 2026
- **Volume:** about 2,650 messages across 49 projects, of which about 1,000 concern a text being written

## Rules, by frequency

Frequencies are approximate counts of messages matching each kind of correction.

### 1. Remove what is not necessary

- **Type:** reading rule
- **Frequency:** ~160 ("not necessary", "not useful", "remove", "no need")
- **Kind:** clarity
- **Examples:**
  - "..., and this is now confirmed rather than merely argued." -> removed
  - "We do not pursue this connection further here." -> removed ("it is visible that it is a short comment only")
- **Relation to WRITING_RULES.md:** confirms §2.4, §2.3

### 2. Make it understandable to a reader who does not know the material

- **Type:** reading rule
- **Frequency:** ~110 ("not clear", "I don't understand", "what does it mean")
- **Kind:** clarity
- **Examples:**
  - A tool named in passing before it is explained -> explain it at first use, delete the later explanation
  - "You explain simple things in an extremely convoluted way" -> "it could be something MASSIVELY simpler"
- **Relation to WRITING_RULES.md:** confirms §2.1, §2.2

### 3. Mark every change in blue, unblue only after approval

- **Type:** process preference
- **Frequency:** ~100
- **Kind:** process
- **Examples:** "Make the modifications in blue so that I can review easily"; "I told you not to unblue the TODO"
- **Relation to WRITING_RULES.md:** confirms §12.5

### 4. "rather than" -> "instead of"; avoid the "X, not Y" contrast

- **Type:** style preference
- **Frequency:** ~90
- **Kind:** AI tell
- **Examples:**
  - "rather than an architectural limit" -> "instead of an architectural limit"
  - "a real ceiling rather than noise" -> "X rather than Y, AI writing pattern. Please reformulate"
- **Relation to WRITING_RULES.md:** confirms §10.1

### 5. Add citations, especially ML ones, and check every reference

- **Type:** reading rule
- **Frequency:** ~65
- **Kind:** citations
- **Examples:** "look at each sentence, and whenever there is a relevant citation we should include it there"; "check every reference individually to check if it exists and that it is correct, and correctly used"
- **Relation to WRITING_RULES.md:** confirms §7

### 6. "ask" -> "question", "wonder", "formulate", "require"

- **Type:** style preference
- **Frequency:** ~60
- **Kind:** word choice
- **Examples:** "Chopra asks what" -> "Chopra questions what"; "a paper asking whether" -> "wondering whether"
- **Relation to WRITING_RULES.md:** confirms §11

### 7. "task" -> "problem"

- **Type:** style preference
- **Frequency:** ~55
- **Kind:** word choice
- **Examples:** "novel tasks" -> "novel problems"; "every task posed in a world" -> "every problem posed in a world"
- **Relation to WRITING_RULES.md:** confirms §11

### 8. Reformulate sentences that read as AI-generated

- **Type:** style preference
- **Frequency:** ~45 explicit "reformulate" requests, ~15 explicit "sounds like AI"
- **Kind:** AI tell
- **Examples:** "testbed", "bookkeeping", "does real work", "made recognizable", "tellingly flags", a title of the form "An identity, not an analogy"
- **Relation to WRITING_RULES.md:** confirms §10.3

### 9. "give" -> "provide"

- **Type:** style preference
- **Frequency:** ~30
- **Kind:** word choice
- **Relation to WRITING_RULES.md:** confirms §11

### 10. Never refer to earlier versions, internal files or the research history

- **Type:** reading rule
- **Frequency:** ~15, several of them emphatic (capitals)
- **Kind:** clarity
- **Examples:** "no longer flagged" -> "WE SHOULD NEVER REFER TO ANY OLDER VERSION OF THE PAPER THE READERS DONT HAVE ACCESS TO"; a reference to `EXPERIMENTS.md` in a draft -> removed
- **Relation to WRITING_RULES.md:** confirms §1

### 11. One word per concept

- **Type:** reading rule
- **Frequency:** ~10, emphatic
- **Kind:** clarity
- **Examples:** givens / clues / fixed cells used for one object -> "MAKE SURE YOU DONT USE MANY DIFFERENT WORDS FOR THE SAME THING"
- **Relation to WRITING_RULES.md:** confirms §2.1

### 12. No em dashes

- **Type:** style preference
- **Frequency:** ~10 (one per paper, applied globally)
- **Kind:** AI tell
- **Examples:** "replace all emdashes with small dashes like '-', or use something else, like parentheses (you can vary a little)"
- **Relation to WRITING_RULES.md:** confirms §10.2

### 13. Do not copy my explanations into the text

- **Type:** process preference
- **Frequency:** ~8, emphatic
- **Kind:** process
- **Examples:** "whenever I say something like that, you become super lazy and just copy what I said"; "you include parts that are meant as explanations for you"
- **Relation to WRITING_RULES.md:** confirms §12.1

### 14. Abstract: no numbers, no technical details, most interesting result first

- **Type:** reading rule (the "no numbers" part is closer to a preference)
- **Frequency:** ~10
- **Kind:** structure
- **Relation to WRITING_RULES.md:** confirms §3.1

### 15. Appendices coherent and self-contained, restating the result they expand on

- **Type:** reading rule
- **Frequency:** ~10
- **Kind:** structure
- **Relation to WRITING_RULES.md:** confirms §3.7

### 16. Alternative views are independent positions, not objections

- **Type:** reading rule
- **Frequency:** ~6 (position papers)
- **Kind:** structure
- **Relation to WRITING_RULES.md:** confirms §3.4

## Process preferences

- Blue for changes, strikethrough for removals when asked, then "unblue" after approval. Red or purple for a sub-round; orange and turquoise boxes for co-author comments and replies.
- Commit and push before large edits.
- Experiment reports in `.md` files: what was done, why, results, interpretation.
- Simulated reviews ("pretend you are a reviewer who doesn't know the material") before submission.
- Review section by section, with edits applied as they are approved.

## Notes for the synthesis

- "I" instead of "we" is because most of the position papers are single-authored. It is not a general rule against "we".
- "task" -> "problem" may partly reflect a mathematician's vocabulary. Other fields may legitimately prefer "task".
- "crash test" instead of "testbed" was proposed for one specific paper (mathematics as a crash test for interpretability methods).
