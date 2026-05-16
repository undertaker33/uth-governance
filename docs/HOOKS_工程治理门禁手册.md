# HOOKS 工程治理门禁手册

> 本手册定义 UTH 工程治理的硬门槛契约。  
> Skill 负责告诉 Agent 怎么做；Hook 负责阻止 Agent 跳过最低治理事实。

---

## 0. 定位

Hook 不是新的研发流程，也不替代 `uth-*` Skill 或 UTH-SP。

Hook 只检查关键动作是否满足最低治理条件：

- 是否已经判定场景。
- 是否在当前场景允许的范围内读写。
- 是否在歧义时澄清或进入 brainstorming。
- 是否在写代码后完成强验证。
- 是否在 Git 写入前获得确认。
- 是否在文档写入时保护 UTF-8。
- 是否在脚本写入时保护 no-BOM，并在环境可用时做语法检查。
- 是否在收口时按场景给出必要证据。

在接入到具体项目时，本手册建议落位为：

```text
docs/_governance/hook-gates.md
```

本治理包的 L1/L2 参考实现位于：

```text
tools/uth-hooks/uth-hook.py
```

它接受 JSON 事件并输出 `PASS` / `WARN` / `ASK` / `BLOCK`。L3 场景收口门禁只检查调用方提供的证据，不主动重复执行编译或测试。

Hook 的目标是防止：

- 没判场景就修改文件。
- 未显式接管的项目误触发 UTH 场景。
- 场景不明还继续开工。
- 跨场景加戏。
- 未授权 Git 写入。
- worker 未记录 Prompt 就派发。
- 未验证却声称完成、修复、通过或可交付。
- 把旧文档或归档文档当当前事实。
- 文档写回后乱码。

---

## 1. 门禁等级

```text
PASS   放行
WARN   提醒并记录，但允许继续
ASK    暂停并请求用户确认，确认后放行
BLOCK  阻断，必须补齐条件或切换场景
```

L0 还会返回 `route_action`，用于区分 `PASS` 的路由含义：

```text
idle                 无工程动作，不触发 UTH
silent               缺少项目 marker，其他 uth-* 子场景保持静默
enter-onboarding    进入 uth-onboarding
enter-scene         已声明场景，可进入对应子场景
yield-skill-creator 让路给 skill-creator
ask                  场景不明，问一个澄清问题
block                缺少必需场景
```

默认规则：

- 涉及 Git 写入、场景不明、硬禁区写入、虚假完成声明时使用 `BLOCK`。
- 涉及合理越界写入时使用 `ASK`。
- 涉及非阻断文档质量、可后续清理事项时使用 `WARN`。
- closeout 字段缺失、证据缺失或格式不完整使用 `BLOCK`，不伪装成用户确认问题。

---

## 2. 运行态状态

Hook 至少需要维护以下运行态信息，可由 wrapper、hook 系统或 Agent 状态文件提供：

```json
{
  "active_scene": "uth-dev",
  "mode": "light-dev",
  "scene_declared": true,
  "ambiguous_state_resolved": true,
  "brainstorming_invoked": false,
  "explicit_no_brainstorm_reason": "scope and acceptance are clear",
  "allowed_writes": ["src/**", "tests/**", "docs/LW-Work/**"],
  "forbidden_writes": ["docs/context/**", "docs/archive/**", "skills/**"],
  "scope_expansions": [],
  "user_git_confirmed": false,
  "verification": {
    "compile_build_pass": false,
    "warnings": null,
    "exceptions": null,
    "evidence": [],
    "waiver_granted": false,
    "waiver_reason": null,
    "user_risk_confirmed": false
  },
  "worker_prompts": [],
  "uth_sp": {
    "decision_recorded": false,
    "selected_methods": [],
    "hard_triggers": [],
    "exemptions": [],
    "no_trigger_reason": null
  },
  "needs_context_sync": false,
  "utf8_guard": {
    "required": false,
    "checked_files": []
  },
  "script_guard": {
    "required": false,
    "checked_files": [],
    "syntax_checked": [],
    "syntax_skipped": []
  }
}
```

运行态状态不是项目事实源，不进入 `docs/context/`。

L3 closeout 事件常用字段：

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

Design 小补丁授权字段可使用：

```json
{
  "design_patch_authorized": true
}
```

或在场景切换事件中使用：

```json
{
  "transition": {
    "authorized_design_patch": true
  }
}
```

---

## 3. L0 Router Gate

触发：

- 项目或仓库会话开始。
- 用户提出新工程请求。
- 用户中途改变目标。
- 用户要求继续之前任务。

检查：

```text
当前项目是否存在 .uth-governance/project.json？
是否显式调用 skill-creator？
是否显式调用 uth-onboarding 或要求启用 UTH？
是否命中 uth-* 场景？
是否多场景？
是否场景不明？
```

规则：

- 显式 `skill-creator`：`PASS`，让路。
- 显式 `uth-onboarding` 或显式 UTH 启用 / 接管：`PASS`，进入 onboarding。
- 缺少 `.uth-governance/project.json` 且不是 onboarding / 安装 / 显式启用：`PASS` + `route_action=silent`，保持 UTH 静默，不路由其他 `uth-*` 场景。
- 场景明确：`PASS`，记录一行 `Scene: uth-dev/debug/...`。
- 多场景：`PASS`，选择第一个执行场景，后续场景收口交接。
- 场景不明：`BLOCK`，只问一个澄清问题。
- 无工程动作：`PASS`，不触发 UTH，不触发 UTH-SP。

---

## 4. L1 Process Gate

触发：

- 准备从只读进入写入。
- 准备从 design 进入 dev。
- 准备从 debug 进入 feature work。
- 准备从 review 进入修复。
- 准备从 docs 进入 Git。
- 准备派发 worker。
- 准备调用或豁免 UTH-SP 方法 Skill。
- 当前任务范围扩大。

### 4.1 Ambiguity / Brainstorm Gate

场景不清：

```text
BLOCK -> 由 uth-governance 问一个澄清问题
```

场景已清，但任务内存在歧义：

```text
要求满足其一：
- brainstorming_invoked = true，且使用 uth-sp-brainstorming
- ambiguous_state_resolved = true
- explicit_no_brainstorm_reason 存在
```

否则：

```text
BLOCK -> 进入对应子 Skill 的澄清 / brainstorming 判断
```

说明：

- L1 只要求 Agent 在歧义处停下来给出判断，不要求每次都进入 `uth-sp-brainstorming`。
- `explicit_no_brainstorm_reason` 必须具体说明目标、范围、验收和影响面为什么已经明确。
- “用户说简单改一下”“看起来不复杂”不能作为不进入澄清 / brainstorming 的理由。

### 4.2 Scene Transition Gate

规则：

- `design -> dev`：必须切换到 `uth-dev`，除非是用户授权的 design 小补丁。
- `debug -> feature`：如果从修 bug 变成新需求，必须切换 `uth-dev` 或 `uth-design`。
- `review -> fix`：review 不直接修复；先切 `uth-debug` 或 `uth-dev`。
- `docs -> git`：必须切 `uth-git`。
- `any -> git`：必须切 `uth-git` 且用户确认。
- `any -> docs/context`：必须切 `uth-docs`。
- `any -> skills`：必须是显式 Skill 维护任务，并使用 `skill-creator` 或等价 Skill 写作流程。

越界转换未显式交接时：

```text
BLOCK
```

### 4.3 Worker Dispatch Gate

规则：

- `worker` 派发前必须有当前正式任务包 Prompt。
- Prompt 必须先写入 `docs/work/D*/prompts/`，再用短提示词派发 worker 去读取。
- 同一 worker 返工追加原 Prompt，不新建 Prompt 文件。
- `planner` / `evaluator` 只读，不记录 Prompt。
- worker 不允许 Git 写入。
- 轻量 dev 通常不派 worker；如果确实派 worker，必须升级为正式任务包或先获得用户确认。

未满足时：

```text
BLOCK
```

### 4.4 UTH-SP Trigger Decision Gate

触发：

- 准备进入 `uth-dev` / `uth-debug` / `uth-design` / `uth-review` / `uth-git` 的具体执行。
- 准备声称“不需要 UTH-SP”。
- 准备执行一个被 UTH-SP 覆盖的成熟方法流程。

要求子场景给出最小判断：

```text
UTH-SP 触发判断：
- 命中的硬触发：
- 选择的 uth-sp-*：
- 满足的豁免条件：
- 未触发原因：
```

规则：

- `uth-governance` 不直接触发 UTH-SP；只要求路由到子场景。
- 子场景必须负责 UTH-SP 判断。
- 命中硬触发时，必须进入对应 `uth-sp-*` 方法 Skill。
- 不触发时必须说明具体豁免条件。
- L1 只检查“是否做出触发判断”；完整 evidence gate 放到后续增强，不在第一阶段硬拦所有场景。

缺少触发判断时：

```text
BLOCK -> 回到当前子场景补齐 UTH-SP 判断
```

---

## 5. L2 Tool Gate

### 5.1 File Write Gate

写文件前检查目标路径。

```text
if path in allowed_writes:
  PASS

if path in hard_forbidden:
  BLOCK

if path outside allowed_writes but not hard_forbidden:
  ASK user for temporary scope expansion
```

硬禁区：

```text
.git/**
skills/**                         # 仅显式 Skill 维护任务可写，维护流程使用 skill-creator 或等价流程
skills/uth-sp-*/**                # 仅显式 UTH-SP 方法 Skill 维护任务可写；同样使用 skill-creator 或等价流程
docs/context/**                   # 仅 uth-docs 可写
docs/archive/**                   # 仅 uth-docs 可写
docs/decisions/ADR-*.md           # 仅 uth-design 可写正文/状态
docs/changelogs/**                # 仅 uth-git / release flow 可写正文
```

超范围但非硬禁区时，向用户确认：

```text
目标文件超出当前允许写入范围：
- <path>

原因：
- <reason>

风险：
- <risk>

是否允许临时扩展写入范围？
```

用户确认后记录：

```json
{
  "path": "<path>",
  "reason": "<reason>",
  "approved_by_user": true
}
```

Skill 维护说明：

- 普通 `uth-dev` / `uth-debug` / `uth-review` / `uth-docs` 不允许顺手修改 `skills/**`。
- 修改任意 Skill 时，应显式进入 Skill 维护语境，并使用 `skill-creator`。
- 修改 `skills/uth-sp-*/**` 时，还必须明确这是 UTH-SP 方法 Skill 维护，不是普通业务任务。
- 上游包同步属于人工维护流程，不作为普通工程 hook 的默认检查项。

### 5.2 Git Write Gate

以下全部视为 Git 写入：

```text
git add
git commit
git push
git tag
git merge
git rebase
git switch / checkout 修改分支或工作区
创建/删除/重命名 branch
创建/删除 worktree
```

要求：

- `active_scene = uth-git`
- 已展示 Git 计划。
- 用户已明确确认。
- release/tag 场景满足 changelog 规则。

否则：

```text
BLOCK
```

### 5.3 UTF-8 Doc Guard

触发：

- 修改 `AGENTS.md`
- 修改根目录 `README.md`
- 修改 `docs/**/*.md`
- 修改任务包 Markdown
- 显式 `skill-creator` 下修改 `skills/**/*.md`
- 显式 UTH-SP 维护下修改 `skills/uth-sp-*/**/*.md`

要求：

- 写前调用 `uth-utf8-guard` 或等价 UTF-8 检查。
- 写后再次调用 `uth-utf8-guard` 或等价 UTF-8 检查。
- 检查 UTF-8 解码、明显乱码、Markdown 代码围栏平衡。

失败时：

```text
BLOCK -> 修复文档编码后再收口
```

### 5.4 Script Guard

触发：

- 修改 `.sh`
- 修改 `.js`
- 修改 `.cjs`
- 修改 `.mjs`
- 修改 `.py`
- 修改 `.ps1`
- 修改带 shebang 的脚本文件
- 当前任务声称脚本可执行、已验证或可交付

基础检查必须执行：

```text
- 文件可 UTF-8 解码
- 无 UTF-8 BOM
- shebang 前无隐藏字符
- 文件不是空脚本
```

条件语法检查：

```text
.js / .cjs / .mjs:
  if node exists:
    run node --check <file>
  else:
    WARN -> record skipped reason

.sh:
  if bash exists:
    run bash -n <file>
  else:
    WARN -> record skipped reason

.py:
  run Python syntax compile without writing pyc files

.ps1:
  if PowerShell parser is available:
    run parser/tokenizer syntax check
  else:
    WARN -> record skipped reason
```

环境缺失时：

```text
WARN
```

但以下情况必须 `BLOCK`：

- 本次修改目标就是该脚本，且脚本是交付物或关键执行入口。
- 用户或场景要求“脚本可执行 / 可运行 / 已验证”。
- Agent 准备声称脚本验证通过。

收口必须列出：

```text
脚本守卫：
- UTF-8：
- no-BOM：
- syntax check：
- skipped：
- 风险：
```

---

## 6. L3 Closeout Gate

### 6.1 全局完成声明规则

准备声称以下状态时触发：

- 完成了。
- 修好了。
- 测试通过。
- 编译通过。
- 可交付。
- 可以提交。
- ready。

要求：

- 有新鲜验证证据；或
- 明确声明未验证，且不声称完成 / 通过 / 可交付。

否则：

```text
BLOCK
```

### 6.2 Code Change Verification Gate

适用：

- `uth-dev` 修改代码。
- `uth-debug` 修改代码。
- `uth-design` 在用户授权下做少量代码补丁。

强治理规则：

```text
代码改动后必须有编译 / 构建通过证据，且 0 warning、0 exception。
```

不接受历史 warning baseline 作为默认豁免。

首次启动 UTH 代码修改场景时，如果项目存在 warning / exception：

- 必须先清理到 0 warning / 0 exception；或
- 如果确实清不掉、后续单独清理更合理，先询问用户是否给出临时豁免。

临时豁免后：

- 不允许声称“完成 / 可交付 / 通过”。
- 收口必须写明编译门槛未达成。
- 后续 Git / release 应继续阻断，除非用户明确承担风险。
- Hook 对非零 warning / exception 且未给出豁免的场景返回 `ASK`，要求调用方询问用户或回到代码场景清理。

### 6.3 uth-onboarding closeout

检查：

- mode 是 `new-project` 或 `existing-project`。
- 已创建 `.uth-governance/project.json`。
- 已复制项目本地 `tools/uth-hooks/`。
- 已创建或更新 `docs/current-state.md` 初始索引。
- 已选择并持久化 `document_language` 到 `.uth-governance/project.json`。
- 修改治理 Markdown 时已通过 UTF-8 Guard。
- 没有修改业务源码或测试。
- 没有执行 Git 写入。

`existing-project` 还必须检查：

- 已创建 `docs/ONBYYMMDDXX-pre-uth-docs-backup.zip`。
- 已创建 `docs/snapshots/ONBYYMMDDXX-existing-project-handoff.md`。
- 已标记旧文档、未确认事实和 `uth-docs` 待处理事项。
- 下一场景是 `uth-docs`，除非用户明确暂停。

### 6.4 uth-dev closeout

检查：

- changed files 已列出。
- 编译通过，0 warning，0 exception。
- 其他必要验证已运行，或明确未验证且不声称完成。
- light-dev：任务完成时已写最终 LW 记录。
- formal-dev：已写 Feedback，或说明为什么未写。
- formal-dev：Feedback 不等待 Git 信息；Git baseline 由 `uth-git` 在 Git 写入成功后追加。
- current-state 只在活跃任务状态变化时更新。
- 如模块事实变化，标记 `Needs uth-docs context-sync`。
- 未执行 Git 写入。

### 6.5 uth-debug closeout

检查：

- root cause 已说明，或明确仍未知。
- fix scope 已说明。
- 修复后编译通过，0 warning，0 exception。
- 复现 / 验证证据已列出。
- formal debug 必要时写 Feedback / Run Log。
- blocker / baseline 变化时更新 current-state。
- 如模块事实变化，标记 `Needs uth-docs context-sync`。

### 6.6 uth-design closeout

默认不改代码。

如果设计过程中发现小型逻辑错误，需要少量代码补丁：

```text
ASK user for design-assisted patch
```

用户确认后允许小范围修改，但必须：

- 说明为什么不切 `uth-dev` / `uth-debug`。
- 列出文件和风险。
- 不顺手实现新功能。
- 不做重构。
- 改完后触发 Code Change Verification Gate。

Hook 字段：

```text
design_patch_authorized = true
或 transition.authorized_design_patch = true
```

如果补丁范围扩大：

```text
BLOCK -> 切换 uth-dev 或 uth-debug
```

设计收口还需检查：

- mode 明确。
- recommendation / open questions 明确。
- Design 只在需要时写。
- ADR 只在用户接受长期决策后写。
- current-state 只作为索引更新。
- implementation 请求交给 `uth-dev`。

### 6.7 uth-review closeout

检查：

- findings-first。
- code files not modified；如需要修复，必须切 `uth-debug` 或 `uth-dev`。
- acceptance basis 已说明。
- 验证证据已列出，或明确 static-review-only。
- recommendation 是 pass / fail / pass with risk / needs follow-up。
- 需要修复时路由到 `uth-debug` 或 `uth-dev`，不在 review 内直接修。
- `pass with risk` 且存在 warning / exception 时，必须有用户风险豁免。

### 6.8 uth-docs closeout

检查：

- mode 已说明。
- read / written 已列出。
- 修改治理 Markdown 前，项目已有 `document_language`，或本次已询问用户并持久化到 `.uth-governance/project.json`。
- 修改 `AGENTS.md`、根 `README.md`、`docs/**/*.md` 时已通过 UTF-8 Guard。
- context touched 时提供 `context_source_evidence`，或提供 `context_source_omitted_reason`；不因等待 Git baseline 阻断文档报告。
- archive touched 时列出迁移前后路径，并确认 current-state 不再列为 active。
- ADR / changelog 边界未越界。
- verification 写明 documentation-only，没有跑检查 / 测试。
- 如需 Git，路由到 `uth-git`。

### 6.9 uth-git closeout

检查：

- 用户确认存在。
- 执行命令已列出。
- 最终 branch / status 已说明。
- commit / PR / tag / release 证据已列出。
- release/tag 满足 changelog 规则。
- light-dev Git 写入成功后，已向现有 LW final record 追加 Git baseline；如需把该追加纳入 Git，必须重新展示 diff 并再次确认。
- formal task Git 写入成功后，已向关联 Feedback 追加 Git baseline，或说明无法追加原因。
- push/tag/merge 等结果有新鲜验证。
- 只生成 Git plan、未执行 Git 写入时，不要求 `user_git_confirmed`，但必须有 `git_plan_present=true` 或 `plan_only=true`，并明确 no Git writes executed。

### 6.10 uth-context-trace closeout

检查：

- anchors used 已列出。
- active / archived evidence 已区分。
- current fact sources 与 historical-only evidence 已分开。
- missing / unclear docs 已说明。
- recommended next scene 已说明。
- files modified = none。

---

## 7. 当前实现状态

当前参考 runner 已实现：

```text
H1 scene-required-before-write
H2 ambiguity-brainstorm-decision
H3 scope-write-confirmation
H4 no-git-without-uth-git-confirmation
H5 code-change-compile-zero-warning
H6 no-worker-without-prompt
H7 utf8-doc-guard
H8 script-guard
H9 per-scene-closeout
Context-source closeout gate for docs/context/** changes
Archive write-scope gate
Archive cleanup closeout gate
Generic positive-claim evidence gate
Code verification evidence gate
```

仍待实现或硬化：

```text
UTH-SP-required-evidence gate
Archive-read gate
Current-state-staleness gate
Broader context-source freshness/staleness gate
```

说明：

- `Context-source` 已在 `uth-docs` L3 closeout 中实现基础门禁：修改 `docs/context/**` 时必须提供 `context_source_evidence` 或 `context_source_omitted_reason`。
- `Archive` 目前已覆盖写入范围和归档清理收口，但没有独立的 archive-read 事件或读取门禁。
- `Current-state` 目前只在 onboarding、dev/debug/review/docs/git 等场景中作为写入范围或收口事实检查的一部分；尚未实现 stale / length / active-index consistency 这类新鲜度门禁。
- `UTH-SP` 目前 L1 只检查是否记录触发判断；尚未校验 hard trigger 是否对应 selected method，也未要求 UTH-SP 执行证据。

UTH-SP 触发层改造完成后，再把 UTH-SP evidence gate 变成硬门槛。

---

## 8. 设计原则

- Hook 拦关键动作，不替代 Agent 思考。
- 强门槛优先放在写入、Git、派工、完成声明和文档编码。
- 合理越界允许用户授权，不让流程僵死。
- 归档和旧文档只作历史证据。
- 文档 UTF-8 守卫只覆盖治理文档，不全局扫描所有代码。
- 脚本守卫只覆盖脚本文件和可执行交付物；环境缺失要记录 WARN，不伪装为通过。
- dev/debug 强治理以 0 warning / 0 exception 为收口门槛。
