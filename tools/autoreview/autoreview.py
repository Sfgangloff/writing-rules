#!/usr/bin/env python3
"""Revise an AI-drafted paper until a simulated reader understands it, then fit it
to the page limits, and record every correction as material for writing rules.

Three agents, each a separate `claude -p` call with its own prompt (in prompts/):

1. The reader sees only the paper up to a paragraph, as a human reading it from
   the beginning would, and nothing else (no tools, no files). For each paragraph
   it says what it understood, whether a reader of the field would understand it
   well enough (clear / mostly / unclear) and asks up to 10 questions.
2. The editor sees the whole paper, the code and the notes, answers the questions
   by changing the text, and reports each change with the questions it answers.
3. The cutter brings the core of the paper to the page limit and the abstract to
   its word limit, moving material to appendices that each cover one theme and
   can be read on their own; the reader then checks each appendix on its own.

Reader and editor alternate, the reader starting again from the beginning of the
paper each round, until every paragraph is clear, the editor stops changing the
text, or the round limit is reached. The original paper is never modified: the
run works on a copy, versioned with git so that each round can be inspected.

Every change is written to corrections.txt, in the format of
tools/extract_messages.py (the reader's question in place of the author's
message), and to corrections.jsonl. `rules` turns the corrections of one or more
runs into writing rules, in the format of contributions/TEMPLATE.md.

Usage:
    python3 tools/autoreview/autoreview.py run --paper paper/main.tex \\
        --context . --pages 8 --abstract-words 200 --out runs/mypaper
    python3 tools/autoreview/autoreview.py measure --run runs/mypaper
    python3 tools/autoreview/autoreview.py rules runs/mypaper [runs/other ...] \\
        --out runs/rules.md

A run can be interrupted and started again with the same command: finished
steps are not redone.
"""

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PROMPTS = os.path.join(HERE, "prompts")
PLUGIN_DIR = os.path.join(ROOT, "plugin")
CORE_END = "autoreview-core-end"

# ---------------------------------------------------------------- LaTeX reading

COMMENT = re.compile(r"(?<!\\)%.*$")
INPUT = re.compile(r"\\(?:input|include)\{([^}]*)\}")
HEADING = re.compile(
    r"^\s*\\(?:part|chapter|section|subsection|subsubsection)\*?\s*(?:\[[^\]]*\])?\{.*\}\s*"
    r"(?:\\label\{[^}]*\}\s*)*$", re.S)
BEGIN = re.compile(r"\\begin\{([^}]*)\}")
END = re.compile(r"\\end\{([^}]*)\}")
# Blocks that produce no text a reader would examine.
NON_PROSE = re.compile(
    r"\\(?:maketitle|appendix|newpage|clearpage|pagebreak|tableofcontents|bibliography"
    r"|bibliographystyle|printbibliography|label|onecolumn|twocolumn|FloatBarrier"
    r"|vspace\*?|vfill|medskip|bigskip|smallskip|noindent)\b(?:\{[^}]*\})?")
# Lines that start a new paragraph, and lines that end one, even without a blank line.
BREAK_BEFORE = re.compile(
    r"\s*\\(?:part|chapter|section|subsection|subsubsection|paragraph|appendix|maketitle"
    r"|bibliography|printbibliography)\b|\s*\\begin\{(?:abstract|thebibliography)\}")
BREAK_AFTER = re.compile(r"\\end\{abstract\}|\\(?:appendix|maketitle)\s*$|\\(?:bibliography|bibliographystyle)\{[^}]*\}\s*$")
REFERENCES = re.compile(r"\\(?:bibliography|printbibliography)\b|\\begin\{thebibliography\}")


def resolve(path, base):
    """Path of an \\input argument, relative to the main file's directory."""
    path = os.path.join(base, path)
    return path if os.path.exists(path) or path.endswith(".tex") else path + ".tex"


def flatten(main, base=None, _depth=0):
    """Lines of the document with \\input and \\include expanded and comments removed.

    Returns a list of (file, line number, text), the file relative to `base`.
    """
    base = base or os.path.dirname(os.path.abspath(main))
    if _depth > 20:
        raise ValueError(f"\\input nested too deeply at {main}")
    lines = []
    with open(main, encoding="utf-8") as f:
        for number, line in enumerate(f, 1):
            text = COMMENT.sub("", line.rstrip("\n"))
            rel = os.path.relpath(main, base)
            position = 0
            for match in INPUT.finditer(text):
                before = text[position:match.start()]
                if before.strip():
                    lines.append((rel, number, before))
                included = resolve(match.group(1), base)
                if os.path.exists(included):
                    lines.extend(flatten(included, base, _depth + 1))
                position = match.end()
            rest = text[position:]
            if rest.strip() or position == 0:
                lines.append((rel, number, rest))
    return lines


def is_prose(text):
    stripped = NON_PROSE.sub("", text)
    stripped = re.sub(r"\\(?:begin|end)\{(?:document|abstract)\}", "", stripped)
    return bool(stripped.strip())


def paragraphs(main):
    """Split the document body into the paragraphs a reader examines, in order.

    A paragraph is a block of lines between blank lines. An environment (table,
    figure, itemize, equation, ...) is never split, a heading goes with the
    paragraph that follows it, and blocks without prose (\\maketitle, \\label, ...)
    are skipped. Each paragraph records whether it belongs to the abstract, the
    core or the appendices.
    """
    lines = flatten(main)
    starts = [i for i, (_, _, t) in enumerate(lines) if "\\begin{document}" in t]
    ends = [i for i, (_, _, t) in enumerate(lines) if "\\end{document}" in t]
    if starts:
        first = lines[starts[0]]
        lines = [(first[0], first[1], first[2].split("\\begin{document}", 1)[1])] + lines[starts[0] + 1:]
    if ends:
        ends = [i for i, (_, _, t) in enumerate(lines) if "\\end{document}" in t]
        last = lines[ends[0]]
        lines = lines[:ends[0]] + [(last[0], last[1], last[2].split("\\end{document}", 1)[0])]

    blocks, current, depth = [], [], 0

    def flush():
        nonlocal current
        if current:
            blocks.append(current)
            current = []

    for item in lines:
        text = item[2]
        if not text.strip() and depth == 0:
            flush()
            continue
        if depth == 0 and BREAK_BEFORE.match(text):
            flush()
        current.append(item)
        opened = [e for e in BEGIN.findall(text) if e not in ("document",)]
        closed = [e for e in END.findall(text) if e not in ("document",)]
        depth = max(0, depth + len(opened) - len(closed))
        if depth == 0 and BREAK_AFTER.search(text):
            flush()
    flush()

    result, pending, region = [], [], "core"
    for block in blocks:
        text = "\n".join(t for _, _, t in block).strip("\n")
        if "\\appendix" in text:
            region = "appendix"
        if REFERENCES.search(text) and region == "core":
            region = "references"
        if HEADING.match(text):
            pending = block + [("", 0, "")]
            continue
        if not is_prose(text) and "\\begin{abstract}" not in text:
            continue
        block = pending + block
        pending = []
        kind = "abstract" if "\\begin{abstract}" in text or "\\end{abstract}" in text else region
        if kind == "references":
            continue
        located = [(f, n) for f, n, t in block if f and t.strip()]
        result.append({
            "id": f"P{len(result) + 1}",
            "kind": kind,
            "text": "\n".join(t for _, _, t in block).strip("\n"),
            "file": located[0][0],
            "lines": [located[0][1], located[-1][1]],
        })
    return result


def abstract_words(paras):
    """Words of the abstract, counting a formula as one word."""
    text = "\n".join(p["text"] for p in paras if p["kind"] == "abstract")
    text = re.sub(r"\\(?:begin|end)\{abstract\}", " ", text)
    text = re.sub(r"\$[^$]*\$", " formula ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    text = re.sub(r"[{}~\\]", " ", text)
    return len([w for w in text.split() if re.search(r"\w", w)])


# -------------------------------------------------------------- compiling

def insert_core_end(main):
    """Put the core-end label before the references or the appendices of the copy."""
    base = os.path.dirname(os.path.abspath(main))
    for path, _, _ in flatten(main):
        full = os.path.join(base, path)
        with open(full, encoding="utf-8") as f:
            if CORE_END in f.read():
                return
    candidates = []
    for path, number, text in flatten(main):
        if "\\appendix" in text or REFERENCES.search(text) or "\\end{document}" in text:
            candidates.append((path, number))
            break
    if not candidates:
        raise ValueError("no \\appendix, references or \\end{document} in the paper")
    path, number = candidates[0]
    full = os.path.join(base, path)
    with open(full, encoding="utf-8") as f:
        lines = f.readlines()
    lines.insert(number - 1, f"\\label{{{CORE_END}}}% autoreview: end of the core, removed at the end\n")
    with open(full, "w", encoding="utf-8") as f:
        f.writelines(lines)


def remove_core_end(directory):
    for folder, _, files in os.walk(directory):
        for name in files:
            if name.endswith(".tex"):
                path = os.path.join(folder, name)
                with open(path, encoding="utf-8") as f:
                    text = f.read()
                if CORE_END in text:
                    text = re.sub(r"\\label\{" + CORE_END + r"\}[^\n]*\n", "", text)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(text)


def compile_paper(main):
    """Compile with latexmk; return the page of the core end (None if it failed)."""
    directory, name = os.path.split(os.path.abspath(main))
    run = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", name],
        cwd=directory, capture_output=True, text=True)
    aux = os.path.join(directory, os.path.splitext(name)[0] + ".aux")
    if run.returncode != 0 or not os.path.exists(aux):
        log = run.stdout[-3000:]
        return None, log
    with open(aux, encoding="utf-8", errors="replace") as f:
        match = re.search(r"\\newlabel\{" + CORE_END + r"\}\{\{[^}]*\}\{([^}]*)\}", f.read())
    return (int(match.group(1)) if match and match.group(1).isdigit() else None), ""


def measure(main):
    """Pages of the core and words of the abstract, as a dict."""
    page, log = compile_paper(main)
    state = {"core_pages": page, "abstract_words": abstract_words(paragraphs(main))}
    if log:
        state["compile_error"] = log
    return state


# ------------------------------------------------------------------ agents

def fill(name, **values):
    with open(os.path.join(PROMPTS, name), encoding="utf-8") as f:
        text = f.read()
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def claude(prompt, *, model, schema=None, system=None, tools="", allowed=(), cwd=None,
           add_dirs=(), plugin=False, log=None):
    """Run one `claude -p` call; return its structured output (or text)."""
    command = ["claude", "-p", "--model", model, "--output-format", "json",
               "--tools", tools, "--setting-sources", "", "--strict-mcp-config",
               "--no-session-persistence", "--disable-slash-commands"]
    if schema:
        command += ["--json-schema", json.dumps(schema)]
    if system:
        command += ["--system-prompt", system]
    if allowed:
        command += ["--allowedTools", *allowed]
    for directory in add_dirs:
        command += ["--add-dir", directory]
    if plugin:
        command = [c for c in command if c != "--disable-slash-commands"]
        command += ["--plugin-dir", PLUGIN_DIR]
    run = subprocess.run(command, input=prompt, capture_output=True, text=True, cwd=cwd)
    if log:
        with open(log, "w", encoding="utf-8") as f:
            f.write(run.stdout or run.stderr)
    try:
        output = json.loads(run.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude failed: {run.stderr[-2000:] or run.stdout[-2000:]}")
    if output.get("is_error"):
        raise RuntimeError(f"claude failed: {output.get('result')}")
    return output.get("structured_output", output.get("result")), output.get("total_cost_usd", 0)


TAGS = ["unclear", "why", "objection", "link", "outside", "missing"]
READER_SCHEMA = {
    "type": "object",
    "properties": {
        "understanding": {"type": "string"},
        "verdict": {"type": "string", "enum": ["clear", "mostly", "unclear"]},
        "questions": {
            "type": "array", "maxItems": 10,
            "items": {
                "type": "object",
                "properties": {
                    "tag": {"type": "string", "enum": TAGS},
                    "quote": {"type": "string"},
                    "question": {"type": "string"},
                    "answer_would_be": {"type": "string"},
                },
                "required": ["tag", "quote", "question", "answer_would_be"],
            },
        },
    },
    "required": ["understanding", "verdict", "questions"],
}
CHANGE = {
    "type": "object",
    "properties": {
        "question_ids": {"type": "array", "items": {"type": "string"}},
        "file": {"type": "string"},
        "before": {"type": "string"},
        "after": {"type": "string"},
        "reason": {"type": "string"},
    },
    "required": ["question_ids", "file", "before", "after", "reason"],
}
EDITOR_SCHEMA = {
    "type": "object",
    "properties": {
        "changes": {"type": "array", "items": CHANGE},
        "author_questions": {"type": "array", "items": {
            "type": "object",
            "properties": {"question_id": {"type": "string"}, "location": {"type": "string"},
                           "question": {"type": "string"}},
            "required": ["question_id", "location", "question"]}},
        "not_answered": {"type": "array", "items": {
            "type": "object",
            "properties": {"question_id": {"type": "string"}, "why": {"type": "string"}},
            "required": ["question_id", "why"]}},
    },
    "required": ["changes", "author_questions", "not_answered"],
}
CUTTER_SCHEMA = {
    "type": "object",
    "properties": {
        "changes": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "kind": {"type": "string",
                         "enum": ["removed", "compressed", "moved", "appendix", "abstract"]},
                "file": {"type": "string"}, "before": {"type": "string"},
                "after": {"type": "string"}, "appendix": {"type": "string"},
                "reason": {"type": "string"}},
            "required": ["kind", "file", "before", "after", "reason"]}},
        "appendices": {"type": "array", "items": {
            "type": "object",
            "properties": {"title": {"type": "string"}, "theme": {"type": "string"}},
            "required": ["title", "theme"]}},
        "core_pages": {"type": "integer"},
        "abstract_words": {"type": "integer"},
    },
    "required": ["changes", "appendices"],
}


def numbered(paras):
    return "\n\n".join(f"[{p['id']}]\n{p['text']}" for p in paras)


def reader_prompt(prefix, target, alone=False):
    """The reader's prompt. The paper comes first so that prompts for successive
    paragraphs share a prefix, which the prompt cache reuses."""
    if alone:
        intro = ("Below are the title and abstract of a paper, then one of its appendices. "
                 "You have not read the main text: you opened the appendix on its own, "
                 "as readers often do. An appendix should be readable this way, except for "
                 "very basic things such as the task and the name of the main method.")
        task = (f"Examine the appendix as a whole, paragraphs {target}. Ask in particular "
                "what cannot be understood without the main text.")
    else:
        intro = "Below is the paper from its beginning, up to the passage you examine."
        task = f"Examine the passage [{target}], the last paragraph above."
    return f"{intro}\n\n<paper>\n{numbered(prefix)}\n</paper>\n\n{task}"


def digest(*parts):
    return hashlib.sha256("\x00".join(parts).encode()).hexdigest()[:20]


class Run:
    def __init__(self, args):
        self.args = args
        self.dir = os.path.abspath(args.out)
        self.work = os.path.join(self.dir, "work")
        self.cache = os.path.join(self.dir, "cache")
        self.cost = 0.0
        self.paper_rel = None

    # -- setup

    def setup(self):
        source_dir = os.path.dirname(os.path.abspath(self.args.paper))
        self.paper_rel = os.path.basename(self.args.paper)
        os.makedirs(self.cache, exist_ok=True)
        if not os.path.exists(self.work):
            shutil.copytree(source_dir, self.work, ignore=shutil.ignore_patterns(
                ".git", "*.aux", "*.log", "*.out", "*.fls", "*.fdb_latexmk", "*.synctex.gz",
                "*.bbl", "*.blg", "*.pdf"))
            # PDFs used as figures are needed to compile: copy those back.
            for folder, _, files in os.walk(source_dir):
                for name in files:
                    if name.endswith(".pdf") and os.path.splitext(name)[0] != os.path.splitext(self.paper_rel)[0]:
                        rel = os.path.relpath(os.path.join(folder, name), source_dir)
                        os.makedirs(os.path.dirname(os.path.join(self.work, rel)), exist_ok=True)
                        shutil.copy2(os.path.join(folder, name), os.path.join(self.work, rel))
            with open(os.path.join(self.work, ".gitignore"), "w") as f:
                f.write("*.aux\n*.log\n*.out\n*.fls\n*.fdb_latexmk\n*.synctex.gz\n*.bbl\n*.blg\n"
                        + os.path.splitext(self.paper_rel)[0] + ".pdf\n")
            self.git("init", "-q")
            self.commit("original paper")
        with open(os.path.join(self.dir, "config.json"), "w") as f:
            json.dump({k: v for k, v in vars(self.args).items() if k != "func"}, f, indent=2)

    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=autoreview", "-c", "user.email=autoreview@localhost",
                               *args], cwd=self.work, capture_output=True, text=True).stdout

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)

    @property
    def main(self):
        return os.path.join(self.work, self.paper_rel)

    def context(self):
        dirs = [os.path.abspath(d) for d in self.args.context]
        if not dirs:
            return "none: answer only from the paper.", []
        return ", ".join(f"`{d}`" for d in dirs) + " (the paper's original directory may be inside: ignore it, the copy here is the one to edit)", dirs

    def allowed_edits(self, extra=()):
        return ["Read", "Glob", "Grep", f"Edit(/{self.work}/**)", f"Write(/{self.work}/**)", *extra]

    def log(self, message):
        print(message, flush=True)
        with open(os.path.join(self.dir, "log.md"), "a", encoding="utf-8") as f:
            f.write(message + "\n")

    # -- reader

    def read_one(self, prefix, target, alone=False):
        prompt = reader_prompt(prefix, target, alone)
        system = fill("reader.md")
        key = digest(self.args.reader_model, system, prompt)
        path = os.path.join(self.cache, f"reader-{key}.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f), True
        result, cost = claude(prompt, model=self.args.reader_model, schema=READER_SCHEMA,
                              system=system, tools="")
        self.cost += cost or 0
        with open(path, "w") as f:
            json.dump(result, f, indent=1)
        return result, False

    def read_paper(self, round_dir, paras):
        """Run the reader on every paragraph, each with only the text before it."""
        jobs = {}
        with concurrent.futures.ThreadPoolExecutor(self.args.parallel) as pool:
            for i, p in enumerate(paras):
                jobs[pool.submit(self.read_one, paras[:i + 1], p["id"])] = p
            results = {}
            for job in concurrent.futures.as_completed(jobs):
                p = jobs[job]
                results[p["id"]], _ = job.result()
        readings = [dict(p, **results[p["id"]]) for p in paras]
        with open(os.path.join(round_dir, "reader.json"), "w") as f:
            json.dump(readings, f, indent=1)
        return readings

    def questions_file(self, round_dir, readings, prefix_id):
        """Write the questions for the editor; return the number of questions."""
        out, count = [], 0
        for r in readings:
            qs = r["questions"]
            if r["verdict"] == "clear" and not qs:
                continue
            last = r["lines"][1]
            out.append(f"## {r['id']} ({r['kind']}), {r['file']}:{r['lines'][0]}-{last}, verdict: {r['verdict']}\n")
            out.append(f"Text:\n\n```latex\n{r['text']}\n```\n")
            out.append(f"Reader's understanding: {r['understanding']}\n")
            for n, q in enumerate(qs, 1):
                q["id"] = f"{prefix_id}{r['id']}.{n}"
                count += 1
                out.append(f"- **{q['id']}** [{q['tag']}] \"{q['quote']}\": {q['question']} "
                           f"(would be answered by: {q['answer_would_be']})")
            out.append("")
        path = os.path.join(round_dir, "questions.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out) or "No questions.\n")
        with open(os.path.join(round_dir, "reader.json"), "w") as f:
            json.dump(readings, f, indent=1)
        return path, count

    # -- editor

    def edit(self, round_dir, questions, mode):
        done = os.path.join(round_dir, "editor.json")
        if os.path.exists(done):
            with open(done) as f:
                return json.load(f)
        text, dirs = self.context()
        asked = os.path.join(self.dir, "author_questions.md")
        asked = (f"`{asked}`: do not ask them again, and treat a reader's question that one of them "
                 "covers as reported" if os.path.exists(asked) else "none yet")
        prompt = fill("editor.md", MAIN=self.paper_rel, CONTEXT=text, QUESTIONS=questions, MODE=mode,
                      ASKED=asked)
        result, cost = claude(prompt, model=self.args.editor_model, schema=EDITOR_SCHEMA,
                              tools="Read,Edit,Write,Glob,Grep", allowed=self.allowed_edits(),
                              cwd=self.work, add_dirs=dirs + [round_dir], plugin=self.args.with_plugin,
                              log=os.path.join(round_dir, "editor-transcript.json"))
        self.cost += cost or 0
        with open(done, "w") as f:
            json.dump(result, f, indent=1)
        return result

    # -- the loop

    def clarity(self):
        verdicts = previous = None
        for n in range(1, self.args.max_rounds + 1):
            round_dir = os.path.join(self.dir, f"round{n}")
            if os.path.exists(os.path.join(round_dir, "done")):
                continue
            os.makedirs(round_dir, exist_ok=True)
            paras = paragraphs(self.main)
            readings = self.read_paper(round_dir, paras)
            verdicts = {v: sum(r["verdict"] == v for r in readings) for v in ("clear", "mostly", "unclear")}
            questions, count = self.questions_file(round_dir, readings, f"R{n}.")
            self.log(f"round {n}: {len(paras)} paragraphs, {verdicts['clear']} clear, "
                     f"{verdicts['mostly']} mostly, {verdicts['unclear']} unclear, {count} questions")
            if verdicts["mostly"] == verdicts["unclear"] == 0:
                self.log("every paragraph is clear")
                return readings
            if verdicts["unclear"] == 0 and previous is not None and verdicts["mostly"] >= previous["mostly"]:
                # What remains is usually waiting for the authors: another round would not change it.
                self.log("no paragraph is unclear and the others no longer improve: stopping")
                return readings
            previous = verdicts
            result = self.edit(round_dir, questions, "Answer the reader's questions.")
            self.record(round_dir, f"round {n}", result["changes"], readings)
            self.write_author_questions(result.get("author_questions", []), f"round {n}")
            self.commit(f"round {n}: answers to the reader")
            open(os.path.join(round_dir, "done"), "w").close()
            self.log(f"round {n}: {len(result['changes'])} changes, "
                     f"{len(result.get('author_questions', []))} questions for the authors")
            if not result["changes"]:
                self.log("the editor made no change: stopping")
                return readings
        self.log(f"stopped after {self.args.max_rounds} rounds")
        return None

    def length(self):
        state = os.path.join(self.dir, "cut")
        os.makedirs(state, exist_ok=True)
        insert_core_end(self.main)
        measured = measure(self.main)
        self.log(f"before the cut: {self.describe(measured)}")
        feedback = ""
        for attempt in range(1, self.args.cut_attempts + 1):
            if self.fits(measured):
                break
            done = os.path.join(state, f"attempt{attempt}.json")
            if os.path.exists(done):
                with open(done) as f:
                    result = json.load(f)
            else:
                text, dirs = self.context()
                command = f"python3 {os.path.abspath(__file__)} measure --run {self.dir}"
                prompt = fill("cutter.md", MAIN=self.paper_rel, CONTEXT=text, LIMITS=self.limits(),
                              MEASURE=command, STATE=self.describe(measured), FEEDBACK=feedback)
                result, cost = claude(prompt, model=self.args.editor_model, schema=CUTTER_SCHEMA,
                                      tools="Read,Edit,Write,Glob,Grep,Bash",
                                      allowed=self.allowed_edits([f"Bash({command})"]),
                                      cwd=self.work, add_dirs=dirs, plugin=self.args.with_plugin,
                                      log=os.path.join(state, f"attempt{attempt}-transcript.json"))
                self.cost += cost or 0
                with open(done, "w") as f:
                    json.dump(result, f, indent=1)
                self.record(state, f"cut {attempt}", result["changes"], None)
                self.commit(f"cut, attempt {attempt}")
            measured = measure(self.main)
            self.log(f"after cut attempt {attempt}: {self.describe(measured)}")
            feedback = (f"An earlier attempt left the paper at {self.describe(measured)}: "
                        "the limits are not met yet. Continue from the current files.")
        self.appendices()
        return measured

    def appendices(self):
        """Ask the reader about each appendix read on its own, then fix them once."""
        round_dir = os.path.join(self.dir, "appendices")
        os.makedirs(round_dir, exist_ok=True)
        paras = paragraphs(self.main)
        front = [p for p in paras if p["kind"] == "abstract"]
        groups, current = [], []
        for p in paras:
            if p["kind"] != "appendix":
                continue
            if re.match(r"\s*\\section", p["text"]) and current:
                groups.append(current)
                current = []
            current.append(p)
        if current:
            groups.append(current)
        if not groups:
            return
        readings = []
        for group in groups:
            ids = f"{group[0]['id']} to {group[-1]['id']}"
            result, _ = self.read_one(front + group, ids, alone=True)
            readings.append(dict(group[0], text="\n\n".join(p["text"] for p in group),
                                 id=f"{group[0]['id']}-{group[-1]['id']}", **result))
        questions, count = self.questions_file(round_dir, readings, "A.")
        self.log(f"appendices read alone: {count} questions")
        if not count or os.path.exists(os.path.join(round_dir, "done")):
            return
        mode = ("This time the reader read each appendix on its own, after the abstract only. "
                "Make each appendix self-contained by changing the appendices only: the core is "
                "at its page limit and must not grow.")
        result = self.edit(round_dir, questions, mode)
        self.record(round_dir, "appendices", result["changes"], readings)
        self.write_author_questions(result.get("author_questions", []), "appendices")
        self.commit("appendices made self-contained")
        open(os.path.join(round_dir, "done"), "w").close()

    # -- bookkeeping

    def limits(self):
        parts = []
        if self.args.pages:
            parts.append(f"the core has at most {self.args.pages} pages")
        if self.args.abstract_words:
            parts.append(f"the abstract has at most {self.args.abstract_words} words")
        return "; ".join(parts) or "none"

    def fits(self, m):
        return (m["core_pages"] is not None
                and (not self.args.pages or m["core_pages"] <= self.args.pages)
                and (not self.args.abstract_words or m["abstract_words"] <= self.args.abstract_words))

    @staticmethod
    def describe(m):
        if m.get("compile_error"):
            return f"the paper does not compile (abstract: {m['abstract_words']} words)"
        return f"core {m['core_pages']} pages, abstract {m['abstract_words']} words"

    def record(self, where, stage, changes, readings):
        """Append the changes to corrections.jsonl and corrections.txt."""
        questions = {}
        for r in readings or []:
            for q in r["questions"]:
                if "id" in q:
                    questions[q["id"]] = (r["id"], q)
        date = datetime.date.today().isoformat()
        name = os.path.basename(self.dir)
        with open(os.path.join(self.dir, "corrections.jsonl"), "a", encoding="utf-8") as js, \
             open(os.path.join(self.dir, "corrections.txt"), "a", encoding="utf-8") as txt:
            for change in changes:
                asked = [dict(questions[i][1], paragraph=questions[i][0])
                         for i in change.get("question_ids", []) if i in questions]
                js.write(json.dumps(dict(change, stage=stage, questions=asked)) + "\n")
                if asked:
                    message = "\n".join(f"Reader on {q['paragraph']} [{q['tag']}] \"{q['quote']}\": "
                                        f"{q['question']}" for q in asked)
                elif "kind" in change:
                    message = f"Length limit ({change['kind']}): {change['reason']}"
                else:
                    message = f"Consistency: {change['reason']}"
                txt.write(f"=== [{date}] autoreview/{name} ({stage})\n{message}\n"
                          f"--- in reply, Claude changed {change['file']}:\n"
                          f"- {change['before']}\n+ {change['after']}\n")

    def write_author_questions(self, questions, stage):
        if not questions:
            return
        with open(os.path.join(self.dir, "author_questions.md"), "a", encoding="utf-8") as f:
            for q in questions:
                f.write(f"- ({stage}, {q['location']}) {q['question']}\n")


def run(args):
    r = Run(args)
    r.setup()
    r.log(f"\n# autoreview {datetime.datetime.now():%Y-%m-%d %H:%M}, paper {args.paper}")
    r.clarity()
    if args.pages or args.abstract_words:
        m = r.length()
        if not r.fits(m):
            r.log("the limits are not met: see cut/ and the log")
    if args.final_read:
        final = os.path.join(r.dir, "final")
        os.makedirs(final, exist_ok=True)
        readings = r.read_paper(final, [p for p in paragraphs(r.main) if p["kind"] != "appendix"])
        _, count = r.questions_file(final, readings, "F.")
        verdicts = {v: sum(x["verdict"] == v for x in readings) for v in ("clear", "mostly", "unclear")}
        r.log(f"final reading of the core: {verdicts}, {count} questions (final/questions.md)")
    out = os.path.join(r.dir, "paper")
    if os.path.exists(out):
        shutil.rmtree(out)
    shutil.copytree(r.work, out, ignore=shutil.ignore_patterns(".git"))
    remove_core_end(out)
    r.log(f"revised paper: {out}\ncorrections: {os.path.join(r.dir, 'corrections.txt')}\n"
          f"cost of this invocation: ${r.cost:.2f}")


def measure_command(args):
    with open(os.path.join(args.run, "config.json")) as f:
        config = json.load(f)
    main = os.path.join(args.run, "work", os.path.basename(config["paper"]))
    m = measure(main)
    print(Run.describe(m))
    if m.get("compile_error"):
        print(m["compile_error"])


def rules_command(args):
    files = [os.path.join(os.path.abspath(r), "corrections.txt") for r in args.runs]
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        sys.exit(f"no corrections in: {', '.join(missing)}")
    out = os.path.abspath(args.out)
    notes = os.path.splitext(out)[0] + ".notes.md"
    prompt = fill("rules.md", CORRECTIONS=", ".join(f"`{f}`" for f in files), NOTES=notes, OUTPUT=out)
    result, cost = claude(prompt, model=args.model, tools="Read,Write,Edit,Glob,Grep",
                          allowed=["Read", "Glob", "Grep", f"Edit(/{out})", f"Write(/{out})",
                                   f"Edit(/{notes})", f"Write(/{notes})"],
                          cwd=ROOT, add_dirs=[os.path.dirname(out)] + [os.path.dirname(f) for f in files])
    print(result)
    print(f"cost: ${cost or 0:.2f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("run", help="revise a paper")
    p.add_argument("--paper", required=True, help="main .tex file; its directory is copied")
    p.add_argument("--context", action="append", default=[],
                   help="directory the editor may read: code, logs, notes (repeatable)")
    p.add_argument("--out", required=True, help="run directory")
    p.add_argument("--pages", type=int, help="page limit of the core")
    p.add_argument("--abstract-words", type=int, help="word limit of the abstract")
    p.add_argument("--max-rounds", type=int, default=4)
    p.add_argument("--cut-attempts", type=int, default=3)
    p.add_argument("--reader-model", default="opus")
    p.add_argument("--editor-model", default="opus")
    p.add_argument("--parallel", type=int, default=4, help="reader calls run at the same time")
    p.add_argument("--with-plugin", action="store_true",
                   help="load the writing-toolkit plugin (rules and linter) in the editor and cutter; "
                        "leave it off when the corrections are meant to produce new rules")
    p.add_argument("--no-final-read", dest="final_read", action="store_false",
                   help="skip the last reading of the core after the cut")
    p.set_defaults(func=run)
    p = sub.add_parser("measure", help="compile a run's paper and print its length")
    p.add_argument("--run", required=True)
    p.set_defaults(func=measure_command)
    p = sub.add_parser("rules", help="draft writing rules from the corrections of runs")
    p.add_argument("runs", nargs="+")
    p.add_argument("--out", required=True)
    p.add_argument("--model", default="opus")
    p.set_defaults(func=rules_command)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
