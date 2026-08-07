---
title: SK-22 消去法（排除特定因子集）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-22
ingested_at: 2026-08-01
last_updated: 2026-08-07
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [experiment_diff, experiment_history, universe_get_universe_overlap, backtest_signals]
verification: 2026-08-07 L3 四步全綠升 active。舊 blocker「atlas 未暴露 experiment_list」為誤判——`/api/experiment/history` 200 回 18 筆真 experiment_id;400 根因是參數名(`id=` → 400,`experiment_id=` → 200)。實驗級 metric delta ✅(sharpe_like 0.00507→0.00642);by-factor 仍 ❌(結構性缺口)。
---

## 一句話定位 + 讀者分流

**一句話**:SK-22 在 atlas 是「**因子對策略的邊際貢獻驗證**」對位——拿掉某因子看策略績效掉多少。

**重要結論**:atlas 端**無原生 ablation / drop_percentage 工具**(2026-08-02 開發 agent 報告 v2 §C「不新增」)。

**讀者分流**:散戶讀 §散戶解讀 + §Darwinian;開發者讀 §atlas 對位;內部 audit 讀 §驗證方式 + §未消化。

**散戶路徑**:「拿掉某因子看 drop」→ ❌ atlas 沒工具 → 走 §Darwinian(7 天連跑偏硬);「策略為什麼失效」→ §Darwinian Step 3 跨 regime 觀察。

---

## 散戶解讀（GROW+ 引用點）

- **G 段(目標)**:用戶問「這個策略真的有效嗎?」→ 反問「拿掉某個因子,績效會不會掉?」→ 這就是 ablation 對位
- **R 段(現狀)**:實驗級 metric delta 現可用(`experiment_diff` 含 baseline/candidate 數值);by-factor ablation **不提供**,要走 §Darwinian 或 PnL FactorAttribution 描述性歸因
- **+E 段(風險)**:**核心警示**——「實驗級 delta 不等於 factor alpha」。單 prompt mutation 的 delta 可能由 confounding 因子造成,要分 regime 看。散戶最常犯「一次回測掉很少就以為該因子不重要」——這是 ablation 誤讀的典型陷阱
- 對位 ATLAS_METHODOLOGY 七時期:消去法是「驗證 regime 切換下哪些因子失效」的工具——RISK_OFF 期間動量因子的 drop 遠大於 RISK_ON,這是散戶教科書看不到的落差

---

## Darwinian-ablation 替代方案（by-factor ablation 不提供時的散戶實務路徑）

**前提**:atlas 不提供 by-factor drop_percentage 端點(開發 agent 報告 v2 §C 必要性為否)。散戶要觀察「策略何時失效」,只能走 Darwinian 多輪 + 跨 regime 對照,**這不是嚴格 ablation,但最接近**:

| Step | 工具 | 看什麼 | 散戶解讀 |
|------|------|--------|---------|
| 1 觀察期 | `strategy_ranker` | 12 條 strategies 的 `tier` + `score` + `win_rate` + `sharpe_ratio` + `alpha_score` | `tier` = Darwinian 生命週期(premium 已多次驗證 / free 觀察中,`sample_days=0` = 尚未被 market 驗證) |
| 2 驗證期 | `strategy_ranker` 跨 7 天連跑 5 次 | 特定 strategy 的 `alpha_score` 演化(例 usd-twd-32-managed-float 264.0 vs dxy-weak-us10y-down 0) | 高 alpha 掉到 0 = **支撐該 strategy 的環境條件變了**,即 by-factor ablation 的近似觀察 |
| 3 歸因期 | `regime_get_history` 拉 30 天 | 當期 regime(BULL/BEAR/HIGH_VOL)vs strategy rank 變化 | strategy 在 RISK_OFF 期間 rank 急降 = 「該 strategy 依賴的因子在熊市失效」的間接證據 |

**SOP**:觀察期 → 驗證期 → 歸因期。**已知不可達**:嚴格排除某因子看 delta、跨 fold 交叉驗證、per-symbol factor score——皆需自帶資料 + client 端 sklearn/pytorch ablation。

完整 `experiment_diff` 5 行卡見 [`_atlas-endpoint-cards/experiment-diff.md`](_atlas-endpoint-cards/experiment-diff.md)。

---

## [INTERNAL] atlas 對位（PR #1443 後修正）

**對位結論**(兩層分開看):
- **實驗級 metric delta**:PR #1443 (commit 383a48b8) 後補回 `acceptance_metric` / `baseline_value` / `candidate_value`。對位 ❌ → ✅。**2026-08-07 更正**:`eval_metrics` 經 18/18 實跑證實不存在,原「若存在則加 R²OOS / Sharpe / CumReturn / MaxDD」為未驗證推測。
- **by-factor 排除式邊際貢獻**:**不提供**——無 ablation 端點、無 per-symbol factor score、audit log 無 `excluded_fields`(2026-08-07 18/18 再確認)。維持 ❌

### 真實對位表（壓縮版）

| 論文概念 | atlas 對位 | 工具 |
|---------|-----------|------|
| by-factor drop_percentage | ❌ 無 ablation 端點 | — |
| excluded_fields metadata | ❌ audit log 無 | experiment_history |
| 實驗級 baseline vs candidate | ✅ PR #1443 後 | experiment_diff |
| 因子集 overlap 評估 | ✅ partial | universe_get_universe_overlap |
| backtest aggregate metric | ✅ partial(無 by-factor) | backtest_signals |

### 論文 vs atlas 關鍵差異

- **論文**同模型內換 X 算 R² drop / **atlas** experiment_diff 換 prompt,judge 對 baseline/candidate scalar 對比
- **PR #1443 翻轉範圍**僅實驗級 prompt mutation delta(by-factor / excluded_fields / recursive elimination / cross-validation fold 平均**未翻轉**)

### 沒有對位的部分（壓縮版）

| 論文概念 | 替代路徑 |
|---------|---------|
| by-factor drop_percentage | pnl-attribution / 自帶資料 |
| recursive elimination | Darwinian 多輪 + judge |
| cross-validation fold 平均 | universe_get_sessions 跨期平均 |
| 與 SK-18 因子 Alpha 關係 | 合併為「因子有效性驗證」組合 skill(待立) |

---

## [INTERNAL] 驗證方式（2026-08-07 L3 四步全綠）

| Step | 端點 | 真實回傳（2026-08-07） |
|------|------|---------|
| 1 | `experiment_history` `GET /api/experiment/history` | **200**,18 條;欄位 experiment_id / mutation_type / promoted_at / status / target_agent_id / target_skill / version。**18/18 無 excluded_fields** |
| 2 | `experiment_diff` `?experiment_id=exec-growth-momentum-01-1775435882` | **200**,acceptance_metric=sharpe_like,baseline=**0.0050727**,candidate=**0.0064193**,skill=growth_momentum + 兩份 prompt。**18/18 無 `eval_metrics`** |
| 3 | `universe_get_universe_overlap` `GET /api/dashboard/universe-overlap` | **200**,29 agents / 29 matrix rows / **86 warnings**(例 semi-desk-01 ↔ super-dru-01 3 檔)。舊記 78 為過時快照 |
| 4 | `backtest_signals` `GET /api/backtest/signals` | **200**,CIRCUIT_BREAKER,drawdown 0.7220,sharpe_long 0.2689,sharpe_short 0.4936,var_95 -0.0225,var_99 -0.0723 |

**⚠️ 參數名陷阱(根因)**:`?id=` 回 `400 experiment_id required`,`?experiment_id=` 回 200。2026-08-02 記的「需等 atlas 暴露 experiment_list」**是誤判**——端點一直在,錯在呼叫方傳 session_id / agent_id。**教訓**:400 訊息若明寫欄位名,先試該欄位名再宣告端點缺失。

---

## [INTERNAL] 論文版概念（忠實還原來源）

- **輸入**:X(特徵矩陣) + y(目標) + model_constructor + excluded_factors
- **動作**:用完整 X 訓練 → 評估 → 從 X 刪除 excluded_factors → 重訓 → 評估 → 計算 drop_percentage = (full − reduced) / full × 100%
- **輸出 JSON**:{full_model_performance, reduced_model_performance, drop_percentage}
- **預設**:excluded_factors=["mom12m", "mom1m"] 排除動量

**論文未提但實務重要**:多輪消去(recursive elimination)、交叉驗證下平均 drop、是否控制其他因子後單獨拿掉。

---

## [INTERNAL] 未消化 / 待補

- [x] experiment_diff 實際回傳欄位 + PR #1443 後 ✅
- [x] experiment_history 18 條全部無 excluded_fields metadata
- [x] pnl-attribution 描述性歸因作為 by-factor ablation 替代
- [x] 散戶實務替代方案(Darwinian-ablation 段完成,L3 實跑 strategy_ranker 數據支撐)
- [x] **(2026-08-07 解除)** 舊 blocker「需等 atlas 暴露 experiment_list」= 誤判;`/api/experiment/history` 一直可用,400 根因為參數名 `id=` vs `experiment_id=`
- [x] **(2026-08-07 證偽)** `eval_metrics` 欄位:18/18 experiment 均無,2026-08-02 「若存在則加」為未驗證推測
- [ ] 與 SK-18 因子 Alpha 的關係:合併為「因子有效性驗證」組合 skill(待立)
- [ ] atlas parameters_get_metadata 是否支援 user-defined excluded_fields——已實跑 ~200 個 parameter 無 excluded_factors 類欄位,需走 experiment_promote 註冊 candidate
- [ ] 沒有「交叉驗證下平均 drop」對位——experiment_diff 只回 1 個 experiment_id,跨期平均不可用
- [ ] by-factor 排除式邊際貢獻仍 ❌:此為**結構性缺口**(atlas 無 ablation 端點),非參數問題,不會因再試參數名而翻轉

---

## [ARCHIVED] 修訂記錄（壓縮版）

- **v1–v2 2026-08-01/02**:初版誤把 experiment_diff 當「實驗級 ablation 給 drop_percentage」;L3 實跑後改寫為 prompt diff(T3-A55~58)。
- **v3–v4 2026-08-02**:PR #1443 merge,實驗級 delta 翻 ✅、by-factor 仍 ❌;重構讀者分流三層。
- **v5 2026-08-07(本版)**:L3 四步全綠升 **active**。解除誤判 blocker(experiment_list 不缺,錯在參數名);證偽 `eval_metrics`(18/18 無);warnings 78 → 86。
