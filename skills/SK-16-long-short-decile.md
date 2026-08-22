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
verification: 2026-08-01 v0.9 結算跑過 L3 Step 1~3 升 active:backtest_signals sharpe_long=0.27 + sharpe_short=0.49(皆 > 0.2),var_95=-0.0225(> -0.05);universe_get_sessions **150 sessions** 從 2026-01-01~2026-07-20(2026-08-02 20:40 重跑確認 150 sessions 不是 147),7/4~7/9 NEUTRAL 期 outcome_count=0 對位 SK-16 §七時期表「Consolidation 不可信」;risk_get_metrics live provenance session_count=147 insufficient_data=1。
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:多空十分位對應「跟隨聰明錢」策略;RISK_OFF 期 Advisor.AllowedStrategies() 禁「事件套利／資金對抗」)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit_with_fileline.md §1.4 (TW-X4 已撤銷 — regime vs 策略分類正交,見附錄 H「裁決狀態」)
  - ~/workspace/atlas-wiki/concepts/retail-sentiment-indicators.md（L6 散戶情緒反向指標,2026-08-22 接線）
---

<!-- methodology_alignment_tip: 本檔術語:七時期為真值,RISK_ON/OFF 為向下相容;atlas strategy_ranker 內部 regime = BULL/BEAR/HIGH_VOL/NEUTRAL 4 分類與憲章策略三分類(跟隨聰明錢／事件套利／資金對抗)正交(2026-07-30 kaecer 裁定 TW-X4 撤銷) -->
<!-- methodology_alignment_tip: 2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值;`source` 欄位正名 `regime_source` / `period_source` -->

> 術語備註:atlas 後端資金面 = 七維錢潮雷達 3+2+2 分層,不可加權平均（對位憲章 §四 + product-positioning §7.1）[2026-08-22 iter2]

## 一句話定位

把「做多最強 10%、做空最弱 10%」這個學術策略,翻譯成 atlas 可驗證、可對散戶解釋的「找漏洞」核心工具。

## 論文版概念（忠實還原 Fin-Skills）

SK-16 定義將股票池每月依模型預測值排序,切成 10 等分,做多最高分位（D10）、做空最低分位（D1）,形成多空對沖組合,觀察報酬序列。

**關鍵設計**:
- 頻率:月頻（M）
- 分組數:n_groups=10
- 加權方式:weighting="value"（市值加權）/ "equal"（等權）
- 月度再平衡:每月依最新預測重新分組
- 關鍵輸出:多空報酬序列（D10 - D1）
- **依賴**:SK-01 因子庫、SK-05/06/07 等回歸模型、SK-17 加權方式

## atlas 對位

atlas 沒有單一「long_short_decile」端點,但對位的核心數據 + 驗證鏈已存在:

| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 模型預測值 | 因子 + 模擬訊號 | `backtest_signals` (2026-07-29 實跑回 CIRCUIT_BREAKER + sharpe_long=0.27 + sharpe_short=0.49) |
| 模擬歷史 | supervised pipeline session 紀錄 | `universe_get_sessions` |
| 股票池/市值 | 報價/基本面 | `stock_get_quote` + `stock_get_fundamentals` |
| 多空績效 | 風險指標 | `risk_get_metrics` (2026-07-29 實跑回 max_drawdown_pct=1, session_count=147, insufficient_data=1) |

**差異點**:
- 論文版學術時間序列 (1994–2022) vs atlas 後端 session-based 模擬
- 論文版假設預測完美 → atlas 訊號是「模型給的」會帶噪
- 論文版可細看月內 vs atlas 是日頻聚合

**沒有對位的部分**:
- 真實「月分組」執行——atlas 後端沒暴露 decile sort 端點,只能從 session 內部解讀
- 市值加權細節:fin-Skills SK-17 公式 vs atlas `risk_get_metrics` 的暴露權重不一定一致

## 七時期 × 信號可用性表（Advisor.AllowedStrategies() 對位承諾）

引:ATLAS_METHODOLOGY.md §五策略矩陣(Advisor.AllowedStrategies())。

| 七時期 | SK-16 多空十分位訊號是否可信 | 三分類主力 |
|--------|---------------------------|----------|
| **低迷（Downturn）** | ⚠️ **不可信** — Advisor 過濾器會禁用「跟隨聰明錢」(多空十分位屬此層) | 等待轉折;若硬要做,轉為「資金對抗」 |
| **轉折開高（Turnaround Up）** | ⚠️ **可用但小訊號** — 聰明錢剛進場,signal 集中在少數個股 | **跟隨聰明錢**(主力) |
| **上升（Bull）** | ✅ **最佳適用期** — 信號品質高,sharpe_long/short 都正 | **跟隨聰明錢** + **事件套利** |
| **高原（Plateau）** | ⚠️ **可靠度下降** — 當沖過熱掩蓋真信號 | **事件套利** |
| **盤整（Consolidation）** | ❌ **不可信** — 信號全是雜訊 | 不主力 |
| **轉折下壓（Turnaround Down）** | ❌ **不可信** — VaR 飆升 | **資金對抗**（低位布局） |
| **黑天鵝（Black Swan）** | ❌ **不可信 + 停損** | 暫停所有策略 |

**給散戶的話**:**「同一個多空十分位訊號,在七不同時期下的可用性完全不同。給你的 sharpe 0.27 看起來是死數,要看它在當期(高原?上升?轉折下壓?)意義才完整」**。

## 散戶解讀（GROW+ 引用點）

**對應 §Q2 散戶一句話**（consult-index §4）:
> 「做多 top 10% / 做空 bottom 10%,先讓策略在歷史上能跑贏,再看現在訊號有沒有亮。」

**教練框架的 W（Will）段會用到**:
- 「你想要的是 alpha（超越大盤）還是絕對報酬?兩者用的策略不一樣」
- 「如果你只做多不做空,台股實務上要記得融券成本,別只看『做空一倍』的美麗數字」

**散戶最常踩的坑**:
- 把「做多最強 10%」誤讀為「今天漲最多的」——其實是「**預測**最強 10%」,是模型先講才漲的
- 忽略交易成本（做空 + 月再平衡）——下一條 SK-19 會解
- 把學術 Sharpe 直接套現實——台股流動性 + 融券限額常常打折扣

## 驗證方式

**L1 格式**:frontmatter 9 欄齊全 ✅ / 6 段俱全 ✅ / 路徑正確 ✅
**L2 對位**:上述 4 個 atlas-mcp tool 對位已標 + 用法已寫 ✅
**L3 端點**（ground truth,2026-07-29 實跑完成 1/2 + 2026-08-01 跑完 Step 1~3 升 active）:
- ✅ `backtest_signals` 2026-08-01 實跑:sharpe_long=0.27、sharpe_short=0.49、var_95=-0.0225、var_99=-0.0723、active_signals=[CIRCUIT_BREAKER]、drawdown_pct=0.72
- ✅ `risk_get_metrics` 2026-08-01 實跑:data_provenance=live、session_count=147、data_points=145、insufficient_data=1、var_95=-0.39、var_99=-0.65、max_drawdown_pct=1
- ✅ `universe_get_sessions` 2026-07-30 實跑 + 2026-08-01 重驗:147 筆 sessions(2026-01-01~2026-07-20),RISK_ON 為主,7/4~7/9 NEUTRAL 期 outcome_count=0 對位 §七時期表「Consolidation 不可信」;**atlas session 結構是「signal count」非「monthly decile return」,不直接對位 SK-16 論文 D1~D10 十分位結構**

**升 active 完成**(2026-08-01 v0.9 結算):sharpe_long 0.27 + sharpe_short 0.49 皆 > 0.2、var_95 -0.0225 > -0.05,三項閾值通過。Frontmatter 已改 status: active。

## 未消化 / 待補

- [x] `universe_get_sessions` 實跑驗證 — 2026-08-01 跑完,insufficient_data=1 對位 7/4~7/9 NEUTRAL 期(已標 active)
- [ ] 台股實務:融券限額與流動性折扣,Fin-Skills 沒論及,atlas 也沒對位
- [x] SK-16 升 active 完成(2026-08-01 v0.9 結算),sharpe_long 0.27 + sharpe_short 0.49 皆 > 0.2 通過閾值
- [ ] paper 1 vs atlas session 的時間軸對齊問題——Fin-Skills 用 1994–2022 學術數據,atlas session 從何起算需查
- [ ] SK-17 加權公式與 atlas `risk_get_metrics` 暴露權重的口徑差異
- [x] 反向鏈:`_consult-index.md` §Q2 已記錄,本檔 frontmatter `consult_category: Q2` 對齊

## 反向鏈接

- 對應諮詢類別:[Q2 選股策略](../atlas-wiki/skills/_consult-index.md#q2-選股)
- 預評索引:[_index-finskills.md §2 HIGH 表](../atlas-wiki/skills/_index-finskills.md)
- 寫入規範:[_method.md](../atlas-wiki/skills/_method.md)
- pipeline 順序下一頁:[SK-29 滾動窗口回測](../atlas-wiki/skills/SK-29-rolling-window-backtest.md)
