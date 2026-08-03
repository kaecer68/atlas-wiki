---
title: SK-07 廣義線性模型（樣條非線性）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-07
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: low
mcp_tools_used: [stock_get_fundamentals, backtest_signals, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 SplineTransformer(degree=2, knots=[0.25,0.5,0.75]) + Lasso(alpha=0.1) 跑 **R²_oos=0.0745**;**GroupLasso 在 sklearn 沒原生,本輪用 Spline+Lasso 替代**,結果趨勢對位但不等於論文 GroupLasso;U 型捕捉能力需 SHAP/PDP 視覺化確認(已寫進 SK-14 互補)。
---

## 一句話定位
SK-07 引入「非線性」+「群組稀疏」——本益比對報酬的關係可能不是直線(可能是 U 型),SK-07 用樣條捕捉;群組 Lasso 把同因子的多個基函數當一組,避免「只保留某因子的部分基」。

## 論文版概念
- 樣條非線性:對每個數值特徵用 `degree=2` 二次樣條展開,節點 `[0.25, 0.5, 0.75]` 分位數
- Group Lasso:每個原始特徵的基函數為一組,整組進整組出
- 結果:模型可學到「PB 太高/太低都不好,中間最好」這類 U 型關係

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 樣條基函數 | 缺(client 端 sklearn) |
| Group Lasso | 缺(client 端) |
| 特徵來源 | `stock_get_fundamentals` |
| 評估 | `risk_get_metrics` |

**差異點**:atlas 完全沒有「ML 訓練」端點,SK-07 100% client 端責任。**但捕捉非線性在金融預測上極有價值**——散戶常誤信線性關係。

**沒有對位的部分**:無樣條 / Group Lasso 端點;無「非線性視覺化」(SK-14 PDP 需另做)。

## 散戶解讀
- **G**:用戶問「PE 越低越好嗎?」 → 不是。PE 太低可能是夕陽產業,太高可能是成長股,中間有甜蜜點——這就是 U 型,SK-07 學得到。
- **+E**:**散戶最常忽略「U 型關係」**,只看線性係數會錯失甜蜜點,看 permutation importance 又會低估(因為線性切割)。**非線性是金融建模的隱藏 alpha**。
- 對位 ATLAS_METHODOLOGY 七時期:U 型的甜蜜點在 regime 切換時會移動,需每期重訓。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` 拉 8 欄 X(PE/PB/殖利率/市值/營收成長/ROE/負債比/淨利率),從 `backtest_signals` 拿 y。
Step 2: client 端 `SplineTransformer(degree=2, knots=[0.25,0.5,0.75])` + `GroupLasso`。
Step 3: 對比 OLS / ElasticNet 的 OOS R²,確認 SK-07 優於線性模型(預期差距 10-20%)。

## 未消化 / 待補
- [ ] Group Lasso 在 sklearn 沒有原生,需自寫或用 `celer` 套件。
- [ ] 樣條節點位置 [0.25, 0.5, 0.75] 是論文的預設,台股分位可能不同(如 PE 分位高度右偏)。
- [ ] 與 SK-14 PDP 的關係:SK-07 學完後用 SK-14 視覺化「PE vs 預期報酬」曲線,確認 U 型假設。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:GLM Spline 需對位非線性關係跨 regime 表現)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)