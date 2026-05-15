---
name: uth-git
description: Use in a UTH-enabled project, identified by .uth-governance/project.json, or when the user explicitly invokes uth-git, for Git, branch, commit, push, PR, merge, rebase, tag, release, changelog, worktree cleanup, or development-branch closure. Requires reading the project git workflow, inspecting current Git state, presenting a write plan, and waiting for explicit user confirmation before any Git write. Handles lightweight commit LW-Work records after successful commits. Stay silent in projects without the UTH marker unless the user explicitly asks to enable UTH first. Do not use for implementation, debug, design, review, or docs maintenance unless the user is explicitly asking for Git/release closure.
---

# uth-git

## Purpose

Use this skill for Git / PR / tag / release closure.

This scene owns:

- Git state inspection
- Git write planning
- commit / push / PR / merge / rebase / tag / release closure
- branch or worktree cleanup
- changelog decision for releases
- LW-Work record after successful lightweight commits
- Git evidence linkage for formal task packages when a commit / PR / tag is created

It does not implement code, fix bugs, review code, or redesign work.

## Trigger Conditions

Use `uth-git` when the user asks for:

- commit
- push
- branch creation, switch, rename, or deletion
- PR creation, update, merge, or closure
- tag
- release
- merge or rebase
- worktree creation or deletion
- finishing a development branch
- changelog or release note closure tied to a tag/release

Typical wording:

- "提交一下"
- "commit"
- "push"
- "开 PR"
- "合并到 main/master"
- "打 tag"
- "发版"
- "删 worktree / 分支"
- "收口这个分支"

Do not use this skill for ordinary implementation, debug, review, or docs work before the user asks for Git/release closure.

## Entry Protocol

Start with:

- `Scene: uth-git`
- requested Git operation
- whether this is read-only planning or confirmed execution
- whether code/doc work appears already complete
- whether this Git closure follows `uth-dev`, `uth-debug`, `uth-review`, `uth-docs`, or a lightweight LW Todo
- the human acceptance boundary that triggered the handoff: light task, Design-level acceptance, explicit user Git request, docs/design stable artifact, release, or branch closure

If the requested Git operation is ambiguous, ask before executing.

Git write operations require explicit user confirmation after the plan is shown.

Do not treat Todo completion as the default formal-task Git boundary. For formal task packages, Git closure should normally follow Design-level human acceptance or an explicit user Git request. Todo completion is Agent self-evidence and may be recorded in Feedback without entering this scene.

If this scene only produces a Git plan and performs no Git writes, closeout may use `git_plan_present=true` or `plan_only=true` and must state that no Git writes were executed. User Git confirmation is required only for actual Git writes.

## Mandatory Reads

Read the project Git workflow before any Git write:

```text
docs/_governance/git-workflow.md
```

If missing, read the docs entry README and `AGENTS.md` for Git rules, then report that the Git workflow file is missing.

Also inspect:

- current branch
- `git status`
- diff summary
- staged vs unstaged changes
- docs entry README and `docs/current-state.md` only when needed to locate active LW/task/changelog pointers
- relevant remote and upstream state when push/PR/release is requested
- changelog/tag state when release or tag is requested
- lock files if the project defines Git Owner or Workspace Owner locks

Do not read `docs/archive/` by default. Archived task packages and archived LW records are not active Git closure targets unless the user explicitly asks to inspect historical closure evidence.

## Git Write Definition

Treat these as Git writes requiring confirmation:

- `git add`
- `git commit`
- `git tag`
- `git merge`
- `git rebase`
- `git push`
- `git switch`
- `git checkout`
- creating, renaming, or deleting branches
- creating or deleting worktrees
- commands that modify `.git`, index, branch pointers, or workspace ownership

Read-only Git commands such as `git status`, `git diff`, `git log`, `git show`, and `git branch --show-current` may run before confirmation.

## Required Plan Before Confirmation

Before any Git write, show:

- current branch
- `git status` summary
- diff summary
- planned Git commands
- proposed commit message, if committing
- PR need: yes / no
- changelog need: yes / no
- tag need: yes / no
- lightweight change: yes / no
- if lightweight: whether LW-Work should be written after commit
- lock state or missing lock information
- risks and rollback notes

Then wait for explicit user confirmation.

Do not treat vague approval as permission for extra Git writes outside the shown plan.

## UTH-SP Flow

Use:

- `uth-sp-finishing-a-development-branch` for PR, merge, release, tag, or branch closure decisions
- `uth-sp-verification-before-completion` before claiming Git operation, release, tag, PR, or branch closure is complete

If verification is missing for the underlying work, report that before asking to commit or release. Do not invent verification.

## Pre-Git Verification Gate

Before committing, tagging, releasing, or asking the user to approve those writes, inspect whether the diff includes code changes.

If code changes are present and the work came from `uth-dev`, `uth-debug`, or an approved `uth-design` patch, require fresh evidence:

```text
compile/build: pass
warnings: 0
exceptions: 0
```

If the evidence is missing or not clean:

- report the missing gate before the Git plan
- do not present the work as complete, passing, ready, or releasable
- block release/tag by default
- proceed with commit only if the user explicitly confirms the risk after seeing the missing gate and the scene closeout allowed a waiver

## LW-Work Rule

For lightweight changes:

1. `uth-dev` creates the lightweight Todo before implementation.
2. Do not write the final LW record before commit.
3. Ask whether the user authorizes commit.
4. After commit succeeds, append or create:

```text
docs/LW-Work/LWYYMMDDXX-轻量任务标题.md
```

5. Record the original request, LW Todo path, commit hash, commit message, changed files summary, verification evidence summary, push/PR status, and timestamp.
6. If the LW record itself should be included in Git, show a new diff and request a second confirmation.

LW-Work is not used for formal task-package Todo work.

Do not create or update LW records under `docs/archive/LW-Work/`. If a matching LW Todo has already been archived, treat it as historical and ask whether to create a new active LW record or route to `uth-docs`.

## Formal Task Git Linkage

Formal Feedback does not have to wait for Git information.

When a Git write succeeds for a formal task package:

- record commit / PR / tag evidence in the `uth-git` closeout
- mention associated task package, Design, and Todo when known
- do not reopen or rewrite Feedback only to add Git information unless the user explicitly asks

## Changelog and Tag Rules

For releases:

- formal tag requires a changelog
- changelog must correspond to the formal tag
- do not create formal tag on a non-main release branch unless project rules explicitly allow it
- changelog is user-facing, not a commit log

If changelog is missing, stop and ask whether to create or update it before tagging.

Use `uth-utf8-guard` before and after writing LW-Work records, changelog Markdown, or other governed Markdown during Git closure.

## Forbidden

Do not:

- execute Git writes before confirmation
- commit unrelated changes without showing them
- tag without release/changelog checks
- delete branches or worktrees without explicit confirmation
- change code to make Git closure easier
- update `docs/archive/`; archive cleanup belongs to `uth-docs`
- hide untracked or unstaged files
- rewrite history unless explicitly requested and confirmed
- claim pushed/tagged/merged unless verified from fresh command output

## Closeout

End with:

- `Scene: uth-git`
- operation requested
- commands executed
- final branch
- final status summary
- commit hash / PR / tag / release, if created
- associated formal task package / Todo, if known
- changelog status
- LW-Work status
- UTF-8 guard result for governed Markdown writes
- verification evidence
- remaining manual steps or risks

If only a plan was produced, state that no Git writes were executed.
