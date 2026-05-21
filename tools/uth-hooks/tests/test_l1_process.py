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


    def test_subagent_issue_requires_origin_worker_fix(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "formal-dev",
                "subagent_issue_loop": {
                    "issue_found": True,
                    "origin_worker_id": "worker-B",
                    "finding_evaluator_id": "evaluator-A",
                    "fix_worker_id": "worker-C",
                },
                "require_uth_sp_decision": False,
            }
        )

        assert_has(findings, "BLOCK", "subagent-fix-worker-mismatch")


    def test_subagent_issue_requires_origin_evaluator_recheck_after_fix(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "formal-dev",
                "subagent_issue_loop": {
                    "issue_found": True,
                    "origin_worker_id": "worker-B",
                    "finding_evaluator_id": "evaluator-A",
                    "fix_worker_id": "worker-B",
                    "fix_completed": True,
                    "recheck_evaluator_id": "evaluator-C",
                },
                "require_uth_sp_decision": False,
            }
        )

        assert_has(findings, "BLOCK", "subagent-recheck-evaluator-mismatch")


    def test_subagent_issue_cannot_close_without_recheck(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "formal-dev",
                "subagent_issue_loop": {
                    "issue_found": True,
                    "origin_worker_id": "worker-B",
                    "finding_evaluator_id": "evaluator-A",
                    "fix_worker_id": "worker-B",
                    "fix_completed": True,
                    "recheck_evaluator_id": "evaluator-A",
                    "issue_closed": True,
                },
                "require_uth_sp_decision": False,
            }
        )

        assert_has(findings, "BLOCK", "subagent-issue-loop-open")


    def test_subagent_issue_loop_passes_with_origin_worker_and_evaluator(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "formal-dev",
                "subagent_issue_loop": {
                    "issue_found": True,
                    "origin_worker_id": "worker-B",
                    "finding_evaluator_id": "evaluator-A",
                    "fix_worker_id": "worker-B",
                    "fix_completed": True,
                    "recheck_evaluator_id": "evaluator-A",
                    "recheck_completed": True,
                    "issue_closed": True,
                },
                "require_uth_sp_decision": False,
            }
        )

        assert_has(findings, "PASS", "subagent-issue-loop-pass")


    def test_formal_dev_requires_task_package_design_and_todo(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "formal-dev",
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "BLOCK", "formal-task-package-missing")
        assert_has(findings, "BLOCK", "formal-design-missing")
        assert_has(findings, "BLOCK", "formal-todo-missing")


    def test_formal_dev_accepts_task_package_design_and_todo_evidence(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "formal-dev",
                "task_package_path": "docs/work/D26052101-demo",
                "accepted_design_path": "docs/work/D26052101-demo/00-D26052101-design.md",
                "active_todo": "docs/work/D26052101-demo/10-D26052101-T01-todo-demo.md",
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "PASS", "formal-task-package-evidence-present")


    def test_todo_breakdown_requires_accepted_design(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "todo-breakdown",
                "task_package_path": "docs/work/D26052101-demo",
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "BLOCK", "formal-design-missing")


    def test_current_design_without_acceptance_does_not_satisfy_formal_gate(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-dev",
                "mode": "todo-breakdown",
                "task_package_path": "docs/work/D26052101-demo",
                "current_design": "docs/work/D26052101-demo/00-D26052101-design.md",
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "BLOCK", "formal-design-missing")


    def test_design_to_dev_requires_user_confirmation_after_explicit_handoff(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-design",
                "transition": {
                    "from": "uth-design",
                    "to": "uth-dev",
                    "explicit_handoff": True,
                },
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "ASK", "design-dev-user-confirmation-missing")


    def test_document_write_intent_requires_brainstorming_preflight(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-design",
                "mode": "design-authoring",
                "docs_write_intent": True,
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "BLOCK", "document-preflight-brainstorming-missing")


    def test_document_write_intent_requires_no_open_user_questions(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-design",
                "mode": "design-authoring",
                "docs_write_intent": True,
                "document_preflight": {"brainstorming_invoked": True},
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "ASK", "document-preflight-confirmation-missing")


    def test_web_page_design_requires_ui_ux_pro_max(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-design",
                "mode": "design-authoring",
                "design_target": "web-page",
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "BLOCK", "web-design-uiux-skill-missing")


    def test_frontend_page_layout_requires_ui_ux_pro_max(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-design",
                "mode": "design-authoring",
                "design_target": "frontend page layout",
                "uth_sp": {"decision_recorded": True},
            }
        )

        assert_has(findings, "BLOCK", "web-design-uiux-skill-missing")


    def test_android_ui_design_does_not_require_ui_ux_pro_max(self):
        findings = check_l1_process(
            {
                "active_scene": "uth-design",
                "mode": "design-authoring",
                "design_target": "android-ui",
                "uth_sp": {"decision_recorded": True},
            }
        )

        self.assertFalse(any(item.get("code") == "web-design-uiux-skill-missing" for item in findings), findings)


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
