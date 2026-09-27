---
title: SK-28 獎勵-績效錯配診斷
description: "問「RL 訓練 reward 一直漲、實盤卻虧錢」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-28
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active（快照）:backtest_signals/risk_get_metrics 跑通。原句「Spearman 相關需 client 端算,atlas 端不暴露 rolling Sharpe + Spearman correlation 端點」。[2026-09-27 batch#5 複驗（7 端點:5×200、1×400、1×404＋`go test ./internal/eval/`）:**源碼層已有**原生 Spearman＋失配判級 —— `internal/eval/mismatch.go` 的 `CheckSLRLAlignment(yTrue,yPred,dailyReturns)` 回 `{mismatch_detected, prediction_r2, trading_sharpe, rank_correlation, severity, diagnosis}`,內部 `spearmanRankCorrelation`（平手用平均等級）;判級 R²>0.1 且 rankCorr<0.1 → severe、R²>0.05 且(Sharpe<0.3 或 rankCorr<0.2) → moderate;`go test ./internal/eval/ -count=1 -v` = **22 PASS / 0 FAIL（0.3 s）**,含 7 個 `TestCheckSLRLAlignment_*`＋`TestRankCorrelation`(4 子測);但**生產呼叫者 0**（`git grep` 只命中 doc.go/mismatch.go/測試檔）⇒ 只有函式、沒有端點;atlas 實作門檻（0.2／0.1）比論文（0.5）寬鬆;**rolling Sharpe 已有 live 代理** = `/api/dashboard/agent-observatory` 的 `rolling_sharpe_trend`;實驗路徑今日仍不可用（history 空、diff 400/404）。見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b5）
l3_endpoints_probed:
  - "/api/dashboard/agent-observatory → 200（rolling_sharpe_trend 5 筆） (2026-09-27T20:26:24+08:00)"
  - "/api/dashboard/risk → 200（無 Sharpe 欄位） (2026-09-27T20:26:19+08:00)"
  - "/api/dashboard/drawdown → 200（var_95=-0.004816） (2026-09-27T20:27:16+08:00)"
  - "/api/backtest/signals → 200（全 0/null） (2026-09-27T20:26:19+08:00)"
  - "/api/experiment/history → 200（history 為空） (2026-09-27T20:26:25+08:00)"
  - "/api/experiment/diff → 400 experiment_id required (2026-09-27T20:27:16+08:00)"
  - "/api/experiment/diff?experiment_id=nonexistent → 404 (2026-09-27T20:27:16+08:00)"
  - "/api/scheduler/status → 200（110 jobs） (2026-09-27T20:26:25+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Reward Mismatch 獎勵錯位需對位 regime 切換下的策略失效)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-28 是 RL 的「驗屍報告」——訓練 reward 一直漲但實盤虧錢?極高比例是 reward 與 Sharpe 錯配。 [2026-08-22 驗證:99% 無來源,弱化為定性描述]SK-28 量化這件事,給出「該改 reward 函數」的明確訊號。

## 論文版概念
- 輸入:reward_history(每輪平均 reward)、backtest_returns(組合報酬)
- 動作:
  1. 算回測滾動 Sharpe(60 日窗)
  2. 算 reward_history 與滾動 Sharpe 的 Spearman 相關
  3. 相關 < 0.5 觸發警告,建議重設 reward
- 輸出:`{spearman_correlation, mismatch_warning, recommendation}`

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| reward 記錄 | 完全 client 端責任 |
| 滾動 Sharpe | `/api/dashboard/agent-observatory` 的 `rolling_sharpe_trend`（`risk_get_metrics` 無 Sharpe 欄位,2026-09-27） |
| 診斷報告 | `experiment_diff` 對比不同 reward（今日不可用:history 空、diff 400/404,2026-09-27） |

**差異點**（2026-09-27 更正）:診斷邏輯**已有原生實作**（`CheckSLRLAlignment`,Spearman＋判級）,但**沒有端點、0 生產呼叫者** ⇒ 目前實務上仍要 client 端跑;atlas 的可取用部分是 Sharpe／rolling Sharpe 資料源。

**沒有對位的部分**（2026-09-27 更正）:無「reward-Sharpe 相關性」**端點**（函式有）;無獨立「rolling Sharpe」端點,但 `agent-observatory` 已內含 `rolling_sharpe_trend`。

## 散戶解讀
- **G**:用戶問「RL 訓練 reward 漲 10 倍,實盤卻虧 5%?」 → 跑 SK-28,多數情況下 Spearman < 0.3,代表 reward 設計錯。 [2026-08-22 驗證:9 成無來源,弱化為定性描述]
- **+E**:**散戶最常見 RL 失敗模式就是 reward 錯配**——論文把這件事量化成單一數字,讓 debug 有依據,不是「看感覺」。
- 對位 ATLAS_METHODOLOGY 七時期:regime 切換時 reward-Sharpe 相關會掉,SK-28 觸發警告 → 改 reward 函數 → 重訓。

## 驗證方式
Step 1: 從 SK-25 4 種 reward 訓練的 reward_history 各抓 100 個 epoch 平均值。
Step 2: 對每個 PPO agent 跑 `backtest_signals` 拿 backtest_returns,client 端算 60 日 rolling Sharpe。
Step 3: 算 Spearman(reward_history, rolling_sharpe),預期 continuous_rank 最高(> 0.5),top1_hit 最低(< 0.3)。

### L3 端點實跑（2026-09-27,本 PR）

| 端點／命令 | http_code／exit | 實測結果 | timestamp |
|---|---|---|---|
| `go test ./internal/eval/ -count=1 -v` | 0 | **22 PASS / 0 FAIL**（0.3 s）;含 7 個 `TestCheckSLRLAlignment_*`＋`TestRankCorrelation`(4 子測) | 2026-09-27T20:29 |
| `/api/dashboard/agent-observatory` | 200 | **5** scorecards,每筆都有 `rolling_sharpe_trend`（−0.001598～+1.0e-4）、`is_sharpe`／`oos_sharpe`／`is_oos_ratio`／`overfit_warning`／`t_stat`;全部 `overfit_warning=true` | 2026-09-27T20:26:24+08:00 |
| `/api/dashboard/risk` | 200 | **無 Sharpe 欄位**（keys: `degraded/gate_mode/risk_snapshot/session_count/source/var_gate`）;`session_count`=210、`insufficient_data`=1 | 2026-09-27T20:26:19+08:00 |
| `/api/dashboard/drawdown` | 200 | `var_95=-0.00481584029711588`、`max_drawdown`=0.9229（全站唯一非零 `var_95` 出口） | 2026-09-27T20:27:16+08:00 |
| `/api/backtest/signals` | 200 | 全 0/null ⇒ 60 日滾動 Sharpe 的輸入序列今日取不到 | 2026-09-27T20:26:19+08:00 |
| `/api/experiment/history` | 200 | `{"history":[]}` | 2026-09-27T20:26:25+08:00 |
| `/api/experiment/diff`（裸 GET／不存在 id） | **400／404** | `experiment_id required`／`experiment result not found` | 2026-09-27T20:27:16+08:00 |

**更正（2026-09-27）**

1. 「atlas 端不暴露 rolling Sharpe + Spearman correlation 端點」只對一半:**函式層已存在** —— `internal/eval/mismatch.go` 提供 `CheckSLRLAlignment`（回 `prediction_r2`、`trading_sharpe`、`rank_correlation`、`severity`、`diagnosis`）與 `spearmanRankCorrelation`（平手取平均等級;長度不足回 0）。**缺的是端點與生產呼叫者**（`git grep CheckSLRLAlignment` 只命中 `doc.go`、`mismatch.go`、`mismatch_test.go`;2026-09-27）。
2. **門檻口徑不同,引用時必須註明**:論文寫「相關 < 0.5 觸發警告」;atlas 原生實作是 `severe` = R²>0.1 且 rankCorr<0.1、`moderate` = R²>0.05 且（Sharpe<0.3 或 rankCorr<0.2）。**atlas 門檻明顯較寬鬆**,不得把兩者當同一把尺。
3. 健康度 ↔ 偏離度不對稱:論文驗的是 `Spearman(reward_history, rolling_sharpe)`;atlas 原生驗的是 `Spearman(yPred, yTrue)`（預測排序 vs 實際報酬排序）＋ Sharpe 水準 ⇒ 兩者**輸入不同**,atlas 版不能直接吃 reward_history。
4. 「滾動 Sharpe 只能 client 端自算」**已不成立**:`agent-observatory` 每筆 scorecard 都有 `rolling_sharpe_trend`（2026-09-27T20:26:24+08:00）;60 日窗仍需 client 端另算,因為端點未給窗長參數。

## 未消化 / 待補
- [ ] rolling Sharpe 視窗(60 日)是論文預設,需驗證台股月度資料下的最佳視窗。
- [ ] Spearman 0.5 閾值是經驗值,可能偏嚴或偏鬆。
- [ ] 與 SK-22 消去法的關係:SK-22 驗「因子重要性」,SK-28 驗「reward 重要性」,可共用 experiment_diff 框架。
