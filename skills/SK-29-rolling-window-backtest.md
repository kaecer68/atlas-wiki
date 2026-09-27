---
title: SK-29 滾動窗口回測模擬（atlas 對位版）
description: "問「單筆最大能虧多少、這個回測可不可信」時載入。"
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
verification: "歷史快照(2026-08-02 升 active)：drawdown max_drawdown=0.9235/var_95=-0.0046、sessions 150、session_count 150、verdict=calibrated(修復時間軸對位 docs/archive/2026-07-20-stress-api-ledger-drift.md A03 同型 bug)。**2026-09-27 L3**：sessions 90(只有 regime)、session_count 210、max_drawdown_pct 0.7220/insufficient_data 1、drawdown 0.9229/var_95 -0.0048158、verdict=stable、backtest_signals 全 0/null；三欄交叉只在 /api/regime/history。單位與閘門以源碼定案：drawdown=0–1 分數、insufficient_data=MinObservationsForVaR 252 樣本閘門、risk_get_metrics 無 Sharpe、window_size=252 不在回測路徑。見 §驗證方式。"
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b6）
l3_endpoints_probed:
  - "/api/dashboard/sessions → 200（90 筆,只有 regime 欄） (2026-09-27T20:33:10+08:00)"
  - "/api/dashboard/sessions/session-20260926-daily → 200 (2026-09-27T20:34:31+08:00)"
  - "/api/dashboard/risk → 200（session_count 210,無 Sharpe 欄位） (2026-09-27T20:33:10+08:00)"
  - "/api/dashboard/drawdown → 200（max_drawdown 0.9229） (2026-09-27T20:33:10+08:00)"
  - "/api/dashboard/risk-calibration → 200（verdict stable） (2026-09-27T20:33:10+08:00)"
  - "/api/backtest/signals → 200（active_signals null） (2026-09-27T20:33:10+08:00)"
  - "/api/regime/history?days=7 → 200（period/period_name_zh 唯一出口） (2026-09-27T20:34:31+08:00)"
  - "源碼 internal/backtest/rolling_split.go（stopYear=2020,窗粒度=年） (2026-09-27T20:35+08:00)"
  - "源碼 internal/risk/var_calculator.go（MinObservationsForVaR=252） (2026-09-27T20:35+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:回測績效強烈依賴當期,高原期 OK 不代表轉折下壓期 OK)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit.md §1.5
---

<!-- methodology_alignment_tip: 本檔術語:七時期為真值;session 落在七不同時期結論可能差很多,需交叉看 period/regime 兩欄 -->

## 一句話定位

「滾動窗口回測」是 mission「找漏洞」的時間序列外殼——沒有真實回測,Alpha 都是紙上富貴。

## 論文版概念（忠實還原 Fin-Skills）

sliding window(預設 252 天)、月度再平衡、逐步納入新數據,模擬「資料陸續進來」的時序決策;介接有 `.predict()`／`.act()` 的策略物件,輸出權重-報酬-指標時序。為何重要:超額報酬聲稱需先過滾動回測、靜態 split 易過擬合、Newey-West 校正序列相關並給 t 統計量。

## atlas 對位

| 論文概念 | atlas 對位 | tool_name |
|---------|---------------|-----------|
| 滾動 session | 每日模擬 session 序列(今日 90 筆滾動窗,**只有 `regime`**) | `universe_get_sessions` |
| 風險指標 | VaR / Drawdown(**無 Sharpe**) | `risk_get_metrics`、`risk_get_drawdown` |
| 最大回撤 | `max_drawdown` / `max_drawdown_pct`(0–1 分數) | `risk_get_drawdown`、`risk_get_metrics` |
| 校正驗證 | 預測 vs 實測對齊門檻(sanity floor) | `risk_get_calibration` |
| 信號回測 | 多空訊號源(今日 null) | `backtest_signals` |
| 時期／regime 交叉 | 三欄交叉的**唯一出口** | `/api/regime/history` |

**差異點**:論文版 window 以「日」計(252)→ atlas 滾動窗以**年**計(`-valid-years` 2／`-step-years` 1,且 `stopYear := 2020` 硬編);Newey-West 顯式 → atlas 走 calibration sanity floor;train/valid/test 三段 → atlas session 無此 split。

## 散戶解讀（GROW+ 引用點）

**對應 §Q4**:「單筆最大能虧多少(回撤)比賺多少更重要。先求不破產,再求賺錢。」O 段用回撤當門檻(「過去最大回撤 30%,帳面 -30% 撐得住嗎?」)。**常見坑**:看年化 30% 不看 max_drawdown;把 sample-period 偏誤當 Sharpe 2.0;忽略 `insufficient_data`(今日 209 筆 < 252 閘門 ⇒ VaR=0 是「資料不足」不是「零風險」)。

## 期間依賴性警告

引:ATLAS_METHODOLOGY.md §三+§五。同一回撤數字在七時期意義不同:高原／盤整「1% 可能正常」(盤整下無風險=無機會)、上升期可能**低估**、轉折下壓／低迷可能正常或低估(斷頭爆量未反映)、黑天鵝若仍報 1% 即**過低**。

**對位操作**:三欄交叉今日**不在** `universe_get_sessions`(見更正 4),須走 `/api/regime/history?days=7`(2026-09-27 實測)。只給 `risk_get_metrics` 數字是「死數字」。

## 驗證方式

**L1 格式** ✅ / **L2 對位** ✅(6 個 atlas 出口已標)/ **升 active 條件(4 項)**:2026-08-02、2026-09-27 兩批實跑結清。

### L3 端點實跑（2026-09-27,本 PR）

| 端點／命令 | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/dashboard/sessions` | 200 | **90** sessions(2026-06-25→2026-09-27 每日);每筆只有 `regime`,**無 `market_period`/`period_name_zh`**;regime 分佈 RISK_ON 49／RISK_OFF 40／NEUTRAL 1 | 2026-09-27T20:33:10+08:00 |
| `/api/dashboard/sessions/session-20260926-daily` | 200 | 150 KB;`summary.portfolio_value`=3,097,172.40、`position_count`=3、`order_count`=0(可逐 session 展開) | 2026-09-27T20:34:31+08:00 |
| `/api/dashboard/risk` | 200 | `session_count`=**210**、`max_drawdown_pct`=**0.7220**、`data_points`=209、`insufficient_data`=1、VaR/CVaR 全 0、keys 只有 `degraded/gate_mode/risk_snapshot/session_count/source/var_gate` | 2026-09-27T20:33:10+08:00 |
| `/api/dashboard/drawdown` | 200 | `max_drawdown`=**0.9229**、`var_95`=**-0.00481588029711588**(全站唯一非零 `var_95`) | 2026-09-27T20:33:10+08:00 |
| `/api/dashboard/risk-calibration` | 200 | `verdict`=**stable**(非 2026-08-02 的 calibrated)、`orders_evaluated`=2926、2 提案被 sanity floor 拒(`risk_max_position_size` floor 0.12／`risk_max_daily_loss_pct` floor 0.03) | 2026-09-27T20:33:10+08:00 |
| `/api/backtest/signals` | 200 | `active_signals`=null、`sharpe_short`/`sharpe_long`/`drawdown_pct` 全 0 ⇒ 報酬序列今日取不到 | 2026-09-27T20:33:10+08:00 |
| `/api/regime/history?days=7` | 200 | **三欄交叉唯一出口**:`regime`=RISK_ON + `period`/`market_period`=consolidation + `period_name_zh`=盤整 + `regime_source`/`period_source` | 2026-09-27T20:34:31+08:00 |
| 源碼 `internal/backtest/rolling_split.go` + `internal/risk/var_calculator.go` | — | 前者 `stopYear := 2020` 硬編、窗粒度=年、**無 252 日窗參數**;後者 `const MinObservationsForVaR = 252`,不足時 VaR/CVaR 歸 0 只留 drawdown | 2026-09-27T20:35+08:00 |

**更正（2026-09-27）**

1. **`max_drawdown_pct` 單位已定案**:`risk` 0.7220 與 `drawdown` 0.9229 **皆為 0–1 分數**(不是「1 = 1%」)。數字不同是**端點不同源**(前者 `ComputeRiskSnapshot` 吃 PG session summary,後者 `CalculateMaxDrawdown` 吃 portfolio 序列)⇒ 引用必須寫端點名。
2. **`insufficient_data` 邏輯已定案**:非模糊標記,而是 `MinObservationsForVaR=252` 硬閘門(源碼註記「never surface a provisional VaR value」)。`data_points`=209 < 252 ⇒ VaR=CVaR=0(2026-09-27T20:33:10+08:00);**此狀態下 `var_95=0` 不可當零風險**。
3. **`risk_get_metrics` 沒有 Sharpe**:原表此歸屬不成立;IS/OOS Sharpe 走 `/api/dashboard/agent-observatory`。
4. **三欄交叉不靠 `universe_get_sessions`**:`market_period`/`period_name_zh` 今日不在 sessions payload(2026-08 的 `recent_regime_5_days` 也不在),須走 `/api/regime/history`。
5. **`window_size=252` 不在回測路徑**:252 只作統計常數出現(最小 VaR 樣本、`/api/capital-flow/daily` 校準 `sample_count`、ff5 √252 年化)。

## 未消化 / 待補

- [ ] paper 1 vs paper 2 的回測窗口差異(預測策略 vs RL 策略)對 atlas 同一個 universe_get_sessions 怎麼分流?

> **2026-09-27 已解**:①`max_drawdown_pct` 單位=0–1 分數②`insufficient_data=1`=252 筆樣本閘門③`window_size=252` 未由 atlas 暴露(窗以年計)④`session_count` 口徑:atlas session 是**每交易日一筆事件**(今日 90 筆滾動窗),非重訓次數。

## 反向鏈接

- 對應諮詢類別:[Q4 風險/回測](../atlas-wiki/skills/_consult-index.md#q4-風險回測)
- 預評索引:[_index-finskills.md §2 HIGH 表](../atlas-wiki/skills/_index-finskills.md)
- 前一頁在 pipeline:[SK-16 多空十分位數](../atlas-wiki/skills/SK-16-long-short-decile.md)
- 寫入規範:[_method.md](../atlas-wiki/skills/_method.md)
