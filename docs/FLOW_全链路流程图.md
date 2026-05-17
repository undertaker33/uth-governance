# UTH Governance 全链路流程图

## 0. 安装与启用边界

```mermaid
flowchart TD
    A["安装 UTH Governance"] --> B["checkout pack"]
    B --> C["scripts/install.py"]
    C --> D["安装全局 skills"]
    D --> E{"显式 uth-onboarding?"}
    E -- "否" --> F["不初始化项目"]
    F --> F1["不建 .uth-governance"]
    F --> F2["不复制 hooks"]
    E -- "是" --> G["uth-onboarding"]
    G --> H["复制 tools/uth-hooks"]
    H --> I["写 project.json"]
    I --> J["启用 uth-* 路由"]
```

## 1. 总览路由

```mermaid
flowchart TD
    A["用户工程请求"] --> B{"显式启用/接管?"}
    B -- "是" --> C["uth-onboarding"]
    B -- "否" --> D["uth-governance"]
    D --> E{"有 project.json?"}
    E -- "否" --> F["UTH 静默"]
    E -- "是" --> G{"工程动作?"}
    G -- "否" --> H["普通回答"]
    G -- "是" --> I{"场景明确?"}
    I -- "否" --> J["澄清/brainstorming"]
    I -- "是" --> K["进入 uth-*"]
    K --> L{"场景"}
    L --> D1["uth-design"]
    L --> D2["uth-dev"]
    L --> D3["uth-debug"]
    L --> D4["uth-review"]
    L --> D5["uth-docs"]
    L --> D6["uth-context-trace"]
    L --> D7["uth-git"]
```

## 2. 场景内执行

```mermaid
flowchart TD
    A["uth-* 场景"] --> B["最小上下文"]
    B --> C{"需求/范围清楚?"}
    C -- "否" --> D["uth-sp-brainstorming"]
    D --> C
    C -- "是" --> E["L1 过程门"]
    E --> F["L2 写前/工具门"]
    F --> G["执行/写回"]
    G --> H["写后守卫/验证证据"]
    H --> I["L3 收口门"]
    I --> J{"可建议 Git?"}
    J -- "否" --> K["场景收口"]
    J -- "是" --> L["询问用户"]
    L -- "未确认" --> K
    L -- "确认" --> M["交给 uth-git"]
```

## 3. onboarding 接管

```mermaid
flowchart TD
    A["uth-onboarding"] --> B{"模式"}
    B -- "new-project" --> C["最小文档骨架"]
    B -- "existing enable-only" --> C
    C --> D["复制 hooks"]
    D --> E["写 project.json"]
    E --> F["最小启用完成"]

    B -- "existing full-takeover" --> G["备份旧文档"]
    G --> H["接管快照"]
    H --> I["复制 hooks"]
    I --> J["写 project.json"]
    J --> K["handoff: uth-docs onboarding-followup"]
    K --> L{"docs 完成?"}
    L -- "full-project-docs-complete" --> M["回到 onboarding 收口"]
    L -- "blocked/module-split" --> N["暂停或下窗交接"]
```

## 4. docs 治理地图

```mermaid
flowchart TD
    A["uth-docs"] --> B{"模式"}
    B -- "onboarding-followup" --> C["代码事实基线"]
    B -- "full-project-baseline" --> C
    B -- "scoped-sync" --> D["指定范围同步"]
    B -- "module-split" --> E["写 00-* 拆分计划"]
    E --> F["更新模块索引"]
    F --> G["用户确认"]
    G --> H["module-governance"]
    B -- "module-governance" --> H
    H --> I["按 01-* 顺序治理"]
    I --> J{"module_queue 空?"}
    J -- "否" --> I
    J -- "是" --> K["docs 收口"]
    C --> K
    D --> K
    K --> L{"建议 Git?"}
    L -- "否" --> M["docs 收口"]
    L -- "是" --> N["询问用户"]
    N -- "确认" --> O["交给 uth-git"]
    N -- "未确认" --> M
```

## 5. Git 收口边界

```mermaid
flowchart TD
    A["debug/design/docs/dev 建议 Git"] --> B["先询问用户"]
    B -- "未确认" --> C["原场景收口"]
    B -- "确认" --> D["uth-git"]
    X["用户显式 Git 请求"] --> D
    D --> E["读取 Git 规则"]
    E --> F["检查 status/diff/remote"]
    F --> G["形成写入计划"]
    G --> H{"用户确认计划?"}
    H -- "否" --> I["不执行 Git 写入"]
    H -- "是" --> J["L2 Git Gate"]
    J --> K["add/commit/push/PR/tag"]
    K --> L["远端/本地验证"]
    L --> M["Git 收口"]
```

## 6. Hook 门禁位置

```mermaid
flowchart TD
    A["进入 uth-*"] --> B["L1 Process Gate"]
    B --> C["场景/歧义/UTH-SP/worker"]
    C --> D["准备执行或写入"]
    D --> E["L2 Tool Gate"]
    E --> F["范围/Git/UTF-8/脚本"]
    F --> G["场景写回或 Git 写入"]
    G --> H["L3 Closeout Gate"]
    H --> I["证据/例外/输出语言"]
    I --> J["最终收口"]
```

## Notes

- 场景规则、进入条件、收口语义见 `docs/AGENT_工程治理启动手册.md`。
- Hook 事件字段、L1/L2/L3 门禁证据见 `docs/HOOKS_工程治理门禁手册.md`。
