---
title: atals 策略模擬指南：L1-L5 訊號驅動框架
created: 2026-08-02
updated: 2026-08-02
type: concept
tags: [framework, strategy, methodology]
sources:
  - atlas-mcp:strategy_list_active
  - atlas-mcp:strategy_ranker
  - atlas-mcp:universe_get_sessions
  - concepts/atals-strategy-taxonomy.md
  - concepts/atlas-mcp-interpretation-guide.md
confidence: medium
contested: false
contradictions: []
---

# atals 策略模擬指南（Simulation Guide）

> **一句話**：atals 策略模擬採用 L1（全球流動性）→ L2（外資行為）→ L3（產業催化）→ L4（匯率籌碼）→ L5（地緣政治）五層訊號驅動框架，搭配 Darwinian 權重動態調整與 PRISM cohort 訓練，共 12 個活躍策略。

本文件說明 atals 平台 **策略模擬、PRISM 訓練、回測驗證、Darwinian 權重、實驗管理** 的完整流程與解讀方式。LLM agent 在協助使用者做投資研究時，應先理解本指南所述的生命週期與指標語義。

相關入口：[[concepts/atals-strategy-taxonomy]]、[[concepts/atals-risk-management-framework]]、[[concepts/atals-platform-overview]]

延伸主題：[[concepts/atals-strategy-taxonomy|L1-L5 策略分類]]、[[concepts/atals-risk-management-framework|風險管理]]、[[concepts/atals-mcp-tools-reference|MCP 工具]]。

---

## 1. 策略模擬的完整流程

從 MCP 工具表面行為反推，Atlas 的策略模擬是一條 **由宏觀到個股、由歷史到即時、由單策略到組合優化** 的管線：

```
┌────────────────────────────────────────────────────────────────┐
│ ① 資料落地 → channel ingestion（Fugle/TWSE/Yahoo/FinMind）     │
│      ↓                                                           │
│ ② 分析聚合 → macro snapshot / capital flow / stress index       │
│      ↓                                                           │
│ ③ 訊號偵測 → L1–L5 訊號偵測器（strategy_list_active）           │
│      ↓                                                           │
│ ④ 權重決策 → Darwinian 權重調整（synergy_get_darwinian_status）  │
│      ↓                                                           │
│ ⑤ 組合配置 → sector_allocation_plan + get_recommendations        │
│      ↓                                                           │
│ ⑥ 個股選擇 → universe 模擬 session + PRISM cohort               │
│      ↓                                                           │
│ ⑦ 統計驗證 → backtest_signals + experiment_judge                 │
│      ↓                                                           │
│ ⑧ 報告輸出 → daily_report / report_get_performance              │
└────────────────────────────────────────────────────────────────┘
```

每個階段皆有對應的 MCP 工具可供追問、稽核與回放。

---

## 2. L1–L5 策略層級說明

> **注意**：以下層級定義係從 `strategy_get_layers`、`strategy_list_active`、`detector_registry_list` 等工具的命名與敘事觀察反推，並非官方完整公開規格。各層級下的具體偵測器請以 `strategy_list_active` 當下回傳為準。

> 對齊 atlas internal/strategy_techniques/enums.go canonical 定義（L1 全球流動性 / L2 外資行為 / L3 產業催化 / L4 匯率籌碼 / L5 地緣政治）[2026-08-22 iter2]

### 2.1 L1 — 全球流動性（Macro Drivers）
- **核心訊號**：美元指數（DXY）、美債 10Y/2Y 殖利率、VIX、美元/台幣匯率。
- **典型假說**：當 DXY 走弱、美債實質利率回落時，新興市場資金回流 → 台股外資偏多。
- **對應工具**：`macro_get_snapshot_latest`、`macro_get_snapshot_history`、`narrative_get_models` 中的 regime detector。

### 2.2 L2 — 外資行為（Institutional Flow）
- **核心訊號**：外資連續買超天數、投信持股變化、自營商避險部位、費半+外資同步確認。
- **典型假說**：外資連 3 日買超 + 投信不賣 → 短期動能延續。
- **對應工具**：`capital_flow_daily` / `capital_flow_summary`、`stock_get_chips`、`macro_get_capital_flow_latest`。
- **特殊觀察窗**：`synergy_get_l2_4_schedule` 揭露 L2.4 observation window（觀察期與切邊界）。

### 2.3 L3 — 產業催化（Cross-Market Linkage）
- **核心訊號**：S&P500、NASDAQ、SOX、NVDA、TSM ADR；美股四大指數同步性。
- **典型假說**：NVDA 與 TSM ADR 同漲 → 台積電（2330）隔日動能延續。
- **對應工具**：`crossmarket_get_us_indices`、`crossmarket_get_correlation`、`crossmarket_get_status`。

### 2.4 L4 — 匯率籌碼（Local Structure）
- **核心訊號**：融資餘額極端（過熱/過冷）、土洋對作訊號、央行匯市干預、VIX 結構。
- **典型假說**：融資餘額連 5 日增加 + 當沖比例 > 30% → 短期超買訊號。
- **對應工具**：`capital_flow_daily` 中的 retail/government 維度、`narrative_stress_index_thresholds`。

### 2.5 L5 — 地緣政治（Geopolitical Risk）
- **核心訊號**：台海緊張指數、中國 PMI / 放緩訊號、美國對中關稅政策、央行匯率干預。
- **典型假說**：台海風險升溫 + 美國關稅加碼 → 防禦性配置（`get_recommendations` 中的 defensive）。
- **對應工具**：`narrative_get_bundle` / `narrative_get_chains` / `narrative_stress_index_thresholds`、`event_calendar` / `event_flow_prediction`。

### 2.6 跨層組合
`get_recommendations` 回傳的 **portfolio-level 策略**（growth、momentum、defensive、all_weather、value）為跨 L1–L5 的最終配置組合；`strategy_list_active` 則回傳 **個別 signal detector**（如 `foreign-3day-inflow`、`margin-balance-extreme`）。兩者層級不同，不宜直接混用。

---

## 3. 策略評估指標

每個策略透過 `strategy_get_summary` 揭露以下指標：

| 指標 | 語義 | 解讀方式 |
|------|------|---------|
| `hit_rate` | 命中率（建議與實際方向一致的比例） | > 0.55 為可接受；> 0.65 為強訊號 |
| `total_hits` | 命中次數 | 與 `total_tests` 共同看 |
| `total_tests` | 總測試次數 | 樣本數；建議 > 30 才有統計意義 |
| `regimes` | 該策略在不同 regime（RISK_ON / RISK_OFF / NEUTRAL / TRANSITIONAL）下的表現 | 用 `regime_get_history` 對照 |
| `sharpe_short` / `sharpe_long` | 短/長期夏普比率 | > 1.0 為良好；< 0 需謹慎 |
| `drawdown_pct` | 最大回撤百分比 | 越小越穩健 |
| `risk` | 該策略的風險評級 | 由 `risk_get_calibration` 校正 |
| `sectors` | 該策略適用的產業清單 | 與 `industry_sector_list` 對照 |

LLM agent 在引用單一策略表現時，**必須同時引用 total_tests 與 regime 切換紀錄**，避免在小樣本或單一 regime 下過度推論。

---

## 4. Darwinian 權重機制

Darwinian 權重是 Atlas 在不同市場環境下 **自動調整策略權重** 的核心機制。

### 4.1 觀察當前狀態
```text
synergy_get_darwinian_status     → 哪些策略正在被 promote / demote、當前 weight delta
synergy_get_darwinian_trend      → 各策略 N 日權重趨勢（用 days 參數）
synergy_get_l2_4_schedule        → L2.4 觀察窗當前狀態與下個 boundary
```

### 4.2 運作邏輯（從可觀察行為反推）
- 每個策略都有 **baseline weight**（長期平均）與 **當前 weight**（近期表現調整後）。
- 當策略在近 N 日表現顯著優於同儕 → 權重 **上調**（promote）。
- 當策略失效率上升或 regime 切換導致不適配 → 權重 **下調**（demote）。
- 權重變動會同步寫入 `parameters_get_audit_log`，可追溯。

### 4.3 對 LLM agent 的注意事項
- 不要把 `synergy_get_darwinian_status` 的單次快照當成穩定狀態 — 它是動態的。
- 若要說明「為什麼這個策略佔比變高」，應同時讀取 `parameters_get_audit_log` 與 `strategy_get_summary` 的 regimes 區段。

---

## 5. PRISM 訓練

PRISM（推測為 "Portfolio Regime-Informed Strategy Model"）是 cohort-based 的策略訓練流程。

### 5.1 取得結果
```text
prism_get_training_results   → 最新 cohort 訓練結果（config + metrics）
```

### 5.2 訓練流程（從工具表面行為反推）
1. 將歷史資料切成多個 cohort（時間分段 + regime 分組）。
2. 每個 cohort 對所有 L1–L5 偵測器做樣本內最佳化。
3. 用樣本外（OOS）資料驗證，計算 Sharpe、drawdown、hit rate。
4. 表現良好的 cohort 配置會被 promote 到 baseline policy。

### 5.3 與 experiment_* 的關係
PRISM 訓練結果屬於 **模型層**；`experiment_*` 屬於 **策略層 A/B 測試**。兩者可獨立運作，也可串接：
- PRISM 訓練 → 產生 candidate experiment
- experiment_judge → 統計 Welch t-test、Sharpe stability、drawdown protection、OOS validation
- experiment_promote / experiment_revert → 套用到 baseline policy

---

## 6. 回測機制

### 6.1 取得回測狀態
```text
backtest_signals   → 當前 active signals、VaR 95/99、Sharpe short/long、drawdown_pct
backtest_status    → 最後一次自動回測日期、最後 portfolio value
```

### 6.2 回測特性（從工具說明反推）
- **基於歷史資料**的統計驗證，不涉及未來資料（look-ahead bias 防護）。
- 回測訊號與當前 **Darwinian 權重** 連動 — 若權重變動，回測結果會跟著變。
- 包含 **regime-conditioned backtest**：在不同 regime 下分別驗證。
- 不含 **slippage / transaction cost** 的精細模擬（須注意實際交易會有摩擦成本）。

### 6.3 解讀注意事項
- `var_95` / `var_99` 為歷史模擬 VaR，非蒙地卡羅預測。
- `drawdown_pct` 為歷史最大回撤，不代表未來不會突破。
- 若要看 **組合層級** 的回測，應優先用 `risk_get_drawdown` + `strategy_get_attribution`。

---

## 7. 模擬 Session 的生命週期

### 7.1 取得 session 清單
```text
universe_get_sessions                       → 近期 session 列表（id、date、status、top_strategies）
universe_get_session_detail(session_id)     → 單一 session 完整推薦結果 + summary
universe_get_universe_overlap               → 多 session 的 universe 重疊分析
```

### 7.2 Session 生命週期（從工具回傳欄位反推）
1. **建立（Created）**：排程觸發或手動觸發，universe 與參數快照寫入。
2. **執行中（Running）**：依序跑 L1–L5 偵測器 → Darwinian 權重套用 → sector allocation → 個股選擇。
3. **完成（Completed）**：個股清單 + 績效指標 + decision trace 寫入。
4. **過期（Archived）**：超出保留天數後進入 archive，但仍可透過 session_id 查詢。

### 7.3 單一 session 結構（推測欄位）
```json
{
  "session_id": "ses_20260802_morning",
  "date": "2026-08-02",
  "status": "completed",
  "universe": ["2330", "2454", "2303", ...],
  "top_strategies": ["foreign-3day-inflow", "margin-balance-extreme", ...],
  "summary": { "hit_rate": 0.62, "sharpe": 1.15, "drawdown": -0.08 },
  "decision_chains": [...],
  "trace_session_id": "trace_..."
}
```

LLM agent 在引用 session 結果時，**應明確標註 session_id 與 date**，避免將不同 session 結果混為一談。

---

## 8. 如何解讀模擬結果

### 8.1 從個股到決策鏈
```text
trace_get_decision_chain(symbol)   → 從 macro → sector → agent 的完整因果鏈
trace_get_reasoning(session_id)    → 該 session 的 RAG / CoT 推理步驟
trace_get_sim_latest               → 最新一次模擬推理 trace
trace_get_agent_observatory        → 當前所有 agent 的活動狀態
```

### 8.2 從策略到歸因
```text
strategy_get_attribution(id)   → 該策略在指定期間的歸因（哪些 regime / sector 貢獻最多）
```

### 8.3 從整體到報告
```text
report_get_performance                → 期間可配置（YTD / QTD / MTD）的完整績效
report_get_daily_summary              → 文字/結構化摘要
report_get_tax_snapshot               → 已實現損益、股利、外資稅額
report_get_export_link                → 簽署下載連結（短 TTL）
```

### 8.4 解讀 SOP（給 LLM agent 的建議步驟）
1. **確認 regime**：`macro_get_stress_index_current` + `regime_get_history`
2. **確認訊號**：`strategy_list_active` 篩選當前啟用的偵測器
3. **確認權重**：`synergy_get_darwinian_status` 看是否有近期 promote/demote
4. **確認組合**：`sector_allocation_plan` + `get_recommendations`
5. **確認個股**：`universe_get_session_detail` + `trace_get_decision_chain`
6. **驗證歷史**：`strategy_get_attribution` + `backtest_signals`
7. **確認風險**：`risk_exposure` + `risk_get_drawdown`
8. **輸出報告**：`explain_market_move`（中文解說）或 `report_get_performance`（量化報告）

---

## 9. 實驗管理（Experiment Lifecycle）

Atlas 的策略調整透過 **experiment** 物件管理：

| 工具 | 用途 |
|------|------|
| `experiment_diff` | 比較 candidate experiment 與 baseline 的 config + metrics 差異 |
| `experiment_history` | 歷史 judge 結果、promotions、reverts |
| `experiment_judge` | 觸發統計 replay judge（Welch t-test、Sharpe stability、drawdown protection、OOS validation）— 不呼叫 LLM |
| `experiment_promote` | 將 candidate 提升為 baseline policy（需 ATLAS_API_KEY） |
| `experiment_revert` | 撤銷 candidate，恢復原 baseline（需 ATLAS_API_KEY） |

LLM agent **不應主動呼叫 `experiment_promote` / `experiment_revert`**，這些操作屬於人類管理者決策範疇。

---

## 10. 常見誤判陷阱

| 陷阱 | 說明 |
|------|------|
| 小樣本 `hit_rate` 高 | `total_tests` < 30 時，命中率波動大，不可推論 |
| 單 regime 表現外推 | 策略在 RISK_ON 下表現好不代表 RISK_OFF 也好 — 必看 `regimes` |
| Darwinian 權重當成 static | 權重每日變動，引用時應附 timestamp |
| PRISM 結果當成未來保證 | PRISM 是 OOS 驗證，不是 forward-looking |
| 把 portfolio strategy 與 signal detector 混用 | `get_recommendations` 是組合層；`strategy_list_active` 是訊號層 |
| 忽略 `provenance` 與 `fallback` 欄位 | `sector_allocation_plan` 含 mutation receipt，務必讀取 |

---

## 11. 與其他文件的關係

- **架構與分層總覽**：`platform-overview.md`
- **完整 MCP 工具清單與調用順序**：`mcp-integration.md`

---

> **再次強調**：本平台所有回測、模擬、策略歸因結果皆為 **歷史統計**，不代表未來表現。LLM agent 對外引用時，必須附上資料時段、regime、total_tests 與 provenance。
## 相關入口

- [[concepts/atals-strategy-taxonomy]] — L1-L5 策略分類
- [[concepts/atals-risk-management-framework]] — 風險管理框架
- [[concepts/atals-platform-overview]] — 平台架構
