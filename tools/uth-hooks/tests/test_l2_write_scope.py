from __future__ import annotations

import unittest

from helpers import REPO_ROOT, assert_has, load_config
from uth_hooks.l2_write_scope import check_file_write


class TestL2WriteScope(unittest.TestCase):
    def test_write_skills_in_uth_dev_blocks(self):
        findings = check_file_write(
            {"active_scene": "uth-dev", "paths": ["skills/uth-dev/SKILL.md"]},
            load_config(),
            REPO_ROOT,
        )

        assert_has(findings, "BLOCK", "skill-write-blocked")


    def test_write_docs_context_in_uth_dev_blocks(self):
        findings = check_file_write(
            {"active_scene": "uth-dev", "paths": ["docs/context/10-backend.md"]},
            load_config(),
            REPO_ROOT,
        )

        assert_has(findings, "BLOCK", "context-write-blocked")


    def test_non_docs_scenes_do_not_pass_global_docs_markdown_writes(self):
        for scene in ("uth-design", "uth-debug", "uth-review"):
            with self.subTest(scene=scene):
                findings = check_file_write(
                    {"active_scene": scene, "paths": ["docs/current-state.md"]},
                    load_config(),
                    REPO_ROOT,
                )

                self.assertFalse(
                    any(item.get("decision") == "PASS" for item in findings),
                    findings,
                )
                assert_has(findings, "BLOCK", "global-doc-write-blocked")


    def test_uth_docs_can_write_global_docs_markdown(self):
        findings = check_file_write(
            {"active_scene": "uth-docs", "paths": ["docs/current-state.md"]},
            load_config(),
            REPO_ROOT,
        )

        assert_has(findings, "PASS", "write-allowed")


    def test_forbidden_writes_override_allowed_writes(self):
        findings = check_file_write(
            {
                "active_scene": "uth-dev",
                "paths": ["src/generated/out.py"],
                "allowed_writes": ["src/**"],
                "forbidden_writes": ["src/generated/**"],
            },
            load_config(),
            REPO_ROOT,
        )

        assert_has(findings, "BLOCK", "write-forbidden")


    def test_uth_git_can_append_formal_feedback_baseline(self):
        findings = check_file_write(
            {
                "active_scene": "uth-git",
                "paths": ["docs/work/D26051601-demo/11-D26051601-T01-feedback-demo.md"],
            },
            load_config(),
            REPO_ROOT,
        )

        assert_has(findings, "PASS", "write-allowed")


if __name__ == "__main__":
    unittest.main()
