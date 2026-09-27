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
verification: 2026-08-01 v0.9 結算跑過 L3 升 active（快照）:backtest_signals sharpe_long 0.27/sharpe_short 0.49;risk_get_metrics session_count=147（2026-08-01 快照）。**PPO 訓練完全在 client 端,atlas 端不提供 RL 訓練**。[2026-09-27 batch#5 複驗（7 端點:5×200、2×404）:「atlas 無 RL 訓練面」今日**三路成立**——HTTP 無端點（`/api/rl/status`、`/api/agent/status` 皆 404 route not found）、排程無 job（110 jobs,0 個 rl/ppo/reward/policy）、源碼 0 實作（`\bppo\b`/`\blstm\b`/`\btransformer\b` 0 命中,`reinforcement` 僅 2 處註解）;**但「atlas 完全沒有訓練層」不成立**（PRISM regime 分群訓練樣本佇列 `prism_training` 今日 09:29Z 跑過;`ml_retrain` description 寫「D2 決策暫停:無消費端」且 disabled）;原句「backtest_signals 的 Sharpe」與「risk_get_metrics 取 Sharpe」**不可重現**（今日 signals 全 0/null、`/api/dashboard/risk` 無 Sharpe 欄位）⇒ Sharpe 一律走 `/api/dashboard/agent-observatory`。見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b5）
l3_endpoints_probed:
  - "/api/backtest/signals → 200（全 0/null） (2026-09-27T20:26:19+08:00)"
  - "/api/backtest/status → 200 (2026-09-27T20:26:19+08:00)"
  - "/api/dashboard/risk → 200（無 Sharpe 欄位） (2026-09-27T20:26:19+08:00)"
  - "/api/dashboard/agent-observatory → 200（5 scorecards） (2026-09-27T20:26:24+08:00)"
  - "/api/scheduler/status → 200（110 jobs） (2026-09-27T20:26:25+08:00)"
  - "/api/rl/status → 404 route not found (2026-09-27T20:26:25+08:00)"
  - "/api/agent/status → 404 route not found (2026-09-27T20:26:25+08:00)"
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
| 評估 | `risk_get_metrics` **無 Sharpe 欄位**（2026-09-27）⇒ 實際取 Sharpe 要走 `/api/dashboard/agent-observatory` |

**差異點**:PPO 完全 client 端;atlas 只負責資料與回測驗證（今日複驗成立,但「atlas 無任何訓練層」不成立:PRISM regime 分群訓練樣本佇列在跑;見 §驗證方式）。**論文版 RL 勝出 SL,但這個結論依賴 reward function 設計(SK-25),reward 設計錯了 RL 就崩**。

**沒有對位的部分**:無原生 PPO 端點;無 RL 環境 endpoint;無「軌跡儲存」(replay buffer)。

## 散戶解讀
- **G**:用戶問「AI 自動選產業?」 → PPO 是當前主流,論文中勝出 SL。
- **+E**:**論文 RL 勝出不代表你跑 RL 也會勝**——reward function 設計、網路架構、訓練步數、樣本效率,任何一項錯就全錯。**散戶若沒 ML 工程能力,不要碰 RL**。
- 對位 ATLAS_METHODOLOGY 七時期:PPO 在 regime 切換時幾乎一定要重訓,且需要「transition data」做 offline RL 預熱。

## 驗證方式
Step 1: 環境用 SK-23 產業輪動(client 端組裝),reward 用 SK-25 continuous_rank。
Step 2: client 端 `PPO('MlpPolicy', env, learning_rate=3e-4)` 訓練 100k steps。
Step 3: 對 `backtest_signals` 跑出的 RL 序列取 Sharpe 時,**不要用 `risk_get_metrics`**（無 Sharpe 欄位,2026-09-27）;改用 `/api/dashboard/agent-observatory`（今日 5 scorecards、附 `is_sharpe`/`oos_sharpe`/`overfit_warning`/`t_stat`）。

### L3 端點實跑（2026-09-27,本 PR）

| 端點 | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/rl/status` | **404** | `{"code":"404","error":"route not found"}` ⇒ 無 RL 狀態面 | 2026-09-27T20:26:25+08:00 |
| `/api/agent/status` | **404** | 同上,無 RL agent 面 | 2026-09-27T20:26:25+08:00 |
| `/api/scheduler/status` | 200 | **110** jobs;`rl`/`ppo`/`reward`/`policy` 名稱 0 命中;`ml_retrain` **disabled**;`prism_training` enabled（last_run 2026-09-27T09:29Z） | 2026-09-27T20:26:25+08:00 |
| `/api/backtest/signals` | 200 | `active_signals=null`、`sharpe_short`/`sharpe_long` 皆 0（**與 2026-08-01 的 0.27/0.49 不同,今日不可重現**） | 2026-09-27T20:26:19+08:00 |
| `/api/dashboard/risk` | 200 | keys 只有 `degraded/gate_mode/risk_snapshot/session_count/source/var_gate`;**無 Sharpe 欄位**;`session_count`=210、`insufficient_data`=1 | 2026-09-27T20:26:19+08:00 |
| `/api/dashboard/agent-observatory` | 200 | **5** scorecards（`etf-rotation-01`／`value-yield-01`／`super-ack-01`／`financials-desk-01`／`energy-desk-01`）,全部 `overfit_warning=true`、`statistically_significant=false` | 2026-09-27T20:26:24+08:00 |
| `/api/backtest/status` | 200 | `last_auto_date=2026-09-23`、`last_auto_portfolio_val`=3097172.40 | 2026-09-27T20:26:19+08:00 |

**更正（2026-09-27）**

1. 「`backtest_signals` sharpe_long 0.27／sharpe_short 0.49」**不可重現**:今日該端點兩欄皆 0、`active_signals=null`（2026-09-27T20:26:19+08:00）。原數字只能當 2026-08-01 快照。
2. 「評估用 `risk_get_metrics` 拿 Sharpe」**口徑錯誤**:`/api/dashboard/risk` 今日 payload 無 Sharpe 欄位（2026-09-27T20:26:19+08:00）⇒ 一律改走 `/api/dashboard/agent-observatory`。
3. 「atlas 端不提供 RL 訓練」**成立且今日三路驗證**:HTTP（2 個 404）、排程（110 jobs 中 0 個 RL job）、源碼（`\bppo\b`/`\blstm\b`/`\btransformer\b` 在 `*.go` 0 命中;`reinforcement` 只 2 處註解,其中 1 處就在 `internal/eval/doc.go` 標 SK-28）。
4. **新增（原頁未載）**:atlas 有 regime 分群訓練樣本層 PRISM（`prism (cohort training queues) → janus → simulation`;排程 `prism_training` enabled、last_run 2026-09-27T09:29Z）,是**監督式/replay 樣本**,不是 RL;`ml_retrain` 排程 description 明寫「D2 決策暫停:無消費端」且 `enabled=false`（2026-09-27T20:26:25+08:00）。CLI 複驗:`go run ./cmd/backtest-pipeline -synthetic -model nn` = **exit 1**,訊息列出白名單 `ols, pcr, pls, elasticnet, glm, rf`（無 RL/NN）。

## 未消化 / 待補
- [ ] stable-baselines3 PPO 的 hyperparameter 預設與論文差異需驗證。
- [ ] RL 訓練成本(100k steps × 47 動作)極高,實務需 GPU。
- [ ] 與 SK-28 獎勵錯配診斷:若 PPO 訓練 reward 高但 OOS Sharpe 低,需 SK-28 介入。
- [ ] SK-27 量子 PPO 實務效能更差,論文已警告,SK-24 不建議用量子網路。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:PPO 強化學習需對位 7 時期切換下的策略適應)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)