from __future__ import annotations

import json
import unittest

from helpers import HOOK_ROOT


class TestHookSchemas(unittest.TestCase):
    def test_event_schema_exists_and_declares_event_type(self):
        data = json.loads((HOOK_ROOT / "schemas" / "event.schema.json").read_text(encoding="utf-8"))

        self.assertEqual(data["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIn("type", data["properties"])

    def test_project_marker_schema_exists_and_matches_marker_version(self):
        data = json.loads((HOOK_ROOT / "schemas" / "project-marker.schema.json").read_text(encoding="utf-8"))

        self.assertEqual(data["properties"]["schema"]["const"], "uth-governance-project/v1")
        self.assertIn("entrypoints", data["required"])

    def test_closeout_evidence_schema_exists(self):
        data = json.loads((HOOK_ROOT / "schemas" / "closeout-evidence.schema.json").read_text(encoding="utf-8"))

        self.assertIn("active_scene", data["required"])
        self.assertIn("verification", data["properties"])


if __name__ == "__main__":
    unittest.main()
