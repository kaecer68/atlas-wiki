---
title: SK-18 因子模型風險調整 Alpha（atlas 對位版）
description: "問「這策略賺的是運氣還是真本事（α）」時載入。"
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
verification: 2026-08-01 v0.9 結算跑過 L3 升 active（快照）:risk_exposure 4 個 factor_exposure(agent 0.71/quality 0.99/momentum -0.004/value 0.05,total 0.393),sector 電子零組件 100%;risk_get_calibration verdict=calibrated、795 orders、baseline -1.7483 → optimized 0（原「-40% delta」錯誤,2026-08-22 修正）;Newey-West lag=12 對月頻偏高（慣例 lag≈floor(4×(T/100)^(2/9))）[2026-08-22 驗證]。[2026-09-27 batch#4 複驗:5 端點全 200;因子集今日實測**只有 momentum/value/quality/agent**（無 FF3/FF5）;`cvar_95=0` 成因 = `var_available:false`（非零風險）;calibration 今日 verdict=**stable**、2926 orders;`/api/dashboard/agent-observatory` 提供 t_stat／statistically_significant／is_sharpe／oos_sharpe（5 scorecards、0 顯著）;Newey-West 源碼 0 命中。見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b4）
l3_endpoints_probed:
  - /api/dashboard/risk → 200 (2026-09-27T20:13:25+08:00)
  - /api/dashboard/risk-exposure → 200 (2026-09-27T20:13:25+08:00)
  - /api/dashboard/risk-calibration → 200 (2026-09-27T20:13:25+08:00)
  - /api/dashboard/agent-observatory → 200 (2026-09-27T20:13:25+08:00)
  - /api/backtest/signals → 200 (2026-09-27T20:13:25+08:00)
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Alpha 在七不同時期下表現可能天差地別)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit.md §1.2
---

<!-- methodology_alignment_tip: 七時期為真值;Alpha 顯著性在七不同時期下可能天差地別,BULL 5% 不代表黑天鵝期 5% -->

> 術語備註:atlas 後端資金面 = 七維錢潮雷達 3+2+2 分層,不可加權平均（對位憲章 §四 + product-positioning §7.1）[2026-08-22 iter2]

## 一句話定位

把「多空十分位是不是真的賺到 alpha」這條 mission「找漏洞」的最關鍵一層,翻譯成 atlas 可驗可解的因子風險調整工具。

## 論文版概念（忠實還原 Fin-Skills）

SK-18 定義把多空組合報酬序列（來自 SK-16）對因子報酬做迴歸:R = α + β1*Mkt + β2*SMB + ... + ε,回傳 α、t、p、R²。Newey-West 12 滯後期校正序列相關。

**關鍵設計**:因子集 FF3 (Mkt, SMB, HML) + MOM (Carhart) → 預設 `FF3+MOM`,進階 `FF5+MOM`;校正 Newey-West 標準誤 lag=12;**依賴** SK-16 多空報酬序列 + 因子報酬表。

**為什麼重要**:「多空賺 5%」若是被 SMB/Value 因子承擔,就只是賺因子暴露不是 alpha;真 alpha 必須 t > 2 且 p < 0.05。「找漏洞」= 看顯著性,不是看星星數。

## atlas 對位

| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 因子暴露 (β) | risk exposure 拆解 | `risk_exposure` |
| 風險指標 + VaR | 風險快照（無權重、無 Sharpe） | `risk_get_metrics`（舊快照 var_95=-0.387／var_99=-0.648,2026-08-01） |
| 校正驗證 | 預測 vs 實測 VaR 對齊 | `risk_get_calibration` |
| 多空訊號 | 信號源 | `backtest_signals` |

**差異點**:論文版 FF 美股因子 → atlas 用自訂因子（momentum/value/quality/agent,2026-09-27 實測）,FF3/FF5 結構不存在;論文版顯式 α + t → atlas **也有** t_stat／statistically_significant,但在 `agent-observatory` 不在 risk 端（2026-09-27 更正）。

## 散戶解讀（GROW+ 引用點）

**對應 §Q2 + Q4 跨界問題**:「這個策略是運氣還是真本事?」——因子 Alpha 就是把運氣剝掉,看剩下的。

**R + W 段教練句**:
- 「你的策略賺的是 β 還是 α?如果是 β,你只是買了指數型 ETF 扮聰明」
- 「最大回撤 + VaR 在 -30% 以上,即使 alpha 顯著也別重押」

**散戶最常踩的坑**:看年化報酬就上車;用 Sharpe 當 alpha 顯著證據（它不校正序列相關）;看到 alpha 1% 就嗨但沒看 t-stat（p > 0.05 是 noise）。

## 驗證方式

**L1** ✅（frontmatter 10 欄／6 段）　**L2** ✅（4 個 atlas-mcp tool 已標）

**舊跑（快照 2026-07-29~08-01）**:var_95 -0.387／var_99 -0.648;factor_exposure={agent 0.7075, quality 0.9854, total 0.393};verdict="calibrated"、795 orders。

### L3 端點實跑（2026-09-27,本 PR;每列附 http_code 與 UTC+0800 時戳）

| 端點（GET 127.0.0.1:18080） | http_code | 今日實測結果 | timestamp |
|---|---|---|---|
| `/api/dashboard/risk` | 200 | session_count=210、insufficient_data=1、var_95=0;**無 Sharpe 欄位** | 2026-09-27T20:13:25+08:00 |
| `/api/dashboard/risk-exposure` | 200 | factor_exposure={momentum 0.160, value 0.05, quality 0.476, agent 0.608, total 0.295};sector 其他 100%;**var_available=false** | 2026-09-27T20:13:25+08:00 |
| `/api/dashboard/risk-calibration` | 200 | verdict=**stable**（非 calibrated）;orders 2926 | 2026-09-27T20:13:25+08:00 |
| `/api/dashboard/agent-observatory` | 200 | 5 scorecards（含 t_stat／is_sharpe／oos_sharpe／overfit_warning）;**0/5 顯著、5/5 overfit=true** | 2026-09-27T20:13:25+08:00 |
| `/api/backtest/signals` | 200 | active_signals=null、sharpe_long/short=0 ⇒ 今日無回測序列 | 2026-09-27T20:13:25+08:00 |

**今日結論（皆 2026-09-27 實跑）**
1. **顯著性與 IS/OOS 都在 agent-observatory**:今日 5 scorecard 有 t_stat／statistically_significant／is_sharpe／oos_sharpe;etf-rotation-01 is_sharpe=0.072 vs oos_sharpe=-1.369（is_oos_ratio 0.052）;energy-desk-01 t_stat=3.49 但 statistically_significant=false（口徑未定義,勿推論）⇒ 舊句「透過 var_95/99 隱含顯著性」**不成立**。
2. **`cvar_95=0` 成因（結案）**:risk-exposure 回 `var_available=false`、risk 端 `insufficient_data=1`（2026-09-27 實測）⇒ 0 = **未計算**,非零風險。
3. **因子集（結案）**:live 鍵 = momentum／value／quality／agent;config 另有 narrative 0.10／industry_cycle 0.10 ⇒ **自訂因子,不含 FF3/FF5 Mkt/SMB/HML**。
4. **Newey-West（否定）**:源碼（commit b5108fb）`newey` **0 命中** ⇒ 校正未內建,須 client 端自做。

## 期間適用性（七時期 × 策略三分類 對位）

引：ATLAS_METHODOLOGY.md §五、§三七時期。

| 七時期 | 對 SK-18 因子 Alpha 解讀 | 策略三分類對位 |
|--------|---------------------|------------------|
| **低迷 Downturn** | alpha 顯著性可能低估（策略不勇於進場） | **資金對抗** + 緩慢累積 |
| **轉折開高 Turnaround Up** | alpha 顯著性高度估計（聰明錢集中進場） | **跟隨聰明錢** |
| **上升 Bull** | 統計最有信心 | **跟隨聰明錢** + **事件套利** |
| **高原 Plateau** | alpha 顯著性偏低（當沖過熱蓋掉真 alpha） | **事件套利** |
| **盤整 Consolidation** | alpha 可能完全消失 | 不主力,輔助防禦 |
| **轉折下壓 Turnaround Down** | alpha 失效,VaR/最大回撤加劇 | **資金對抗**（低位布局） |
| **黑天鵝 Black Swan** | alpha 完全失效,VaR > 30% | 暫停策略,轉現金/防禦 |

**給散戶的話**:「Alpha 顯著性七時期下可能天差地別;顯著但 VaR > 30% 不可重押（轉折下壓/黑天鵝期尤甚）」。

## 未消化 / 待補

- [ ] paper 1（SK-01–18）vs paper 2（SK-23–32 RL）的 alpha 驗證能否在同一 risk tool 內完成?**部分已解（2026-09-27）**:agent-observatory 一個端點對所有 agent 打分;但 scorecard 只有 `skill`／`layer`,**無 paper 家族標記**,無法按 paper 分組。
- [ ] 升 active 條件 3「非零顯著性」**今日仍未達成**:agent-observatory 5/5 scorecard `statistically_significant=false`（2026-09-27）;本頁 active 是依條件 1/2 通過。

> **2026-09-27 batch#4 結案（移出本段）**:①「因子集是否含 FF3/FF5」→ **否**（live 鍵只有 momentum／value／quality／agent）;②「`cvar_95=0` 是未計算還是零風險」→ **未計算**（`var_available=false`）;③「Newey-West 是否內建」→ **未內建**（源碼 0 命中）;④「Q2↔Q4 跨界標記」→ **已在**（`_consult-index.md` 的 Q2 與 Q4 兩列同列 SK-18）。見 §驗證方式。

## 反向鏈接

- 諮詢類別:[Q2](../atlas-wiki/skills/_consult-index.md#q2-選股)／[Q4](../atlas-wiki/skills/_consult-index.md#q4-風險回測)（_consult-index 兩列同列本頁）
- pipeline:[SK-16 多空十分位](../atlas-wiki/skills/SK-16-long-short-decile.md) → [SK-29 滾動窗口](../atlas-wiki/skills/SK-29-rolling-window-backtest.md)
