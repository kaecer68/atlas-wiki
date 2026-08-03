---
title: SK-22 消去法（排除特定因子集）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-22
ingested_at: 2026-08-01
last_updated: 2026-08-02
status: draft
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [experiment_diff, experiment_judge, universe_get_universe_overlap, backtest_signals]
verification: 2026-08-02 L3 實跑確認 atlas 無原生 ablation 端點;PR #1443 (commit 383a48b8) merge 後 `experiment_diff` 補 judge metric 欄位（acceptance_metric / baseline_value / candidate_value / eval_metrics），實驗級 metric delta 翻 ✅（單 experiment 級），factor 級排除式邊際貢獻仍 ❌。
---

## 一句話定位 + 讀者分流（2026-08-02 重構版）

**一句話**:SK-22 在 atlas 是「**因子對策略的邊際貢獻驗證**」對位——拿掉某因子看策略績效掉多少。

**重要結論**:atlas 端**沒有原生 ablation / drop_percentage 工具**(2026-08-02 開發 agent 報告 v2 §C 拍板「不新增」)。

**讀者分流**(2026-08-02 新增):
- **散戶**:讀 §一句話定位(這段)+ §散戶解讀 + §Darwinian-ablation(可選 SOP)
- **開發者**:§atlas 對位(PR #1443 細節)
- **內部 audit**:§論文版概念 + §驗證方式 + §未消化

**散戶路徑**:
- 「拿掉某因子看 drop」→ ❌ atlas 沒工具 → §Darwinian(注意:7 天連跑偏硬,評估可行性)
- 「策略為什麼失效」→ §Darwinian Step 3 跨 regime 觀察
- 純理解概念 → §散戶解讀即可

---

## 散戶解讀（GROW+ 引用點）

- **G 段(目標)**:用戶問「這個策略真的有效嗎?」 → 反問「拿掉某個因子,績效會不會掉?」 → 這就是 ablation 對位
- **R 段(現狀)**:對位 atlas(PR #1443 後)→「實驗級 metric delta 現可用(`experiment_diff` 含 baseline/candidate 數值)。by-factor ablation **不提供**,要走 §Darwinian-ablation 替代方案 或 PnL FactorAttribution 描述性歸因」
- **+E 段(風險)**:**核心警示**——「實驗級 delta 不等於 factor alpha」。單 prompt mutation 帶來的 delta 可能由 confounding 因子造成,要分 regime 看。散戶最常犯「一次回測掉很少就以為該因子不重要」錯誤——這是 ablation 結果誤讀的典型陷阱
- 對位 ATLAS_METHODOLOGY 七時期:消去法是「驗證 regime 切換下哪些因子失效」的工具——RISK_OFF 期間動量因子的 drop 會遠大於 RISK_ON,這是散戶教科書看不到的落差

---

## experiment_diff 端點速查

完整 5 行卡見 [`_atlas-endpoint-cards/experiment-diff.md`](_atlas-endpoint-cards/experiment-diff.md)(2026-08-03 kaecer v6.6 派工對位 wiki 教學)。

---

## Darwinian-ablation 替代方案（by-factor ablation 不提供時的散戶實務路徑）

**前提**:atlas 不提供 by-factor drop_percentage 端點(開發 agent 報告 v2 §C 必要性為否)。散戶要觀察「策略何時失效」,只能走 Darwinian 多輪 + 跨 regime 對照,**這不是嚴格 ablation,但最接近**:

| Step | 工具 | 看什麼 | 散戶解讀 |
|------|------|--------|---------|
| 1 觀察期 | `strategy_ranker` | 12 條 strategies 的 `tier`(premium/registered/free)+ `score` + `win_rate` + `sharpe_ratio` + `alpha_score` | `tier` = Darwinian 驗證生命週期(premium 已多次驗證通過 / free 觀察中,`sample_days=0` 表示尚未被 market 驗證) |
| 2 驗證期 | `strategy_ranker` 跨 7 天連跑 5 次 | 觀察特定 strategy 的 `alpha_score` 演化(例:usd-twd-32-managed-float `alpha_score=264.0` vs dxy-weak-us10y-down `alpha_score=0`) | 高 alpha → 掉到 0,**隱含「支撐該 strategy 的某環境條件變了」**,這是 by-factor ablation 的近似觀察 |
| 3 歸因期 | `regime_get_history` 拉 30 天 | 當期 regime(BULL/BEAR/HIGH_VOL 等)vs strategy rank 變化 | strategy 在 RISK_OFF 期間 rank 急降 = 「該 strategy 依賴的某因子在熊市失效」的間接證據 |

**SOP**:觀察期 → 驗證期 → 歸因期。**已知不可達**:嚴格排除某因子看 delta、跨 fold 交叉驗證、per-symbol factor score——這些都需自帶資料 + client 端 sklearn/pytorch ablation。

---

## [INTERNAL — 開發者用] atlas 對位（2026-08-02 PR #1443 merge 後修正）

> 此段為內部對位 audit,散戶不需讀。

**對位結論**(兩層分開看):
- **實驗級 metric delta**:PR #1443 (commit 383a48b8, 2026-08-02) 後補回 `acceptance_metric` / `baseline_value` / `candidate_value`(若存在則加 `eval_metrics` = R²OOS / Sharpe / CumReturn / MaxDD)。對位 ❌ → ✅
- **by-factor 排除式邊際貢獻**:**不提供**——無 ablation 端點、無 per-symbol factor score 端點、`experiment_history` audit log 仍無 `excluded_fields` metadata。對位維持 ❌

### 真實對位表（壓縮版）

| 論文概念 | atlas 對位 | 工具 |
|---------|-----------|------|
| by-factor drop_percentage | ❌ 無 ablation 端點 | — |
| excluded_fields metadata | ❌ audit log 無 | experiment_history |
| 實驗級 baseline vs candidate | ✅ PR #1443 後 | experiment_diff |
| 因子集 overlap 評估 | ✅ partial | universe_get_universe_overlap |
| backtest aggregate metric | ✅ partial(無 by-factor) | backtest_signals |

### 論文 vs atlas 關鍵差異

- **論文**:同模型內換 X 算 R² drop / **atlas**:experiment_diff 換 prompt,judge 對 baseline/candidate scalar 對比
- **PR #1443 翻轉範圍**:僅實驗級 prompt mutation delta(by-factor / excluded_fields / recursive elimination / cross-validation fold 平均**未翻轉**)
- **factor 級 mission 落差(維持)**:atlas 沒有 1-step by-factor 工具

### 沒有對位的部分（壓縮版）

| 論文概念 | 替代路徑 |
|---------|---------|
| by-factor drop_percentage | pnl-attribution / 自帶資料 |
| recursive elimination | Darwinian 多輪 + judge |
| cross-validation fold 平均 | universe_get_sessions 跨期平均 |
| 與 SK-18 因子 Alpha 關係 | 合併為「因子有效性驗證」組合 skill(待立) |

---

## [INTERNAL — agent audit] 驗證方式（2026-08-02 PR #1443 後）

| Step | 動作 | 真實回傳 |
|------|------|---------|
| 1 | `experiment_history` | 18 條 prompt mutation,無 excluded_fields metadata |
| 2 | `experiment_diff` (experiment_id=`exec-growth-momentum-01-1775435882`) | PR #1443 後:baseline_prompt + candidate_prompt + skill + target_agent_id + acceptance_metric="sharpe_like" + baseline_value=0.00507 + candidate_value=0.00642 + eval_metrics(若存在) |
| 3 | `universe_get_universe_overlap` | 29×28 matrix + 78 warnings |
| 4 | `backtest_signals` | {active_signals:["CIRCUIT_BREAKER"], drawdown_pct:0.72, sharpe_long:0.27, sharpe_short:0.49, var_95:-0.023, var_99:-0.072} |

---

## [INTERNAL — agent audit] 論文版概念（忠實還原來源）

- **輸入**:X(特徵矩陣) + y(目標) + model_constructor + excluded_factors
- **動作**:用完整 X 訓練 → 評估 → 從 X 刪除 excluded_factors → 重訓 → 評估 → 計算 drop_percentage = (full − reduced) / full × 100%
- **輸出 JSON**:{full_model_performance, reduced_model_performance, drop_percentage}
- **預設**:excluded_factors=["mom12m", "mom1m"] 排除動量

**論文未提但實務重要**:多輪消去(recursive elimination)、交叉驗證下平均 drop、是否控制其他因子後單獨拿掉。

---

## [INTERNAL — agent audit] 未消化 / 待補

- [x] experiment_diff 實際回傳欄位 + PR #1443 後 ✅
- [x] experiment_history 18 條全部無 excluded_fields metadata
- [x] pnl-attribution 描述性歸因作為 by-factor ablation 替代
- [x] 散戶實務替代方案(Darwinian-ablation 段完成,L3 實跑 strategy_ranker 數據支撐)
- [ ] 與 SK-18 因子 Alpha 的關係:合併為「因子有效性驗證」組合 skill(待立)
- [ ] atlas parameters_get_metadata 是否支援 user-defined excluded_fields——已實跑 ~200 個 parameter 無 excluded_factors 類欄位,需走 experiment_promote 註冊 candidate
- [ ] 沒有「交叉驗證下平均 drop」對位——experiment_diff 只回 1 個 experiment_id,跨期平均不可用

---

## [ARCHIVED 2026-08-02] 修訂記錄

**v1 / 2026-08-01 初版**:寫對位表,誤把 experiment_diff 寫成「實驗級 ablation,給 metric delta / drop_percentage」——SK-22 對位反轉結論確認**完全錯估**。

**v2 / 2026-08-02 對位反轉**:L3 實跑 4 個端點 → experiment_diff 是 prompt diff 非 ablation → 對位表改寫 + Pitfall 7 三層轉化(L1 SK-22 / L2 _consult-index / L3 governance) + T3-A55/56/57/58。

**v3 / 2026-08-02 PR #1443 merge 後部分翻轉**:實驗級 metric delta 翻 ✅,by-factor 仍 ❌。

**v4 / 2026-08-02 重構版(本版)**:kaecer 拍「SK-22 還需要做什麼,要做就做到正確」→ 檢討發現 wiki 像「內部審計報告」不像「散戶教學文檔」→ 重構為「讀者分流」(散戶 / 開發者 / 內部 audit 三層)+ §散戶解讀 移前 + §Darwinian 段加散戶實務門檻警語 + 內部段標 `[INTERNAL — ...]` + byte 預估 8500-9000B。
