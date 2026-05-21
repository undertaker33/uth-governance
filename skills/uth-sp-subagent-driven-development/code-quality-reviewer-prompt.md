# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable)

**Only dispatch after spec compliance review passes.**

```
Task tool (general-purpose):
  Use template at ../uth-sp-requesting-code-review/code-reviewer.md

  DESCRIPTION: [task summary, from implementer's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  REVIEW_SCOPE: [changed files, diff range, or workspace scope supplied by uth-dev]
  ACCOUNTABILITY: You are the evaluator for every quality finding you raise.
  Report your evaluator id / stable handle if available. If you find issues,
  the controller must send them back to the worker that produced the output,
  then ask you to recheck the same findings after that worker fixes them.
```

**In addition to standard code quality concerns, the reviewer should check:**
- Does each file have one clear responsibility with a well-defined interface?
- Are units decomposed so they can be understood and tested independently?
- Is the implementation following the file structure from the plan?
- Did this implementation create new files that are already large, or significantly grow existing files? (Don't flag pre-existing file sizes — focus on what this change contributed.)

**Code reviewer returns:** evaluator id / stable handle if available, Strengths, Issues (Critical/Important/Minor), Assessment
