#!/usr/bin/env python3
"""Install UTH Governance into a target project."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass, field
from pathlib import Path


UTH_BLOCK_START = "<!-- UTH-GOVERNANCE:START -->"
UTH_BLOCK_END = "<!-- UTH-GOVERNANCE:END -->"


@dataclass
class Report:
    actions: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def action(self, message: str) -> None:
        self.actions.append(message)

    def skip(self, message: str) -> None:
        self.skipped.append(message)

    def print(self) -> None:
        print("UTH Governance install report")
        print()
        print("Actions:")
        for item in self.actions or ["None"]:
            print(f"- {item}")
        print()
        print("Skipped:")
        for item in self.skipped or ["None"]:
            print(f"- {item}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install UTH Governance into a target project.")
    parser.add_argument("--source", default=None, help="UTH package root. Defaults to this script's parent repository.")
    parser.add_argument("--target", required=True, help="Target project root.")
    parser.add_argument("--runtime", choices=["codex", "claude", "opencode", "custom"], default="codex")
    parser.add_argument("--skills-dir", default=None, help="Override skill install directory.")
    parser.add_argument("--project-init-only", action="store_true", help="Only initialize target project docs and AGENTS.md.")
    parser.add_argument("--skip-skills", action="store_true", help="Do not install skills.")
    parser.add_argument("--skip-tools", action="store_true", help="Do not install hook tools.")
    parser.add_argument("--skip-docs", action="store_true", help="Do not create project docs or AGENTS.md block.")
    parser.add_argument("--force-docs", action="store_true", help="Overwrite UTH project documentation scaffold files and AGENTS.md UTH block.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing UTH skill/tool directories.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files.")
    return parser.parse_args()


def package_root(args: argparse.Namespace) -> Path:
    root = Path(args.source).expanduser().resolve() if args.source else Path(__file__).resolve().parents[1]
    required = ["AGENTS.md", "skills", "tools/uth-hooks"]
    missing = [item for item in required if not (root / item).exists()]
    if missing:
        raise SystemExit(f"Source is not a UTH package root: {root}; missing {', '.join(missing)}")
    return root


def default_skills_dir(runtime: str) -> Path:
    home = Path.home()
    if runtime == "codex":
        import os

        base = os.environ.get("CODEX_HOME")
        return Path(base).expanduser() / "skills" if base else home / ".codex" / "skills"
    if runtime == "claude":
        return home / ".claude" / "skills"
    if runtime == "opencode":
        import os

        base = os.environ.get("OPENCODE_CONFIG_DIR")
        return Path(base).expanduser() / "skills" if base else home / ".config" / "opencode" / "skills"
    raise SystemExit("--runtime custom requires --skills-dir")


def ensure_dir(path: Path, report: Report, dry_run: bool) -> None:
    if path.exists():
        return
    report.action(f"create directory {path}")
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)


def copy_directory(src: Path, dst: Path, *, force: bool, dry_run: bool, report: Report) -> None:
    if src.resolve() == dst.resolve():
        report.skip(f"source and destination are identical: {dst}")
        return
    if dst.exists() and not force:
        report.skip(f"exists; use --force to overwrite: {dst}")
        return
    if dst.exists() and force:
        report.action(f"overwrite directory {dst}")
        if not dry_run:
            shutil.rmtree(dst)
    else:
        report.action(f"copy directory {src} -> {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)


def install_skills(source: Path, skills_dir: Path, args: argparse.Namespace, report: Report) -> None:
    ensure_dir(skills_dir, report, args.dry_run)
    for src in sorted((source / "skills").iterdir()):
        if src.is_dir() and src.name.startswith("uth-"):
            copy_directory(src, skills_dir / src.name, force=args.force, dry_run=args.dry_run, report=report)


def install_tools(source: Path, target: Path, args: argparse.Namespace, report: Report) -> None:
    copy_directory(source / "tools" / "uth-hooks", target / "tools" / "uth-hooks", force=args.force, dry_run=args.dry_run, report=report)


def write_if_absent(path: Path, content: str, report: Report, dry_run: bool, *, force: bool = False) -> None:
    if path.exists() and not force:
        report.skip(f"exists: {path}")
        return
    report.action(f"{'overwrite' if path.exists() else 'create'} file {path}")
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def append_agents_block(target: Path, report: Report, dry_run: bool, *, force: bool = False) -> None:
    agents = target / "AGENTS.md"
    block = f"""

{UTH_BLOCK_START}
## UTH Governance

- 工程任务先由 `uth-governance` 判断场景，再进入对应 `uth-*` 子 Skill。
- 本文件只保留仓库级最小入口；项目治理规则放在 `docs/_governance/`。
- `docs/current-state.md` 是当前状态索引，不是日志。
- 文档结构入口：`docs/README.md`。
- Hook 入口：`tools/uth-hooks/uth-hook.py`。
{UTH_BLOCK_END}
""".lstrip()
    if agents.exists():
        text = agents.read_text(encoding="utf-8")
        if UTH_BLOCK_START in text:
            if not force:
                report.skip(f"UTH block already present: {agents}")
                return
            start = text.index(UTH_BLOCK_START)
            end = text.index(UTH_BLOCK_END, start) + len(UTH_BLOCK_END)
            new_text = text[:start].rstrip() + "\n\n" + block.rstrip() + "\n" + text[end:].lstrip()
            report.action(f"replace UTH block in {agents}")
        else:
            new_text = text.rstrip() + "\n\n" + block
            report.action(f"append UTH block to {agents}")
    else:
        new_text = "# AGENTS.md\n\n本文件是仓库级 Agent 最小入口。完整场景流程由 `uth-*` skills 承接。\n\n" + block
        report.action(f"create {agents}")
    if not dry_run:
        agents.write_text(new_text, encoding="utf-8", newline="\n")


def project_doc_files(target: Path) -> dict[Path, str]:
    return {
        target / "docs" / "README.md": """# 项目文档入口

本文档目录按“当前事实、任务证据、长期记录、归档”分层。Agent 先读本文件，再按任务场景读取必要文档，不默认扫描全部 `docs/`。

## 1. 常驻上下文

- `current-state.md`：当前项目状态索引，不是日志。
- `project-overview.md`：项目概览、技术栈、模块和非目标范围。
- `architecture.md`：当前架构、模块边界和调用关系。
- `development.md`：本地环境、启动、测试和构建。
- `context/`：模块级当前事实摘要，用于按需装载上下文。

## 2. 治理规则

- `_governance/`：Agent、Git、Subagent、文档写入、状态维护、ADR / 发布、Hook 门禁等项目制度。
- `_governance/` 不保存 `uth-*` skill 的路由、触发条件或执行流程。

## 3. 任务包

- `work/`：正式任务包，按 `DYYMMDDXX-任务包标题/` 聚合 Design / Todo / Feedback / Prompt / Run Log。
- `work/LW-Work/`：轻量开发 Todo 和轻量 Git 提交记录。

## 4. 归档与长期记录

- `archive/`：已确认完成且不再活跃的任务包和 LW 文档，不作为当前事实源。
- `decisions/`：ADR 决策证据链，不作为当前事实源。
- `changelogs/`：正式版本 changelog。
""",
        target / "docs" / "_governance" / "README.md": """# 工程治理规则目录

本目录存放项目内工程治理规则。

本目录不保存 `uth-*` skill 的路由表、触发条件或执行流程。场景判断、上下文装载策略和收口协议由 `uth-governance` 与各子 Skill 自身负责。

## 文件说明

- `agent-rules.md`：Agent 行为细则和常见误判。
- `git-workflow.md`：Git、分支、PR、tag、release、锁规则。
- `subagent-workflow.md`：Main Agent / 子代理 / worktree 协作规则。
- `writing-rules.md`：Design / Todo / Feedback / Run Log / LW-Work 写入规则。
- `hook-gates.md`：L1-L3 门禁：歧义、写入范围、Git、强验证、UTF-8、脚本守卫。
- `state-rules.md`：current-state 和 snapshots 维护规则。
- `adr-release-rules.md`：ADR、Changelog、版本号和发布规则。

## 使用原则

- Agent 不默认全读本目录。
- 只有当前场景需要对应制度时，才读取对应规则文件。
- 写入、派工、Git、完成声明和文档编码应通过 Hook 或等价门禁。
""",
        target / "docs" / "_governance" / "agent-rules.md": """# Agent 行为规则

本文件记录通用 Agent 行为约束、跨场景误判和项目内长期协作规则。项目级当前主线、模块索引和仓库特有硬约束写入根 `AGENTS.md`；当前事实写入 `docs/current-state.md` 和 `docs/context/`。

## 1. 总原则

- 默认少读少写。
- 任务范围不清时停下来问一个澄清问题。
- 不把其他场景动作带入当前场景。
- 不把旧 Design、旧 Feedback、旧 Run Log、Prompt 或 LW 记录当作当前事实。
- 不伪造测试、构建、验证结果。
- 代码改动默认要求编译 / 构建通过且 `0 warning / 0 exception`。
- 不在用户确认前执行 Git 写入。
- 修改 `AGENTS.md`、根目录 `README.md`、`docs/**/*.md` 或任务包 Markdown 前后，必须做 UTF-8 检查。

## 2. 禁止跨场景加戏

- 只读分析不自动升级为文档治理。
- Debug 不自动升级为架构设计。
- 增量开发不自动升级为重构。
- Git 收口不自动修改业务代码。
- 文档治理不自动审查全仓代码。

## 3. 高频误判

如同一类跨模块误判重复出现两次及以上，再补充到本节。
""",
        target / "docs" / "_governance" / "git-workflow.md": """# Git 工作流规则

任何 Git 写入前必须进入 `uth-git`，展示计划并等待用户确认。

## 1. Git 写入包括

- `git add`
- `git commit`
- `git tag`
- `git merge`
- `git rebase`
- `git push`
- `git switch`
- `git checkout`
- 创建、重命名或删除分支
- 创建或删除 worktree

## 2. Git 写入前必须展示

- 当前分支。
- `git status`。
- diff 摘要。
- 计划执行的 Git 命令。
- 建议 commit message。
- 是否需要 PR。
- 是否需要 changelog。
- 是否需要 tag。
- 是否为轻量改动，以及 commit 成功后是否追加 LW 记录。
- 如包含代码改动，最近一次编译 / 构建结果、warning 数和 exception 数。

## 3. Commit Message

建议采用 Conventional Commits：

```text
type(scope): summary
```

常用类型：`feat`、`fix`、`docs`、`chore`、`refactor`、`test`、`build`、`ci`。

## 4. 轻量 Git 记录

轻量改动完成后，先询问用户是否允许提交。commit 成功后，再追加或创建 `docs/work/LW-Work/LWYYMMDDXX-轻量任务标题.md`。
""",
        target / "docs" / "_governance" / "subagent-workflow.md": """# Subagent 协作规则

## 1. 核心原则

```text
主窗口负责上下文和收口。
子代理负责边界清晰的局部任务。
Git 写入只由获得用户确认的主窗口执行。
不创建 worktree 时，同一个物理工作区只能有一个写入者。
```

## 2. 默认角色

- `worker`：授权范围内实现，不执行 Git 写入。
- `planner`：只读探索、方案拆分、上下文整理，不修改代码。
- `evaluator`：只读验收，不修改代码和文档。

## 3. Worker Prompt

凡派发 `worker`，完整 Prompt 必须先写入当前正式任务包 `prompts/`。同一 worker 返工时追加更新原 Prompt；planner / evaluator 不记录 Prompt。

短提示词只要求 worker 读取对应 Prompt 文件并执行。
""",
        target / "docs" / "_governance" / "writing-rules.md": """# 文档写入规则

## 1. Design

Design 是任务包设计，不是长期事实。

```text
docs/work/DYYMMDDXX-任务包标题/00-DYYMMDDXX-design.md
```

## 2. Todo

Todo 是 Agent 可以在一个连续开发窗口内完成并自证的最小交付块，不按文件、层级或技术步骤机械拆分。

```text
10-DYYMMDDXX-T01-todo-任务名.md
20-DYYMMDDXX-T02-todo-任务名.md
```

## 3. Feedback

Feedback 是 Todo 的交付报告，不是过程日志。Git 证据由 `uth-git` 收口记录；如果当时已经存在，可以在 Feedback 中作为可选链接补充。

## 4. LW-Work

轻量开发使用两份文档，均放在 `docs/work/LW-Work/`：

```text
LWYYMMDDXX-轻量任务标题-todo.md
LWYYMMDDXX-轻量任务标题.md
```

- 轻量 Todo 在开发前或首次写文件前创建。
- 最终 LW 记录只在轻量改动 commit 成功后追加或创建。
- 无 commit 不写最终 LW 记录。

## 5. Context

`docs/context/` 是模块级当前事实摘要，不是任务日志。模块 context 应标明 Git baseline；如根据未提交工作区改动更新，可暂不写或不更新 baseline，并在收口说明。
""",
        target / "docs" / "_governance" / "hook-gates.md": """# Hook 门禁规则

Hook 是工程治理门禁，不是研发流程。Hook 只检查调用方提供的场景、范围、确认和验证事实，不定义 `uth-*` 的路由或执行流程。

## 1. 门禁结果

```text
PASS  放行
WARN  提醒并记录
ASK   暂停并请求用户确认
BLOCK 阻断
```

## 2. L1 Process Gate

- 场景清楚但需求、范围、方案或验收有歧义时，必须提供已澄清、已 brainstorming 或明确豁免理由。
- `worker` 派发前必须先写入完整 Prompt。
- `planner` / `evaluator` 只读，不记录 Prompt。

## 3. L2 Tool Gate

- 写入目标在当前场景允许范围内才放行。
- 超范围但非硬禁区，先问用户是否临时扩展范围。
- Git 写入必须进入 `uth-git` 并等待用户确认。
- 修改治理 Markdown 前后，必须通过 UTF-8 检查。

## 4. L3 Closeout Gate

- 声称完成、修复、通过、可交付前必须有新鲜证据。
- `uth-dev` / `uth-debug` 代码改动后必须编译 / 构建通过，且 `0 warning / 0 exception`。
- 确实清不掉且后续单独清理更合理时，先询问用户是否临时豁免；用户显式豁免后，不得声称完成、通过、可交付。
""",
        target / "docs" / "_governance" / "state-rules.md": """# 状态维护规则

`docs/current-state.md` 是当前状态索引，不是项目日志。

## 1. 建议上限

- 不超过 80-120 行。
- 最近变化最多 3 条。
- 最近验证最多 1 条。

## 2. 必须更新

- Todo 完成。
- Todo 阻塞。
- 当前活跃任务包变化。
- 当前阶段变化。
- 关键阻塞变化。
- 最近一次验证结果影响下一步判断。

## 3. 不必更新

- 只读分析。
- 纯讨论。
- 没形成任务状态变化的方案评估。
- 临时 Debug 过程中的每一步。
- 普通轻量改动的 LW 记录，除非影响当前阶段、阻塞、验证基线或发布判断。
""",
        target / "docs" / "_governance" / "adr-release-rules.md": """# ADR 与发布规则

## 1. ADR

ADR 只记录长期技术决策。ADR 是决策证据链，不是当前事实源；当前事实必须同步到常驻上下文文档。

适合写 ADR：

- 技术栈选择或变更。
- 核心架构变化。
- 数据库模型重大变化。
- 接口契约策略变化。
- 部署方式变化。
- 长期影响后续开发的规则变化。

ADR 状态：`Proposed`、`Accepted`、`Superseded`、`Deprecated`、`Rejected`。

## 2. Changelog

Changelog 只在正式版本发布时写。

- 一个正式 Git tag 必须对应一个 changelog。
- 一个 changelog 必须对应一个正式 Git tag。
- 普通开发 commit 不强制新增 changelog。
""",
        target / "docs" / "current-state.md": """# 当前项目状态

更新时间：YYYY-MM-DD HH:mm

## 1. 当前阶段

- 阶段：未记录

## 2. 当前活跃任务包

| 任务包 | 状态 | 说明 |
| --- | --- | --- |
| 无 | - | - |

## 3. 当前活跃 Todo

| Todo | 状态 | 文件 |
| --- | --- | --- |
| 无 | - | - |

## 4. 当前阻塞项

- 无

## 5. 最近 3 条变化

- 暂无

## 6. 最近一次验证

| 时间 | 命令或方式 | 结果 | 说明 |
| --- | --- | --- | --- |
| 无 | - | - | - |

## 7. 下一步

- 补齐 `docs/project-overview.md`、`docs/architecture.md`、`docs/development.md` 或 `docs/context/` 中的当前事实。

## 8. 当前事实来源

- `docs/README.md`
- `docs/project-overview.md`
- `docs/architecture.md`
- `docs/development.md`
- `docs/context/README.md`
""",
        target / "docs" / "project-overview.md": """# 项目概览

## 1. 项目名称

## 2. 一句话定位

本项目用于【解决什么问题】，面向【目标用户】，核心价值是【核心价值】。

## 3. 项目结构

```text
project-root/
├─ docs/
└─ ...
```

## 4. 技术栈

Frontend:

-

Backend:

-

Database:

-

Infrastructure / Tools:

-

## 5. 启动命令

```bash
```

## 6. 构建命令

```bash
```

## 7. 测试命令

```bash
```

## 8. 当前阶段

## 9. 非目标范围

-

## 10. 关键约束

-
""",
        target / "docs" / "architecture.md": """# 架构说明

## 1. 总体架构

```text
Client / UI
    |
API / Service
    |
Data / Runtime / External Tools
```

## 2. 模块职责

| 模块 | 职责 | 不负责 |
| --- | --- | --- |
|  |  |  |

## 3. 调用关系

```text
入口
-> 应用服务
-> 领域规则 / 工具
-> 数据访问 / 外部服务
```

## 4. 数据流

```text
输入
-> 校验
-> 处理
-> 持久化
-> 输出
```

## 5. 禁止事项

- 不允许跨层调用。
- 不允许 UI 层写核心业务规则。
- 不允许 API 层承载复杂业务流程。
- 不允许数据访问层混入复杂业务判断。
- 不允许临时代码绕过统一入口。
""",
        target / "docs" / "development.md": """# 开发运行手册

## 1. 环境要求

- 操作系统：
- 语言运行时：
- 包管理器：
- SDK：

## 2. 环境变量

| 变量名 | 是否必填 | 示例 | 说明 |
| --- | --- | --- | --- |
|  |  |  |  |

必须提供 `.env.example`，不得提交真实密钥。

## 3. 安装依赖

```bash
```

## 4. 启动开发环境

```bash
```

## 5. 测试

```bash
```

## 6. 构建

```bash
```

## 7. 常见本地问题

### 问题 1

现象：

处理：
""",
        target / "docs" / "work" / "README.md": """# 任务包目录

`docs/work/` 存放正式任务包。每个任务包对应一个阶段目标、功能闭环、修复包或设计包。

## 1. 正式任务包

```text
docs/work/DYYMMDDXX-任务包标题/
├─ 00-DYYMMDDXX-design.md
├─ 10-DYYMMDDXX-T01-todo-任务名.md
├─ 11-DYYMMDDXX-T01-feedback-任务名.md
├─ prompts/
└─ runs/
```

## 2. 轻量开发

轻量开发记录放在 `LW-Work/`。轻量 Todo 在开发前或首次写文件前创建；最终 LW 记录只在 commit 成功后追加或创建。
""",
        target / "docs" / "work" / "LW-Work" / "README.md": """# 轻量开发记录

本目录保存轻量开发 Todo 和轻量 Git 提交记录，不替代正式任务包。

## 文件

```text
LWYYMMDDXX-轻量任务标题-todo.md
LWYYMMDDXX-轻量任务标题.md
```

## 规则

- 轻量 Todo 在开发前或首次写文件前创建。
- 最终 LW 记录只在用户确认并完成 Git commit 后追加或创建。
- 无 commit 不写最终 LW 记录。
- LW 记录不进入 `current-state`，除非它影响当前阶段、阻塞、验证基线或发布判断。
""",
        target / "docs" / "context" / "README.md": """# 模块上下文入口

`docs/context/` 保存模块级当前事实摘要，用于帮助 Agent 按需装载上下文。

本目录不是任务日志，不记录每次 diff，不复制 Feedback / worker Prompt / Run Log。

## 拆分原则

简单项目可先按前端、后端、数据、部署等技术边界拆分。

复杂项目应先由文档治理窗口理解全仓并提出拆分建议，经用户确认后再创建模块上下文。优先按业务 / 领域边界拆分，其次按运行时职责、架构层、协作边界和验证边界拆分。

## 使用原则

- 开发、Debug、Review 前按需读取相关模块文件。
- 如果只是定位代码位置，不需要默认读取全部 context。
- 旧任务包、Prompt、Run Log、LW 记录不能覆盖 context 中的当前事实。
- 模块文件应标明 Git baseline；如根据未提交工作区改动更新，可暂不写或不更新 baseline，并在收口说明。
""",
        target / "docs" / "archive" / "README.md": """# 文档归档

本目录保存已明确完成且不再活跃的任务包和轻量开发记录。

归档内容不是当前事实源；当前事实仍以 `docs/current-state.md`、`docs/context/` 和常驻上下文文档为准。

## 1. 目录

- `work/`：正式任务包归档。
- `LW-Work/`：轻量开发 Todo 和最终 LW 记录归档。

## 2. 归档规则

- 只归档已确认完成、废弃或被替代，且不再出现在 current-state 活跃索引中的内容。
- LW 归档时，`LW*-todo.md` 与 `LW*.md` 一起迁移；如只有 Todo，说明未提交或未生成最终记录。
""",
        target / "docs" / "decisions" / "README.md": """# ADR 决策记录

本目录保存长期技术决策证据链。

ADR 不是当前事实源。当前事实必须同步到 `docs/current-state.md`、`docs/context/` 或常驻上下文文档。
""",
        target / "docs" / "changelogs" / "README.md": """# Changelog

本目录保存正式版本 changelog。

Changelog 面向用户，不充当 commit log。普通开发 commit 不强制新增 changelog。
""",
    }


def install_docs(target: Path, args: argparse.Namespace, report: Report) -> None:
    dirs = [
        target / "docs",
        target / "docs" / "_governance",
        target / "docs" / "work",
        target / "docs" / "work" / "LW-Work",
        target / "docs" / "context",
        target / "docs" / "archive",
        target / "docs" / "archive" / "work",
        target / "docs" / "archive" / "LW-Work",
        target / "docs" / "decisions",
        target / "docs" / "changelogs",
        target / "docs" / "state" / "snapshots",
    ]
    for directory in dirs:
        ensure_dir(directory, report, args.dry_run)

    for path, content in project_doc_files(target).items():
        write_if_absent(path, content, report, args.dry_run, force=args.force_docs)
    append_agents_block(target, report, args.dry_run, force=args.force_docs)


def main() -> int:
    args = parse_args()
    if args.project_init_only:
        args.skip_skills = True
        args.skip_tools = True
    source = package_root(args)
    target = Path(args.target).expanduser().resolve()
    skills_dir = Path(args.skills_dir).expanduser().resolve() if args.skills_dir else default_skills_dir(args.runtime)
    report = Report()

    ensure_dir(target, report, args.dry_run)
    if not args.skip_skills:
        install_skills(source, skills_dir, args, report)
    if not args.skip_tools:
        install_tools(source, target, args, report)
    if not args.skip_docs:
        install_docs(target, args, report)

    report.print()
    print()
    print(f"Source: {source}")
    print(f"Target: {target}")
    print(f"Skills directory: {skills_dir}")
    print("Dry run: yes" if args.dry_run else "Dry run: no")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
