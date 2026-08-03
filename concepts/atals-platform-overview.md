---
title: atals 平台概覽：台股策略模擬平台架構
created: 2026-08-02
updated: 2026-08-02
type: concept
tags: [framework, methodology]
sources:
  - atlas-mcp:mcp_quickstart
  - atlas-mcp:system_get_health
  - concepts/atlas-mcp-interpretation-guide.md
confidence: medium
contested: false
contradictions: []
---

# atals 平台概覽（Platform Overview）

> **一句話**：atals 是台股散戶投資人策略模擬與交易模擬平台，採用 Go+gin 後端 + Kafka 事件流，透過 MCP 對外提供 6 大類 40+ 工具，覆蓋從宏觀數據到策略模擬的完整投資決策鏈路。

本文件供 LLM agent 理解 atals 台股投資平台的整體定位、架構分層、對外介面與使用脈絡，作為後續策略模擬、風險控管與報告生成任務的入口導讀。

相關入口：[[concepts/atals-simulation-guide]]、[[concepts/atals-mcp-tools-reference]]、[[concepts/atals-strategy-taxonomy]]、[[concepts/atlas-mcp-interpretation-guide]]

延伸主題：[[concepts/atals-mcp-tools-reference|MCP 工具]]、[[concepts/atals-strategy-taxonomy|策略層級 L1-L5]]、[[concepts/taiwan-chip-flow-analysis|籌碼流分析]]。

---

## 1. 平台定位

Atlas 是專為 **台股散戶投資人** 設計的 **策略模擬與交易模擬平台**，核心目標：

- 把總體經濟、法人籌碼、技術指標、地緣風險等多源資訊，整合成可解釋的市場敘事（narrative）。
- 提供 **L1–L5 多層級訊號偵測器** 與 **Darwinian 權重動態調整機制**，自動產出每日投資組合建議（rebalance、sector allocation、position sizing）。
- 透過 **PRISM cohort 訓練** 與 **backtest 統計驗證**，量化每個策略的歷史勝率、夏普比率、最大回撤。
- 透過 **MCP（Model Context Protocol）介面** 把所有市場速覽、宏觀快照、策略訊號、風險指標、模擬結果，無差別開放給 LLM agent 進行二次推理。

平台 **不直接執行下單**；所有「建議」皆為模擬層輸出，協助使用者做研究、決策與回測。

---

## 2. 核心架構分層

從 MCP 工具表面行為反推，Atlas 後端採分層架構：

```
┌─────────────────────────────────────────────────────────────┐
│  LLM MCP 介面層  （atlas-mcp_* tools，本文件主要描述對象）    │
└─────────────────────────────────────────────────────────────┘
                          ▲
┌─────────────────────────────────────────────────────────────┐
│  報告層   daily_report / report_get_* / explain_market_move │
└─────────────────────────────────────────────────────────────┘
                          ▲
┌─────────────────────────────────────────────────────────────┐
│  風險層   risk_* / alert_* / control_*（斷路器、sector ban）  │
└─────────────────────────────────────────────────────────────┘
                          ▲
┌─────────────────────────────────────────────────────────────┐
│  模擬層   universe_get_sessions / backtest_* / experiment_* │
│           / prism_get_training_results                      │
└─────────────────────────────────────────────────────────────┘
                          ▲
┌─────────────────────────────────────────────────────────────┐
│  策略層   L1–L5 訊號偵測器、strategy_list_active、           │
│           Darwinian 權重、parameters_get_*                  │
└─────────────────────────────────────────────────────────────┘
                          ▲
┌─────────────────────────────────────────────────────────────┐
│  分析層   macro_get_*、capital_flow_*、narrative_*、         │
│           stress_index、crossmarket_*                       │
└─────────────────────────────────────────────────────────────┘
                          ▲
┌─────────────────────────────────────────────────────────────┐
│  資料層   Fugle / TWSE / Yahoo Finance / FinMind / 內部     │
│           channel ingestion pipeline  → Kafka event stream  │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 資料層（Data Layer）

- **資料源**：Fugle 即時報價、TWSE 集中市場、Yahoo Finance（美股/指數）、FinMind（基本面/籌碼）、內部自有資料流。
- **通道管理**：`system_get_data_pipeline`、`data_get_channels`、`channel_health`、`macro_get_ingest_status` 提供每個 channel 的最後抓取時間、錯誤率、延遲秒數。
- **事件流**：高頻 tick 與法人買賣超透過 Kafka 進入分析層，由 cron 排程（`scheduler_get_status`）定期聚合。

### 2.2 分析層（Analytics Layer）

- **宏觀快照**：`macro_get_snapshot_latest` / `macro_get_snapshot_history` 整合 DXY、美債殖利率、VIX、美元指數、台幣匯率等。
- **籌碼流**：`capital_flow_daily` / `capital_flow_summary` 提供七維錢潮雷達（3 官方 + 2 行為代理 + 2 領先訊號）。
- **壓力指數**：`macro_get_stress_index_current` / `taiwan_stress_index` 量化市場恐慌程度，驅動 regime 切換。
- **敘事引擎**：`narrative_get_bundle` / `narrative_get_events` / `narrative_get_chains` 把事件組裝成因果鏈。
- **跨市場**：`crossmarket_get_us_indices` / `crossmarket_get_correlation` 監看 S&P500、NASDAQ、SOX、NVDA、TSM ADR。

### 2.3 策略層（Strategy Layer）

- **L1–L5 分層**：由 `strategy_get_layers` 與 `strategy_list_active` 揭露，從總體經濟驅動到地緣政治風險。
- **Darwinian 權重**：根據近期表現自動調整策略權重（`synergy_get_darwinian_status` / `synergy_get_darwinian_trend`）。
- **參數管理**：`parameters_get` / `parameters_get_categories` / `parameters_get_metadata` 提供 darwinian、factor、optimizer、sizing、health、garch、experiment、baseline 等分類。
- **可解釋性**：`parameters_get_audit_log` 記錄每次參數變更（誰/為何/何時）。

### 2.4 模擬層（Simulation Layer）

- **模擬 session**：`universe_get_sessions` / `universe_get_session_detail` 提供個股 universe 的歷史模擬結果。
- **回測**：`backtest_signals` / `backtest_status` 提供 active signals、VaR、Sharpe、drawdown。
- **PRISM 訓練**：`prism_get_training_results` 回傳 cohort 訓練結果（config + metrics）。
- **實驗管理**：`experiment_diff` / `experiment_history` / `experiment_judge` / `experiment_promote` / `experiment_revert` 處理 A/B 測試流程。
- **決策追溯**：`trace_get_decision_chain` / `trace_get_reasoning` / `trace_get_sim_latest` 解釋為何推薦某檔個股。

### 2.5 風險層（Risk Layer）

- **風險指標**：`risk_get_metrics` / `risk_exposure` 提供 VaR 95/99、CVaR、最大回撤、現金比例。
- **斷路器**：`system_get_circuit_breaker` 監控每個外部呼叫點的熔斷狀態。
- **產業禁入**：`control_sector_ban` 對特定產業下達 ban override。
- **告警**：`alert_list` / `alert_scan` / `alert_get_rules` 提供 WARNING/ERROR/CRITICAL/INFO 分級。

### 2.6 報告層（Report Layer）

- **每日摘要**：`daily_report` / `report_get_daily_summary` 一站式晨報。
- **績效報告**：`report_get_performance` / `report_get_tax_snapshot` / `report_get_export_link`。
- **市場解說**：`explain_market_move` 用繁體中文解釋「為什麼漲跌」。

---

## 3. 平台技術棧

| 層級 | 技術 |
|------|------|
| 後端語言 | Go（gin framework） |
| 事件流 | Kafka（高頻 tick、法人買賣超、跨市場行情） |
| 排程 | 內建 cron dispatcher（`scheduler_get_status` 監控） |
| 資料庫 | PostgreSQL + TimescaleDB（推測，宏觀與策略指標含時間序列） |
| 快取 | 5 分鐘週期 on-disk cache（`macro_get_snapshot_latest` 註明 may lag real-time） |
| LLM 介面 | MCP（Model Context Protocol）— atlas-mcp_* tools |
| 部署 | Docker（atlas-go / atlas-mcp 等容器）；cron 與 daily-replay-sync 為獨立容器 |

---

## 4. MCP 工具總覽分類

完整 MCP 工具清單以 `mcp-integration.md` 為準；本章節僅列出 **任務導向分類**，協助 agent 快速路由。

### 4.1 市場速覽類（Quick Snapshot）
- `mcp_quickstart`：一站式速覽（macro + capital + regime + events）
- `daily_report`：每日完整 JSON 報告
- `report_get_daily_summary`：文字/結構化摘要
- `explain_market_move`：繁體中文「為什麼漲跌」解說

### 4.2 市場數據類（Market Data）
- `macro_get_snapshot_latest` / `macro_get_snapshot_history`
- `macro_get_capital_flow_latest` / `capital_flow_daily` / `capital_flow_summary`
- `crossmarket_get_us_indices` / `crossmarket_get_correlation` / `crossmarket_get_status`
- `stock_get_quote` / `stock_get_technical` / `stock_get_fundamentals` / `stock_get_chips`
- `industry_sector_list` / `industry_sector_lookup` / `sector_allocation_plan`

### 4.3 策略訊號類（Strategy Signals）
- `strategy_list_active`：L1–L5 啟用中的偵測器
- `strategy_get` / `strategy_get_summary` / `strategy_get_attribution`
- `strategy_ranker`：按表現排名（free / registered / premium tier 標記）
- `strategy_get_layers`：L1–L5 全層級配置
- `detector_registry_list`：24 個 template trigger detectors 的啟用狀態

### 4.4 投資組合類（Portfolio）
- `get_recommendations`：growth / momentum / defensive / all_weather / value 五種 tier-appropriate 配置
- `sector_allocation_plan`：模擬層 sector allocation snapshot（含 provenance、fallback、mutation receipt）
- `risk_exposure`：當前 portfolio VaR、drawdown、concentration

### 4.5 分析與敘事類（Narrative & Analysis）
- `narrative_get_bundle` / `narrative_get_events` / `narrative_get_chains`
- `narrative_get_models` / `narrative_get_templates` / `narrative_get_seasonal`
- `narrative_stress_index_thresholds`
- `event_calendar` / `event_flow_prediction`

### 4.6 模擬與回測類（Simulation）
- `universe_get_sessions` / `universe_get_session_detail` / `universe_get_universe_overlap`
- `prism_get_training_results`
- `backtest_signals` / `backtest_status`
- `experiment_diff` / `experiment_history` / `experiment_judge`

### 4.7 風險與告警類（Risk & Alert）
- `risk_get_metrics` / `risk_exposure` / `risk_get_drawdown`
- `risk_get_calibration` / `risk_get_correlation_matrix` / `risk_get_commentary`
- `system_get_circuit_breaker`
- `alert_list` / `alert_list_unacknowledged` / `alert_scan`

### 4.8 系統健康類（Observability）
- `system_get_health` / `system_get_metrics` / `system_get_metrics_trend`
- `system_get_data_pipeline` / `system_get_thresholds` / `system_get_maturity`
- `mcp_get_call_stats` / `mcp_get_tenant_usage` / `mcp_get_top_slow_tools`
- `mcp_get_session_topology` / `mcp_anomaly_get_recent`

### 4.9 控制類（Control — 需 API key）
- `control_pause_agent` / `control_resume_agent`
- `control_sector_ban` / `control_approve_recommendation` / `control_reject_recommendation`
- `experiment_promote` / `experiment_revert`
- `parameters_get_audit_log`
- `alert_acknowledge` / `alert_resolve` / `alert_silence`

---

## 5. 使用者角色與權限層級

Atlas 採用 **三層訂閱制**，於 `strategy_ranker` 的回傳中以 tier 標籤區分：

| Tier | 能力差異（MCP 工具可觀察） |
|------|---------------------------|
| **Free** | 可呼叫 `mcp_quickstart`、`daily_report`、`report_get_daily_summary`、`get_recommendations`（受限版）、`strategy_list_active` 等唯讀公開資料 |
| **Registered** | 加入完整 `strategy_get_summary` / `strategy_get_attribution` / `risk_get_metrics` / `capital_flow_daily` 七維資料 |
| **Premium** | 解鎖 sector allocation plan、PRISM cohort 細節、experiment_judge、attribution 完整指標 |

控制類（`control_*`、`experiment_promote/revert`、`parameters_*` 修改）**一律需要 `ATLAS_API_KEY`**，且操作會寫入 `control_get_audit_log`。

---

## 6. 資料更新頻率與延遲特性

| 工具 | 更新週期 | 延遲特性 |
|------|---------|---------|
| `stock_get_quote` | 即時 | FUGLE_API_KEY 驅動，盤中即時；盤後為收盤價 |
| `macro_get_snapshot_latest` | 5 分鐘 on-disk cache | 文件明註 "may lag real-time data" |
| `capital_flow_daily` | T+1 每日收盤後 | 官方法人 T86 為主，行為代理為即時推算 |
| `crossmarket_get_us_indices` | 即時 | Yahoo Finance live fetch，盤中美股時段即時 |
| `backtest_signals` | 即時 | 動態計算，與最新策略權重連動 |
| `risk_exposure` | 即時 | 與模擬 session 同步 |
| `parameters_get_metadata` | 事件驅動 | 參數變更時立即更新 |

---

## 7. MCP 介面統一存取點

所有工具以 `atlas-mcp_<category>_<action>` 命名，遵循 MCP 規範：

- **Transport**：stdio / SSE（由 MCP client 配置）
- **錯誤格式**：MCP `ToolResult` 含 `isError` 與 `error` content block
- **斷路器**：寫入類工具失敗會觸發 `system_get_circuit_breaker` 顯示 OPEN 狀態
- **審計**：`mcp_get_call_stats` / `mcp_get_tenant_usage` 記錄每個工具的呼叫次數、p50 延遲、錯誤率

---

## 8. 對 LLM agent 的建議工作流

```text
1. 健康檢查 → system_get_health
2. 一站式速覽 → mcp_quickstart
3. 細部追問 → capital_flow_summary → stock_get_chips(個股)
4. 策略檢視 → strategy_list_active → strategy_get_summary
5. 風險評估 → risk_exposure → risk_get_drawdown
6. 模擬驗證 → universe_get_sessions → experiment_diff
7. 報告輸出 → report_get_performance 或 explain_market_move
```

完整工作流範例、錯誤處理、控制操作注意事項，請參閱 `mcp-integration.md` 與 `simulation-guide.md`。

---

## 9. 文件索引

- `simulation-guide.md` — L1–L5 策略層級、PRISM 訓練、模擬 session 生命週期、結果解讀
- `mcp-integration.md` — 完整 MCP 工具清單、調用順序、組合範例、錯誤處理、安全注意事項

---

> **本平台所有輸出皆為研究與模擬性質，不構成投資建議。** LLM agent 對外引用任何策略或風控結論時，必須同時引用對應的 `source` 與 `provenance` 欄位，並遵守 `risk_get_commentary` 的風險提示。
## 相關入口

- [[concepts/atals-simulation-guide]] — 策略模擬與 PRISM 訓練生命週期
- [[concepts/atals-mcp-tools-reference]] — MCP 工具速查
- [[concepts/atals-strategy-taxonomy]] — L1-L5 訊號驅動策略分類
- [[concepts/atlas-mcp-interpretation-guide]] — MCP 解讀紀律
