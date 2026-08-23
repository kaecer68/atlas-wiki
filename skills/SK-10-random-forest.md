---
title: SK-10 隨機森林模型
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-10
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, backtest_signals, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 RandomForestRegressor(n_estimators=500, max_depth=2, min_samples_split=5, max_features="sqrt") 跑 **R²_oos=0.1248**;論文用 max_depth=2 故意淺防過擬合(台股月度資料 max_depth=2 偏弱,max_depth=4-5 可能在台股更穩);n_estimators=500 足夠(內部經驗值,提到 1000 不顯著改善 [2026-08-22 驗證]);feature_importances_ 跑通(SK-13 互補)。
---

## 一句話定位
SK-10 是金融 ML 的「萬用 baseline」——非線性、處理共線、給出 importance,但**深度限制很重要**——論文用 max_depth=2 防止過擬合,散戶若設太深會慘輸 OLS。

## 論文版概念
- 集成 500 棵淺決策樹(max_depth=2,min_samples_split=5),bagging + 隨機特徵
- 輸入:`n_estimators=500`、`max_depth=2`、`max_features="sqrt"`
- 優點:非線性、給出 feature_importances_、不需標準化
- 缺點:不外推(訓練範圍外預測為定值)、對樣本少時不穩

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| RF 訓練 | 缺(client 端 sklearn) |
| 特徵來源 | `stock_get_fundamentals` + `stock_get_technical` |
| 評估 | `risk_get_metrics` |
| 重要性 | `experiment_diff` / SK-13 permutation |

**差異點**:RF 給的 feature_importances_ 是「不純度降低」,與 SK-13 permutation importance 不同——前者對高基數特徵有偏。

**沒有對位的部分**:無原生 RF / Gradient Boosting 端點。

## 散戶解讀
- **G**:用戶問「線性模型不夠,我要非線性」 → RF 是起點,XGBoost 是進階。
- **+E**:**`max_depth=2` 是金融特規——散戶若設 5/10,馬上 overfit**;`n_estimators=500` 是穩定而非越多越好。**金融 RF 跟影像 RF 設定完全相反**。
- 對位 ATLAS_METHODOLOGY 七時期:RF 的特徵重要性在 regime 切換時排名會洗牌,需每期重訓。

## 驗證方式
Step 1: 拉 18 欄 X,從 `backtest_signals` 拿 y。
Step 2: client 端 `RandomForestRegressor(n_estimators=500, max_depth=2)`。
Step 3: OOS R² 對比 SK-05 OLS(預期 RF 優 10-20%);同時算 `feature_importances_`,看 top-5 是否包含 SK-13 permutation 認定的 top-5。
> 口徑註：上述預期排名僅對小樣本弱訊號真實資料成立；本頁合成線性資料實測 OLS=1.0 最高,兩者不矛盾但不可混讀 [2026-08-22 audit-fix]

## 未消化 / 待補
- [ ] XGBoost / LightGBM 是否在 atlas 端有對位?論文中沒用,但實務主流。
- [ ] `n_estimators=500` 在台股月度資料是否足夠?可能需 1000。
- [ ] RF 對 regime 切換的適應性比線性差,需監控特徵重要性穩定性。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Random Forest 非線性需對位 regime 切換)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)