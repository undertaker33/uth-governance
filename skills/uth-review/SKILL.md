---
name: uth-review
description: Use in a UTH-enabled project, identified by .uth-governance/project.json, for code review, validation, acceptance, test execution, delivery check, Todo acceptance, diff review, or readiness assessment, including explicit uth-review requests inside an enabled project. Routes review through minimal context loading, task-boundary evidence, optional uth-context-trace, verification before positive claims, and read-only findings-first output. Stay silent in projects without the UTH marker unless the user explicitly asks to enable UTH first. Do not use for direct bug repair, implementation, architecture design, documentation maintenance, or Git/release closure unless explicitly requested after review.
---

# uth-review

## Purpose

Use this skill for validation, review, and acceptance.

Default posture: read first, judge against the declared task boundary, report findings before summaries, and do not modify code.

This scene answers:

- is the change correct for its stated task
- what blocks acceptance
- what risks remain
- which verification was run or is missing
- whether the work should pass, fail, or continue

## Trigger Conditions

Use `uth-review` when the user asks for:

- code review
- validation or acceptance
- running tests to verify a task
- checking whether a Todo is complete
- comparing implementation against Design/Todo
- reviewing a diff
- assessing delivery readiness
- checking subagent or worker output

Typical wording:

- "review this"
- "帮我审查一下"
- "验收这个 Todo"
- "看看能不能交付"
- "跑一下验证"
- "检查 diff"
- "这个改动有没有问题"

Do not use this skill for:

- unknown bug root-cause investigation; use `uth-debug`
- implementing requested fixes; switch to `uth-dev` or `uth-debug`
- architecture option design; use `uth-design`
- docs cleanup or context sync; use `uth-docs`
- commit, push, PR, tag, release; use `uth-git`

## Entry Protocol

Start with:

- `Scene: uth-review`
- review target: diff / Todo / branch / files / worker output / validation command
- acceptance basis: user request / Todo / Design / explicit checklist
- write policy: read-only unless the user explicitly asks for Feedback/current-state closeout
- code write policy: forbidden in this scene

If the target, acceptance basis, or expected review depth is unclear, use `uth-sp-brainstorming` or ask one concise clarifying question.

## Document Lookup

Do not scan all docs by default.

Read:

1. repository agent entry, usually `AGENTS.md`, if it exists
2. docs structure README, usually `docs/README.md`, if present
3. current-state index, usually `docs/current-state.md`, if referenced by the docs entrypoint or needed for active task pointers
4. current Todo when reviewing a Todo
5. diff or user-specified files

Read on demand:

- current Design
- `docs/architecture.md`
- `docs/development.md`
- related `docs/context/*.md`
- verification instructions from the active task
- `uth-context-trace` output for Design/Todo/Feedback/worker Prompt/Run/LW evidence chains
- archived task package or archived LW record only when the review target explicitly depends on historical evidence

Default to not reading:

- all docs
- old task packages
- `docs/archive/`, unless archive is explicitly in scope
- old Design or Feedback
- old worker prompts
- old Run Logs
- unrelated ADRs or changelogs
- unrelated modules

Use historical and archived evidence only to understand task boundary, worker instruction, or delivery evidence. It does not override `docs/current-state.md`, `docs/context/`, or stable project docs.

## UTH-SP Flow

Use:

- `uth-sp-requesting-code-review` when requesting or performing structured review for completed implementation or pre-merge work
- `uth-sp-receiving-code-review` only when the task is to process review feedback
- `uth-sp-verification-before-completion` before claiming accepted, passing, complete, ready, or safe to merge

If review discovers a bug requiring root-cause work, hand off to `uth-debug`.

If review discovers missing implementation work, hand off to `uth-dev`.

## Hook Gates

Respect the project hook gates when available:

- declare `Scene: uth-review` before acceptance or validation
- remain read-only for code; review writeback may only touch allowed task documents
- use `uth-utf8-guard` before and after modifying governed Markdown (`docs/**/*.md`, Feedback, Run Log, current-state, root `README.md`, or `AGENTS.md`)
- do not perform Git writes

## Code-Change Acceptance Gate

When the review target includes code changes from `uth-dev`, `uth-debug`, or an approved `uth-design` patch, acceptance requires fresh verification evidence.

For code-changing work, positive acceptance requires:

```text
compile/build: pass
warnings: 0
exceptions: 0
```

If this evidence is missing, either:

- run the verification in this review scene, or
- mark the result as `static-review-only`, `pass with risk`, or `needs follow-up`

Do not claim accepted, passing, complete, ready, or mergeable when the compile/build gate is missing or has warnings/exceptions.

If warnings or exceptions are present, ask whether the user accepts a temporary review-risk waiver or route back to `uth-dev` / `uth-debug` to clear them. A waiver can produce `pass with risk`, not `pass`.

For hook events, pass the waiver as `verification.waiver_granted=true` or `review_risk_accepted=true`. Without that field, `pass with risk` for non-zero warnings/exceptions must ask the user first.

## Subagent Policy

Review may use an `evaluator` for independent read-only acceptance, but it is not mandatory.

Rules:

- `evaluator` is read-only and does not modify code or docs.
- Do not write prompt files for `evaluator`.
- Do not use `worker` in this scene.
- If fixes are requested, switch scenes before implementation.

## Write Scope

Default: no file writes.

Source code and test writes are forbidden in `uth-review`, even when a defect is obvious. Route to `uth-debug` or `uth-dev` first.

Allowed only when explicitly requested or when closing a formal Todo:

- Feedback file, if the user asks to write or supplement delivery feedback
- `docs/current-state.md`, only when Todo acceptance, blocker, active task state, or verification baseline changed
- Run Log, only when verification evidence is important and the current task package needs it

Forbidden by default:

- source code
- tests
- Design
- Todo creation or expansion
- worker prompts
- `docs/context/`
- `docs/archive/`
- ADRs
- changelog
- Git writes
- unrelated docs

If review finds module context drift, mark `Needs uth-docs scoped-sync`; do not update `docs/context/`.

## Review Output Rules

For code review, lead with findings ordered by severity.

Use this order:

1. blocking findings
2. non-blocking findings
3. missing verification
4. acceptance recommendation
5. residual risk
6. document writeback, if any

Findings should include file and line references when available.

If no issues are found, say that clearly and still mention verification gaps or residual risk.

Do not bury findings below a long summary.

## Closeout

If `.uth-governance/project.json` contains `document_language`, render the closeout report in that language. For `zh-CN`, use Chinese headings and Chinese prose; preserve literal paths, commands, skill names, schema values, and code identifiers.

End with:

- `Scene: uth-review`
- review target
- acceptance basis
- context read
- findings
- verification run and result, including compile/build pass plus warning/exception count when reviewing code changes
- recommendation: pass / fail / pass with risk / needs follow-up
- documents written or not written
- UTF-8 guard result for governed Markdown writes
- `Needs uth-docs scoped-sync`, if applicable
- next scene: none / `uth-debug` / `uth-dev` / `uth-docs` / `uth-git`

Never claim accepted, passing, complete, or ready without fresh verification evidence, unless the output explicitly says it is a static review only.
