---
title: SK-24 PPO 強化學習訓練框架
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-24
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:backtest_signals sharpe_long 0.27/sharpe_short 0.49;risk_get_metrics live session_count=147;**PPO 訓練完全在 client 端(stable-baselines3),atlas 端不提供 RL 訓練**:論文中 PPO 100k steps + 30% policy clip + 0.99 gamma 需 GPU;atlas 端只能驗證「訓練好後」回測結果,不能驗證訓練本身。
---

## 一句話定位
SK-24 是論文的強化學習核心——用 PPO 訓練一個「產業輪動 agent」,每天決定資金在 47 個產業間怎麼分。**論文實證 RL 勝出 SL(SK-16),但這是學術結論,實務散戶要小心**。

## 論文版概念
- 標準 PPO:gamma=0.99, clip_epsilon=0.2, entropy_coef=0.01
- 策略網路:SK-26(LSTM)或 SK-27(量子)
- 環境:SK-23 產業輪動
- 動作:每期 47 個產業的權重
- 獎勵:SK-25 的 reward 函數

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| PPO 訓練 | 缺(client 端 stable-baselines3) |
| 環境建構 | SK-23 部分對位 |
| 回測 | `backtest_signals` |
| 評估 | `risk_get_metrics` |

**差異點**:PPO 完全 client 端;atlas 只負責資料與回測驗證。**論文版 RL 勝出 SL,但這個結論依賴 reward function 設計(SK-25),reward 設計錯了 RL 就崩**。

**沒有對位的部分**:無原生 PPO 端點;無 RL 環境 endpoint;無「軌跡儲存」(replay buffer)。

## 散戶解讀
- **G**:用戶問「AI 自動選產業?」 → PPO 是當前主流,論文中勝出 SL。
- **+E**:**論文 RL 勝出不代表你跑 RL 也會勝**——reward function 設計、網路架構、訓練步數、樣本效率,任何一項錯就全錯。**散戶若沒 ML 工程能力,不要碰 RL**。
- 對位 ATLAS_METHODOLOGY 七時期:PPO 在 regime 切換時幾乎一定要重訓,且需要「transition data」做 offline RL 預熱。

## 驗證方式
Step 1: 環境用 SK-23 產業輪動(client 端組裝),reward 用 SK-25 continuous_rank。
Step 2: client 端 `PPO('MlpPolicy', env, learning_rate=3e-4)` 訓練 100k steps。
Step 3: 對 `backtest_signals` 跑出的 RL 序列,call `risk_get_metrics` 拿 Sharpe,對比 SK-16 SL 策略(預期 RL 優 10-30%)。

## 未消化 / 待補
- [ ] stable-baselines3 PPO 的 hyperparameter 預設與論文差異需驗證。
- [ ] RL 訓練成本(100k steps × 47 動作)極高,實務需 GPU。
- [ ] 與 SK-28 獎勵錯配診斷:若 PPO 訓練 reward 高但 OOS Sharpe 低,需 SK-28 介入。
- [ ] SK-27 量子 PPO 實務效能更差,論文已警告,SK-24 不建議用量子網路。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:PPO 強化學習需對位 7 時期切換下的策略適應)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)