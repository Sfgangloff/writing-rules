import json
import os
import re
import unittest

from helpers import ROOT, SKILL


class PluginTest(unittest.TestCase):
    def test_manifests_are_valid_json(self):
        for path in [".claude-plugin/marketplace.json", "plugin/.claude-plugin/plugin.json",
                     "plugin/hooks/hooks.json", "plugin/skills/academic-writing/scripts/lint_rules.json"]:
            with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
                json.load(handle)

    def test_skill_lists_exactly_the_reference_files(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as handle:
            skill = handle.read()
        self.assertTrue(skill.startswith("---\nname: academic-writing\ndescription: "))
        listed = set(re.findall(r"`reference/([\w-]+\.md)`", skill))
        present = set(os.listdir(os.path.join(SKILL, "reference")))
        self.assertEqual(listed, present)

    def test_default_rules_have_unique_ids(self):
        with open(os.path.join(SKILL, "scripts", "lint_rules.json"), encoding="utf-8") as handle:
            ids = [rule["id"] for rule in json.load(handle)["rules"]]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
