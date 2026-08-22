---
title: SK-20 規模分組穩健性檢驗
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-20
ingested_at: 2026-07-30
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [industry_sector_lookup, stock_get_quote, stock_get_fundamentals]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:industry_sector_lookup(2330→半導體 12 成分股,7/30)+ stock_get_quote(2330 現價 2425,high 2425/low 2345,2026-08-01 23:42)+ stock_get_fundamentals(PE 30.19/PB 9.57/DividendYield 1.1%/sector=semiconductor,7/30)三端點全跑通;**atlas 端無直接「市值分組」端點,需 client 端用 stock_get_fundamentals 算市值後分組**(端點活≠論文 D1~D10 十分位結構)。
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §四(七大資金勢力行為)+ §七(散戶可捕捉事件);對位需考慮「市值是 dimension 還是 behavior_proxy 層」(CF-INV-07 加權風險)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit.md §1.3
---

<!-- methodology_alignment_tip: 本檔術語:七時期為 PeriodDetector 真值;RISK_ON/OFF/NEUTRAL 為向下相容層 -->
<!-- methodology_alignment_tip: atlas 後端有 8+18 產業映射(B5-3 PR-A/B)與公股資金 per-broker 對位,本文未交叉引用 -->
<!-- methodology_alignment_tip: 2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值;`source` 欄位正名 `regime_source` / `period_source` -->

> 術語備註:atlas 後端資金面 = 七維錢潮雷達 3+2+2 分層,不可加權平均（對位憲章 §四 + product-positioning §7.1）[2026-08-22 iter2]

## 一句話定位
SK-20 是「同一策略在大股 vs 小股上是否都賺錢」的對照實驗——在 atlas 用來挑出「只在某一邊有效」的偽因子。
> ⚠️ PB/PE 是價值因子,不能當規模代理——用估值切 Big/Small 會混淆規模效應與價值效應；正確做法是用市值本身分組 [待 atlas 暴露市值欄位] [2026-08-22 audit-fix]
> 口徑註：本頁 18 產業 vs SK-21/23 的 38 產業（atlas）與 47 產業（論文）是不同時點/分類口徑,引用時需註明 [2026-08-22 audit-fix]

## 論文版概念(忠實還原來源)
- **核心動作**:每月按市值排序,將樣本切成 Big(大公司)與 Small(小公司)兩組,或切成 tercile 三分組
- **split_method**:`"median"`(預設,切兩半)或 `"tercile"`(切三等分)
- **對象**:一支已建好的策略函數(SK-16 多空十分位數最常見)
- **輸出**:兩組各自的累積報酬、夏普、Alpha 對比表
- **隱含假設**:穩健的因子應在兩個規模組都正貢獻;只在小股有效 = 可能是流動性溢償或仙股雜訊

## atlas 對位（產業 × 市值 雙軸）

引:ATLAS_METHODOLOGY.md §四七大資金勢力行為 + §七維錢潮雷達 3+2+2(從「七大資金勢力」混稱正名)。
**本節關鍵**:SK-20 不只切 Big/Small,需與產業映射互鎖。

| 論文概念 | atlas-mcp 對位 | tool_name | 對位憲章 |
|---------|---------------|-----------|---------|
| 月度市值排序 | 單次取市值快照 → 用 `stock_get_fundamentals` 拿 PE/PB 後用 PB 估值反推市值分組 | `stock_get_fundamentals` | §七維錢潮雷達 3+2+2(市值是 dimension 還是 behavior_proxy 層需釐清) |
| **產業歸屬(必加)** | 用 `industry_sector_lookup` 取個股歸屬,**雙軸分組** = 產業(18) × 市值(Big/Small/tercile) = 54 組 | `industry_sector_lookup` | ATLAS_SYSTEM_STATE.md:192 B5-3 PR-A W4 `SectorIndexReader` 已建立 8/18 產業映射 |
| 切 Big/Small 兩組 | `industry_sector_list` 拿到 TWSE/TPEx 完整 universe,再用市值分位切 | `industry_sector_list` | §七維錢潮雷達 3+2+2 |
| 兩組獨立做策略 | 對每組 symbol list 跑 `stock_get_quote` 拿近 60 日收盤,自算夏普 | `stock_get_quote` | 同上 |
| 累積報酬 / Alpha 對比 | `risk_get_metrics` 拿到策略層級夏普,搭配 `risk_get_calibration` 看分組後是否仍校準 | `risk_get_metrics` | §五策略矩陣 |
| 結論「只在 Small 有效」 | 記進 `_inbox.md` 跨頁待辦,標 `[SUSPECTED — size-tilted]` | (寫檔,非 tool) | — |

**為何必須雙軸**:atlas 後端 `SectorIndexReader`(B5-3 PR-A) 與 `GovernmentBrokerAggregator` per-broker 對位都用了**產業 × 規模** 雙軸做 canonical mapping。原文只切市值未對位產業 = 對位憲章 §四時漏接「內資抗衡」風險(低迷/轉折下壓期公股連買是橫跨各產業的現象)。
**CF-INV-07 加權風險警示**:規模統計若跨產業混加,股數/百分比不同分母(同 CF-INV-07 規定);嚴禁不分類加權平均。

**差異點**:論文版假設有乾淨的市值日資料;atlas-mcp 沒有原生 time-series 市值端點,只能用 `stock_get_fundamentals` 現值快照 + `stock_get_quote` 歷史價反推。這是 atlas 的硬限制。

**沒有對位的部分**:論文的「monthly re-split」時間軸在 atlas 沒有對應的排程觸發器;若要走月度重切,需自建 cron 或等 `scheduler_get_status` 暴露 hook。

## 散戶解讀(GROW+ 引用點)
- **R 段(Reality)**:教練問「你這個策略最近 60 天在 2330 跟 6547 上表現一樣嗎?」——直接引到 SK-20 的「不是在說有效性,是在說規模依賴」。
- **+E 段**:提醒「小股做不出來不代表策略失敗,可能只是流動性不夠吃;大股做不出來也不代表穩健,可能是因子在大股早被吃光。」
- **教練句**:**「規模分組穩健性不是確認你的策略多好,是確認它壞在哪一邊。」**

## 驗證方式
Step 1: `mcp__atlas_mcp__industry_sector_list` 取得 universe 大致清單,記下前 20 個產業代號
Step 2: 從中挑 3 個市值大股(以 PE/PB 估值中位以上為 proxy)+ 3 個小股,跑 `stock_get_quote` 取近 60 日收盤
Step 3: 兩組各算一次近 60 日夏普(年化 std × √252),對比;若一邊 < 0.3 且另一邊 > 0.8,即代表「只在某規模有效」

**L3 端點實跑狀態(2026-07-30)**:
- ✅ `stock_get_fundamentals` 已對位(industry_sector_lookup 2330 → 半導體, 12 支代表股)
- ⏳ `industry_sector_list` / `stock_get_quote` 待實跑

## 未消化 / 待補
- [ ] L3 端點真跑:上面 Step 1~3 尚未執行(2026-07-30 仍 draft)
- [ ] atlas-mcp 沒有原生市值時序,只能用現值快照 + 價格反推,真實回測時務必補上
- [ ] 「tercile」三切分版未寫,理論上對應低/中/高 beta 分群,但需要先驗 median 版
- [ ] 與 SK-21(排除仙股)的關係:SK-20 切小股會自然帶到仙股,兩者是否重複驗證待釐清
- [ ] monthly re-split 排程 hook — atlas-mcp 是否會在 `scheduler_get_status` 暴露對應 API 待查
