---
name: uth-debug
description: Use in a UTH-enabled project, identified by .uth-governance/project.json, for bugs, failing tests, runtime errors, regressions, unexpected behavior, or defect diagnosis and repair, including explicit uth-debug requests inside an enabled project. Routes debug work through minimal document lookup, optional uth-context-trace evidence loading, systematic debugging, verification, and narrow task-document writeback. Stay silent in projects without the UTH marker unless the user explicitly asks to enable UTH first. Do not use for feature requests, architecture redesign, broad refactors, or pure code review unless a concrete defect must be diagnosed.
---

# uth-debug

## Purpose

Use this skill for Debug / fault repair. Keep the work narrow: identify the symptom, find the root cause, apply the smallest valid fix, verify with fresh evidence, and write back only the task evidence that matters.

Do not turn debug into feature development, architecture redesign, broad refactor, release work, or general documentation maintenance.

## Entry Protocol

At the start, state:

- `Scene: uth-debug`
- whether this is read-only diagnosis or authorized repair
- what is known: symptom, expected behavior, failing command, affected module, recent change, or user-provided evidence

If the issue, expected behavior, permission to modify, or repair scope is ambiguous, use `uth-sp-brainstorming` first. Do not repair while the task could actually be a requirement change.

If the user only asks "why" or "locate the cause", stay read-only until they authorize changes.

## Document Lookup

Do not guess document locations and do not scan all docs by default.

First find the documentation structure entrypoint:

1. Read the repository agent entry, usually `AGENTS.md`, if it exists.
2. Read the docs entry README, usually `docs/README.md` or another README that explains the docs structure.
3. Read the current-state index only after `.uth-governance/project.json` `entrypoints.current_state` confirms where it lives.
4. Follow those entrypoints to the relevant active task package, Design, Todo, Feedback, worker prompts, runs, LW-Work record, ADR, changelog, or context file.

Do not enter `docs/archive/` by default. Use archive only when the user explicitly asks for historical evidence, a task id or LW id is known to be archived, or `uth-context-trace` identifies an archived item as relevant to the bug.

If the structure README is missing or unclear:

- read only the directly relevant code, test, command output, and nearby README files
- report that the documentation entrypoint is missing or unclear
- do not invent a new document structure inside the debug task

Use `uth-context-trace` when available and useful to locate the evidence chain. It should locate documents; this skill still owns the debug workflow.

## Reading Rules

Prefer the smallest useful context set:

- bug report, failing output, stack trace, or reproduction command
- docs structure README and current-state index
- current task package if linked by the index or user
- related Design, Todo, Feedback, worker prompts, and runs only when linked to this issue
- LW-Work and Git commit info when the issue follows a lightweight committed change
- archived task package or archived LW record only when the bug is tied to that historical evidence
- relevant `docs/context/*.md` only when the docs README/current-state points to it or the affected module is clear
- code and tests directly on the failure path

Default to not reading:

- all docs
- old Design, old Feedback, old runs, or old worker prompts
- unrelated task packages
- `docs/archive/`, unless archive is explicitly in scope
- unrelated ADRs or changelogs
- unrelated modules

Historical docs and archived docs are clues, not current facts. They do not override the localized current-state entrypoint, `docs/context/`, or stable project docs.

## UTH-SP Flow

After loading the minimum context, use:

- `uth-sp-systematic-debugging` for diagnosis and root-cause work
- `uth-sp-test-driven-development` when changing behavior or fixing code where a regression test is feasible
- `uth-sp-verification-before-completion` before claiming the issue is fixed, tests pass, or work is complete

Do not invoke full development planning just because debug touches code. Switch to `uth-dev`, `uth-design`, or another scene only when the work has become new functionality, architecture change, broad refactor, or release closure.

## Hook Gates

Respect the project hook gates when available:

- declare `Scene: uth-debug` before diagnosis or repair
- stay read-only until repair scope and permission are clear
- use `uth-utf8-guard` before and after modifying governed Markdown (`docs/**/*.md`, Feedback, Todo status, Run Log, Prompt, current-state, root `README.md`, or `AGENTS.md`)
- ask before writing outside the repair scope
- do not perform Git writes

## Code Verification Gate

After a code repair, run the project build or compile command needed to prove the repaired path compiles.

Strong-governance closeout requires:

```text
compile/build: pass
warnings: 0
exceptions: 0
```

Do not accept an old warning baseline by default. On the first UTH code-changing scene in a project, if the build already has warnings or exceptions, clean them to `0 / 0` before claiming the bug is fixed, unless the user explicitly grants a temporary waiver.

If the user grants a waiver:

- state the waiver and remaining warnings/exceptions in closeout
- do not claim fixed, passing, complete, ready, or deliverable
- recommend another repair pass before Git/release closure
- if warning/exception cleanup is genuinely better handled later, ask the user for the waiver explicitly; otherwise clean them before closeout

## Subagent Use

Subagents are allowed, not mandatory.

Use:

- `planner` for read-only investigation and context tracing
- `worker` for bounded repair when the write scope is clear
- `evaluator` for independent verification or review

Rules:

- Write full prompts only for `worker` subagents, under the current formal task package `prompts/`, before dispatch.
- If multiple workers are dispatched, write one prompt file per worker.
- If the same worker needs rework, append the rework instructions to the same worker Prompt file.
- Do not write prompt files for `planner` or `evaluator`; summarize their read-only findings in closeout, runs, or Feedback when useful.
- Send a worker only a short instruction to read its prompt file.
- Keep `planner` and `evaluator` read-only.
- Let the `worker` modify only the assigned repair scope.
- Apply "who caused the implementation problem fixes it; who raised the acceptance issue verifies it."

For lightweight debug without a formal task package, avoid subagents unless the user explicitly wants them or the issue is complex enough to justify creating a formal package first.

## Write Scope

Allowed when repair is authorized:

- directly related code
- directly related tests
- current task package Feedback
- current task package Todo
- current task package runs
- current task package worker prompts
- localized current-state entrypoint only when current phase, blocker, baseline, or acceptance status changed
- LW-Work final record only when this bug repair has explicitly been routed as lightweight development; Git baseline append belongs to `uth-git` after a successful Git write

Forbidden by default:

- `docs/context/`
- ADRs
- changelogs
- Git commit, tag, push, merge, or release
- unrelated modules
- unrelated task packages
- historical Design, Feedback, runs, or worker prompts
- `docs/archive/`
- opportunistic refactors

If the fix changes module responsibilities, public entrypoints, dependencies, boundaries, verification methods, or long-lived risks, do not update `docs/context/` here. Mark `Needs uth-docs scoped-sync` in the closeout.

## Writeback Rules

Write task evidence only when it exists.

Write Feedback when a formal task debug produced a conclusion, fix, regression note, verification result, or unresolved blocker.

Update Todo only when task status, remaining work, or acceptance state changed.

Write runs when verification commands or reproduction commands were executed and their result matters.

Write prompts only when `worker` subagents were used, including rework prompts. Do not write prompts for `planner` or `evaluator`.

Update current-state only for active phase/blocker/baseline/acceptance changes.

Do not write documents for a pure read-only pass with no stable conclusion. Do not write ADR/changelog/context from this scene.

## Closeout

If `.uth-governance/project.json` contains `document_language`, render the closeout report in that language. For `zh-CN`, use Chinese headings and Chinese prose; preserve literal paths, commands, skill names, schema values, and code identifiers.

End with a compact report:

- `Scene: uth-debug`
- Mode: read-only diagnosis or repair
- Root cause, or what remains unknown
- Files changed, if any
- Verification run and result, including compile/build pass plus warning/exception count for code repairs
- Documents written or deliberately not written
- UTF-8 guard result for governed Markdown writes
- `Needs uth-docs scoped-sync`, if module context may need an update
- human acceptance boundary: read-only diagnosis / independent light repair reached / formal Design reached / formal Todo-only not reached
- Git-closure decision: not suggested / suggested, waiting for user / user handed off to `uth-git`
- Git status: not executed in this scene

Never claim fixed, passing, or complete without fresh verification evidence. If verification was not run, say so plainly.

Always evaluate and report Git closure after debug closeout. For read-only diagnosis, the decision is normally `not suggested`. For independent light repair, evaluate Git closure after the repair is verified. For a repair inside a formal task package, use the Design-level human acceptance boundary, not the individual Todo boundary. Enter `uth-git` only after the user explicitly agrees.
