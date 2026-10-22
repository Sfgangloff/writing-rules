You are drafting an anonymous contribution to a repository of **academic writing rules for Claude**. Work without asking questions: nobody will answer until you are done.

Files:
- Extracted messages (input, read-only): `{{MESSAGES}}`
- Your scratch notes: `{{NOTES}}`
- The contribution to write: `{{OUTPUT}}`
- A privacy report for the contributor: `{{REPORT}}`

Do not create or modify any other file.

1. Read `WRITING_RULES.md` and `contributions/TEMPLATE.md`.
2. Read the **whole** messages file, in chunks of a few hundred lines. Do not sample it. These are the messages the contributor typed in Claude Code sessions. After each chunk, append what you found to the scratch notes, so nothing is lost if your context gets summarized.
3. Keep only corrections to **academic texts**: papers, position papers, research proposals, research reports, theses. These include rewordings ("X -> Y"), complaints ("reads like AI", "not clear", "remove"), structural requests, instructions about how edits should be shown or reviewed, and questions about a draft that reveal what was unclear. Ignore code, infrastructure, logistics and any non-academic writing (emails, social media, documentation, personal matters).
4. Group the corrections into recurring rules. A rule needs several occurrences, or one occurrence where the contributor was clearly emphatic (capitals, frustration). Estimate each rule's frequency and classify it as a **reading rule** or a **style/process preference**, as the template explains.
5. Write `{{OUTPUT}}` following the template exactly. Use `{{ID}}` as the title. Phrase rules as instructions to Claude, order them by frequency, and give one or two short before/after examples per rule. Say for each rule whether it is new, confirms a section of `WRITING_RULES.md`, or contradicts one.
6. **The contribution must be anonymous.** It must not contain, even in examples:
   - names of people (the contributor, collaborators, reviewers, cited authors are fine only if they appear as a standard reference such as "Marr's levels");
   - usernames, emails, phone numbers, addresses, URLs, file paths, account or document numbers;
   - institutions, labs, funding bodies, project or grant names, cluster or server names;
   - titles of unpublished papers, or quotes long enough to identify an unpublished paper or project (rewrite examples generically: "the rule pool" instead of a project-specific term);
   - anything else that would let a reader guess who the contributor is.
   For the profile, give only broad categories (for example "machine learning", "ML conference papers").
7. Write `{{REPORT}}`: a short list of what you left out or generalized for anonymity, and anything you were unsure about. This report is never published.
8. If you found fewer than about 20 writing corrections in total, say so at the top of the privacy report: the history may not contain enough close reviewing for a useful contribution.
9. Finish by printing one line: the path of the contribution file.
