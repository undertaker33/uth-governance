from __future__ import annotations

import unittest

from helpers import assert_has, dispatch
from uth_hooks.l3_closeout import check_l3_closeout


class TestL3Closeout(unittest.TestCase):
    def test_code_closeout_without_compile_evidence_blocks(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-dev",
                "mode": "light-dev",
                "changed_files": ["src/app.py"],
                "lw_final_record_written": True,
            }
        )

        assert_has(findings, "BLOCK", "code-verification-evidence-missing")


    def test_chinese_complete_claim_without_evidence_blocks(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-docs",
                "claims": ["完成了"],
                "changed_files": ["docs/current-state.md"],
                "utf8_guard_passed": True,
            }
        )

        assert_has(findings, "BLOCK", "positive-claim-evidence-missing")


    def test_warning_positive_claim_blocks(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-dev",
                "mode": "light-dev",
                "changed_files": ["src/app.py"],
                "lw_final_record_written": True,
                "claims": ["complete"],
                "verification": {
                    "compile_build_pass": True,
                    "warnings": 1,
                    "exceptions": 0,
                    "evidence": ["build completed with warning"],
                },
            }
        )

        assert_has(findings, "BLOCK", "positive-claim-with-warning-exception")

    def test_light_dev_requires_final_record_at_completion(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-dev",
                "mode": "light-dev",
                "changed_files": ["src/app.py"],
                "verification": {
                    "compile_build_pass": True,
                    "warnings": 0,
                    "exceptions": 0,
                    "evidence": ["compile pass"],
                },
            }
        )

        assert_has(findings, "BLOCK", "lw-final-missing")


    def test_onboarding_markdown_requires_document_language(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-onboarding",
                "mode": "new-project",
                "project_marker_written": True,
                "current_state_written": True,
                "hook_tools_copied": True,
                "changed_files": ["docs/current-state.md"],
                "utf8_guard_passed": True,
            }
        )

        assert_has(findings, "BLOCK", "document-language-missing")


    def test_docs_markdown_requires_document_language(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-docs",
                "changed_files": ["docs/current-state.md"],
                "utf8_guard_passed": True,
            }
        )

        assert_has(findings, "BLOCK", "document-language-missing")


    def test_docs_markdown_accepts_persisted_document_language(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-docs",
                "changed_files": ["docs/current-state.md"],
                "utf8_guard_passed": True,
                "project_marker_document_language": True,
                "closeout_report_language_applied": True,
            }
        )

        assert_has(findings, "PASS", "l3-closeout-pass")


    def test_docs_markdown_accepts_available_document_language(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-docs",
                "changed_files": ["docs/current-state.md"],
                "utf8_guard_passed": True,
                "document_language_available": True,
                "closeout_report_language_applied": True,
            }
        )

        assert_has(findings, "PASS", "l3-closeout-pass")


    def test_selected_document_language_requires_localized_closeout_report(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-onboarding",
                "mode": "new-project",
                "project_marker_written": True,
                "current_state_written": True,
                "hook_tools_copied": True,
                "changed_files": ["docs/current-state.md"],
                "utf8_guard_passed": True,
                "document_language_selected": True,
                "document_language_persisted": True,
            }
        )

        assert_has(findings, "BLOCK", "closeout-report-language-missing")


    def test_selected_document_language_accepts_localized_closeout_report(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-onboarding",
                "mode": "new-project",
                "project_marker_written": True,
                "current_state_written": True,
                "hook_tools_copied": True,
                "changed_files": ["docs/current-state.md"],
                "utf8_guard_passed": True,
                "document_language_selected": True,
                "document_language_persisted": True,
                "closeout_report_language_applied": True,
            }
        )

        assert_has(findings, "PASS", "l3-closeout-pass")


    def test_light_dev_commit_requires_git_baseline_append(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-git",
                "git_write_performed": True,
                "user_git_confirmed": True,
                "commands_executed": ["git commit -m test"],
                "final_status": "clean except baseline append",
                "commit_created": True,
                "commit_hash": "abc1234",
                "light_dev_commit": True,
            }
        )

        assert_has(findings, "BLOCK", "lw-git-baseline-missing")


    def test_formal_task_commit_requires_feedback_git_baseline_append(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-git",
                "git_write_performed": True,
                "user_git_confirmed": True,
                "commands_executed": ["git commit -m test"],
                "final_status": "clean except baseline append",
                "commit_created": True,
                "commit_hash": "abc1234",
                "formal_task_commit": True,
                "associated_task_package": "docs/work/D26051601-demo",
            }
        )

        assert_has(findings, "BLOCK", "feedback-git-baseline-missing")


    def test_docs_context_change_requires_source_evidence(self):
        findings = check_l3_closeout(
            {
                "active_scene": "uth-docs",
                "changed_files": ["docs/context/backend.md"],
                "utf8_guard_passed": True,
            }
        )

        assert_has(findings, "BLOCK", "context-source-missing")


    def test_uth_git_plan_only_passes(self):
        response = dispatch(
            {
                "type": "l3-closeout",
                "active_scene": "uth-git",
                "plan_only": True,
                "git_plan_present": True,
            }
        )

        self.assertEqual(response["decision"], "PASS")
        assert_has(response["findings"], "PASS", "git-plan-only")


if __name__ == "__main__":
    unittest.main()
