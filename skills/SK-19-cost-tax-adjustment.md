---
title: SK-19 交易成本與稅務調整
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-19
ingested_at: 2026-07-31
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics, report_get_tax_snapshot]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:backtest_signals sharpe_long=0.27/sharpe_short=0.49(交易成本前後);risk_get_metrics live session_count=147;report_get_tax_snapshot simulated 0(no positions,需真實持倉才有意義,誠實標);atlas cost model 預設 0.00654/0.003 需 parameters_get 確認(2026-08-02 20:30 實跑 `parameters_get` **401 unauthorized** atlas-go auth 問題,需 token;atlas 端問題不在我層可修);台灣 ETF 稅制:股票型 ETF 賣方證交稅 0.1%、債券型 ETF 免徵證交稅、無「配息稅」(配息走股利所得),atlas 端未對位,需 client 端修補;**2026-08-02 20:30 L3 頁面驗證 Step 2 確認:backtest_signals 回傳**無 gross_sharpe/net_sharpe 區分**(只有 sharpe_long + sharpe_short 兩欄),故 SK-19 line 49 「backtest_signals 是 gross 還是 net?」可勾 — **結論:無區分 = 預設應為 gross,需自行扣成本**。 **2026-08-22 audit-fix:修正 ETF 稅制與當沖稅率事實——股票型 ETF 賣方證交稅 0.1%(2017 起由 0.3% 調降)、債券型 ETF 免徵證交稅(落日多次延長,現行至 2026-12-31)、不存在「配息稅」(配息走股利所得:28% 分離課稅或併入綜所稅享 8.5% 抵減,每戶上限 8 萬元;單次股利給付 ≥2 萬元另扣二代健保補充保費 2.11%);0.3% 賣方證交稅為長期現制,2017-04-28 變革為當沖賣方稅率減半至 0.15%(2026-08-22 官方驗證:歷經 107/110/114 年三次延長,現行有效至 2027-12-31;稅率自始 0.15% 從無 0.25%/0.2% 中間稅率;立法依據=證交稅條例第 2-2 條,非第 2-3 條[權證避險])。** **2026-09-27 L3 重跑(三端點全 200):`parameters_get` 帶 `X-API-Key` 即 200(1669 key,`baseline.avg_trading_cost`=0.00654、`tax.transaction_tax_rate`=0.003、`tax.dividend_tax_rate`=0.28、`tax.nhi_surcharge_rate`=0.0211;1669 key 中**無當沖稅率鍵、無任何 fee/borrow 鍵**)⇒ 2026-08-02 的 401 是**缺 key**,非端點問題;`report_get_tax_snapshot` 今日回 **is_simulated=false、3 筆持倉**(2603.TW/2609.TW/00713.TW,before_tax_pnl=-1788.29、after_tax_pnl=-21788.18、total_tax_paid=19999.89),不再是 2026-08-01 的「simulated 0」;`backtest_signals` 今日回全 0;`parameters_get_audit_log` 回 `{"changes":null}`(改動史查不到)。**
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-sk39-short-cost）
l3_endpoints_probed:
  - "/api/parameters → 200 (11:30:42Z)｜/api/parameters/audit-log → 200 (11:31:04Z)"
  - /api/dashboard/tax-snapshot → 200 (11:30:42Z)｜/api/backtest/signals → 200 (11:30:42Z)｜/api/dashboard/risk → 200 (11:30:42Z)
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
| avg_trading_cost + tax_rate 預設值 | atlas 內部 cost model(預期有台股預設 0.00654 / 0.003) | `parameters_get` |
| 每月 turnover | session 內 monthly_turnover | `universe_get_session_detail` |
| raw → net 轉換 | backtest 結果是否區分 gross / net | `backtest_signals` |
| 淨報酬夏普 | 樣本外 risk-adjusted 指標 | `risk_get_metrics` |
| 已實現損益(稅務真值) | 實盤稅務快照 | `report_get_tax_snapshot` |

**差異點**:SK-19 是「回測層」的淨化,atlas 多了「實盤層」的 `report_get_tax_snapshot`——前者是模擬,後者是真實扣抵。對散戶而言實盤值才是決策錨點。

**雙邊成本口徑（2026-09-27 結案）**:atlas **不區分買進／賣出**——`internal/tax/taiwan_tax.go` 只有單一 `AvgTradingCost`（0.00654，＝手續費 0.1425%×券商折扣 ~0.6 ＋滑價的混合值）配 `TaxRate`（0.003，註明明確為 sell side only），以 `stockpicker.costs.round_trip_pct`=0.00585 這種「來回」口徑計算，故 SK-19 的合併公式與 atlas **1:1 對位**，不存在「atlas 單獨報買進成本」的錯位。

**借券費不在 SK-19 預設內（2026-09-27 結案）**：atlas 的 short 側只有 `backtest_signals.sharpe_short`（今日回 0），`internal/strategy_ranker` 對 short/side **0 命中**，1669 key 中 borrow/fee 各 0 ⇒ 「strategy_ranker 是否涵蓋 short 成本」的答案＝**沒有**。完整放空成本已獨立成頁 → `skills/SK-39-short-cost-model.md`。

**沒有對位的部分**:SK-19 預設台股 `tax_rate=0.003` 為「賣方」稅,但 ETF 與權證有不同稅制(股票型 ETF 賣方證交稅 0.1%、債券型 ETF 免徵證交稅(現行至 2026-12-31)、無「配息稅」)[2026-08-22 audit-fix],atlas 沒暴露「依標的調整稅率」的 tool。

## 散戶解讀(GROW+ 引用點)
- **G 段(目標)**:用戶若問「這策略一年能賺多少」→ **永遠先問「含成本嗎?」**;台股高週轉策略成本可吃掉 30% 以上 alpha。
- **R 段(現狀)**:對位實盤 → 「你上個月 turnover 多少?」 對位 atlas → 「`universe_get_session_detail` monthly_turnover 平均值多少?」 兩邊對齊才能驗證淨報酬預期。
- **+E 段(風險)**:警示「回測 15% 年化 → 實盤 8%」的真實落差,這是台股散戶最常見的策略夭折原因。

## 驗證方式
**L3 實跑（2026-09-27，本 PR）**：`parameters_get` 200（11:30:42Z）⇒ atlas 預設與 SK-19 公式**完全一致**：`baseline.avg_trading_cost`=0.00654、`tax.transaction_tax_rate`=0.003；源碼 `internal/tax/taiwan_tax.go` 的 `RoundTripCost = turnover × (AvgTradingCost + TaxRate)`、`NetReturn = rawReturn − RoundTripCost` 即 SK-19 公式本體（`AvgTradingCost` 註解＝手續費 0.1425% × 券商折扣 ~0.6 ＋滑價；`TaxRate` 註明 **sell side only**）。`parameters_get_audit_log` 200 ⇒ `{"changes":null}`（無改動史可核）。`report_get_tax_snapshot` 200 ⇒ `is_simulated` false、3 筆持倉、`after_tax_pnl` -21788.18（僅稅，不含手續費）。`backtest_signals` 200 ⇒ 今日全 0。

Step 1: 呼叫 `parameters_get` 確認 atlas cost model 預設是否為 `avg_trading_cost=0.00654` 與 `tax_rate=0.003`。
Step 2: 呼叫 `backtest_signals` 抽一條 active signal,看回傳欄位是否區分 gross_sharpe 與 net_sharpe。
Step 3: 呼叫 `report_get_tax_snapshot` 看實盤 realized gains 與 backtest 推算的 net return 是否在 10% 區間內(若差距過大代表 turnover 預期錯了)。
- `backtest_signals` 的 Sharpe **無 gross/net 之分**：只回 `sharpe_long`／`sharpe_short`（= 預設 gross）→ 扣成本須自行處理（2026-08-02 L3 確認）。

## 散戶稅後淨報酬三塊 [2026-08-22 audit-fix]

散戶實拿報酬 = 名目報酬 − 三塊成本：

(1) **證交稅**：賣方 0.3%、當沖賣出 0.15%（僅賣方課徵）。
(2) **手續費**：法定上限 0.1425% 買賣雙邊（券商折扣另計）。
(3) **股利稅 + 二代健保**：高股息策略必扣——28% 分離課稅或併入綜所稅享 8.5% 抵減（每戶上限 8 萬元）；單次股利給付 ≥2 萬元另扣補充保費 2.11%。

## 未消化 / 待補
- [ ] 當沖／ETF 稅制的**較低稅率**（當沖賣出 0.15%、股票型 ETF 賣方 0.1%）在 atlas 端**沒有欄位**：1669 key 只有單一 `tax.transaction_tax_rate`=0.003，tax snapshot 亦只帶 0.003 ⇒ 策略含當沖或 ETF 時，**client 端必須自行覆蓋稅率**（2026-09-27 實跑，見 §驗證方式）。
- [ ] `parameters_get_audit_log` 回 `{"changes":null}`（2026-09-27 實跑）⇒ `tax.transaction_tax_rate` 的設定／變更史**無法查證**，只能用當日快照值（第五條鐵律：附時點）。
