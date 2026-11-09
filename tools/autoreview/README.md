# autoreview

Turns a paper drafted by AI from its experiments into a paper a human reader can follow, and records every correction it makes, so that the corrections can be turned into writing rules the same way as a researcher's own corrections.

The `review-pass` skill of the plugin does a similar review inside a Claude Code session, with the author. `autoreview` runs without the author, as a script: each agent is a separate `claude -p` call with a fixed prompt, every step is saved, and runs can be compared. This makes it suitable for experiments.

## How it works

1. **Reader** ([`prompts/reader.md`](prompts/reader.md)). For each paragraph, a researcher of the field who has read only the paper up to that paragraph (no tools, no files: the text is in its prompt) says what it understood, whether a reader would understand it well enough (`clear`, `mostly` or `unclear`), and asks at most 10 questions, each tagged `unclear`, `why`, `objection`, `link`, `outside` or `missing`. Comments in the LaTeX source are removed, since a reader of the PDF does not see them.
2. **Editor** ([`prompts/editor.md`](prompts/editor.md)). With the whole paper, the code and the notes, it answers the questions by changing the text: where the answer belongs, with what the work actually contains. It never invents a number or a motivation. Questions that only the authors can answer go to `author_questions.md` and to a `% AUTHOR:` comment in the source.
3. The reader starts again from the beginning, since an edit changes what later paragraphs can rely on. Paragraphs whose text and preceding text have not changed are not read again. The loop stops when every paragraph is `clear`; when none is `unclear` and the number of `mostly` paragraphs stops decreasing, since what remains then usually waits for the authors; when the editor changes nothing; or after `--max-rounds`.
4. **Cutter** ([`prompts/cutter.md`](prompts/cutter.md)). If limits are given, it removes repetitions, compresses, and moves material to appendices that each cover one theme and can be read on their own, until the core (everything before the references or the appendices) and the abstract fit. It can compile and measure the paper itself. Up to `--cut-attempts` attempts.
5. The reader reads each appendix **on its own**, after the abstract only, and the editor fixes what cannot be understood without the core, changing only the appendices.
6. A **final reading** of the core reports what remains unclear after the cut, without changing anything.

The original paper is never modified. The run works on a copy, versioned with git (`work/`, one commit per step), and the result is copied to `paper/`.

## Usage

```bash
python3 tools/autoreview/autoreview.py run \
    --paper ~/project/paper/main.tex \
    --context ~/project \
    --pages 8 --abstract-words 200 \
    --out runs/project
```

- `--context` (repeatable): directories the editor and the cutter may read but not change: code, logs, notes. The reader never sees them.
- `--pages`, `--abstract-words`: limits. Without them, the cut is skipped.
- `--reader-model`, `--editor-model`: `opus` by default.
- `--with-plugin`: load the `writing-toolkit` plugin (rules and linter) in the editor and cutter. Leave it off when the corrections are meant to produce new rules, otherwise they repeat the existing ones.
- `--parallel`: reader calls run at the same time (4).

An interrupted run continues where it stopped if you run the same command again.

The reader is called once per paragraph with all the text before it, so a round costs about as much as reading the paper `n / 2` times for `n` paragraphs. Successive calls share their beginning, which the prompt cache reuses.

## What a run produces

| File | Contents |
|---|---|
| `paper/` | the revised paper |
| `log.md` | verdicts per round, measurements, cost |
| `roundN/questions.md` | the reader's understanding, verdict and questions for each paragraph |
| `roundN/reader.json`, `editor.json` | the same, and the editor's report, as data |
| `cut/`, `appendices/`, `final/` | the cut, the appendix check, the final reading |
| `author_questions.md` | what only the authors can answer |
| `corrections.txt` | every change with the question it answers, in the format of `tools/extract_messages.py` |
| `corrections.jsonl` | the same, as data |
| `work/` | the git repository of the run: `git log -p` shows each step |

## From corrections to rules

```bash
python3 tools/autoreview/autoreview.py rules runs/paper1 runs/paper2 --out runs/rules.md
```

Claude reads the corrections of the runs and drafts rules in the format of [`contributions/TEMPLATE.md`](../../contributions/TEMPLATE.md), saying for each whether it is new, confirms a rule of the skill, or contradicts one. The editor's changes are not all improvements, and the prompt asks Claude to leave out those that a human reader would not want. The rules still come from a model reading for a model: compare them with rules from human corrections before adding them to the skill.
