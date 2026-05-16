# 老项目接管与 `uth-docs` 完成边界设计

## 背景

当前 UTH Governance Pack 已经区分了全局安装、项目启用和后续场景治理，但老项目接管存在一个语义缺口：`uth-onboarding` 会创建项目标记、备份、快照并交给 `uth-docs`，但仍以“minimal onboarding”收口；`uth-docs onboarding-followup` 有动作清单，却缺少“完整接管完成”的硬边界。因此实际执行中可能只生成索引和待办，就对用户声称接管或文档治理完成。

老项目接管应当是一个完整事务，而不是“启用项目标记”或“生成几个文档入口”。用户说“接管老项目”时，最终结果必须是旧文档已保护、已分类、已迁移或归档，当前事实已由代码状态确认，遗留文档不再污染活跃上下文。

## 目标

- 让 `/uth-onboarding existing-project` 在用户要求接管老项目时承担完整事务编排责任。
- 让 `/uth-docs onboarding-followup` 继续作为文档治理执行者，避免在 `uth-onboarding` 中复制完整文档治理逻辑。
- 只有完整接管证据齐备后，才允许最终报告说“老项目接管完成”。
- 普通 `/uth-docs` 场景保持自收口，不因为存在回跳机制而回到 `/uth-onboarding`。
- 项目过大、模块边界不清、旧文档可信度无法判断时，必须停下来问用户，而不是把阻塞项写成待办后声称完成。

## 非目标

- 不改变 UTH 的安装语义：全局安装仍不初始化当前项目。
- 不让未启用 UTH 的项目自动被 `uth-*` 场景接管。
- 不让 `uth-docs` 执行代码、测试、Git 或 skill 修改。
- 不要求 onboarding 读取全量源码来假装完成项目理解。
- 不把普通文档同步、归档清理、规则维护都纳入 onboarding 回跳。

## `uth-docs` 重新定位

`uth-docs` 不是轻量索引生成器，也不是只按 mode 补几个文档的维护工具。它是 UTH 中独立的项目文档治理窗口，负责以代码事实为基础、项目文档为辅助，对项目进行全生命周期的文档治理。

`uth-docs` 的核心产物是“可信文档基线”：

- 当前项目事实来自一手代码、构建配置、模块声明、运行入口、测试入口和脚本。
- 旧文档、README、AGENTS、历史任务文档只能作为辅助证据，必须接受代码事实校验。
- `docs/context/`、`docs/current-state.md`、项目入口文档和归档结构共同表达当前文档基线。
- 没有可信基线时，`uth-docs` 不能用局部更新结果声称项目文档治理完成。

### 完整代码事实读取

首次文档治理、老项目接管、可信基线缺失或可信基线失效时，`uth-docs` 必须进入 full-project baseline 流程。

full-project baseline 需要读取并整理：

- first-party source code。
- build、dependency、workspace、module declaration 文件。
- application/runtime entrypoints。
- test and verification entrypoints。
- scripts and local development commands。
- existing README、AGENTS、docs、old governance docs。
- module-local README 或 architecture docs。

排除范围：

- `.git/`
- dependency folders
- build outputs
- caches
- generated artifacts
- binary assets，除非它们本身是文档治理对象

“完整读取”不等于把依赖、构建产物或缓存纳入治理，也不等于在一个回复里倾倒所有源码内容；它要求 agent 建立全项目代码事实索引，并按模块读到足以确认职责、边界、入口、依赖和验证路径的细节。

### Diff、Git Range 和指定版本治理

根据 git diff、git range、指定 commit、tag 或用户指定版本做文档治理时，`uth-docs` 仍然以全项目可信基线为前提。

允许局部读取的条件：

- 已存在可信的 full-project documentation baseline。
- 本次请求明确限定了 diff、range、commit、tag、版本或模块范围。
- agent 能从变更影响范围追踪到相关模块、入口、依赖、测试和文档。
- 更新后能证明全项目文档基线仍然成立。

如果没有可信基线，或者 diff 影响穿透到无法确认的模块边界，必须先进入 full-project baseline 或停下来询问是否按模块拆分治理，不能只同步局部 diff 后声称完成。

### `uth-docs` 完成状态

`uth-docs` 的 closeout 必须区分完成等级：

- `full-project-docs-complete`：全项目可信文档基线已建立或重新确认。
- `scoped-docs-complete`：指定 diff、range、版本、模块或文件范围已同步，且既有全项目基线仍可信。
- `blocked`：继续治理需要用户选择、缺少必要代码事实、项目过大需要拆分、或写入范围超出当前场景。
- `partial/paused`：用户显式要求暂停，或用户只要求执行局部维护且不要求全项目完成。

只有 `full-project-docs-complete` 才能说“项目完整文档治理完成”。`scoped-docs-complete` 只能说“指定范围文档治理完成”，不得扩大成全项目完成。

允许保留 `scoped-docs-complete`，但禁止把它简称为“完成”。当用户问“文档治理完成了吗”时，默认按全项目口径回答；只有用户明确询问指定 diff、range、版本、模块或文件范围时，才按 scoped 口径回答。

### 大项目模块拆分治理

当项目过大，无法在当前上下文中可靠建立 full-project baseline 时，`uth-docs` 不应降级为半成品，也不应把未完成工作写成待办后声称完成。它应先说明阻塞点，并询问用户是否允许按模块拆分治理。

用户允许后，`uth-docs` 自动进入模块拆分场景：

- 读取足够的目录结构、构建配置、模块声明、入口文件和现有文档，识别候选模块边界。
- 写入或更新 `docs/context/README.md`、模块索引、模块拆分说明和必要的 context 报告。
- 输出模块拆分结果，包括模块列表、每个模块的职责假设、主要入口、依赖线索、待确认问题和建议治理顺序。
- 停下来等待用户确认模块拆分结果。

用户确认模块拆分结果后，`uth-docs` 按模块顺序逐个治理。每完成一个模块：

- 写入对应模块 context 报告。
- 标明该模块的完成状态、代码事实来源、排除范围、仍需后续模块确认的交叉依赖。
- 停下来等待用户确认，再进入下一个模块。

模块拆分和逐模块治理应作为一个轻量开发型治理事务留下 final record，用于跨窗口续跑。final record 至少记录：

- 用户原始请求。
- 当前治理目标。
- 已确认的模块拆分结果。
- 已完成模块和对应 context 文件。
- 未完成模块队列。
- 当前模块治理状态。
- 下一步提示词。

如果上下文过长、模块数量过多、或继续在当前窗口会降低可靠性，agent 必须提示用户建议更换窗口继续，并给出可直接复制的新窗口提示词。新窗口收到提示词后，应先读取轻量 dev final record，再继续未完成模块治理，直到全部模块完成并重新确认 full-project baseline。

## 推荐架构

采用“onboarding 编排、docs 执行、onboarding 总收口”的三段式设计。

### 1. `/uth-onboarding existing-project` 前置接管

`uth-onboarding` 负责接管事务的入口和前置安全动作，并必须先区分 `takeover_scope=enable-only` 与 `takeover_scope=full-takeover`：

- 确认并持久化 `document_language`。
- 创建或更新 `.uth-governance/project.json`。
- `enable-only` 只启用 UTH，不要求备份 zip、handoff snapshot 或 `uth-docs` 路由。
- `full-takeover` 备份旧文档到 `docs/ONBYYMMDDXX-pre-uth-docs-backup.zip`。
- 建立完整 `docs/` 目录骨架。
- 根据项目状态建立一次性接管快照。
- 记录旧文档候选、项目入口、代码事实线索、未确认事实和需要 `uth-docs` 处理的范围。
- 生成 handoff evidence，并自动路由到 `/uth-docs onboarding-followup`。

这一阶段不能声称“老项目接管完成”。它只能声称“接管前置流程完成，已进入文档治理”。

### 2. `/uth-docs onboarding-followup` 完整文档治理

`uth-docs` 负责真正的旧文档治理：

- 读取 onboarding handoff snapshot。
- 校验备份 zip 路径已记录且可解释。
- 建立或补齐完整 `docs/` 结构。
- 执行 full-project baseline，基于代码、配置、入口文件、测试入口和已有稳定文档建立当前项目快照。
- 对旧文档逐项分类：current candidate、historical evidence、archive candidate、discard candidate。
- 对可用旧文档迁移到对应目录，并在 context/current-state 中只保留仍然成立的事实。
- 对不可用或过期旧文档归档，或从活跃上下文中移除。
- 删除或移动原位置旧文档前，必须证明该文档已经存在于本次备份 zip 中；未进入备份 zip 的文档不得删除。
- 清理 `docs/current-state.md` 中的待确认事实、旧索引和半成品待办。
- 清理旧文档残留时，只能删除或移动已被备份 zip 收录的文档；保留备份 zip，并在收口中告知备份 zip 存放位置。
- 输出 takeover completion evidence 给 `uth-onboarding`。

这一阶段可以说“`uth-docs onboarding-followup` 文档治理完成”，但不能代表整个接管事务最终完成，最终完成声明由回跳后的 `uth-onboarding` 发出。

### 3. 回到 `/uth-onboarding` 总收口

只有当 `/uth-docs onboarding-followup` 带着完整接管证据回跳，`uth-onboarding` 才能做最终总收口：

- 检查 `takeover_session_id` 与 handoff snapshot 匹配。
- 检查旧文档已全部分类。
- 检查迁移、归档、丢弃或保留策略均有记录。
- 检查 `docs/current-state.md` 不再把待确认事实当成活跃事实。
- 检查普通旧文档残留已清理，或有明确用户确认的保留理由。
- 检查备份 zip 路径在最终报告中明确告知用户。
- 检查没有未处理的 in-scope takeover blocker。

通过后，最终报告才允许使用“老项目接管完成”。

## 回跳隔离规则

`/uth-docs` 只有在以下字段齐全时，才允许把完成证据交回 `/uth-onboarding`：

```text
origin_scene: uth-onboarding
origin_mode: existing-project
handoff_type: existing-project-takeover
takeover_session_id: ONBYYMMDDXX
return_to: uth-onboarding
```

普通 `/uth-docs` 模式不回跳：

- `rules-maintenance`
- `context-bootstrap`
- `scoped-sync`
- `state-cleanup`
- `archive-cleanup`
- `snapshot`
- `migration`

这些模式应在 `/uth-docs` 内自收口。若发现需要 Git，下一路由是 `/uth-git`；若发现需要 ADR 决策内容，下一路由是 `/uth-design`；若发现需要代码或测试修改，下一路由是 `/uth-dev` 或 `/uth-debug`。

## 完成边界

### 老项目接管完成

只有满足以下条件，才能称为老项目接管完成：

- 前置 onboarding 已完成：项目标记、语言偏好、hook tools、备份 zip、handoff snapshot、完整 docs 骨架。
- `uth-docs onboarding-followup` 已完成：旧文档分类、当前事实快照、context 重建、current-state 清理、归档或清理旧文档。
- 没有未分类旧文档。
- 没有以 `Needs uth-docs confirmation from code facts` 形式残留的接管范围内事实。
- 没有接管范围内的活跃待办被写成“后续处理”后仍声称完成。
- 所有被删除或从原位置移走的旧文档，都能在本次备份 zip 中找到对应备份。
- 已告知用户备份 zip 的具体路径。

### `uth-docs` 普通场景完成

普通 `uth-docs` 的完成边界由所选 mode 决定：

- `context-bootstrap`：如果项目没有可信文档基线，应进入 full-project baseline；项目过大时，先询问是否按模块拆分。
- `scoped-sync`：只在已有可信全项目基线时允许按指定 diff、range、版本或模块范围同步；同步后必须确认基线仍可信。
- `state-cleanup`：只要求 current-state 清理完成，不要求迁移旧文档，但不能把未确认事实写成已确认事实。
- `archive-cleanup`：只要求指定完成项已归档，且 current-state 不再把它们列为活跃。
- `rules-maintenance`：只要求规则或模板变更完成并通过 UTF-8/fence 检查。
- `migration`：只要求指定旧文档迁移完成；若迁移范围不等于全量接管，不能声称接管完成或项目完整文档治理完成。
- `module-split`：项目过大时先拆分模块、写入 context 索引和拆分报告，停下来等用户确认；它本身不能声称项目完整文档治理完成。

普通场景发现阻塞时，应输出“blocked”或“partial/paused”，并明确下一步需要用户确认或切换场景，不能以完成报告掩盖阻塞。

## 阻塞与询问规则

只有项目过大、模块边界无法一次确认、旧文档可信度无法由有限代码事实判断、或用户要求超出当前场景写入范围时，才停下来询问用户。

询问前必须说明：

- 已完成哪些接管步骤。
- 当前卡在哪个判定点。
- 用户需要在什么选项中做选择。
- 继续后会影响哪些文档范围。

如果不是这些阻塞，agent 应继续完成文档治理，不应把未完成工作写成待办后收口。

## Hook 与证据设计

L3 closeout 需要新增或强化老项目接管证据字段。建议最少包括：

```text
takeover_session_id
takeover_scope
handoff_snapshot_path
backup_zip_path
docs_completion_level
full_project_baseline_completed
baseline_source_scope
baseline_excluded_paths
baseline_still_trusted
module_split_required
module_split_confirmed_by_user
module_split_report_written
module_context_index_written
module_queue
module_current
module_completed
module_pause_after_each_completed
lw_final_record_written
handoff_prompt_for_new_window
docs_followup_completed
old_docs_discovered
old_docs_classified
old_docs_unclassified_count
current_state_cleaned
context_rebuilt_or_confirmed
cleanup_paths_verified_in_backup_zip
active_takeover_blockers
backup_zip_reported_to_user
return_to_onboarding
```

`uth-docs onboarding-followup` 若声称完成，应阻断以下情况：

- `docs_completion_level` 不是 `full-project-docs-complete`。
- `full_project_baseline_completed` 不是 true。
- `old_docs_unclassified_count` 大于 0。
- `active_takeover_blockers` 非空。
- `current_state_cleaned` 不是 true。
- `context_rebuilt_or_confirmed` 不是 true。
- `cleanup_paths_verified_in_backup_zip` 不是 true，且本次清理删除或移动了原位置旧文档。
- 接管范围内仍有 `Needs uth-docs confirmation from code facts`。

普通 `uth-docs` 若声称 `full-project-docs-complete`，应阻断以下情况：

- 没有 `full_project_baseline_completed`。
- 没有记录 `baseline_source_scope`。
- 没有记录排除范围或排除理由。
- 仍存在未读关键模块、未确认入口、未确认验证路径或未解决文档冲突。
- `module_split_required` 为 true，但模块队列尚未全部完成。

普通 `uth-docs` 若声称 `scoped-docs-complete`，应阻断以下情况：

- 没有既有可信 baseline。
- 没有记录本次 diff、range、版本、模块或文件范围。
- 影响范围追踪不完整。
- 更新后没有确认 `baseline_still_trusted`。

`uth-docs module-split` 或大项目拆分流程应阻断以下情况：

- 用户尚未允许模块拆分。
- `module_split_report_written` 不是 true。
- `module_context_index_written` 不是 true。
- 没有输出模块列表和治理顺序。
- 没有在拆分完成后停下来等待用户确认。

逐模块治理应阻断以下情况：

- 完成一个模块后没有停下来等待用户确认。
- 模块 context 报告缺少代码事实来源。
- 未更新 `module_completed` 和 `module_queue`。
- 上下文过长但没有给出新窗口续跑提示词。
- 跨窗口续跑时没有读取轻量 dev final record。

`uth-onboarding existing-project` 最终总收口若声称接管完成，应额外要求：

- `docs_followup_completed` 为 true。
- `docs_completion_level` 为 `full-project-docs-complete`。
- `return_to_onboarding` 为 true。
- `backup_zip_reported_to_user` 为 true。

## 输出语义

为了避免误导，报告用语需要区分三种状态：

- `前置流程完成`：只允许用于 `/uth-onboarding` 初段。
- `指定范围文档治理完成`：只允许用于 `/uth-docs` 的 scoped 完成。
- `项目完整文档治理完成`：只允许用于 `/uth-docs` 完成或重新确认 full-project baseline。
- `老项目接管完成`：只允许用于回跳后的 `/uth-onboarding` 总收口。

如果用户只要求“启用 UTH，不完整接管旧文档”，`uth-onboarding` 可以停在前置流程，但必须明确写：

```text
仅完成 UTH 启用，未完成老项目接管。
```

## 验证策略

验证应覆盖三层：

- Skill 文案验证：`uth-onboarding`、`uth-docs`、流程图和启动手册中的职责描述一致。
- Hook 单测验证：半成品 `onboarding-followup` 不能通过完成门禁；普通 `uth-docs` 不会回跳 onboarding。
- 文档编码验证：修改后的治理 Markdown 保持 UTF-8、无 BOM、无明显 mojibake，Markdown fence 平衡。

设计完成后，后续实现应优先修改 skill 边界和 L3 evidence gate，再同步 README、启动手册、流程图和测试。
