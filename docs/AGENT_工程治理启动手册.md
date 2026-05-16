# AGENT 工程治理启动手册

> 版本定位：基于原 `docs/AGENT_工程治理启动手册.md` 优化。  
> 保留三层治理结构与 `Design -> Todo -> Feedback` 主线；优化目录组织、场景触发、状态文件膨胀、开发日志分片、ADR 事实边界，以及 `AGENTS.md` 的原生入口定位。

---

## 0. 当前核心变化

本治理包不推翻原有轻量工程治理，只做以下调整：

1. **规则集中**：Git、Agent、Subagent、人类流程、写入规则等集中到 `docs/_governance/`。
2. **任务聚合**：Design、Todo、Feedback 不再分散到三个顶层目录，改为按任务包聚合到 `docs/work/DYYMMDDXX-任务包标题/`。
3. **状态瘦身**：`docs/current-state.md` 只做当前状态索引，不做开发日志；历史状态归档到 `docs/state/snapshots/`。
4. **日志分片**：不再维护全局开发日志；过程记录按任务包写入 `runs/`。
5. **AGENTS.md 降噪**：`AGENTS.md` 只作为仓库级 Agent 原生入口文件，不承载完整治理手册和长模板。
6. **ADR 边界明确**：ADR 是决策证据链，不直接作为当前事实源；当前事实仍以常驻上下文文档为准。
7. **场景触发**：Agent 先判断场景，再按场景读取和写入，避免默认全读、默认全写。
8. **UTH Skill 分层**：`uth-governance` 负责顶层路由；各 `uth-*` 子 Skill 负责文档读写治理、场景内 UTH-SP 触发门槛和收口协议，不替代成熟研发流程。
9. **强流程门槛**：UTH-SP 不是随意触发；命中硬触发必须完整执行，只有满足明确豁免条件才走轻量路径。场景不清由 `uth-governance` 澄清；场景内需求、范围或验收不清时，再由子 Skill 判断是否进入 `uth-sp-brainstorming`。
10. **轻量记录**：轻量代码改动不默认创建正式任务包；任务完成时直接写 `docs/LW-Work/` 最终记录；如用户确认提交并完成 Git 写入，再由 `uth-git` 追加 Git baseline。
11. **Worker Prompt 留痕**：只有派发 `worker` 时，完整派发提示词必须先写入当前正式任务包 `prompts/`；同一 `worker` 返工时追加更新原 Prompt，不新建文件；有几个 `worker` 就记录几份。`planner` / `evaluator` 不记录 Prompt。
12. **文档定位 Skill**：文档定位作为独立辅助 Skill，用于追溯 Design / Todo / Feedback / worker Prompt / Run Log 证据链，不替代代码搜索和局部阅读。
13. **模块上下文层**：新增 `docs/context/` 保存模块级当前事实摘要，辅助 Agent 装载上下文；它不是任务日志，也不是 diff 流水。
14. **归档隔离**：已完成且不再活跃的任务包和 LW 文档迁移到 `docs/archive/`，不再污染 current-state 和 context。
15. **Context 来源**：模块 context 可标明来源证据，但不因等待 Git baseline 阻断文档报告；Git baseline 只在 `uth-git` 中追加到 LW final record 或正式 Feedback。
16. **场景不明即停**：顶层路由无法确定场景时，只问一个澄清问题，不为了开工而继续读文档或猜场景。
17. **Hook 门禁**：写入、派工、Git、完成声明和文档编码由 Hook 或等价门禁检查；门禁手册作为治理规则，不替代场景 Skill。
18. **代码强验证**：`uth-dev`、`uth-debug` 以及经用户确认的 `uth-design` 小补丁，代码改动后必须编译 / 构建通过且 `0 warning / 0 exception`；首次进入 UTH 代码修改场景时不默认接受旧告警基线。
19. **UTF-8 文档守卫**：修改 `docs/**/*.md`、根目录 `README.md`、`AGENTS.md` 或任务包 Markdown 时，调用 `uth-utf8-guard` 或等价检查，防止中文治理文档乱码。
20. **显式项目接管**：安装只负责全局 skills；项目初始化必须由用户显式调用 `uth-onboarding`，由 onboarding 将 Hook 工具复制到项目本地 `tools/uth-hooks/`，并写入 `.uth-governance/project.json`。
21. **静默机制**：当前项目根目录没有 `.uth-governance/project.json` 时，除 `uth-onboarding`、安装流程或用户显式 UTH 启用请求外，其他 `uth-*` 场景默认静默。

---

## 1. 治理目标

这套治理不是大而全的重型文档库，而是轻量、可执行、可持续维护的 Agent 工程治理体系。

它要让人类和 Agent 都能快速回答：

- 这个项目是什么？
- 当前做到哪一步？
- 当前任务属于哪个场景？
- 应该读哪些文件？
- 不应该读哪些文件？
- 这次需要写哪些文件？
- 哪些文档不能乱写？
- 做完以后怎么证明完成？
- 什么时候写 ADR、changelog、tag、PR？
- 什么时候需要 Git 写入确认？
- 什么时候触发 UTH-SP，什么时候允许轻量处理？
- 什么时候需要记录轻量 Git 改动或 worker Prompt？
- 什么时候必须被 Hook 阻断、询问或强验证？

核心原则：

```text
少读、少写、强触发、强收口。
```

---

## 2. 三层治理结构

当前规则继续保留原三层结构。

```text
1. 常驻上下文层：项目长期事实与当前状态
2. 任务流转层：Design -> Todo -> Feedback
3. 长期记录层：ADR、Changelog、Git 操作
```

### 2.1 常驻上下文层

用于描述当前项目事实。Agent 判断当前事实时，应优先读取这一层，而不是翻旧 Design、旧 Feedback 或旧 Run Log。

推荐文件：

```text
docs/current-state.md
docs/project-overview.md
docs/architecture.md
docs/development.md
docs/context/README.md
docs/context/*.md             # 按模块或技术边界维护
docs/api-contract.md          # 可选
docs/data-model.md            # 可选
docs/domain-glossary.md       # 可选
docs/ui-guidelines.md         # 可选
docs/deployment.md            # 可选
```

### 2.2 任务流转层

用于承载某个需求、阶段、功能包或修复包的完整闭环。

当前规则推荐按任务包聚合：

```text
docs/work/DYYMMDDXX-任务包标题/
├─ 00-DYYMMDDXX-design.md
├─ 10-DYYMMDDXX-T01-todo-任务名.md
├─ 11-DYYMMDDXX-T01-feedback-任务名.md
├─ 20-DYYMMDDXX-T02-todo-任务名.md
├─ 21-DYYMMDDXX-T02-feedback-任务名.md
├─ prompts/
│  └─ PYYMMDD-HHMM-T01-worker-任务名.md
└─ runs/
   └─ RYYMMDD-HHMM-T01-执行记录.md

docs/LW-Work/
└─ LWYYMMDDXX-轻量任务标题.md
```

`Design -> Todo -> Feedback` 主线不变，只是物理位置由三个分散目录改为一个任务包目录。

`prompts/` 保存 `worker` 完整派发输入，是执行证据，不是当前事实源；`planner` / `evaluator` 的只读提示词不落盘。

`LW-Work/` 保存轻量开发完成记录，不替代正式任务包。

### 2.3 长期记录层

用于记录长期影响、发布和版本。

推荐文件：

```text
docs/decisions/
docs/changelogs/
docs/_governance/git-workflow.md
docs/archive/                  # 已完成任务包和轻量记录的归档区
```

ADR 记录决策历史和理由，不直接取代当前事实文档。  
Changelog 只记录正式版本变化，不充当 commit log。  
Git 规则只在涉及分支、commit、PR、tag、release 时读取。
Archive 只保存已明确完成且不再活跃的任务包与 LW 记录，不作为当前事实源。

---

## 3. AGENTS.md 定位原则

`AGENTS.md` 遵循 Agent 原生入口文件定位，只保存仓库级、稳定、每次会话都需要的最小指令。

### 3.1 AGENTS.md 应该是什么

```text
AGENTS.md = repo-level agent instructions
```

它只保存：

- 仓库级长期硬约束。
- 每次进入仓库都必须知道的入口文件。
- 每次会话都必须遵守的禁止事项。
- 常用启动、测试、构建命令的索引。
- 场景判定入口。
- Git 写入前的确认要求。
- 重复出现两次以上的跨模块误判。

### 3.2 AGENTS.md 不应该是什么

`AGENTS.md` 不作为完整工程治理手册，不承载长模板，不记录任务过程，不保存历史设计，不展开完整场景流程。

以下内容不要塞进 `AGENTS.md`：

- 完整 Design 模板。
- 完整 Todo 模板。
- 完整 Feedback 模板。
- 完整 Git 治理细则。
- 完整 Subagent 角色百科。
- 单次任务过程。
- 临时结论。
- 旧 Design / 旧 Feedback / 旧 Run Log 的摘要。
- 大段工程治理理念。

### 3.3 AGENTS.md 与其他文件的边界

```text
.uth-governance/project.json
  项目级 UTH 启用标记。

AGENTS.md
  仓库级 Agent 最小入口。

docs/_governance/
  项目内治理规则库。

docs/_governance/hook-gates.md
  写入、派工、Git、收口和文档编码门禁规则。

tools/uth-hooks/
  项目本地 Hook runner 与 L0/L1/L2/L3 门禁脚本。

skills/
  场景触发与流程执行协议。

docs/current-state.md
  当前状态事实索引。

docs/context/
  模块级当前事实摘要。

docs/work/
  任务包、Design、Todo、Feedback、Prompt、Run Log、轻量 Git 记录。

docs/decisions/
  ADR 决策证据链。

docs/changelogs/
  正式版本变化记录。
```

### 3.4 Claude Code 兼容

如果使用 Claude Code，可以将同等内容写入 `CLAUDE.md`。  
原则相同：短、稳定、可执行，不承载完整治理流程和长模板。

---

## 4. 推荐目录结构

新项目建议建立：

```text
.uth-governance/
└─ project.json

AGENTS.md
README.md

tools/
└─ uth-hooks/

docs/
├─ README.md
├─ current-state.md
├─ project-overview.md
├─ architecture.md
├─ development.md
├─ context/
│  ├─ README.md
│  ├─ 00-overview.md
│  ├─ 10-frontend.md
│  ├─ 20-backend.md
│  └─ 90-cross-cutting.md
├─ api-contract.md              # 可选
├─ data-model.md                # 可选
├─ domain-glossary.md           # 可选
├─ ui-guidelines.md             # 可选
├─ deployment.md                # 可选
│
├─ _governance/
│  ├─ README.md
│  ├─ agent-rules.md
│  ├─ git-workflow.md
│  ├─ subagent-workflow.md
│  ├─ human-workflow.md
│  ├─ writing-rules.md
│  ├─ hook-gates.md
│  ├─ prompt-rules.md              # 可选，可并入 subagent-workflow.md
│  ├─ state-rules.md
│  └─ adr-release-rules.md
│
├─ work/
│  ├─ D26051401-任务包标题/
│  │  ├─ 00-D26051401-design.md
│  │  ├─ 10-D26051401-T01-todo-任务名.md
│  │  ├─ 11-D26051401-T01-feedback-任务名.md
│  │  ├─ 20-D26051401-T02-todo-任务名.md
│  │  ├─ 21-D26051401-T02-feedback-任务名.md
│  │  ├─ prompts/
│  │  │  └─ P260514-1530-T01-worker-实现某功能.md
│  │  └─ runs/
│  │     └─ R260514-1530-T01-执行记录.md
│
├─ LW-Work/
│  └─ LW26051401-add-button.md
│
├─ snapshots/
│  └─ ONB26051401-existing-project-handoff.md
│
├─ state/
│  └─ snapshots/
│     └─ S260514-D26051401阶段状态.md
│
├─ archive/
│  ├─ work/
│  │  └─ D26051401-任务包标题/
│  └─ LW-Work/
│     └─ LW26051401-add-button.md
│
├─ decisions/
│  ├─ README.md
│  └─ ADR-0001-中文标题.md
│
└─ changelogs/
   └─ v0.1.0.md
```

---

## 5. 文件职责边界

### 5.1 根目录

| 文件 | 职责 |
| --- | --- |
| `.uth-governance/project.json` | 当前项目已接入并启用 UTH 的项目级标记 |
| `AGENTS.md` | 仓库级 Agent 最小入口指令 |
| `README.md` | 项目对外或人类入口说明 |

### 5.2 `docs/` 常驻上下文

| 文件 | 职责 |
| --- | --- |
| `docs/README.md` | 文档索引，告诉人和 Agent 文档怎么找 |
| `docs/current-state.md` | 当前状态索引，只保留最新活跃事实 |
| `docs/project-overview.md` | 项目概览、目标用户、模块、非目标范围 |
| `docs/architecture.md` | 当前架构、模块职责、调用边界 |
| `docs/development.md` | 环境、启动、测试、构建、本地问题 |
| `docs/context/` | 模块级当前事实摘要，帮助 Agent 按需装载上下文 |
| `docs/snapshots/` | 项目级快照，例如老项目接管 handoff |
| `docs/api-contract.md` | 当前 API 契约 |
| `docs/data-model.md` | 当前数据模型 |
| `docs/domain-glossary.md` | 当前领域术语 |
| `docs/ui-guidelines.md` | 当前 UI / UX 规则 |
| `docs/deployment.md` | 当前部署与回滚方式 |

`docs/context/` 的定位：

- 保存当前仍有效的模块事实。
- 帮助 Agent 在开发、Debug、Review 前快速理解相关模块。
- 简单项目可按 `frontend` / `backend` / `data` / `deployment` 拆分。
- 复杂项目应先由文档治理窗口理解全仓后提出拆分建议，经用户确认后再创建。
- 不记录开发流水、Prompt 原文、Feedback 全文或过期 TODO。

### 5.3 `docs/_governance/`

| 文件 | 职责 |
| --- | --- |
| `agent-rules.md` | Agent 行为细则和常见误判 |
| `git-workflow.md` | 分支、PR、commit、tag、Git Owner、Workspace Owner |
| `subagent-workflow.md` | Main Agent / 子代理 / worktree 协作规则 |
| `human-workflow.md` | 项目 Owner 日常使用流程 |
| `writing-rules.md` | Design / Todo / Feedback / Run Log 写入规则 |
| `hook-gates.md` | L0-L3 门禁：场景、歧义、写入范围、Git、强验证、UTF-8、脚本守卫 |
| `prompt-rules.md` | worker Prompt 落盘、命名和短提示词派发规则，可并入 `subagent-workflow.md` |
| `state-rules.md` | current-state 和 snapshots 维护规则 |
| `adr-release-rules.md` | ADR、Changelog、版本号和发布规则 |

`docs/_governance/` 不保存 `uth-*` skill 的路由表、触发条件或执行流程。  
场景判断、上下文装载策略和收口协议由 `uth-governance` 与各子 Skill 自身负责。

### 5.4 `docs/work/`

`docs/work/` 存放任务包。每个任务包对应一个阶段目标、功能闭环、修复包或设计包。

规则：

- 一个任务包必须有一个 `00-DYYMMDDXX-design.md`。
- Todo 必须归属于某个任务包。
- Feedback 必须归属于某个 Todo。
- 派发 `worker` 时，完整 Prompt 必须归属于当前正式任务包的 `prompts/`；`planner` / `evaluator` 不记录 Prompt。
- Run Log 是过程记录，不是交付报告。
- 已完成或废弃任务包默认不作为当前事实来源。

`docs/LW-Work/` 存放轻量开发最终记录。

规则：

- 轻量改动不创建单独 LW Todo。
- 轻量改动完成并验证后，创建或更新最终 LW 记录。
- LW 记录保存用户原始需求、任务边界、修改摘要、验证摘要、风险和回滚方式。
- Git 写入成功后，由 `uth-git` 向该 LW 记录追加 Git baseline。
- LW 记录不进入 `current-state`，除非它影响当前阶段、阻塞、验证基线或发布判断。
- LW 记录不是正式 Design / Todo / Feedback，不用于承载复杂任务过程。

### 5.5 `docs/state/`

`docs/state/snapshots/` 存放历史状态快照。

规则：

- `docs/current-state.md` 只保留当前状态。
- 任务包完成时可生成 snapshot。
- 正式版本发布前可生成 snapshot。
- current-state 超长时必须归档旧内容到 snapshot。

### 5.6 `docs/archive/`

`docs/archive/` 存放已明确完成且不再活跃的任务包和 LW 文档。

规则：

- 正式任务包归档到 `docs/archive/work/`。
- 轻量开发最终 LW 记录归档到 `docs/archive/LW-Work/`。
- 归档文件不是当前事实源。
- 归档前必须确认 current-state 不再把对应文档列为活跃项。

### 5.7 `docs/decisions/`

ADR 存放长期技术决策历史。

规则：

- ADR 是决策证据，不是当前事实源。
- 当前事实应同步到常驻上下文文档。
- 技术选型变更时新增 ADR，而不是直接篡改旧 ADR。
- 被替代的 ADR 应标记为 `Superseded` 或 `Deprecated`。

### 5.8 `docs/changelogs/`

Changelog 只记录正式版本变化。

规则：

- 一个正式 Git tag 必须对应一个 changelog。
- 一个 changelog 必须对应一个正式 Git tag。
- 普通开发 commit 不写 changelog。
- Changelog 面向用户，不写过多技术细节。

---

## 6. 场景触发机制

Agent 收到任务后，第一步不是读取全量文档，而是先判断场景。

### 6.1 顶层路由

已接入 UTH 的项目或仓库会话开始时，先进入 `uth-governance` 做轻量场景判断。

`uth-governance` 只做路由，不执行具体研发流程。

静默机制：

```text
当前项目根目录没有 .uth-governance/project.json 时，
除 uth-onboarding / 安装流程 / 用户显式 UTH 启用请求外，
其他 uth-* 场景默认静默。
```

`.uth-governance/project.json` 只表示当前项目已经被 UTH 接管并启用。安装是全局状态，不是项目状态。

分层判断：

1. 用户显式调用 `skill-creator` 时，让路给 `skill-creator`。
2. 用户显式调用 `uth-onboarding`，或明确要求启用 / 接管 UTH 时，进入 `uth-onboarding`。
3. 当前项目没有 `.uth-governance/project.json`，且用户没有显式 UTH 启用请求时，不触发其他 `uth-*` 子 Skill。
4. 用户显式指定某个 `uth-*` 子 Skill 时，直接进入该子 Skill。
5. 没有工程动作信号，且没有任何 UTH 场景命中时，正常回答，不触发子 Skill。
6. 只有一个 UTH 场景命中时，输出一行简短判定并直接进入子 Skill。
7. 多场景命中时，选择第一个执行场景，后续场景留到收口时交接。
8. 场景仍不明确时，停下来问一个澄清问题。

场景不明确时，不默认开工、不默认只读分析、不继续读更多文档来硬凑场景。

纯闲聊、简单解释或无工程动作请求，不输出场景判定表，不触发 UTH-SP。

`skill-creator` 规则：

- UTH 不维护或修改 `skills/`。
- 创建、修改或修补 Skill 时，由用户显式调用 `skill-creator`。
- 用户未显式调用 `skill-creator` 却要求修改 Skill 时，停下来提醒用户显式调用。

如果用户明确要求只读分析或方案评估，则进入 S1。

S1 意味着：

- 不改代码。
- 不改文档。
- 不执行 Git 写入。
- 只输出分析、建议、风险和下一步。

如果主场景已明确，但需求、范围、验收口径或方案存在歧义，由对应子 Skill 判断是否进入 `uth-sp-brainstorming`。

### 6.2 主场景

推荐场景：

```text
S0 项目接入 / UTH 启用
S1 只读分析 / 方案评估
S2 架构设计 / 技术决策
S3 增量开发
S4 Debug / 故障修复
S5 重构 / 结构调整
S6 验证 / Review / 验收
S7 Git / PR / 发布收口
S8 文档治理 / 规范维护
辅助场景：文档定位 / 证据追踪
```

UTH Skill 推荐映射：

```text
uth-governance    -> 顶层场景路由 / 防跨场景加戏
uth-onboarding    -> S0 显式项目接入 / UTH 启用
uth-design        -> S1 方案评估 / S2 架构设计
uth-debug         -> S4 Debug / 故障修复
uth-review        -> S6 验证 / Review / 验收
uth-dev           -> S3 增量开发
uth-docs          -> S8 单开文档治理 / 规范维护
uth-git           -> S7 Git / PR / 发布收口
uth-context-trace -> 辅助定位文档证据链
uth-utf8-guard    -> 文档写入编码守卫
```

`uth-governance` 只负责场景判断、最小读取和路由。  
各子 `uth-*` 负责场景触发、文档装载、UTH-SP 触发门槛、执行边界和文档收口。  
具体研发方法如果由 UTH-SP 覆盖，命中触发条件后应完整执行对应 UTH-SP 流程。

### 6.3 场景判定输出

场景判定的用户可见输出格式由 `uth-governance` Skill 内置维护。  
启动手册和项目 docs 不再保存场景判定模板，避免形成第二事实源。

如果用户只是闲聊、简单解释或无工程动作请求，不输出场景判定。

### 6.4 UTH-SP 触发门槛

UTH 不替代 UTH-SP 方法 Skill，只优化触发条件和文档治理边界。

`uth-governance` 不直接调用 UTH-SP；它只负责路由。  
UTH-SP 是否触发，由进入的子 Skill 按场景判断。  
原始自动触发层应禁用或让路；项目内只调用 `skills/uth-sp-*`。

原则：

- 命中硬触发时，必须完整执行对应 UTH-SP 方法 Skill。
- 只有全部满足明确豁免条件，才允许走轻量路径。
- 场景已确定后，需求、范围、方案或验收判断不清时，由子 Skill 判断是否进入 `uth-sp-brainstorming`。
- 用户说“简单改一下”不能覆盖硬触发。
- 不触发 UTH-SP 时，必须说明不触发理由。

常见映射：

| UTH-SP | 硬触发 | 允许豁免 |
| --- | --- | --- |
| `uth-sp-brainstorming` | 任一场景出现需求、范围、方案、验收歧义 | 目标、范围、验收和影响面都明确 |
| `uth-sp-systematic-debugging` | 原因未知的报错、失败、异常、白屏、测试/构建失败 | 用户已明确根因和修复点，且只需最小改动 |
| `uth-sp-test-driven-development` | 业务逻辑、API、权限、状态机、核心流程、回归 bug | 纯样式、文案、无新行为的小 UI 调整 |
| `uth-sp-subagent-driven-development` | 正式增量开发需要子代理实现 | 超轻量改动由主窗口直接完成 |
| `uth-sp-verification-before-completion` | 要声称完成、修复、通过、可交付 | 只读分析或明确未交付 |
| `uth-sp-finishing-a-development-branch` | PR、merge、release、tag、分支收口 | 仅输出 Git 建议，不执行 Git 写入 |

### 6.5 Hook 门禁

Hook 是流程门禁，不是新研发流程。  
完整规则放在 `docs/_governance/hook-gates.md`；本仓库分发版可参考 `docs/HOOKS_工程治理门禁手册.md`。

建议按四层实现：

```text
L0 Router Gate：先判场景，场景不明即停。
L1 Process Gate：歧义是否 brainstorming、UTH-SP 触发判断、是否允许场景切换、worker Prompt 是否落盘。
L2 Tool Gate：文件写入范围、Git 写入确认、UTF-8 文档守卫、脚本 no-BOM / 语法守卫。
L3 Closeout Gate：分场景收口、强验证、完成声明证据。
```

门禁结果：

```text
PASS / WARN / ASK / BLOCK
```

强治理默认：

- `uth-dev` / `uth-debug` 代码改动后必须编译 / 构建通过，且 `0 warning / 0 exception`。
- 经用户确认的 `uth-design` 小补丁同样触发代码强验证。
- 首次进入 UTH 代码修改场景时，如果项目已有 warning / exception，默认先清到 `0 / 0`；如果确实清不掉、后续单独清理更合理，先询问用户是否临时豁免。
- 有豁免时，不得声称完成、通过、可交付；Git / release 继续阻断，除非用户明确承担风险。
- 修改治理文档、任务包 Markdown、根目录 `README.md` 或 `AGENTS.md` 时，调用 `uth-utf8-guard` 或等价检查。
- 修改脚本文件时，至少检查 UTF-8、no-BOM 和 shebang；可用环境下运行对应语法检查，环境缺失时记录 WARN，不伪装为通过。

### 6.6 Git 收口交接判断

Git 收口交接判断以人类验收口径触发，而不是以 Agent Todo 自证口径触发。

规则：

- `uth-dev`：轻量任务实现和验证完成后必须判断是否建议 Git 收口；正式任务包只有达到 Design 级人类验收口径时才判断，单个 Todo 完成只写 Feedback、current-state 或继续下一个 Todo。
- `uth-debug`：只读诊断不触发；独立轻量修复完成并验证后必须判断；正式任务包内修复按 Design 级人类验收口径判断。
- `uth-docs` / `uth-design`：由 Agent 判断是否形成稳定、可提交的治理或设计成果。
- `uth-review` / `uth-context-trace`：默认不触发，除非用户显式要求 Git 动作。
- 进入 `uth-git` 必须先询问用户；进入 `uth-git` 后，任何 Git 写入仍必须展示计划并等待用户确认。

### 6.7 文档定位辅助场景

文档定位用于查找相关 Design / Todo / Feedback / worker Prompt / Run Log / LW 记录，包括必要时查找已归档证据。

适合：

- Debug 需要还原问题引入链路。
- Review 需要追溯任务边界或子代理派发输入。
- 用户明确询问“这个需求/问题对应哪个文档”。
- 用户明确询问已归档任务包、旧 LW 记录或历史证据。
- 实现和文档冲突，需要区分当前事实与历史证据。

不适合：

- 只是定位代码位置。
- 已知目标文件和改动范围的小改动。
- 为了“规范”默认翻旧任务包。
- 为了“保险”默认扫描 `docs/archive/`。

归档读取规则：

- `docs/archive/` 默认不读。
- 只有用户明确要求历史证据、已知任务 / LW 已归档、当前文档指向归档，或活跃区找不到且归档是唯一窄范围下一步时才读。
- 归档文件只作历史证据，不覆盖 `docs/current-state.md`、`docs/context/` 或常驻上下文中的当前事实。

文档定位输出：

```text
关联任务包：
归档位置：
关联 LW 记录：
关联 Design：
关联 Todo：
关联 Feedback：
关联 worker Prompt：
关联 Run Log：
证据链摘要：
当前事实来源：
仅作历史证据的文件：
```

---

## 7. 场景读写规则

### 7.1 S0 项目接入 / UTH 启用

触发：

- 新项目初始化。
- 老项目接管。
- 用户显式调用 `uth-onboarding`。
- 用户明确要求“在当前项目启用 UTH / 接管这个项目 / 初始化 UTH 文档体系”。

默认读取：

```text
AGENTS.md
README.md
项目目录结构
已有 README / 配置 / 构建脚本 / 测试目录
```

允许写入：

```text
.uth-governance/project.json
tools/uth-hooks/
AGENTS.md
docs/README.md
docs/current-state.md
docs/project-overview.md
docs/architecture.md
docs/development.md
docs/context/README.md
docs/work/README.md
docs/LW-Work/README.md
docs/snapshots/
docs/_governance/
docs/archive/
docs/decisions/README.md
docs/changelogs/README.md
```

禁止：

- 不修改业务代码。
- 不伪造启动、测试、构建结果。
- 不把空模板当成已完成治理。
- 不读取全量源码来假装完成项目理解。
- 不在安装流程里顺手初始化当前目录。

收口：

- 输出新增文件、修改文件、备份、快照、项目标记、未确认事实和后续场景。
- 老项目接管完成后自动接上 `uth-docs`。
- 不执行 Git 写入。

### 7.2 S1 只读分析 / 方案评估

触发：

- “帮我看看”
- “评估一下”
- “有没有矛盾”
- “这个方案怎么样”
- “先别改”
- 用户明确要求只读分析或方案评估

场景不明确不自动归入 S1；由 `uth-governance` 停下来问一个澄清问题。

默认读取：

```text
AGENTS.md
docs/current-state.md
用户指定文件
```

按需读取：

```text
docs/project-overview.md
docs/architecture.md
当前任务包 Design / Todo
```

如果评估过程中出现目标、范围、方案或验收歧义，进入 `uth-sp-brainstorming`。  
如果只是在比较已有方案，不写 Design、不进入实现。

禁止写入：

- 不改代码。
- 不改文档。
- 不执行 Git 写入。
- 不主动补全治理体系。

收口：

- 输出结论、风险、建议。
- 如需进入开发，建议切换到 S2 / S3 / S4 / S5。

### 7.3 S2 架构设计 / 技术决策

触发：

- 新模块设计。
- 技术选型。
- 核心架构变化。
- 数据模型重大变化。
- 接口策略变化。
- Agent workflow 设计。

默认读取：

```text
AGENTS.md
docs/current-state.md
docs/project-overview.md
docs/architecture.md
```

按需读取：

```text
docs/development.md
docs/api-contract.md
docs/data-model.md
docs/domain-glossary.md
docs/decisions/
```

UTH-SP：

- 方案、范围、权衡或验收口径存在歧义时，必须进入 `uth-sp-brainstorming`。
- Design 已确认且需要拆成多步实施时，可进入 `uth-sp-writing-plans`。

允许写入：

```text
docs/work/DYYMMDDXX-任务包标题/00-DYYMMDDXX-design.md
docs/decisions/ADR-XXXX-中文标题.md     # 如涉及长期决策
docs/current-state.md                  # 只更新当前活跃设计索引
```

禁止：

- 不直接实现业务代码；如设计中发现小型逻辑错误，只能在用户确认后做少量 design-assisted patch，并触发编译 / 构建强验证。
- 不把 Design 当作长期事实终点。
- 不写 Todo；Todo 拆分归 S3 / `uth-dev`。
- 不写 Feedback，除非已有 Todo 被执行。
- 不写 Changelog，除非进入发布收口。

收口：

- 明确目标、范围、不做什么、模块边界、影响范围、验收口径。
- 如果准备开发，交给 S3 / `uth-dev` 拆 Todo 或实现。

### 7.4 S3 增量开发

触发：

- 新增接口。
- 新增页面。
- 新增小功能。
- 实现某个 Todo。
- 补字段、补模块能力。

默认读取：

```text
AGENTS.md
docs/current-state.md
当前任务包 00-design
当前 Todo
```

轻量改动如果没有当前正式任务包，可只读取 `AGENTS.md`、`docs/current-state.md` 和相关代码/局部文档。  
轻量改动不默认调用文档定位；定位代码位置用代码搜索和局部阅读，只有需要追溯历史任务证据链时才调用文档定位。

涉及代码修改时读取：

```text
docs/_governance/git-workflow.md
```

按需读取：

```text
改 API -> docs/api-contract.md
改数据模型 -> docs/data-model.md
改 UI -> docs/ui-guidelines.md
改部署 -> docs/deployment.md
```

必须写入：

```text
当前 Todo 对应 Feedback
docs/current-state.md
```

上述“必须写入”只适用于正式任务包内的增量开发。

轻量改动规则：

- 不要求创建正式 Design / Todo / Feedback。
- 不创建单独 LW Todo。
- 完成并验证后，创建或更新最终 LW 记录：`docs/LW-Work/LWYYMMDDXX-轻量任务标题.md`。
- 最终 LW 记录写用户原始需求、任务边界、修改摘要、验证摘要、未验证项、风险和回滚方式。
- 无 commit 也要写最终 LW 记录；Git baseline 先标记为 `pending uth-git`。
- LW 记录默认不更新 `docs/current-state.md`，除非影响当前阶段、阻塞、验证基线或发布判断。

Subagent 规则：

- 正式增量开发可使用 subagent；使用 subagent 时必须挂到正式任务包。
- `worker` 负责实现。
- `planner` 负责只读探索、方案拆分和上下文整理。
- `evaluator` 负责只读验收，不修改代码和文档。
- 谁弄出的问题谁解决，谁提出的问题谁验收。
- 凡派发 `worker`，完整 Prompt 必须先写入当前任务包 `prompts/`，再用短提示词让 worker 读取；同一 worker 返工时追加更新原 Prompt，不新建文件。`planner` / `evaluator` 不写 Prompt。

强验证规则：

- 代码改动后必须运行项目编译 / 构建命令。
- 收口要求编译 / 构建通过，且 `0 warning / 0 exception`。
- 首次进入 UTH 代码修改场景时，如已有 warning / exception，默认先清理到 `0 / 0`；如果确实清不掉、后续单独清理更合理，先询问用户是否临时豁免。
- 豁免后不得声称完成、通过、可交付。

文档守卫：

- 写 LW final record、Feedback、Prompt、Run Log、current-state 等 Markdown 前后，调用 `uth-utf8-guard` 或等价检查。

按需写入：

```text
docs/api-contract.md
docs/data-model.md
docs/ui-guidelines.md
docs/development.md
```

禁止：

- 不跳过 Todo 直接开发业务功能。
- 不把轻量改动扩展成无边界开发。
- 不顺手重构无关模块。
- 不静默引入依赖。
- 不把未验证内容写成已验证。
- 不执行 Git 写入，除非进入 S7 并获得确认。

收口：

- 正式任务包：写 Feedback，更新 current-state。
- 轻量改动：写最终 LW 记录，说明修改、验证和未验证项；如用户确认进入 `uth-git` 且 Git 写入成功，由 `uth-git` 追加 Git baseline。
- 代码改动：列出编译 / 构建命令、结果、warning 数、exception 数。
- 输出 Git / PR 建议。

### 7.5 S4 Debug / 故障修复

触发：

- 报错。
- 启动失败。
- 测试失败。
- 构建失败。
- 页面白屏。
- 接口异常。
- 线上或本地故障。

默认读取：

```text
AGENTS.md
docs/current-state.md
docs/development.md
错误日志 / 复现步骤
```

按需读取：

```text
docs/architecture.md
相关代码
相关 Todo / Feedback
docs/work/*/runs/ 中相关近期记录
```

按需追溯开发上下文：

```text
当前任务包 Design
导致 bug 的 Todo
对应 Feedback
相关 prompts/
相关 runs/
相关 LW-Work 记录
```

这些文件用于还原问题引入链路，不直接作为当前事实源。  
如果需要查找这些文件，先进入文档定位辅助场景。

强验证规则：

- 修复代码后必须运行项目编译 / 构建命令。
- 收口要求编译 / 构建通过，且 `0 warning / 0 exception`。
- 首次进入 UTH 代码修改场景时，如已有 warning / exception，默认先清理到 `0 / 0`，除非用户显式豁免。
- 豁免后不得声称 fixed / passing / complete。

允许写入：

- 小修：更新 current-state 的最近变化即可。
- 明确任务修复：写 Todo + Feedback。
- 过程追踪：写当前任务包下的 `runs/`。

禁止：

- 不默认新建架构 Design。
- 不把 Debug 扩大成重构。
- 不顺手改无关问题。
- 不执行 Git 写入，除非进入 S7。

收口：

- 说明根因。
- 说明修改范围。
- 说明验证命令和结果，包括编译 / 构建、warning 数、exception 数。
- 说明未验证项。
- 说明风险和回滚方式。
- 如读取了 Design / Todo / Feedback / worker Prompt / Run Log / LW 记录，说明证据链和当前事实来源。

### 7.6 S5 重构 / 结构调整

触发：

- 拆模块。
- 调整目录。
- 抽组件。
- 清理重复代码。
- 优化调用边界。
- 不改变业务行为的结构调整。

默认读取：

```text
AGENTS.md
docs/current-state.md
docs/architecture.md
相关代码
```

涉及代码修改时读取：

```text
docs/_governance/git-workflow.md
```

必须写入：

- 小重构：Todo + Feedback + current-state。
- 架构级重构：Design + Todo + Feedback + current-state + 必要 ADR。

禁止：

- 不改变业务行为，除非明确切换到 S3。
- 不无关扩大范围。
- 不把“重构”当成重写项目。
- 不跳过验证。

收口：

- 说明行为是否保持不变。
- 说明影响范围。
- 运行回归验证。
- 写清回滚方式。

### 7.7 S6 验证 / Review / 验收

触发：

- 代码审查。
- 跑测试。
- 验收 Todo。
- 检查是否可交付。
- 对比验收标准。

默认读取：

```text
AGENTS.md
docs/current-state.md
当前 Todo
修改 diff
```

按需读取：

```text
当前 Design
docs/architecture.md
docs/development.md
```

按需读取文档定位结果：

```text
相关 Design / Todo / Feedback / worker Prompt / Run Log / LW 记录
```

这些文件用于判断任务边界、派发输入和交付证据，不直接覆盖当前事实。

代码验收门槛：

- 如果验收对象包含代码改动，正向验收必须有新鲜编译 / 构建证据。
- 收口要求编译 / 构建通过，且 `0 warning / 0 exception`。
- 缺少该证据时，只能标记为 static-review-only、pass with risk 或 needs follow-up，不得声称可交付。

默认禁止写入：

- 不改代码。
- 不改文档。
- 不执行 Git 写入。

例外：

- 如果用户要求“补交付反馈”，可补 Feedback。
- 如果作为 Todo 收口，可更新 current-state。

收口：

- 阻塞问题。
- 非阻塞问题。
- 缺失验证。
- 是否建议通过。
- 剩余风险。
- 如涉及 worker 交付，说明关联 worker Prompt 和 evaluator 验收结论。

### 7.8 S7 Git / PR / 发布收口

触发：

- commit。
- push。
- branch。
- PR。
- tag。
- release。
- merge / rebase。
- 删除分支。
- 删除 worktree。

必须读取：

```text
docs/_governance/git-workflow.md
```

必须展示：

```text
当前分支
git status
diff 摘要
计划执行的 Git 命令
建议 commit message
是否需要 PR
是否需要 changelog
是否需要 tag
Git Owner / Workspace Owner 状态
```

轻量改动 Git 收口：

- 轻量改动完成后，应已有最终 LW 记录。
- 先询问用户是否允许提交。
- 用户确认后执行 Git 写入流程。
- Git 写入成功后，向对应 `docs/LW-Work/LWYYMMDDXX-轻量任务标题.md` 追加 Git baseline。
- Git baseline 追加后是否再次纳入 Git，由本场景重新展示 diff 并等待用户确认。
- 正式任务包的 commit / PR / tag 证据由 `uth-git` closeout 记录，并追加到关联 Feedback；Feedback 不等待 Git 信息才生成。
- 正式任务包的 Git 收口边界通常是 Design 级人类验收，而不是单个 Todo 完成。

代码改动 Git 门槛：

- 如果 diff 包含代码改动，Git 计划必须展示最近一次编译 / 构建结果。
- 默认要求编译 / 构建通过，且 `0 warning / 0 exception`。
- 缺少强验证证据时，先路由回 `uth-dev` / `uth-debug` / `uth-review`。
- 用户显式承担风险时可继续 commit，但不得发布 release / tag，除非用户再次明确确认。

禁止：

- 用户确认前不执行 Git 写入。
- 不在非 main 分支打正式 tag。
- 无 changelog 不打正式 tag。
- 不删除分支或 worktree，除非用户确认。

收口：

- 执行用户确认过的 Git 命令。
- 释放锁。
- 输出最终状态。

### 7.9 S8 文档治理 / 规范维护

触发：

- 修改工程规范。
- 修改治理目录结构。
- 优化模板。
- 清理 current-state。
- 初始化或同步 `docs/context/` 模块上下文。
- 根据用户指定的 commit / git range / 稳定代码状态 / 工作区改动同步模块上下文。
- 清理或归档已完成任务包和 LW 记录。
- 创建状态快照。
- 迁移旧 Design/Todo/Feedback。
- 更新 AGENTS.md / `_governance`。
- 修改根目录 README.md 或治理 Hook 手册。

默认读取：

```text
AGENTS.md
docs/current-state.md
docs/_governance/ 相关文件
docs/context/README.md
用户指定文档
```

本场景指单开的文档治理窗口。  
各研发场景中的 Feedback、worker Prompt、Run Log、LW 记录和 current-state 更新，仍由各自场景负责。

`uth-docs` 可包含以下模式：

```text
rules-maintenance：更新 AGENTS.md、docs/_governance/、模板。
context-bootstrap：为新项目或复杂项目建立 docs/context/。
context-sync：根据用户指定 commit / git range / 稳定代码 / 工作区改动同步模块当前事实。
state-cleanup：清理 docs/current-state.md 的旧事实和旧索引。
archive-cleanup：归档已确认完成的正式任务包和 LW 文档。
snapshot：保存历史状态快照。
migration：迁移旧 Design / Todo / Feedback / Run Log。
onboarding-followup：老项目接管后自动承接旧文档治理。
```

`context-bootstrap` 规则：

- 新项目或简单项目可先按前端、后端、数据、部署等技术边界拆分。
- 复杂项目不要直接强拆；先读取入口文档、目录结构、构建配置和关键入口，提出模块拆分建议。
- 模块拆分建议经用户确认后，再创建 `docs/context/README.md` 和模块文件。
- 拆分优先考虑业务/领域边界，其次考虑运行时职责、架构层、协作边界和验证边界。

`context-sync` 规则：

- 根据用户指定 commit、git range、稳定代码状态或工作区改动判断影响哪些模块。
- 只更新模块职责、入口、依赖、边界、验证方式和仍有效风险。
- 不把提交过程写成日志。
- 不复制 Feedback / worker Prompt / Run Log。
- 普通小 UI、文案或局部实现细节不更新 context，除非改变当前模块事实。
- 模块 context 可标明来源证据：commit、git range、稳定代码状态或实际读取的工作区改动。
- 不因等待 Git baseline 阻断 context 或交付报告写回。

`state-cleanup` 规则：

- `docs/current-state.md` 是当前状态索引，不是日志。
- 可清理已完成、已废弃、已替代或不再活跃的任务包 / Todo 索引。
- 可清理旧事实，并改为指向 `docs/context/` 或稳定常驻文档。
- 不把旧 Feedback、Run Log 或提交流水搬进 current-state。

`archive-cleanup` 规则：

- 只迁移明确确认已完成且不再活跃的任务包和 LW 文档。
- 正式任务包迁移到 `docs/archive/work/`。
- 轻量开发最终 LW 记录迁移到 `docs/archive/LW-Work/`。
- 迁移前确认 current-state 不再把这些文档列为活跃项；迁移后更新仍有效索引。

ADR 边界：

- ADR 内容修改、新 ADR、ADR 状态变更归 `uth-design`。
- `uth-docs` 只允许修复 ADR 索引、链接 ADR、或标记“需要进入 uth-design 更新 ADR”。
- `docs/context/` 可索引 ADR，但不复制 ADR 内容，也不详细复述决策正文。

AGENTS.md 边界：

- 可根据开发窗口 Feedback 中重复出现的问题，总结为稳定仓库级规则。
- 不把单次任务经验、长模板、完整治理流程或历史记录写入 AGENTS.md。

验证与 Git：

- `uth-docs` 不跑检查和测试；如引用已有验证记录，必须说明“未在本场景重新验证”。
- 修改 `AGENTS.md`、根目录 `README.md`、`docs/**/*.md` 或任务包 Markdown 前后，必须调用 `uth-utf8-guard` 或等价检查。
- `uth-docs` 不执行 Git 写入；如果需要 commit / PR / tag / release，收口后路由到 `uth-git`。

允许写入：

```text
AGENTS.md
README.md
docs/_governance/
docs/current-state.md
docs/context/
docs/work/
docs/archive/
docs/snapshots/
docs/state/snapshots/
```

禁止：

- 不修改 `skills/`。
- 不修改业务代码、测试和构建产物。
- 不修改 ADR 决策正文。
- 不写 release changelog 正文，除非用户明确把它作为文档维护任务并确认不进入发布流程。
- 不主动审查业务代码，除非用户要求。
- 不把文档治理扩展成代码重构。
- 不把单次任务记录写进 AGENTS.md。
- 不把 diff 摘要流水写进 `docs/context/`。
- 不在 current-state 中写长日志。
- 不执行 Git 写入。

收口：

- 输出修改文件。
- 输出修改理由。
- 输出迁移影响。
- 如果涉及 `docs/context/`，输出模块拆分或同步依据。
- 如果涉及 `docs/context/`，输出实际来源证据；不要求等待 Git baseline。
- 如果涉及归档，输出迁移前后路径。
- 输出未运行检查 / 测试的说明。
- 输出后续使用方式。

---

## 8. current-state 维护规则

`docs/current-state.md` 是当前状态索引，不是项目日志。

### 8.1 内容上限

建议硬限制：

```text
不超过 80-120 行。
最近变化最多 3 条。
最近验证最多 1 条。
```

### 8.2 何时更新

必须更新：

- Todo 完成。
- Todo 阻塞。
- 当前活跃任务包变化。
- 当前阶段变化。
- 关键阻塞变化。
- 最近一次验证结果影响下一步判断。

不必更新：

- 只读分析。
- 纯讨论。
- 未形成任务状态变化的方案评估。
- 临时 Debug 过程中的每一步。
- 普通轻量改动的 LW 记录，除非影响当前阶段、阻塞、验证基线或发布判断。

### 8.3 何时归档 snapshot

建议归档：

- 一个任务包完成。
- 一个阶段结束。
- 正式版本发布前。
- current-state 超过长度上限。
- 项目状态发生大切换。

### 8.4 snapshot 规则

```text
docs/state/snapshots/SYYMMDD-说明.md
```

snapshot 是历史状态，不作为默认读取文件。

---

## 9. Design / Todo / Feedback 规则

### 9.1 Design 定位

Design 是任务包设计，不是整体项目事实。

它用于描述：

- 一个阶段能力。
- 一个功能闭环。
- 一个修复包。
- 一个架构设计任务。
- 一组相关 Todo 的设计背景和边界。

Design 不用于记录：

- 项目长期当前事实。
- 开发过程流水账。
- 每次验证日志。
- Git 提交历史。

长期事实必须同步到：

```text
docs/project-overview.md
docs/architecture.md
docs/development.md
docs/context/
docs/api-contract.md
docs/data-model.md
docs/ui-guidelines.md
docs/deployment.md
```

### 9.2 Todo 定位

Todo 是可执行工单。

每个 Todo 必须归属于某个 Design，并明确：

- 目标。
- 范围。
- 不做什么。
- 允许修改范围。
- 禁止修改范围。
- 验收标准。
- 必跑验证。
- 对应 Feedback 文件。

### 9.3 Feedback 定位

Feedback 是 Todo 的交付报告，不是过程日志。

Feedback 必须说明：

- 当前状态。
- 完成内容。
- 修改文件。
- 验证命令和结果。
- 未验证项。
- 风险和回滚方式。
- 后续建议。

### 9.4 Run Log 定位

Run Log 是过程记录，只在必要时写。

适合写 Run Log：

- Debug 过程较复杂。
- 验证失败需要保留日志重点。
- 多轮 Agent 执行需要保留交接记录。
- 子代理执行结果需要分片记录。

不适合写 Run Log：

- 简单小修。
- 纯讨论。
- 没有产生有效结论的临时尝试。

### 9.5 Prompt 定位

Prompt 是 `worker` 派发输入证据，不是当前事实源。

凡派发 `worker`，完整派发提示词必须先写入：

```text
docs/work/DYYMMDDXX-任务包标题/prompts/PYYMMDD-HHMM-T01-worker-任务名.md
```

实际派发给 worker 的短提示词只要求其读取并执行该 Prompt 文件，不需要另存。

`planner` / `evaluator` 是只读辅助角色，不记录 Prompt；它们的结论在主窗口收口、Run Log 或 Feedback 中按需摘要。

如果同一 Todo 派发多个 `worker`，每个 `worker` 必须各有一份 Prompt，用不同任务名或序号区分。  
如果同一 `worker` 返工，返工要求必须追加到该 worker 原 Prompt 文件中，不新建 Prompt 文件。

Prompt 必须说明：

- 关联任务包和 Todo。
- 子代理角色：`worker`。
- 必读文件。
- 默认不读文件。
- 任务目标。
- 允许修改范围。
- 禁止修改范围。
- 必跑验证。
- 回传格式。

### 9.6 LW-Work 定位

`docs/LW-Work/` 保存轻量开发最终记录。

LW 记录不是正式 Design / Todo / Feedback，不用于管理复杂任务。

适合写 LW：

- 轻量改动没有正式任务包。
- 任务完成时需要留下用户原始需求、任务边界、修改摘要、验证摘要、风险和回滚方式。
- 后续 Git 写入成功后，需要追加 commit / PR / tag 等 Git baseline。

不适合写 LW：

- 只读分析。
- 已经归属正式任务包的 Todo。
- 需要 Design / Todo / Feedback 的复杂任务。

### 9.7 Context 定位

`docs/context/` 是常驻上下文层的一部分，用于保存模块级当前事实摘要。

适合写入：

- 模块职责或“不负责什么”发生变化。
- 模块入口、关键依赖、调用边界发生变化。
- 主要验证入口发生变化。
- 代码和现有 context 不一致，且代码代表当前事实。
- Review / Debug 发现仍有效的模块风险。

不适合写入：

- 单次开发过程。
- 普通小改动的 diff 摘要。
- Prompt、Run Log、Feedback 全文。
- 已过期的历史结论。

推荐文件：

```text
docs/context/README.md
docs/context/00-overview.md
docs/context/10-模块名.md
docs/context/90-cross-cutting.md
```

每个模块文件应简短说明：

- 职责。
- 不负责。
- 关键入口。
- 关键依赖。
- 常见修改点。
- 验证入口。
- 当前风险。
- Source evidence：该上下文对应的 commit / git range / 稳定代码 / 工作区来源 / 更新时间。
- 相关任务包 / ADR 索引。

如果 context 根据未提交工作区改动更新，或用户明确要求暂按工作区改动整理，记录实际读取来源即可，不等待 Git baseline。

---

## 10. ADR 规则

ADR 只记录长期技术决策。

适合写 ADR：

- 技术栈选择或变更。
- 核心架构变化。
- 数据库模型重大变化。
- 接口契约策略变化。
- 部署方式变化。
- 长期影响后续开发的规则变化。

不写 ADR：

- 普通 bug 修复。
- 普通 UI 调整。
- 普通接口字段补充。
- 单次任务实现细节。
- 临时探索过程。

### 10.1 ADR 状态

推荐状态：

```text
Proposed
Accepted
Superseded
Deprecated
Rejected
```

### 10.2 ADR 与当前事实

ADR 是决策证据链，不是当前事实源。

当技术选型或架构更新时：

1. 新增 ADR，说明变更原因。
2. 将旧 ADR 标记为 `Superseded` 或 `Deprecated`。
3. 同步更新常驻上下文文件。
4. 在 current-state 中记录状态变化和事实来源。

ADR 正文、状态变更和新增决策由架构设计场景负责；文档治理场景只维护 ADR 索引、链接和当前事实引用。

---

## 11. Changelog 与版本规则

Changelog 只在正式版本发布时写。

规则：

- 一个正式 Git tag 必须对应一个 changelog。
- 一个 changelog 必须对应一个正式 Git tag。
- 没有 changelog 不打正式 tag。
- 普通开发 commit 不强制新增 changelog。
- Changelog 面向普通用户，不写过多技术实现细节。

版本采用 SemVer：

```text
vMAJOR.MINOR.PATCH
```

不使用日期作为版本号。  
日期已经体现在 Design 编号、changelog 发布日期和 Git tag 时间里。

---

## 12. Subagent 规则

Subagent 不默认启用，只有触发条件成立时使用。  
正式增量开发可采用 subagent-first；超轻量改动可由主窗口直接完成。

适合使用：

- 需要同时阅读多个模块。
- 前端、后端、文档、测试可以明确拆分。
- 需要一个代理实现，另一个代理审查。
- 单窗口上下文太大。
- 多个写入代理并行，且可以创建独立 worktree。

不建议使用：

- 一两处简单文档修正。
- 单文件小改动。
- 任务目标还没有 Design / Todo。
- 主窗口还没弄清边界。
- 子代理之间会改同一批文件，且无法拆开。
- 不创建 worktree，却希望多个 `worker` 同时改代码。

硬规则：

```text
主窗口负责上下文和收口。
子代理负责边界清晰的局部任务。
子代理不得执行 Git 写入。
不创建 worktree 时，同一物理工作区只能有一个写入者。
多个 `worker` 并行写代码时，必须创建独立 worktree。
```

默认角色：

- `worker`：负责实现授权范围内的改动。
- `planner`：负责只读探索、方案拆分和上下文整理。
- `evaluator`：负责只读验收，不修改代码和文档。

协作原则：

- 谁弄出的问题谁解决。
- 谁提出的问题谁验收。
- `evaluator` 发现问题时回传给主窗口，不直接修复。
- 子代理不得执行 Git 写入。
- `worker` Prompt 必须落盘到当前正式任务包 `prompts/`；`planner` / `evaluator` 不记录 Prompt。

Worker Prompt 派发流程：

```text
1. 主窗口为每个 worker 写入完整 Prompt 文件；同一 worker 返工时追加更新原文件。
2. 主窗口用短提示词派发 worker。
3. worker 读取 Prompt 文件并执行。
4. worker 回传读取范围、修改范围、验证、风险和阻塞。
5. 主窗口负责整合、验证、Feedback、current-state 和 Git 建议。
```

短提示词示例：

```text
请读取并执行：
docs/work/DYYMMDDXX-任务包标题/prompts/PYYMMDD-HHMM-T01-worker-任务名.md

不得执行 Git 写入。完成后按文件里的回传格式回复。
```

---

## 13. Git 规则

Git 细则统一维护在：

```text
docs/_governance/git-workflow.md
```

任何 Git 写入前，必须读取该文件。

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
- 任何修改 `.git`、index、当前分支指针或工作区归属关系的命令

Git 写入前必须展示：

- 当前分支。
- `git status`。
- diff 摘要。
- 计划执行的 Git 命令。
- 建议 commit message。
- 是否需要 PR。
- 是否需要 changelog。
- 是否需要 tag。
- 是否为轻量改动，以及 Git 成功后是否追加 baseline 到 LW / Feedback。
- Git Owner / Workspace Owner 状态。

未经用户确认，不得执行 Git 写入。

轻量 Git 记录：

- 轻量改动的最终 LW 记录已由 `uth-dev` 在任务完成时写好。
- 用户确认并完成 Git 写入后，向 `docs/LW-Work/` 下的最终记录追加 Git baseline。
- Git baseline 追加后如果需要纳入 Git，必须重新进入 Git 写入确认流程。

---

## 14. 新项目初始化流程

新项目初始化必须由用户显式调用 `uth-onboarding` 或明确要求启用 UTH。

安装流程不执行本节，不询问“当前路径是否项目目录”，不创建项目文档。

步骤：

1. 读取 `AGENTS.md`，若不存在则准备创建轻量入口。
2. 扫描项目目录、README、配置文件、启动脚本、测试目录、构建脚本。
3. 仅记录技术栈、模块边界、启动方式、测试方式、构建方式的线索；证据不足时标记待 `uth-docs` 确认。
4. 创建或补齐常驻上下文层。
5. 创建或补齐 `docs/_governance/`。
6. 创建或补齐 `docs/context/`、`docs/work/`、`docs/LW-Work/`、`docs/archive/`、`docs/snapshots/`、`docs/decisions/`、`docs/changelogs/`。
7. 从 `uth-onboarding` 的 bundled assets 复制项目本地 Hook 工具到 `tools/uth-hooks/`。
8. 创建 `.uth-governance/project.json`。
9. 不修改业务代码。
10. 输出新增文件、修改文件、项目本地 Hook、项目标记、未确认事实和后续使用方式。
11. 不执行 Git 写入；如用户要求提交，进入 S7 并等待用户确认。

---

## 15. 老项目接管流程

老项目接管必须由用户显式调用 `uth-onboarding` 或明确要求 UTH 接管。

老项目不要一上来重构，也不要一上来读全量源码。先保护旧文档，建立最小治理入口，再自动交给 `uth-docs` 深化。

步骤：

1. 先创建文档备份压缩包：`docs/ONBYYMMDDXX-pre-uth-docs-backup.zip`。
2. 备份范围是 onboarding + docs 第一次接管时后续可能影响的所有文档类文件。
3. 扫描当前结构、已有文档、入口 README、配置 / 构建 / workspace 声明和少量 Git 基线。
4. 创建一次性接管快照：`docs/snapshots/ONBYYMMDDXX-existing-project-handoff.md`。
5. 创建或补齐最小 UTH 文档骨架。
6. 从 `uth-onboarding` 的 bundled assets 复制项目本地 Hook 工具到 `tools/uth-hooks/`。
7. 建立或更新 `docs/current-state.md` 初始索引。
8. 创建 `.uth-governance/project.json`。
9. 不修改业务代码。
10. 不把旧 Design、旧 Todo、旧 Feedback、旧 Run Log 或 Prompt 当成当前事实。
11. 自动进入 `uth-docs`，继续旧文档分类、context 重建、current-state 深化和归档处理。

老项目接管阶段的 `current-state.md` 只能是初始索引。没有读到足够代码事实时，写“待 `uth-docs` 根据代码事实深化确认”，不要写成已确认事实。

---

## 16. 后续任务执行协议

Agent 收到任务后，按以下顺序执行：

```text
1. 由 uth-governance / 子 Skill 完成场景判定和 UTH-SP 触发判断。
2. 进入对应 uth-* Skill。
3. 只读取该场景必要文件。
4. 说明任务理解、修改范围、风险点、验收标准。
5. 如需求、范围、方案或验收存在歧义，进入 brainstorming。
6. 如派发 worker，先写 worker Prompt，再用短提示词派发；planner/evaluator 不写 Prompt。
7. 按场景执行。
8. 写入前通过场景写入范围门禁；超范围写入先问用户。
9. 运行必要验证；代码改动默认要求编译 / 构建通过且 `0 warning / 0 exception`。
10. 按场景写入 Feedback / LW final record / current-state / ADR / changelog / worker Prompt / Run Log；治理 Markdown 写入前后走 `uth-utf8-guard`。
11. 轻量改动完成后询问是否提交；Git 写入成功后追加 Git baseline 到 LW final record 或正式 Feedback。
12. 输出 Git / PR 建议。
13. Git 写入前等待用户确认。
```

禁止：

- 不允许跳过场景判定。
- 不允许默认扫描全部 docs。
- 不允许把旧 Design 当当前事实。
- 不允许把 Prompt、Run Log、LW 记录当当前事实源。
- 不允许无关重构。
- 不允许静默引入依赖。
- 不允许伪造验证结果。
- 不允许未确认就执行 Git 写入。

---

## 17. 最小交付标准

一个 Todo 只有满足以下条件，Agent 才能说完成：

- 已说明完成了什么。
- 已列出修改文件。
- 已运行 Todo 要求的验证命令，或说明无法运行原因。
- 已说明验证结果；代码改动包含编译 / 构建、warning 数和 exception 数。
- 已说明未验证的部分。
- 已说明风险点。
- 已说明回滚方案。
- 已写 Feedback。
- 已更新 `docs/current-state.md`。
- 如使用 worker subagent，已记录关联 worker Prompt。
- 必要时已更新 ADR 或 changelog。

轻量改动不适用完整 Todo 最小交付标准，但至少应说明：

- 修改了什么。
- 修改文件。
- 验证方式和结果。
- 未验证项。
- 是否建议提交。
- 如用户确认并完成 commit，已追加 LW 记录。

如果任何验证无法执行，必须写明：

- 为什么不能执行。
- 缺少什么环境。
- 人工应该如何补测。

---

## 18. 旧版布局迁移建议

如果项目已经使用旧结构：

```text
docs/designs/
docs/todos/
docs/feedback/
```

建议迁移为：

```text
docs/work/DYYMMDDXX-任务包标题/
```

迁移映射：

```text
docs/designs/D26051401-xxx.md
  -> docs/work/D26051401-xxx/00-D26051401-design.md

docs/todos/D26051401/D26051401-T01-xxx.md
  -> docs/work/D26051401-xxx/10-D26051401-T01-todo-xxx.md

docs/feedback/D26051401/D26051401-T01-开发反馈.md
  -> docs/work/D26051401-xxx/11-D26051401-T01-feedback-xxx.md
```

治理规则文件迁移：

```text
docs/agent-rules.md
  -> docs/_governance/agent-rules.md

docs/git-workflow.md
  -> docs/_governance/git-workflow.md

docs/human-workflow.md
  -> docs/_governance/human-workflow.md

docs/subagent-workflow.md
  -> docs/_governance/subagent-workflow.md

docs/HOOKS_工程治理门禁手册.md 或等价门禁说明
  -> docs/_governance/hook-gates.md
```

过渡期可以在旧路径保留薄跳转文件，避免 Agent 或工具链找不到旧路径。

---

## 19. 最后提醒

这套治理的重点不是多写文档，而是保持四个事实清楚：

```text
项目现在是什么状态。
当前任务属于什么场景。
当前 Todo 到底做什么。
做完以后功能处于什么状态。
```

Agent 不应该为了“看起来规范”而多读、多写、补模板。  
只有触发条件成立时，才升级治理强度。
