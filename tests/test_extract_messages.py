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


if __name__ == "__main__":
    unittest.main()
