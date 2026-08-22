---
title: SK-32 獎勵函數敏感性分析
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-32
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics, experiment_diff]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:backtest_signals/risk_get_metrics 跑通;**experiment_diff 可用性更新：2026-08-07 SK-22 證實原 400 為參數名誤判（id= 應為 experiment_id=）,端點可用 [2026-08-22 audit-fix]**:端點活,4 種 reward 函數(continuous_rank/top10_hit/top1_hit/risk_penalty)可 A/B 對比,但需 client 端自己 4 輪 experiment 產生 experiment_id;論文中 continuous_rank 最優無法用 atlas 驗證,需另起 PPO 訓練環境。
---

## 一句話定位
SK-32 把 SK-25 的 4 種 reward 函數變成「哪個最優」的可信結論——單獨看 SK-25 還不夠,**reward function 對結果的敏感度必須量化**,散戶才知道「換 reward 值不值得」。

## 論文版概念
- 對每個 reward_variant:
  1. 複製環境(同樣隨機種子)
  2. 設新 reward 函數
  3. 訓練 PPO 100k steps
  4. 回測算 eval_metric(預設 sharpe_ratio)
- 彙整成 DataFrame:reward_variant → 評估指標
- 排序找最佳

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 環境複製 | 完全 client 端 |
| PPO 訓練 | 缺(client 端 stable-baselines3) |
| 評估 | `backtest_signals` + `risk_get_metrics` |
| 跨 reward 對比 | `experiment_diff` |

**差異點**:訓練全 client 端;atlas 提供「評估與對比」端點。**這是 atlas 端對位完整度高的 SK 之一**。

**沒有對位的部分**:無「自動化多 reward sweep」端點;無「hyperparameter 搜尋」端點。

## 散戶解讀
- **G**:用戶問「哪個 reward 函數最賺?」 → 跑 SK-32 出敏感性表,**論文的答案是 continuous_rank,但散戶的台股資料上可能 top10_hit 反而好**——一定要自己跑。
- **+E**:**reward 函數是 RL 唯一的「可控設計選擇」**——架構(LSTM/MLP)、訓練步數、隨機種子都不可控或成本高,**唯獨 reward 函數可以快速 A/B 測試**。**散戶若只碰 RL 的一個東西,應該是 reward 函數**。
- 對位 ATLAS_METHODOLOGY 七時期:regime 切換時最佳 reward 函數可能換——SK-32 需每期重跑。

## 驗證方式
Step 1: 用 SK-25 4 種 reward 各訓練 100k steps(client 端,固定隨機種子)。
Step 2: 對每個 agent 跑 `backtest_signals` 拿序列,call `risk_get_metrics` 拿 Sharpe / max_drawdown / 換手率。
Step 3: client 端彙整成 DataFrame,sort by sharpe_ratio desc,確認連續型 reward(continuous_rank)在前 2 名(論文結論)。

## 未消化 / 待補
- [ ] 4 種 reward 的「訓練成本」需列入:有些 reward(如 risk_penalty)訓練更慢。
- [ ] 與 SK-36 的關係:SK-32 確認最佳 reward,SK-36 確認最佳策略族(SL vs RL),兩者交集才是「最佳實務」。
- [ ] 「換 reward 的邊際效益」需量化,才能判斷 A/B 測試的 ROI。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Reward Sensitivity 敏感度需對位 regime 切換下的策略穩健性)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)