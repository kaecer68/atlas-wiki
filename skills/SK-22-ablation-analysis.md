---
title: SK-22 消去法（排除特定因子集）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-22
ingested_at: 2026-08-01
last_updated: 2026-09-18
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [experiment_diff, experiment_history, universe_get_universe_overlap, backtest_signals]
verification: L3 四步全綠(2026-08-07),四端點 200。實驗級 metric delta ✅(sharpe_like 0.00507→0.00642);by-factor 排除式邊際貢獻 ❌ 結構性缺口(atlas 無 ablation 端點)。詳見 §驗證方式。
---

## 一句話定位

SK-22 在 atlas 是「**因子對策略的邊際貢獻驗證**」對位——拿掉某因子,看策略績效掉多少。

**重要結論**:atlas 端**無原生 ablation / `drop_percentage` 工具**(2026-08-02 開發 agent 報告 v2 §C 結論「不新增」)。atlas 的等價能力只到「實驗級 prompt mutation 的 metric delta」,**不是** by-factor 排除。

**讀者分流**:散戶讀 §散戶解讀;開發者讀 §atlas 對位;審計讀 §驗證方式 + §未消化。

## 論文版概念（忠實還原 Fin-Skills）

- **輸入**:X(特徵矩陣) + y(目標) + model_constructor + `excluded_factors`
- **動作**:完整 X 訓練 → 評估 → 從 X 刪除 `excluded_factors` → 重訓 → 評估 → 計算 `drop_percentage = (full − reduced) / full × 100%`
- **輸出 JSON**:`{full_model_performance, reduced_model_performance, drop_percentage}`
- **預設**:`excluded_factors = ["mom12m", "mom1m"]`(排除動量)

**論文未提但實務重要**:多輪消去(recursive elimination)、交叉驗證下平均 drop、是否控制其他因子後單獨拿掉。

## atlas 對位

### 對位表

| 論文概念 | atlas 對位 | 工具 |
|---------|-----------|------|
| by-factor `drop_percentage` | ❌ 無 ablation 端點 | — |
| `excluded_fields` metadata | ❌ audit log 無此欄 | experiment_history |
| 實驗級 baseline vs candidate | ✅ PR #1443(383a48b8)後 | experiment_diff |
| 因子集 overlap 評估 | ✅ partial | universe_get_universe_overlap |
| backtest aggregate metric | ✅ partial(無 by-factor) | backtest_signals |

### 論文 vs atlas 關鍵差異

- **論文**:同模型內換 X,算 R² drop。
- **atlas**:`experiment_diff` 換 prompt,judge 對 baseline / candidate 做 scalar 對比。
- **PR #1443 翻轉範圍**僅止於**實驗級 prompt mutation delta**;by-factor / `excluded_fields` / recursive elimination / cross-validation fold 平均**均未翻轉**。

### 沒有對位的部分(替代路徑)

| 論文概念 | 替代路徑 |
|---------|---------|
| by-factor `drop_percentage` | pnl-attribution 描述性歸因 / 自帶資料 |
| recursive elimination | Darwinian 多輪 + judge |
| cross-validation fold 平均 | `universe_get_sessions` 跨期平均 |
| 與 SK-18 因子 Alpha 的關係 | 合併為「因子有效性驗證」組合 skill(待立,見 §未消化) |

## 散戶解讀（GROW+ 引用點）

- **G 段(目標)**:用戶問「這個策略真的有效嗎?」→ 反問「拿掉某個因子,績效會不會掉?」→ 這就是 ablation 對位。
- **R 段(現狀)**:實驗級 metric delta 可用(`experiment_diff` 含 baseline / candidate 數值);**by-factor ablation 不提供**,要走下方替代路徑或 PnL FactorAttribution 描述性歸因。
- **+E 段(風險)**:**核心警示——「實驗級 delta 不等於 factor alpha」**。單 prompt mutation 的 delta 可能由 confounding 因子造成,必須分 regime 看。散戶最常犯「一次回測掉很少就以為該因子不重要」,這是 ablation 誤讀的典型陷阱。
- **對位 ATLAS_METHODOLOGY 七時期**:消去法是「驗證 regime 切換下哪些因子失效」的工具——RISK_OFF 期間動量因子的 drop 遠大於 RISK_ON,這是散戶教科書看不到的落差。

### 替代路徑:Darwinian-ablation(by-factor 不提供時的散戶實務做法)

**前提**:atlas 不提供 by-factor `drop_percentage` 端點。散戶要觀察「策略何時失效」,只能走 Darwinian 多輪 + 跨 regime 對照——**這不是嚴格 ablation,但是最接近的實務近似**。

| Step | 工具 | 看什麼 | 散戶解讀 |
|------|------|--------|---------|
| 1 觀察期 | `strategy_ranker` | 12 條 strategies 的 `tier` / `score` / `win_rate` / `sharpe_ratio` / `alpha_score` | `tier` = Darwinian 生命週期(premium 已多次驗證 / free 觀察中;`sample_days=0` = 尚未被 market 驗證) |
| 2 驗證期 | `strategy_ranker` 跨 7 天連跑 5 次 | 特定 strategy 的 `alpha_score` 演化(例 usd-twd-32-managed-float 264.0 vs dxy-weak-us10y-down 0) | 高 alpha 掉到 0 = **支撐該 strategy 的環境條件變了**,即 by-factor ablation 的近似觀察 |
| 3 歸因期 | `regime_get_history` 拉 30 天 | 當期 regime(BULL / BEAR / HIGH_VOL)vs strategy rank 變化 | strategy 在 RISK_OFF 期間 rank 急降 = 「該 strategy 依賴的因子在熊市失效」的間接證據 |

**SOP**:觀察期 → 驗證期 → 歸因期。**已知不可達**:嚴格排除某因子看 delta、跨 fold 交叉驗證、per-symbol factor score——皆需自帶資料 + client 端 sklearn / pytorch ablation。

## 驗證方式（2026-08-07 L3 四步全綠）

| Step | 端點 | 回傳重點(2026-08-07 實跑) |
|------|------|--------------------------|
| 1 | `experiment_history`(GET `/api/experiment/history`) | **200**,18 條;欄位 experiment_id / mutation_type / promoted_at / status / target_agent_id / target_skill / version。**18/18 無 `excluded_fields`** |
| 2 | `experiment_diff`(`?experiment_id=exec-growth-momentum-01-1775435882`) | **200**,acceptance_metric=sharpe_like,`baseline_value`=**0.0050727**,`candidate_value`=**0.0064193**,skill=growth_momentum。**18/18 無 `eval_metrics`** |
| 3 | `universe_get_universe_overlap`(GET `/api/dashboard/universe-overlap`) | **200**,29 agents / 29 matrix rows / **86 warnings** |
| 4 | `backtest_signals`(GET `/api/backtest/signals`) | **200**,CIRCUIT_BREAKER,drawdown 0.7220,sharpe_long 0.2689,sharpe_short 0.4936,var_95 -0.0225,var_99 -0.0723 |

逐欄位回傳明細與 5 步走法見 [`_atlas-endpoint-cards/experiment-diff.md`](_atlas-endpoint-cards/experiment-diff.md)。

**⚠️ 參數名陷阱(根因)**:`?id=` 回 `400 experiment_id required`;`?experiment_id=` 回 200。**教訓**:400 訊息若明寫欄位名,先試該欄位名,再宣告端點缺失(當初即誤傳 `session_id` / `agent_id`,應傳 `experiment_id`)——「等 atlas 暴露 experiment_list」的舊 blocker 即此誤判(端點一直在)。

## 未消化 / 待補

- [ ] 與 SK-18 因子 Alpha 的關係:合併為「因子有效性驗證」組合 skill(待立)
- [ ] `parameters_get_metadata` 是否支援 user-defined `excluded_fields`:已實跑 ~200 個 parameter 無 `excluded_factors` 類欄位,需走 `experiment_promote` 註冊 candidate
- [ ] 「交叉驗證下平均 drop」無對位:`experiment_diff` 只回 1 個 `experiment_id`,跨期平均不可用
- [ ] by-factor 排除式邊際貢獻仍 ❌:此為**結構性缺口**(atlas 無 ablation 端點),非參數問題,不會因再試參數名而翻轉
- [ ] pnl-attribution 描述性歸因作為 by-factor 替代,尚未寫成獨立 SK(目前僅本頁 §散戶解讀 替代路徑)
