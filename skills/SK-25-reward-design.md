---
title: SK-25 獎勵函數設計與評估
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-25
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active（快照）:backtest_signals/risk_get_metrics 跑通。**reward 函數是 client 端設計+PPO 環境內,atlas 端只能驗證訓練後的回測**。[2026-09-27 batch#5 複驗（7 端點:5×200、1×400、1×404）:「reward 端點不存在」今日**成立**（Go 源碼 `reward` 只命中 config 文案,排程 110 jobs 中 0 個 reward/policy job）;但**「atlas 完全沒有 reward 相關邏輯」過強** —— 原生 `internal/eval/mismatch.go` 的 `CheckSLRLAlignment` 就是 reward/績效錯配評分（見 SK-28）;「4 個 experiment 才能 A/B」今日**不可行**（`/api/experiment/history`=`{"history":[]}` 0 筆、`/api/experiment/diff` 裸 GET 400、不存在 id 404）;`risk_get_metrics` **無 Sharpe 欄位**,取 Sharpe 走 `/api/dashboard/agent-observatory`。見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b5）
l3_endpoints_probed:
  - "/api/experiment/history → 200（history 為空） (2026-09-27T20:26:25+08:00)"
  - "/api/experiment/diff → 400 experiment_id required (2026-09-27T20:27:16+08:00)"
  - "/api/experiment/diff?experiment_id=nonexistent → 404 experiment result not found (2026-09-27T20:27:16+08:00)"
  - "/api/backtest/signals → 200（全 0/null） (2026-09-27T20:26:19+08:00)"
  - "/api/dashboard/risk → 200（無 Sharpe 欄位） (2026-09-27T20:26:19+08:00)"
  - "/api/dashboard/agent-observatory → 200（5 scorecards） (2026-09-27T20:26:24+08:00)"
  - "/api/scheduler/status → 200（110 jobs,0 個 reward/policy） (2026-09-27T20:26:25+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Reward 函數設計需對位 regime × 策略三分類對位)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-25 是 RL 成功的關鍵——論文實證 **reward 函數的選擇比 PPO 架構更重要**。同一個 PPO agent 換 4 種 reward,Sharpe 可能差異巨大(數倍)。 [2026-08-22 驗證:3 倍無來源,弱化為定性描述]

## 論文版概念
- 4 種 reward:
  - `top10_hit`:選中下期前 10 產業 +1,否則 -0.1
  - `continuous_rank`:reward = 1 - (rank/num_sectors)
  - `risk_penalty`:額外減波動率項
  - `top1_hit`:選中第 1 名 +1
- 評估:用 SK-28 診斷 reward-history 與 backtest-Sharpe 的 Spearman 相關

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| reward 設計 | 完全 client 端責任 |
| reward 評估 | 需 `backtest_signals` 拿序列;Sharpe **不可**用 `risk_get_metrics`（無此欄位,2026-09-27）⇒ 用 `/api/dashboard/agent-observatory` |
| 診斷 | `experiment_diff` 對比不同 reward 的最終策略 |

**差異點**:atlas 沒有 reward function **端點**;**但 reward 是 RL 唯一使用者可控的設計選擇**。

**沒有對位的部分**（2026-09-27 更正）:無原生 reward function 端點（成立）;「reward-Sharpe 相關性」**函式層已有**（`internal/eval/mismatch.go` 的 `CheckSLRLAlignment`,含 Spearman 等級相關）,缺的只是**端點與生產呼叫者**（見 SK-28）。

## 散戶解讀
- **G**:用戶問「我的 RL 為什麼訓練 reward 高、實盤卻虧?」 → 大多是 reward 函數設計錯。**論文實證 continuous_rank 最優**。 [2026-08-22 驗證:9 成無來源,弱化為定性描述]
- **+E**:**散戶最常見錯誤:用「絕對報酬」做 reward,結果 RL 學會「all-in 單一高波動資產」,Sharpe 反倒負**。**reward 函數必須反映「風險調整後報酬」,不能只看絕對數字**。
- 對位 ATLAS_METHODOLOGY 七時期:同一個 reward 在不同 regime 表現差異極大,需 regime-aware reward(進階題)。

## 驗證方式
Step 1: client 端實作 4 種 reward 函數,分別餵進 SK-24 PPO 訓練。
Step 2: 對每個 PPO agent 跑 `backtest_signals` 拿序列;Sharpe 走 `/api/dashboard/agent-observatory`（`risk_get_metrics` 無 Sharpe 欄位,2026-09-27）。
Step 3: 4 個 Sharpe 對比,預期 continuous_rank 最優(論文結論);若 top10_hit 反而最差,代表 RL 學會「猜中稀少的高 reward」而非「穩定選好產業」。

### L3 端點實跑（2026-09-27,本 PR）

| 端點 | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/experiment/history` | 200 | `{"history":[]}` ⇒ **0 筆實驗**,4 種 reward 的 A/B 對比今日無資料 | 2026-09-27T20:26:25+08:00 |
| `/api/experiment/diff` | **400** | `{"error":"experiment_id required"}` | 2026-09-27T20:27:16+08:00 |
| `/api/experiment/diff?experiment_id=nonexistent` | **404** | `experiment result not found` ⇒ 無實驗結果可 diff | 2026-09-27T20:27:16+08:00 |
| `/api/dashboard/risk` | 200 | 無 Sharpe 欄位;`session_count`=210、`insufficient_data`=1 | 2026-09-27T20:26:19+08:00 |
| `/api/backtest/signals` | 200 | 全 0/null（`active_signals=null`） | 2026-09-27T20:26:19+08:00 |
| `/api/dashboard/agent-observatory` | 200 | **5** scorecards,全部 `overfit_warning=true` | 2026-09-27T20:26:24+08:00 |
| `/api/scheduler/status` | 200 | **110** jobs,`reward`/`policy` 0 命中 | 2026-09-27T20:26:25+08:00 |

**更正（2026-09-27）**

1. 「需在 atlas 端登錄為 4 個 experiment,4 個實驗結果才能 A/B 對比」**今日不可行**:`experiment_history` 回空、`experiment_diff` 裸 GET 400／不存在 id 404（2026-09-27T20:27:16+08:00）。實驗路徑與 SK-22 於 batch#4 的結論一致。
2. 「atlas 完全沒 reward function 端點」**成立**（無端點、無排程 job）;但**「atlas 完全沒有 reward 相關邏輯」不成立** —— `internal/eval/mismatch.go` 的 `CheckSLRLAlignment` 原生做「預測品質 vs 交易績效」失配評分（`prediction_r2`＋`trading_sharpe`＋`rank_correlation`,7 個測試 PASS）,即 SK-28 的核心。
3. Sharpe 取用口徑更正:凡本頁寫「`risk_get_metrics` 算 Sharpe」處,一律改讀 `/api/dashboard/agent-observatory`（2026-09-27 實測 `risk` 端點無 Sharpe 欄位）。
4. 論文「continuous_rank 最優」今日**無法在 atlas 端複驗**（無 reward 端點、無實驗記錄）⇒ 維持 client 端待驗,不可引用為 atlas 結論。

## 未消化 / 待補

已解（2026-09-27）:「RL 沒有 R² 概念」**不成立**——atlas 原生失配偵測 `CheckSLRLAlignment`（`internal/eval/mismatch.go`）就是用 `prediction_r2`（`OOSR2`）＋ `rank_correlation`＋`trading_sharpe` 三件套判級,RL 路徑在 atlas 語意裡有 R²（作為預測品質代理）。
- [ ] 4 種 reward 的 hyperparameter(penalty=-0.1 等)需 tune,非開箱即用。
- [ ] regime-aware reward 是進階題,需 SK-22 消去法思路結合 SK-28 錯配診斷。
