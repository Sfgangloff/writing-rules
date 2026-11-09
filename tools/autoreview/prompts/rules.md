You are drafting writing rules for Claude from corrections made to AI-drafted academic papers. Work without asking questions: nobody will answer until you are done.

Files:
- The corrections (input, read-only): {{CORRECTIONS}}
- Your scratch notes: `{{NOTES}}`
- The rules to write: `{{OUTPUT}}`

Do not create or modify any other file.

The corrections were not made by a human. A simulated reader, a model that sees only the paper up to each paragraph, asked questions about each paragraph; an editor model, which knows the whole work, changed the text to answer them; then a cutter model brought the paper to its page limits. Each correction gives the reader's question, or the reason for a cut, and the change made in reply.

1. Read the current rules, in `plugin/skills/academic-writing/` (`SKILL.md` and every file in `reference/`), and `contributions/TEMPLATE.md`.
2. Read the **whole** corrections files, in chunks of a few hundred lines. After each chunk, append what you found to the scratch notes.
3. **Find the rule behind each correction.** Ask what was wrong with the text before, in general, beyond this instance: a term used before its definition, a number without its motivation, a claim stronger than the table, a reference to an internal run name. A question the editor answered by adding a fact is a rule about what the first draft omitted ("state the size of the test set when it is introduced"), not about style.
4. **Judge each correction.** The editor can be wrong too: it may answer a question that a human would not ask, or add text a human would find padding. Leave out corrections whose change does not make the text better for a human reader, and say so in the notes.
5. Group the corrections into recurring rules. A rule needs several occurrences, in different papers if there are several. Estimate each rule's frequency.
6. Write `{{OUTPUT}}` following the template, with the title "Rules from automated review". In the profile, say that the corrections come from the automated review, how many papers and corrections they cover, and that every rule is a reading rule found by a simulated reader. Phrase rules as instructions to Claude, order them by frequency, give one or two short before/after examples per rule, rewritten generically. Say for each rule whether it is new, confirms a rule of the skill, or contradicts one (name the file and the rule).
7. Finish by printing one line: the path of the rules file.
