# UTH Governance Installation

This guide is written for both humans and LLM agents. The preferred path is:
read this guide, run the installer, verify the result, and report exactly what
changed. Do not invent project facts while installing the governance pack.

## For Humans

Give your agent this prompt:

```text
Install and configure UTH Governance from GitHub:
https://github.com/undertaker33/uth-governance.git

Target project is the current working directory.
Follow docs/guide/installation.md from that repository.
Use runtime codex.
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
python scripts/install.py --target /path/to/project --runtime codex
```

If UTH skills and hooks are already installed and you only want to initialize
the target project's documentation system:

```bash
python scripts/install.py --target /path/to/project --runtime codex --project-init-only
```

Use one of:

- `--runtime codex`
- `--runtime claude`
- `--runtime opencode`
- `--runtime custom --skills-dir /path/to/skills`

## For LLM Agents

Follow these steps in order.

1. Confirm the source repository root.
   - If the source repository is not already local, clone it from GitHub first.
   - Canonical URL: `https://github.com/undertaker33/uth-governance.git`.
   - SSH URL is acceptable when the user has configured Git for SSH.
   - Clone into a temporary directory outside the target project, for example
     `%TEMP%/uth-governance-install-*` on Windows or `/tmp/uth-governance-install-*`
     on Unix-like systems.
   - It must contain `AGENTS.md`, `skills/`, `tools/uth-hooks/`, and `scripts/install.py`.
   - Do not treat this governance-pack repository as the target project.

2. Confirm the target project root.
   - If the user did not provide one, ask once.
   - Do not install into the governance-pack repository unless the user explicitly asks.

3. Determine the skill runtime.
   - For Codex: use `$CODEX_HOME/skills` when set, otherwise `~/.codex/skills`.
   - For Claude Code: use `~/.claude/skills`.
   - For OpenCode: use `$OPENCODE_CONFIG_DIR/skills` when set, otherwise `~/.config/opencode/skills`.
   - If unsure, ask the user or pass `--runtime custom --skills-dir <path>`.

4. Run a dry run first.

   ```bash
   python scripts/install.py --target <target-project> --runtime codex --dry-run
   ```

5. Run the install.

   ```bash
   python scripts/install.py --target <target-project> --runtime codex
   ```

   Use `--force` only when the user explicitly wants to overwrite existing UTH
   skills or hook tools.
   Use `--force-docs` only when the user explicitly wants to replace the UTH
   scaffold docs or the marked UTH block in `AGENTS.md`.

   If the user says UTH is already installed and only wants project docs:

   ```bash
   python scripts/install.py --target <target-project> --runtime codex --project-init-only
   ```

6. Verify the install.

   PowerShell:

   ```powershell
   '{"type":"l1","active_scene":"uth-docs"}' | python <target-project>/tools/uth-hooks/uth-hook.py --event -
   ```

   Bash:

   ```bash
   printf '%s' '{"type":"l1","active_scene":"uth-docs"}' | python <target-project>/tools/uth-hooks/uth-hook.py --event -
   ```

7. Report the result.
   - List the skill directory used.
   - List whether `tools/uth-hooks/` was installed or skipped.
   - List the project docs created or already present.
   - If a temporary source clone was created, remove it after successful
     verification unless the user asked to keep it.
   - State that no Git push was performed unless the user explicitly requested it.

## What the Installer Does

- Copies `skills/uth-*` and `skills/uth-sp-*` into the selected skills directory.
- Copies `tools/uth-hooks/` into the target project.
- Creates a lightweight documentation skeleton:
  - `docs/README.md`
  - `docs/_governance/README.md`
  - `docs/_governance/agent-rules.md`
  - `docs/_governance/git-workflow.md`
  - `docs/_governance/subagent-workflow.md`
  - `docs/_governance/writing-rules.md`
  - `docs/_governance/hook-gates.md`
  - `docs/_governance/state-rules.md`
  - `docs/_governance/adr-release-rules.md`
  - `docs/current-state.md`
  - `docs/project-overview.md`
  - `docs/architecture.md`
  - `docs/development.md`
  - `docs/work/README.md`
  - `docs/work/LW-Work/`
  - `docs/work/LW-Work/README.md`
  - `docs/context/README.md`
  - `docs/archive/README.md`
  - `docs/archive/work/`
  - `docs/archive/LW-Work/`
  - `docs/decisions/README.md`
  - `docs/changelogs/README.md`
  - `docs/state/snapshots/`
- Appends a small UTH block to the target project root `AGENTS.md` if the block
  is not already present.

## What the Installer Does Not Do

- It does not push Git commits.
- It does not copy old task packages, archived work, or current-state facts from
  this governance-pack repository into the target project.
- It does not duplicate scene-flow details into the target project `AGENTS.md`.
- It does not modify existing project docs except for appending the marked UTH
  block to root `AGENTS.md`.
