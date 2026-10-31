---
title: SK-19 交易成本與稅務調整
description: "問「這策略一年能賺多少、含成本嗎」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-19
ingested_at: 2026-07-31
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics, report_get_tax_snapshot]
verification: 2026-11-01 L3 重跑（`/api/parameters` 200、`/api/dashboard/tax-snapshot` 200、`/api/backtest/signals` 200；時戳見 l3_endpoints_probed）：atlas 預設 `baseline.avg_trading_cost`=0.00654、`tax.transaction_tax_rate`=0.003、`tax.dividend_tax_rate`=0.28、`tax.nhi_surcharge_rate`=0.0211（1669 key，**無 fee／borrow／當沖稅率鍵**）；tax snapshot `is_simulated=false`、3 檔持倉（00878／1216／2886）、`total_tax_paid`=4350.54；`backtest_signals` 已非全 0（`sharpe_short`=0.5115、`sharpe_long`=0 ❓成因未說明；2026-09-27 當日為全 0）。**歷史更正保留**：2026-08-01 的 0.27／0.49 不可重現，不得當現值；2026-08-02 的 `parameters_get` 401 是**缺 X-API-Key**、非端點問題；`backtest_signals` 無 gross/net 之分 ⇒ 成本須自行扣。ETF 稅制與當沖 0.15% 見 §散戶稅後淨報酬三塊。
l3_run_at: 2026-11-01
l3_run_by: cio（refinement pass，atlas-wiki refinement cron）
l3_endpoints_probed:
  - "/api/parameters → 200 (2026-11-01T03:03:14+08:00)｜/api/dashboard/tax-snapshot → 200 (2026-11-01T03:03:14+08:00)"
  - "/api/backtest/signals → 200 (2026-11-01T03:02:00+08:00)｜/api/parameters/audit-log → 200 (2026-09-27T19:31:04+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:交易成本需對位 regime 切換,高波動期成本更高)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-19 在 atlas 是「回測報酬 → 實盤淨報酬」的最後一公里,把學術年化報酬壓回台股散戶的真實可到手金額。

## 論文版概念(忠實還原來源)
- **成本拆解**:`total_cost[t] = turnover[t] × (avg_trading_cost + tax_rate)`
- **台股預設**:`avg_trading_cost=0.00654`(雙邊手續費 + 證交稅結構簡化)、`tax_rate=0.003`(賣方交易稅)
- **淨報酬公式**:`net_return[t] = raw_return[t] − total_cost[t]`
- **輸入契約**:需要 `raw_returns`(原始月報酬)與 `turnover`(月度換股率)兩個 array
- **輸出**:與 raw 同長度的 `net_returns` 序列

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| avg_trading_cost + tax_rate 預設值 | atlas 內部 cost model(台股預設 0.00654 / 0.003，2026-11-01 複驗同值) | `parameters_get` |
| 每月 turnover | session 內 monthly_turnover | `universe_get_session_detail` |
| raw → net 轉換 | backtest 結果是否區分 gross / net | `backtest_signals` |
| 淨報酬夏普 | 樣本外 risk-adjusted 指標 | `risk_get_metrics` |
| 已實現損益(稅務真值) | 實盤稅務快照 | `report_get_tax_snapshot` |

**差異點**:SK-19 是「回測層」的淨化,atlas 多了「實盤層」的 `report_get_tax_snapshot`——前者是模擬,後者是真實扣抵。對散戶而言實盤值才是決策錨點。

**雙邊成本口徑（2026-09-27 結案）**:atlas **不區分買進／賣出**——`internal/tax/taiwan_tax.go` 只有單一 `AvgTradingCost`（0.00654，＝手續費 0.1425%×券商折扣 ~0.6 ＋滑價的混合值）配 `TaxRate`（0.003，註明明確為 sell side only），以 `stockpicker.costs.round_trip_pct`=0.00585 這種「來回」口徑計算，故 SK-19 的合併公式與 atlas **1:1 對位**，不存在「atlas 單獨報買進成本」的錯位。

**借券費不在 SK-19 預設內（2026-09-27 結案）**：atlas 的 short 側只有 `backtest_signals.sharpe_short`（2026-09-27 回 0；2026-11-01 為 0.5115），`internal/strategy_ranker` 對 short/side **0 命中**，1669 key 中 borrow/fee 各 0 ⇒ 「strategy_ranker 是否涵蓋 short 成本」的答案＝**沒有**。完整放空成本已獨立成頁 → `skills/SK-39-short-cost-model.md`。

**沒有對位的部分**:SK-19 預設台股 `tax_rate=0.003` 為「賣方」稅,但 ETF 與權證有不同稅制(股票型 ETF 賣方證交稅 0.1%、債券型 ETF 免徵證交稅(現行至 2026-12-31)、無「配息稅」)[2026-08-22 audit-fix],atlas 沒暴露「依標的調整稅率」的 tool。

## 散戶解讀(GROW+ 引用點)
- **G 段(目標)**:用戶若問「這策略一年能賺多少」→ **永遠先問「含成本嗎?」**;台股高週轉策略成本可吃掉 30% 以上 alpha。
- **R 段(現狀)**:對位實盤 → 「你上個月 turnover 多少?」 對位 atlas → 「`universe_get_session_detail` monthly_turnover 平均值多少?」 兩邊對齊才能驗證淨報酬預期。
- **+E 段(風險)**:警示「回測 15% 年化 → 實盤 8%」的真實落差,這是台股散戶最常見的策略夭折原因。

## 驗證方式

**L3 重跑（2026-11-01，refinement pass；每列附 http_code 與 +08:00 時戳）**

| 端點（GET 127.0.0.1:18080） | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/parameters` | 200 | 1669 key；`baseline.avg_trading_cost`=0.00654、`tax.transaction_tax_rate`=0.003、`tax.dividend_tax_rate`=0.28、`tax.nhi_surcharge_rate`=0.0211；fee／borrow／當沖稅率鍵 **0 命中** | 2026-11-01T03:03:14+08:00 |
| `/api/dashboard/tax-snapshot` | 200 | `is_simulated=false`、3 檔（00878／1216／2886）、`total_tax_paid`=4350.54、`before_tax_pnl`=-1812.73、`after_tax_pnl`=-6163.27（＝−1812.73−4350.54，僅稅不含手續費） | 2026-11-01T03:03:14+08:00 |
| `/api/backtest/signals` | 200 | **已非全 0**：`active_signals=["CIRCUIT_BREAKER"]`、`sharpe_short`=0.5115、`sharpe_long`=0（❓成因端點未說明）、`var_95`=-0.0148 | 2026-11-01T03:02:00+08:00 |

**跨日校正（本次新增）**：2026-09-27 的 tax snapshot 持倉為 2603／2609／00713、`total_tax_paid`=19999.89；2026-11-01 已換為 00878／1216／2886、`total_tax_paid`=4350.54 ⇒ **快照值不可跨日比較**，只能同日對照；`backtest_signals` 同理（09-27 全 0、11-01 非零），引舊值必須帶日期。

Step 1: 呼叫 `parameters_get` 確認 atlas cost model 預設是否為 `avg_trading_cost=0.00654` 與 `tax_rate=0.003`。
Step 2: 呼叫 `backtest_signals` 抽一條 active signal,看回傳欄位是否區分 gross_sharpe 與 net_sharpe。
Step 3: 呼叫 `report_get_tax_snapshot` 看實盤 realized gains 與 backtest 推算的 net return 是否在 10% 區間內(若差距過大代表 turnover 預期錯了)。
- `backtest_signals` 的 Sharpe **無 gross/net 之分**：只回 `sharpe_long`／`sharpe_short`（= 預設 gross）→ 扣成本須自行處理（2026-08-02 L3 確認，2026-11-01 複驗欄位未變）。

## 散戶稅後淨報酬三塊 [2026-08-22 audit-fix]

散戶實拿報酬 = 名目報酬 − 三塊成本：

(1) **證交稅**：賣方 0.3%、當沖賣出 0.15%（僅賣方課徵）。
(2) **手續費**：法定上限 0.1425% 買賣雙邊（券商折扣另計）。
(3) **股利稅 + 二代健保**：高股息策略必扣——28% 分離課稅或併入綜所稅享 8.5% 抵減（每戶上限 8 萬元）；單次股利給付 ≥2 萬元另扣補充保費 2.11%。

## 未消化 / 待補
- [ ] 當沖／ETF 稅制的**較低稅率**（當沖賣出 0.15%、股票型 ETF 賣方 0.1%）在 atlas 端**沒有欄位**：1669 key 只有單一 `tax.transaction_tax_rate`=0.003，tax snapshot 亦只帶 0.003 ⇒ 策略含當沖或 ETF 時，**client 端必須自行覆蓋稅率**（2026-09-27 實跑、2026-11-01 複驗同）。
- [ ] `parameters_get_audit_log` 回 `{"changes":null}`（2026-09-27 實跑）⇒ `tax.transaction_tax_rate` 的設定／變更史**無法查證**，只能用當日快照值（第五條鐵律：附時點）。
