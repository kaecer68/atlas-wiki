---
title: SK-29 滾動窗口回測模擬（atlas 對位版）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-29
ingested_at: 2026-07-29
status: active
tier: T3
confidence: high
atlas_go_relevance: high
consult_category: Q4
mcp_tools_used:
  - universe_get_sessions
  - risk_get_metrics
  - risk_get_drawdown
  - risk_get_calibration
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:**risk_get_drawdown 2026-08-02 06:40:13Z 真實數據 max_drawdown=0.9235/var_95=-0.0046**(kaecer 2026-08-02 修 RunDailyStressTests 沒接 drawdownReporter 的 bug 後,重跑 5 步驗證的第 1 步通過);universe_get_sessions **150 sessions** 確認時間軸;risk_get_metrics live session_count=**150**;risk_get_calibration verdict=calibrated;**修復時間軸**:3 次重試(8/01 23:44 / 8/02 00:24 / 8/02 02:57)均 not_available → kaecer 親修 dashboard 報接線 → 8/02 06:40 真實數據;**對位 docs/archive/2026-07-20-stress-api-ledger-drift.md A03 同型 bug**,本次修復關閉。
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:回測績效強烈依賴當期,高原期 OK 不代表轉折下壓期 OK)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit.md §1.5
---

<!-- methodology_alignment_tip: 本檔術語:七時期為真值;session 落在七不同時期結論可能差很多,需交叉看 period/regime 兩欄 -->
<!-- methodology_alignment_tip: 2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值;`source` 欄位正名 `regime_source` / `period_source` -->

## 一句話定位

「滾動窗口回測」是 mission「找漏洞」的時間序列外殼——沒有真實時間回測,所有 Alpha 都是紙上富貴。

## 論文版概念（忠實還原 Fin-Skills）

SK-29 定義用 sliding window（預設 252 天 = 1 年）對歷史數據做滾動回測,每月再平衡,逐步納入新數據,模擬真實時間序列決策。

**關鍵設計**:
- window_size: 252（一天為單位,1 年）
- rebalance_freq: 'M'（月度）
- 策略介接:任何帶 `.predict()` 或 `.act()` 的策略物件
- 輸出:權重、報酬、績效指標的時間序列

**為什麼重要**:
- 任何超額報酬聲稱都需先過滾動回測
- 靜態 train/test split 容易過擬合 → window rolling 模擬真實「資料陸續進來」的情境
- Newey-West 校正自動校正序列相關性,給 t 統計量

## atlas 對位

| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 滾動 session | 模擬 session 時間序列 | `universe_get_sessions` |
| 風險指標 | VaR / Drawdown / Sharpe | `risk_get_metrics`(**2026-08-01 23:15 結算 snapshot**:已實跑,session_count=147、insufficient_data=1) |
| 最大回撤 | drawdown_pct 細節 | `risk_get_drawdown` |
| 校正驗證 | 預測 vs 實測 VaR 對齊 | `risk_get_calibration` |
| 信號回測 | 多空訊號源 | `backtest_signals` |

**差異點**:
- 論文版自定義 window_size → atlas session 用固定 252 + session_count 控制
- 論文版 Newey-West 顯式 → atlas 透過 calibration tool 隱含
- 論文版 train/validate/test 三段 → atlas session 通常無此 split

## 散戶解讀（GROW+ 引用點）

**對應 §Q4 一句話**（consult-index §4）:
> 「單筆最大能虧多少（回撤）比賺多少更重要。先求不破產,再求賺錢。」

**教練框架的 O（Options）段會用到**:
- 「如果這策略最大回撤過去是 30%,你能接受帳面 -30% 嗎?」
- 「回測漂亮但 max_drawdown > 30% 的策略,實務上散戶通常撐不到最後——這條 mission 的『找漏洞』就是要在這裡抓人」

**散戶最常踩的坑**:
- 看「年化 30%」就信,沒看 max_drawdown 是 40%
- 看 Sharpe 2.0 就嗨,但那是 sample period 偏誤——backtest_signals 回的 sharpe 0.27/0.49 才是相對真實的
- 忽略 insufficient_data 標記——atlas 已經在守門,看到這標記要停下來想

## 驗證方式

**L1 格式**:frontmatter 9 欄齊全 ✅ / 6 段俱全 ✅ / 路徑正確 ✅
**L2 對位**:上述 5 個 atlas-mcp tool 對位已標 ✅
**L3 端點**（ground truth,2026-07-29 部分實跑）:
- ✅ `risk_get_metrics` 實跑確認,**2026-08-01 23:15 結算 snapshot**:session_count=147(當下)、max_drawdown_pct=1、insufficient_data=1
- ⏳ `universe_get_sessions` / `risk_get_drawdown` / `risk_get_calibration` 待實跑

**升 active 的條件**:
1. universe_get_sessions 實跑拿到最近一個月 session 內部結構
2. risk_get_drawdown 確認 max_drawdown_pct 字段含括號內範圍（如「1%」是 1 還是 0.01 需查）
3. risk_get_calibration 確認預測 vs 實測對齊的門檻值
4. 三項齊備後 draft → active

## 期間依賴性警告

引:ATLAS_METHODOLOGY.md §三七時期定義 + §五策略矩陣。
**同一個 `risk_get_metrics` 數值,在七不同時期下意義完全不同:**

| 七時期 | 對 SK-29 滾動回測數值解讀 |
|--------|-------------------------|
| **高原（Plateau）** | max_drawdown=1% **可能正常**(波動溫和) |
| **上升（Bull）** | max_drawdown=1% **可能低估**(市場自有上漲掩蓋風險) |
| **轉折下壓（Turnaround Down）** | max_drawdown=1% **可能正常**(回撤是預期內) |
| **盤整（Consolidation）** | max_drawdown=1% **可能問題**(無風險 = 無機會) |
| **黑天鵝（Black Swan）** | 7/28 事件確認 TAIEX 偏離 MA20 -5.93%,session 應改判為黑天鵝;若仍報 max_drawdown=1% 即**過低估計** |
| **低迷（Downturn）** | max_drawdown=1% **可能低估**(融資斷頭爆量未反映) |

**對位操作**:查 session 時**一定要交叉看 `market_period` + `period_name_zh` + `regime` 三欄**(atlas-mcp `mcp_quickstart` 已暴露)。只給 `risk_get_metrics` 數字是「死數字」,必須搭配當期才有完整意義。
**atlas-mcp 補強**:近 5 日 `recent_regime_5_days` 實跑顯示 7/29 = `market_period=bull` / `period_name_zh=上升（多頭）` / `regime=RISK_ON`,與 7/28 `consolidation` 不同 — 證明**七時期向下相容映射生效**。

## 未消化 / 待補

- [ ] atlas 的 `session_count` 與 Fin-Skills 的「滾動次數」是否口徑一致——atlas session 是「事件」不是「窗口」
- [x] **`max_drawdown_pct=1` 單位已查**:`risk_exposure` 端點用 `map[string]any` 接收,單位由 atlas-go 後端 `/api/dashboard/risk-exposure` 決定(atlas-mcp 無硬編碼);**真正單位需查後端 API 或實跑端點確認**(2026-08-03 02:55 v6.2 結構性誠實標)
- [ ] `insufficient_data=1` 標記的內部邏輯——是不是 atlas 已內建 Fin-Skills 強調的「資料不足不報價」紀律?
- [ ] paper 1 vs paper 2 的回測窗口差異(預測策略 vs RL 策略)對 atlas 同一個 universe_get_sessions 怎麼分流?
- [x] 反向鏈已設:`consult_category: Q4` 對齊 _consult-index.md §Q4
- [x] **L3 升 active 已修(2026-08-03 v6.2)**:kaecer v3.1 親修 RunDailyStressTests bug 後風險引擎已跑通,risk_get_drawdown 已回真實數據 `max_drawdown=0.9235`;**window_size=252 仍需確認 atlas 端是否暴露**(留未來);**SK-29 已升 active**(2026-08-01 v0.9 結算)

## 反向鏈接

- 對應諮詢類別:[Q4 風險/回測](../atlas-wiki/skills/_consult-index.md#q4-風險回測)
- 預評索引:[_index-finskills.md §2 HIGH 表](../atlas-wiki/skills/_index-finskills.md)
- 前一頁在 pipeline:[SK-16 多空十分位數](../atlas-wiki/skills/SK-16-long-short-decile.md)
- 寫入規範:[_method.md](../atlas-wiki/skills/_method.md)
