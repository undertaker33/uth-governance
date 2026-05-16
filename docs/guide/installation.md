# UTH Governance Installation

This guide is written for humans and LLM agents.

Installation is global. It installs UTH skills only. It does not install hook
tools globally, does not initialize the current project, does not create project
docs, and does not create `.uth-governance/project.json`.

Project onboarding is a separate explicit action handled by `uth-onboarding`.

## For Humans

Give your agent this prompt:

```text
Install UTH Governance from GitHub:
https://github.com/undertaker33/uth-governance.git

Follow docs/guide/installation.md from that repository.
Use runtime codex.
Do not initialize the current project during installation.
```

If the GitHub repository is private, authenticate Git first. The agent may use
the equivalent SSH URL when SSH is already configured:

```text
git@github.com:undertaker33/uth-governance.git
```

If you are installing by hand:

```bash
git clone https://github.com/undertaker33/uth-governance.git
cd uth-governance
python scripts/install.py --runtime codex
```

To update an existing install, give your agent this prompt:

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

When installing for a different agent tool, keep the same install or update
flow and change the `--runtime` value:

- Codex: `--runtime codex`
- Claude Code: `--runtime claude`
- OpenCode: `--runtime opencode`
- Custom or non-standard skill directory: `--runtime custom --skills-dir /path/to/skills`

Optional:

- `--skip-skills`
- `--update`
- `--force`
- `--dry-run`

## For LLM Agents

Follow these steps in order.

1. Confirm the source repository root.
   - If the source repository is not already local, clone it from GitHub first.
   - Canonical URL: `https://github.com/undertaker33/uth-governance.git`.
   - SSH URL is acceptable when the user has configured Git for SSH.
   - Clone into a temporary directory, for example `%TEMP%/uth-governance-install-*`
     on Windows or `/tmp/uth-governance-install-*` on Unix-like systems.
   - It must contain `AGENTS.md`, `skills/`, `scripts/install.py`, and the reference hook assets under `tools/uth-hooks/`.
   - Do not treat this governance-pack repository as a target project.

2. Determine the skill runtime.
   - For Codex: use `$CODEX_HOME/skills` when set, otherwise `~/.codex/skills`.
   - For Claude Code: use `~/.claude/skills`.
   - For OpenCode: use `$OPENCODE_CONFIG_DIR/skills` when set, otherwise `~/.config/opencode/skills`.
   - If unsure, ask the user or pass `--runtime custom --skills-dir <path>`.

3. Run a dry run first.

   ```bash
   python scripts/install.py --runtime codex --dry-run
   ```

   For an update request, use the update flag in the dry run:

   ```bash
   python scripts/install.py --runtime codex --update --dry-run
   ```

4. Run the install or update.

   ```bash
   python scripts/install.py --runtime codex
   ```

   For an update request:

   ```bash
   python scripts/install.py --runtime codex --update
   ```

   Use `--force` or `--update` only when the user explicitly wants to overwrite
   existing UTH skills. A user request to update, refresh, or upgrade an
   existing UTH install counts as overwrite approval for UTH skill directories
   only.

5. Verify the install.

   Confirm the `uth-onboarding` skill exists in the selected skills directory.
   Hook tools are verified after project onboarding because they are project-local.

6. Report the result.
   - List the skill directory used.
   - State that hook tools were not installed globally.
   - State that no project docs were created.
   - State that `.uth-governance/project.json` was not created.
   - If a temporary source clone was created, remove it after successful verification unless the user asked to keep it.
   - State that no Git push was performed unless the user explicitly requested it.

## What the Installer Does

- Copies `skills/uth-*` and `skills/uth-sp-*` into the selected skills directory.
- With `--force` or `--update`, overwrites existing UTH skill directories in
  that selected skills directory.

Default directories:

```text
Codex skills: ~/.codex/skills
Claude skills: ~/.claude/skills
OpenCode skills: ~/.config/opencode/skills
```

## What the Installer Does Not Do

- It does not initialize the current project.
- It does not install hook tools globally.
- It does not create project docs.
- It does not modify root `AGENTS.md`.
- It does not create `.uth-governance/project.json`.
- It does not create a global `.uth-governance/` directory. `.uth-governance/` is project-local only.
- It does not ask whether the current directory is a project directory.
- It does not push Git commits.
- It does not copy old task packages, archived work, or current-state facts from
  this governance-pack repository into any target project.

## Project Onboarding After Install

To enable UTH in a project, open that target project and explicitly run:

```text
/uth-onboarding
```

or tell the agent:

```text
Use uth-onboarding to enable UTH governance for this project.
```

`uth-onboarding` creates `.uth-governance/project.json`, copies project-local
`tools/uth-hooks/`, creates or updates the minimal docs scaffold, and for
existing projects creates the docs backup and handoff snapshot before handing
deeper cleanup to `uth-docs`.
