import os
import tempfile
import unittest

from helpers import load

anonymity = load("tools/check_anonymity.py")


class AnonymityTest(unittest.TestCase):
    def labels(self, text, forbid=()):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as handle:
            handle.write(text)
        self.addCleanup(os.remove, handle.name)
        return [label for _, label, _ in anonymity.check(handle.name, anonymity.forbidden_terms(forbid))]

    def test_detects_identifying_patterns(self):
        self.assertIn("email", self.labels("write to jane.doe@uni.edu"))
        self.assertIn("URL", self.labels("see https://example.org/paper"))
        self.assertIn("file path", self.labels("in /Users/jane/paper.tex"))
        self.assertIn("file path", self.labels("in /home/jane/paper.tex"))
        self.assertIn("@handle", self.labels("thanks @janedoe"))

    def test_detects_identity_strings_and_their_parts(self):
        self.assertEqual(self.labels("Jane wrote this", ["Jane Doe"]), ["identity string"])
        self.assertEqual(self.labels("nothing here", ["Jane Doe"]), [])

    def test_ignores_generic_email_parts(self):
        self.assertEqual(anonymity.forbidden_terms(["jane@gmail.com"]), ["jane", "jane@gmail.com"])

    def test_clean_rule_passes(self):
        self.assertEqual(self.labels('- "rather than" -> "instead of"\n'), [])


if __name__ == "__main__":
    unittest.main()
