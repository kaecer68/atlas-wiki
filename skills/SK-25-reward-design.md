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
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:backtest_signals/risk_get_metrics 跑通;**reward 函數是 client 端設計+PPO 環境內,atlas 端只能驗證訓練後的回測**:4 種 reward(continuous_rank/top10_hit/top1_hit/risk_penalty)需 client 端各自訓練+在 atlas 端登錄為 4 個 experiment,4 個實驗結果才能 A/B 對比;論文中 continuous_rank 最優需 client 端驗證。
---

## 一句話定位
SK-25 是 RL 成功的關鍵——論文實證 **reward 函數的選擇比 PPO 架構更重要**。同一個 PPO agent 換 4 種 reward,Sharpe 可能差 3 倍。

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
| reward 評估 | 需 `backtest_signals` 拿序列 + `risk_get_metrics` 算 Sharpe |
| 診斷 | `experiment_diff` 對比不同 reward 的最終策略 |

**差異點**:atlas 完全沒 reward function 端點;**但 reward 是 RL 唯一使用者可控的設計選擇**。

**沒有對位的部分**:無原生 reward function 端點;無「reward-Sharpe 相關性」端點。

## 散戶解讀
- **G**:用戶問「我的 RL 為什麼訓練 reward 高、實盤卻虧?」 → 9 成是 reward 函數設計錯。**論文實證 continuous_rank 最優**。
- **+E**:**散戶最常見錯誤:用「絕對報酬」做 reward,結果 RL 學會「all-in 單一高波動資產」,Sharpe 反倒負**。**reward 函數必須反映「風險調整後報酬」,不能只看絕對數字**。
- 對位 ATLAS_METHODOLOGY 七時期:同一個 reward 在不同 regime 表現差異極大,需 regime-aware reward(進階題)。

## 驗證方式
Step 1: client 端實作 4 種 reward 函數,分別餵進 SK-24 PPO 訓練。
Step 2: 對每個 PPO agent 跑 `backtest_signals` 拿序列,call `risk_get_metrics` 拿 Sharpe。
Step 3: 4 個 Sharpe 對比,預期 continuous_rank 最優(論文結論);若 top10_hit 反而最差,代表 RL 學會「猜中稀少的高 reward」而非「穩定選好產業」。

## 未消化 / 待補
- [ ] 4 種 reward 的 hyperparameter(penalty=-0.1 等)需 tune,非開箱即用。
- [ ] regime-aware reward 是進階題,需 SK-22 消去法思路結合 SK-28 錯配診斷。
- [ ] 與 SK-12 R²_oos 對比:RL 沒有 R² 概念,只能用 Sharpe 對比,評估方法不同。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Reward 函數設計需對位 regime × 策略三分類對位)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)