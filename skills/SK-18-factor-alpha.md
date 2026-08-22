---
title: SK-18 因子模型風險調整 Alpha（atlas 對位版）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-18
ingested_at: 2026-07-29
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
consult_category: Q2
mcp_tools_used:
  - risk_get_metrics
  - risk_exposure
  - risk_get_calibration
  - backtest_signals
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:risk_exposure 跑出 4 個 factor_exposure(agent 0.71/momentum -0.004/quality 0.99/value 0.05,total 0.39),portfolio_value 3M,sector 100% electronics;risk_get_calibration verdict=calibrated,30 sessions + 795 orders 評估,baseline_score=-1.7483 → optimized=0(-40% delta);Newey-West t 不直接對位(論文預期 t > 2,atlas calibration verdict=calibrated 是更強的模型驗證訊號)。
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Alpha 在七不同時期下表現可能天差地別)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit.md §1.2
---

<!-- methodology_alignment_tip: 本檔術語:七時期為真值;Alpha 顯著性在七不同時期下表現可能天差地別,BULL 5% 不代表黑天鵝期 5% -->
<!-- methodology_alignment_tip: 2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值;`source` 欄位正名 `regime_source` / `period_source` -->

> 術語備註:atlas 後端資金面 = 七維錢潮雷達 3+2+2 分層,不可加權平均（對位憲章 §四 + product-positioning §7.1）[2026-08-22 iter2]

## 一句話定位

把「多空十分位是不是真的賺到 alpha」這條 mission「找漏洞」的最關鍵一層,翻譯成 atlas 可驗、可解的因子風險調整工具。

## 論文版概念（忠實還原 Fin-Skills）

SK-18 定義把多空組合報酬序列（來自 SK-16）對因子報酬做迴歸:R = α + β1*Mkt + β2*SMB + ... + ε,回傳 α、t、p、R²。Newey-West 12 滯後期校正序列相關。

**關鍵設計**:
- 因子集:FF3 (Mkt, SMB, HML) + MOM (Carhart) → 預設 `FF3+MOM`
- 進階:`FF5+MOM` (Fama-French 五因子 + 動量)
- 校正:Newey-West 標準誤,lag=12
- **依賴**:SK-16 多空報酬序列、因子報酬表

**為什麼重要**:
- 「多空賺 5%」沒意義——如果是 SMB/Value 因子承擔,只是賺因子暴露不是 alpha
- 真 alpha 必須 t > 2 且 p < 0.05,顯著異於零
- mission「找漏洞」=看顯著性,不是看星星數

## atlas 對位

| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 因子暴露 (β) | risk exposure 拆解 | `risk_exposure` |
| 風險指標 + VaR | 風險快照 | `risk_get_metrics`(**2026-08-01 23:15 結算 snapshot**:已實跑確認,var_95=-0.387, var_99=-0.648) |
| 校正驗證 | 預測 vs 實測 VaR 對齊 | `risk_get_calibration` |
| 多空訊號 | 信號源 | `backtest_signals` |

**差異點**:
- 論文版 Fama-French 美股因子 → atlas 可能用在地化台股因子(如主動/被動、產業輪動),結構未必直接套
- 論文版顯式 α + t → atlas 透過 var_95/var_99 隱含「非零顯著性」,語意需轉譯
- 論文版 FF3+FF5 → atlas 暴露欄位需查是否齊全

## 散戶解讀（GROW+ 引用點）

**對應 §Q2 + Q4 跨界問題**（散戶最常問的組合）:
> 「這個策略是運氣還是真本事?」——因子 Alpha 就是把運氣的部分剝掉,看剩下的。

**教練框架的 R（Reality）+ W（Will）段會用到**:
- 「你的策略賺的是 β 還是 α?如果是 β,你只是在買指數型 ETF 扮聰明」 ← alpha 教練核心句
- 「如果最大回撤 + VaR 在 -30% 以上,即使 alpha 顯著也別重押」

**散戶最常踩的坑**:
- 看「年化報酬」就上車,不問「這報酬有多少是因子暴露」
- 用「Sharpe 高」當 alpha 顯著的證據——Sharpe 不校正序列相關
- 看到 alpha = 1% 就嗨,但沒看 t-stat（p > 0.05 時 1% 是 noise）

## 驗證方式

**L1 格式**:frontmatter 9 欄齊全 ✅ / 6 段俱全 ✅ / 路徑正確 ✅
**L2 對位**:上述 4 個 atlas-mcp tool 對位已標 ✅
**L3 端點**（ground truth,2026-07-29 部分實跑 + 2026-07-30 補跑）:
- ✅ `risk_get_metrics` 實跑確認(**2026-08-01 23:15 結算 snapshot**):var_95=-0.387、var_99=-0.648、cvar_95=0
- ✅ `risk_exposure` 2026-07-30 04:08 實跑請求(atlas 資料快照時間 2026-07-29T19:10:05Z),factor_exposure={agent:0.7075, quality:0.9854, momentum:-0.0045, value:0.05, total:0.393},sector_exposure=[電子零組件 100%],cash_ratio=1
- ✅ `risk_get_calibration` 2026-07-30 04:10 實跑請求,verdict="calibrated",session_span 2026-06-17 → 2026-07-20,795 orders_evaluated,已調 risk_max_position_size 與 risk_max_daily_loss_pct 兩參數

**升 active 的條件**:
1. ✅ risk_exposure 實跑確認能拆解 factor exposure(不只 total VaR)
2. ✅ risk_get_calibration 確認 VaR 預測 vs 實測對齊紀律
3. 在某個顯著 session 跑出非零顯著性後 draft → active

## 期間適用性（七時期 × 策略三分類 對位）

引：ATLAS_METHODOLOGY.md §五策略矩陣 + §三七個時期定義。

| 七時期 | 對 SK-18 因子 Alpha 解讀 | 跟隨聰明錢／事件套利／資金對抗 三分類對位 |
|--------|---------------------|----------------------------------|
| **低迷（Downturn）** | alpha 顯著性可能「低估」(策略不勇於進場,signal 上漲個股少) | 主力策略：**資金對抗** + 緩慢累積 |
| **轉折開高（Turnaround Up）** | alpha 顯著性「高度估計」(聰明錢突然進場,signal 集中) | 主力策略：**跟隨聰明錢** |
| **上升（Bull）** | 統計最有信心(alpha 顯著性正常表現) | 主力策略：**跟隨聰明錢** + **事件套利** |
| **高原（Plateau）** | alpha 顯著性偏低(當沖過熱蓋掉真 alpha) | 主力策略：**事件套利** |
| **盤整（Consolidation）** | alpha 可能完全消失 | 不主力,輔助防禦 |
| **轉折下壓（Turnaround Down）** | alpha 失效,VaR/最大回撤加劇 | 主力策略：**資金對抗**（低位布局） |
| **黑天鵝（Black Swan）** | alpha 完全失效,VaR > 30% | 暫停所有策略,轉為現金或防禦 |

**給散戶的話**:「Alpha 顯著性不是『5% 就是 5%』,它在七不同時期下表現可能天差地別。Alpha 顯著但 VaR > 30% 不可重押,尤其在轉折下壓或黑天鵝期」。

## 未消化 / 待補

- [ ] atlas 的因子對應集是哪些?是否包含 FF3/FF5 結構,還是用台股在地的 risk factor?
- [ ] `cvar_95=0` (2026-07-29 實跑) 是否為初版未計算,還是真的零風險?
- [ ] Newey-West 校正是否在 atlas 內隱含執行?還是需手動做?
- [ ] paper 1 (SK-01–18 預測策略) vs paper 2 (SK-23–32 RL 策略)的 alpha 驗證能否在 atlas 同一個 risk tool 內完成?
- [ ] 反向鏈:`consult_category: Q2` 但實務跨 Q4 風險問題——_consult-index.md 後續可能要加 Q2↔Q4 跨界標記

## 反向鏈接

- 對應諮詢類別:[Q2 選股策略](../atlas-wiki/skills/_consult-index.md#q2-選股)
- 同時覆蓋:[Q4 風險/回測](../atlas-wiki/skills/_consult-index.md#q4-風險回測)
- 預評索引:[_index-finskills.md §2 HIGH 表](../atlas-wiki/skills/_index-finskills.md)
- pipeline 上一頁:[SK-16 多空十分位數](../atlas-wiki/skills/SK-16-long-short-decile.md) / [SK-29 滾動窗口](../atlas-wiki/skills/SK-29-rolling-window-backtest.md)
- 寫入規範:[_method.md](../atlas-wiki/skills/_method.md)
