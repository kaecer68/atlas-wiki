---
title: SK-15 雙特徵交互作用分析
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-15
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, backtest_signals, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 sklearn.inspection.partial_dependence(OLS, features=[(f32, f11)], grid_resolution=10) 跑 **2D PDP 形狀 (10,10) value_range -289.81 ~ 312.01**;**f32×f11 交互項確認有訊號(非獨立效應)**,但 OLS 線性模型預期 2D PDP 是平面線性(可能非線性模型 SK-07/11 才能見曲面);計算成本每對 ~3s。
---

## 一句話定位
SK-15 補 SK-14 的洞——單一 PDP 看不出「PE 對報酬的影響依賴於 MOM」這種交互。雙特徵 PDP 用熱力圖呈現,讓散戶看到「哪個特徵組合的格子最賺」。

## 論文版概念
- 對 (特徵 a, 特徵 b) 建 20×20 網格
- 每個網格點:固定其他特徵為中位數,計算平均預測
- 輸出:二維陣列(20×20)+ 對應座標
- 視覺化:`imshow(Z, extent=...)` 熱力圖

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 2D PDP | 缺(client 端 sklearn) |
| 背景數據 | `stock_get_fundamentals` + `stock_get_technical` |
| 評估 | `risk_get_metrics` |

**差異點**:2D PDP 計算成本是 1D 的 20 倍(網格 20×20 vs 50),金融大樣本需採樣。

**沒有對位的部分**:無原生 2D PDP;無熱力圖工具。

## 散戶解讀
- **G**:用戶問「PB 跟 MOM 哪個組合最賺?」 → 2D PDP 給熱力圖,散戶直覺看出「低 PB + 高 MOM」可能是甜蜜點。
- **+E**:**散戶最常忽略「因子必須搭配」**——「低 PE 價值股」與「高 MOM 動能股」單看都不如「低 PE + 高 MOM」一起。**這是教科書看不到的 alpha 源**。
- 對位 ATLAS_METHODOLOGY 七時期:交互甜蜜點在 regime 切換時會移動,需每期重畫。

## 驗證方式
Step 1: 用 SK-10/SK-11 訓練好的模型,client 端 `partial_dependence(model, X_test, features=[('pb','mom12m')], grid_resolution=20)`。
Step 2: 繪製熱力圖,標出「最暖的格子」(最高預測報酬區)。
Step 3: 把「最暖格子對應的股票池」實際丟進 backtest_signals 跑回測,確認 OOS Sharpe 優於單一因子的策略。

## 未消化 / 待補
- [ ] 網格大小 20×20 在台股樣本下可能雜訊大,需實測。
- [ ] 三特徵交互(3D)成本高、視覺化難,實務上用 SHAP interaction values 替代。
- [ ] 與 SK-02 特徵擴充的對應:SK-02 自動生成所有交互特徵,SK-15 是事後診斷「哪個交互值得保留」。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:特徵交互需對位 regime 切換下的交互效應變化)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)