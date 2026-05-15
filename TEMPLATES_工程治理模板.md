# 工程治理模板

> 本文件只保存模板。  
> 启动手册不内嵌模板，Agent 只有在需要创建或更新对应文件时才读取本文件。

---

## 1. AGENTS.md 模板

````md
# AGENTS.md

本文件是仓库级 Agent 入口和项目全局规则层。  
只记录新窗口进入本仓库时必须立即知道的稳定信息。  
场景路由和执行流程由 `uth-*` skills 承接；`docs/_governance/` 只保存非场景流程类的项目制度。

## 0. 入口与让路

- 进入本仓库处理工程任务时，先由 `uth-governance` 判定场景。
- 用户显式调用某个 `uth-*` 子 Skill 时，直接进入该子 Skill。
- 用户显式调用 `skill-creator` 时，让路给 `skill-creator`。
- 用户要求创建、修改或修补 Skill，但没有显式调用 `skill-creator` 时，停下来提醒用户显式调用。
- 如果没有工程动作信号，正常回答，不强行触发治理流程。
- 场景不明确时，停下来问一个澄清问题。
- 场景明确但需求、范围、方案或验收存在歧义时，由对应子 Skill 判断是否进入 `uth-sp-brainstorming`。

## 1. 开始前默认阅读顺序

1. `docs/README.md`
2. 本文件 `AGENTS.md`
3. `docs/current-state.md`
4. 当前任务明确指定的 Design / Todo / Feedback / 文件
5. 目标模块文档；模块位置从 `docs/context/README.md` 或 `docs/README.md` 的索引查找
6. 只有治理规则不清时，再读取 `docs/_governance/` 下对应规则文件

不要默认扫描整个 `docs/`，不要把旧 Design、旧 Feedback、旧 Run Log 当作当前事实。

## 2. 当前项目全局规则

本节只写跨模块、长期有效、每个新窗口都应知道的项目事实或硬约束。

### 2.1 【全局规则名称】

- 

### 2.2 【全局规则名称】

- 

## 3. 当前高频易错点

如果同一类跨模块误判重复出现两次及以上，把它补回本节。  
只属于单模块的事实，不回填到本文件，直接维护对应模块文档。

1. 

## 4. 模块细节应该去哪里找

按项目实际情况维护下列索引。复杂项目推荐按模块列出，简单项目可只保留前端 / 后端 / 文档 / 部署等入口。

- 项目概览：`docs/project-overview.md`
- 当前状态：`docs/current-state.md`
- 架构与模块边界：`docs/architecture.md`
- 本地启动、测试、构建：`docs/development.md`
- 模块上下文索引：`docs/context/README.md`
- 【模块 A】：
- 【模块 B】：

## 5. 新窗口开始开发时的最小动作

1. 先确认当前任务属于哪个场景，以及是否已有明确任务包 / Todo / LW Todo。
2. 先定位目标模块，再读该模块当前事实文档和必要代码。
3. 如果基线不清、问题跨模块或涉及历史追溯，先进入文档定位或读取 `docs/current-state.md` 指向的活跃任务包。
4. 修改代码前确认允许修改范围；越界文件必须先询问用户。
5. 修改完成后按对应场景 Skill 收口；代码改动的验证命令写在任务包、Todo 或项目验证入口里。

## 6. 文档维护代理规则

当任务是维护 `docs/` 文档体系，而不是实现代码或编写任务方案时：

1. 先判定变更属于哪一层，只改最少必要文件。
2. 检查模块私有内容是否被错误上浮到 `docs/README.md` 或本文件。
3. 检查同一段正文是否在多个层级重复；能引用就不要复述。
4. 更新 `docs/context/` 时，必须基于当前代码状态或用户指定的 git diff / git log 范围。
5. 修改 Markdown 后执行 UTF-8 / fence 检查。

## 7. 回填规则

只有以下内容可以回填到 `AGENTS.md`：

- 仓库级长期硬约束
- 每个新窗口都必须知道的当前主线
- 跨模块、重复出现两次以上的误判
- 新成员或新 Agent 进入仓库必须知道的最小动作

以下内容不要写进 `AGENTS.md`：

- 单次任务过程
- 临时结论
- 长模板
- 完整治理流程
- 模块私有事实
- 旧 Design / 旧 Feedback / 旧 Run Log 摘要

通用 Agent 行为规则写入 `docs/_governance/agent-rules.md`。  
文档写入规则写入 `docs/_governance/writing-rules.md`。  
当前事实索引写入 `docs/current-state.md` 和 `docs/context/`。
````

---

## 2. docs/README.md 模板

````md
# 项目文档入口

本文档目录分为六类：

## 1. 常驻上下文

- `current-state.md`：当前项目状态索引。
- `project-overview.md`：项目概览、技术栈、模块、非目标范围。
- `architecture.md`：当前架构、模块边界、调用关系。
- `development.md`：本地环境、启动、测试、构建。
- `context/`：模块级当前事实摘要，帮助 Agent 按需装载上下文。
- `api-contract.md`：API 契约，可选。
- `data-model.md`：数据模型，可选。
- `domain-glossary.md`：领域术语，可选。
- `ui-guidelines.md`：UI / UX 规则，可选。
- `deployment.md`：部署说明，可选。

## 2. 治理规则

- `_governance/`：Agent 规则、Git、Subagent、文档写入、状态维护、ADR / 发布、Hook 门禁等项目制度；不保存 `uth-*` skill 路由或执行说明。

## 3. 任务包

- `work/`：按任务包聚合 Design、Todo、Feedback、Prompt 和 Run Log。
- `LW-Work/`：轻量开发 Todo 和轻量 Git 提交记录，不替代正式任务包。
  该目录记录轻量开发约束和已提交轻量改动追溯信息，不是 current-state。

## 4. 状态快照

- `state/snapshots/`：历史状态快照。

## 5. 归档

- `archive/`：已明确完成且不再活跃的任务包和 LW 文档归档区，不作为当前事实源。
- `archive/work/`：正式任务包归档。
- `archive/LW-Work/`：轻量开发 Todo 和最终 LW 记录归档。

## 6. 长期记录

- `decisions/`：ADR 技术决策记录。
- `changelogs/`：正式版本变化记录。
````

---

## 3. docs/current-state.md 模板

````md
# 当前项目状态

更新时间：YYYY-MM-DD HH:mm

## 1. 当前阶段

- 阶段：

## 2. 当前活跃任务包

| 任务包 | 状态 | 说明 |
| --- | --- | --- |
| DYYMMDDXX-任务包标题 | 草案 / 已确认 / 执行中 / 已完成 / 阻塞 / 废弃 |  |

## 3. 当前活跃 Todo

| Todo | 状态 | 文件 |
| --- | --- | --- |
| DYYMMDDXX-T01 | 未开始 / 进行中 / 已完成 / 阻塞 / 放弃 | `docs/work/DYYMMDDXX-任务包标题/10-DYYMMDDXX-T01-todo-任务名.md` |

## 4. 当前阻塞项

- 无

## 5. 最近 3 条变化

- YYYY-MM-DD HH:mm：
- YYYY-MM-DD HH:mm：
- YYYY-MM-DD HH:mm：

## 6. 最近一次验证

| 时间 | 命令或方式 | 结果 | 说明 |
| --- | --- | --- | --- |
|  |  |  |  |

## 7. 下一步

- 

## 8. 当前事实来源

- `docs/project-overview.md`
- `docs/architecture.md`
- `docs/development.md`
- `docs/context/README.md`
- `docs/work/DYYMMDDXX-任务包标题/00-DYYMMDDXX-design.md`
````

---

## 4. docs/project-overview.md 模板

````md
# 项目概览

## 1. 项目名称

## 2. 一句话定位

本项目用于【解决什么问题】，面向【目标用户】，核心价值是【核心价值】。

## 3. 目标用户

- 用户 A：
- 用户 B：
- 管理员 / 运营 / 开发者：

## 4. 项目结构

```text
project-root/
├─ frontend/
├─ backend/
├─ docs/
└─ scripts/
```

说明：

- `frontend/`：
- `backend/`：
- `docs/`：
- `scripts/`：

## 5. 技术栈

Frontend:

- 

Backend:

- 

Database:

- 

Infrastructure / Tools:

- 

## 6. 启动命令

```bash
```

## 7. 构建命令

```bash
```

## 8. 测试命令

```bash
```

## 9. 功能模块列表

| 模块 | 当前状态 | 说明 |
| --- | --- | --- |
| 模块 A | 未开始 / 进行中 / 可用 |  |

## 10. 当前阶段

## 11. 非目标范围

当前阶段不做：

- 

## 12. 关键约束

- 
````

---

## 5. docs/architecture.md 模板

````md
# 架构说明

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
````

---

## 6. docs/development.md 模板

````md
# 开发运行手册

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
````

---

## 7. docs/context/README.md 模板

````md
# 模块上下文入口

`docs/context/` 保存模块级当前事实摘要，用于帮助 Agent 按需装载上下文。

本目录不是任务日志，不记录每次 diff，不复制 Feedback / worker Prompt / Run Log。

## 拆分原则

简单项目：

- `10-frontend.md`
- `20-backend.md`
- `30-data.md`
- `40-deployment.md`

复杂项目：

- 先由文档治理窗口理解全仓并提出拆分建议。
- 经用户确认后再创建模块上下文。
- 优先按业务 / 领域边界拆分，其次按运行时职责、架构层、协作边界和验证边界拆分。

## 文件说明

- `00-overview.md`：整体模块地图。
- `10-xxx.md`：具体模块当前事实。
- `90-cross-cutting.md`：跨模块约束、共享风险和共用验证入口。

## 使用原则

- 开发、Debug、Review 前按需读取相关模块文件。
- 如果只是定位代码位置，不需要默认读取全部 context。
- 旧任务包、Prompt、Run Log、LW 记录不能覆盖 context 中的当前事实。
- 模块文件应标明 Git baseline；如根据未提交工作区改动更新，可暂不写或不更新 baseline，并在收口说明。
````

---

## 8. docs/context/模块文件模板

文件：

```text
docs/context/10-模块名.md
```

模板：

````md
# 10-模块名

## 1. 职责

- 

## 2. 不负责

- 

## 3. 关键入口

- 

## 4. 关键依赖

- 

## 5. 常见修改点

- 

## 6. 验证入口

```bash
```

## 7. 当前风险

- 

## 8. Git Baseline

- Commit：
- Source：commit / git range / stable code / workspace changes
- Updated at：YYYY-MM-DD HH:mm

## 9. 相关任务包 / ADR

- 
````

---

## 9. docs/_governance/README.md 模板

````md
# 工程治理规则目录

本目录存放项目内工程治理规则。

本目录不保存 `uth-*` skill 的路由表、触发条件或执行流程。  
场景判断、上下文装载策略和收口协议由 `uth-governance` 与各子 Skill 自身负责。

## 文件说明

- `agent-rules.md`：Agent 行为细则和常见误判。
- `git-workflow.md`：Git、分支、PR、tag、release、锁规则。
- `subagent-workflow.md`：Main Agent / 子代理 / worktree 协作规则。
- `prompt-rules.md`：worker Prompt 落盘、命名和短提示词派发规则，可并入 `subagent-workflow.md`。
- `human-workflow.md`：项目 Owner 日常使用流程。
- `writing-rules.md`：Design / Todo / Feedback / Run Log 写入规则。
- `hook-gates.md`：L0-L3 门禁：场景、歧义、写入范围、Git、强验证、UTF-8、脚本守卫。
- `state-rules.md`：current-state 和 snapshots 维护规则。
- `adr-release-rules.md`：ADR、Changelog、版本号和发布规则。

## 使用原则

- Agent 不默认全读本目录。
- 只有当前场景需要对应制度时，才读取对应规则文件。
- 写入、派工、Git、完成声明和文档编码应通过 Hook 或等价门禁。
````

---

## 10. hook-gates.md 模板

````md
# Hook 门禁规则

Hook 是工程治理门禁，不是研发流程。  
Hook 只检查调用方提供的场景、范围、确认和验证事实，不定义 `uth-*` 的路由或执行流程。

## 1. 门禁结果

```text
PASS  放行
WARN  提醒并记录
ASK   暂停并请求用户确认
BLOCK 阻断
```

## 2. L0 Router Gate

- 项目动作前必须已有明确 `uth-*` 场景判定。
- 场景不明确时 `BLOCK`，交还调用方澄清。
- 无工程动作时不触发 UTH，不触发 UTH-SP。

## 3. L1 Process Gate

- 场景清楚但需求、范围、方案或验收有歧义时，必须提供已澄清、已 brainstorming 或明确豁免理由。
- 子场景必须给出 UTH-SP 触发判断；Hook 只检查判断事实是否存在，不展开方法流程。
- `worker` 派发前必须先写入完整 Prompt。
- `planner` / `evaluator` 只读，不记录 Prompt。
- 场景切换必须显式交接。

## 4. L2 Tool Gate

- 写入目标在当前场景允许范围内才放行。
- 超范围但非硬禁区，先问用户是否临时扩展范围。
- Git 写入必须进入 `uth-git` 并等待用户确认。
- 修改 `AGENTS.md`、根目录 `README.md`、`docs/**/*.md` 或任务包 Markdown 前后，必须通过 UTF-8 检查。
- 修改 `.sh`、`.js`、`.cjs`、`.mjs`、`.py`、`.ps1` 或带 shebang 的脚本时，必须检查 UTF-8、no-BOM 和 shebang；可用环境下运行语法检查，环境缺失时记录 WARN。

## 5. L3 Closeout Gate

- 声称完成、修复、通过、可交付前必须有新鲜证据。
- `uth-dev` / `uth-debug` 代码改动后必须编译 / 构建通过，且 `0 warning / 0 exception`。
- 经用户确认的 `uth-design` 小补丁同样触发代码强验证。
- 首次进入 UTH 代码修改场景时，不默认接受旧 warning / exception baseline；默认先清到 `0 / 0`。
- 确实清不掉且后续单独清理更合理时，先询问用户是否临时豁免；用户显式豁免后，不得声称完成、通过、可交付。
````

---

## 11. agent-rules.md 模板

````md
# Agent 行为规则

本文件记录通用 Agent 行为约束、跨场景误判和项目内长期协作规则。  
项目级当前主线、模块索引和仓库特有硬约束写入根 `AGENTS.md`；当前事实写入 `docs/current-state.md` 和 `docs/context/`。
本文件不记录 `uth-*` skill 的路由、触发条件或执行流程。

## 1. 总原则

- 默认少读少写。
- 任务范围不清时停下来问一个澄清问题。
- 不把其他场景动作带入当前场景。
- 不把旧 Design 当作当前事实。
- 不把 Prompt、Run Log、LW 记录当作当前事实。
- 不伪造测试、构建、验证结果。
- 代码改动默认要求编译 / 构建通过且 `0 warning / 0 exception`。
- 不在用户确认前执行 Git 写入。
- 修改 `AGENTS.md`、根目录 `README.md`、`docs/**/*.md` 或任务包 Markdown 前后，必须做 UTF-8 检查。
- 修改脚本时必须做 no-BOM / shebang 基础检查；语法工具不可用时记录 WARN，不得声称脚本验证通过。

## 2. 禁止跨场景加戏

- 只读分析不自动升级为文档治理。
- Debug 不自动升级为架构设计。
- 增量开发不自动升级为重构。
- Git 收口不自动修改业务代码。
- 文档治理不自动审查全仓代码。

## 3. 高频误判

### E001：把旧 Design 当当前事实

现象：

原因：

处理：

预防：

### E002：为了规范而写过多文档

现象：

原因：

处理：

预防：

### E003：把轻量改动强行升级成完整任务包

现象：

原因：

处理：

预防：

### E004：派发 worker 但未保存 Prompt

现象：

原因：

处理：

预防：

### E005：代码改动后跳过 0 warning / 0 exception 门槛

现象：

原因：

处理：

预防：

### E006：治理 Markdown 写回后乱码

现象：

原因：

处理：

预防：
````

---

## 12. git-workflow.md 模板

````md
# Git 工作流规则

## 1. 分支命名

- `main`：稳定主线。
- `feature/*`：新增功能或阶段能力。
- `fix/*`：修复明确问题。
- `docs/*`：文档。
- `chore/*`：工程配置、依赖、仓库维护。
- `refactor/*`：不改变行为的结构调整。
- `test/*`：测试补充。
- `spike/*`：探索验证，不保证合入。

## 2. PR 规则

- 第一次初始化仓库时，可以直接提交并推送 `main`，用于建立项目基线。
- 正式开发开始后，默认走 PR。
- PR 默认使用 squash merge。
- 正式版本 tag 只允许在 `main` 上创建。

## 3. Commit Message

采用 Conventional Commits：

```text
type(scope): summary
```

常用类型：

- `feat`
- `fix`
- `docs`
- `chore`
- `refactor`
- `test`
- `build`
- `ci`

## 4. Git Owner 锁

Git 写入前必须检查：

```text
.git-governance/lock.json
```

Git 写入包括：

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

## 5. Workspace Owner 锁

写文件或切分支前必须检查：

```text
.git-governance/workspace-lock.json
```

不创建 worktree 时，同一物理工作区只能有一个写入者。

## 6. 用户确认规则

Git 写入前必须展示：

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

用户确认后才能执行 Git 写入。

如果代码改动缺少编译 / 构建通过且 `0 warning / 0 exception` 的证据，默认不发布 release / tag。用户显式承担风险时可继续 commit，但必须记录风险。

## 7. 轻量 Git 记录

轻量改动不预先写 LW 记录。

流程：

1. `uth-dev` 创建轻量 Todo 并完成轻量改动。
2. 用户确认进入 `uth-git`。
3. `uth-git` 展示 Git 写入计划并等待确认。
4. commit 成功后，追加或创建 `docs/LW-Work/LWYYMMDDXX-轻量任务标题.md`。
5. LW 记录追加后如需纳入 Git，必须重新展示 diff 并等待用户确认。
````

---

## 13. subagent-workflow.md 模板

````md
# Subagent 协作规则

## 1. 核心原则

```text
主窗口负责上下文和收口。
子代理负责边界清晰的局部任务。
Git 写入只由获得用户确认的主窗口执行。
不创建 worktree 时，同一个物理工作区只能有一个写入者。
```

## 2. 什么时候使用 subagent

适合：

- 需要同时阅读多个模块。
- 前端、后端、文档、测试可以并行。
- 需要实现和审查分离。
- 单窗口上下文太大。
- 多个写入代理并行，且可以创建独立 worktree。

不适合：

- 简单文档修正。
- 单文件小改动。
- 任务目标还没有 Design / Todo。
- 主窗口还没弄清边界。
- 不创建 worktree 却希望多个 `worker` 同时改代码。

## 3. 默认角色

- Main Agent：上下文、派发、整合、验证、Feedback、current-state、Git 计划。
- planner：只读探索、方案拆分、上下文整理，不修改代码。
- worker：授权范围内实现，不执行 Git 写入。
- evaluator：只读验收，不修改代码和文档。

原则：

- 谁弄出的问题谁解决。
- 谁提出的问题谁验收。
- evaluator 发现问题时回传给主窗口，不直接修复。
- 子代理不得执行 Git 写入。
- worker Prompt 必须落盘到当前正式任务包 `prompts/`；planner / evaluator 不记录 Prompt。

## 4. Worker Prompt 派发流程

```text
1. 主窗口为每个 worker 写入完整 Prompt 文件；同一 worker 返工时追加更新原文件：
   docs/work/DYYMMDDXX-任务包标题/prompts/PYYMMDD-HHMM-T01-worker-任务名.md
2. 主窗口用短提示词派发 worker。
3. worker 读取 Prompt 文件并执行。
4. worker 按回传格式回复。
5. 主窗口负责整合、验证、Feedback、current-state 和 Git 建议。
```

规则：

- 有几个 worker，就写几份 Prompt。
- 同一 worker 返工时，返工要求追加到原 Prompt 文件，不另存新文件。
- planner / evaluator 不写 Prompt；其只读结论由主窗口在收口、Run Log 或 Feedback 中按需摘要。

短提示词：

```text
请读取并执行：
docs/work/DYYMMDDXX-任务包标题/prompts/PYYMMDD-HHMM-T01-worker-任务名.md

不得执行 Git 写入。完成后按文件里的回传格式回复。
```

## 5. 回传格式

```text
角色：
任务：
状态：完成 / 部分完成 / 阻塞 / 放弃

读取的 worker Prompt：

读取范围：
修改范围：

完成内容：
未完成内容：

验证：
编译/构建：
warning 数：
exception 数：
未验证：

风险：
需要主窗口处理：
```
````

---

## 14. writing-rules.md 模板

````md
# 文档写入规则

## 1. Design

Design 是任务包设计，不是长期事实。

文件位置：

```text
docs/work/DYYMMDDXX-任务包标题/00-DYYMMDDXX-design.md
```

## 2. Todo

Todo 是可执行工单，必须归属于某个 Design。

文件命名：

```text
10-DYYMMDDXX-T01-todo-任务名.md
20-DYYMMDDXX-T02-todo-任务名.md
```

## 3. Feedback

Feedback 是 Todo 的交付报告，不是过程日志。

Feedback 不强制记录 Git hash、PR 或 tag。Git 证据由 `uth-git` 收口记录；如果当时已经存在，可以在 Feedback 中作为可选链接补充。

文件命名：

```text
11-DYYMMDDXX-T01-feedback-任务名.md
21-DYYMMDDXX-T02-feedback-任务名.md
```

## 4. Run Log

Run Log 是过程记录，只在必要时写。

文件位置：

```text
docs/work/DYYMMDDXX-任务包标题/runs/RYYMMDD-HHMM-T01-执行记录.md
```

## 5. Worker Prompt

Prompt 是 worker 派发输入证据，不是当前事实源。

文件位置：

```text
docs/work/DYYMMDDXX-任务包标题/prompts/PYYMMDD-HHMM-T01-worker-任务名.md
```

凡派发 worker，完整 Prompt 必须先落盘。planner / evaluator 不记录 Prompt。  
同一 worker 返工时，追加更新原 Prompt 文件；多个 worker 才创建多份 Prompt。

## 6. LW-Work

LW-Work 是轻量开发文档和轻量 Git 提交记录，不替代正式任务包。

文件位置：

```text
docs/LW-Work/LWYYMMDDXX-轻量任务标题-todo.md
docs/LW-Work/LWYYMMDDXX-轻量任务标题.md
```

- 轻量 Todo 在开发前或首次写文件前创建。
- 最终 LW 记录只在轻量改动 commit 成功后追加或创建。
- 无 commit 不写最终 LW 记录。

## 7. Context

Context 是模块级当前事实摘要，不是任务日志。

文件位置：

```text
docs/context/
```

只在模块职责、入口、依赖、边界、验证方式或仍有效风险发生变化时更新。

模块 context 应标明 Git baseline：commit、来源和更新时间。  
如根据未提交工作区改动更新，可暂不写或不更新 baseline，并在收口说明。

## 8. 不写入原则

- 只读分析不写文件。
- 纯讨论不写文件。
- 简单问题不写长日志。
- 旧 Design 不作为当前事实。
- 未提交的轻量改动不写 LW 记录。
- 普通小改动不写 context，除非改变当前模块事实。
- 已归档任务和 LW 记录不作为当前事实源。
````

---

## 15. state-rules.md 模板

````md
# 状态维护规则

## 1. current-state 定位

`docs/current-state.md` 是当前状态索引，不是项目日志。

## 2. 内容上限

- 不超过 80-120 行。
- 最近变化最多 3 条。
- 最近验证最多 1 条。

## 3. 必须更新的情况

- Todo 完成。
- Todo 阻塞。
- 当前活跃任务包变化。
- 当前阶段变化。
- 关键阻塞变化。
- 最近一次验证结果影响下一步判断。

## 4. 不必更新的情况

- 只读分析。
- 纯讨论。
- 没形成任务状态变化的方案评估。
- 临时 Debug 过程中的每一步。
- 普通轻量改动的 LW 记录，除非影响当前阶段、阻塞、验证基线或发布判断。

## 5. snapshot

归档位置：

```text
docs/state/snapshots/SYYMMDD-说明.md
```

建议归档时机：

- 任务包完成。
- 阶段结束。
- 正式版本发布前。
- current-state 超过长度上限。
````

---

## 16. adr-release-rules.md 模板

````md
# ADR 与发布规则

## 1. ADR

ADR 只记录长期技术决策。

适合写 ADR：

- 技术栈选择或变更。
- 核心架构变化。
- 数据库模型重大变化。
- 接口契约策略变化。
- 部署方式变化。
- 长期影响后续开发的规则变化。

ADR 状态：

- Proposed
- Accepted
- Superseded
- Deprecated
- Rejected

ADR 是决策证据链，不是当前事实源。  
当前事实必须同步到常驻上下文文档。

## 2. Changelog

Changelog 只在正式版本发布时写。

规则：

- 一个正式 Git tag 必须对应一个 changelog。
- 一个 changelog 必须对应一个正式 Git tag。
- 没有 changelog 不打正式 tag。
- 普通开发 commit 不强制新增 changelog。

## 3. 版本号

采用 SemVer：

```text
vMAJOR.MINOR.PATCH
```
````

---

## 17. Design 模板

文件：

```text
docs/work/DYYMMDDXX-任务包标题/00-DYYMMDDXX-design.md
```

模板：

````md
# DYYMMDDXX：任务包标题

## 1. 基本信息

- 设计编号：DYYMMDDXX
- 标题：
- 创建日期：
- 状态：草案 / 已确认 / 执行中 / 已完成 / 阻塞 / 废弃

## 2. 背景

## 3. 目标

- 

## 4. 范围

本任务包包含：

- 

## 5. 不做什么

- 

## 6. 涉及模块

- 

## 7. 方案

说明整体方案，不写过细实现步骤。

## 8. 数据 / API / UI / 工作流影响

数据：

- 

API：

- 

UI：

- 

工作流：

- 

## 9. 验收口径

- [ ] 

## 10. Todo 拆分

| Todo 编号 | 标题 | 状态 | 文件 |
| --- | --- | --- | --- |
| DYYMMDDXX-T01 |  | 未开始 | `10-DYYMMDDXX-T01-todo-任务名.md` |

## 11. 风险点

- 

## 12. 相关 ADR

- 
````

---

## 18. Todo 模板

文件：

```text
docs/work/DYYMMDDXX-任务包标题/10-DYYMMDDXX-T01-todo-任务名.md
```

模板：

````md
# DYYMMDDXX-T01：任务名

## 1. 基本信息

- 所属任务包：DYYMMDDXX
- Todo 编号：DYYMMDDXX-T01
- 状态：未开始 / 进行中 / 已完成 / 阻塞 / 放弃
- 对应反馈：`11-DYYMMDDXX-T01-feedback-任务名.md`

## 2. 目标

- 

## 3. 范围

允许修改：

- 

禁止修改：

- 

## 4. 不做什么

- 

## 5. 开发 checklist

- [ ] 

## 6. 验收标准

- [ ] 

## 7. 基线要求

开始本 Todo 前，项目至少应满足：

- [ ] 后端可启动，或说明本 Todo 不涉及后端。
- [ ] 前端可启动，或说明本 Todo 不涉及前端。
- [ ] 当前主干无明显阻塞问题。
- [ ] 已知失败项已记录。
- [ ] 如基线不满足，本 Todo 本身就是修复该基线问题，或已获得用户确认继续。

## 8. 必跑验证

```bash
```

代码改动默认要求编译 / 构建通过且 `0 warning / 0 exception`。

## 9. 风险点

- 

## 10. 回滚方式

- 
````

---

## 19. Feedback 模板

文件：

```text
docs/work/DYYMMDDXX-任务包标题/11-DYYMMDDXX-T01-feedback-任务名.md
```

模板：

````md
# DYYMMDDXX-T01 开发反馈：任务名

## 1. 基本信息

- 对应任务包：DYYMMDDXX
- 对应 Todo：DYYMMDDXX-T01
- 执行日期：
- 当前状态：已完成 / 部分完成 / 阻塞 / 放弃

## 2. 完成内容

- 

## 3. 未完成内容

- 

## 4. 修改文件

- 

## 5. 关联 worker Prompts

- 无 / `docs/work/DYYMMDDXX-任务包标题/prompts/PYYMMDD-HHMM-T01-worker-任务名.md`

## 6. 验证命令和结果

| 命令或方式 | 结果 | warning | exception | 说明 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 7. 未验证项

- 

## 8. 风险与遗留问题

- 

## 9. 回滚方式

- 

## 10. 后续 Todo 建议

- 

## 11. Git / PR 建议

- 当前分支：
- 建议 commit message：
- 是否建议 PR：
- 是否建议 tag：
- 是否需要 changelog：
- Git 信息：未提交 / 已提交（可选；正式 Git 证据以 `uth-git` closeout 为准）
````

---

## 20. Run Log 模板

文件：

```text
docs/work/DYYMMDDXX-任务包标题/runs/RYYMMDD-HHMM-T01-执行记录.md
```

模板：

````md
# RYYMMDD-HHMM-T01 执行记录

## 1. 基本信息

- 时间：
- 场景：Debug / 验证 / 子代理执行 / 其他
- 关联 Todo：
- 关联 worker Prompt：
- 执行者：

## 2. 本次目标

- 

## 3. 执行过程摘要

- 

## 4. 关键日志 / 证据

```text
```

## 5. 结论

- 

## 6. 后续处理

- 
````

---

## 21. Worker Prompt 模板

文件：

```text
docs/work/DYYMMDDXX-任务包标题/prompts/PYYMMDD-HHMM-T01-worker-任务名.md
```

模板：

````md
# PYYMMDD-HHMM-T01 worker：任务名

## 1. 关联信息

- 任务包：DYYMMDDXX-任务包标题
- Todo：DYYMMDDXX-T01
- 角色：worker
- 创建时间：YYYY-MM-DD HH:mm
- 派发者：

## 2. 必读文件

- 

## 3. 默认不读

- 旧 Design
- 旧 Feedback
- 旧 Run Log
- 无关源码目录

## 4. 任务目标

- 

## 5. 允许修改

- 

## 6. 禁止修改

- 

## 7. 执行约束

- 不执行 Git 写入。
- 不扩大范围。
- 不引入新依赖，除非本 Prompt 明确允许。
- 遇到歧义或越界风险时停止并回传。
- 如果修改代码，回传编译 / 构建结果、warning 数和 exception 数。

## 8. 必跑验证

```bash
```

代码改动默认要求编译 / 构建通过且 `0 warning / 0 exception`。

## 9. 回传格式

- 读取的 worker Prompt：
- 读取范围：
- 修改范围：
- 完成内容：
- 未完成内容：
- 验证：
- 编译/构建：
- warning 数：
- exception 数：
- 未验证：
- 风险：
- 需要主窗口处理：

## 10. 返工追加记录

### Rework N - YYYY-MM-DD HH:mm

原因：

追加要求：

验证：

回传要求：
````

---

## 22. LW-Work 模板

轻量 Todo 文件：

```text
docs/LW-Work/LWYYMMDDXX-轻量任务标题-todo.md
```

模板：

````md
# LWYYMMDDXX Todo：轻量任务标题

## 1. 原始需求

用户原话：

> 

## 2. 场景判定

- 场景：uth-dev / light-dev
- 不创建正式任务包原因：
- UTH-SP 触发判断：

## 3. 目标

- 

## 4. 范围

允许修改：

- 

禁止修改：

- 

## 5. 验收方式

- 

## 6. 不做什么

- 
````

最终 LW 记录文件：

```text
docs/LW-Work/LWYYMMDDXX-轻量任务标题.md
```

模板：

````md
# LWYYMMDDXX：轻量任务标题

## 1. 原始需求

用户原话：

> 

## 2. 场景判定

- 场景：uth-dev / 轻量增量
- 未触发 UTH-SP 原因：
- 是否使用 subagent：否
- 关联正式任务包：无

## 3. 修改摘要

- 修改文件：
- 行为变化：
- 未涉及：

## 4. 验证

- 命令或方式：
- 结果：
- warning 数：
- exception 数：
- 未验证：

## 5. Git 信息

- 分支：
- commit：
- PR：
- tag：
````

---

## 23. ADR 模板

文件：

```text
docs/decisions/ADR-0001-中文标题.md
```

模板：

````md
# ADR-0001：中文标题

## 状态

Proposed / Accepted / Superseded / Deprecated / Rejected

## 日期

YYYY-MM-DD

## 背景

## 决策

## 理由

## 替代方案

## 影响

## 被谁替代

如果状态为 Superseded，填写新 ADR：
````

---

## 24. Changelog 模板

文件：

```text
docs/changelogs/v0.1.0.md
```

模板：

````md
# v0.1.0：版本标题

发布日期：YYYY-MM-DD

## 新增

- 

## 改进

- 

## 修复

- 

## 需要注意

- 
````

---

## 25. State Snapshot 模板

文件：

```text
docs/state/snapshots/SYYMMDD-说明.md
```

模板：

````md
# SYYMMDD：状态快照说明

## 1. 快照时间

YYYY-MM-DD HH:mm

## 2. 当前阶段

## 3. 已完成任务包

- 

## 4. 活跃任务包

- 

## 5. 阻塞项

- 

## 6. 最近验证结果

- 

## 7. 下一步

- 
````

---

## 26. Archive README 模板

文件：

```text
docs/archive/README.md
```

模板：

````md
# 文档归档

本目录保存已明确完成且不再活跃的任务包和轻量开发记录。

归档内容不是当前事实源；当前事实仍以 `docs/current-state.md`、`docs/context/` 和常驻上下文文档为准。

## 1. 目录

- `work/`：正式任务包归档。
- `LW-Work/`：轻量开发 Todo 和最终 LW 记录归档。

## 2. 归档规则

- 只归档已确认完成、废弃或被替代，且不再出现在 current-state 活跃索引中的内容。
- LW 归档时，`LW*-todo.md` 与 `LW*.md` 一起迁移；如只有 Todo，说明未提交或未生成最终记录。
- 归档后，如仍有当前事实价值，应先提炼到 `docs/context/` 或常驻上下文文件，而不是依赖归档文件。
````

## 27. Git 写入计划模板

````md
## Git 写入计划

当前分支：

## git status 摘要

```text
```

## diff 摘要

```text
```

## 计划执行命令

```bash
```

## 建议 commit message

```text
type(scope): summary
```

## PR / Changelog / Tag 判断

- 是否需要 PR：
- 是否需要 changelog：
- 是否需要 tag：
- 是否为轻量改动：
- commit 成功后是否追加 LW 记录：

## 锁状态

- Workspace Owner：
- Git Owner：

等待用户确认后再执行 Git 写入。
````
