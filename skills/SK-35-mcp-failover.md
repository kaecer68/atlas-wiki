---
title: SK-35 atlas-mcp 失敗時 4 級 fallback 鏈(2026-08-07 D4 v1.0)
type: skill-inbound
source: concepts/atlas-mcp-failover-policy.md(2026-08-07 v1.0)
ingested_at: 2026-08-07
status: active
tier: T2
confidence: high
atlas_go_relevance: high
mcp_tools_used: [system_get_circuit_breaker, system_get_health, system_get_data_pipeline]
verification: "歷史(2026-08-07)：對位 concepts/atlas-mcp-failover-policy.md §4 4 級鏈 + hermes `data-source-decision` §1 三層架構；`system_get_circuit_breaker`/`system_get_health`/`system_get_data_pipeline` 三端點實跑 200。**2026-09-27 L3 實跑**：circuit-breaker 200 但 `state`=uninitialized／`initialized`=false、system-health 200(data_channels 全 ok、warnings 2 筆擁擠交易)、data-pipeline 200(來源全 ok、twse_replay lag 4m)；外部兩臂實測 —— **L2-A TPEx openapi 200**(真實報價)、**L2-B Yahoo chart 直連 429**；加密貨幣候選 CoinGecko 200。atlas 側 fail-closed 為真(`/api/parameters` 的 `stockpicker.flow_gateway.fail_closed_when_all_missing`=true)。見 §驗證方式。"
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b6）
l3_endpoints_probed:
  - "/api/dashboard/circuit-breaker → 200（state uninitialized） (2026-09-27T20:33:47+08:00)"
  - "/api/dashboard/system-health → 200（data_channels 全 ok） (2026-09-27T20:34:31+08:00)"
  - "/api/dashboard/data-pipeline → 200（來源全 ok） (2026-09-27T20:33:47+08:00)"
  - "/api/parameters → 200（fail_closed_when_all_missing=true） (2026-09-27T20:34:20+08:00)"
  - "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes → 200（L2-A） (2026-09-27T20:34:00+08:00)"
  - "https://query1.finance.yahoo.com/v8/finance/chart/NVDA → 429（L2-B） (2026-09-27T20:34:00+08:00)"
  - "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd → 200 (2026-09-27T20:34:48+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §三(對外發布規範)
related:
  - concepts/atlas-mcp-failover-policy.md(政策本體)
  - summaries/_division_of_labor_skills_vs_agent.md(分工)
  - skills/SK-33-audience-routing.md(audience 切換)
  - skills/SK-34-listed-otc-routing.md(範圍分流)
  - ~/.hermes/skills/data-source-decision/SKILL.md(三層架構)
amendable_by: kaecer
---

<!-- methodology_alignment_tip: 三 audience + 4 級 fallback + 來源標籤強制;對位 SK-00 §1 三條 pipeline 之外的元能力 -->

## 一句話定位

atlas-mcp 不在 atlas 範圍(上市/上櫃之外)或端點失敗時,**走 4 級 fallback 鏈**,任何引用強制附來源標籤 `[來源: atlas-mcp <tool_name> @ <ISO 8601>]` 或 `[來源: <站名> @ <URL> @ <ISO 8601>]`。

## 論文版概念 / 起源說明（忠實還原來源）

> 本 skill 屬 **skill-inbound**，原始設計來自 hermes `~/.hermes/skills/data-source-decision/SKILL.md` §1 三層架構（Layer 3 atlas-mcp → Layer 2 handler → Layer 1 HybridProvider + circuit breaker + fallback chain）。

| 工程概念 | 對位內容 | 經典出處 |
|---|---|---|
| **Circuit Breaker Pattern** | L1 失敗時進入熔斷；`system_get_circuit_breaker` 檢查狀態，避免持續對故障下游施壓 | Michael T. Nygard, *Release It!*, 2007 (2nd ed. 2018) |
| **Graceful Degradation / Cascading Fallback** | L2-A/B 公開資料源 → L3 誠實標示「不知道」，逐級降級而非直接失敗 | Netflix Hystrix 設計文檔（2012） |

**差異點**：經典模式討論通用分散式容錯；SK-35 具體化為 atlas-mcp 專用 4 級決策鏈，並疊加三層 audience 標籤紀律（對位 SK-33）。

## 4 級 fallback 鏈(對位 failover-policy.md §4)

### Level 1:atlas-mcp(範圍內)
上市/上櫃標的(2330/6488)→ `stock_get_*` / `industry_sector_lookup`;標籤 `[來源: atlas-mcp <tool> @ <ISO>]`;失敗訊號 5xx / circuit_breaker / not_available → 走 L2。

### Level 2-A:TPEx 公開網站(興櫃/上櫃但 atlas 失敗)
curl TPEx 公開端點;**風險**:15 分鐘延遲,atlas owner 不負責資料品質。

### Level 2-B:Yahoo Finance / Investing.com(海外/一般)
curl 公開端點;**風險**:rate limit(2026-09-27 實測本機直連 **429**,見下表)。

### Level 3:不知道(誠實標示)
不假裝、不猜測 → `[來源: 不知道]` + 引導補代碼/來源。**對位 SK-33**:user 看「抱歉,沒有這標的資料」;admin 看「L1 失敗 5xx、L2-A timeout、L2-B 429、L3 觸發、audit 全記錄」。

## atlas 對位

| 場景 | 觸發 | 路徑 | 標籤格式 |
|---|---|---|---|
| 2330 / 6488 | 上市/上櫃 | L1 atlas-mcp | `[來源: atlas-mcp <tool> @ <ISO>]` |
| atlas 失敗 503 | 系統熔斷 | L2-A TPEx / L2-B Yahoo | `[來源: <站名> @ <URL> @ <ISO>]` |
| NVDA | 海外 | L2-B Yahoo | 同上 |
| 興櫃 XYZ | 範圍外 | L2-A TPEx 興櫃 | 同上 |
| 比特幣 | 非股票 | L2-B Investing.com／CoinGecko | 同上 |
| 未知標的 | 沒有資料 | L3 不知道 | `[來源: 不知道]` |

**atlas 側的政策實作(2026-09-27 量到)**:`stockpicker.flow_gateway.fail_closed_when_all_missing=true`(三層全缺時 fail-closed,不是靜默放行)、`risk_gate.in_trade.circuit_breaker_daily_loss_pct=-0.05`、`risk_gate.post_trade.max_drawdown_halt_pct=0.2`、`risk_gate.pre_trade.var_limit_pct=0.02`(全部經 `/api/parameters` 實跑讀出)。

## 散戶解讀(對位 SK-33)
散戶:`[來源: 不知道]` → 看到「請提供代碼」,**不看到 error code**;開發者:看到完整端點錯誤(例 Yahoo 429);管理者:看到 L1→L2-A→L2-B→L3 全鏈 audit。

## 驗證方式

**歷史(2026-08-07)**:三個 system 端點實跑 200(見下表今日複驗)。

### L3 端點實跑（2026-09-27,本 PR）

| 端點／命令 | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/dashboard/circuit-breaker` | 200 | `state`=**uninitialized**、`initialized`=**false**、`consecutive_sl`=0、`events`=[](端點活著,但本部署**從未進入熔斷態**) | 2026-09-27T20:33:47+08:00 |
| `/api/dashboard/system-health` | 200 | `baseline_version`=v1、`replay_data_latest_date`=2026-09-24、`regime`=RISK_ON;`data_channels` 全部 `status: ok`(含 `us_yahoo` updated 2026-09-27T12:33:21Z);`warnings` 2 筆擁擠交易(0056.TW／00878.TW) | 2026-09-27T20:34:31+08:00 |
| `/api/dashboard/data-pipeline` | 200 | `sources` 全部 `status: ok`;`twse_replay` lag 4m、`us_yahoo`(producer=Yahoo Finance API) lag 0m | 2026-09-27T20:33:47+08:00 |
| `/api/parameters` | 200 | 1669 鍵;`fail_closed_when_all_missing`=**true**、`risk_gate.in_trade.circuit_breaker_daily_loss_pct`=-0.05 | 2026-09-27T20:34:20+08:00 |
| TPEx openapi(L2-A) | **200** | 真實報價(`Date` 1150924,含 ETF/個股 close/open/high/low)⇒ **L2-A 可用** | 2026-09-27T20:34:00+08:00 |
| Yahoo chart API(L2-B) | **429** | `Too Many Requests`(未帶 cookie 直連,174 ms 即回)⇒ **L2-B 本機不可直接用,需備援** | 2026-09-27T20:34:00+08:00 |
| CoinGecko simple price | 200 | `{"bitcoin":{"usd":84950}}` ⇒ 加密貨幣候選源可用(尚未納入 policy 正文) | 2026-09-27T20:34:48+08:00 |
| 源碼 `internal/llm/clients/circuit_breaker.go` + `internal/monitoring/service/circuitbreaker.go` | — | 兩層熔斷實作存在:LLM 客戶端 breaker(closed/…)與 dashboard 狀態機(`state`=uninitialized 由 service 層給) | 2026-09-27T20:36+08:00 |

**更正（2026-09-27）**

1. 「`system_get_circuit_breaker` 已實跑,確認熔斷狀態」需補口徑:今日 `state`=**uninitialized**、`initialized`=false、`events`=[] ⇒ 量到的是「端點可用、狀態未初始化」,**不是**「熔斷運作正常」。
2. **L2-B Yahoo 今日在本機被 429**(而 atlas 自己的 `us_yahoo` channel 在 system-health 仍 `status: ok`)⇒ 「channel ok」與「client 端直連可用」是兩件事,查證時不可互相推論。
3. 來源標籤紀律(2026-08-07 遺留的 checkbox 清單)已在 `concepts/atlas-mcp-failover-policy.md` 成文;本頁不再以 checkbox 記,改由該政策檔 + SK-33 承載。

## 未消化 / 待補

- [ ] 加密貨幣可靠公開源**選定**(候選 CoinGecko 2026-09-27 實測 200,選定仍待拍板)
- [ ] 對位 `agent://` 跨 session 標籤一致性(若用戶跨 session 引用同一標籤,需可追溯)
- [ ] 對位 SK-34 上市/上櫃分流優先序(哪個先走?)
- [ ] 對位 SOUL §3.7.3 第 6 條邊界(改 hermes runtime 設定不外推,本檔已對位)

> **2026-09-27 已解(移出本段)**:「Yahoo Finance / TPEx rate limit 實測」已跑 —— TPEx openapi **200**、Yahoo chart **429**(皆 2026-09-27T20:34:00+08:00)。
