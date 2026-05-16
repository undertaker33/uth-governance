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
| `/uth-onboarding` | Enable UTH in a new or existing project. |
| `/uth-governance` | Ask the agent to classify an unclear engineering request. |
| `/uth-design` | Evaluate architecture, compare options, or write an accepted Design. |
| `/uth-dev` | Implement a clear bounded change or formal Todo. |
| `/uth-debug` | Diagnose and repair a bug, failing test, build error, or regression. |
| `/uth-review` | Review, validate, accept, or run readiness checks. |
| `/uth-docs` | Sync current-state, context, archive, snapshots, or governance docs. |
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
| `/uth-sp-subagent-driven-development` | Formal development should use worker subagents. |
| `/uth-sp-dispatching-parallel-agents` | Independent domains can be delegated in parallel. |
| `/uth-sp-verification-before-completion` | A scene is about to claim complete, fixed, passing, ready, or releasable. |
| `/uth-sp-requesting-code-review` | Completed work needs structured code review. |
| `/uth-sp-receiving-code-review` | External review feedback needs triage before fixes. |
| `/uth-sp-using-git-worktrees` | Work needs isolated workspaces or worktrees. |
| `/uth-sp-finishing-a-development-branch` | Branch, PR, merge, cleanup, tag, or release closure needs structured options. |
| `/uth-sp-writing-skills` | UTH or method skills themselves are being created, updated, or verified. |

## Lightweight vs Formal Work

Lightweight development writes one `docs/LW-Work/LW*.md` final record when the
task is completed. It does not create a separate LW Todo, and it does not wait
for Git baseline details before the report exists.

Formal work uses Design/Todo/Feedback documents under `docs/work/D*/`. The
Feedback record is written when the work is accepted, before any Git closure.

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
- Other `uth-*` scenes stay silent unless the project has
  `.uth-governance/project.json`, except when the user explicitly asks to enable
  UTH governance for that project.

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

Supported runtimes are `codex`, `claude`, `opencode`, and `custom`.
Use `--runtime custom --skills-dir <path>` when the target agent loads skills
from a non-standard directory.

Useful installer options:

- `--source <path>`: install from an explicit UTH package root.
- `--skills-dir <path>`: override the detected skill install directory.
- `--skip-skills`: run without installing skills.
- `--force`: overwrite existing UTH skill directories.
- `--dry-run`: print planned changes without writing files.

## Maintain This Pack

Run the verification bundle before publishing governance-pack changes:

```bash
python scripts/verify.py
```

Versioning belongs to the outer package folder or release artifact. Internal
handbook/template filenames intentionally do not carry version suffixes.
