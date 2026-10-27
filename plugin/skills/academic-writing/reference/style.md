# Patterns that read as AI-generated

Readers increasingly notice these patterns and discount the text because of them. Remove them in every self-review pass, unless the author's rules allow them. The linter (`scripts/lint_text.py`) catches many of them mechanically, but not all: the rhythm patterns below need a reading.

## Contrast constructions (the most frequent correction)

- **"rather than"**: use "instead of", or restructure the sentence.
- **"X, not Y", "not X but Y"** used for emphasis: remove the contrast if Y adds nothing. If both halves are needed, put the positive claim first ("is the one that maximizes agency, and not the one that minimizes effort").
- **Defensive appositives** that rebut an objection nobody raised. Remove them:
  - ", not a single small run", ", not just a pooled number"
  - ", not the other way around", ", not an incidental weakness to explain away"
  - "and this is now confirmed rather than merely argued"
  - "instead of hiding it", "not a new concept"
  - "deliberate choices, not defaults inherited without justification" (write "natural choices")
- **"is an empirical question, not one we assume the answer to"** and similar.

## Punctuation and rhythm

- **No em dashes.** Use a spaced hyphen (" - "), parentheses, commas or a new sentence, and vary between them.
- **Break the "X: Y" pattern.** A colon followed by an explanation in sentence after sentence is a tell. Prefer two sentences, or a subordinate clause.
- **Avoid triplets** ("well-defined, verifiable, and easily generated").
- **Avoid fragment sentences** ("A real average improvement." → "This is a real average improvement."), including label-like paragraph openers ("The computation." → "Computation of the NMI.").
- **Split long sentences**, especially in abstracts.

## Vocabulary

| Avoid | Instead |
|---|---|
| testbed, controlled testbed | example, setting, toy model |
| bookkeeping, grab-bag, piecemeal, yardstick, stopgap | reformulate plainly |
| genuinely, real, truly (as intensifiers) | remove |
| load-bearing, does real work, what X buys | reformulate |
| tellingly, gracefully, for free | remove or reformulate |
| "is worth making explicit" | remove, and say the thing |
| "In a specific sense, ..." | remove unless the sense is then given |
| titles such as "An identity, not an analogy" | plain descriptive titles |
