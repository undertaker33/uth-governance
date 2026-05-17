# HOOKS 工程治理门禁手册

> 本手册只定义可执行 Hook 契约。
> 场景教程、模板写法和完整流程分别见 `docs/AGENT_工程治理启动手册.md`、`docs/FLOW_全链路流程图.md`、`docs/TEMPLATES_工程治理模板.md`。

---

## 0. 定位

Hook 不替代 `uth-*` Skill、UTH-SP 或人工判断。Hook 只检查关键动作前后的最低治理事实：

- 路由前：是否应该触发 UTH，是否存在项目 marker，是否已声明场景。
- 过程前：是否存在歧义、场景越界、worker 派发缺少 Prompt、UTH-SP 触发判断缺失。
- 写入前：文件路径、Git 写入、治理 Markdown 编码、脚本可执行性是否满足硬条件。
- 收口前：完成声明、代码验证、场景边界、文档语言、docs/onboarding 接管证据是否齐全。

参考 runner：

```text
tools/uth-hooks/uth-hook.py
```

输入是 JSON event，可用 `type` 或 `event_type` 指定事件；输出为：

```json
{
  "schema_version": "uth-hook-result/v1",
  "decision": "PASS|WARN|ASK|BLOCK",
  "event_type": "<normalized-event-type>",
  "findings": []
}
```

L0 findings 可携带 `route_action`；若存在，最终响应也会把第一个 `route_action` 提升到顶层。

Hook 只检查调用方提供的事实和证据。L3 不主动重跑编译、测试、文档扫描或 Git 命令。

---

## 1. 门禁等级

```text
PASS   放行
WARN   记录非阻断风险，允许继续
ASK    暂停并要求用户确认；确认后由调用方重新提交事实
BLOCK  阻断；必须补齐事实、修复问题或切换场景
```

L0 `route_action` 合法语义：

```text
idle                 无工程动作，不触发 UTH
silent               无 .uth-governance/project.json，其他 uth-* 子场景静默
enter-onboarding    显式 uth-onboarding / UTH enable / takeover
enter-scene         已声明 active_scene 或 requested_scene
yield-skill-creator 显式 skill-creator 工作让路
ask                  场景不明，只问一个澄清问题
block                UTH-enabled 工程动作缺少必需场景
```

默认判定：

- Git 写入缺少 `active_scene="uth-git"`、`git_plan_present=true` 或 `user_git_confirmed=true`：`BLOCK`。
- 场景不明、硬禁区写入、虚假完成声明：`BLOCK`。
- 超出当前允许写入范围但非硬禁区：`ASK`。
- 环境缺失导致非关键语法检查跳过：`WARN`。
- closeout 字段或证据缺失：`BLOCK`，不转成用户确认问题。

---

## 2. 运行态状态

运行态状态由 wrapper、hook 调用方或 Agent 会话维护，不是项目事实源，不写入 `docs/context/`。

最小事件字段示例：

```json
{
  "type": "l3-closeout",
  "active_scene": "uth-dev",
  "mode": "light-dev",
  "changed_files": ["src/example.py"],
  "claims": [],
  "verification": {
    "compile_build_pass": true,
    "warnings": 0,
    "exceptions": 0,
    "evidence": ["command output summary"],
    "waiver_granted": false,
    "waiver_reason": null,
    "user_risk_confirmed": false
  }
}
```

核心字段契约：

| 字段 | 契约 |
| --- | --- |
| `active_scene` | 当前执行场景；L1/L2/L3 的主路由字段。L3 仅接受 `uth-onboarding`、`uth-dev`、`uth-debug`、`uth-design`、`uth-review`、`uth-docs`、`uth-git`、`uth-context-trace`。 |
| `route_action` | L0 输出字段，不由调用方伪造业务完成状态。 |
| `next_scene` | 下一场景意图；`next_scene="uth-git"` 会触发代码豁免后的 Git 风险确认。 |
| `next_mode` | 下一场景模式；`next_scene="uth-docs"` 且 `next_mode="onboarding-followup"` 表示老项目 full-takeover docs follow-up。 |
| `git_plan_present` | Git 写入或 Git plan-only 收口证据；Git 写入前必须为 true。 |
| `user_git_confirmed` | 用户已明确授权 Git 写入；Git 写入前和 Git 写入收口都需要。 |
| `document_language_code` | 本次事件提供的项目文档语言代码，例如 `zh-CN` 或 `en-US`。 |
| `project_document_language_code` | 与 `document_language_code` 等价的项目级文档语言代码。二者至少一个存在，才能执行治理 Markdown 语言/文件名检查。 |
| `module_split_confirmed_by_user` | `uth-docs` 的 `module-split` 模式继续前，必须有用户确认；缺失返回 `ASK`。 |
| `module_context_files` | 本次写入或更新的模块上下文 Markdown；会参与治理 Markdown、模块文件名编号和 `00-` 保留规则检查。 |
| `docs_followup_completed` | 老项目 full-takeover 最终收口字段，只能在独立 `uth-docs onboarding-followup` 完成后作为证据。preflight 阶段不得提前提供。 |
| `return_to_onboarding` | `uth-docs onboarding-followup` 完成后返回 `uth-onboarding` 总收口的证据。preflight 阶段不得提前提供。 |

治理 Markdown 写入时，`document_language_code` 和 `project_document_language_code` 的取值规则是：

```text
effective_document_language_code =
  document_language_code 或 project_document_language_code
```

---

## 3. L0 Router Gate

事件别名：

```text
l0
l0-router
router
preflight
```

输入检查与结果：

| 条件 | 结果 |
| --- | --- |
| `no_engineering_action=true` 或 `engineering_action` 不为 true | `PASS` + `route_action=idle` |
| `skill_creator_active=true` 或 `explicit_skill_creator=true` | `PASS` + `route_action=yield-skill-creator` |
| `explicit_onboarding=true`、`explicit_uth_enable=true` 或 `explicit_uth_takeover=true` | `PASS` + `route_action=enter-onboarding` |
| 缺少 `.uth-governance/project.json` | `PASS` + `route_action=silent` |
| marker JSON 无效、schema 不为 `uth-governance-project/v1`、`enabled` 不是 true、必需 entrypoints 缺失 | `BLOCK` |
| `scene_ambiguous=true` | `BLOCK` + `route_action=ask` |
| `active_scene` 或 `requested_scene` 存在 | `PASS` + `route_action=enter-scene` |
| UTH-enabled 工程动作缺少场景 | `BLOCK` + `route_action=block` |

L0 只做路由，不展开场景教程。场景选择说明见 `docs/AGENT_工程治理启动手册.md`。

---

## 4. L1 Process Gate

事件别名：

```text
l1
l1-process
process
```

字段检查：

| 检查 | 通过条件 | 失败结果 |
| --- | --- | --- |
| 场景存在 | `active_scene` 非空，且 `scene_ambiguous` 不为 true | `BLOCK scene-ambiguous` |
| 任务歧义 | `ambiguity.present` 不为 true，或 `ambiguity.brainstorming_invoked=true`，或 `ambiguity.resolved=true`，或 `ambiguity.explicit_no_brainstorm_reason` 非空 | `BLOCK ambiguity-unresolved` |
| 场景切换 | 受限 transition 必须有 `transition.explicit_handoff=true`；design 小补丁可用 `transition.authorized_design_patch=true` | `BLOCK` 或 `ASK` |
| worker 派发 | `worker.role="worker"` 时必须 `worker.prompt_written=true` 且 `worker.prompt_path` 非空；worker 不得 `git_write_allowed=true` | `BLOCK` |
| light-dev 派发 worker | `mode="light-dev"` 且派发 worker 时，需要 `worker.user_confirmed_worker=true` | `ASK` |
| planner/evaluator | `worker.role` 为 `planner` 或 `evaluator` 时不应写 Prompt | `WARN` |
| UTH-SP 判断 | `require_uth_sp_decision=true` 或当前场景属于代码相关场景时，`uth_sp.decision_recorded=true` | `BLOCK uth-sp-decision-missing` |

受限 transition 契约：

```text
uth-design -> uth-dev          需要 explicit_handoff
uth-design -> code-patch/debug 需要 authorized_design_patch，否则 ASK
uth-debug  -> feature/dev/design 需要 explicit_handoff
uth-review -> fix/dev/debug    需要 explicit_handoff
any        -> uth-git          需要 explicit_handoff
```

UTH-SP 这里只检查是否记录触发判断，不检查方法 Skill 的完整执行证据。

---

## 5. L2 Tool Gate

### 5.1 File Write Gate

事件别名：

```text
file-write
write
pre-write
```

路径来源：`paths` 或单个 `path`。

判定顺序：

1. 归一化路径。
2. 检查硬禁区。
3. 检查当前场景 forbidden patterns。
4. 检查 `extra_hard_forbidden`。
5. 匹配 `default_allowed_writes`、`scene_write_rules[active_scene]`、`allowed_writes`、已批准 `scope_expansions`。

硬禁区：

| 路径 | 契约 |
| --- | --- |
| `.git/**` | 永远 `BLOCK`。 |
| `skills/uth-sp-*/**` | 仅 `skill_creator_active`/`explicit_skill_maintenance`/`active_scene="skill-creator"` 且 `explicit_uth_sp_maintenance=true` 时放行。 |
| `skills/**` | 仅显式 Skill 维护语境放行。 |
| `docs/context/**` | 仅 `active_scene` 为 `uth-docs` 或 `uth-onboarding`。 |
| `docs/archive/**` | 仅 `active_scene` 为 `uth-docs` 或 `uth-onboarding`。 |
| 全局 `docs/*.md` 治理文档 | 仅文档治理允许的场景。 |
| `docs/decisions/ADR-*.md` | 仅 `uth-design`。 |
| `docs/changelogs/**` | 仅 `uth-git`；onboarding scaffold index 例外。 |

非硬禁区但不在允许范围：`ASK write-scope-expansion`。

### 5.2 Git Write Gate

事件别名：

```text
git-write
git
```

写入命令包括但不限于：

```text
git add / commit / push / tag / merge / rebase / switch / checkout / branch ...
git reset / restore / rm / mv / clean / fetch / stash / pull / cherry-pick / revert
git worktree add|remove|move|prune|repair
gh pr checkout|create|merge|edit|close|reopen|ready
gh release create|delete|edit|upload
```

只读命令如 `git status`、`git diff`、`git log`、`git show`、`gh pr view`、`gh run view` 不触发写入阻断。

Git 写入放行条件：

```text
active_scene = "uth-git"
git_plan_present = true
user_git_confirmed = true
release_or_tag=true 时 changelog_ok=true
```

缺任一条件：`BLOCK`。

### 5.3 UTF-8 Doc Guard

事件别名：

```text
utf8-doc
utf8
doc-guard
```

触发范围：

```text
AGENTS.md
README.md
docs/**/*.md
任务包 Markdown
显式 skill-creator 下的 skills/**/*.md
显式 UTH-SP 维护下的 skills/uth-sp-*/**/*.md
```

检查项：

- 文件存在。
- UTF-8 可解码。
- 无明显 mojibake marker。
- Markdown 代码围栏成对。

失败：`BLOCK`。通过：逐文件 `PASS utf8-doc-pass`。

### 5.4 Script Guard

事件别名：

```text
script-guard
script
```

触发范围：

```text
.sh
.js
.cjs
.mjs
.py
.ps1
带 shebang 的脚本
声称脚本可执行、已验证或可交付的文件
```

基础硬检查：

```text
UTF-8 可解码
无 UTF-8 BOM
shebang 前无隐藏字符或空白
非空脚本
```

语法检查：

```text
JS/CJS/MJS: node --check 可用则执行
SH:        bash -n 可用则执行
PY:        Python compile，且不写 pyc
PS1:       PowerShell parser/tokenizer 可用则执行
```

语法工具缺失时通常 `WARN`；如果调用方正在声称脚本验证通过，或脚本是本次关键交付入口，则缺失/失败必须 `BLOCK`。

---

## 6. L3 Closeout Gate

事件别名：

```text
l3
l3-closeout
closeout
```

L3 支持的 `active_scene`：

```text
uth-onboarding
uth-dev
uth-debug
uth-design
uth-review
uth-docs
uth-git
uth-context-trace
```

全局检查：

| 检查 | 契约 |
| --- | --- |
| 正向完成声明 | `claims`、`claim`、`claims_complete`、`claims_fixed`、`claims_passing`、`claims_ready`、`claims_deliverable`、`claims_accepted` 或 `recommendation=pass/accepted/ready/mergeable` 命中时，必须有 `verification.evidence`。 |
| 代码验证 | 代码改动 closeout 必须有编译/构建证据、`compile_build_pass=true`、`warnings=0`、`exceptions=0`。 |
| 非零 warning/exception | 无正向完成声明时可 `ASK` 用户临时豁免；已豁免只能 `WARN`，不能支撑完成/通过/ready 声明。 |
| Git/Release 风险 | 有豁免且 `next_scene="uth-git"`、`git_closure_requested=true` 或 `release_or_tag=true` 时，需要 `user_risk_confirmed=true`。 |
| 治理 Markdown 语言 | 有治理 Markdown 写入时，必须有 `document_language_code` 或 `project_document_language_code`。 |
| 非英文文档文件名 | 非入口治理 Markdown 文件名不能继续使用默认英文治理文件名；`AGENTS.md`、`README.md` 是硬例外。 |

场景字段检查：

| 场景 | 必需字段 / 行为 |
| --- | --- |
| `uth-onboarding` | `mode` 为 `new-project` 或 `existing-project`；`project_marker_written=true`；`current_state_written=true`；`hook_tools_copied=true`；治理 Markdown 写入时 `utf8_guard_passed=true`；不得 `git_write_performed=true`；不得修改源码/测试。 |
| `uth-onboarding` existing-project | `takeover_scope` 必须是 `enable-only` 或 `full-takeover`。 |
| full-takeover preflight | 需要 `backup_zip_created=true`、`handoff_snapshot_created=true`、旧文档分类证据、关键事实证据，并路由到 `next_scene="uth-docs onboarding-followup"`，或 `next_scene="uth-docs"` 且 `next_mode="onboarding-followup"`。不得同时提供 `docs_followup_completed=true`、`return_to_onboarding=true`、`docs_completion_level=full-project-docs-complete` 等内联完成证据。 |
| full-takeover final | 需要 `takeover_final_closeout=true`、`takeover_scope="full-takeover"`、`docs_followup_completed=true`、`docs_completion_level="full-project-docs-complete"`、独立 docs 证据字段至少一个非空：`docs_scene_final_record`、`docs_scene_run_id`、`docs_followup_final_record` 或 `docs_scene_evidence`；还需要 `return_to_onboarding=true`、`backup_zip_reported_to_user=true`、旧文档已分类、无 active takeover blocker、current-state 已清理、context 已重建或确认。 |
| `uth-dev` | 有变更时列出 `changed_files`；代码验证通过；`mode="light-dev"` 时 `lw_final_record_written=true`；formal/todo 模式需要 `feedback_written=true` 或 `feedback_not_written_reason`；不得 Git 写入。 |
| `uth-debug` | 需要 `root_cause` 或 `root_cause_unknown=true`；代码修复需要 `fix_scope`；代码验证通过；不得 Git 写入。 |
| `uth-design` | 默认不改代码；代码补丁需 `design_patch_authorized=true` 或 `transition.authorized_design_patch=true`；范围扩大需切 `uth-dev`/`uth-debug`；不得开始 feature implementation。 |
| `uth-review` | 不得修改源码/测试；代码评审给 `pass/accepted/ready/mergeable` 时强制代码验证；`static_review_only=true` 不得给正向 pass；`pass with risk` 的 warning/exception 需要风险豁免；不得 Git 写入。 |
| `uth-docs` | documentation-only；不得改代码；治理 Markdown 写入需要文档语言和 `utf8_guard_passed=true`；`docs/context/**` 变更需要 `context_source_evidence` 或 `context_source_omitted_reason`；归档清理需要 before/after paths 和 current-state active 清理证据。 |
| `uth-git` | 未执行 Git 写入时，需要 `git_plan_present=true` 或 `plan_only=true`；执行 Git 写入时需要 `user_git_confirmed=true`、`commands_executed`、`final_status`；commit/PR/tag/release 分别需要对应证据；release/tag 需要 `changelog_ok=true`。 |
| `uth-context-trace` | 只读；需要区分 active/current facts 与 historical/archive evidence；需要 `recommended_next_scene` 或明确 none。 |

`uth-docs` 完成级别字段：

```text
docs_completion_level = full-project-docs-complete | scoped-docs-complete | blocked | partial/paused
```

`full-project-docs-complete` 必需：

```text
full_project_baseline_completed = true
baseline_source_scope 非空
baseline_excluded_paths 非空，或 baseline_excluded_reason 非空
无 unread / unconfirmed / unresolved critical facts
module_split_required=true 时 module_queue 为空
```

`scoped-docs-complete` 必需：

```text
trusted_full_project_baseline = true
scoped_source_scope / git_range / commit / tag / module_scope 至少一个非空
scoped_impact_traced = true
baseline_still_trusted = true
```

`module-split` 必需：

```text
module_split_confirmed_by_user = true        # 缺失返回 ASK
module_split_report_written = true
module_split_plan_path 非空，且文件名以 00- 开头
module_context_index_written = true
module_queue 非空
paused_for_user_confirmation = true
```

`module-governance` 必需：

```text
module_context_files 文件名必须使用两位数字前缀；普通模块不能占用 docs/context/00-*.md
module_context_report_written=true 时 module_source_evidence、module_completed、module_queue 必须存在
module_completed 非空时必须有 module_split_plan_path 且 module_order_followed=true
context_too_long=true 时需要 lw_final_record_written=true 和 handoff_prompt_for_new_window
resumed_from_new_window=true 时需要 read_lw_final_record=true
```

---

## 7. 当前实现状态

已实现事件：

```text
L0: l0 / l0-router / router / preflight
L1: l1 / l1-process / process
L2: file-write / write / pre-write
L2: git-write / git
L2: utf8-doc / utf8 / doc-guard
L2: script-guard / script
L3: l3 / l3-closeout / closeout
```

未知事件类型返回：

```text
BLOCK unknown-event-type
```

已实现门禁：

```text
L0 router 与 project marker 校验
L1 scene / ambiguity / transition / worker / UTH-SP decision presence
L2 write scope / Git write / UTF-8 doc / script guard
L3 per-scene closeout
positive-claim evidence gate
code verification evidence gate
document_language_code / project_document_language_code gate
non-English governance filename gate
docs/context source evidence gate
archive write scope 与 cleanup closeout gate
full-project / scoped docs completion gate
module-split / module-governance gate
existing-project onboarding full-takeover preflight/final gate
```

仍待实现或硬化：

```text
UTH-SP required evidence gate（目前只检查 decision_recorded）
Archive-read 独立读取门禁
Current-state stale / length / active-index consistency 门禁
更广范围的 context-source freshness / staleness 门禁
```

实现状态必须以 `tools/uth-hooks/uth_hooks/` 和 `tools/uth-hooks/tests/` 为准；本手册不得把计划中的门禁写成已实现。

---

## 8. 设计原则

- Hook 拦关键动作，不替代 Agent 推理。
- 契约字段优先于叙事说明；教程放到 AGENT/FLOW/TEMPLATES。
- 写入、Git、派工、完成声明、文档编码、脚本交付是硬门槛。
- 合理越界用 `ASK` 请求用户授权；硬禁区直接 `BLOCK`。
- L3 closeout 检查证据，不重跑昂贵命令。
- 归档和旧文档只能作为历史证据，不能冒充当前事实。
- 代码收口默认要求编译/构建通过且 0 warning、0 exception。
- 文档语言和文件名规则必须由真实项目字段驱动，不能由报告话术替代。
