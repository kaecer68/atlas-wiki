---
title: SK-17 加權方式（等權/價值加權）
description: "問「名單分 5 檔、每檔各放多少錢」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-17
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, universe_get_sessions]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:stock_get_fundamentals (2330 PE 30.19/PB 9.57/DividendYield 1.1%);universe_get_sessions **150 sessions** 提供回測窗口;**atlas 無「加權計算」端點,需 client 端按 SK-17 公式 weight=1/N 或 MV_i/ΣMV_j 算**。[2026-09-27 更正:L3 實測 `stock_get_fundamentals` **不提供市值**(無 market_cap/shares_outstanding),原「提供市值」為誤記 ⇒ 本頁實際可跑者僅 equal weight 1/N。][2026-09-27 batch#4 複驗:7 端點全 200;`/api/field-contract` 2262 欄 `market_cap`/`shares_outstanding` 仍 0 命中;`/api/dashboard/sessions` 今日 **90 sessions**;權重欄位實測於 `risk_exposure`（concentration weight = market_value / portfolio_value,含現金分母）;`optimizer.min_trade_size=1`（股）＋源碼 Todo「Currently unused」⇒ **1 張=1000 股約束不在模擬路徑**。詳見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b4）
l3_endpoints_probed:
  - /api/stock/fundamentals?symbol=2330 → 200 (2026-09-27T20:13:25+08:00)
  - /api/dashboard/sessions → 200 (2026-09-27T20:13:25+08:00)
  - /api/dashboard/risk → 200 (2026-09-27T20:13:25+08:00)
  - /api/dashboard/risk-exposure → 200 (2026-09-27T20:13:25+08:00)
  - /api/backtest/signals → 200 (2026-09-27T20:13:25+08:00)
  - /api/field-contract → 200 (2026-09-27T20:13:26+08:00)
  - /api/parameters → 200 (2026-09-27T20:13:26+08:00)
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:加權方式需對位 7 時期 × 策略三分類,等權 vs 價值加權跨 regime 表現)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-17 在 atlas 是「組合內股票各放多少錢」——等權(1/N 散戶直覺)、價值加權(大股多吃),對應同一個選股名單會跑出完全不同的夏普。

## 論文版概念（忠實還原來源）
- **核心**:兩種加權方式
  - **equal**:每檔股票權重 `w_i = 1 / N`(簡單但忽略市值)
  - **value**:每檔股票權重 `w_i = MV_i / ΣMV_j`(市值佔比,大股多吃)
- **輸入**:stock_list、market_cap(dict)、method ∈ {'equal', 'value'}
- **輸出**:權重 dict
- **文獻口徑**:等權因小股曝險,毛報酬/Sharpe 通常較高;value-weighted 換手低、容量大。淨成本後何者勝出取決於市場與期間 [2026-08-22 audit-fix]

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| stock_list | universe / decile 名單 | `universe_get_sessions` |
| market_cap | **無對位欄位**（2026-09-27 實測） | 缺（`stock_get_fundamentals` 不回市值） |
| 組合回測 | backtest 序列 | `backtest_signals` |
| 效果對比 | risk metrics（**無權重欄位**） | `risk_get_metrics` |
| 權重欄位（唯一出權重處） | concentration weight | `risk_exposure`（2026-09-27 實測） |
| 換手率 | backtest 內含 | `backtest_signals` |

**差異點**:論文版假設已有 market_cap;**atlas 端無此欄位**(2026-09-27 實測)⇒ value-weighted 落地不了,需 client 端自備市值。

**2026-09-27 L3 實測（VERIFIED NEGATIVE;時戳見 §驗證方式）**:
- `market_cap` **不存在** ⇒ **value-weighted 在 atlas 端算不出來**（`stock_get_fundamentals` 只回 PE/PB/DividendYield/Sector;2262 欄 `market_cap`／`shares_outstanding` 0 命中）。
- `min_var`／`max_div`:atlas 源碼 **0 命中**;`risk_parity` 只存在於 `internal/strategy/allocator.go`（策略層）⇒ 三變體皆無可驗證實作。
- **散戶實務解**:小資金 5 檔 → **等權(1/N)**;min_var／risk_parity 需共變異數與市值,atlas 兩者都不給。

**沒有對位的部分**:組合加權單一 endpoint（需 client 端組裝）;換手率獨立欄位（backtest 序列內,今日不可得）;最小交易單位約束（2026-09-27 實測**未實作**,非僅未對位）;**權重欄位不在 `risk_get_metrics`,只在 `risk_exposure`**（2026-09-27 實測）。

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「分 5 檔股票,各放多少錢?」→ 直覺是「各 20%」,但文獻結論分歧。
- **R 段**:對位 atlas → 「用 `universe_get_sessions` 取一份多空名單 → client 端算權重 → `backtest_signals` 回測 → `risk_get_metrics` 看效果」。
- **+E 段**:警示「**散戶用 value-weighted 反而吃虧**,因為小資金買大股只能買零股、買小股又超限;**台股 1 張 = 1000 股的最小交易單位讓等權在小組合下更實用**」。**散戶常犯:直接套學術結論**。
- 對位 ATLAS_METHODOLOGY 七時期:value-weighted 在高原期/盤整期表現穩定,在轉折期(向上或向下)落後等權——**因為大股帶動轉折的時滯較長**。

## 驗證方式
Step 1: 呼叫 `universe_get_sessions` 取一份 10 檔多頭名單。**2026-09-27 L3 實測:`stock_get_fundamentals` 無 `market_cap`,`shares_outstanding` 於 field contract 亦 0 命中** ⇒ value-weighted 無法在本 repo 組裝;本頁可實跑的只有 equal weight(1/N)。
Step 2: client 端算等權權重 dict(1/N),餵進 `backtest_signals` 跑回測;value-weighted 需自備外部市值資料。
Step 3: 呼叫 `risk_get_metrics` 對比回測的 Sharpe / max_drawdown,不預設勝負（文獻:等權毛 Sharpe 較高、value-weighted 換手低/容量大;2026-08-22 修正）。

### L3 端點實跑（2026-09-27,本 PR;每列附 http_code 與 UTC+0800 時戳）

| 端點（GET 127.0.0.1:18080） | http_code | 今日實測結果 | timestamp |
|---|---|---|---|
| `/api/stock/fundamentals?symbol=2330` | 200 | `{"PE":30.19,"PB":9.57,"DividendYield":1.1,"Sector":"semiconductor"}`（無市值） | 2026-09-27T20:13:25+08:00 |
| `/api/dashboard/sessions` | 200 | **90 sessions**（最新 session-20260927-daily） | 2026-09-27T20:13:25+08:00 |
| `/api/dashboard/risk` | 200 | session_count=210、data_points=209、insufficient_data=1、var_95=0;**無權重欄位** | 2026-09-27T20:13:25+08:00 |
| `/api/dashboard/risk-exposure` | 200 | concentration weight 0.1618／0.1613／0.1540;cash_ratio 0.5228 | 2026-09-27T20:13:25+08:00 |
| `/api/backtest/signals` | 200 | active_signals=null、sharpe_long/short=0 ⇒ 今日無回測指標 | 2026-09-27T20:13:25+08:00 |
| `/api/field-contract` | 200 | 2262 欄;`market_cap`／`shares_outstanding` 各 0 命中 | 2026-09-27T20:13:26+08:00 |
| `/api/parameters` | 200 | `optimizer.min_trade_size=1`（股）;無 weight-method selector | 2026-09-27T20:13:26+08:00 |

**今日結論（皆 2026-09-27 實跑）**:

1. **權重口徑（回答 SK-16 未消化項）**:atlas 唯一出權重處 = `risk_exposure.concentration[].weight` = `market_value / portfolio_value`（**現金入分母**）:2609.TW 485190/2998211.71=0.16183、00713.TW 0.16134、2603.TW 0.15399,合計 0.4771 = 1 − cash_ratio 0.5228 ⇒ atlas 內部是**市值加權（含現金）**,非 `1/N` 等權;SK-17 公式只在 client 端成立。
2. **最小交易單位:未處理（已驗證的否定）**:`internal/tax/tax_aware_sizing.go` 有 `TaiwanLotSize=1000` 與向下取整,但 `NewTaxAwareSizer` 10 次出現**全在自身測試檔（生產呼叫者 0）**;live `optimizer.min_trade_size=1` 股,config Todo 明寫「Currently unused; implement minimum trade size」⇒ **模擬路徑不套 1 張約束**。
3. **value-weighted 仍不可組裝**:2262 欄 0 命中,`shares_outstanding × close` 亦不成立。

## 未消化 / 待補
- [ ] value-weighted 需**外部市值資料**:atlas 端 `market_cap`／`shares_outstanding` 2026-09-27 複驗仍 0 命中,替代路徑不成立;外部來源（TWSE／FinMind 等）尚未接入本頁流程。
- [ ] 換手率無獨立端點且今日不可得:`/api/backtest/signals` 200 但 active_signals=null、sharpe 全 0（2026-09-27）,換手率與效果對比須等回測序列恢復。

> **2026-09-27 batch#4 結案（移出本段）**:①「1 張 = 1000 股約束是否處理」→ **NO**（源碼有 lot 常數但 0 生產呼叫者;live `min_trade_size=1` 股且標 unused）,見 §驗證方式 第 2 點;②「與 SK-20 規模分組的關係」→ 同日兩頁皆實跑,value-weighted 與 SK-20 市值分組**共用同一 blocker**（atlas 無市值欄位）⇒ 現階段都不成立。
> **2026-09-27 結案（移出本段,結論併入 §atlas 對位）**:①「`stock_get_fundamentals` 是否含 `market_cap`」→ **NO**;②「`min_var`/`max_div`/`risk_parity` 變體」→ 實測三者皆無可驗證實作（risk_parity 僅策略層）。皆屬已驗證的否定,非待辦。
