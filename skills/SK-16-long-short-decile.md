---
title: SK-16 多空十分位數投資組合（atlas 對位版）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-16
ingested_at: 2026-07-29
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
consult_category: Q2
mcp_tools_used:
  - backtest_signals
  - universe_get_sessions
  - stock_get_fundamentals
  - risk_get_metrics
verification: 2026-08-01 v0.9 結算跑過 L3 Step 1~3 升 active:backtest_signals sharpe_long=0.27 + sharpe_short=0.49(皆 > 0.2),var_95=-0.0225(> -0.05);universe_get_sessions **150 sessions** 從 2026-01-01~2026-07-20(2026-08-02 20:40 重跑確認 150 sessions 不是 147),7/4~7/9 NEUTRAL 期 outcome_count=0 對位 SK-16 §七時期表「Consolidation 不可信」;risk_get_metrics live provenance session_count=147 insufficient_data=1。**2026-09-27 重跑(L3):`universe_get_sessions` 回 **90 sessions**(滾動窗,非 1994 起算)、`risk_get_metrics` session_count=210;`backtest_signals` 當日回 **全 0** ⇒ **2026-08-01 的 0.27/0.49 今日無法重現,不得當現值引用**。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-sk39-short-cost）
l3_endpoints_probed:
  - "/api/dashboard/sessions → 200 (2026-09-27T19:30:41+08:00)｜/api/dashboard/risk → 200｜/api/backtest/signals → 200｜/api/stock/fundamentals?symbol=2330 → 200（皆 11:30:42Z）"
  - "/api/dashboard/risk-exposure → 200 (2026-09-27T19:31:04+08:00)｜/api/dashboard/sessions/session-20260927-daily → 200 (2026-09-27T19:30:42+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(多空十分位屬「跟隨聰明錢」;RISK_OFF 期 Advisor.AllowedStrategies() 禁「事件套利／資金對抗」;2026-07-30 起 `period` 為 PeriodDetector 真值)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit_with_fileline.md §1.4 (TW-X4 已撤銷 — regime vs 策略分類正交,見附錄 H「裁決狀態」)
  - ~/workspace/atlas-wiki/concepts/retail-sentiment-indicators.md（L6 散戶情緒反向指標,2026-08-22 接線）
---

<!-- methodology_alignment_tip: 七時期為真值,RISK_ON/OFF 為向下相容;atlas strategy_ranker 內部 regime(BULL/BEAR/HIGH_VOL/NEUTRAL)與憲章策略三分類正交(2026-07-30 裁定 TW-X4 撤銷);2026-07-30 起 `period` 已是 PeriodDetector 真值、`source` 正名 `regime_source`/`period_source` -->

> 術語備註:atlas 後端資金面 = 七維錢潮雷達 3+2+2 分層,不可加權平均（對位憲章 §四＋product-positioning §7.1）[2026-08-22]

## 一句話定位

把「做多最強 10%、做空最弱 10%」這個學術策略,翻譯成 atlas 可驗證、可對散戶解釋的「找漏洞」核心工具。

## 論文版概念

SK-16 定義將股票池每月依模型預測值排序,切成 10 等分,做多最高分位（D10）、做空最低分位（D1）,形成多空對沖組合,觀察報酬序列。

**關鍵設計**:月頻（M）；n_groups=10；weighting=`value`（市值加權）／`equal`（等權）；每月依最新預測重新分組；輸出多空報酬序列（D10 − D1）。**依賴**:SK-01 因子庫、SK-05/06/07 回歸模型、SK-17 加權方式。

## atlas 對位

atlas 沒有單一「long_short_decile」端點,但對位的核心數據 + 驗證鏈已存在:

| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 模型預測值 | 因子 + 模擬訊號 | `backtest_signals` (2026-07-29 實跑回 CIRCUIT_BREAKER + sharpe_long=0.27 + sharpe_short=0.49) |
| 模擬歷史 | supervised pipeline session 紀錄 | `universe_get_sessions` |
| 股票池/市值 | 報價/基本面 | `stock_get_quote` + `stock_get_fundamentals` |
| 多空績效 | 風險指標 | `risk_get_metrics` (2026-07-29 實跑回 max_drawdown_pct=1, session_count=147, insufficient_data=1) |

**放空腿的可行性（2026-09-27 結案）**:Fin-Skills 未論及的「融券限額／流動性折扣」，atlas **0 對位**——`parameters_get` 1669 key 無任何融券/借券限額或借券費鍵、模擬 session 的 `side` 全為空、`backtest_signals` 無 borrow 成本欄。外部制度面（TWSE 總量管制 25%／10%／30%、標借費上限、平盤下規則）與 atlas 端的落差已獨立成頁 → `skills/SK-39-short-cost-model.md`；流動性折扣 → `skills/SK-37-liquidity-spread-screening.md`。

**差異點**:
- 論文版學術時間序列 (1994–2022) vs atlas 後端 session-based 模擬
- 論文版假設預測完美 → atlas 訊號是「模型給的」會帶噪
- 論文版可細看月內 vs atlas 是日頻聚合

**沒有對位的部分**:真實「月分組」執行（atlas 無 decile sort 端點，只能從 session 內部解讀）；市值加權細節（SK-17 公式 vs atlas 權重口徑，atlas 權重在 `risk_exposure` 而非 `risk_get_metrics`）。

## 七時期 × 信號可用性表（AllowedStrategies 對位）

引:ATLAS_METHODOLOGY.md §五。

| 七時期 | SK-16 多空十分位訊號是否可信 | 三分類主力 |
|--------|---------------------------|----------|
| **低迷（Downturn）** | ⚠️ **不可信** — Advisor 過濾器會禁用「跟隨聰明錢」(多空十分位屬此層) | 等待轉折;若硬要做,轉為「資金對抗」 |
| **轉折開高（Turnaround Up）** | ⚠️ **可用但小訊號** — 聰明錢剛進場,signal 集中在少數個股 | **跟隨聰明錢**(主力) |
| **上升（Bull）** | ✅ **最佳適用期** — 信號品質高,sharpe_long/short 都正 | **跟隨聰明錢** + **事件套利** |
| **高原（Plateau）** | ⚠️ **可靠度下降** — 當沖過熱掩蓋真信號 | **事件套利** |
| **盤整（Consolidation）** | ❌ **不可信** — 信號全是雜訊 | 不主力 |
| **轉折下壓（Turnaround Down）** | ❌ **不可信** — VaR 飆升 | **資金對抗**（低位布局） |
| **黑天鵝（Black Swan）** | ❌ **不可信 + 停損** | 暫停所有策略 |

**給散戶的話**:**同一個多空十分位訊號,在不同時期可用性完全不同；同一個 sharpe 要看當期才有意義**。

## 散戶解讀（GROW+）

**對應 §Q2 散戶一句話**（consult-index §4）:
> 「做多 top 10% / 做空 bottom 10%,先讓策略在歷史上能跑贏,再看現在訊號有沒有亮。」

**教練框架的 W（Will）段**:「你要 alpha（超越大盤）還是絕對報酬?兩者策略不同」「只做多不做空要記得融券成本,別只看『做空一倍』的美麗數字」

**散戶最常踩的坑**:
- 把「做多最強 10%」誤讀為「今天漲最多的」——其實是「**預測**最強 10%」,是模型先講才漲的
- 忽略交易成本（做空 + 月再平衡）——下一條 SK-19 會解
- 把學術 Sharpe 直接套現實——台股流動性與融券限額會打折扣（見 SK-37／SK-39）

## 驗證方式

**L1** ✅（10 欄／6 段齊全）　**L2** ✅（4 個 atlas-mcp tool 已標用法）

**L3 舊跑（2026-08-01，快照已過期）**：`backtest_signals` sharpe_long=0.27、sharpe_short=0.49、var_95=-0.0225；`risk_get_metrics` session_count=147。升 active 判準（2026-08-01 結算）：兩 sharpe 皆 > 0.2 通過。

**L3 端點（2026-09-27 重跑，本 PR）**：
- `universe_get_sessions` 200（11:30:41Z）：**90 sessions**，2026-06-27T23:26Z～2026-09-27T03:19Z；RISK_ON 49／RISK_OFF 40／NEUTRAL 1；78 筆 `top_strategies` 的 `side` 全為空字串。
- `risk_get_metrics` 200（11:30:42Z）：session_count=210、data_points=209、var_95=0、var_99=0、max_drawdown_pct=0.722、insufficient_data=1、source=postgres、gate_mode=NORMAL。
- `backtest_signals` 200（11:30:42Z）：**全 0**（active_signals=null），與 2026-08-01 的 0.27/0.49 不同 ⇒ 今日價值為 0，舊值不得當現值。
- `stock_get_fundamentals` 200（11:30:42Z）：2330 PE 30.19／PB 9.57／DividendYield 1.1（與 2026-07-30 同值）。
- `risk_exposure` 200（11:31:04Z）：position_count 3、cash_ratio 0.5228（`risk_get_metrics` 無權重欄位，權重看這條）。

**結論（2026-09-27）**：atlas session 是**滾動窗**（今日 90 筆），非 1994 起算序列；session 仍是「signal count」而非「monthly decile return」，D1~D10 無直接對位。

## 未消化 / 待補

> **2026-09-27 batch#4 結案（移出本段）**:加權公式比對**已完成** —— atlas 唯一權重欄位 `risk_exposure.concentration[].weight` = `market_value / portfolio_value`（**現金入分母**）:2609.TW 0.16183、00713.TW 0.16134、2603.TW 0.15399,合計 0.4771 = 1 − cash_ratio 0.5228 ⇒ 與 SK-17 的 equal-weight `1/N` **不同口徑**（3 檔等權各 0.3333、不含現金）。明細見 SK-17 §驗證方式。

## 反向鏈接

- 對應諮詢類別:[Q2 選股策略](../atlas-wiki/skills/_consult-index.md#q2-選股)
- 預評索引:[_index-finskills.md §2 HIGH 表](../atlas-wiki/skills/_index-finskills.md)
- 寫入規範:[_method.md](../atlas-wiki/skills/_method.md)
- pipeline 順序下一頁:[SK-29 滾動窗口回測](../atlas-wiki/skills/SK-29-rolling-window-backtest.md)
