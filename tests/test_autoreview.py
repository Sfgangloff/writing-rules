import os
import shutil
import tempfile
import unittest

from helpers import load

autoreview = load("tools/autoreview/autoreview.py")

MAIN = r"""\documentclass{article}
\begin{document}
\maketitle
\begin{abstract}
\input{abstract}
\end{abstract}
\section{Introduction}
\label{sec:intro}

First paragraph, % a comment the reader must not see
over two lines.

\input{sections/body}

\bibliography{refs}
\appendix
\section{Proofs}

An appendix paragraph.
\end{document}
"""

BODY = r"""Second paragraph.

\begin{table}[t]
\centering
\begin{tabular}{ll}
a & b \\

c & d \\
\end{tabular}
\caption{A table with a blank line inside.}
\end{table}
"""


class Paper:
    def __init__(self, abstract="We study $x+y$ with \\emph{hints}, in 12 words or so."):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, "sections"))
        self.write("main.tex", MAIN)
        self.write("abstract.tex", abstract)
        self.write("sections/body.tex", BODY)
        self.main = os.path.join(self.dir, "main.tex")

    def write(self, name, text):
        with open(os.path.join(self.dir, name), "w") as f:
            f.write(text)

    def read(self, name):
        with open(os.path.join(self.dir, name)) as f:
            return f.read()


class TestParagraphs(unittest.TestCase):
    def setUp(self):
        self.paper = Paper()
        self.addCleanup(shutil.rmtree, self.paper.dir)

    def test_order_kinds_and_locations(self):
        paras = autoreview.paragraphs(self.paper.main)
        self.assertEqual([p["kind"] for p in paras], ["abstract", "core", "core", "core", "appendix"])
        self.assertEqual([p["id"] for p in paras], ["P1", "P2", "P3", "P4", "P5"])
        self.assertEqual(paras[2]["file"], os.path.join("sections", "body.tex"))
        self.assertEqual(paras[2]["lines"], [1, 1])

    def test_heading_goes_with_next_paragraph_and_comments_are_removed(self):
        intro = autoreview.paragraphs(self.paper.main)[1]["text"]
        self.assertTrue(intro.startswith("\\section{Introduction}"))
        self.assertIn("First paragraph,", intro)
        self.assertNotIn("comment", intro)

    def test_environment_is_not_split(self):
        table = autoreview.paragraphs(self.paper.main)[3]["text"]
        self.assertIn("a & b", table)
        self.assertIn("c & d", table)
        self.assertIn("\\end{table}", table)

    def test_empty_abstract_is_kept(self):
        paper = Paper(abstract="% TODO: abstract\n")
        self.addCleanup(shutil.rmtree, paper.dir)
        paras = autoreview.paragraphs(paper.main)
        self.assertEqual(paras[0]["kind"], "abstract")
        self.assertEqual(autoreview.abstract_words(paras), 0)

    def test_abstract_words(self):
        paras = autoreview.paragraphs(self.paper.main)
        # We study [formula] with hints, in 12 words or so.
        self.assertEqual(autoreview.abstract_words(paras), 10)


class TestCoreEnd(unittest.TestCase):
    def test_label_before_references_and_removed(self):
        paper = Paper()
        self.addCleanup(shutil.rmtree, paper.dir)
        autoreview.insert_core_end(paper.main)
        autoreview.insert_core_end(paper.main)  # idempotent
        text = paper.read("main.tex")
        self.assertEqual(text.count(autoreview.CORE_END), 1)
        self.assertLess(text.index(autoreview.CORE_END), text.index("\\bibliography"))
        self.assertEqual(len(autoreview.paragraphs(paper.main)), 5)
        autoreview.remove_core_end(paper.dir)
        self.assertEqual(paper.read("main.tex"), MAIN)

    def test_label_before_end_of_document(self):
        paper = Paper()
        self.addCleanup(shutil.rmtree, paper.dir)
        paper.write("main.tex", "\\begin{document}\nText.\n\\end{document}\n")
        autoreview.insert_core_end(paper.main)
        lines = paper.read("main.tex").splitlines()
        self.assertIn(autoreview.CORE_END, lines[2])
        self.assertEqual(lines[3], "\\end{document}")


class TestReaderPrompt(unittest.TestCase):
    def test_successive_prompts_share_a_prefix(self):
        paras = [{"id": f"P{i}", "text": f"text {i}"} for i in range(1, 4)]
        first = autoreview.reader_prompt(paras[:2], "P2")
        second = autoreview.reader_prompt(paras[:3], "P3")
        shared = first.split("</paper>")[0]
        self.assertTrue(second.startswith(shared))
        self.assertNotIn("text 3", first)


if __name__ == "__main__":
    unittest.main()
