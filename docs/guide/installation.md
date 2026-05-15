# UTH Governance Installation

This guide is written for both humans and LLM agents. The preferred path is:
read this guide, run the installer, verify the result, and report exactly what
changed. Do not invent project facts while installing the governance pack.

## For Humans

Give your agent this prompt:

```text
Install and configure UTH Governance from this repository by following:
docs/guide/installation.md

Target project:
<absolute path to target project>
```

If you are installing by hand:

```bash
python scripts/install.py --target /path/to/project --runtime codex
```

Use one of:

- `--runtime codex`
- `--runtime claude`
- `--runtime opencode`
- `--runtime custom --skills-dir /path/to/skills`

## For LLM Agents

Follow these steps in order.

1. Confirm the source repository root.
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
   - State that no Git push was performed unless the user explicitly requested it.

## What the Installer Does

- Copies `skills/uth-*` and `skills/uth-sp-*` into the selected skills directory.
- Copies `tools/uth-hooks/` into the target project.
- Creates a lightweight documentation skeleton:
  - `docs/_governance/README.md`
  - `docs/current-state.md`
  - `docs/work/README.md`
  - `docs/work/LW-Work/`
  - `docs/context/README.md`
  - `docs/archive/README.md`
  - `docs/decisions/README.md`
  - `docs/changelogs/README.md`
- Appends a small UTH block to the target project root `AGENTS.md` if the block
  is not already present.

## What the Installer Does Not Do

- It does not push Git commits.
- It does not copy old task packages, archived work, or current-state facts from
  this governance-pack repository into the target project.
- It does not duplicate scene-flow details into the target project `AGENTS.md`.
- It does not modify existing project docs except for appending the marked UTH
  block to root `AGENTS.md`.
