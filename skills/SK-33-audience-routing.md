---
title: SK-33 三 audience 表達口徑切換(user / developer / admin)
type: skill-inbound
source: ~/workspace/atlas-wiki/skills/_manifest_coverage_routing.md §2 題 3 + §3.3 Day 1
ingested_at: 2026-08-07
status: active
tier: T2
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [strategy_ranker, get_recommendations, risk_exposure, risk_get_metrics, capital_flow_daily]
verification: 2026-08-07 v6.51 Day 1 落定(對位 manifest §2 題 3 + §3.3 Day 1);v6.52 撤銷外推改內部約定(agent 從 session context 讀 audience,預設 user);L3 Step 1 落地;若未來 hermes runtime 提供 HERMES_AUDIENCE env,升級雙層架構
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §二(監理架構三層對應)+ §三(對外發布規範)
related:
  - ~/workspace/atlas-wiki/skills/_manifest_coverage_routing.md §2 題 3 + §3.3 Day 1
  - ~/workspace/atlas-wiki/skills/_inbox_deferred.md(v6.52 改內部約定登記處)
  - ~/workspace/atlas-wiki/concepts/atlas-mcp-failover-policy.md(4 級 fallback 紀律)
  - ~/.hermes/skills/financial-advisor-coach/SKILL.md §X(user 降級口徑 v6.52)
---

<!-- methodology_alignment_tip: 三 audience(user/developer/admin)/ tier-aware 是 audience 子屬性 / 來源標籤 `[來源: ...@ISO 8601]` 對位 L1-L4 fallback 鏈;kaecer「散戶怕 error,管理者要 debug」二分根因 -->

## 一句話定位

把 atlas-mcp 既有「free / registered / premium 三 tier 商業分級」對應到「user / developer / admin 三 audience 表達口徑」——同一個工具,在不同 reader 面前應給不同深度,避免散戶被 raw error 嚇退 / 管理者看不到完整 audit。

## 論文版概念(忠實還原)

**論文無直接對位**——audience routing 是產品體驗層概念,非學術論文主題。對位以下三條產品 / 工程原則:

1. **Progressive Disclosure 漸進披露(Nielsen 2006)** — 系統功能按用戶能力分層揭露,不一次丟全部
2. **Persona-based UX(Cooper 1999 「The Inmates Are Running the Asylum」)** — 不同 persona 對同一訊息有不同反應,系統應區分表達
3. **Least Astonishment Principle(飛行系統設計經典)** — agent 表達方式不應讓對方驚訝:散戶對 raw error 驚訝 = 失敗;管理者對不見 error 驚訝 = 也失敗

**對位 AGENTS.md §1 憲法 mission「找信息差、找漏洞、悶聲賺錢」**:對散戶,**信息差的表達要負責**;對管理者,**漏洞的可見性要充分**。

## atlas 對位

### 三 audience × 三 tier 對位表

| audience | 對位 atlas-mcp tier | 觸發情境 | 輸入 | 輸出 |
|---|---|---|---|---|
| **user** | free / registered | hermes/OpenClaw 對話 + 散戶互動 | 自然語言問題(中文/英文) | 結論 + 來源戳 + 風險標;**禁 raw error code / API 限制訊息** |
| **developer** | registered / premium(實作以上) | agent 開發任務 / atlas-go PR audit / 跨 agent handoff | 任務描述 + tool call | tool_name + ISO timestamp + channel 對位 + circuit breaker 狀態 + git hash |
| **admin** | premium(全權限) | kaecer 直訊 / 02:00 cron health / Telegram gate | 系統觀察 / audit 需求 | 全 audit log + metrics trend + 動作選項 5 條 |

### 觸發器架構

```
                        ┌──────────────────────┐
                        │ HERMES_AUDIENCE env   │
                        │ (user/dev/admin)     │
                        │ 預設 user            │
                        └──────────┬───────────┘
                                   ↓(runtime 讀)
              ┌────────────────────┼────────────────────┐
              ↓                    ↓                    ↓
     ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
     │   user      │      │  developer  │      │   admin     │
     │ 口徑框架     │      │ 口徑框架     │      │ 口徑框架     │
     └─────────────┘      └─────────────┘      └─────────────┘
              │                    │                    │
              ↓                    ↓                    ↓
       散戶/GROW 教練      agent-self-eval       kaecer 對總監
```

**架構原則**:
- **不靠 agent 自判 audience** — 環境變數 / runtime 設定決定,避免 agent 漏 case
- **任何輸出前必讀 audience** — 對位 SOUL §3.2「先結論再依據」、AGENTS.md §1 報告格式
- **單邊境降級 = 絕對禁止** — 給 developer 的 raw error 不能漏給 user(user 怕);給 admin 的 audit 路徑不能省給 developer(看不到問題怎修)

### tier (free/registered/premium) 是 audience 的子屬性

| tier | 含義 | 對 user 表達影響 |
|---|---|---|
| **free** | 唯讀 mcp_quickstart / daily_report / report_get_daily_summary / 受限 get_recommendations / strategy_list_active | 結果可見,但不暴露內部計算細節 |
| **registered** | 加 strategy_get_summary / strategy_get_attribution / risk_get_metrics / capital_flow_daily 七維 | 看得到更多維度,但仍以「對散戶有感」為包裝 |
| **premium** | sector_allocation_plan / PRISM cohort / experiment_judge / 完整 attribution | 技術細節全開,但**仍然要走 user 表達框架**(不漏 raw error) |

**關鍵設計**:user / developer / admin 是**表達口徑**,tier 是**資料可見性**。兩軸獨立但互綁——同一個 free tier 用戶永遠是 user 表達口徑;同一個 premium tier 用戶可在 user / developer / admin 三口徑間切換(根據當下意圖)。

## 散戶解讀(GROW+ 引用點)

教練框架最敏感的環節就是 **audience**:

- **G(Goal)段**:用戶問「我的 2330 怎麼了」→ 這是 `user` audience,G 段必須直覺對應
- **R(Reality)段**:user 表達要從 atlas 找到的數據**包裝後**呈現,原始 `error: 503 service unavailable` 必須改寫為「目前報價資料源不在我的服務範圍」(對位 concepts/atlas-mcp-failover-policy.md v1.0 L4 表達紀律)
- **O(Options)段**:三方案 + 各自風險,**不在 user 表達中暴露策略層 debug 訊息**(那留給 developer / admin)
- **+E(事後教育)段**:user 表達結尾「下次遇到類似情況能自己判斷」= 教育的本質,**此段在 user 口徑中保留最完整**,developer / admin 不需要這層

**財務健康紀律**(`financial-advisor-coach/SKILL.md` 對位):
- user 永遠不寫「我建議你買進」「這支應該會漲」
- developer 可暴露「這個 strategy_ranker tier free 用戶看到的是 tier-aware filter 結果」
- admin 可看到「最近一次 audit 顯示 X 個 endpoint 在 z_score > 2.5」

## 驗證方式

**Step 1**:讀 `strategy_ranker` 回傳,確認三 tier 在 JSON 結構中以 `tier` 欄位標記(`free` / `registered` / `premium`)。
**Step 2**:用 `mcp_roots_list` 確認 hermes daemon 啟動時讀 `HERMES_AUDIENCE` env,若未設則 fallback 為 `user`。
**Step 3**:跨 audience 實跑 3 個樣本對話(腳本):
- user 樣本:問「2330 今天怎樣」→ agent 回結論 + 來源戳,**不暴露 any tool_name 內部代碼**
- developer 樣本:問「為什麼 v6.50 _inbox size 爆到 13448」→ agent 回 tool_name + line + commit hash
- admin 樣本:問「過去 7 天 audit log」→ agent 回全 metrics + 5 條候選動作

**Step 1 對位結果(2026-08-07 v1.0 + v6.52 修)**:atlas-mcp 已有 tier 機制(`strategy_ranker` / `get_recommendations` 都標 tier);**audience 切換器 = agent 自扛**(從 session context 推導,預設 `user`);若未來 hermes runtime 升級提供 `HERMES_AUDIENCE` env,改雙層架構(env 優先,session context fallback)。對位 v6.52 kaecer「我們自己把事做完,不外推」拍板。

## 未消化 / 待補

- [x] tier → audience 對位表 + 觸發情境 + 表達紀律落地 ✅(本檔 v1.0)
- [x] ~~HERMES_AUDIENCE env 提案已落 `_inbox_deferred.md §ENV-CR-2026-08-07`,待 hermes owner 回覆(≤ 14 天)~~ → **2026-08-07 v6.52 撤銷外推**:kaecer 拍板「我們自己把事做完,不外推」,改為**內部約定**(agent 從 session context 讀 audience,預設 `user`);`_inbox_deferred.md` 改為「內部約定登記處」而非「跨邊界移交」;若未來 hermes runtime 提供 env,再升級為雙層架構
- [x] `financial-advisor-coach/SKILL.md` §X 對 user audience 的 atlas-mcp 降級口徑 — **2026-08-07 v6.52 自扛落地**(kaecer「quota 不含直接指令」+ 「我們自己做完」拍板),不走 task-governance
- [ ] Step 3 跨 audience 實跑腳本,待寫(`scripts/dev/verify-audience-routing.py`)
- [ ] 與 `concepts/atlas-mcp-failover-policy.md` v1.0 L4 源不可達散戶表達紀律銜接——L4 觸發時由 user audience 表達,不需要降級審批
