# AGENT 工程治理启动手册

本手册只作为 Agent 开工时的操作手册：判断是否启用 UTH、进入哪个场景、读写哪些文件、如何收口。它不承载完整规则、模板和 Hook 细则。

详细内容统一查阅：

- Hook 门禁：`docs/HOOKS_工程治理门禁手册.md`
- 全链路流程：`docs/FLOW_全链路流程图.md`
- 文档模板：`docs/TEMPLATES_工程治理模板.md`

## 1. 治理目标

UTH 的目标是让人和 Agent 都能快速回答：

- 当前项目事实在哪里。
- 当前任务属于哪个场景。
- 本次只需要读哪些文件、写哪些文件。
- 什么证据能证明任务完成。
- 何时需要设计、开发、Debug、Review、文档治理或 Git 收口。

核心原则：

- 少读：只加载当前场景必要上下文。
- 少写：只写当前场景授权文件。
- 强触发：需求、范围、验收不清时先澄清或进入 brainstorming。
- 强收口：完成声明必须有验证、证据和风险说明。

## 2. 三层模型

UTH 保留三层工程治理模型：

| 层级 | 用途 | 典型位置 |
| --- | --- | --- |
| 常驻上下文层 | 保存当前仍有效的项目事实 | `.uth-governance/project.json`、`entrypoints.current_state`、`docs/context/` |
| 任务流转层 | 承载一次需求、阶段、修复或交付闭环 | `docs/work/`、`docs/LW-Work/` |
| 长期记录层 | 记录长期决策、版本和发布事实 | `docs/decisions/`、`docs/changelogs/`、Git baseline |

`Design -> Todo -> Feedback` 是正式任务主线。轻量开发不创建正式任务包，完成时写 `docs/LW-Work/` 最终记录。

### 2.1 轻量与正式任务硬边界

`light-dev` 不是 Agent 自行判断的“我觉得很小”。它必须通过 L1 模型硬边界：

- 声明 `llm_model`，且模型在首批支持表内。
- 声明 `task_shape.changed_files_count`、`task_shape.modules_count`、`task_shape.implementation_steps_count`。
- 不命中 Design、正式 Todo、新功能面、API/契约、数据库迁移、权限安全、架构边界、依赖构建、跨模块数据流、外部集成、并发/状态机、数据丢失风险、worker/并行 Agent 等正式触发。

首批 `light-dev` 支持模型：`claude-opus-4.6`、`claude-opus-4.7`、`gpt-5.4`、`gpt-5.5`、`gpt-5.3-codex-spark`、`deepseek-v4-pro`、`deepseek-v4-flash`、`mimo-v2.5-pro`、`kimi-k2.6`。

具体上限和字段契约以 `docs/HOOKS_工程治理门禁手册.md` 的 L1 Process Gate 为准。未知模型、缺少计数字段、超出模型上限或命中正式触发时，必须切换到 `formal-dev` 或先澄清/补设计，不得继续轻量路径。

## 3. AGENTS.md 定位

`AGENTS.md` 是仓库级 Agent 原生入口，只放每次会话都必须知道的稳定规则。

它应该保留：

- UTH 是否启用以及入口文件。
- 必读的最小索引和常用命令。
- 场景路由入口和禁止事项。
- Git 写入前必须确认的要求。
- 指向本手册、模板、Hook 和流程图的链接。

它不应该承载：

- 完整 Design、Todo、Feedback 模板。
- 完整 Hook 规则表。
- 完整 Git、Subagent、发布手册。
- 单次任务过程、旧结论、历史日志或大段治理理念。

## 4. 目录职责

| 路径 | 职责 |
| --- | --- |
| `.uth-governance/project.json` | 项目已启用 UTH 的标记，保存 `entrypoints`、`document_language` 等项目级事实 |
| `AGENTS.md` | Agent 最小入口和稳定约束 |
| `README.md` | 面向人类或外部使用者的项目入口 |
| `docs/README.md` | 文档索引 |
| `entrypoints.current_state` | 当前状态索引，实际路径来自 `.uth-governance/project.json` |
| `docs/context/` | 模块级当前事实摘要，不记录流水和旧结论 |
| `docs/work/` | 正式任务包：Design、Todo、Feedback、worker Prompt、Run Log |
| `docs/LW-Work/` | 轻量任务最终记录 |
| `docs/snapshots/` | 接管、阶段或状态快照 |
| `docs/archive/` | 已完成且不再活跃的任务包和轻量记录 |
| `docs/decisions/` | ADR 决策证据链 |
| `docs/changelogs/` | 正式版本变更记录 |
| `tools/uth-hooks/` | 项目本地 Hook runner，由 `uth-onboarding` 复制，不全局安装 |

旧任务包、归档、current-state 或 context 不得被复制成新目标项目事实。当前事实必须来自目标项目当前代码、配置、文档和用户确认。

## 5. 场景触发与路由

### 5.1 静默规则

当前项目根目录没有 `.uth-governance/project.json` 时，除以下情况外，其他 `uth-*` 场景保持静默：

- 用户显式调用 `uth-onboarding`。
- 用户明确要求启用 UTH 或接管当前项目。
- 安装流程正在安装治理包本身，且没有初始化目标项目。

没有项目标记时，不得擅自创建治理文档、任务包、Hook 工具或 current-state。

### 5.2 顶层判断

进入任务后先判断场景：

| 需求类型 | 场景 |
| --- | --- |
| 启用、初始化、接管项目 | `uth-onboarding` |
| 架构设计、方案比较、技术选型 | `uth-design` |
| 增量功能、字段、UI、API、业务行为实现 | `uth-dev` |
| Bug、失败测试、运行错误、回归 | `uth-debug` |
| 验收、Review、 readiness 判断 | `uth-review` |
| 文档同步、当前事实整理、接管后文档治理 | `uth-docs` |
| 分支、commit、push、PR、tag、release | `uth-git` |
| 查找任务包、历史证据、上下文冲突 | `uth-context-trace` |

如果需求、范围、方案或验收标准不清，先提出一个最关键澄清问题；需要结构化澄清时进入 `uth-sp-brainstorming`。

### 5.3 UTH-SP 触发

UTH-SP 是场景内方法技能，不是独立业务场景。只有当当前场景需要计划、TDD、系统化 Debug、Subagent 协作、Review 流程或收口验证时，才由 owning scene 触发。

命中触发条件时必须完整执行；满足明确豁免条件时才走轻量路径。详细触发和豁免规则看 `docs/FLOW_全链路流程图.md`。

## 6. 场景读写边界

| 场景 | 可读重点 | 可写边界 |
| --- | --- | --- |
| `uth-onboarding` | 项目入口、README、配置、构建脚本、少量代码线索 | `.uth-governance/project.json`、最小治理骨架、项目本地 `tools/uth-hooks/`、接管快照 |
| `uth-design` | 当前事实、相关模块、必要 ADR | Design、ADR 草案或已确认决策、必要 current-state 摘要 |
| `uth-dev` | Todo、Design、相关 context、实现文件 | 授权代码范围、Feedback 或 LW final record、必要 current-state |
| `uth-debug` | 错误证据、相关代码、相关历史任务 | 修复代码、Debug 反馈、必要 current-state 或风险记录 |
| `uth-review` | diff、Todo、Feedback、验证命令、相关 context | Review 结论、验收反馈；不直接修改业务代码，除非重新路由 |
| `uth-docs` | 当前代码事实、配置、schema、文档索引 | 文档治理范围内的 current-state、context、README、归档和同步报告 |
| `uth-git` | Git 状态、diff、Git 工作流、待提交文档 | Git 写入、PR、tag、release、Git baseline 回写 |
| `uth-context-trace` | active/archived task package、Design、Todo、Feedback、Prompt、Run Log | 默认只读；只输出定位结果 |

跨出场景写入边界前必须停下说明原因，并获得用户确认或重新路由。

治理 Markdown 写入前后必须执行 UTF-8 守卫或等价检查，防止中文文档乱码、BOM 和 Markdown fence 失衡。

## 7. 跨场景收口规则

- `debug`、`design`、`docs`、`dev` 场景收口时可以建议进入 `uth-git`，但绝不自动进入 `uth-git`。
- Git 写入必须由用户显式确认，并由 `uth-git` 执行。
- `light-dev` 在任务完成时写 `docs/LW-Work/` 的 LW final record；如果用户之后确认并完成 Git 写入，再由 `uth-git` 追加 Git baseline。
- 正式 `dev` 或 `debug` 完成后，按 Todo/Feedback 记录交付、验证、风险和回滚方式。
- 使用 `worker` 时，完整 Prompt 必须先写入正式任务包的 `prompts/`；`planner` 和 `evaluator` 不落盘 Prompt。
- closeout 只能引用已经执行或明确豁免的证据，不得把“计划运行”写成“已经通过”。

Hook 的 L0/L1/L2/L3 具体输入、输出和阻断规则以 `docs/HOOKS_工程治理门禁手册.md` 为准。

## 8. 新项目 onboarding

新项目启用 UTH 必须由用户显式调用 `uth-onboarding` 或明确要求启用 UTH。安装治理包不等于初始化当前项目。

最小流程：

1. 判断项目是否已有 `.uth-governance/project.json`。
2. 如无标记，读取最少项目线索：README、配置、入口、构建、测试目录。
3. 在首次治理 Markdown 写入或场景 closeout 报告前，询问并持久化 `document_language`。
4. 创建 `.uth-governance/project.json` 和必要 `entrypoints`。
5. 创建最小治理文档骨架，未知事实写 `TBD` 或“待 `uth-docs` 根据代码事实确认”。
6. 将包内 Hook 工具复制到目标项目 `tools/uth-hooks/`。
7. 不修改业务代码，不执行 Git 写入。
8. 输出新增/修改文件、未确认事实、后续建议和是否需要 `uth-docs`。

`document_language` 必须在第一次 governed Markdown 写入或场景 closeout 报告前保存到 `.uth-governance/project.json`，后续治理文档和收口报告沿用该语言。

## 9. 既有项目接管

既有项目接管也必须由用户显式调用 `uth-onboarding` 或明确要求 UTH 接管。

先保护现状，再建立治理入口：

1. 创建接管前文档备份，例如 `docs/ONBYYMMDDXX-pre-uth-docs-backup.zip`。
2. 扫描入口、已有文档、配置、构建和少量 Git 基线。
3. 创建接管快照：`docs/snapshots/ONBYYMMDDXX-existing-project-handoff.md`。
4. 创建或补齐最小 UTH 骨架和项目本地 Hook 工具。
5. 创建 `.uth-governance/project.json`，并持久化 `document_language`。
6. 不把旧 Design、旧 Todo、旧 Feedback、旧 Run Log 或 Prompt 当作当前事实。
7. 不修改业务代码，不执行 Git 写入。

如果用户要求 `full-takeover`，`uth-onboarding` 必须把它当作一个事务编排：最小启用完成后，路由到独立的 `uth-docs onboarding-followup`。`uth-docs` 负责基于代码事实执行 `full-project-baseline`、旧文档分类、context 重建、current-state 清理和归档处理；`uth-onboarding` 不内联执行这些动作。

接管完成必须等到 `uth-docs` 返回 `full-project-docs-complete` 和 docs 场景收口证据后，才能由 `uth-onboarding` 给出最终接管收口。

## 10. 后续任务协议

UTH 启用后的每次任务按以下顺序执行：

1. 读取 `.uth-governance/project.json`，确认 UTH 已启用、入口文件和 `document_language`。
2. 判定场景；场景不清时澄清，不默认全量读文档。
3. 只读取当前场景必要文件和代码证据。
4. 说明理解、范围、风险和验收标准。
5. 必要时触发对应 UTH-SP。
6. 写入前执行 L2 写入范围、Git、脚本或 UTF-8 预检；不满足则停下处理。
7. 按授权范围执行实现、修复、文档同步或 Review。
8. 运行必要验证；不能运行时说明原因、缺少环境和人工补测方式。
9. 按场景写 Feedback、LW final record、current-state、ADR、changelog 或 docs 同步结果。
10. 对治理 Markdown 做写后 UTF-8/Markdown 守卫。
11. 输出收口报告，并在需要时建议 `uth-git`，但等待用户显式进入。

## 11. 最小交付标准

任务完成声明至少包含：

- 完成了什么。
- 修改了哪些文件。
- 运行了哪些验证，结果是什么。
- 未验证部分和原因。
- 风险点和回滚方式。
- 对应场景的文档记录是否已写入。
- 是否建议后续进入 `uth-git`。

代码改动默认需要编译、构建或测试证据；如果场景规则要求 `0 warning / 0 exception`，没有通过或没有豁免就不能声称完成。

文档改动必须确认 UTF-8、无 BOM、无替换字符、Markdown fence 平衡。

## 12. 最后提醒

- UTH 的重点不是多写文档，而是让当前事实、任务边界、验证证据和收口状态清楚。
- 不要把旧任务记录、Prompt、Run Log、归档或 ADR 当作当前事实源。
- 不要为了开工而跳过场景判断。
- 不要为了收口而伪造验证结果。
- 不要在非 `uth-git` 场景执行 Git 写入。
- 不要在没有 `.uth-governance/project.json` 的项目里静默启动 `uth-*` 场景。
