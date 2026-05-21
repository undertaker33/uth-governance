[English](README.md) | [中文](README.zh-CN.md)

# UTH Governance

UTH Governance is a lightweight engineering-governance pack for coding agents.
It focuses on when to read documents, when to write documents, what context to
load, and how to close engineering work without turning every task into a
heavyweight process.

## Why use UTH

- Keeps agent work traceable without making every task heavyweight.
- Separates scene commands, method skills, hook gates, docs, and Git closure.
- Supports lightweight development and formal Design/Todo/Feedback work.

## How it works

UTH has three layers:

1. Global skills installed once.
2. Project-local activation through `/uth-onboarding`.
3. Scene commands that select the right governance path.

## Quickstart

### Step 1: Install UTH

Use an agent:

```text
Install UTH Governance from GitHub:
https://github.com/undertaker33/uth-governance.git

Follow docs/guide/installation.md from that repository.
Use runtime codex.
Do not initialize the current project during installation.
```

Or install manually:

```bash
git clone https://github.com/undertaker33/uth-governance.git
cd uth-governance
python scripts/install.py --runtime codex
```

To update an existing install, see [One-Sentence Update](#one-sentence-update).

### Step 2: Enable UTH in a project

Open the target project and explicitly run:

```text
/uth-onboarding
```

### Step 3: Use a scene command

Use the scene command that matches the work:

```text
/uth-dev
/uth-debug
/uth-review
/uth-git
```

## Scene Commands

| Command | Use when |
| --- | --- |
| `/uth-onboarding` | Enable UTH in a new project, enable-only in an existing project, or orchestrate full existing-project takeover when explicitly requested. |
| `/uth-governance` | Ask the agent to classify an unclear engineering request. |
| `/uth-design` | Evaluate architecture, compare options, or write an accepted Design. |
| `/uth-dev` | Implement a clear bounded change or formal Todo. |
| `/uth-debug` | Diagnose and repair a bug, failing test, build error, or regression. |
| `/uth-review` | Review, validate, accept, or run readiness checks. |
| `/uth-docs` | Govern project documentation from code facts: full-project baseline, scoped sync, module split, onboarding follow-up, current-state, context, archive, snapshots, and migrations. |
| `/uth-git` | Commit, push, open/merge PRs, tag, release, or close a branch. |
| `/uth-context-trace` | Locate Design/Todo/Feedback/Prompt/Run/LW/ADR evidence. |
| `/uth-utf8-guard` | Check governed Markdown for UTF-8, mojibake, and fence balance. |

## UTH-SP Method Skills

`uth-sp-*` means UTH Superpower. These skills are the Superpower method layer
used by UTH scenes. They are normally selected by the active scene, but you can
still name them explicitly when you want that method:

| Command | Use when |
| --- | --- |
| `/uth-sp-brainstorming` | Requirements, scope, options, or acceptance are unclear. |
| `/uth-sp-writing-plans` | An accepted Design needs an implementation plan. |
| `/uth-sp-executing-plans` | An accepted plan should be executed inline. |
| `/uth-sp-test-driven-development` | Behavior, API, permission, state, or regression work needs a test-first path. |
| `/uth-sp-systematic-debugging` | Debugging needs root-cause discipline before repair. |
| `/uth-sp-subagent-driven-development` | Formal development should use worker subagents with origin-worker fixes and origin-evaluator rechecks. |
| `/uth-sp-dispatching-parallel-agents` | Independent domains can be delegated in parallel. |
| `/uth-sp-verification-before-completion` | A scene is about to claim complete, fixed, passing, ready, or releasable. |
| `/uth-sp-requesting-code-review` | Completed work needs structured code review. |
| `/uth-sp-receiving-code-review` | External review feedback needs triage before fixes. |
| `/uth-sp-using-git-worktrees` | Work needs isolated workspaces or worktrees. |
| `/uth-sp-finishing-a-development-branch` | Branch, PR, merge, cleanup, tag, or release closure needs structured options. |
| `/uth-sp-writing-skills` | UTH or method skills themselves are being created, updated, or verified. |

When `uth-design` is designing a Web page, Web app screen, browser UI, or frontend page layout, it must invoke `ui-ux-pro-max`. Android UI/UX design does not trigger `ui-ux-pro-max` by default.

## Lightweight vs Formal Work

Lightweight development writes one `docs/LW-Work/LW*.md` final record when the
task is completed. It does not create a separate LW Todo, and it does not wait
for Git baseline details before the report exists.

`light-dev` is gated by model-specific hard boundaries, not by agent judgment.
The first supported batch is `claude-opus-4.6`, `claude-opus-4.7`, `gpt-5.4`,
`gpt-5.5`, `gpt-5.3-codex-spark`, `deepseek-v4-pro`, `deepseek-v4-flash`,
`mimo-v2.5-pro`, and `kimi-k2.6`. L1 Process Gate requires `llm_model` plus
`task_shape.changed_files_count`, `modules_count`, and
`implementation_steps_count`; API/contract, database, security, architecture,
dependency/build, cross-module data-flow, integration/protocol, concurrency,
state-machine, data-loss, worker, and parallel-agent triggers always route to
formal work.

Formal work uses Design/Todo/Feedback documents under `docs/work/D*/`. The
Feedback record is written when the work is accepted, before any Git closure.
Once work is routed to formal development, implementation cannot start until an
active task package, accepted Design, and current Todo all exist. Design to dev
handoff must pause for explicit user confirmation.

Before any governed Markdown is persisted, the owning scene must complete a
brainstorming preflight and confirm that no open user questions remain.

Git baseline details belong to `uth-git`. After a successful Git write,
`uth-git` appends the baseline to the lightweight final record or to the formal
Feedback record. Normal development and review flows should not block report
generation while waiting for Git.

## Project Activation Behavior

- The installer only installs global skills.
- The installer does not edit the current project, create project docs, install
  hook tools globally, or create `.uth-governance/project.json`.
- `/uth-onboarding` creates the project marker, copies project-local
  `tools/uth-hooks/`, and creates the minimal governance docs scaffold.
- Before the first governed Markdown write or scene closeout report, UTH asks
  for the project documentation language and saves it in
  `.uth-governance/project.json` as `document_language`.
- Hard entry filenames stay stable as `AGENTS.md` and every directory-entry `README.md`; generated
  governance Markdown filenames follow the selected `document_language` and are
  recorded in `.uth-governance/project.json` `entrypoints`.
- Other `uth-*` scenes stay silent unless the project has
  `.uth-governance/project.json`, except when the user explicitly asks to enable
  UTH governance for that project.

## Existing Project Takeover And Docs Baselines

When the user asks UTH to take over an existing project, `/uth-onboarding` is the orchestrator. It performs preflight safety work, routes to `/uth-docs onboarding-followup` as a separate docs scene, stops preflight, then resumes for final takeover closeout only after docs-scene completion evidence returns.

`/uth-docs` is the code-fact documentation governance window. It may report `scoped-docs-complete` for a specified diff, range, version, module, or file scope only when a trusted full-project baseline already exists. Only `full-project-docs-complete` supports the claim that project documentation governance is complete.

For large projects, `/uth-docs` asks whether module split is allowed before entering `module-split`. After approval it writes a numbered module split plan such as `docs/context/00-module-split.md` or `docs/context/00-模块拆分.md` and the context module index, pauses for user confirmation, then governs modules in that order with numbered module context files (`01-...md`, ..., `09-...md`, `10-...md`) without pausing between modules. If the context becomes too long, it writes a lightweight final record and gives the user a new-window prompt so the next window can resume from that record.

## Package Contents

- `skills/`: UTH scene skills and UTH-SP method skills.
- `tools/uth-hooks/`: reference L0/L1/L2/L3 hook runner, copied into a target project by `uth-onboarding`.
- `docs/guide/installation.md`: install guide for humans and agents.
- `docs/AGENT_工程治理启动手册.md`: governance handbook.
- `docs/TEMPLATES_工程治理模板.md`: document templates.
- `docs/HOOKS_工程治理门禁手册.md`: hook gate manual.
- `docs/FLOW_全链路流程图.md`: scene and hook flow diagrams.
- `scripts/install.py`: global skill installer.
- `scripts/verify.py`: verification bundle for this governance pack.

## Installation Details

For agent-driven installation, ask the agent to clone the repository, read
`docs/guide/installation.md`, and run the installer for the target runtime.
If the repository is private, make sure the agent's Git environment can access
GitHub first. An equivalent SSH clone URL is fine when SSH is configured.

For manual installation:

```bash
python scripts/install.py --runtime codex
```

### One-Sentence Update

When UTH is already installed and you want to refresh the global skills, give
your agent this prompt:

```text
Update UTH Governance from GitHub:
https://github.com/undertaker33/uth-governance.git

Follow docs/guide/installation.md from that repository.
Use runtime codex.
Overwrite existing UTH skills with --update.
Do not initialize the current project during update.
```

Or update manually from a fresh clone or an updated local clone:

```bash
python scripts/install.py --runtime codex --update
```

`--update` is an alias for `--force`. It overwrites existing UTH skill
directories in the selected global skills directory only. It still does not run
`uth-onboarding`, create project docs, copy hook tools into the current project,
or create `.uth-governance/project.json`.

When installing for a different agent tool, keep the same install or update
flow and change the `--runtime` value:

- Codex: `--runtime codex`
- Claude Code: `--runtime claude`
- OpenCode: `--runtime opencode`
- Custom or non-standard skill directory: `--runtime custom --skills-dir <path>`

Useful installer options:

- `--source <path>`: install from an explicit UTH package root.
- `--skills-dir <path>`: override the detected skill install directory.
- `--skip-skills`: run without installing skills.
- `--update`: update existing UTH skill directories; alias for `--force`.
- `--force`: overwrite existing UTH skill directories.
- `--dry-run`: print planned changes without writing files.

## Maintain This Pack

Run the verification bundle before publishing governance-pack changes:

```bash
python scripts/verify.py
```

Versioning belongs to the outer package folder or release artifact. Internal
handbook/template filenames intentionally do not carry version suffixes.

## License

UTH Governance is licensed under the Apache License, Version 2.0. See
[`LICENSE`](LICENSE).

Some `uth-sp-*` method-skill materials include or adapt content from
[Superpowers](https://github.com/obra/superpowers), which is licensed under the
MIT License. Keep the upstream copyright and license notices when
redistributing those materials.

## Acknowledgements

The UTH-SP method-skill layer is inspired by and partially adapted from
[Superpowers](https://github.com/obra/superpowers), an agentic skills framework
created by Jesse Vincent and the Superpowers contributors.

Superpowers is licensed under the MIT License. When redistributing UTH-SP
materials that include or adapt Superpowers content, keep the upstream
copyright and license notices.

Thanks to the Superpowers project for the method patterns behind structured
brainstorming, systematic debugging, test-driven development, planning,
subagent development, and verification-before-completion workflows.
