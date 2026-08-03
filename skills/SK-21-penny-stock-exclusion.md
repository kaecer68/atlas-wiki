---
title: SK-21 排除仙股穩健性檢驗
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-21
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [industry_sector_list, industry_sector_lookup, stock_get_quote, stock_get_fundamentals]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:industry_sector_list 38 個產業;industry_sector_lookup(2330)→半導體 12 成分股;stock_get_quote(2330 2026-08-01 23:42) last=2425/high 2425/low 2345;stock_get_fundamentals(2330) PE 30.19/PB 9.57/sector=semiconductor;**atlas 無「市值分組」端點,需 client 端用 stock_get_fundamentals 算市值後分 Big/Small**,台股 1 張=1000 股的最小交易單位需 client 端修補。
---

## 一句話定位
SK-21 在 atlas 是「策略會不會被仙股污染」的真值檢驗——剔除最低價 20% 股票重跑,若策略績效大幅衰退,代表 alpha 來自小股操縱/雜訊,實盤不可行。

## 論文版概念（忠實還原來源）
- **核心**:把每月股價最低 20% 股票剃掉,重新評估策略
- **輸入**:data(含股價/報酬/預測值)、`percentile_threshold=0.2`、strategy_func
- **動作**:
  1. 每月算股價第 20 百分位數
  2. 剔除股價 < 該分位數的股票
  3. 在篩選後樣本上重跑 strategy_func
  4. 輸出排除前後差異
- **為何重要**:**仙股(低價股)流動性差、操縱成本低、報價雜訊大**,任何在仙股上有顯著 alpha 的策略,實盤執行成本會吃掉所有利潤
- **散戶盲點**:**台股很多「飆股故事」發生在 < 20 元的仙股**,散戶看到「某策略一年賺 100%」就買,結果是仙股拉動,自己實際交易根本跟不上

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 股價資料 | 報價序列 | `stock_get_quote` |
| 市值確認 | 基本面(驗證低價股也是小股) | `stock_get_fundamentals` |
| 排除後回測 | backtest 序列 | `backtest_signals` |
| 效果對比 | risk metrics | `risk_get_metrics` |
| 排除名單規則 | 需 client 端實作 percentile filter | 缺(client) |

**差異點**:論文是純 Python 操作,atlas 沒有「價格百分位篩選」端點,需 client 端算每月第 20 百分位 + 過濾。

**沒有對位的部分**:
- 沒有「百分位篩選」endpoint
- 沒有「流動性指標」endpoint(仙股的流動性比股價更該看,需 `stock_get_chips` 對位成交量)
- 沒有「操縱風險標記」endpoint

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「這個策略 1 年賺 80%,要不要跟?」 → 反問「賺的錢是從哪幾檔來的?若是低於 20 元的股票占大多數,實盤你根本買不到足夠數量」。
- **R 段**:對位 atlas → 「`stock_get_quote` 拿現價 → client 端算每月第 20 百分位 → 排除後重跑 `backtest_signals` → `risk_get_metrics` 對比」。
- **+E 段**:警示「**排除仙股後若 Sharpe 從 2.0 掉到 0.3,這策略就別碰**;若 Sharpe 維持 1.5 以上,才是真 alpha」。對位 ATLAS_METHODOLOGY 七時期:仙股 alpha 在 RISK_ON 上升期特別亮眼(因為投機熱),在 RISK_OFF 黑天鵝期直接歸零——**散戶若只看到上升期就跑進去,實盤遇到一次黑天鵝就畢業**。
- 散戶實務:台股 1 張 = 1000 股,股價 < 10 元的股票要 1 萬本金才能買 1 張,**「等權」對小資族在仙股上根本不可行**。

## 驗證方式
Step 1: 呼叫 `stock_get_quote` 取 universe 全股票現價,client 端算第 20 百分位閾值(預期在 10-15 元區間)。
Step 2: client 端用 `universe_get_sessions` 拿一份策略名單,排除股價低於閾值的股票。
Step 3: 對排除前/後各跑一次 `backtest_signals`,呼叫 `risk_get_metrics` 對比 Sharpe / 換手率 / max_drawdown,看排除後是否仍維持 > 1.0 的 Sharpe。

## 未消化 / 待補
- [ ] atlas 沒有「流動性分位篩選」,光看股價可能漏掉「中價股但成交量極低」的隱性仙股;應加 `stock_get_chips` 對位。
- [ ] 排除比例 20% 是論文預設,實務該看產業:台灣電子股 80% < 20 元是常態,金融股 80% > 20 元,需分產業處理。
- [ ] 與 SK-20 規模分組的差別:SK-20 按市值切,SK-21 按股價切,兩個高度相關但不完全重疊(高價小股 vs 低價大股)。
- [ ] 「實盤流動性」需考量 bid-ask spread,atlas 目前無 spread 資料,需另尋 data source。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:仙股排除需對位 7 時期,不同時期仙股風險溢價不同)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)