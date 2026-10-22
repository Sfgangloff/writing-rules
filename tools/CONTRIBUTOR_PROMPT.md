# Contributor prompt

Paste everything below the line into a Claude Code session started in your clone of this repository. Claude will extract your past messages locally, read them, and draft `contributions/<your-handle>.md`. Review the draft yourself before opening a pull request.

Nothing leaves your machine until you push. The raw extraction (`user_messages.txt`) is git-ignored and must never be committed.

---

I want to contribute my writing preferences to this repository. Please do the following.

1. Run `python3 tools/extract_messages.py --out user_messages.txt`. If I only want some projects, I will tell you which ones, and you can pass them with `--filter`.
2. Read the **whole** output file, in chunks if needed. Do not sample it. As you read, keep running notes in a scratch file, so nothing is lost if the context gets summarized.
3. Collect every message in which I asked for a change to a text: rewordings ("X -> Y"), complaints ("this reads like AI", "not clear", "remove"), structural requests, process instructions (how I want edits shown, reviewed or committed), and the questions I asked about a draft that reveal what was unclear to me. Ignore messages about code, infrastructure and logistics.
4. Group the corrections into recurring rules. A rule must be backed by several occurrences, or by one occurrence where I was clearly emphatic (capitals, frustration). For each rule, estimate how often it occurred, and classify it as a **reading rule** (helps any reader, whatever the writer's taste) or a **style/process preference** (my taste or my way of working), as explained in the template.
5. Write `contributions/<my-handle>.md` following `contributions/TEMPLATE.md` exactly. Rules are phrased as instructions to Claude, ordered by frequency, each with one or two short before/after examples.
6. **Privacy pass, before showing me the draft.** Remove anything that identifies me or other people beyond my chosen handle: names of collaborators, emails, addresses, account or ID numbers, unpublished paper titles, and quotes long enough to reveal unpublished work. Rewrite the examples generically when in doubt. Then list for me what you removed.
7. Show me the draft and wait for my review. Do not commit, push or open a pull request until I say so.

Also read `WRITING_RULES.md` before drafting, and tell me which of my rules are **new**, which **confirm** an existing rule, and which **contradict** one. Contradictions are valuable, because they show where preferences differ between writers.
