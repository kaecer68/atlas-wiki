---
title: SK-20 規模分組穩健性檢驗
description: "問「同一策略在大股與小股表現一樣嗎」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-20
ingested_at: 2026-07-30
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [industry_sector_lookup, stock_get_quote, stock_get_fundamentals]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active（快照）:industry_sector_lookup(2330→半導體 12 成分股,7/30)+ stock_get_quote(2330 2425,2026-08-01 23:42)+ stock_get_fundamentals(PE 30.19/PB 9.57,7/30);[2026-08-22:2425/PE30.19/PB9.57 皆 2026-07-30~08-01 快照,勿當現值]。[2026-09-27 batch#4:6 端點全 200;`industry_sector_list` **首次實跑 = 38 產業（20 個有代表成分股）**,非舊記的 18;**市值欄位仍 0 命中**（field contract 2262 欄,`market_cap`／`shares_outstanding` 皆 0）⇒ atlas 端**無法**做市值分組,原「用 PB 反推市值」為誤記;`/api/scheduler/status` 110 個 job **無月度規模重切**;atlas 唯一 market-cap 分段碼是 `detectMarketCapGaps` **空殼**（回空 slice）。見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b4）
l3_endpoints_probed:
  - /api/industry/sectors → 200 (2026-09-27T20:13:26+08:00)
  - /api/industry/sector-lookup?symbol=2330 → 200 (2026-09-27T20:13:26+08:00)
  - /api/stock/quote?symbol=2330 → 200 (2026-09-27T20:13:25+08:00)
  - /api/stock/fundamentals?symbol=2330 → 200 (2026-09-27T20:13:25+08:00)
  - /api/field-contract → 200 (2026-09-27T20:13:26+08:00)
  - /api/scheduler/status → 200 (2026-09-27T20:15:05+08:00)
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §四(七大資金勢力行為)+ §七(散戶可捕捉事件);對位需考慮「市值是 dimension 還是 behavior_proxy 層」(CF-INV-07 加權風險)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit.md §1.3
---

<!-- methodology_alignment_tip: 本檔術語:七時期為 PeriodDetector 真值;RISK_ON/OFF/NEUTRAL 為向下相容層 -->
<!-- methodology_alignment_tip: atlas 後端 38 產業映射(2026-09-27 實測)與公股資金 per-broker 對位,本文未交叉引用 -->

> 術語備註:atlas 資金面 = 七維錢潮雷達 3+2+2,不可加權平均（憲章 §四 + product-positioning §7.1）[2026-08-22 iter2]

## 一句話定位
SK-20 是「同一策略在大股 vs 小股上是否都賺錢」的對照實驗——在 atlas 用來挑出「只在某一邊有效」的偽因子。
> ⚠️ PB/PE 是價值因子,不能當規模代理——用估值切 Big/Small 會混淆規模效應與價值效應；正確做法是用市值本身分組 [待 atlas 暴露市值欄位] [2026-08-22 audit-fix]
> 口徑註：atlas live 為 **38 產業**（2026-09-27 實測 `/api/industry/sectors`,20 個有代表成分股）;本頁舊記的「18」為 stale,已更正;論文版為 47 產業分類口徑,不同來源勿混 [2026-08-22 audit-fix,2026-09-27 更正]

## 論文版概念(忠實還原來源)
- **核心動作**:每月按市值排序,將樣本切成 Big(大公司)與 Small(小公司)兩組,或切成 tercile 三分組
- **split_method**:`"median"`(預設,切兩半)或 `"tercile"`(切三等分)
- **對象**:一支已建好的策略函數(SK-16 多空十分位數最常見)
- **輸出**:兩組各自的累積報酬、夏普、Alpha 對比表
- **隱含假設**:穩健的因子應在兩個規模組都正貢獻;只在小股有效 = 可能是流動性溢償或仙股雜訊

## atlas 對位（產業 × 市值 雙軸）

引:ATLAS_METHODOLOGY.md §四 + §七維錢潮雷達 3+2+2。
**本節關鍵**:SK-20 不只切 Big/Small,需與產業映射互鎖。

| 論文概念 | atlas-mcp 對位 | tool_name | 憲章 |
|---------|---------------|-----------|------|
| 月度市值排序 | **無對位**（無 `market_cap`／`shares_outstanding`,2026-09-27 實測）⇒ PB 反推市值是**誤記** | 缺 | §四 |
| **產業歸屬(必加)** | `industry_sector_lookup` 取歸屬;**雙軸 = 產業(38) × 市值** 因市值軸缺 → 只能單軸 | `industry_sector_lookup` | §四 |
| 切 Big/Small、兩組各自做策略 | universe 清單 + `stock_get_quote` 近 60 日收盤自算夏普（規模軸目前不可切） | `industry_sector_list`／`stock_get_quote` | §七維 3+2+2 |
| 累積報酬／Alpha 對比 | 策略層夏普 + 校準檢查 | `risk_get_metrics`／`risk_get_calibration` | §五 |
| 結論「只在 Small 有效」 | 寫 `_inbox.md` 標 `[SUSPECTED — size-tilted]` | (寫檔) | — |

**為何必須雙軸**:atlas 後端 `SectorIndexReader` 與 `GovernmentBrokerAggregator` 都用**產業 × 規模**雙軸做 canonical mapping;原文只切市值 = 對位憲章 §四時漏接「內資抗衡」（轉折下壓期公股連買跨產業）。2026-09-27 實測:規模軸在 atlas 根本無資料（見 §驗證方式）。
**CF-INV-07 加權風險警示**:規模統計若跨產業混加,股數/百分比不同分母(同 CF-INV-07 規定);嚴禁不分類加權平均。

**差異點**:論文版有乾淨市值日資料;**atlas 連現值市值都沒有**（2026-09-27 實測 0 命中）⇒ 不是快照落差,是**完全無此資料**。

**沒有對位的部分**:月度 re-split — `/api/scheduler/status` 今日 110 個 job 無規模重切（2026-09-27 實測）;market-cap 分段碼只有 `detectMarketCapGaps` 空殼。

## 散戶解讀(GROW+ 引用點)
- **R 段(Reality)**:教練問「你這個策略最近 60 天在 2330 跟 6547 上表現一樣嗎?」→ 引出 SK-20 的「規模依賴」。
- **+E 段**:提醒「小股做不出來不代表策略失敗,可能只是流動性不夠吃;大股做不出來也不代表穩健,可能是因子在大股早被吃光。」
- **教練句**:**「規模分組穩健性不是確認你的策略多好,是確認它壞在哪一邊。」**

## 驗證方式
Step 1: `industry_sector_list`（`/api/industry/sectors`）取產業清單。**2026-09-27 首次實跑:38 產業,20 個有代表成分股。**
Step 2: ~~挑 3 個市值大股（以 PE/PB 中位以上為 proxy）~~ **此步在 atlas 不可行**:PE/PB 是估值不是規模代理,且 field contract 無 `market_cap`（2026-09-27 實測）⇒ 只能改用外部市值資料。
Step 3: 兩組各算近 60 日夏普(年化 std × √252),對比;若一邊 < 0.3 且另一邊 > 0.8,即代表「只在某規模有效」——**規模分組未落地前此步無從執行**。

### L3 端點實跑（2026-09-27,本 PR;每列附 http_code 與 UTC+0800 時戳）

| 端點（GET 127.0.0.1:18080） | http_code | 今日實測結果 | timestamp |
|---|---|---|---|
| `/api/industry/sectors` | 200 | **38 產業**,20 個有代表成分股（semiconductor→12 檔） | 2026-09-27T20:13:26+08:00 |
| `/api/industry/sector-lookup?symbol=2330` | 200 | found=true,sector=半導體/semiconductor,12 檔代表股 | 2026-09-27T20:13:26+08:00 |
| `/api/stock/quote?symbol=2330` | 200 | last=2475、volume=12989000（2026-08-01 快照為 2425） | 2026-09-27T20:13:25+08:00 |
| `/api/stock/fundamentals?symbol=2330` | 200 | 只有 PE 30.19／PB 9.57／DividendYield 1.1／Sector semiconductor;**無市值** | 2026-09-27T20:13:25+08:00 |
| `/api/field-contract` | 200 | 2262 欄;`market_cap` **0 命中**、`shares_outstanding` **0 命中** | 2026-09-27T20:13:26+08:00 |
| `/api/scheduler/status` | 200 | 110 個 job;**無月度規模重切**（僅 window_backtest 週頻） | 2026-09-27T20:15:05+08:00 |

**今日結論（皆 2026-09-27 實跑）**
1. **規模軸不可用（已驗證的否定）**:無 `market_cap`／`shares_outstanding`,`/api/parameters` 2465 鍵也無市值參數 ⇒ Big/Small 分組**無資料基礎**,須自備外部市值。
2. **唯一 market-cap 分段碼是 stub**:`internal/spawning/gap_detector.go` 的 `detectMarketCapGaps` 直接回空 slice ⇒ 非可用實作。
3. **雙軸降為單軸（更正）**:產業軸今日 38 組（20 組有成分股）,非舊記 18;選股軸是 sector→stock_symbols。

## 未消化 / 待補
- [ ] 論文 D1~D10 十分位結構未落地:三端點已跑通(2026-08-01),但 client 端市值分組與十分位重切仍待實作（2026-09-27 追加:市值欄位 0 命中 ⇒ 缺**資料**,不只缺 client 程式;回測前須接外部來源 TWSE／FinMind）
- [ ] 「tercile」三切分版未寫,理論上對應低/中/高 beta 分群,但需要先驗 median 版

> **2026-09-27 batch#4 結案（移出本段）**:①「與 SK-21 重複驗證?」→ 軸不同（SK-20 市值、SK-21 股價）:SK-20 在 atlas 無資料基礎、SK-21 股價軸可用 ⇒ 不重複,但 SK-20 現階段不可實作;②「`scheduler_get_status` 有 re-split hook?」→ 110 個 job 無規模重切 ⇒ **否定**。
