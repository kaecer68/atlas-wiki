---
title: atlas MCP 工具參考：六類 40+ 工具速查
created: 2026-08-02
updated: 2026-08-02
type: concept
tags: [framework, methodology]
sources:
  - concepts/atlas-mcp-interpretation-guide.md
  - atlas-mcp:mcp_quickstart
confidence: high
contested: false
contradictions: []
---

# atlas MCP 工具參考（MCP Integration Guide）

> **一句話**：atlas MCP 提供 6 大類 40+ 工具（市場速覽、宏觀數據、資金流向、國際市場、策略訊號、風險管理），是 agent 存取 atlas 平台能力的統一介面，調用時應遵循「診斷 before fetch」的解讀紀律。

本文件提供 atlas 平台 **MCP（Model Context Protocol）介面的完整工具清單、調用順序、組合範例、錯誤處理與安全注意事項**，是 LLM agent 操作 atlas 的實務參考手冊。

相關入口：[[concepts/atlas-mcp-interpretation-guide]]、[[concepts/atals-platform-overview]]、[[concepts/atals-simulation-guide]]

延伸主題：[[concepts/atlas-mcp-interpretation-guide|MCP 解讀原則]]、[[concepts/atals-platform-overview|平台架構]]、[[concepts/atals-strategy-taxonomy|模擬策略]]。

---

## 1. MCP 介面概述

### 1.1 什麼是 MCP
MCP（Model Context Protocol）是把工具能力以 **結構化 JSON** 形式開放給 LLM agent 的標準協議。Atlas 透過 MCP 介面把後端所有市場數據、策略訊號、風險指標、模擬結果、控制能力，統一暴露為 `atlas-mcp_<category>_<action>` 命名空間的工具。

### 1.2 介面特性
- **唯讀為主**：絕大多數工具是 read-only（市場快照、策略列表、風險指標、回測結果）。
- **寫入需授權**：控制類工具（`control_*`、`experiment_promote/revert`、`alert_*` 變更、`parameters_*` 修改）一律需要 `ATLAS_API_KEY`。
- **快取策略**：宏觀類快照有 5 分鐘 on-disk cache；即時報價類（`stock_get_quote`）需 `FUGLE_API_KEY`。
- **錯誤透傳**：所有失敗以 MCP `ToolResult.isError=true` 加上人類可讀 `error` 內容回傳。

### 1.3 對 LLM agent 的建議
- **先讀類、後寫類**：讀資料不需要授權，但寫操作會被 audit log 記錄。
- **善用 one-shot endpoint**：`mcp_quickstart` 一次拿 macro + capital + regime + events，避免多次 round-trip。
- **組合呼叫**：以下章節提供典型工作流的調用順序範例。

---

## 2. 完整工具分類清單

### 2.1 市場速覽類（Quick Snapshot）

| 工具 | 用途 | 備註 |
|------|------|------|
| `mcp_quickstart` | 一站式速覽（macro + capital + regime + events） | 首次接入推薦 |
| `daily_report` | 最新每日報告 JSON（含全球資金總開關、台股七維錢潮雷達、事件日曆、策略訊號、風險提示） | 適合晨報摘要生成 |
| `report_get_daily_summary` | 文字/結構化摘要 | 可選擇 emoji 或 plain |
| `explain_market_move` | 繁體中文「為什麼漲跌」解說 | 含大盤表現、資金面、國際環境、風險提示 |

### 2.2 宏觀數據類（Macro Data）

| 工具 | 用途 |
|------|------|
| `macro_get_snapshot_latest` | 最新宏觀快照（on-disk cache，5 分鐘週期） |
| `macro_get_snapshot_history` | 過去 N 天快照（預設 30，最大 365） |
| `macro_get_capital_flow_latest` | 最新外資 / 法人 / 散戶資金流快照 |
| `macro_get_stress_index_current` | 當前台灣壓力指數（TRJ narrative） |
| `macro_get_stress_index_history` | 壓力指數歷史（days 參數） |
| `macro_get_ingest_status` | channel ingestion 狀態（last fetch times、error counts） |
| `taiwan_stress_index` | 台灣壓力指數（score、regime、components by source） |

### 2.3 資金流向類（Capital Flow）

| 工具 | 用途 |
|------|------|
| `capital_flow_daily` | 完整七維錢潮雷達（3 官方 + 2 行為代理 + 2 領先訊號） |
| `capital_flow_summary` | 簡明版七維摘要，僅官方三維共識 |
| `stock_get_chips` | 個股法人買賣超（foreign / domestic fund / dealer） |

### 2.4 國際市場類（Cross-Market）

| 工具 | 用途 |
|------|------|
| `crossmarket_get_us_indices` | 美股指數與科技股即時（live-fetched from Yahoo Finance） |
| `crossmarket_get_correlation` | 台灣產業 vs 美股指數相關性矩陣 |
| `crossmarket_get_status` | 跨市場資料源狀態、新鮮度、錯誤計數 |

### 2.5 個股資料類（Stock）

| 工具 | 用途 | 備註 |
|------|------|------|
| `stock_get_quote` | 最新 intraday 報價 | 需 FUGLE_API_KEY |
| `stock_get_fundamentals` | PE、PB、PS、dividend yield、sector | |
| `stock_get_technical` | SMA20、SMA50、RSI14（N 日，預設 90，最大 365） | |
| `stock_get_chips` | 三大法人買賣超（foreign / domestic fund / dealer） | |

### 2.6 產業分類類（Sector）

| 工具 | 用途 |
|------|------|
| `industry_sector_list` | 全部 20 個台股產業 canonical 識別（中英標籤 + 代表股） |
| `industry_sector_lookup` | 以 symbol 或 sector 名稱查產業 |
| `sector_allocation_plan` | 模擬層 sector allocation snapshot（含 provenance、fallback、mutation receipt） |

### 2.7 策略訊號類（Strategy）

> 對齊 atlas internal/strategy_techniques/enums.go canonical 定義（L1 全球流動性 / L2 外資行為 / L3 產業催化 / L4 匯率籌碼 / L5 地緣政治）[2026-08-22 iter2]

| 工具 | 用途 |
|------|------|
| `strategy_list_active` | 當前啟用的 L1–L5 偵測器（含 `foreign-3day-inflow` 等） |
| `strategy_get` | 單一策略完整 config + state metadata |
| `strategy_get_summary` | hit_rate、Sharpe、drawdown、regime behavior |
| `strategy_get_attribution` | 指定期間的策略歸因 |
| `strategy_ranker` | 按表現排名，含 free / registered / premium tier 標記 |
| `strategy_get_layers` | L1–L5 全部層級配置 |
| `detector_registry_list` | 24 個 template trigger detectors 啟用狀態 |
| `get_recommendations` | 組合層策略（growth / momentum / defensive / all_weather / value） |

> **時期 × 策略對位（2026-08-22 iter2 複查）**：
> - M1 ✅：`macro_get_snapshot_latest` 已公開 `current_period` + `current_period_name_zh` 七時期欄位（audit_state M1 ⬜→✅，#1488 註記不重複實作獨立 PeriodDetector 工具）
> - M4 ✅：`strategy_for_period`（period=downturn/turnaround_up/bull/plateau/consolidation/turnaround_down/black_swan）回傳適用策略 + category/priority，讀 `configs/methodology_rules.yaml` 同源 MethodologyAdvisor；2026-08-22 實跑 `bull` → allowed=[momentum, growth, event_arbitrage]
> - C2 狀態：`strategy_ranker` / `strategy_get_summary` 仍無 period 欄（2026-08-22 複查 atlas-go 源碼無 period 欄位）→ 對位改用 `strategy_for_period`，不再等 ranker 加欄

### 2.8 風險與告警類（Risk & Alert）

| 工具 | 用途 |
|------|------|
| `risk_get_metrics` | 當前 regime risk、VaR 估計、drawdown、exposure |
| `risk_exposure` | VaR 95/99、CVaR 95、max_drawdown_pct、cash_ratio、sector/factor/concentration 細項 |
| `risk_get_drawdown` | 當前回撤、peak drawdown、recovery stats |
| `risk_get_calibration` | 風險模型校正（predicted vs realized VaR） |
| `risk_get_correlation_matrix` | 跨策略相關性矩陣（風險集中度指標） |
| `risk_get_commentary` | 最新敘事風險解說（由 risk engine 自動生成） |
| `system_get_circuit_breaker` | 每個外部呼叫點的熔斷狀態 |

### 2.9 事件與敘事類（Event & Narrative）

| 工具 | 用途 |
|------|------|
| `event_calendar` | 未來 14 天市場事件（ETF rebalances、MSCI、revenue、shareholder meetings、window dressing、holidays） |
| `event_flow_prediction` | 5 日事件驅動資金流預測（含信心分數） |
| `narrative_get_bundle` | 編譯好的 briefing bundle（events + chains + templates） |
| `narrative_get_events` | 最新敘事事件（regime shifts、capital flows、macro shocks） |
| `narrative_get_chains` | 當前敘事鏈（cause-effect graphs） |
| `narrative_get_models` | 啟用中的敘事模型（regime detector、flow forecaster 等） |
| `narrative_get_templates` | cause-effect templates |
| `narrative_get_seasonal` | 最新 seasonal narrative packet（regime-by-month statistics） |
| `narrative_stress_index_thresholds` | 壓力指數的可配置閾值 |
| `template_detector_status` | template detector scan 結果（從 ledger 讀取最新 DetectionResult） |

### 2.10 模擬與回測類（Simulation）

| 工具 | 用途 |
|------|------|
| `universe_get_sessions` | 近期模擬 sessions（id、date、status、top_strategies） |
| `universe_get_session_detail` | 單一 session 完整推薦 + summary |
| `universe_get_universe_overlap` | 多 session 的 universe 重疊分析 |
| `prism_get_training_results` | PRISM cohort 訓練結果（config + metrics） |
| `backtest_signals` | 當前 active signals、VaR 95/99、Sharpe、drawdown |
| `backtest_status` | 最後自動回測日期、最後 portfolio value |
| `experiment_diff` | candidate vs baseline 的 config + metrics 比較 |
| `experiment_history` | 歷史 judge 結果、promotions、reverts |
| `experiment_judge` | 觸發統計 replay judge（Welch t-test、Sharpe stability、drawdown protection、OOS validation，**不呼叫 LLM**） |
| `trace_get_decision_chain` | 個股決策鏈（macro → sector → agent recommendation） |
| `trace_get_reasoning` | RAG / CoT 推理步驟（可指定 session_id） |
| `trace_get_sim_latest` | 最新模擬推理 trace |
| `trace_get_agent_observatory` | 當前所有 agent 活動狀態 |

### 2.11 系統健康類（Observability）

| 工具 | 用途 |
|------|------|
| `system_get_health` | 整體系統健康（HTTP: /api/dashboard/system-health） |
| `system_get_metrics` | 即時指標（request rate、error rate、circuit-breaker） |
| `system_get_metrics_trend` | per-minute 聚合趨勢 |
| `system_get_data_pipeline` | 資料 pipeline 狀態 |
| `system_get_thresholds` | SLO 閾值（latency、error rate、saturation） |
| `system_get_maturity` | 各模組成熟度（S/E/X/U） |
| `scheduler_get_status` | 排程狀態（哪些任務執行、最後結果） |
| `mcp_get_call_stats` | 近期呼叫統計（total calls、error count、p50 latency、per-tool breakdown） |
| `mcp_get_top_slow_tools` | p50 延遲最慢的工具 |
| `mcp_get_tenant_usage` | 各 tenant 使用統計 |
| `mcp_get_session_topology` | agent_id → tool call 矩陣 |
| `mcp_anomaly_get_recent` | 最近 anomaly events |

### 2.12 資料管線類（Data Pipeline）

| 工具 | 用途 |
|------|------|
| `data_get_channels` | 所有資料 channels 清單（fugle、twse、yahoo、finmind、internal）與狀態 |
| `data_get_channel_detail` | 單一 channel 細節（latency、error rate、last fetch） |
| `data_get_quality` | 資料品質指標（gaps、stale symbols、completeness by source） |
| `data_get_field_contract` | model field contract schema 內省 |
| `channel_health` | channel-level health summary |

### 2.13 LLM 與敘事監控類（LLM Router & Narrator）

| 工具 | 用途 |
|------|------|
| `llm_get_cost` | LLM cost snapshot（recent spend、by model、by capability） |
| `llm_get_health` | LLM router 健康（provider status、circuit-breaker、fallback chain） |

### 2.14 參數管理類（Parameters — 需授權）

| 工具 | 用途 | 授權 |
|------|------|------|
| `parameters_get` | 當前參數（flat key→type map） | 讀 |
| `parameters_get_categories` | 參數分類（darwinian、factor、optimizer、sizing、health、garch、experiment、baseline 等） | 讀 |
| `parameters_get_metadata` | 完整 provenance（value、rationale、source、citation、last_calibrated） | 讀 |
| `parameters_get_audit_log` | 參數變更審計 log | 讀 |
| `parameters_get_snapshots` | 歷史快照（預設 20 天） | 讀 |

### 2.15 控制類（Control — 需 ATLAS_API_KEY）

| 工具 | 用途 |
|------|------|
| `control_pause_agent` | 暫停特定 agent 的推薦 |
| `control_resume_agent` | 恢復已暫停的 agent |
| `control_sector_ban` | 對特定產業下達禁入 |
| `control_approve_recommendation` | 核准推薦 override（讀取狀態） |
| `control_reject_recommendation` | 拒絕推薦 override（讀取狀態） |
| `control_get_active_overrides` | 當前所有 active overrides（paused agents、sector bans、weight overrides） |
| `control_get_audit_log` | 控制變更審計 log |
| `experiment_promote` | candidate experiment 提升為 baseline |
| `experiment_revert` | 撤銷 candidate experiment |

### 2.16 告警管理類（Alert — 部分需授權）

| 工具 | 用途 |
|------|------|
| `alert_scan` | 掃描當前 in-flight alerts（含 severity counts、blocker status） |
| `alert_list` | 所有 alerts（含過濾） |
| `alert_list_unacknowledged` | 未確認 alerts（可選 severity、rule 過濾） |
| `alert_get_stats` | 告警統計（by severity、by source、ack latency） |
| `alert_get_rules` | 設定的告警規則（severity、threshold、channels） |
| `alert_acknowledge` | 確認告警（需授權） |
| `alert_resolve` | 解除告警（需授權） |
| `alert_silence` | 對特定 rule silence 一段時間（需授權） |
| `mcp_anomaly_ack` | 確認 anomaly alert |

### 2.17 任務與排程類（Task & Scheduler）

| 工具 | 用途 |
|------|------|
| `task_list` | 列出 background tasks（可依 status 過濾） |
| `task_get` | 單一 task（status、progress、last result） |
| `task_get_events` | 單一 task 的事件流（ordered lifecycle events） |
| `scheduler_get_status` | 排程狀態（哪些任務跑了、何時、最後結果） |

### 2.18 Roots 與檔案讀取類（Roots — 受宣告範圍限制）

| 工具 | 用途 |
|------|------|
| `mcp_roots_list` | 列出連線 MCP client 宣告的 file:// roots |
| `mcp_roots_read_file` | 讀取 root 下的檔案（read-only、path-traversal hardened、audited） |

---

## 3. 推薦的調用順序與工作流

### 3.1 晨報三分鐘（Three-Step Morning Briefing）

```text
Step 1: mcp_quickstart                  → 一次拿 macro + capital + regime + events
Step 2: capital_flow_summary            → 確認三大法人方向
Step 3: strategy_list_active            → 看當前啟用的 L1–L5 偵測器
```

可選補丁：
```text
risk_exposure                          → 確認當前 portfolio VaR
sector_allocation_plan                 → 確認 sector 配置（含 mutation receipt）
explain_market_move                     → 中文解說（給人類讀者）
```

### 3.2 個股深度研究（Deep Dive on Symbol）

```text
Step 1: stock_get_quote                 → 即時報價
Step 2: stock_get_fundamentals          → PE/PB/殖利率/sector
Step 3: stock_get_technical             → SMA20/50、RSI14
Step 4: stock_get_chips                 → 三大法人買賣超
Step 5: industry_sector_lookup(symbol)  → 所在產業 canonical ID
Step 6: strategy_get_attribution        → 該個股適用的策略歸因
Step 7: trace_get_decision_chain        → 完整決策鏈（macro → sector → agent）
```

### 3.3 風險評估（Risk Assessment）

```text
Step 1: risk_get_metrics                → aggregate metrics
Step 2: risk_exposure                   → VaR 95/99、CVaR、concentration
Step 3: risk_get_drawdown               → 當前/peak/recovery
Step 4: risk_get_calibration            → predicted vs realized VaR
Step 5: alert_list_unacknowledged       → 未確認告警
Step 6: system_get_circuit_breaker      → 外部呼叫熔斷狀態
```

### 3.4 模擬驗證（Simulation Verification）

```text
Step 1: universe_get_sessions           → 近期 sessions
Step 2: universe_get_session_detail     → 挑特定 session 看完整推薦
Step 3: experiment_diff                 → candidate vs baseline
Step 4: experiment_judge                → 統計 replay judge（不呼叫 LLM）
Step 5: backtest_signals                → 當前 active signals
Step 6: prism_get_training_results      → 最新 cohort 訓練結果
```

### 3.5 報告輸出（Reporting）

```text
Step 1: report_get_daily_summary        → 文字/結構化摘要
Step 2: report_get_performance          → 期間可配置（YTD/QTD/MTD）績效
Step 3: report_get_tax_snapshot         → 稅務快照
Step 4: report_get_export_link          → 簽署下載連結（短 TTL）
```

### 3.6 系統健康檢查（Health Check）

```text
Step 1: system_get_health               → 整體健康
Step 2: system_get_metrics              → 即時指標
Step 3: system_get_data_pipeline        → 資料流狀態
Step 4: scheduler_get_status            → 排程狀態
Step 5: mcp_get_call_stats              → MCP 呼叫統計
Step 6: mcp_anomaly_get_recent          → 最近 anomalies
```

---

## 4. 工具組合使用範例

### 4.1 三步驟晨報（給 LLM agent 的完整 prompt pattern）

```text
1. mcp_quickstart
2. 解析 regime：若 RISK_OFF → capital_flow_summary 看外資是否連賣
3. 解析 strategy：strategy_list_active → 篩選 L2（外資行為）偵測器
4. 補丁：explain_market_move(format="plain") 生成中文解說
```

### 4.2 風險警報處置

```text
1. alert_scan → 找到 severity=CRITICAL 的告警
2. alert_get_rules → 確認該 rule 的 threshold
3. risk_exposure → 看當前 portfolio 是否觸及該 threshold
4. （人類決策）alert_acknowledge 或 alert_silence
```

> **注意**：步驟 4 的確認與 silence 需授權，LLM agent **不應主動執行**，應把人類決策建議輸出。

### 4.3 產業配置合理性檢查

```text
1. sector_allocation_plan → 取得當前 sector 配置（含 provenance）
2. industry_sector_list → 對照全部 20 個產業
3. risk_get_correlation_matrix → 看 sector 間相關性是否過度集中
4. （若需要）experiment_diff → 比較不同 sector 配置 candidate
```

### 4.4 敘事鏈追溯（Debugging 推薦）

```text
1. narrative_get_events → 找到最新事件
2. narrative_get_chains → 取得該事件的因果鏈
3. trace_get_decision_chain(symbol) → 追溯到具體個股決策
4. trace_get_reasoning(session_id) → 看 LLM 推理步驟
5. parameters_get_audit_log → 確認當時參數狀態
```

---

## 5. 錯誤處理

### 5.1 常見錯誤情境

| 情境 | 症狀 | 處置 |
|------|------|------|
| **API key 缺失** | `control_*` / `experiment_promote` 回傳 401/403 | LLM agent 不應嘗試繞過，請使用者提供 ATLAS_API_KEY |
| **斷路器熔斷** | 工具回傳 `circuit breaker is OPEN` | 等待 `system_get_circuit_breaker` 顯示 HALF_OPEN → CLOSED 再試 |
| **資料延遲** | `macro_get_snapshot_latest` 註明 may lag | 改用 `crossmarket_get_us_indices`（live）或降低期待 |
| **樣本不足** | `strategy_get_summary` total_tests < 30 | 不要做強結論，明確標註「小樣本」 |
| **session 不存在** | `universe_get_session_detail` 回 404 | 改用 `universe_get_sessions` 拿有效 id |
| **FUGLE_API_KEY 缺失** | `stock_get_quote` 回 503 | 改用 `stock_get_technical`（歷史技術指標，不需 key） |

### 5.2 斷路器行為

`system_get_circuit_breaker` 揭露每個外部呼叫點的熔斷狀態：

- **CLOSED**：正常，請求可通過
- **OPEN**：熔斷中，請求直接失敗（不消耗後端資源）
- **HALF_OPEN**：探測恢復，少量請求通過觀察成功率

LLM agent 遇到 OPEN 狀態時，**應自動改用其他資料源或暫停該類請求**，而非重試硬塞。

### 5.3 重試策略

- **指數退避（exponential backoff）**：連續失敗 3 次後等待 1s → 2s → 4s。
- **替代路徑**：若 `stock_get_quote` 失敗，改用 `stock_get_technical` 取得最近收盤技術指標。
- **降級輸出**：若所有資料源失敗，明確告知使用者「目前無法取得即時資料」並提供上一次快照時間戳。

---

## 6. 安全注意事項

### 6.1 API Key 使用

| Key | 用途 | 存放建議 |
|-----|------|---------|
| `ATLAS_API_KEY` | 控制類（`control_*`、`experiment_promote/revert`、`parameters_*` 修改、`alert_acknowledge/resolve/silence`） | 環境變數或 secret manager，**絕不入 git** |
| `FUGLE_API_KEY` | 即時報價 `stock_get_quote` | 同上 |

LLM agent **絕不應** 把 API key 寫入日誌、回應或 commit 訊息。

### 6.2 敏感操作限制

下列操作需 ATLAS_API_KEY，且會寫入 `control_get_audit_log` 或 `parameters_get_audit_log`：

- 暫停/恢復 agent
- 產業禁入
- 核准/拒絕推薦 override
- 提升/撤銷 experiment
- 修改 parameters
- 確認/解除/沉默 alert

**LLM agent 對這些操作應採取「只讀不寫」原則**：
- 可讀取 `control_get_active_overrides`、`control_get_audit_log`、`parameters_get_audit_log`
- **不應主動呼叫寫入工具**，應把建議交給人類管理者決策。

### 6.3 資料敏感性

- `universe_get_session_detail` 與 `strategy_get_attribution` 可能含 **模擬層內部推理** — 對外引用應摘要，避免暴露完整 reasoning trace。
- `report_get_tax_snapshot` 含 **個人稅務資料** — 應視為機敏資料，不寫入對外 channel。
- `parameters_get_metadata` 的 `citation` 與 `rationale` 欄位可能含內部備註，引用前應檢查。

### 6.4 審計與可追溯性

所有寫入操作皆有審計：
- `control_get_audit_log`：控制類操作
- `parameters_get_audit_log`：參數變更
- `mcp_get_call_stats` / `mcp_get_tenant_usage`：呼叫次數與錯誤率
- `mcp_get_session_topology`：agent → tool 對應關係

LLM agent 在執行寫入操作前，**應先說明「這個操作會被 audit log 記錄」**，並要求使用者明確授權。

---

## 7. 對 LLM agent 的工程建議

### 7.1 避免過度呼叫
- 單次工作流不超過 **15 個工具呼叫**；超過則考慮 batch 或摘要。
- 同一 session 內，`mcp_quickstart` 只需呼叫一次，重複呼叫浪費 round-trip。
- `system_get_health` 等可觀察性工具不應在主流程中反覆呼叫，移到除錯階段。

### 7.2 善用快取
- 5 分鐘內重複詢問同一 `macro_get_snapshot_latest` 不會得到新資料 — 直接用前次結果。
- `strategy_list_active` 結果在 regime 不變時相對穩定，可短期快取。

### 7.3 錯誤降級
- 不要因為單一工具失敗就放棄整個工作流。
- 建議實作 fallback chain：`quickstart → capital_flow → strategy → risk → report`，任何一步失敗都應有備援路徑。

### 7.4 Prompt Hygiene
- 在 system prompt 中標明當前訂閱 tier（free / registered / premium）。
- 引用數據時附 timestamp 與 source。
- 對風險/虧損/預測類輸出，必須附上 `risk_get_commentary` 的風險提示。

---

## 8. 文件索引

- `platform-overview.md` — 平台總覽、架構分層、技術棧、tier 權限
- `simulation-guide.md` — L1–L5 策略層級、PRISM 訓練、模擬 session 生命週期、結果解讀

---

> **本平台所有輸出為研究與模擬性質，不構成投資建議。** LLM agent 對外引用任何資料、策略、風險結論時，必須附上對應的 source、provenance、timestamp 與 risk commentary。
## 相關入口

- [[concepts/atlas-mcp-interpretation-guide]] — MCP 解讀紀律
- [[concepts/atals-platform-overview]] — 平台架構
- [[concepts/atals-simulation-guide]] — 模擬流程
