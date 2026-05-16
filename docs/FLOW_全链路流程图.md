# UTH Governance 全链路流程图

本文件画 UTH Governance 的纵向流程图谱。这里的 `UTH-SP` 指改造后保留在本包内的 `uth-sp-*` 方法 Skill，也就是从 Superpower 流程中拆出并纳入 UTH 调度的成熟方法流程。

详细规则仍以各场景 Skill、`docs/AGENT_工程治理启动手册.md`、`docs/HOOKS_工程治理门禁手册.md` 和 `docs/TEMPLATES_工程治理模板.md` 为准。

## 0. 安装与项目启用边界

```mermaid
flowchart TD
    A["用户要求安装 UTH Governance"] --> B["clone / checkout<br/>uth-governance pack"]
    B --> C["scripts/install.py<br/>只安装全局 skills"]
    C --> D["全局 skills 可被 Agent 发现<br/>uth-* / uth-sp-*"]
    D --> E{"用户是否在目标项目<br/>显式调用 /uth-onboarding？"}
    E -- "否" --> F["不创建项目文档<br/>不创建 .uth-governance/<br/>不安装全局 Hook"]
    E -- "是" --> G["uth-onboarding<br/>项目启用 / 新项目初始化 / 老项目接管"]
    G --> H["复制项目本地 Hook<br/>tools/uth-hooks/"]
    H --> I["创建项目标记<br/>.uth-governance/project.json"]
    I --> J["其他 uth-* 场景开始自动路由"]
```

## 1. 全链路总览

```mermaid
flowchart TD
    A["用户提出工程任务"] --> A1{"显式 uth-onboarding<br/>或 UTH 启用/接管？"}
    A1 -- "是" --> A2["uth-onboarding<br/>项目启用 / 新项目初始化 / 老项目接管"]
    A2 --> A3{"existing-project？"}
    A3 -- "是" --> A4["自动接上 uth-docs<br/>旧文档治理 / context / current-state"]
    A3 -- "否" --> A5["最小接管收口"]
    A4 --> A5
    A1 -- "否" --> B["uth-governance<br/>顶层场景路由"]
    B --> B0{"是否存在<br/>.uth-governance/project.json？"}
    B0 -- "否" --> B1["UTH 静默<br/>按普通 Codex 行为"]
    B0 -- "是" --> C{"是否有工程动作？"}
    C -- "否" --> C1["正常回答<br/>不触发 UTH / UTH-SP"]
    C -- "是" --> D{"场景是否明确？"}
    D -- "否" --> D1["停下澄清一个问题"]
    D1 --> B
    D -- "是" --> E["进入对应 uth-* 子 Skill"]

    E --> F["最小上下文装载<br/>AGENTS / docs README / current-state / 相关任务包"]
    F --> G{"场景内是否有需求、范围、方案、验收歧义？"}
    G -- "是" --> H["UTH-SP / Superpower<br/>uth-sp-brainstorming"]
    G -- "否" --> I["记录 UTH-SP 触发判断"]
    H --> I

    I --> J["Hook L1 Process Gate<br/>场景 / 歧义 / UTH-SP 判断 / worker Prompt"]
    J --> K["场景内执行<br/>design / dev / debug / review / docs / git"]
    K --> L["Hook L2 Tool Gate<br/>写入范围 / Git / UTF-8 / 脚本守卫"]
    L --> M["按场景写回文档<br/>Design / Todo / Feedback / LW-Work / current-state / context"]
    M --> N["Hook L3 Closeout Gate<br/>完成证据 / 强验证 / 豁免"]
    N --> O{"是否达到人类验收口径<br/>并建议 Git 收口？"}
    O -- "否" --> P["场景收口"]
    O -- "是" --> Q["询问用户是否进入 uth-git"]
    Q --> R{"用户确认？"}
    R -- "否" --> P
    R -- "是" --> S["uth-git<br/>计划 / 用户确认 / Git 写入 / 远端验证"]
    S --> P
```

## 2. uth-governance 场景路由

```mermaid
flowchart TD
    A["会话或任务开始"] --> B{"用户显式调用 skill-creator？"}
    B -- "是" --> B1["让路给 skill-creator<br/>不进入 UTH"]
    B -- "否" --> C{"显式 uth-onboarding<br/>或 UTH 启用/接管？"}
    C -- "是" --> C1["进入 uth-onboarding"]
    C -- "否" --> C2{"项目是否有<br/>.uth-governance/project.json？"}
    C2 -- "否" --> C3["UTH 静默<br/>不路由其他 uth-*"]
    C2 -- "是" --> D{"用户显式指定 uth-*？"}
    D -- "是" --> D1["直接进入指定子 Skill"]
    D -- "否" --> E{"是否有工程动作信号？"}
    E -- "否" --> E1["正常回答<br/>不触发 UTH-SP"]
    E -- "是" --> F["分层判断场景"]
    F --> G{"唯一场景命中？"}
    G -- "是" --> H["输出简短场景判定<br/>进入子 Skill"]
    G -- "否，多场景" --> I["选择第一个执行场景<br/>后续场景留到收口交接"]
    G -- "否，不明确" --> J["停下问一个澄清问题"]

    H --> K["Hook L1<br/>scene_declared / no_engineering_action / scene_ambiguous"]
    I --> K
    J --> L["不读全量 docs<br/>不直接开工"]
```

说明：`uth-governance` 不直接调用 UTH-SP / Superpower。UTH-SP 触发判断由进入的子 Skill 负责。

## 2.1 uth-onboarding 项目启用 / 接管

```mermaid
flowchart TD
    A["用户显式要求启用 UTH<br/>或调用 /uth-onboarding"] --> B{"模式"}
    B -- "new-project" --> C["读取最小入口<br/>AGENTS / README / docs / 构建配置 / 目录树"]
    B -- "existing-project" --> D["读取最小入口<br/>旧文档结构 / README / 配置 / 少量 git 基线"]

    C --> E["创建最小文档骨架<br/>docs/README / current-state / context / work / LW-Work / _governance"]
    E --> F["复制项目本地 Hook<br/>tools/uth-hooks/"]
    F --> G["写 .uth-governance/project.json"]
    G --> H1["Hook L3<br/>hook tools + project marker + current-state + UTF-8"]
    H1 --> H["UTH 最小接管完成"]

    D --> I["先备份后续可能影响的文档<br/>docs/ONB*-pre-uth-docs-backup.zip"]
    I --> J["创建接管快照<br/>docs/snapshots/ONB*-existing-project-handoff.md"]
    J --> K["复制项目本地 Hook<br/>tools/uth-hooks/"]
    K --> L["建立 current-state 初始索引<br/>不读全量源码，不声称全仓理解"]
    L --> M["写 .uth-governance/project.json"]
    M --> M1["Hook L3<br/>backup + snapshot + hook tools + marker + current-state"]
    M1 --> N["自动进入 uth-docs<br/>旧文档分类 / context / current-state / 归档"]
```

## 3. uth-design 方案评估 / 架构设计

```mermaid
flowchart TD
    A["用户要求方案评估 / 架构设计 / 技术选型"] --> B["Scene: uth-design"]
    B --> C["读取最小上下文<br/>AGENTS / docs README / current-state / 相关 context"]
    C --> D{"目标、范围、方案、验收是否清楚？"}
    D -- "否" --> E["UTH-SP / Superpower<br/>uth-sp-brainstorming"]
    E --> D
    D -- "是" --> F["Hook L1<br/>记录 UTH-SP 判断"]

    F --> G{"模式"}
    G -- "只读评估" --> H["输出方案、风险、取舍<br/>不写文件"]
    G -- "正式设计" --> I["写 Design<br/>docs/work/D*/00-D*-design.md"]
    G -- "重大长期决策" --> J["写 ADR<br/>docs/decisions/ADR-*.md"]
    G -- "用户接受后要求计划" --> K["UTH-SP / Superpower<br/>uth-sp-writing-plans"]

    I --> L["Hook L2<br/>Design / ADR / current-state 写入范围"]
    J --> L
    K --> L
    L --> M["按需更新 current-state<br/>只做索引"]
    M --> N["Hook L3<br/>设计文档存在、范围清楚、未伪造验证"]
    H --> O["收口：评估结论 / 风险 / 是否交给 uth-dev"]
    N --> P{"是否形成稳定可提交的设计成果？"}
    P -- "是" --> Q["建议 Git 收口<br/>询问用户是否进入 uth-git"]
    P -- "否" --> O
    Q --> R{"用户确认？"}
    R -- "是" --> S["交给 uth-git"]
    R -- "否" --> O
```

补充：`uth-design` 默认不写 Todo；Todo 拆分由 `uth-dev` 负责。设计场景如经用户确认做少量代码补丁，必须走 L2 写入范围和 L3 代码强验证。设计场景是否建议 Git 收口由 Agent 判断，但进入 `uth-git` 仍需用户确认。

## 4. uth-dev 增量开发

```mermaid
flowchart TD
    A["用户要求新增功能 / UI 改动 / Todo 实现"] --> B["Scene: uth-dev"]
    B --> C{"light-dev 还是 formal-dev？"}

    C -- "light-dev" --> D["读取最小上下文<br/>AGENTS / docs README / current-state / 相关代码"]
    D --> E["记录轻量任务边界<br/>场景入口 + allowed scope"]
    E --> F["Hook L2<br/>允许相关代码与 docs/LW-Work/**"]
    F --> G{"是否需要 UTH-SP？"}
    G -- "歧义" --> H["UTH-SP / Superpower<br/>uth-sp-brainstorming"]
    G -- "行为逻辑变化" --> I["UTH-SP / Superpower<br/>uth-sp-test-driven-development"]
    G -- "不需要" --> J["记录不触发理由"]
    H --> J
    I --> J
    J --> K["实现轻量改动"]

    C -- "formal-dev / Todo 实现" --> L["读取 Design + Todo<br/>docs/work/D*/00-design + 10-todo"]
    L --> M{"是否使用 worker subagent？"}
    M -- "是" --> N["写 worker Prompt<br/>docs/work/D*/prompts/P*-worker.md"]
    N --> O["Hook L1<br/>worker Prompt 已落盘"]
    O --> P["UTH-SP / Superpower<br/>uth-sp-subagent-driven-development"]
    M -- "否" --> Q{"是否按计划内联执行？"}
    Q -- "是" --> R["UTH-SP / Superpower<br/>uth-sp-executing-plans"]
    Q -- "否" --> S["主窗口直接实现"]
    P --> T["整合 worker 结果"]
    R --> T
    S --> T

    K --> U["运行编译 / 构建 / 必要验证"]
    T --> U
    U --> V["UTH-SP / Superpower<br/>uth-sp-verification-before-completion"]
    V --> W["Hook L3<br/>compile/build pass<br/>warnings=0 exceptions=0 或用户豁免"]
    W --> X{"开发口径"}
    X -- "light-dev" --> Y["写最终 LW 记录<br/>任务完成即生成报告<br/>触发 Git 收口判断"]
    X -- "formal-dev Todo 未完" --> Z["写 Feedback / current-state<br/>继续下一个 Todo<br/>不触发 Git 收口"]
    X -- "formal-dev Design 完成" --> AA["Design 级人类验收口径达成<br/>触发 Git 收口判断"]
    Y --> AB["询问用户是否进入 uth-git"]
    AA --> AB
    AB --> AC{"用户确认？"}
    AC -- "否" --> AD["场景收口<br/>Git 未执行"]
    AC -- "是" --> AE["交给 uth-git"]
    Z --> AD
```

## 5. uth-debug 故障定位 / 修复

```mermaid
flowchart TD
    A["用户报告 bug / 失败测试 / 运行异常 / 回归"] --> B["Scene: uth-debug"]
    B --> C["读取最小证据<br/>错误输出 / 复现方式 / 相关文档入口 / 相关代码"]
    C --> D{"是否需要追溯任务证据？"}
    D -- "是" --> E["辅助 Skill<br/>uth-context-trace<br/>定位 Design / Todo / Feedback / Prompt / Run"]
    D -- "否" --> F["继续局部排查"]
    E --> F

    F --> G{"症状、期望、修复权限是否清楚？"}
    G -- "否" --> H["UTH-SP / Superpower<br/>uth-sp-brainstorming"]
    H --> G
    G -- "是" --> I["Hook L1<br/>记录 debug 范围和 UTH-SP 判断"]

    I --> J["UTH-SP / Superpower<br/>uth-sp-systematic-debugging"]
    J --> K["先找根因<br/>不先猜修复"]
    K --> L{"需要修改行为或回归保护？"}
    L -- "是" --> M["UTH-SP / Superpower<br/>uth-sp-test-driven-development"]
    L -- "否" --> N["最小修复"]
    M --> N

    N --> O["Hook L2<br/>只写相关代码 / 测试 / 当前任务证据"]
    O --> P["运行复现验证 + 编译 / 构建"]
    P --> Q["UTH-SP / Superpower<br/>uth-sp-verification-before-completion"]
    Q --> R["Hook L3<br/>修复证据 + 0 warning / 0 exception 或用户豁免"]
    R --> S["写 Feedback / Todo / Run Log<br/>仅当有正式任务或需要证据"]
    S --> T{"是否达到人类验收口径？"}
    T -- "只读诊断" --> U["不触发 Git 收口"]
    T -- "正式任务包未到 Design 验收" --> V["不触发 Git 收口<br/>继续任务包流程"]
    T -- "独立轻量修复完成" --> W["触发 Git 收口判断"]
    T -- "正式任务包 Design 验收达成" --> W
    W --> X["询问用户是否进入 uth-git"]
    X --> Y{"用户确认？"}
    Y -- "否" --> Z["debug 场景收口<br/>Git 未执行"]
    Y -- "是" --> ZA["交给 uth-git"]
    U --> Z
    V --> Z
```

## 6. uth-review 审查 / 验收

```mermaid
flowchart TD
    A["用户要求 review / 验收 / diff 检查 / readiness"] --> B["Scene: uth-review"]
    B --> C["读取最小审查上下文<br/>AGENTS / docs README / current-state / 目标 diff / Todo"]
    C --> D{"审查口径是否清楚？"}
    D -- "否" --> E["UTH-SP / Superpower<br/>uth-sp-brainstorming"]
    E --> D
    D -- "是" --> F["Hook L1<br/>审查范围明确"]

    F --> G{"review 类型"}
    G -- "主动审查" --> H["UTH-SP / Superpower<br/>uth-sp-requesting-code-review"]
    G -- "处理外部反馈" --> I["UTH-SP / Superpower<br/>uth-sp-receiving-code-review"]
    G -- "验收验证" --> J["读取验收证据 / 运行允许的检查"]

    H --> K["只读发现问题<br/>不直接改代码"]
    I --> K
    J --> K
    K --> L["UTH-SP / Superpower<br/>uth-sp-verification-before-completion<br/>仅在声称通过/可合并前"]
    L --> M["Hook L3<br/>审查发现 / 验收证据 / 禁止代码写入"]
    M --> N{"有问题？"}
    N -- "是" --> O["交给 uth-debug 或 uth-dev<br/>不在 review 场景修"]
    N -- "否" --> P["收口：Findings-first / 验收结论 / 未验证风险<br/>默认不触发 Git 收口"]
```

## 7. uth-docs 单开文档治理

```mermaid
flowchart TD
    A["用户要求文档治理 / context 同步 / current-state 清理 / 归档"] --> B["Scene: uth-docs"]
    B --> C["选择模式<br/>rules / context / state / archive / snapshot / migration"]
    C --> D["读取最小文档入口<br/>AGENTS / docs README / current-state / _governance README"]
    D --> E{"是否涉及代码事实同步？"}
    E -- "是" --> F["只读代码 / git diff / git log<br/>提炼当前事实"]
    E -- "否" --> G["只处理目标文档"]
    F --> H["不跑测试 / 不改代码"]
    G --> H

    H --> I{"是否要写治理 Markdown？"}
    I -- "是" --> J["辅助 Skill<br/>uth-utf8-guard<br/>写前 UTF-8 / fence 检查"]
    I -- "否" --> K["只读输出"]
    J --> L["Hook L2<br/>docs/** / AGENTS.md / README.md 写入范围"]
    L --> M["更新 docs/_governance / current-state / context / archive / snapshots"]
    M --> N["辅助 Skill<br/>uth-utf8-guard<br/>写后检查"]
    N --> O["Hook L3<br/>文档场景收口<br/>不声称代码验证"]
    K --> O
    O --> P{"是否形成稳定可提交的治理成果？"}
    P -- "是" --> Q["建议 Git 收口<br/>询问用户是否进入 uth-git"]
    Q --> S{"用户确认？"}
    S -- "是" --> T["交给 uth-git"]
    S -- "否" --> R["收口：写了什么 / 没碰什么 / baseline / 归档影响"]
    P -- "否" --> R
```

说明：`uth-docs` 通常不调用 UTH-SP / Superpower；若文档治理目标、范围或验收不清，可以由场景内判断进入 `uth-sp-brainstorming`。

## 8. uth-git Git / PR / 发布收口

```mermaid
flowchart TD
    A["用户要求 commit / push / PR / tag / release"] --> B["Scene: uth-git"]
    B --> C["读取 Git 规则<br/>docs/_governance/git-workflow.md 或 AGENTS.md"]
    C --> D["检查 Git 状态<br/>branch / status / diff / remote / locks"]
    D --> E{"是否 release / tag / PR / 分支收口？"}
    E -- "是" --> F["UTH-SP / Superpower<br/>uth-sp-finishing-a-development-branch"]
    E -- "否" --> G["普通 commit / push 计划"]
    F --> H["形成 Git 写入计划"]
    G --> H

    H --> I{"是否有代码改动且缺少强验证证据？"}
    I -- "是" --> J["阻止 release/tag<br/>commit 需用户确认风险"]
    I -- "否" --> K["展示计划<br/>等待用户确认"]
    J --> K
    K --> L["Hook L2 Git Gate<br/>active_scene=uth-git<br/>plan + user confirmed"]
    L --> M["执行 Git 写入<br/>add / commit / push / PR / tag"]
    M --> N{"Git 写入成功？"}
    N -- "轻量改动" --> O["向现有 LW final record<br/>追加 Git baseline"]
    N -- "正式任务包" --> P["向关联 Feedback<br/>追加 Git baseline"]
    N -- "无报告目标" --> R["远端或本地 Git 证据验证"]
    O --> Q["辅助 Skill<br/>uth-utf8-guard<br/>检查 LW / Feedback / changelog"]
    P --> Q
    Q --> R
    R --> S["UTH-SP / Superpower<br/>uth-sp-verification-before-completion"]
    S --> T["Hook L3<br/>Git closeout evidence"]
    T --> U["收口：commit / remote / PR / tag / changelog / 风险"]
```

## 9. uth-context-trace 文档定位 / 证据追踪

```mermaid
flowchart TD
    A["需要定位任务文档证据链"] --> B["Scene: uth-context-trace"]
    B --> C["读取文档入口<br/>AGENTS / docs README / current-state"]
    C --> D{"目标是否指向活跃任务？"}
    D -- "是" --> E["定位 docs/work/D*/<br/>Design / Todo / Feedback / prompts / runs"]
    D -- "否" --> F{"是否明确需要历史或归档？"}
    F -- "是" --> G["只读 docs/archive/<br/>定位历史证据"]
    F -- "否" --> H["不进入 archive<br/>报告未定位到活跃证据"]
    E --> I["按需定位 docs/LW-Work / ADR / changelog / context"]
    G --> I
    H --> I
    I --> J["输出证据链<br/>不改文件 / 不判断代码 / 不执行 Git<br/>不触发 Git 收口"]
```

说明：`uth-context-trace` 是只读辅助 Skill，不调用 UTH-SP，不替代代码搜索，也不负责修复或审查。

## 10. uth-utf8-guard 文档编码守卫

```mermaid
flowchart TD
    A["准备修改治理 Markdown"] --> B["uth-utf8-guard 写前检查"]
    B --> C{"UTF-8 / mojibake / fence 是否正常？"}
    C -- "否" --> D["先修复编码或 fence<br/>不继续写入"]
    C -- "是" --> E["执行文档写入"]
    E --> F["Hook L2<br/>确认写入范围"]
    F --> G["uth-utf8-guard 写后检查"]
    G --> H{"检查通过？"}
    H -- "否" --> I["修复文档<br/>重新检查"]
    I --> G
    H -- "是" --> J["文档场景可收口"]
```

## 11. Hook 门禁位置总览

```mermaid
flowchart TD
    A["进入 uth-* 子 Skill"] --> B["Hook L1 Process Gate"]
    B --> B1["检查：场景声明 / 歧义是否处理 / UTH-SP 判断 / worker Prompt"]
    B1 --> C["执行或准备写入"]
    C --> D["Hook L2 Tool Gate"]
    D --> D1["检查：文件范围 / Git 确认 / UTF-8 / 脚本 no-BOM 与语法"]
    D1 --> E["场景写回或 Git 写入"]
    E --> F["Hook L3 Closeout Gate"]
    F --> F1["检查：完成证据 / 代码强验证 / 场景禁止事项 / 豁免记录"]
    F1 --> G["最终收口"]
```

## 图例

- `uth-governance` 只负责顶层场景路由，不直接调用 UTH-SP / Superpower。
- `uth-*` 子 Skill 负责场景内上下文装载、UTH-SP 触发判断、执行边界、文档写回和收口协议。
- `UTH-SP / Superpower` 节点表示调用本包内 `skills/uth-sp-*` 方法 Skill。
- Hook 是门禁，不是流程；它只检查调用方提供的场景、范围、确认和验证事实。
- `docs/LW-Work/` 属于轻量开发记录；正式任务包放在 `docs/work/DYYMMDDXX-*`。
