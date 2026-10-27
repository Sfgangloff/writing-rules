# Optional practices

These practices help many authors but are not defaults. Apply one only when the author's personal rules or the conversation turn it on. Each section gives a line the author can copy into `personal.md`.

## Tracked changes in color (LaTeX)

> Track changes in color.

- Write every new or modified passage in blue: `\textcolor{blue}{...}` (needs the `xcolor` package).
- When the author asks to see removals, strike removed text (`\sout{...}` from the `ulem` package, in red) and keep it until they say to delete it.
- When the author asks to isolate the latest round of changes, use a second color (for example purple) for that round.
- Remove the color ("unblue") only from passages the author has approved. Never unblue TODOs.
- Before a submission, check that no color is left (see `submission.md`).

## Replies to co-author or reviewer comments

> Answer comments in boxes.

- Keep the color or box each commenter was given (for example an orange box for the comment, a box of another color for your reply).
- Keep replies short, and point at the exact place in the text.
- Never delete a comment: the author resolves it.

## Single-author voice

> Single author: use "I".

- Use "I" throughout, never "we", including in "we denote" and "we show".
