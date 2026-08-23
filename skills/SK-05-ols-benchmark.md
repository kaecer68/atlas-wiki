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
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 LinearRegression 跑 make_regression(86 因子×336 樣本),**R²_oos=1.0(完美擬合—OLS 對線性資料可達此值,真實台股會因 noise<0.5 而偏低)**;對位 SK-16 SK-18 已升 active 的 backtest_signals + risk_get_metrics,atlas 端 R²_oos 需 client 端算(SOUL §3.3 誠實標)。
---

> 口徑註：R²_oos ∈ [-0.05, 0.10] 為未實證之猜測範圍（2026-08-22 驗證時 backend :18080 未通,無法以 backtest_signals 實跑;合成線性資料實測 OLS R²=1.0 不代表真實台股,維持猜測標註,需回測確認）[2026-08-22 驗證]

## 一句話定位
SK-05 是其他所有模型(SK-06~11)的比較基準——沒跑過 OLS 就說「我的模型好」等於沒對照組。

## 論文版概念
- 標準 OLS 回歸,支援兩種 spec:`'all'`(全部因子)或 `'three_factors'`(只 log_mve_ff + log_bm + mom12m,即 Fama-French 三因子)
- 去除 NaN → sklearn LinearRegression 擬合 → 返回 coef_, intercept_, predict()

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 三因子(mve, bm, mom) | `stock_get_fundamentals`(PB,市值)+ `stock_get_technical`(SMA) |
| 訓練 | 缺(client 端 sklearn) |
| 評估 | `risk_get_metrics` |
| 對比基準 | OLS 是所有 ML 模型的「地板線」,務必先跑 |

**差異點**:OLS 在 atlas 端沒原生訓練,必須 client 端跑;但 atlas 提供 X 與 y 端點已經足夠組裝。**OLS 在高維(86 因子)下會 overfit,SK-06~11 都是為了解決這問題**。

**沒有對位的部分**:無原生 OLS / LinearRegression 端點。

## 散戶解讀
- **G**:用戶問「我的策略好不好?」 → 先跑 OLS 基準,任何模型 Sharpe < OLS 該被丟掉。
- **+E**:**OLS 在台股會被 Fama-French 三因子解釋掉大部分 alpha**,散戶看到的「神奇策略」多數只是押對因子,非真 alpha。**這是散戶最該學的第一課**。
- 對位 ATLAS_METHODOLOGY 七時期:OLS 的係數穩定性在 regime 切換時崩壞,SK-22 消去法正是要驗這件事。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` 拉 6 欄 X,從 `backtest_signals` 拿 OOS y。
Step 2: client 端跑 `LinearRegression().fit(X_train, y_train)`,predict X_test。
Step 3: 對比 `risk_get_metrics` 給的 R²,確認 OLS R²_oos 範圍在 -0.05 ~ 0.10(對台股合理);若 < 0 屬於正常(預測難度大)。

## 未消化 / 待補
- [ ] `spec='three_factors'` 的 Fama-French 在台股的等效因子需驗證(SMB/HML/MOM 是否真有效)。
- [ ] OLS 與 SK-22 消去法的關係:跑完 OLS 看哪些係數顯著,再用 SK-22 驗證刪掉後是否真掉分。
- [ ] OLS 不處理共線性,SK-09 PLS 與 SK-08 PCR 是降維替代方案。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:OLS 基準需對位 7 時期,R² 在不同 regime 表現可能差異大)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)