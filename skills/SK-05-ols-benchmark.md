---
title: SK-05 OLS 基準線性模型
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-05
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, backtest_signals, risk_get_metrics]
verification: 2026-09-27 L3 端點實跑 (http_code + timestamp 見 `l3_endpoints_probed`;明細見 §驗證方式):4 個 HTTP 端點全 200,但**皆無 R²_oos 欄位** → 頁內 `R²_oos ∈ [-0.05, 0.10]` 的猜測範圍**今日仍無法由 atlas 驗證**（且 `field-contract` 2262 欄中 r2/r_squared 0 命中）;(2) **atlas 原生 OLS 可實跑（CLI 代理驗證）**:`go run ./cmd/backtest-pipeline -synthetic -model ols` 2026-09-27T19:30:33+08:00 exit 0 → 500 samples × 2 features、True β [2.00, 3.00]、**R²_OOS = +0.9993（PASS,R²>0.9）**;此結果獨立複現本頁「合成線性資料 R²≈1.0 不代表真實台股」的註記,並更正「OLS 在 atlas 端沒原生訓練」——repo 內有原生 OLS 基準（`cmd/backtest-pipeline` 支援 `-model ols/pcr/pls/elasticnet/glm/rf`）,只是不在 MCP／HTTP 面。歷史:2026-08-02 v0.9 結算跑過 L3 升 active（client 端 sklearn 1.8.0 LinearRegression 跑 make_regression）。**2026-09-27 更正（本批發現）**：CLI `-synthetic` 印出的 `R²_OOS` **實為 in-sample**——`cmd/backtest-pipeline/main.go` 的 `runSynthetic` 對**同一份 X** 先 `Fit` 後 `Predict`（第 ~382–388 行），且 `rand.Float64()` 未設 seed ⇒ 同日重跑值即變動（rf +0.9909～+0.9928 實測）。⇒ 此列只能當「模型可跑」的存在性檢查，**不可當 OOS 證據**。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b1）
l3_endpoints_probed:
  - "/api/stock/fundamentals?symbol=2330 → 200（PE 30.19/PB 9.57/DY 1.1,X 來源）（2026-09-27T19:27:52+08:00）"
  - "/api/backtest/signals → 200（active_signals null，無 OOS y）（2026-09-27T19:27:54+08:00）"
  - "/api/dashboard/risk → 200（session_count 210；無 R² 欄位）（2026-09-27T19:27:54+08:00）"
  - "/api/field-contract → 200（2262 欄；r2/r_squared 0 命中）（2026-09-27T19:27:52+08:00）"
  - "/api/parameters → 200（`experiment.oos_window_days`=30、`experiment.walk_forward_embargo_days`=5）（2026-09-27T19:27:54+08:00）"
  - "CLI 代理（無 HTTP 端點）: go run ./cmd/backtest-pipeline -synthetic -model ols → R²_OOS +0.9993（實為 in-sample,非 OOS）（2026-09-27T19:30:33+08:00）"

---

> 口徑註：R²_oos ∈ [-0.05, 0.10] 為未實證之猜測範圍（2026-08-22:backend :18080 未通,無法以 backtest_signals 實跑;合成線性資料 OLS R²=1.0 不代表真實台股）。**2026-09-27 複驗:backend 通了、4 端點全 200,但沒有任何端點回 R²_oos（`field-contract` 2262 欄中 r2/r_squared 0 命中）→ 範圍維持猜測標註,只能由 client 端回測確認。** [2026-08-22 驗證;2026-09-27 複驗]

## 一句話定位
SK-05 是其他所有模型(SK-06~11)的比較基準——沒跑過 OLS 就說「我的模型好」等於沒對照組。

## 論文版概念
- 標準 OLS 回歸,支援兩種 spec:`'all'`(全部因子)或 `'three_factors'`(只 log_mve_ff + log_bm + mom12m,即 Fama-French 三因子)
- 去除 NaN → sklearn LinearRegression 擬合 → 返回 coef_, intercept_, predict()

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 三因子(mve, bm, mom) | `stock_get_fundamentals`(PB,市值)+ `stock_get_technical`(SMA) |
| 訓練 | MCP 缺（client 端 sklearn）;**repo 內有原生 OLS**:`cmd/backtest-pipeline -model ols`（2026-09-27 實跑） |
| 評估 | `risk_get_metrics` |
| 對比基準 | OLS 是所有 ML 模型的「地板線」,務必先跑 |

**差異點**:OLS 在 atlas 端沒原生訓練,必須 client 端跑;但 atlas 提供 X 與 y 端點已經足夠組裝。**OLS 在高維(86 因子)下會 overfit,SK-06~11 都是為了解決這問題**。

**沒有對位的部分**:無原生 OLS / LinearRegression 端點。

## 散戶解讀
- **G**:用戶問「我的策略好不好?」 → 先跑 OLS 基準,任何模型 Sharpe < OLS 該被丟掉。
- **+E**:**OLS 在台股會被 Fama-French 三因子解釋掉大部分 alpha**,散戶看到的「神奇策略」多數只是押對因子,非真 alpha。**這是散戶最該學的第一課**。
- 對位 ATLAS_METHODOLOGY 七時期:OLS 的係數穩定性在 regime 切換時崩壞,SK-22 消去法正是要驗這件事。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` 拉 6 欄 X,從 `backtest_signals` 拿 OOS y。**2026-09-27 實測:X 端點可用（2330 PE/PB/DY）,但 `backtest_signals` 今日回 `active_signals: null` 且全 0 → 沒有 OOS y 可取,Step 1 今日只完成一半。**
Step 2: client 端跑 `LinearRegression().fit(X_train, y_train)`,predict X_test。
Step 3: 對比 `risk_get_metrics` 給的 R²,確認 OLS R²_oos 範圍在 -0.05 ~ 0.10(對台股合理);若 < 0 屬於正常(預測難度大)。**2026-09-27 實測:`/api/dashboard/risk` 回 `degraded/gate_mode/risk_snapshot/session_count/source/var_gate`,**沒有 R² 欄位** → 本步驟不可由 atlas 完成;`/api/parameters` 可讀到 `experiment.oos_window_days=30`、`experiment.walk_forward_embargo_days=5`（OOS 窗長與 embargo 的既有設定,可作為 client 端切分的對位依據）。**

### L3 端點實跑 + CLI 代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19 / PB 9.57 / DY 1.1 | 2026-09-27T19:27:52+08:00 |
| 2 | `/api/backtest/signals` | 200 | active_signals null，全 0 | 2026-09-27T19:27:54+08:00 |
| 3 | `/api/dashboard/risk` | 200 | session_count 210；無 R² 欄位 | 2026-09-27T19:27:54+08:00 |
| 4 | `/api/field-contract` | 200 | 2262 欄；r2 / r_squared 0 命中 | 2026-09-27T19:27:52+08:00 |
| 5 | `/api/parameters` | 200 | `experiment.oos_window_days`=30、`experiment.walk_forward_embargo_days`=5 | 2026-09-27T19:27:54+08:00 |
| 6 | CLI（非 HTTP）:`go run ./cmd/backtest-pipeline -synthetic -model ols` | exit 0 | 500 samples × 2 features，True β [2.00, 3.00]，**R²_OOS +0.9993 → PASS（實為 in-sample,非 OOS）** | 2026-09-27T19:30:33+08:00 |

- 第 6 列是**本頁唯一新增的模型證據(只證「模型可跑」,非 OOS)**:atlas repo 原生就有 OLS 基準（`cmd/backtest-pipeline` 的 `-model` 支援 `ols/pcr/pls/elasticnet/glm/rf`,另有 `-synthetic` 專門驗 β 回收）,輸出格式為 `R²_OOS`。它與本頁 client 端 sklearn 的結論一致（合成線性資料 R²≈1.0）,但該 score 為 in-sample ⇒ 只能當存在性檢查,不可當 OOS 交叉驗證證據。
- 但第 1–5 列證明:**這條路徑不在 MCP／HTTP 面**,MCP 端仍須 client 端自算 R²_oos。

## 未消化 / 待補
- [ ] `spec='three_factors'` 的 Fama-French 在台股的等效因子需驗證(SMB/HML/MOM 是否真有效)。（2026-09-27 實測:`/api/field-contract` 2262 欄中 `smb`/`hml` **0 命中**,只有 `momentum`/`momentum_20d`/`mom_pct` 與 `market`/`market_value` → atlas 端目前只能對位三因子中的 MOM 與 size 代理,無 HML/SMB 欄位）
- [ ] OLS 與 SK-22 消去法的關係:跑完 OLS 看哪些係數顯著,再用 SK-22 驗證刪掉後是否真掉分。
- [ ] OLS 不處理共線性,SK-09 PLS 與 SK-08 PCR 是降維替代方案。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:OLS 基準需對位 7 時期,R² 在不同 regime 表現可能差異大)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)