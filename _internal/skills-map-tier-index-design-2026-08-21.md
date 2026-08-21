# Skills Map 分層索引機制（2026-08-21 設計）

## §1 三層索引架構

### 1.1 核心層 (core) — 5-10 個，永遠注入
- **載入時機**：每個 session 啟動時 always-on
- **目的**：SOUL 紅線 / 任務路由 / 治理底線
- **淘汰條件**：被新 skill 取代 / 任務流程變更 / 已 deprecated

### 1.2 活躍層 (active) — 30-50 個，任務觸發
- **載入時機**：任務類型匹配路由表時觸發
- **目的**：當前任務所需的 task / mode / escalation skill
- **淘汰條件**：90 天無引用 / 已被新 skill 取代 / 路由表改變

### 1.3 冷卻層 (cold) — 100+ 個，按需載入
- **載入時機**：`skill_view` 命令明確呼叫
- **目的**：歷史參考 / niche 任務 / 一次性工具
- **淘汰條件**：180 天無引用 → 自動 archive

## §2 貢獻度評判 SOP（非純數字評估）

> 關鍵：護欄強度不是看引用次數等量化指標，而是看**工程價值、業務價值、管理價值、時效性**四維度的綜合評判。

### 2.1 評估維度

| 維度 | 評估問題 | 舉例（atlas-wiki SKILL） |
|------|---------|------------------------|
| **工程價值 (E)** | 是否影響 hermes 運作底層（config、治理、MCP 整合）？ | hermes-agent, hermes-agent-skill-authoring |
| **業務價值 (B)** | atlas 散戶金融判斷是否需要？散戶端是否受益？ | task-financial-judgment, financial-advisor-coach, atlas-skill-discipline |
| **管理價值 (M)** | 是否影響任務編排 / 派工 / 報告？ | task-governance, mode-reporting, task-tracking |
| **時效性 (T)** | 現在還合用嗎？是否已被新 skill 取代？ | 已 deprecated: 0；in-transition: 需重評估 |

### 2.2 評估 SOP（每個 skill 必跑）

1. **E 評估**：拆解 skill 內容，看是否觸及 hermes 內部運作？
   - 有 → E = high
   - 只有外部 tool wrapper → E = low

2. **B 評估**：對位 `~/workspace/atlas/docs/ATLAS_METHODOLOGY.md`，是否幫助散戶？
   - 有 → B = high
   - 是通用 tool（xlsx, pdf）→ B = low

3. **M 評估**：是否影響任務編排 / 派工流程？
   - 是 task/mode 路由層 → M = high
   - 是工具封裝 → M = low

4. **T 評估**：上次更新距今多久？路由表是否已標遷移？
   - < 30 天且 active → T = high
   - 60-90 天 in-transition → T = medium
   - > 90 天 deprecated → T = low

### 2.3 評估矩陣（建議初始分層）

| E | B | M | T | 分層 |
|---|---|---|---|------|
| high | high | high | high | **core** |
| 任意 high | 任意 high | 任意 high | medium+ | **active** |
| low | low | low | high | **cold** |
| 任意 | 任意 | 任意 | low | **archive** |

### 2.4 評估範例（Top 5 SKILL）

| skill | E | B | M | T | 分層 |
|---|---|---|---|---|---|
| agent-self-judgment-mode | high (影響 hermes 判斷姿態) | high (散戶對位) | high (任務編排底線) | high | **core** |
| mode-no-guess-before-evidence | high (防亂猜) | high (品質) | high (任務品質) | high | **active** |
| kaecer-session-trust-patterns | medium (trust pattern) | medium | high (kaecer 偏好) | high | **active** |
| personal-knowledge-copilot | high (workflow) | high (用戶體驗) | medium | high | **active** |
| atlas-skill-discipline | high (atlas 治理) | high (atlas mission) | high | high | **active** |

## §3 索引載入機制（取代 always-on 全量）

### 3.1 現況問題
- 148 個 skill 名字 + 描述 always-on 注入 = 14,413 chars = ~5,766 tokens
- 每次 session 啟動就帶上

### 3.2 提案（Plan A 落實）

```
┌─────────────────────────────────────────────────────────────┐
│ Session 啟動注入                                              │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Core 層 (5-10 個)                                       │ │
│ │ SOUL/AGENTS + 任務路由 + 治理底線                       │ │
│ │ → ~2,000 tokens                                        │ │
│ ├────────────────────────────────────────────────────────┤ │
│ │ Active 層 (30-50 個)                                    │ │
│ │ 任務類型觸發時載入                                       │ │
│ │ → ~3,000-5,000 tokens（按任務類型變動）                  │ │
│ ├────────────────────────────────────────────────────────┤ │
│ │ Cold 層 (100+)                                          │ │
│ │ skill_view 命令明確呼叫                                  │ │
│ │ → 0 tokens always-on                                  │ │
│ └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 落地優先序

1. **Week 3 Day 1**: skills-map.md 加 §分層索引機制章節（本設計文件落地）
2. **Week 3 Day 2**: config.yaml `[skills]` 加 `tier_limits` 設定
3. **Week 3 Day 3**: hermes-agent-skill-authoring 加 lifecycle 護欄檢查
4. **Week 3 Day 4**: 144 個 skill 跑 §2 評估 SOP 分層
5. **Week 3 Day 5**: 示範 1 次「新增 skill 跑競爭 SOP」

## §4 護欄規則（取代純數字評判）

### 4.1 新增 skill 競爭 SOP
- 新增前必跑：
  1. 搜尋現有 skill 看是否有 70% 重疊
  2. 若有重疊 → 寫成現有 skill 的 references/ 子檔
  3. 若無重疊 → 寫新增提案（1 段）給 kaecer 拍板
  4. 拍板通過才落地 SKILL.md

### 4.2 自動 lifecycle 規則
- **created**: 新建立（90 天觀察期）
- **draft**: 0-30 天，未驗證（紅標）
- **active**: 30+ 天，有引用（綠標）
- **in-transition**: 60+ 天，路由表標遷移（黃標）
- **deprecated**: 90+ 天，沒引用（灰標）
- **archived**: 180+ 天，移到 `_archive/` 目錄

### 4.3 護欄強度（混合模式，建議採用）
- **硬上限**: core 10 + active 50 + cold 100 = 160 個
- **軟警告**: 90 天沒引用 → LLM 提示「建議 archive」
- **不自動執行**: archive 需 kaecer 拍板

## §5 對位 kimi-k3 顧問分解

| 計畫 | 內容 | 對位本設計 |
|------|------|----------|
| Plan F | Top 5 SKILL 拆分 + 未來護欄 | 本設計是 Plan F Week 3 內容 |
| Plan A | skills lifecycle 設計 | §4 lifecycle 規則 |
| Plan B | tool 過濾 | config.yaml `[toolsets]` 設定（不在本文件範圍）|
| Plan H | cron toolset 過濾 | 4 個 cron job 各自 `enabled_toolsets`（不在本文件範圍）|

## §6 對位 kaecer 8/21 21:15 拍板

- ✅ skills map 分層索引進入 top 5（§1 + §3 落地）
- ✅ agent-self-judgment-mode 進入 core 層（§2.4 評估範例）
- ✅ 護欄看工程/業務/管理貢獻度，非純數字（§2 評估 SOP）
- ✅ Plan B/A/H 同步落實（§5 對位）

---

**狀態**: design draft (2026-08-21 21:15)
**owner**: kaecer
**amendable_by**: kaecer
**落地順序**: Plan F Week 3 Day 1-5

