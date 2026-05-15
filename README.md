# UTH Governance

UTH Governance is a lightweight engineering-governance pack for coding agents.
It focuses on when to read documents, when to write documents, what context to
load, and how to close engineering work without turning every task into a
heavyweight process.

## Install With an Agent

Ask your coding agent to install the pack by following the installation guide:

```text
Install and configure UTH Governance from GitHub:
https://github.com/undertaker33/uth-governance.git

Target project is the current working directory.
Follow docs/guide/installation.md from that repository.
Use runtime codex.
```

If the repository is private, make sure the agent's Git environment can access
GitHub first. An equivalent SSH clone URL is fine when SSH is configured.

## Manual Install

Clone the repository, then run the installer:

```bash
git clone https://github.com/undertaker33/uth-governance.git
cd uth-governance
python scripts/install.py --target /path/to/project --runtime codex
```

If skills and hooks are already installed and you only want to initialize a
project's documentation system:

```bash
python scripts/install.py --target /path/to/project --runtime codex --project-init-only
```

Use `--runtime claude`, `--runtime opencode`, or `--skills-dir <path>` when the
target agent loads skills from a different location.

The installer copies UTH skills, installs the hook runner, creates the target
project documentation skeleton, and appends a small UTH block to the target
project `AGENTS.md` if needed.

## Package Contents

- `skills/`: UTH scene skills and UTH-SP method skills.
- `tools/uth-hooks/`: reference L1/L2/L3 hook runner.
- `AGENT_工程治理启动手册.md`: governance handbook.
- `TEMPLATES_工程治理模板.md`: document templates.
- `HOOKS_工程治理门禁手册.md`: hook gate manual.
- `docs/guide/installation.md`: install guide for humans and agents.

Versioning belongs to the outer package folder or release artifact. Internal
handbook/template filenames intentionally do not carry version suffixes.
