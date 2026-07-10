---
name: uth-sp-executing-plans
description: Use when an owning UTH scene or the user chooses inline execution of an accepted implementation plan with review checkpoints. Do not use to bypass UTH Todo, document, verification, or Git gates.
---

# Executing Plans

## UTH Boundary

This is a UTH-scoped method skill, not a top-level router.

- Use only after `uth-governance` or an owning `uth-*` scene selects it, or when the user explicitly names this skill.
- UTH owns scene routing, document locations, allowed writes, worker Prompt persistence, verification gates, and Git confirmation.
- Do not write project documentation by default. Write only to paths supplied by the owning UTH scene.
- Do not run Git writes, create commits, push, tag, merge, rebase, switch branches, or create/delete worktrees unless the owning scene is `uth-git` and the user has confirmed the Git plan.
- If this skill conflicts with an owning UTH scene, follow the UTH scene.


## Overview

Load an accepted UTH plan, review critically, execute tasks inline, and return evidence to the owning UTH scene.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** If subagents are available and the owning UTH scene selected worker mode, use `uth-sp-subagent-driven-development` instead of this skill.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create tracked todos for the plan items and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Return to UTH Closeout

After all tasks complete and verified:
- Return changed files, verification evidence, risks, and blockers to the owning UTH scene.
- Do not invoke Git, branch, PR, tag, release, or cleanup flows from this skill.

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Workflow skills, only when selected by the owning UTH scene:**
- **uth-sp-using-git-worktrees** - Set up isolated workspace only when approved
- **uth-sp-writing-plans** - Creates the plan this skill executes
