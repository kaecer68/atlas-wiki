---
title: SK-28 獎勵-績效錯配診斷
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-28
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:backtest_signals/risk_get_metrics 跑通;**Spearman 相關需 client 端算**,atlas 端不暴露 rolling Sharpe + Spearman correlation 端點;收集 SK-24/SK-25 訓練過程的 reward_history(客戶端),call risk_get_metrics 算 backtest 滾動 Sharpe(客戶端 rolling),client 端算 Spearman(reward_history, rolling_sharpe) < 0.5 觸發警告;論文結論:rewards 與 Sharpe 相關 < 0.5 應重設 reward function。
---

## 一句話定位
SK-28 是 RL 的「驗屍報告」——訓練 reward 一直漲但實盤虧錢?99% 是 reward 與 Sharpe 錯配。SK-28 量化這件事,給出「該改 reward 函數」的明確訊號。

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
| 滾動 Sharpe | `risk_get_metrics`(可能需 client 端算 rolling) |
| 診斷報告 | `experiment_diff` 對比不同 reward |

**差異點**:診斷邏輯在 client 端;atlas 提供「reward 與 Sharpe 的資料源」,**correlation 計算必須 client 端跑**。

**沒有對位的部分**:無原生「reward-Sharpe 相關性」端點;無「rolling Sharpe」單一端點(可能需 client 端自算)。

## 散戶解讀
- **G**:用戶問「RL 訓練 reward 漲 10 倍,實盤卻虧 5%?」 → 跑 SK-28,9 成機率 Spearman < 0.3,代表 reward 設計錯。
- **+E**:**散戶最常見 RL 失敗模式就是 reward 錯配**——論文把這件事量化成單一數字,讓 debug 有依據,不是「看感覺」。
- 對位 ATLAS_METHODOLOGY 七時期:regime 切換時 reward-Sharpe 相關會掉,SK-28 觸發警告 → 改 reward 函數 → 重訓。

## 驗證方式
Step 1: 從 SK-25 4 種 reward 訓練的 reward_history 各抓 100 個 epoch 平均值。
Step 2: 對每個 PPO agent 跑 `backtest_signals` 拿 backtest_returns,client 端算 60 日 rolling Sharpe。
Step 3: 算 Spearman(reward_history, rolling_sharpe),預期 continuous_rank 最高(> 0.5),top1_hit 最低(< 0.3)。

## 未消化 / 待補
- [ ] rolling Sharpe 視窗(60 日)是論文預設,需驗證台股月度資料下的最佳視窗。
- [ ] Spearman 0.5 閾值是經驗值,可能偏嚴或偏鬆。
- [ ] 與 SK-22 消去法的關係:SK-22 驗「因子重要性」,SK-28 驗「reward 重要性」,可共用 experiment_diff 框架。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Reward Mismatch 獎勵錯位需對位 regime 切換下的策略失效)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)