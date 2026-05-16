[English](README.md) | [中文](README.zh-CN.md)

# UTH Governance

UTH Governance 是一个面向编码代理的轻量工程治理包。它关注代理在工程任务中何时读文档、何时写文档、加载哪些上下文，以及如何在不把所有任务都变成重流程的前提下完成可追踪的收口。

## 为什么使用 UTH

- 保持代理工作可追踪，同时避免每个任务都过度治理。
- 区分场景命令、方法技能、Hook 门禁、文档和 Git 收口。
- 同时支持轻量开发和正式的 Design/Todo/Feedback 工作流。

## 工作方式

UTH 有三层：

1. 一次性安装的全局 skills。
2. 通过 `/uth-onboarding` 在项目本地显式启用。
3. 通过场景命令选择合适的治理路径。

## 快速开始

### 第 1 步：安装 UTH

把下面这段交给代理执行：

```text
Install UTH Governance from GitHub:
https://github.com/undertaker33/uth-governance.git

Follow docs/guide/installation.md from that repository.
Use runtime codex.
Do not initialize the current project during installation.
```

也可以手动安装：

```bash
git clone https://github.com/undertaker33/uth-governance.git
cd uth-governance
python scripts/install.py --runtime codex
```

如果是更新已有安装，见 [一句话更新](#一句话更新)。

### 第 2 步：在项目中启用 UTH

打开目标项目，并显式运行：

```text
/uth-onboarding
```

### 第 3 步：使用场景命令

根据任务选择对应的场景命令：

```text
/uth-dev
/uth-debug
/uth-review
/uth-git
```

## 场景命令

| 命令 | 适用场景 |
| --- | --- |
| `/uth-onboarding` | 在新项目中启用 UTH，在已有项目中只做 enable-only 启用，或在用户明确要求时编排完整的老项目接管。 |
| `/uth-governance` | 让代理判断一个不明确的工程请求应该进入哪个 UTH 场景。 |
| `/uth-design` | 评估架构、比较方案，或写入已接受的 Design。 |
| `/uth-dev` | 实现清晰、边界明确的变更或正式 Todo。 |
| `/uth-debug` | 诊断并修复 bug、失败测试、构建错误或回归。 |
| `/uth-review` | 做代码审查、验证、验收或就绪检查。 |
| `/uth-docs` | 基于代码事实治理项目文档：全项目基线、范围同步、模块拆分、onboarding follow-up、current-state、context、归档、快照和迁移。 |
| `/uth-git` | 提交、推送、开 PR、合并 PR、打 tag、发布或关闭分支。 |
| `/uth-context-trace` | 查找 Design/Todo/Feedback/Prompt/Run/LW/ADR 等证据。 |
| `/uth-utf8-guard` | 检查治理 Markdown 的 UTF-8、乱码风险和代码围栏平衡。 |

## UTH-SP 方法技能

`uth-sp-*` 表示 UTH Superpower。这些 skill 是 UTH 场景使用的 Superpower 方法层，通常由当前场景自动选择；如果你明确需要某个方法，也可以直接点名。

| 命令 | 适用场景 |
| --- | --- |
| `/uth-sp-brainstorming` | 需求、范围、选项或验收标准不清晰。 |
| `/uth-sp-writing-plans` | 已接受的 Design 需要落成实施计划。 |
| `/uth-sp-executing-plans` | 已接受的计划需要在当前窗口内执行。 |
| `/uth-sp-test-driven-development` | 行为、API、权限、状态机或回归工作需要测试先行。 |
| `/uth-sp-systematic-debugging` | 修复前需要先做系统化根因诊断。 |
| `/uth-sp-subagent-driven-development` | 正式开发需要使用 worker 子代理。 |
| `/uth-sp-dispatching-parallel-agents` | 多个独立领域可以并行委派。 |
| `/uth-sp-verification-before-completion` | 场景即将声明完成、修复、通过、就绪或可发布。 |
| `/uth-sp-requesting-code-review` | 已完成工作需要结构化代码审查。 |
| `/uth-sp-receiving-code-review` | 外部 review 反馈需要先分流，再决定是否修复。 |
| `/uth-sp-using-git-worktrees` | 工作需要隔离 workspace 或 worktree。 |
| `/uth-sp-finishing-a-development-branch` | 分支、PR、合并、清理、tag 或发布需要结构化收口。 |
| `/uth-sp-writing-skills` | 正在创建、更新或验证 UTH skill 或方法 skill。 |

## 轻量工作与正式工作

轻量开发在任务完成时写入一个 `docs/LW-Work/LW*.md` final record。它不创建单独的 LW Todo，也不会因为等待 Git baseline 信息而阻塞报告生成。

正式工作使用 `docs/work/D*/` 下的 Design/Todo/Feedback 文档。Feedback 在工作被接受时写入，并且早于任何 Git 收口。

Git baseline 信息属于 `uth-git` 场景。Git 写入成功后，`uth-git` 会把 baseline 追加到轻量 final record 或正式 Feedback 中。普通开发和 review 流程不应该因为等待 Git 而不生成报告。

## 项目启用行为

- 安装器只安装全局 skills。
- 安装器不会编辑当前项目、创建项目文档、全局安装 hook 工具，也不会创建 `.uth-governance/project.json`。
- `/uth-onboarding` 创建项目 marker，复制项目本地 `tools/uth-hooks/`，并创建最小治理文档脚手架。
- 在首次写入治理 Markdown 或生成场景收口报告前，UTH 会询问项目文档语言，并保存到 `.uth-governance/project.json` 的 `document_language` 中。
- 除非项目已经有 `.uth-governance/project.json`，其他 `uth-*` 场景会保持静默；用户显式要求启用 UTH 治理时除外。

## 老项目接管与文档基线

当用户要求 UTH 接管老项目时，`/uth-onboarding` 是编排者。它先完成安全前置流程，再路由到 `/uth-docs onboarding-followup` 做完整文档治理，最后回到 `/uth-onboarding` 做总收口。

`/uth-docs` 是基于代码事实的文档治理窗口。只有已有可信全项目基线时，才允许对指定 diff、range、版本、模块或文件范围输出 `scoped-docs-complete`。只有 `full-project-docs-complete` 才能支撑“项目完整文档治理完成”的声明。

项目过大时，`/uth-docs` 可以进入 `module-split`。它先写入 context 模块索引和拆分报告，停下来等待用户确认，然后逐模块治理。上下文过长时，它必须写轻量 final record，并给出新窗口续跑提示词，让下一个窗口从该记录继续。

## 包内容

- `skills/`：UTH 场景 skills 和 UTH-SP 方法 skills。
- `tools/uth-hooks/`：参考 L0/L1/L2/L3 hook runner，由 `uth-onboarding` 复制到目标项目。
- `docs/guide/installation.md`：面向人和代理的安装指南。
- `docs/AGENT_工程治理启动手册.md`：治理启动手册。
- `docs/TEMPLATES_工程治理模板.md`：文档模板。
- `docs/HOOKS_工程治理门禁手册.md`：Hook 门禁手册。
- `docs/FLOW_全链路流程图.md`：场景与 Hook 流程图。
- `scripts/install.py`：全局 skill 安装器。
- `scripts/verify.py`：治理包验证入口。

## 安装详情

代理安装时，让代理 clone 仓库、阅读 `docs/guide/installation.md`，并为目标运行时执行安装器。如果仓库是私有仓库，需要先保证代理的 Git 环境可以访问 GitHub。已经配置 SSH 时，也可以使用等价的 SSH clone URL。

手动安装：

```bash
python scripts/install.py --runtime codex
```

### 一句话更新

当 UTH 已经安装过，需要刷新全局 skills 时，把下面这段交给代理执行：

```text
Update UTH Governance from GitHub:
https://github.com/undertaker33/uth-governance.git

Follow docs/guide/installation.md from that repository.
Use runtime codex.
Overwrite existing UTH skills with --update.
Do not initialize the current project during update.
```

也可以在新的 clone 或已更新的本地 clone 中手动执行：

```bash
python scripts/install.py --runtime codex --update
```

`--update` 是 `--force` 的别名。它只覆盖所选全局 skills 目录中的既有 UTH skill 目录。它仍然不会运行 `uth-onboarding`、创建项目文档、把 hook 工具复制进当前项目，也不会创建 `.uth-governance/project.json`。

使用不同代理工具安装时，保持同一套安装或更新流程，只修改 `--runtime` 参数：

- Codex：`--runtime codex`
- Claude Code：`--runtime claude`
- OpenCode：`--runtime opencode`
- 自定义或非标准 skills 目录：`--runtime custom --skills-dir <path>`

常用安装参数：

- `--source <path>`：从指定 UTH 包根目录安装。
- `--skills-dir <path>`：覆盖自动检测到的 skills 安装目录。
- `--skip-skills`：运行安装器但不安装 skills。
- `--update`：更新已有 UTH skill 目录，是 `--force` 的别名。
- `--force`：覆盖已有 UTH skill 目录。
- `--dry-run`：只打印计划变更，不写入文件。

## 维护此治理包

发布治理包变更前运行验证：

```bash
python scripts/verify.py
```

版本号属于外层包目录或发布产物。内部手册和模板文件名有意不带版本后缀。

## 许可证

UTH Governance 使用 Apache License, Version 2.0。详见 [`LICENSE`](LICENSE)。

部分 `uth-sp-*` 方法技能材料包含或改编自 [Superpowers](https://github.com/obra/superpowers)，Superpowers 使用 MIT License。重新分发这些材料时，请保留上游版权和许可声明。

## 致谢

UTH-SP 方法技能层受 [Superpowers](https://github.com/obra/superpowers) 启发，并部分改编自该项目。Superpowers 是 Jesse Vincent 和 Superpowers 贡献者创建的 agentic skills framework。

Superpowers 使用 MIT License。重新分发包含或改编自 Superpowers 内容的 UTH-SP 材料时，请保留上游版权和许可声明。

感谢 Superpowers 项目提供结构化 brainstorming、systematic debugging、test-driven development、planning、subagent development 和 verification-before-completion 等方法模式。
