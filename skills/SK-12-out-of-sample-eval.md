---
title: SK-12 樣本外評估（R² / 夏普 / 累積報酬）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-12
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics, risk_get_drawdown, risk_get_correlation_matrix]
verification: "2026-09-27 L3 端點實跑（明細見 §驗證方式）:7 個端點群中 5 個 200、2 個非 200。**更正 #1:`risk_get_metrics` 不提供 sharpe**——`/api/dashboard/risk` 只有 6 個 key;IS/OOS 唯一出口是 `/api/dashboard/agent-observatory`,今日 5 張 scorecard **全部 `overfit_warning=true`**（etf-rotation-01 IS +0.0717／OOS −1.3685）。**更正 #2:OOS R² 有原生實作但只在 judge 路徑**——`internal/experiment/judge.go` 用 `eval.OOSR2` 產出 `eval_metrics.r2_oos`,且 `eval.SharpeRatio(..., 0)` **rf 硬編 0**;今日 experiment 端點無實例可取。**更正 #3:端點 sharpe 未年化**（`FrequencyPerOutcome` 無乘數）。今日快照:risk session_count **210**、`var_95` 0 且 `insufficient_data` 1（=資料不足,非零風險）。歷史:2026-08-01 v0.9 結算升 active（sharpe_long 0.27／sharpe_short 0.49／session_count 147;當日快照;sharpe 來源已更正）。"
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b3）
l3_endpoints_probed:
  - "/api/dashboard/risk → 200（無 sharpe 欄位;var_95 0＋insufficient_data 1）（2026-09-27T20:12:12+08:00）"
  - "/api/dashboard/agent-observatory → 200（5 scorecard 全 overfit_warning true;含 is_sharpe／oos_sharpe／is_oos_ratio／regime_breakdown）（2026-09-27T20:12:12+08:00）"
  - "/api/dashboard/drawdown → 200（max_drawdown 0.9229;var_95 −0.004816）（2026-09-27T20:12:13+08:00）"
  - "/api/backtest/signals → 200（active_signals null;sharpe_short／long 皆 0）（2026-09-27T20:12:12+08:00）"
  - "/api/dashboard/correlation-matrix → 200（20 個策略／類股標的）（2026-09-27T20:12:13+08:00）"
  - "/api/experiment/history → 200（空）;diff 缺 id／不存在 id → 400／404（2026-09-27T20:12:13+08:00）"
  - 源碼代理（無 HTTP 端點）＝ internal/eval/metrics.go ＋ judge 的 eval_metrics;`go test ./internal/eval/` → 22 PASS／0 FAIL（2026-09-27T20:12:14+08:00）
---

## 一句話定位
SK-12 在 atlas 是「策略對不對得起來」的官方裁判——同時算「模型準不準」(R²_oos)跟「投資賺不賺」(Sharpe/累積報酬/回撤),讓散戶看到 alpha 跟實際可賺的錢不是同一回事。

## 論文版概念（忠實還原來源）
- **核心**:同時輸出模型擬合指標 + 投資績效指標
- **公式**:
  - `R²_oos = 1 - Σ(y - ŷ)² / Σy²`(樣本外決定係數;不是訓練 R²;**分母 Σy² 為 uncentered 變體(非 Σ(y-ȳ)²),兩者數值不同 [2026-08-22 驗證]**)
  - `cumulative_return = ∏(1 + r_t) - 1`
  - `sharpe_ratio = mean(r_t - r_f) / std(r_t) × √12`(年化)
  - `max_drawdown = max peak-to-trough decline`
- **輸入**:y_true、y_pred、可選 portfolio_returns、可選 risk_free_rate
- **輸出**:`{R2_oos, cumulative_return, sharpe_ratio, max_drawdown}`
- **關鍵區別**:R²_oos 衡量「預測誤差」,Sharpe 衡量「投資獲利」——**R² 高不代表 Sharpe 高**(散戶最常誤解)

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| R²_oos(預測準度) | 端點面缺;**repo 有原生 `eval.OOSR2`**,由 judge 產出 `eval_metrics.r2_oos`（2026-09-27 實證） | 缺(client)／judge 內部 |
| sharpe_ratio | **更正（2026-09-27）:`risk_get_metrics` 沒有 sharpe**;唯一出口 = agent-observatory 的 `sharpe`／`is_sharpe`／`oos_sharpe`（未年化） | `trace_get_agent_observatory` |
| max_drawdown | drawdown 序列提供（2026-09-27 實測 0.9229） | `risk_get_drawdown` |
| cumulative_return | 端點缺;原生 `eval.CumulativeReturn` 存在（judge 的 `eval_metrics.cum_return`） | 缺(client) |
| correlation 跨策略 | 跨策略相關矩陣（2026-09-27:20 個策略／類股標的） | `risk_get_correlation_matrix` |

**差異點**:論文版一次算完 4 個指標,atlas 版分散在多端點 + client 端計算（**設計取捨,不是 bug**）,使用者需自己組裝。

**沒有對位的部分**:
- **端點面**沒有「OOS R²」與「累積報酬」（原生 `eval.OOSR2`／`eval.CumulativeReturn` 只餵 judge,不經 HTTP）
- **端點面的 sharpe 未年化**（`FrequencyPerOutcome`）;年化只在 `eval.SharpeRatio`（√252）與 `shared.ComputeSharpe`（日頻 √252、台股 √243）

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「這個策略好不好?」 → 反問「你要『預測準不準』還是『賺不賺錢』?」兩者不是同一件事。
- **R 段**:對位 atlas → 「client 端算 R²_oos → `agent-observatory` 拿 Sharpe → `risk_get_drawdown` 拿 max DD → 擺在一起看」（2026-09-27 更正:`risk_get_metrics` 沒有 Sharpe）。
- **+E 段**:警示「R²_oos > 0 但 Sharpe < 0 的策略**比 R² 低但 Sharpe 高更常見**——前者過擬合、實盤失效。**散戶最常買到前者**」。
- 對位 ATLAS_METHODOLOGY 七時期:同一策略在 RISK_ON vs RISK_OFF 期間的 Sharpe 可能差 3 倍,**只算全期 Sharpe 是誤導**。

## 驗證方式
Step 1: 呼叫 `backtest_signals` 取一條 active signal 的 OOS 預測與實際報酬序列,確認樣本數 ≥ 60(5 年月度)。
Step 2: client 端算 `R²_oos = 1 - sum((y - ŷ)²) / sum(y²)`,再算 `cumulative_return = prod(1 + r) - 1`。
Step 3: 呼叫 `risk_get_metrics` 取 sharpe_ratio、volatility,呼叫 `risk_get_drawdown` 取 max_drawdown;四指標擺在一起 cross-check 是否有 R² > 0 但 Sharpe < 0 的警示訊號。
> ⚠️ **更正（2026-09-27）**:`risk_get_metrics` 不回 sharpe／volatility;IS/OOS 與 Sharpe 改走 `/api/dashboard/agent-observatory`,其 `overfit_warning` 即本 Step 的警示訊號。

### L3 端點實跑 + 源碼代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/dashboard/risk` | 200 | session_count **210**;keys 只有 6 個（**無 sharpe**）;`var_95` 0 且 `insufficient_data` 1 | 2026-09-27T20:12:12+08:00 |
| 2 | `/api/dashboard/agent-observatory` | 200 | **5 張 scorecard 全 `overfit_warning=true`**;etf-rotation-01 IS +0.0717／OOS −1.3685,financials-desk-01 IS +0.2491／OOS −2.4e15 | 2026-09-27T20:12:12+08:00 |
| 3 | `/api/dashboard/drawdown` | 200 | `max_drawdown` 0.9229;`var_95` −0.004816（**var_95 非 0 的出口在這一支**） | 2026-09-27T20:12:13+08:00 |
| 4 | `/api/backtest/signals` | 200 | `active_signals` null;`sharpe_short`／`sharpe_long` 皆 0 | 2026-09-27T20:12:12+08:00 |
| 5 | `/api/dashboard/correlation-matrix` | 200 | 20 個標的（`ai_supply_chain`／`consumer`…）→ 策略／類股層 | 2026-09-27T20:12:13+08:00 |
| 6 | `/api/experiment/history`／`diff` | 200／**400、404** | history 空;diff 缺 id 回 `experiment_id required`,不存在 id 回 404 | 2026-09-27T20:12:13+08:00 |
| 7 | 源碼代理（無 HTTP 端點）:`internal/eval/metrics.go`＋judge | exit 0 | `go test ./internal/eval/` → **22 PASS／0 FAIL**（含 OOSR2／SharpeRatio／CumulativeReturn／MaxDrawdown 測試） | 2026-09-27T20:12:14+08:00 |

- **更正（2026-09-27）**:第 1 列推翻「sharpe 由 risk metrics 提供」;第 2 列才是唯一 IS/OOS 出口,`overfit_warning` 判準 = `is_oos_ratio > 2.0` 或 `IS>0 且 OOS≤0`（`internal/ledger/ledger.go`;IS／OOS = 依時間排序前 80%／後 20%）。本頁 2026-08-01 舊數字為該日快照,不可與今日混用。
- **樣本警語**:financials-desk-01 的 OOS Sharpe −2.4e15 是**退化值**（分母趨近 0）,不可讀成「極差策略」;5 張的 `statistically_significant` 皆 false。


## 未消化 / 待補
- [ ] 與 SK-22 消去法的關係:R²_oos 與 Sharpe 哪個對「刪掉某因子」更敏感?需實測才能確認 atlas 端該用哪個做 ablation 判準。

> **2026-09-27 已解並移出本段（3 項）**:①`risk_get_metrics` 是否含 OOS R²?→ **否**,且連 Sharpe 都沒有（payload 只有 6 個 key）;OOS R² 原生只在 `eval.OOSR2`／judge。②是否暴露 risk-free 來源?→ `SharpeConfig.RiskFreeRate` 只是呼叫端參數、**未經端點暴露**,而 judge **硬編 0** ⇒ 「rf=0 在台股不適用」在 atlas 原生路徑**成立**。③sharpe 是否年化?→ **端點值未年化**（`FrequencyPerOutcome`）;年化版本在 `eval.SharpeRatio`（√252）與 `shared.ComputeSharpe`（日頻 √252、台股 √243）。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:OOS 樣本外評估需對位 7 時期切換的真實表現)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)