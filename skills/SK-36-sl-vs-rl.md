---
title: SK-36 監督學習 vs. 強化學習策略比較
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-31 (wiki 編號已改為 SK-36, 2026-08-21 kaecer 拍板, kimi-for-coding 審查 8 步執行)
renumbered_from: SK-31
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics, experiment_diff]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:backtest_signals sharpe_long 0.27/sharpe_short 0.49(SL 對比基準);risk_get_metrics live session_count=147;**experiment_diff 可用性更新：2026-08-07 SK-22 證實原 400 為參數名誤判（id= 應為 experiment_id=）,端點可用 [2026-08-22 audit-fix]**;論文中 RL 勝出 SL 的結論需 client 端 GPU + stable-baselines3 驗證,atlas 端只提供回測引擎不提供 RL 訓練;atlas SL/RL 都用同一 backtest_signals 端點,真實分流依 `experiment_diff` 需真 experiment_id。
---

## 一句話定位
SK-36 是論文的「論文對論文」對比——同樣的台股資料,SL(SK-16)與 RL(SK-24)哪個強?**論文結論是 RL 勝出,但這個結論需散戶親自驗證,不能照單全收**。

## 論文版概念
- 輸入:sl_strategy(SK-16)、rl_strategy(SK-24 + SK-29)、test_data
- 動作:
  1. SL 策略跑回測 → 報酬序列
  2. RL 策略跑回測 → 報酬序列
  3. 算 sharpe / cumulative_return / max_drawdown
  4. 對比報告 + 視覺化
- 論文結論:RL 勝出(在產業輪動任務上)

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 兩套策略回測 | `backtest_signals`(同資料源) |
| 對比指標 | `risk_get_metrics` |
| 統一報告 | `experiment_diff` |

**差異點**:論文的 SL vs RL 對比需 client 端組裝兩套策略;atlas 提供「回測引擎 + 評估 + 對比」三件套。**這是 atlas 端對位完整的 SK 之一**。

**沒有對位的部分**:無「跨策略對比報告」單一端點(需 client 端組裝);無「視覺化」端點。

## 散戶解讀
- **G**:用戶問「SL 跟 RL 哪個好?」 → 論文的答案是 RL,散戶的答案可能不同(因為 RL 在小樣本下極不穩定)。
- **+E**:**論文結論可參考但不可照單全收**——論文的 RL 用了 100k steps 訓練,散戶沒這個算力。**散戶若想驗證 SK-36 結論,需先有 GPU + stable-baselines3 經驗**。
- 對位 ATLAS_METHODOLOGY 七時期:RL 對 regime 切換的適應力是 SL 強項(因為有獎勵驅動),但訓練成本數量級高於 SL(論文用 100k steps,未給實測倍數),trade-off 真實存在。 [2026-08-22 驗證:100 倍無來源,弱化為數量級描述]

## 驗證方式
Step 1: 確認 SK-16 SL 策略已訓練好(client 端或 atlas 內),SK-24 RL agent 也訓練好。
Step 2: 同一份 test_data,call `backtest_signals` 對兩策略各跑一次。
Step 3: call `risk_get_metrics` 對比 sharpe_ratio、max_drawdown;call `experiment_diff` 出統一 diff 報告(若 atlas 端 SL/RL 都已登錄為 experiment)。

## 未消化 / 待補
- [ ] 論文結論 RL 勝出的具體條件(訓練步數、reward 函數、樣本量)需記錄,讓散戶知道「這個結論的 valid scope」。
- [ ] 跨策略對比的「公平性」:SL 與 RL 的訓練成本差異 100x,單看 Sharpe 不夠,需把「算力成本」列入。
- [ ] 與 SK-32 敏感性分析:SL 的 hyperparameter 沒 RL 多,SL 結果更穩定是預期之內。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:SL vs RL 對比需對位 7 時期 × 策略三分類,跨 regime 表現差異大)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)