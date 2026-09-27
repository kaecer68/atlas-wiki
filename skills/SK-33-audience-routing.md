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
verification: "歷史(2026-08-07 v6.51/v6.52)：對位 manifest §2 題 3 + §3.3 Day 1;撤銷外推改內部約定(agent 從 session context 讀 audience,預設 user);L3 Step 1 落地。**2026-09-27 L3 實跑**：`/api/strategy-ranker/rank` 12 檔**每筆都有 `tier`**(premium 2／registered 2／free 8)、`/api/recommendations` 回 `tier`=free、`/api/dashboard/risk-exposure` 與 `/api/capital-flow/daily` 200;**Step 2 的 `mcp_roots_list` 今日 route 404(`/api/mcp/roots` route not found)且 `HERMES_AUDIENCE` 在 atlas-go 全 repo 0 命中** ⇒ audience env 為已驗證的否定;Step 3 腳本 `scripts/dev/verify-audience-routing.py` 不存在。見 §驗證方式。"
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b6）
l3_endpoints_probed:
  - "/api/strategy-ranker/rank → 200（12 檔,每筆有 tier） (2026-09-27T20:33:47+08:00)"
  - "/api/recommendations → 200（tier=free） (2026-09-27T20:33:47+08:00)"
  - "/api/dashboard/risk-exposure → 200（cash_ratio 0.5228） (2026-09-27T20:34:31+08:00)"
  - "/api/dashboard/risk → 200（無 Sharpe 欄位） (2026-09-27T20:33:10+08:00)"
  - "/api/capital-flow/daily → 200（foreign z_score -0.78） (2026-09-27T20:34:31+08:00)"
  - "/api/mcp/roots → 404 route not found（Step 2 前提不成立） (2026-09-27T20:34:20+08:00)"
  - "源碼 git grep HERMES_AUDIENCE（atlas-go）→ 0 命中 (2026-09-27T20:35+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §二(監理架構三層對應)+ §三(對外發布規範)
related:
  - ~/workspace/atlas-wiki/skills/_manifest_coverage_routing.md §2 題 3 + §3.3 Day 1
  - ~/workspace/atlas-wiki/skills/_inbox_deferred.md(v6.52 改內部約定登記處;ENV-CR-2026-08-07)
  - concepts/atlas-mcp-failover-policy.md(4 級 fallback 紀律 + L4 散戶表達)
  - ~/.hermes/skills/financial-advisor-coach/SKILL.md §X(user 降級口徑 v6.52)
---

<!-- methodology_alignment_tip: 三 audience(user/developer/admin)/ tier-aware 是 audience 子屬性 / 來源標籤 `[來源: ...@ISO 8601]` 對位 L1-L4 fallback 鏈 -->

## 一句話定位

把 atlas-mcp 既有「free / registered / premium 三 tier 商業分級」對應到「user / developer / admin 三 audience 表達口徑」——同一個工具,在不同 reader 面前應給不同深度,避免散戶被 raw error 嚇退 / 管理者看不到完整 audit。

## 論文版概念(忠實還原)

**論文無直接對位**——audience routing 是產品體驗層概念。對位三條產品/工程原則:①Progressive Disclosure(Nielsen 2006)按能力分層揭露 ②Persona-based UX(Cooper 1999)不同 persona 對同一訊息反應不同 ③Least Astonishment:散戶對 raw error 驚訝 = 失敗,管理者對「不見 error」驚訝 = 也失敗。對位 mission:對散戶表達要負責,對管理者漏洞要可見。

## atlas 對位

| audience | 對位 atlas-mcp tier | 觸發情境 | 輸出紀律 |
|---|---|---|---|
| **user** | free / registered | 散戶對話 | 結論 + 來源戳 + 風險標;**禁 raw error code / API 限制訊息** |
| **developer** | registered / premium | agent 開發 / atlas-go PR audit / handoff | tool_name + ISO timestamp + channel 對位 + circuit breaker 狀態 + git hash |
| **admin** | premium(全權限) | kaecer 直訊 / 02:00 cron health / Telegram gate | 全 audit log + metrics trend + 候選動作 |

**架構原則**:不靠 agent 自判 audience(環境變數/runtime 決定);任何輸出前必讀 audience;單邊境降級絕對禁止(developer 的 raw error 不漏給 user;admin 的 audit 路徑不省給 developer)。切換器位置 = `HERMES_AUDIENCE` env(預設 user)→ 三套口徑框架(user／developer／admin),**今日該 env 在 atlas-go 0 命中**(見更正 2),故實務上仍由 agent 從 session context 推導。

**tier 是 audience 的子屬性**:`free`(唯讀 quickstart/daily_report,結果可見不暴露內部計算)、`registered`(加 strategy summary/attribution/risk/capital_flow 七維)、`premium`(sector_allocation_plan/PRISM cohort/experiment_judge/完整 attribution,技術細節全開但**仍走 user 表達框架**)。兩軸獨立但互綁:同一個 free tier 用戶永遠是 user 口徑;premium 用戶可在三口徑間切換。

## 散戶解讀(GROW+ 引用點)

- **G 段**:用戶問「我的 2330 怎麼了」→ 這是 user audience,直覺對應。
- **R 段**:原始 `error: 503 service unavailable` 必須改寫為「目前報價資料源不在我的服務範圍」(對位 `concepts/atlas-mcp-failover-policy.md` L4 表達紀律)。
- **O 段**:三方案 + 各自風險,不暴露策略層 debug(留 developer/admin)。
- **+E 段**:「下次能自己判斷」= 教育本質,user 口徑保留最完整。
- **財務健康紀律**:user 永不寫「我建議你買進」;developer 可暴露 tier-aware filter;admin 可看 audit 指標(如資本流 `z_score`)。

## 驗證方式

**Step 1**:讀 `strategy_ranker` 回傳,確認三 tier 以 `tier` 欄位標記。
**Step 2**:用 `mcp_roots_list` 確認 hermes daemon 啟動時讀 `HERMES_AUDIENCE`,未設 fallback `user`。
**Step 3**:跨 audience 實跑 3 個樣本對話(腳本)。

### L3 端點實跑（2026-09-27,本 PR）

| 端點／命令 | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/strategy-ranker/rank` | 200 | **12 檔策略,每筆都有 `tier`**:premium 2(us-tariff-shock-tech 61.17、sox-foreignflow 59.15)／registered 2(foreign-3day-inflow 59.07 等)／free 8 ⇒ **Step 1 成立** | 2026-09-27T20:33:47+08:00 |
| `/api/recommendations` | 200 | 頂層 `tier`=**free**、`market.regime`=low、`stress_index`=17.745、`warning`=capital_flow_assessment_calibrating | 2026-09-27T20:33:47+08:00 |
| `/api/dashboard/risk-exposure` | 200 | `position_count`=3、`cash_ratio`=0.5228、`max_drawdown_pct`=0.7220、`var_95`=0(premium 層資料可見性的實測值) | 2026-09-27T20:34:31+08:00 |
| `/api/dashboard/risk` | 200 | **無 Sharpe 欄位**;`insufficient_data`=1 ⇒ 引用時不可寫「risk 給 Sharpe」 | 2026-09-27T20:33:10+08:00 |
| `/api/capital-flow/daily` | 200 | `forces[]` 含 `z_score`／`calibration_status`(foreign z_score=-0.78、`sample_count`=252、`eligible`)⇒ admin 層「z_score 門檻」示例可對真值檢查(今日無 >2.5 項) | 2026-09-27T20:34:31+08:00 |
| `/api/mcp/roots`(`mcp_roots_list`) | **404** | `{"code":"404","error":"route not found","path":"/api/mcp/roots"}` ⇒ **Step 2 的前提今日不成立**(route 不存在,非資源 404) | 2026-09-27T20:34:20+08:00 |
| 源碼 `git grep HERMES_AUDIENCE`（atlas-go 全 repo） | 0 命中 | 三 tier 是**端點欄位**;audience 是**純 client 端約定**,atlas 側沒有任何 env 讀取或 audience 欄位 | 2026-09-27T20:35+08:00 |
| `ls scripts/dev/verify-audience-routing.py` | 不存在 | `scripts/dev/` 只有 auto-commit-pr.sh／hooks／install-hooks.sh ⇒ Step 3 腳本未落地 | 2026-09-27T20:35+08:00 |

**更正（2026-09-27）**

1. **Step 1 成立且比 2026-08-07 更硬**:tier 不只是「有標」,今日 12 檔的 tier 分佈為 premium 2／registered 2／free 8,且 `get_recommendations` 頂層亦有 `tier`。
2. **Step 2 為已驗證的否定**:`mcp_roots_list` 的 route(`/api/mcp/roots`)今日回 **route 404**,且 `HERMES_AUDIENCE` 在 atlas-go 全 repo **0 命中** ⇒ 「hermes daemon 讀 HERMES_AUDIENCE」目前**沒有任何實作面**,audience 切換仍是 agent 自扛(與 v6.52 內部約定一致)。
3. **`risk_get_metrics` 不提供 Sharpe**:本頁工具清單裡的該項今日只回 VaR/drawdown(且 `insufficient_data`=1)。
4. **三 audience 的「表達紀律」是政策層,不是端點可驗證項**:本頁 L3 能證的是「tier 欄位存在 + 資料面可讀」;至於「user 不看 raw error」屬 `concepts/atlas-mcp-failover-policy.md` L4 政策條文,只能以條文 + 人工樣本驗,不能假裝有端點證據。

## 未消化 / 待補

- [ ] Step 3 跨 audience 實跑腳本,待寫(`scripts/dev/verify-audience-routing.py`;2026-09-27 複驗:該路徑不存在,`scripts/dev/` 只有 auto-commit-pr.sh／hooks／install-hooks.sh)
- [ ] 與 `concepts/atlas-mcp-failover-policy.md` v1.0 L4 源不可達散戶表達紀律銜接——L4 觸發時由 user audience 表達,不需要降級審批
