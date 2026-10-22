# Synthesis prompt

Maintainers run this in a Claude Code session at the repository root when new contributions arrive. It updates `WRITING_RULES.md` from all the files in `contributions/`.

---

Please update `WRITING_RULES.md` from the contributions.

1. Read `WRITING_RULES.md` and **every** file in `contributions/` except `TEMPLATE.md`.
2. For every rule in every contribution, decide one of:
   - **Merge**: it states an existing rule. Strengthen that rule's wording or examples if the contribution adds something.
   - **Add**: it is a new rule supported by at least two contributors, or by one contributor with high frequency and general applicability.
   - **Scope**: contributors disagree, or the rule only holds for some kinds of writing. Keep it, but qualify it ("in position papers", "for single-author papers", "some writers prefer..."). Do not silently pick a side.
   - **Leave out**: it is personal taste specific to one writer. It stays in that writer's contribution file.
3. Keep the three parts of the file separate. **Part I (reading rules)** holds rules that improve the text for any reader. **Part II (style preferences)** and **Part III (working process)** hold matters of taste. Check each contributor's classification and correct it if needed: a rule belongs in Part I only if a careful reader with different tastes would still benefit from it. For preferences, contributors may legitimately disagree. When they do, record both options and their scope instead of choosing one.
4. Reorder rules within each section by how many contributors support them and how often, highest first.
5. Keep the file directly usable as a prompt: instructions addressed to Claude, short, concrete, with before/after examples. Do not add attributions or counts inside the rules.
6. Update `SYNTHESIS_LOG.md` with the date, the contributions included, and one line per rule added, merged, scoped or left out, with the reason.
7. Show me the diff of `WRITING_RULES.md` and wait for my review before committing.
