# Synthesis prompt

Maintainers run this in a Claude Code session at the repository root when new contributions arrive. It updates the academic writing skill (`plugin/skills/academic-writing/`) from all the files in `contributions/`.

---

Please update the academic writing skill in `plugin/skills/academic-writing/` from the contributions.

1. Read `SKILL.md`, every file in `reference/`, `scripts/lint_rules.json`, and **every** file in `contributions/` except `TEMPLATE.md`.
2. For every rule in every contribution, decide one of:
   - **Merge**: it states an existing rule. Strengthen that rule's wording or examples if the contribution adds something.
   - **Add**: it is a new rule supported by at least two contributors, or by one contributor with high frequency and general applicability.
   - **Scope**: contributors disagree, or the rule only holds for some kinds of writing. Keep it, but qualify it ("in position papers", "for single-author papers", "some writers prefer..."). Do not silently pick a side.
   - **Leave out**: it is personal taste specific to one writer. It stays in that writer's contribution file.
3. Keep reading rules and preferences apart. A rule is a **reading rule** only if a careful reader with different tastes would still benefit from it; check each contributor's classification and correct it if needed. Preferences shared by several contributors go in `reference/style.md` or `reference/collaboration.md`. When contributors disagree on a preference, record both options and their scope instead of choosing one. A personal practice that could help others but should not be a default (such as tracked changes in color) goes in `reference/optional-practices.md`, with the line an author copies into their `personal.md` to turn it on. Taste specific to one writer is left out: it stays in their contribution file, and they can put it in their own `personal.md`.
4. Place each rule in the right file. `SKILL.md` keeps only the core rules that apply to every academic text, short, and with the table that says when to read each reference file. Keep `SKILL.md` under about 150 lines.
5. If a style rule can be detected by a regular expression, add it to `scripts/lint_rules.json`, with a replacement only if the replacement is correct in almost every context. Run `python3 -m unittest discover tests` afterwards.
6. Reorder rules within each section by how many contributors support them and how often, highest first.
7. Keep the files directly usable as a prompt: instructions addressed to Claude, short, concrete, with before/after examples. Do not add attributions or counts inside the rules.
8. Update `SYNTHESIS_LOG.md` with the date, the contributions included, and one line per rule added, merged, scoped, made optional or left out, with the reason.
9. Show me the diff of the skill and wait for my review before committing.
