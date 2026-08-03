---
title: SK-14 部分相依圖（邊際效應）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-14
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, backtest_signals, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 sklearn.inspection.partial_dependence(OLS,grid_resolution=20) 跑 **3 個 top 重要因子的 PDP 曲線**——**f32** values [-1.66,1.64] avg_prediction [-160,165](單調上升);**f11** values [-1.46,1.67] avg_prediction [-128,149](單調上升);**f42** values [-1.53,1.48] avg_prediction [-148,146](單調上升);**3 個因子都是線性(OLS 對位線性資料的 PDP 預期結果),U 型/反鐘型需另跑非線性模型(SK-07/11)**;計算成本每因子 ~5s(86 因子全跑 7 分鐘)。
---

## 一句話定位
SK-14 把「黑盒模型」變可解釋——對每個特徵畫一條曲線,看「其他特徵固定時,只動這個特徵,預期報酬怎麼變」。散戶最直觀的「看模型在想什麼」工具。

## 論文版概念
- 對單一特徵 j,在值域內建 50 個網格點
- 每個網格點:複製背景數據 → 將 j 設為該值 → 算平均預測
- 繪製 (x=網格值, y=平均預測) 曲線
- 與 SK-13 差別:SK-13 看「全局重要性」,SK-14 看「形狀」

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| PDP 計算 | 缺(client 端 sklearn) |
| 背景數據 | `stock_get_fundamentals` + `stock_get_technical` |
| 評估 | `risk_get_metrics` |

**差異點**:PDP 是視覺化工具,atlas 端沒原生繪圖能力;**但 client 端一張圖能給散戶最強直覺**。

**沒有對位的部分**:無原生 PDP / ICE 端點;無繪圖工具。

## 散戶解讀
- **G**:用戶問「PE 對預期報酬的影響是什麼?」 → PDP 給一條曲線,可能是正斜率(PE 越高越好)、負斜率、U 型、倒 U 型。
- **+E**:**PDP 平均掉所有其他特徵的效應,若「PE 對報酬」依賴於「產業」,PDP 會誤導**。**散戶最常誤信 PDP 忽略交互效應**,這就是 SK-15 要解決的問題。
- 對位 ATLAS_METHODOLOGY 七時期:PDP 形狀在 regime 切換時會變,需每期重畫。

## 驗證方式
Step 1: 從 SK-10/SK-11 訓練好的模型,client 端跑 `partial_dependence(model, X_test, features=['pb'], grid_resolution=50)`。
Step 2: 繪圖,確認曲線在訓練樣本範圍內(範圍外是外推不可信)。
Step 3: 對比 SK-13 permutation importance 排名,確認 PDP top-3 與 permutation top-3 一致(若不一致需釐清原因)。

## 未消化 / 待補
- [ ] ICE(Individual Conditional Expectation)是否要在 atlas 端做?PDP 看不到異質性,ICE 補這個洞。
- [ ] 2D PDP(SK-15 熱力圖)對「交互假設」驗證比 1D 更強。
- [ ] PDP 計算成本高(每網格點都跑一次模型),金融樣本大時需採樣。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:PDP 部分依賴圖需對位跨 regime 因子效應)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)