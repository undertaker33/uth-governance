---
name: uth-sp-finishing-a-development-branch
description: Use inside uth-git when implementation is already verified and the user wants branch, PR, merge, cleanup, tag, or release closure options. Do not execute Git writes outside uth-git confirmation.
---

# Finishing a Development Branch

## UTH Boundary

This is a UTH-scoped method skill, not a top-level router.

- Use only after `uth-governance` or an owning `uth-*` scene selects it, or when the user explicitly names this skill.
- UTH owns scene routing, document locations, allowed writes, worker Prompt persistence, verification gates, and Git confirmation.
- Do not write project documentation by default. Write only to paths supplied by the owning UTH scene.
- Do not run Git writes, create commits, push, tag, merge, rebase, switch branches, or create/delete worktrees unless the owning scene is `uth-git` and the user has confirmed the Git plan.
- If this skill conflicts with an owning UTH scene, follow the UTH scene.


## Overview

Guide `uth-git` branch closure by presenting clear options and the Git plan for the chosen workflow.

**Core principle:** Verify evidence → Present options → Hand a confirmed plan to `uth-git`.

**Announce at start:** "I'm using uth-sp-finishing-a-development-branch to prepare branch closure options for uth-git."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 4: Prepare Chosen Git Plan

Do not execute the commands below unless the owning scene is `uth-git`, the full plan has been shown, and the user has explicitly confirmed it.

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

Then: include cleanup in the `uth-git` plan if appropriate.

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create the PR with the forge tooling selected by uth-git.
# Include a concise summary and the verified test plan.
```

Then: include cleanup in the `uth-git` plan if appropriate.

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed by `uth-git`:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: include cleanup in the `uth-git` plan if appropriate.

### Step 5: Cleanup Worktree Plan

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

Only treat project-local `.worktrees/` or `worktrees/` paths as UTH-owned. Preserve externally managed worktrees unless the user explicitly includes them in the confirmed cleanup plan.

If user confirms cleanup through `uth-git`:
```bash
cd <main-repository-root>
git worktree remove <worktree-path>
git worktree prune
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 4 structured options

**Automatic worktree cleanup**
- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1 and 4

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**
- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Integration

**Called by:**
- **uth-git** when branch, PR, merge, tag, release, or cleanup closure is requested

**Pairs with:**
- **uth-sp-using-git-worktrees** - Plans cleanup for worktrees created under UTH control
