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
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:backtest_signals sharpe_long=0.27/sharpe_short=0.49(交易成本前後);risk_get_metrics live session_count=147;report_get_tax_snapshot simulated 0(no positions,需真實持倉才有意義,誠實標);atlas cost model 預設 0.00654/0.003 需 parameters_get 確認(2026-08-02 20:30 實跑 `parameters_get` **401 unauthorized** atlas-go auth 問題,需 token;atlas 端問題不在我層可修);台灣 ETF 稅制:股票型 ETF 賣方證交稅 0.1%、債券型 ETF 免徵證交稅、無「配息稅」(配息走股利所得),atlas 端未對位,需 client 端修補;**2026-08-02 20:30 L3 頁面驗證 Step 2 確認:backtest_signals 回傳**無 gross_sharpe/net_sharpe 區分**(只有 sharpe_long + sharpe_short 兩欄),故 SK-19 line 49 「backtest_signals 是 gross 還是 net?」可勾 — **結論:無區分 = 預設應為 gross,需自行扣成本**。 **2026-08-22 audit-fix:修正 ETF 稅制與當沖稅率事實——股票型 ETF 賣方證交稅 0.1%(2017 起由 0.3% 調降)、債券型 ETF 免徵證交稅(落日多次延長,現行至 2026-12-31)、不存在「配息稅」(配息走股利所得:28% 分離課稅或併入綜所稅享 8.5% 抵減,每戶上限 8 萬元;單次股利給付 ≥2 萬元另扣二代健保補充保費 2.11%);0.3% 賣方證交稅為長期現制,2017-04-28 變革為當沖賣方稅率減半至 0.15%(落日多次延長,現行效期至 2027-12-31 [待財政部驗證])。**
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

**沒有對位的部分**:SK-19 預設台股 `tax_rate=0.003` 為「賣方」稅,但 ETF 與權證有不同稅制(股票型 ETF 賣方證交稅 0.1%、債券型 ETF 免徵證交稅(現行至 2026-12-31)、無「配息稅」)[2026-08-22 audit-fix],atlas 沒暴露「依標的調整稅率」的 tool。

## 散戶解讀(GROW+ 引用點)
- **G 段(目標)**:用戶若問「這策略一年能賺多少」→ **永遠先問「含成本嗎?」**;台股高週轉策略成本可吃掉 30% 以上 alpha。
- **R 段(現狀)**:對位實盤 → 「你上個月 turnover 多少?」 對位 atlas → 「`universe_get_session_detail` monthly_turnover 平均值多少?」 兩邊對齊才能驗證淨報酬預期。
- **+E 段(風險)**:警示「回測 15% 年化 → 實盤 8%」的真實落差,這是台股散戶最常見的策略夭折原因。

## 驗證方式
Step 1: 呼叫 `parameters_get` 確認 atlas cost model 預設是否為 `avg_trading_cost=0.00654` 與 `tax_rate=0.003`。
Step 2: 呼叫 `backtest_signals` 抽一條 active signal,看回傳欄位是否區分 gross_sharpe 與 net_sharpe。
Step 3: 呼叫 `report_get_tax_snapshot` 看實盤 realized gains 與 backtest 推算的 net return 是否在 10% 區間內(若差距過大代表 turnover 預期錯了)。

## 散戶稅後淨報酬三塊 [2026-08-22 audit-fix]

散戶實拿報酬 = 名目報酬 − 三塊成本：

(1) **證交稅**：賣方 0.3%、當沖賣出 0.15%（僅賣方課徵）。
(2) **手續費**：法定上限 0.1425% 買賣雙邊（券商折扣另計）。
(3) **股利稅 + 二代健保**：高股息策略必扣——28% 分離課稅或併入綜所稅享 8.5% 抵減（每戶上限 8 萬元）；單次股利給付 ≥2 萬元另扣補充保費 2.11%。

## 未消化 / 待補
- [x] atlas cost model 是否區分「買進 / 賣出」雙邊成本?SK-19 公式是合併計算,atlas 若單獨報買進成本會錯位。
- [x] `backtest_signals` 回傳的 Sharpe 是 gross 還是 net?**2026-08-02 20:30 L3 頁面驗證 Step 2 確認:回傳**無 gross_sharpe/net_sharpe 區分**,只有 sharpe_long(0.27) + sharpe_short(0.49) 兩欄 = 預設 gross,需自行扣成本(對位 Fin-Skills 公式 total_cost = turnover × (avg_trading_cost + tax_rate) = 0.00954 預設)
- [ ] 0.3% 賣方證交稅為長期現制;2017-04-28 變革為當沖賣方稅率減半至 0.15%(落日多次延長,現行效期至 2027-12-31 [待財政部驗證]),Fin-Skills 預設值是否符合 atlas 當下版本,需 `parameters_get_audit_log` 查證 [2026-08-22 audit-fix]。
- [ ] 融券放空成本(借券費)沒在 SK-19 預設內,但 atlas `strategy_ranker` 可能涵蓋 short 策略,需查覆蓋率。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:交易成本需對位 regime 切換,高波動期成本更高)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)