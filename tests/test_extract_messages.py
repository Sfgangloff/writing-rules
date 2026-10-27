import json
import os
import tempfile
import unittest

from helpers import load

extract = load("tools/extract_messages.py")


class ExtractTest(unittest.TestCase):
    def test_project_name_drops_the_home_directory(self):
        for folder, expected in [
            ("-Users-me-Desktop-Paper", "Desktop-Paper"),
            ("-home-alice-papers-thesis", "papers-thesis"),
            ("C--Users-bob-Docs-Thesis", "Docs-Thesis"),
            ("-Users-me", "home"),
        ]:
            self.assertEqual(extract.project_name(f"/projects/{folder}/session.jsonl"), expected)

    def test_message_text_keeps_only_typed_text(self):
        typed = {"type": "user", "message": {"content": "Remove this sentence <system-reminder>x</system-reminder>"}}
        self.assertEqual(extract.message_text(typed), "Remove this sentence")
        parts = {"type": "user", "message": {"content": [
            {"type": "text", "text": "Not clear"}, {"type": "tool_result", "content": "output"}]}}
        self.assertEqual(extract.message_text(parts), "Not clear")

    def test_message_text_skips_other_entries(self):
        self.assertIsNone(extract.message_text({"type": "assistant", "message": {"content": "hi"}}))
        self.assertIsNone(extract.message_text({"type": "user", "isMeta": True, "message": {"content": "x"}}))
        self.assertIsNone(extract.message_text({"type": "user", "message": {"content": "<command-name>/x"}}))


    def test_read_session_attaches_text_changes(self):
        def edit(path, old, new):
            return {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Edit", "input": {"file_path": path, "old_string": old, "new_string": new}}]}}

        entries = [
            {"type": "user", "message": {"content": "Write the results paragraph"}},
            edit("/Users/me/paper/results.tex", "", "A rather than B"),
            edit("/Users/me/code/train.py", "x", "y"),
            {"type": "user", "message": {"content": [{"type": "tool_result", "content": "ok"}]}},
            {"type": "user", "message": {"content": "rather than -> instead of"}},
            edit("/Users/me/paper/results.tex", "A rather than B", "A instead of B"),
        ]
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
            handle.write("\n".join(json.dumps(entry) for entry in entries))
        self.addCleanup(os.remove, handle.name)

        first, second = list(extract.read_session(handle.name))
        self.assertIsNone(first[2])
        self.assertEqual(first[3], ("results.tex", "- \n+ A rather than B"))
        self.assertEqual(second[1], "rather than -> instead of")
        self.assertEqual(second[2], ("results.tex", "- \n+ A rather than B"))
        self.assertEqual(second[3], ("results.tex", "- A rather than B\n+ A instead of B"))
        self.assertNotIn("/Users/me", str(second))


if __name__ == "__main__":
    unittest.main()
