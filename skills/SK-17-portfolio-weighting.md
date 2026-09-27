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
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:stock_get_fundamentals (2330 PE 30.19/PB 9.57/DividendYield 1.1%);universe_get_sessions **150 sessions** 提供回測窗口;**atlas 無「加權計算」端點,需 client 端按 SK-17 公式 weight=1/N 或 MV_i/ΣMV_j 算**。[2026-09-27 更正:L3 實測 `stock_get_fundamentals` **不提供市值**(無 market_cap/shares_outstanding),原「提供市值」為誤記 ⇒ 本頁實際可跑者僅 equal weight 1/N。]
---

## 一句話定位
SK-17 在 atlas 是「組合內股票各放多少錢」——等權(1/N 散戶直覺)、價值加權(大股多吃),對應同一個選股名單會跑出完全不同的夏普。

## 論文版概念（忠實還原來源）
- **核心**:兩種加權方式
  - **equal**:每檔股票權重 `w_i = 1 / N`(簡單但忽略市值)
  - **value**:每檔股票權重 `w_i = MV_i / ΣMV_j`(市值佔比,大股多吃)
- **輸入**:stock_list、market_cap(dict)、method ∈ {'equal', 'value'}
- **輸出**:權重 dict
- **文獻口徑**:文獻上口徑分歧：等權組合因小股曝險,毛報酬/Sharpe 通常較高；value-weighted 的優點是換手率低、可執行性高、容量大。淨成本後何者勝出取決於市場與期間 [2026-08-22 audit-fix 修正]

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| stock_list | universe / decile 名單 | `universe_get_sessions` |
| market_cap | **無對位欄位**（2026-09-27 實測） | 缺（`stock_get_fundamentals` 不回市值） |
| 組合回測 | backtest 序列 | `backtest_signals` |
| 效果對比 | risk metrics | `risk_get_metrics` |
| 換手率 | backtest 內含 | `backtest_signals` |

**差異點**:論文版假設已有 market_cap;**atlas 端無此欄位**(2026-09-27 實測,見下)⇒ 論文版 value-weighted 在 atlas 落地不了,只能 client 端自備市值輸入。

**2026-09-27 L3 實測（VERIFIED NEGATIVE;端點皆 GET,值取自當日 Mac Mini `127.0.0.1:18080`）**:
- `market_cap` **不存在**:`stock_get_fundamentals`(2330) 只回 `PE`/`PB`/`DividendYield`/`Sector`;`data_get_field_contract`（當日 2262 欄）`market_cap` **0 命中**、`shares_outstanding` **0 命中** ⇒ 連 `shares_outstanding × close` 備援路徑也不成立 ⇒ **value-weighted 在 atlas 端算不出來**。
- `min_var` / `max_div`:atlas 源碼 (`~/workspace/atlas`) **0 命中**;`risk_parity` 只存在於 `internal/strategy/allocator.go`（策略層權重,非個股加權）⇒ 三變體在 atlas 皆無可驗證實作。
- 無任何「組合加權 / 權重方法選擇器」端點（`optimizer.*` 有參數,但無 weight-method selector）。
- **散戶實務解**:小資金 5 檔 → **等權(1/N)**;min_var / risk_parity 需共變異數與市值,atlas 兩者都不給。

**沒有對位的部分**:
- 沒有「組合加權」單一 endpoint(需 client 端組裝)
- 沒有「換手率」單獨 endpoint(在 backtest 序列內)
- 沒有「最小交易單位」約束(台股 1 張 = 1000 股,等權算下來可能買不到 1 張)

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「分 5 檔股票,各放多少錢?」 → 最直覺是「各 20%」,但文獻結論分歧(見論文版概念)。
- **R 段**:對位 atlas → 「用 `universe_get_sessions` 取一份多空名單 → client 端算權重 → `backtest_signals` 回測 → `risk_get_metrics` 看效果」。
- **+E 段**:警示「**散戶用 value-weighted 反而吃虧**,因為小資金買大股只能買零股、買小股又超限;**台股 1 張 = 1000 股的最小交易單位讓等權在小組合下更實用**」。**散戶最常誤信學術結論直接套到自己帳上**。
- 對位 ATLAS_METHODOLOGY 七時期:value-weighted 在高原期/盤整期表現穩定,在轉折期(向上或向下)落後等權——**因為大股帶動轉折的時滯較長**。

## 驗證方式
Step 1: 呼叫 `universe_get_sessions` 取一份 10 檔多頭名單。**2026-09-27 L3 實測:`stock_get_fundamentals` 無 `market_cap`,`shares_outstanding` 於 field contract 亦 0 命中** ⇒ value-weighted 無法在本 repo 組裝;本頁可實跑的只有 equal weight。
Step 2: client 端算等權權重 dict(1/N),餵進 `backtest_signals` 跑回測;value-weighted 需自備外部市值資料(2026-09-27 實測 atlas 無欄位)。
Step 3: 呼叫 `risk_get_metrics` 對比回測的 Sharpe / max_drawdown,不預設勝負（主流文獻多為等權毛 Sharpe 較高、value-weighted 換手低/容量大;原「預期 Sharpe 高 0.1-0.3」與文獻相反,2026-08-22 修正 [2026-08-22 驗證]）。

## 未消化 / 待補
- [ ] 「台股 1 張 = 1000 股」最小交易單位約束在 atlas 回測中是否處理?若否,equal weight 的「理論等權」與「實際可執行權重」會有顯著差距。

- [ ] 與 SK-20 規模分組的關係:value-weighted 偏向大股,SK-20 規模分組驗證策略在大股/小股分組下是否穩健,兩者應一併驗證。

> **2026-09-27 結案（移出本段,結論併入 §atlas 對位）**:原兩條未消化 ①「`stock_get_fundamentals` 是否含 `market_cap`」→ 實測 **NO**（欄位不存在）;②「`min_var`/`max_div`/`risk_parity` 變體」→ 實測 **atlas 端三者皆無可驗證實作**（risk_parity 僅策略層）。兩者皆屬**已驗證的否定**,非待辦。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:加權方式需對位 7 時期 × 策略三分類,等權 vs 價值加權跨 regime 表現)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)