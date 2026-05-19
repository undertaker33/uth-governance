from __future__ import annotations

import unittest

from helpers import assert_has
from uth_hooks.l1_process import check_l1_process


class TestL1Process(unittest.TestCase):
    def test_scene_missing_blocks(self):
        findings = check_l1_process({"engineering_action": True})

        assert_has(findings, "BLOCK", "scene-ambiguous")


    def test_ambiguity_unresolved_blocks(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-design",
                "ambiguity": {"present": True},
                "require_uth_sp_decision": False,
            }
        )

        assert_has(findings, "BLOCK", "ambiguity-unresolved")


    def test_worker_without_prompt_blocks(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "formal-dev",
                "worker": {"role": "worker"},
                "require_uth_sp_decision": False,
            }
        )

        assert_has(findings, "BLOCK", "worker-prompt-missing")


    def test_light_dev_requires_supported_model_boundary(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "light-dev",
                "llm_model": "unknown-model",
                "task_shape": {
                    "changed_files_count": 1,
                    "modules_count": 1,
                    "implementation_steps_count": 1,
                },
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "BLOCK", "lwdev-unsupported-model")


    def test_light_dev_model_file_limit_blocks(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "light-dev",
                "llm_model": "gpt-5.3-codex-spark",
                "task_shape": {
                    "changed_files_count": 4,
                    "modules_count": 1,
                    "implementation_steps_count": 1,
                },
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "BLOCK", "lwdev-changed-files-limit")


    def test_light_dev_formal_trigger_blocks_for_all_models(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "light-dev",
                "llm_model": "gpt-5.5",
                "task_shape": {
                    "changed_files_count": 1,
                    "modules_count": 1,
                    "implementation_steps_count": 1,
                    "database_schema_or_migration": True,
                },
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "BLOCK", "lwdev-formal-trigger")


    def test_light_dev_supported_model_within_limits_passes(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "light-dev",
                "llm_model": "claude-opus-4.7",
                "task_shape": {
                    "changed_files_count": 2,
                    "modules_count": 1,
                    "implementation_steps_count": 2,
                },
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "PASS", "lwdev-model-boundary-pass")


if __name__ == "__main__":
    unittest.main()
