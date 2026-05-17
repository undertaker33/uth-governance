# 工程治理模板

本文件只保存可复制模板和最少字段说明。

场景规则见 `docs/AGENT_工程治理启动手册.md`；Hook 字段和门禁细节见 `docs/HOOKS_工程治理门禁手册.md`。

占位说明：

- `<localized-*>` 按 `.uth-governance/project.json` 的 `document_language` 选择文件名和正文语言。
- 本文件示例默认以中文为主；实例化到非中文项目时，标题和自然语言标签必须按 `document_language` 翻译。路径、JSON key、skill 名、命令、`Git Baseline`、`Source evidence` 等稳定标识可保留英文。
- 没有代码证据的事实写 `TBD` 或 `Needs uth-docs confirmation from code facts.`。
- `Source evidence` 填文件路径、命令输出、git range、数据库 schema、运行截图或用户确认来源。

---

## 1. AGENTS.md 模板

````md
# AGENTS.md

本仓库启用 UTH 工程治理。

## 入口文件

- 治理标记: `.uth-governance/project.json`
- 文档索引: `docs/README.md`
- 当前状态: see `.uth-governance/project.json` -> `entrypoints.current_state`
- 模块上下文索引: `docs/context/README.md`

## 规则指针

- 场景路由由已安装的 `uth-*` skills 执行。
- 项目本地制度：`docs/_governance/README.md`
- Hook runner：`tools/uth-hooks/uth-hook.py`

## 阅读顺序

1. `AGENTS.md`
2. `.uth-governance/project.json`
3. `docs/README.md`
4. `entrypoints.current_state`
5. 与任务相关的 `docs/context/*.md`
6. 当前 Design / Todo / Feedback / Worker Prompt

## 稳定项目约束

-
````

---

## 2. docs/README.md 模板

````md
# 项目文档入口

## 常驻上下文

- `<localized-current-state>.md`: 当前状态索引。
- `<localized-project-overview>.md`: 项目定位、结构、技术栈。
- `<localized-architecture>.md`: 架构、模块边界、调用关系。
- `<localized-development>.md`: 本地启动、测试、构建。
- `context/README.md`: 模块上下文入口。

## 治理制度

- `_governance/README.md`: 项目本地制度索引。
- 场景路由由已安装的 `uth-*` skills 执行。
- Hook runner 见项目本地 `tools/uth-hooks/uth-hook.py`。

## 任务与记录

- `work/`: Design、Todo、Feedback、Run Log、Worker Prompt。
- `LW-Work/`: 轻量开发最终记录。
- `decisions/`: ADR。
- `changelogs/`: 正式版本 changelog。
- `snapshots/`: onboarding handoff 等项目级快照。
- `state/snapshots/`: 历史状态快照。
- `archive/`: 不再活跃的任务和轻量记录。
````

---

## 3. .uth-governance/project.json 模板

```text
.uth-governance/project.json
```

```json
{
  "schema": "uth-governance-project/v1",
  "enabled": true,
  "onboarded_at": "YYYY-MM-DDTHH:mm:ss+08:00",
  "onboarding_mode": "new-project | existing-project",
  "docs_root": "docs",
  "document_language": {
    "code": "zh-CN | en-US | bilingual | custom",
    "label": "Simplified Chinese | English | bilingual | user-specified label",
    "source": "user-selected",
    "selected_at": "YYYY-MM-DDTHH:mm:ss+08:00",
    "applies_to": "governance-docs-and-closeout-reports"
  },
  "entrypoints": {
    "agent": "AGENTS.md",
    "docs": "docs/README.md",
    "current_state": "docs/<localized-current-state>.md",
    "context": "docs/context/README.md"
  }
}
```

---

## 4. docs/<localized-current-state>.md 模板

````md
# 当前项目状态

更新时间: YYYY-MM-DD HH:mm

## 当前阶段

- 阶段:
- 状态:

## 当前活跃工作

| Item | Status | File |
| --- | --- | --- |
| DYYMMDDXX | draft / active / blocked / complete | `docs/work/...` |

## 模块队列 / 已完成 / 当前

- 当前:
- 队列:
- 已完成:

## 阻塞项

- None

## 验证

| Time | Command or method | Result | Notes |
| --- | --- | --- | --- |
|  |  |  |  |

## 未验证项

-

## 风险与回滚

- 风险:
- 回滚:

## Git Baseline

- Branch:
- Commit:
- Source: commit / git range / stable code / workspace state
- 更新时间:

## 事实来源证据

- `.uth-governance/project.json`
- `docs/context/README.md`
-
````

---

## 5. docs/<localized-project-overview>.md 模板

````md
# 项目概览

## 项目名称

-

## 一句话定位

-

## 目标用户

-

## 仓库结构

```text
project-root/
├── frontend/
├── backend/
├── docs/
├── tools/
│   └── uth-hooks/
└── scripts/
```

## 技术栈

- Frontend:
- Backend:
- Database:
- Infrastructure:
- Tools:

## 主要入口

- App:
- API:
- CLI:
- Docs:

## 范围

- 范围内:
- 范围外:

## 事实来源证据

-
````

---

## 6. docs/<localized-architecture>.md 模板

````md
# 架构说明

## 系统形态

```text
Client / UI
-> API / Service
-> Domain / Runtime
-> Data / External Systems
```

## 模块边界

| Module | Owns | Does not own |
| --- | --- | --- |
|  |  |  |

## 调用流

```text
Entry
-> Validation
-> Business logic
-> Persistence / integration
-> Output
```

## 验证

- Architecture checks:
- Build/test checks:

## 事实来源证据

-
````

---

## 7. docs/<localized-development>.md 模板

````md
# 开发运行手册

## 环境要求

- OS:
- Language runtime:
- Package manager:
- SDK:

## 环境要求 Variables

| Name | Required | Example | Notes |
| --- | --- | --- | --- |
|  |  |  |  |

## 安装依赖

```bash
```

## 启动

```bash
```

## 测试

```bash
```

## 构建

```bash
```

## 验证

- Expected local checks:
- Known limits:

## 事实来源证据

-
````

---

## 8. docs/context/README.md 模板

````md
# 模块上下文入口

`docs/context/` 保存模块级当前事实摘要。

## 模块队列 / 已完成 / 当前

- 当前:
- 队列:
- 已完成:

## 模块索引

| File | Module | Status | Source evidence |
| --- | --- | --- | --- |
| `01-module.md` |  | current / queued / completed |  |

## 跨模块上下文

- Shared constraints:
- Shared verification:
- Shared risks:

## 事实来源证据

-
````

---

## 9. docs/context/<NN-module>.md 模板

```text
docs/context/01-module-name.md
```

````md
# 01-module-name

## 职责

-

## 不负责

-

## 入口文件

-

## 依赖

-

## 常见修改点

-

## 验证

```bash
```

## 未验证项

-

## 风险与回滚

- 风险:
- 回滚:

## Git Baseline

- Branch:
- Commit:
- Source: commit / git range / stable code / workspace state
- 更新时间:

## 事实来源证据

-
````

---

## 10. docs/_governance/README.md 模板

````md
# 工程治理规则目录

本目录只保存项目本地制度；场景路由由已安装的 `uth-*` skills 执行，Hook 由项目本地 `tools/uth-hooks/uth-hook.py` 执行。

## 文件

- `agent-rules.md`: 项目本地 Agent 行为约束。
- `git-workflow.md`: Git 写入、PR、tag、release 约束。
- `subagent-workflow.md`: main / worker / evaluator 协作约束。
- `prompt-rules.md`: Worker Prompt 命名和落盘约束。
- `human-workflow.md`: 人类 Owner 检查点。
- `writing-rules.md`: 文档写入位置和必填字段。
- `hook-gates.md`: 项目本地 Hook 配置说明。
- `state-rules.md`: current-state 和 snapshot 维护字段。
- `adr-release-rules.md`: ADR、changelog、版本记录字段。
````

---

## 11. docs/_governance/agent-rules.md 模板

````md
# Agent 行为规则

场景路由由已安装的 `uth-*` skills 执行；本文件只记录本项目额外行为约束。

## 项目特定规则

-

## 已知误区

| ID | Symptom | Correct handling | Source evidence |
| --- | --- | --- | --- |
| E001 |  |  |  |
````

---

## 12. docs/_governance/hook-gates.md 模板

````md
# Hook 门禁项目配置

Hook 基础契约来自 UTH 治理包；本文件只记录本项目对 `tools/uth-hooks/uth-hook.py` 的本地配置和证据字段约定。

## 项目本地 Hook Runner

- Runner: `tools/uth-hooks/uth-hook.py`
- Config:
- Known exceptions:

## 必需证据字段

- Verification:
- Unverified items:
- Risk and rollback:
- Source evidence:
````

---

## 13. docs/_governance/git-workflow.md 模板

````md
# Git 工作流规则

## 分支策略

- Default branch:
- Work branch prefix:

## Git 写入确认

- Git 写入前必须先填写并展示 `Git 写入计划`。
- 用户确认后才执行 commit / push / merge / tag / release。

## 发布字段

- Changelog:
- Tag:
- Verification:
- Risk and rollback:
````

---

## 14. docs/_governance/subagent-workflow.md 模板

````md
# Subagent 协作规则

## 角色

- Main:
- Worker:
- Evaluator:

## 写入范围

- Allowed:
- Forbidden:

## 关联 worker Prompt

- Prompt directory: `docs/work/DYYMMDDXX-task/prompts/`
- Return format:
````

---

## 15. docs/_governance/prompt-rules.md 模板

````md
# Prompt 规则

## Worker Prompt 路径

```text
docs/work/DYYMMDDXX-task/prompts/PYYMMDD-HHMM-T01-worker-task-name.md
```

## 必填字段

- Task:
- Read scope:
- Allowed edits:
- Forbidden edits:
- Verification:
- Risk and rollback:
- Return format:
````

---

## 16. docs/_governance/human-workflow.md 模板

````md
# Human Workflow

## 所有者检查点

- Before implementation:
- Before Git write:
- Before release:

## 必需用户确认

- Scope:
- Risk and rollback:
- Git 写入计划:
````

---

## 17. docs/_governance/writing-rules.md 模板

````md
# 文档写入规则

## 写入目标

| Need | File |
| --- | --- |
| Current project status | `entrypoints.current_state` |
| Module facts | `docs/context/*.md` |
| Task design | `docs/work/.../00-...-design.md` |
| Todo | `docs/work/.../10-...-todo-...md` |
| Feedback | `docs/work/.../11-...-feedback-...md` |
| Lightweight final record | `docs/LW-Work/LWYYMMDDXX-...md` |

## 必填字段

- Verification
- Unverified items
- Risk and rollback
- Associated worker prompts
- Source evidence
- Git Baseline
````

---

## 18. docs/_governance/state-rules.md 模板

````md
# 状态维护规则

## current-state 字段

- Current Phase
- Active Work
- module queue/completed/current
- Verification
- Unverified items
- Risk and rollback
- Git Baseline
- Source evidence

## 快照路径

```text
docs/state/snapshots/SYYMMDD-description.md
```
````

---

## 19. docs/_governance/adr-release-rules.md 模板

````md
# ADR 与发布规则

## ADR 字段

- 状态:
- Date:
- Context:
- Decision:
- Consequences:

## Changelog 字段

- Version:
- Release date:
- Added:
- Changed:
- Fixed:
- Verification:
- Risk and rollback:
````

---

## 20. Design 模板

```text
docs/work/DYYMMDDXX-task-title/00-DYYMMDDXX-design.md
```

````md
# DYYMMDDXX: task title

## 基本信息

- Design ID: DYYMMDDXX
- 状态: draft / accepted / active / complete / blocked / abandoned
- Created at:

## 背景

-

## 目标

-

## 范围

- In:
- Out:

## 涉及模块

-

## 方案

-

## 验收口径

- [ ]

## Todo 拆分

| Todo ID | Title | Status | File |
| --- | --- | --- | --- |
| DYYMMDDXX-T01 |  | not started | `10-DYYMMDDXX-T01-todo-task-name.md` |

## 验证

- Required:

## 风险与回滚

- 风险:
- 回滚:

## 事实来源证据

-
````

---

## 21. Todo 模板

```text
docs/work/DYYMMDDXX-task-title/10-DYYMMDDXX-T01-todo-task-name.md
```

````md
# DYYMMDDXX-T01: task name

## 基本信息

- Design: DYYMMDDXX
- Todo ID: DYYMMDDXX-T01
- 状态: not started / active / complete / blocked / abandoned
- Feedback: `11-DYYMMDDXX-T01-feedback-task-name.md`

## 目标

-

## 允许范围

-

## 禁止范围

-

## 检查清单

- [ ]

## 验收口径

- [ ]

## 验证

```bash
```

## 未验证项

-

## 风险与回滚

- 风险:
- 回滚:

## 事实来源证据

-
````

---

## 22. Feedback 模板

```text
docs/work/DYYMMDDXX-task-title/11-DYYMMDDXX-T01-feedback-task-name.md
```

````md
# DYYMMDDXX-T01 Feedback: task name

## 基本信息

- Design: DYYMMDDXX
- Todo: DYYMMDDXX-T01
- 状态: complete / partial / blocked / abandoned
- Date:

## 已完成

-

## 未完成

-

## 修改文件

-

## 关联 worker Prompt

- None / `docs/work/DYYMMDDXX-task-title/prompts/PYYMMDD-HHMM-T01-worker-task-name.md`

## 验证

| Command or method | Result | warning | exception | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 未验证项

-

## 风险与回滚

- 风险:
- 回滚:

## Git Baseline

- 状态: pending uth-git / committed
- Branch:
- Commit:
- PR:

## 事实来源证据

-
````

---

## 23. Run Log 模板

```text
docs/work/DYYMMDDXX-task-title/runs/RYYMMDD-HHMM-T01-run-log.md
```

````md
# RYYMMDD-HHMM-T01 Run Log

## 基本信息

- Time:
- Scene:
- Todo:
- Executor:

## 目标

-

## 步骤

-

## 证据

```text
```

## 验证

-

## 关联 worker Prompt

- None

## 未验证项

-

## 事实来源证据

-
````

---

## 24. Worker Prompt 模板

```text
docs/work/DYYMMDDXX-task-title/prompts/PYYMMDD-HHMM-T01-worker-task-name.md
```

````md
# PYYMMDD-HHMM-T01 worker: task name

## 关联工作

- Design:
- Todo:
- Role: worker
- Created at:
- Dispatcher:

## 必读文件

-

## 默认跳过

- Old Design:
- Old Feedback:
- Old Run Log:

## 任务

-

## 允许修改

-

## 禁止修改

-

## 验证

```bash
```

## 未验证项

-

## 风险与回滚

- 风险:
- 回滚:

## 回传格式

- Read scope:
- Changed files:
- Completed:
- Not completed:
- Verification:
- warning count:
- exception count:
- Unverified items:
- Risk and rollback:
````

---

## 25. LW-Work 模板

```text
docs/LW-Work/LWYYMMDDXX-light-task-title.md
```

````md
# LWYYMMDDXX: light task title

## 原始需求

>

## 场景判定

- Scene: uth-dev / light-dev
- UTH-SP used: no / yes, reason:
- Formal work item: none /

## 修改内容

- Changed files:
- Behavior change:
- Not touched:

## 验证

- Command or method:
- Result:
- warning count:
- exception count:

## 未验证项

-

## 风险与回滚

- 风险:
- 回滚:

## Git Baseline

- 状态: pending uth-git / committed
- Branch:
- Commit:
- PR:
- tag:
- 更新时间:

## 事实来源证据

-
````

---

## 26. ADR 模板

```text
docs/decisions/ADR-0001-title.md
```

````md
# ADR-0001: title

## 状态

Proposed / Accepted / Superseded / Deprecated / Rejected

## 日期

YYYY-MM-DD

## 背景

-

## 决策

-

## 替代方案

-

## 影响

-

## 事实来源证据

-
````

---

## 27. Changelog 模板

```text
docs/changelogs/v0.1.0.md
```

````md
# v0.1.0: release title

Release date: YYYY-MM-DD

## 新增

-

## 变更

-

## 修复

-

## 验证

-

## 风险与回滚

- 风险:
- 回滚:

## 事实来源证据

-
````

---

## 28. State Snapshot 模板

```text
docs/state/snapshots/SYYMMDD-description.md
```

````md
# SYYMMDD: state snapshot description

## 快照时间

YYYY-MM-DD HH:mm

## 当前阶段

-

## 已完成 Work

-

## 当前活跃工作

-

## 模块队列 / 已完成 / 当前

- 当前:
- 队列:
- 已完成:

## 验证

-

## 未验证项

-

## 风险与回滚

- 风险:
- 回滚:

## Git Baseline

- Branch:
- Commit:

## 事实来源证据

-
````

---

## 29. Archive README 模板

```text
docs/archive/README.md
```

````md
# 文档归档

本目录保存已完成、废弃或不再活跃的任务包和轻量记录。

## 索引

- `work/`: archived formal work packages.
- `LW-Work/`: archived light-work final records.

## 归档记录

| Path | Archived at | Reason | Source evidence |
| --- | --- | --- | --- |
|  |  |  |  |
````

---

## 30. Onboarding Handoff Snapshot 模板

```text
docs/snapshots/ONBYYMMDDXX-existing-project-handoff.md
```

````md
# ONBYYMMDDXX existing-project handoff

## 交接时间

YYYY-MM-DD HH:mm

## Git Baseline

- Branch:
- Commit:
- Dirty state:

## 备份

- `docs/ONBYYMMDDXX-pre-uth-docs-backup.zip`

## 旧文档结构

```text
```

## 已发现入口

-

## 已发现技术栈

-

## 已发现模块

-

## 可继承旧规则

-

## 未验证项

-

## 需要 uth-docs 继续处理

-

## 事实来源证据

-
````

---

## 31. Git 写入计划模板

````md
## Git 写入计划

## 当前分支

-

## git status 摘要

```text
```

## diff 摘要

```text
```

## 计划命令

```bash
```

## 建议 commit message

```text
type(scope): summary
```

## 验证

-

## 未验证项

-

## 风险与回滚

- 风险:
- 回滚:

## PR / Changelog / Tag 判断

- PR:
- Changelog:
- Tag:
- Release:

## Git 成功后的 Baseline 回填

- Feedback:
- LW-Work:
- current-state:

## 用户确认

- Waiting for explicit user confirmation before Git write: yes / no
````
