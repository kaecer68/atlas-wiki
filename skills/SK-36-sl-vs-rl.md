---
title: SK-36 監督學習 vs. 強化學習策略比較
description: "問「監督學習跟強化學習哪個好」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-31 (wiki 編號已改為 SK-36, 2026-08-21 kaecer 拍板, kimi-for-coding 審查 8 步執行)
renumbered_from: SK-31
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics, experiment_diff]
verification: "歷史(2026-08-01 v0.9 升 active)：backtest_signals sharpe_long 0.27／sharpe_short 0.49(SL 對比基準)、risk_get_metrics session_count=147；[2026-08-22 audit-fix] experiment_diff 原 400 為參數名誤判。**2026-09-27 L3 實跑**：backtest_signals 全 0/null(Sharpe 對比基準今日不可得)、risk 無 Sharpe 欄位、experiment/history 空、diff 400／404、`/api/strategies/active` **12 檔 SL 策略(source=backtest)**、`go test ./internal/eval/ -count=1 -v` 72 PASS／0 FAIL(含 7 個 TestCheckSLRLAlignment_*＝原生 SL/RL 錯配檢定,但 0 生產呼叫者)。見 §驗證方式。"
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b6）
l3_endpoints_probed:
  - "/api/backtest/signals → 200（sharpe 全 0） (2026-09-27T20:33:10+08:00)"
  - "/api/dashboard/risk → 200（無 Sharpe 欄位） (2026-09-27T20:33:10+08:00)"
  - "/api/strategies/active → 200（12 檔 SL 策略） (2026-09-27T20:36:30+08:00)"
  - "/api/strategies/layers → 200（L1 1/L2 2/L3 2/L4 4/L5 3＝12） (2026-09-27T20:36:30+08:00)"
  - "/api/dashboard/agent-observatory → 200（5 筆,全部 overfit） (2026-09-27T20:33:47+08:00)"
  - "/api/experiment/history → 200（history 空） (2026-09-27T20:33:47+08:00)"
  - "/api/experiment/diff → 400／不存在 id 404 (2026-09-27T20:34:20+08:00)"
  - "go test ./internal/eval/ -count=1 -v → 0（72 PASS／0 FAIL） (2026-09-27T20:36+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:SL vs RL 對比需對位 7 時期 × 策略三分類,跨 regime 表現差異大)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-36 是論文的「論文對論文」對比——同樣的台股資料,SL(SK-16)與 RL(SK-24)哪個強?**論文結論是 RL 勝出,但這個結論需散戶親自驗證,不能照單全收**。

## 論文版概念
- 輸入:sl_strategy(SK-16)、rl_strategy(SK-24 + SK-29)、test_data。
- 動作:SL 策略跑回測 → RL 策略跑回測 → 算 sharpe / cumulative_return / max_drawdown → 對比報告 + 視覺化。
- 論文結論:RL 勝出(在產業輪動任務上)。

## atlas 對位
| 論文概念 | atlas-mcp 對位 | 今日實測 |
|---------|---------------|---------|
| SL 側策略清單 | `strategy_list_active` / `/api/strategies/layers` | 200:**12 檔**(source=`backtest`) |
| RL 側策略 | 無(SK-24 三路驗證:無 `/api/rl/status`、無 RL 排程、源碼 0 命中) | — |
| 兩套策略回測 | `backtest_signals`(同資料源) | 200:`active_signals`=null、sharpe 全 0 |
| 對比指標 | `risk_get_metrics` | 200:**無 Sharpe 欄位** |
| 統一報告 | `experiment_diff` | 400(裸 GET)／404(資源不存在);history 空 |
| 原生 SL/RL 錯配檢定 | `internal/eval/mismatch.go` `CheckSLRLAlignment` | `go test ./internal/eval/` 72 PASS;7 個 `TestCheckSLRLAlignment_*`;**0 生產呼叫者** |

**差異點**:論文的 SL vs RL 對比需 client 端組裝兩套策略;atlas 提供「回測引擎 + 評估 + 對比」三件套,但**RL 側整條不存在**,對比今日無法在 atlas 內完成。
**沒有對位的部分**:無「跨策略對比報告」單一端點;無「視覺化」端點。

## 散戶解讀
- **G**:用戶問「SL 跟 RL 哪個好?」 → 論文答案 RL,散戶答案可能不同(RL 在小樣本下極不穩定;atlas 端 5 檔 scorecard 今日 5/5 overfit 可作側證)。
- **+E**:**論文結論可參考但不可照單全收**——論文 RL 用 100k steps 訓練,散戶沒這個算力。要驗證 SK-36 需先有 GPU + stable-baselines3 經驗。
- 對位 ATLAS_METHODOLOGY 七時期:RL 對 regime 切換的適應力是賣點,但訓練成本數量級高於 SL,trade-off 真實存在。 [2026-08-22 驗證:100 倍無來源,弱化為數量級描述]

## 驗證方式
Step 1: 確認 SK-16 SL 策略已訓練好(client 端或 atlas 內),SK-24 RL agent 也訓練好。
Step 2: 同一份 test_data,call `backtest_signals` 對兩策略各跑一次。
Step 3: call `risk_get_metrics` 對比 sharpe_ratio、max_drawdown;call `experiment_diff` 出統一 diff 報告。

### L3 端點實跑（2026-09-27,本 PR）

| 端點／命令 | http_code／exit | 實測結果 | timestamp |
|---|---|---|---|
| `/api/backtest/signals` | 200 | `active_signals`=null、`sharpe_short`/`sharpe_long`=**0**(2026-08-01 的 0.49／0.27 今日量不到)、`drawdown_pct`/`var_95` 全 0 | 2026-09-27T20:33:10+08:00 |
| `/api/dashboard/risk` | 200 | **無 Sharpe 欄位**;`session_count`=210、`max_drawdown_pct`=0.7220、`insufficient_data`=1 | 2026-09-27T20:33:10+08:00 |
| `/api/strategies/active` | 200 | **12 檔**策略,欄位含 `layer`/`hit_rate`/`total_tests`/`total_hits`/`regimes`,`source`=`backtest` ⇒ SL 側基數可查 | 2026-09-27T20:36:30+08:00 |
| `/api/strategies/layers` | 200 | L1 1／L2 2／L3 2／L4 4／L5 3,**total 12**(與 SK-24 的「無 RL 層」對照) | 2026-09-27T20:36:30+08:00 |
| `/api/dashboard/agent-observatory` | 200 | 5 scorecards:`is_sharpe` 0.072～0.249、`oos_sharpe` 全負(含哨兵 -2.4e15)、**5/5 `overfit_warning=true`、0/5 顯著** | 2026-09-27T20:33:47+08:00 |
| `/api/experiment/history` ／ `/api/experiment/diff` | 200／**400／404** | history `[]`;裸 GET `experiment_id required`;不存在 id `experiment result not found` ⇒ diff 報告今日不可產 | 2026-09-27T20:34:20+08:00 |
| `go test ./internal/eval/ -count=1 -v` | 0 | **72 PASS／0 FAIL**(0.3 s);含 7 個 `TestCheckSLRLAlignment_*`(PerfectAlignment／HighR2LowSharpe／HighR2NegativeRankCorrelation／LowR2LowSharpe／ModerateMismatch／EmptyInputs／LengthMismatch) | 2026-09-27T20:36+08:00 |
| 源碼 `git grep CheckSLRLAlignment` | — | 只命中 `doc.go`／`mismatch.go`／`mismatch_test.go` ⇒ **0 生產呼叫者**(有函式、無端點) | 2026-09-27T20:36+08:00 |

**更正（2026-09-27）**

1. Step 3 的 `risk_get_metrics` **不提供 Sharpe**(今日 payload 無此欄位)⇒ SL/RL 的 Sharpe 對比只能走 `/api/dashboard/agent-observatory`,且今日該端點 5/5 overfit、0/5 顯著。
2. SL 對比基準(2026-08-01 的 sharpe_long 0.27／sharpe_short 0.49)**今日不可重現**:`/api/backtest/signals` 全 0/null(同上 SK-32、SK-28 的觀測)。
3. 「atlas 提供三件套 ⇒ 對位完整」只對 SL 側成立:**RL 側整條不存在**(SK-24),`experiment_diff` 今日亦無資料 ⇒ SL vs RL 對比在 atlas 內**今日不可執行**。
4. **atlas 端唯一的 SL/RL 原生介面是檢定函式不是端點**:`internal/eval/mismatch.go` 的 `CheckSLRLAlignment(yTrue, yPred, dailyReturns)` 回 `mismatch_detected/prediction_r2/trading_sharpe/rank_correlation/severity/diagnosis`,7 個測試釘住行為,但 `git grep` 顯示 0 生產呼叫者 ⇒ 要當 SL/RL 的「對齊度證據」必須先在 atlas-go 側接線。

## 未消化 / 待補
- [ ] 論文結論 RL 勝出的具體條件(訓練步數、reward 函數、樣本量)需記錄,讓散戶知道「這個結論的 valid scope」。
- [ ] 跨策略對比的「公平性」:SL 與 RL 的訓練成本差異 100x,單看 Sharpe 不夠,需把「算力成本」列入。
- [ ] 與 SK-32 敏感性分析:SL 的 hyperparameter 沒 RL 多,SL 結果更穩定是預期之內。
