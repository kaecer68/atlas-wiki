---
title: SK-16 多空十分位數投資組合（atlas 對位版）
description: "問「做多最強 10%、做空最弱 10% 怎麼跑」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-16
sources:
  - "制度面引文見 concepts/tw-short-cost-sources.md（操作辦法 115.01.09；2026-09-27 實測 200）"
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
verification: 2026-08-01 舊跑 sharpe_long=0.27／sharpe_short=0.49 **已不可重現**（2026-09-27、2026-11-01 兩次重跑皆不同值）⇒ 不得當現值引用。2026-11-01 重跑：`backtest_signals` 200（active_signals=[CIRCUIT_BREAKER]、sharpe_short=0.5115、sharpe_long=0 ❓成因端點未說明）、`risk_get_metrics` session_count=244、`universe_get_sessions` 滾動窗 90 筆。明細見 §驗證方式。
l3_run_at: 2026-11-01
l3_run_by: cio（refinement pass，atlas-wiki refinement cron）
l3_endpoints_probed:
  - "/api/backtest/signals → 200 (2026-11-01T03:02:00+08:00)｜/api/health → 200 (2026-11-01T03:02:00+08:00)"
  - "/api/dashboard/risk → 200 (2026-11-01T03:02:02+08:00)｜/api/dashboard/risk-exposure → 200 (2026-11-01T03:02:02+08:00)"
  - "/api/dashboard/sessions → 200 (2026-11-01T03:02:23+08:00)｜/api/stock/fundamentals?symbol=2330 → 200 (2026-11-01T03:02:02+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(多空十分位屬「跟隨聰明錢」;RISK_OFF 期禁「事件套利／資金對抗」;2026-07-30 起 `period` 為 PeriodDetector 真值)
related:
  - _methodology_alignment_audit_with_fileline.md §1.4（TW-X4 已撤銷 — regime 與策略分類正交，見附錄 H）
  - concepts/retail-sentiment-indicators.md（L6 散戶情緒反向指標，2026-08-22 接線）
---

> 術語備註:atlas 後端資金面 = 七維錢潮雷達 3+2+2 分層,不可加權平均（對位憲章 §四＋product-positioning §7.1）[2026-08-22]

## 一句話定位

把「做多最強 10%、做空最弱 10%」學術策略,翻譯成 atlas 可驗證、對散戶可解釋的「找漏洞」核心工具。

## 論文版概念

SK-16 將股票池每月依模型預測值排序,切 10 等分,做多最高分位（D10）、做空最低分位（D1）,形成對沖組合,觀察報酬序列。

**關鍵設計**:月頻（M）；n_groups=10；weighting=`value`（市值加權）／`equal`（等權）；每月依最新預測重新分組；輸出多空報酬序列（D10 − D1）。**依賴**:SK-01 因子庫、SK-05/06/07 回歸模型、SK-17 加權方式。

## atlas 對位

atlas 無單一「long_short_decile」端點,但核心數據 + 驗證鏈已存在:

| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 模型預測值 | 因子 + 模擬訊號 | `backtest_signals`（現值見 §驗證方式，勿引 2026-08-01 舊值） |
| 模擬歷史 | supervised pipeline session 紀錄 | `universe_get_sessions`（滾動窗 90 筆） |
| 股票池/市值 | 報價/基本面 | `stock_get_quote` + `stock_get_fundamentals`（無市值欄） |
| 多空績效 | 風險指標 | `risk_get_metrics`（`insufficient_data=1` ⇒ 勿把 `var_95=0` 當零風險） |

**放空腿（2026-09-27 結案）**:atlas **0 對位**——`parameters_get` 1669 key 無融券／借券限額／借券費鍵、session `side` 全空、`backtest_signals` 無 borrow 成本欄。外部制度面（TWSE 總量管制 25%／10%／30%、標借費上限、平盤下規則）→ `skills/SK-39-short-cost-model.md`；流動性折扣 → `skills/SK-37-liquidity-spread-screening.md`。

**差異點**:論文版為 1994–2022 學術長序列，atlas 是 session-based 模擬；論文版假設預測完美，atlas 訊號帶模型噪聲；論文版看月內，atlas 為日頻聚合。

**沒有對位的部分**:真實「月分組」執行（atlas 無 decile sort 端點，只能從 session 內部解讀）；市值加權細節（SK-17 公式 vs atlas 權重口徑，atlas 權重在 `risk_exposure`）。

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

**給散戶的話**:**同一訊號在不同時期可用性完全不同;sharpe 要看當期才有意義**。

## 散戶解讀（GROW+）

**對應 §Q2 散戶一句話**（consult-index §4）:
> 「做多 top 10% / 做空 bottom 10%,先讓策略在歷史上能跑贏,再看現在訊號有沒有亮。」

**教練框架的 W（Will）段**:「你要 alpha（超越大盤）還是絕對報酬?兩者策略不同」「只做多不做空要記得融券成本,別只看『做空一倍』的美麗數字」

**散戶常踩坑**:
- 把「做多最強 10%」誤讀為「今天漲最多的」——其實是「**預測**最強 10%」,是模型先講才漲的
- 忽略交易成本（做空 + 月再平衡）——下一條 SK-19 會解
- 把學術 Sharpe 直接套現實——台股流動性與融券限額會打折扣（見 SK-37／SK-39）

## 驗證方式

**L1** ✅（10 欄／6 段齊全）　**L2** ✅（4 個 atlas-mcp tool 已標用法）

**L3 現值（2026-11-01 實跑，全部 200）**

| 端點 | 實測結果 | timestamp |
|---|---|---|
| `/api/backtest/signals` | `active_signals=["CIRCUIT_BREAKER"]`、`sharpe_short=0.5115`、`sharpe_long=0`（❓ 單邊 0 成因端點未說明；另一邊非 0 ⇒ 非整體資料不足）、`var_95=-0.0148`、`drawdown_pct=0.7106` | 2026-11-01T03:02:00+08:00 |
| `/api/dashboard/risk` | session_count=244、data_points=243、`var_95=0`＋`insufficient_data=1` ⇒ **資料不足（門檻 252 筆），不是零風險**、max_drawdown_pct=0.7220、gate_mode=NORMAL | 2026-11-01T03:02:02+08:00 |
| `/api/dashboard/sessions` | **90 筆滾動窗**（2026-08-03～2026-10-31；RISK_ON 70／NEUTRAL 3／RISK_OFF 17）；`top_strategies` 180 列、`side` **全空** | 2026-11-01T03:02:23+08:00 |
| `/api/dashboard/risk-exposure` | position_count 3、cash_ratio 0.5163（權重口徑見 SK-17） | 2026-11-01T03:02:02+08:00 |
| `/api/stock/fundamentals?symbol=2330` | PE 30.19／PB 9.57／DividendYield 1.1（同 2026-07-30／09-27） | 2026-11-01T03:02:02+08:00 |

**跨日對位（兩次重跑一致的結構性結論）**
- **session 是滾動窗**：2026-09-27 回 90 筆（起點 2026-06-27）、2026-11-01 仍 90 筆（起點 2026-08-03）⇒ 視窗隨日推移，**非 1994 起算長序列**；`session_count` 則累積（147→210→244）。
- **D1~D10 無直接對位**：session 記的是訊號數與 conviction，不是月度十分位報酬。
- **`backtest_signals` 曾回空、現已恢復**：2026-09-27 為 `active_signals=null`、sharpe 全 0；2026-11-01 回 CIRCUIT_BREAKER ＋ `sharpe_short=0.5115` ⇒ 「端點無值」是**當日狀態**，不是端點性質；引舊結論必須帶日期。
- **2026-08-01 的 0.27／0.49 不得當現值**：與 2026-09-27、2026-11-01 兩次實測皆不同。

## 未消化 / 待補

> **2026-09-27 已結案**：atlas 唯一權重欄位＝`risk_exposure.concentration[].weight`（`market_value / portfolio_value`，**現金入分母**），與 SK-17 的 `1/N` 不同口徑；明細見 SK-17 §驗證方式。
> **2026-11-01 未解**：`sharpe_long=0` 的成因（無多單訊號／未計分／其他）端點與源碼皆未說明 ⇒ 待查；`backtest_signals` 無 `gross/net` 區分（成本面見 SK-19）。

## 反向鏈接

- 對應諮詢類別:[Q2 選股策略](../atlas-wiki/skills/_consult-index.md#q2-選股)
- 預評索引:[_index-finskills.md §2 HIGH 表](../atlas-wiki/skills/_index-finskills.md)
- 寫入規範:[_method.md](../atlas-wiki/skills/_method.md)
- pipeline 順序下一頁:[SK-29 滾動窗口回測](../atlas-wiki/skills/SK-29-rolling-window-backtest.md)
