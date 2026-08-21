# Plan B — Tool 過濾機制設計（2026-08-21）

## §1 現況問題

`hermes prompt-size --json` 量化：
- 24 個 tool schemas always-on 注入 = **59,112 B / ~17,734 tokens**
- 每次 session 啟動都帶上
- 大部分 tool 與當前任務無關（如 audio/tts 在金融任務中無用）

## §2 Tool 分組（按用途）

### 2.1 現有 24 個 tool 的分組（從 prompt-size 輸出）

| 工具組 | tools | size | 任務相關性 |
|--------|-------|------|-----------|
| computer_use | 1 | 9,699 B | 低（金融任務無用）|
| file | 4 | 6,704 B | 高（讀寫 wiki）|
| session_search | 1 | 6,457 B | 高（搜尋歷史）|
| delegation | 1 | 5,780 B | 高（派工）|
| skills | 3 | 5,646 B | 高（skill_view）|
| terminal | 2 | 4,819 B | 高（shell）|
| browser_use | 1 | 3,383 B | 中（網頁驗證）|
| memory | 1 | 2,833 B | 高（MEMORY 引用）|
| clarify | 1 | 2,739 B | 高（升級）|
| code_execution | 1 | 2,548 B | 中（驗證）|
| web | 2 | 1,910 B | 中 |
| tts | 1 | 1,868 B | **低（金融任務無用）** |
| todo | 1 | 1,372 B | 高 |
| vision | 1 | 1,360 B | 中 |

## §3 5 個 Toolset 設計（任務導向）

### 3.1 任務分類 → 所需 toolset

| 任務類型 | 必要 tools | toolsets |
|---------|-----------|----------|
| **金融判斷** (task-financial-judgment) | mcp_atlas_*, file, memory, session_search, web | governance-toolset + finance-toolset |
| **知識整理** (task-knowledge-routing) | file, memory, wiki-editor | content-toolset |
| **治理變更** (task-governance) | file, delegation, memory, terminal | governance-toolset |
| **程式修改** (task-coding) | terminal, code_execution, file, git, delegation | coding-toolset |
| **報告輸出** (mode-reporting) | memory, session_search, tts, vision | reporting-toolset |
| **一般對話** | session_search, memory, todo | general-toolset |

### 3.2 Toolset 定義（config.yaml 提案）

```yaml
# ~/.hermes/config.yaml
toolsets:
  governance-toolset:
    - file
    - delegation
    - memory
    - terminal
    - todo
  finance-toolset:
    - mcp_atlas
    - session_search
    - web
    - memory
  content-toolset:
    - file
    - memory
    - web
    - session_search
  coding-toolset:
    - file
    - terminal
    - code_execution
    - delegation
    - git
  reporting-toolset:
    - memory
    - session_search
    - tts
    - vision
    - delegation
  general-toolset:
    - session_search
    - memory
    - todo
    - web
```

### 3.3 任務 → Toolset 對應表

| 任務類型 | toolset | 估算 size |
|---------|---------|----------|
| 金融判斷 | governance + finance | ~10,000 B (vs 59,112 B 全量) |
| 知識整理 | governance + content | ~8,000 B |
| 治理變更 | governance only | ~5,000 B |
| 程式修改 | governance + coding | ~10,000 B |
| 報告輸出 | reporting only | ~3,500 B |
| 一般對話 | general only | ~3,000 B |

**估算節省**: 59,112 B → 平均 8,000 B（-86%）

## §4 落地 SOP

### Week 3 Day 2（Plan B 落地）

1. **config.yaml 改動**：
   - 加 `[toolsets]` 區塊
   - 加 `[tasks.toolset_mapping]` 任務 → toolset 對應
2. **hermes-agent-skill-authoring 加 SOP**：
   - 每個 task skill 必填 `toolsets: [toolset1, ...]`
   - LLM 啟動時依 task 載入對應 toolset
3. **驗證**：
   - `hermes prompt-size` 顯示 tool schemas 從 59,112 B 降到 ~10,000 B
   - 任務完成率不變

## §5 風險與回退

### 風險
- toolset 過窄 → 任務無法完成
- 任務分類錯誤 → 載入錯誤 toolset

### 回退
- 每個 task skill 加 `fallback_toolset: general-toolset`
- hermes-agent-skill-authoring 加「toolset 完整性檢查」

## §6 與 Plan A / H 對位

- **Plan A** (skills lifecycle): 與本計畫並行，配置 `[skills.tier_limits]`
- **Plan H** (cron toolset 過濾): 4 個 cron job 各自配置 `enabled_toolsets`（在 cron config）

