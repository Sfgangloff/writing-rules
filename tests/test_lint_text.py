import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr
from unittest import mock

from helpers import load

lint = load("plugin/skills/academic-writing/scripts/lint_text.py")


class LintTest(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.TemporaryDirectory()
        self.project = tempfile.TemporaryDirectory()
        patcher = mock.patch.dict(os.environ, {"HOME": self.home.name})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.home.cleanup)
        self.addCleanup(self.project.cleanup)

    def ids(self, text, tex=True):
        rules = lint.load_config(self.project.name)["rules"]
        return [rule["id"] for _, _, rule, _, _ in lint.find(text, rules, tex)]

    def write_override(self, directory, rules):
        folder = os.path.join(directory, ".claude", "writing-rules")
        os.makedirs(folder)
        with open(os.path.join(folder, "lint.json"), "w") as handle:
            json.dump({"rules": rules}, handle)

    def test_default_rules_match(self):
        self.assertEqual(self.ids("We use A rather than B."), ["rather-than"])
        self.assertEqual(self.ids("A model—a big one."), ["em-dash"])
        self.assertEqual(self.ids("A model---a big one."), ["em-dash"])
        self.assertEqual(self.ids("A model --- a big one."), ["em-dash"])
        self.assertEqual(self.ids("---\n<!-- note -->", tex=False), [])
        self.assertEqual(self.ids("This is genuinely new."), ["intensifiers"])
        self.assertEqual(self.ids("The method is fast."), [])

    def test_latex_comments_and_escaped_percent(self):
        self.assertEqual(self.ids("% rather than"), [])
        self.assertEqual(self.ids("50\\% rather than 40"), ["rather-than"])
        self.assertEqual(self.ids("% rather than", tex=False), ["rather-than"])

    def test_fix_keeps_case_and_comments(self):
        rules = lint.load_config(self.project.name)["rules"]
        text = "Rather than A, B rather than C. % rather than\n"
        self.assertEqual(lint.fix(text, rules, True), "Instead of A, B instead of C. % rather than\n")

    def test_user_and_project_overrides(self):
        self.write_override(self.home.name, [{"id": "rather-than", "enabled": False}])
        self.assertEqual(self.ids("A rather than B"), [])
        self.write_override(self.project.name, [
            {"id": "rather-than", "enabled": True, "replace": "and not"},
            {"id": "utilize", "pattern": "\\butilize\\b", "message": "use 'use'", "replace": "use"},
        ])
        rules = lint.load_config(self.project.name)["rules"]
        self.assertEqual(lint.fix("Rather than X we utilize Y", rules, False), "And not X we use Y")

    def test_invalid_rule_is_skipped(self):
        self.write_override(self.project.name, [{"id": "broken", "pattern": "(", "message": "x"}])
        with redirect_stderr(io.StringIO()):
            ids = [rule["id"] for rule in lint.load_config(self.project.name)["rules"]]
        self.assertNotIn("broken", ids)
        self.assertIn("rather-than", ids)

    def run_hook(self, event):
        stderr = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO(json.dumps(event))), redirect_stderr(stderr):
            status = lint.run_hook()
        return status, stderr.getvalue()

    def test_hook_lints_only_new_text_of_tex_files(self):
        path = os.path.join(self.project.name, "paper.tex")
        status, report = self.run_hook({"tool_input": {
            "file_path": path, "old_string": "rather than", "new_string": "This is truly new."}})
        self.assertEqual(status, 2)
        self.assertIn("truly", report)
        self.assertNotIn("rather-than", report)

        status, _ = self.run_hook({"tool_input": {"file_path": path, "content": "Plain text."}})
        self.assertEqual(status, 0)
        status, _ = self.run_hook({"tool_input": {"file_path": "notes.py", "content": "rather than"}})
        self.assertEqual(status, 0)

    def test_hook_reads_multiedit(self):
        path = os.path.join(self.project.name, "paper.tex")
        status, report = self.run_hook({"tool_input": {"file_path": path, "edits": [
            {"old_string": "a", "new_string": "fine"}, {"old_string": "b", "new_string": "a testbed"}]}})
        self.assertEqual(status, 2)
        self.assertIn("testbed", report)


if __name__ == "__main__":
    unittest.main()
