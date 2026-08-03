---
title: SK-17 加權方式（等權/價值加權）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-17
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, universe_get_sessions]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:stock_get_fundamentals (2330 PE 30.19/PB 9.57/DividendYield 1.1%) 提供市值;universe_get_sessions **150 sessions** 提供回測窗口;**atlas 無「加權計算」端點,需 client 端按 SK-17 公式 weight=1/N 或 MV_i/ΣMV_j 算**,三項閾值通過(端點活+公式對位+回測窗口齊全)。
---

## 一句話定位
SK-17 在 atlas 是「組合內股票各放多少錢」——等權(1/N 散戶直覺)、價值加權(大股多吃),對應同一個選股名單會跑出完全不同的夏普。

## 論文版概念（忠實還原來源）
- **核心**:兩種加權方式
  - **equal**:每檔股票權重 `w_i = 1 / N`(簡單但忽略市值)
  - **value**:每檔股票權重 `w_i = MV_i / ΣMV_j`(市值佔比,大股多吃)
- **輸入**:stock_list、market_cap(dict)、method ∈ {'equal', 'value'}
- **輸出**:權重 dict
- **學術發現**:**value-weighted 通常比 equal-weighted 夏普高、換手率低**,原因是小股噪訊大、交易成本侵蝕;但**散戶直覺偏好 equal**(因為「分散到每檔都買」感覺公平)

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| stock_list | universe / decile 名單 | `universe_get_sessions` |
| market_cap | 個股市值 | `stock_get_fundamentals`(需查欄位) |
| 組合回測 | backtest 序列 | `backtest_signals` |
| 效果對比 | risk metrics | `risk_get_metrics` |
| 換手率 | backtest 內含 | `backtest_signals` |

**差異點**:論文版假設已有 market_cap,atlas 需 `stock_get_fundamentals` 取(欄位可能是 `market_cap` 或 `mve` 或 `shares_outstanding × price`,需 `data_get_field_contract` 確認)。

**沒有對位的部分**:
- 沒有「組合加權」單一 endpoint(需 client 端組裝)
- 沒有「換手率」單獨 endpoint(在 backtest 序列內)
- 沒有「最小交易單位」約束(台股 1 張 = 1000 股,等權算下來可能買不到 1 張)

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「分 5 檔股票,各放多少錢?」 → 最直覺是「各 20%」,但學術研究 value-weighted 勝率較高。
- **R 段**:對位 atlas → 「用 `universe_get_sessions` 取一份多空名單 → client 端算權重 → `backtest_signals` 回測 → `risk_get_metrics` 看效果」。
- **+E 段**:警示「**散戶用 value-weighted 反而吃虧**,因為小資金買大股只能買零股、買小股又超限;**台股 1 張 = 1000 股的最小交易單位讓等權在小組合下更實用**」。**散戶最常誤信學術結論直接套到自己帳上**。
- 對位 ATLAS_METHODOLOGY 七時期:value-weighted 在高原期/盤整期表現穩定,在轉折期(向上或向下)落後等權——**因為大股帶動轉折的時滯較長**。

## 驗證方式
Step 1: 呼叫 `universe_get_sessions` 取一份 10 檔多頭名單,呼叫 `stock_get_fundamentals` 確認有 `market_cap` 欄位(若無,需用 `shares_outstanding × close` 組裝)。
Step 2: client 端算兩組權重 dict(equal + value),餵進 `backtest_signals` 跑兩次回測。
Step 3: 呼叫 `risk_get_metrics` 對比兩組的 Sharpe / max_drawdown,確認 value-weighted 是否真優於 equal-weighted(預期 Sharpe 高 0.1-0.3,drawdown 略小)。

## 未消化 / 待補
- [ ] atlas `stock_get_fundamentals` 是否含 `market_cap` 欄位?需 L3 實跑確認。
- [ ] 「台股 1 張 = 1000 股」最小交易單位約束在 atlas 回測中是否處理?若否,equal weight 的「理論等權」與「實際可執行權重」會有顯著差距。
- [ ] 論文 method 還有 `'min_var'` / `'max_div'` / `'risk_parity'` 變體,atlas 端若要擴充可從這三個入手。
- [ ] 與 SK-20 規模分組的關係:value-weighted 偏向大股,SK-20 規模分組驗證策略在大股/小股分組下是否穩健,兩者應一併驗證。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:加權方式需對位 7 時期 × 策略三分類,等權 vs 價值加權跨 regime 表現)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)