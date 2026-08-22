---
title: SK-06 彈性網正則化模型
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-06
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, backtest_signals, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 ElasticNetCV(l1_ratio=[0.1,0.5,0.9]) 跑 R²_oos=0.9996(L1+L2 正則化對線性資料接近完美);use_huber=True 在 client 端需自訂(無 sklearn 原生 huber-elasticnet),仍待驗證;l1_ratio=0.5 為平衡點,alpha 由 CV 自動選。
---

## 一句話定位
SK-06 是 OLS 的高維修正版——L1+L2 混合正則化,把不重要因子的係數壓到接近 0,解決「86 個因子但只有 60 個月樣本」的高維小樣本問題。
> 口徑註：本頁 60/12 個月指滾動切割後單一 window 內月數；全樣本為 336 月（1994-01~2022-04,SK-01）[2026-08-22 audit-fix]

## 論文版概念
- 結合 L1(Lasso,稀疏)+ L2(Ridge,平滑),`l1_ratio=0.5` 是平衡點
- 輸入:`l1_ratio=0.5`、`alpha=None`(自動 CV 選)、`use_huber=True`(與 SK-04 整合)
- 動作:標準化 X → CV 選 alpha → ElasticNet 擬合

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| ElasticNet 訓練 | 缺(client 端 sklearn) |
| CV 選 alpha | 缺(client 端 GridSearchCV) |
| 評估 | `risk_get_metrics` |
| 與 SK-04 整合 | Huber ElasticNet 在 client 端即可組合 |

**差異點**:論文版是單純 sklearn 流程,atlas 端需 client 自組;**ElasticNet 的 L1 特性會把 86 個因子自動縮到 ~10-20 個,這與 SK-13 permutation importance 互補——前者看「模型覺得哪些因子有用」,後者看「打亂後掉分多少」**。

**沒有對位的部分**:無原生 ElasticNet 端點。

## 散戶解讀
- **G**:用戶問「86 個因子太多怎麼辦?」 → ElasticNet 是 Lasso + Ridge,自動選重要因子且平滑處理共線。
- **+E**:**`l1_ratio` 選 0.5 是平衡點,但散戶若因子數 << 樣本數,選 0.2(Ridge 為主)更穩**——學術預設不一定是最佳。
- 對位 ATLAS_METHODOLOGY 七時期:ElasticNet 選的因子在 regime 切換時可能完全換一批,**散戶要的是「這個 regime 下 ElasticNet 選哪些」,不是「全期平均 top-10」**。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` + `stock_get_technical` 拉 18 欄 X,從 `backtest_signals` 拿 OOS y。
Step 2: client 端跑 `ElasticNetCV(l1_ratio=[0.1,0.5,0.9], alphas=np.logspace(-4,0,20))`。
Step 3: 對比 SK-05 OLS 與 SK-09 PLS 的 OOS R²,確認 ElasticNet 優於 OLS 但不優於 PLS(預期差距 5-15%)。
> 口徑註：上述預期排名僅對小樣本弱訊號真實資料成立；本頁合成線性資料實測 OLS=1.0 最高,兩者不矛盾但不可混讀 [2026-08-22 audit-fix]

## 未消化 / 待補
- [ ] `alpha` CV 範圍是否足夠?學術建議 logspace(-6, 2, 50)。
- [ ] use_huber=True 對小樣本的影響需實測。
- [ ] ElasticNet 與 SK-22 消去法的因果關係:理論上若 SK-22 顯示某因子刪掉後掉分很多,ElasticNet 應該把該因子的係數保留下來——可交叉驗證。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Elastic Net 正則化需對位 7 時期 × 策略三分類)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)