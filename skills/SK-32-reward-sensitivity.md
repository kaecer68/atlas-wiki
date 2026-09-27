---
title: SK-32 獎勵函數敏感性分析
description: "問「哪個 reward 函數最賺、換 reward 值不值得」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-32
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics, experiment_diff]
verification: "歷史(2026-08-01 v0.9 升 active)：backtest_signals/risk_get_metrics 跑通；[2026-08-22 audit-fix] 原 400 為參數名誤判(id= 應為 experiment_id=)。**2026-09-27 L3 實跑**：backtest_signals 全 0/null、risk 無 Sharpe 欄位、experiment/history 為空 `[]`、experiment/diff 裸 GET 400／不存在 id 404(route 活著、資料 0 筆)、agent-observatory 5 scorecard **全部 `overfit_warning=true`／0 筆顯著**。4 種 reward 函數名在 atlas-go **0 命中**；最近的原生代理是 `internal/eval/mismatch.go` 的 `CheckSLRLAlignment`(0 生產呼叫者)與 `internal/config/inference.go` 的 `SweepParameter`(參數掃描,非 reward)。見 §驗證方式。"
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b6）
l3_endpoints_probed:
  - "/api/backtest/signals → 200（active_signals null） (2026-09-27T20:33:10+08:00)"
  - "/api/dashboard/risk → 200（無 Sharpe 欄位） (2026-09-27T20:33:10+08:00)"
  - "/api/dashboard/agent-observatory → 200（5 筆全部 overfit_warning） (2026-09-27T20:33:47+08:00)"
  - "/api/experiment/history → 200（history 空） (2026-09-27T20:33:47+08:00)"
  - "/api/experiment/diff → 400 experiment_id required (2026-09-27T20:34:20+08:00)"
  - "/api/experiment/diff?experiment_id=does-not-exist → 404（資源不存在） (2026-09-27T20:34:20+08:00)"
  - "源碼 internal/eval/mismatch.go + internal/config/inference.go（reward 函數名 0 命中） (2026-09-27T20:36+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Reward Sensitivity 敏感度需對位 regime 切換下的策略穩健性)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-32 把 SK-25 的 4 種 reward 函數變成「哪個最優」的可信結論——單獨看 SK-25 還不夠,**reward function 對結果的敏感度必須量化**,散戶才知道「換 reward 值不值得」。

## 論文版概念
- 對每個 reward_variant:複製環境(同隨機種子)→ 設新 reward 函數 → 訓練 PPO 100k steps → 回測算 eval_metric(預設 sharpe_ratio)。
- 彙整成 DataFrame:reward_variant → 評估指標,排序找最佳。

## atlas 對位
| 論文概念 | atlas 對位 |
|---------|---------------|
| 環境複製 | 完全 client 端 |
| PPO 訓練 | 缺(client 端 stable-baselines3;2026-09-27 源碼 `\bppo\b` 0 命中,見 SK-24) |
| 評估 | `backtest_signals`(今日全 0/null)＋ `risk_get_metrics`(**無 Sharpe**) |
| 跨 reward 對比 | `experiment_diff`(route 活著;`experiment/history` 今日 0 筆) |
| 唯一可用的評估面 | `/api/dashboard/agent-observatory`(`is_sharpe`/`oos_sharpe`/`t_stat`/`overfit_warning`) |

**差異點**:訓練全 client 端;atlas 提供「評估與對比」端點,但**今日對比路徑無資料**(0 筆 experiment),2026-08 的「atlas 端對位完整度高」評語已降級為「端點在、資料面 0 筆」。
**沒有對位的部分(2026-09-27 源碼複驗仍成立)**:無「自動化多 reward sweep」端點(`SweepParameter`/`RecommendFromSweep` 只存在於 `internal/config`,0 呼叫者、0 路由);無「hyperparameter 搜尋」端點;4 種 reward 函數名在 atlas-go 0 命中。

## 散戶解讀
- **G**:用戶問「哪個 reward 函數最賺?」 → 跑 SK-32 出敏感性表,論文答案是 continuous_rank,但散戶的台股資料上可能 top10_hit 反而好——一定要自己跑(今日 atlas 端無法代跑)。
- **+E**:**reward 函數是 RL 唯一的「可控設計選擇」**——架構、訓練步數、種子都不可控或成本高,唯獨 reward 可快速 A/B。散戶若只碰 RL 的一個東西,應該是 reward 函數。
- 對位 ATLAS_METHODOLOGY 七時期:regime 切換時最佳 reward 可能換——SK-32 需每期重跑。

## 驗證方式
Step 1: 用 SK-25 4 種 reward 各訓練 100k steps(client 端,固定隨機種子)。
Step 2: 對每個 agent 跑 `backtest_signals` 拿序列,call `risk_get_metrics` 拿 Sharpe / max_drawdown / 換手率。
Step 3: client 端彙整成 DataFrame,sort by sharpe_ratio desc,確認連續型 reward 在前 2 名(論文結論)。

### L3 端點實跑（2026-09-27,本 PR）

| 端點／命令 | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/backtest/signals` | 200 | `active_signals`=null、`sharpe_short`/`sharpe_long`/`drawdown_pct`/`var_95` 全 0 ⇒ Step 2 的序列**今日取不到** | 2026-09-27T20:33:10+08:00 |
| `/api/dashboard/risk` | 200 | **無 Sharpe 欄位**(keys `degraded/gate_mode/risk_snapshot/session_count/source/var_gate`);`session_count`=210、`insufficient_data`=1 | 2026-09-27T20:33:10+08:00 |
| `/api/dashboard/agent-observatory` | 200 | **5** scorecards,每筆有 `is_sharpe`(0.072～0.249)、`oos_sharpe`(負值,含哨兵 -2.4e15)、`is_oos_ratio`、`t_stat`、`overfit_warning`;**5/5 `overfit_warning=true`、`statistically_significant` 全 false** | 2026-09-27T20:33:47+08:00 |
| `/api/experiment/history` | 200 | `{"history":[]}`(15 B)⇒ 無任何已登錄 experiment | 2026-09-27T20:33:47+08:00 |
| `/api/experiment/diff`(裸 GET) | **400** | `experiment_id required`(route 活著,非 404) | 2026-09-27T20:34:20+08:00 |
| `/api/experiment/diff?experiment_id=does-not-exist` | **404** | `experiment result not found`(資源不存在型,非 route 404) | 2026-09-27T20:34:20+08:00 |
| 源碼 grep `continuous_rank\|top10_hit\|top1_hit\|risk_penalty\|reward_variant\|reward_function` | 0 命中 | atlas-go **沒有 reward variant 概念**(`internal/eval` 有 `CheckSLRLAlignment` 作為 reward/績效錯配評分,0 生產呼叫者) | 2026-09-27T20:36+08:00 |

**更正（2026-09-27）**

1. Step 2 的 Sharpe **不能**從 `risk_get_metrics` 拿(該端點無 Sharpe);今日唯一 IS/OOS Sharpe 出口是 `/api/dashboard/agent-observatory`,而它今日 **5/5 overfit、0/5 顯著**。
2. 「experiment_diff 可用 ⇒ 4 種 reward 可 A/B」**今日不可執行**:`/api/experiment/history` 為空,沒有 experiment_id 可餵;裸 GET 仍是 400、不存在 id 是 404 ⇒ 端點活著但**資料面 0 筆**。
3. 「atlas 提供評估與對比端點 ⇒ 對位完整度高」下修為:**評估端點在(且今日無效值)、對比端點在(且今日無資料)**。
4. 「無自動化多 reward sweep」以源碼級複驗成立:`SweepParameter`(`internal/config/inference.go`)與 `RecommendFromSweep`(`bayesian_optimizer.go`)都是**對單一 config 參數**的掃描,與 reward 函數無關,且無 HTTP 路由。

## 未消化 / 待補
- [ ] 4 種 reward 的「訓練成本」需列入:有些 reward(如 risk_penalty)訓練更慢。
- [ ] 與 SK-36 的關係:SK-32 確認最佳 reward,SK-36 確認最佳策略族(SL vs RL),兩者交集才是「最佳實務」。
- [ ] 「換 reward 的邊際效益」需量化,才能判斷 A/B 測試的 ROI。
