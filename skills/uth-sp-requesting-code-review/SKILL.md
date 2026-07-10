---
name: uth-sp-requesting-code-review
description: Use inside uth-review when requesting or performing structured review for a completed implementation, worker result, Todo, or pre-merge diff. Do not use as a top-level completion trigger.
---

# Requesting Code Review

## UTH Boundary

This is a UTH-scoped method skill, not a top-level router.

- Use only after `uth-governance` or an owning `uth-*` scene selects it, or when the user explicitly names this skill.
- UTH owns scene routing, document locations, allowed writes, worker Prompt persistence, verification gates, and Git confirmation.
- Do not write project documentation by default. Write only to paths supplied by the owning UTH scene.
- Do not run Git writes, create commits, push, tag, merge, rebase, switch branches, or create/delete worktrees unless the owning scene is `uth-git` and the user has confirmed the Git plan.
- If this skill conflicts with an owning UTH scene, follow the UTH scene.


Dispatch or run a structured reviewer under `uth-review` to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation, not your whole session history.

**Core principle:** Review early, review often.

## When to Request Review

**Use when `uth-review` selects it for:**
- a completed Todo or worker result
- a major feature before acceptance
- a pre-merge diff

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get review range or file scope:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

If Git history is not the right evidence source, use the files, Todo, Feedback, or diff scope supplied by `uth-review`.

**2. Dispatch reviewer or perform structured review:**

Dispatch a `general-purpose` reviewer with the template at
[code-reviewer.md](code-reviewer.md), or perform the same structured review
inline when `uth-review` does not authorize delegation.

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{REVIEW_SCOPE}` - Git range, working-tree diff, explicit files, Todo, or Feedback evidence supplied by `uth-review`
- `{DESCRIPTION}` - Brief summary

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)
- If feedback is for a worker result, route valid fixes back to the worker that produced the reviewed output.
- After that worker fixes, ask the same reviewer who raised each issue to recheck it.

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

[Use review range or file scope supplied by uth-review]

[Dispatch reviewer / run structured review]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from the active UTH Todo
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task
- Preserve accountability: origin worker fixes, origin reviewer rechecks

**Executing Plans:**
- Review after each batch (3 tasks)
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Send a review issue to a different worker than the one who produced the faulty output
- Ask a different reviewer to approve a finding raised by the original reviewer
- Argue with valid technical feedback

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See template at: `code-reviewer.md`
