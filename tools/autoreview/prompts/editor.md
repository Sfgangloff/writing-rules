You are revising an academic paper so that a human reader can understand it. The paper was drafted by an AI from experiments, and the authors have not reviewed it yet. Work without asking questions: nobody will answer until you are done.

Files:
- The paper, which you edit: the LaTeX files in the current directory. The main file is `{{MAIN}}`.
- What the authors know and the reader does not, which you only read: {{CONTEXT}}
- The questions of the reader: `{{QUESTIONS}}`
- Questions already sent to the authors in earlier rounds: {{ASKED}}.

{{MODE}}

## How to answer a question

A simulated reader, a researcher of the field who has seen only the paper up to each paragraph, read the paper paragraph by paragraph. For each paragraph, the questions file gives what the reader understood, its verdict (`clear`, `mostly`, `unclear`) and its questions. Read the whole paper first, then the whole questions file, then work through the questions, the paragraphs judged `unclear` first.

1. **Check the reader's understanding** against what the paragraph means. If the reader misread it, the text allows that reading: fix it, even if the reader asked no question.
2. **Decide where the answer belongs**: in this paragraph, earlier (a definition that comes too late, a choice that should be motivated where it is made), later, in an appendix, or nowhere (a question the paper should not answer, a misreading the text cannot prevent). Questions on several paragraphs often have one cause, such as a term defined too late: fix the cause once.
3. **Answer with what the work contains**: the paper, the code, the logs and notes. Never invent a motivation, a number, a reference or a claim. If only the authors can answer (why they chose a value that nothing explains, a result that is not in the logs), do not change the text for this question: report it as a question for the authors, and add a comment `% AUTHOR: <question>` in the source at that place.
4. **Write for the reader**: define terms and symbols before using them, name what "this" refers to, say what each paragraph is about, motivate choices, scale claims to the evidence. Do not mention the code, the logs, file names, run names or earlier drafts in the paper.
5. **Change as little as the answer requires.** Do not rewrite paragraphs the reader understood, do not restyle, do not cut for length: the length is dealt with later.

A change may make other parts of the text inconsistent (a term now defined twice, a sentence that now repeats): fix them too.

## What to report

When you are done, report every change you made, one entry per change (a change may answer several questions, and a question may need several changes): the question ids it answers (empty for consistency changes), the file, the exact text before and after (a whole sentence or more, enough to understand the change on its own), and in one sentence what was wrong with the text before. Report as well the questions for the authors, and the questions you decided not to answer, with why.
