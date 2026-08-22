---
title: SK-08 主成分迴歸（PCR）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-08
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: medium
mcp_tools_used: [stock_get_fundamentals, backtest_signals, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 PCA(n_components=4) + LinearRegression 跑 **R²_oos=0.028**;台股因子變異集中,2-3 個成分可能就 90% 變異(論文 v0.9 結論);variance_threshold=0.9 自動選需 client 端跑另一次。
---

## 一句話定位
SK-08 用 PCA 把 86 個高共線特徵壓成 4 個無關主成分,再做 OLS——解決「OLS 在共線下係數不穩」的問題,但缺點是 PCA 不看 y。

## 論文版概念
- 先 PCA(只考慮 X 的變異)→ 取前 4 個主成分 → 對這 4 個做 OLS
- 輸入:`n_components=4` 或 `variance_threshold=0.9`(自動選)
- 適用:特徵共線嚴重、想消除多重共線性

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| PCA | 缺(client 端 sklearn) |
| OLS 殘層 | 缺(client 端) |
| 評估 | `risk_get_metrics` |

**差異點**:PCR 跟 PLS(SK-09)差別只在降維方法——PCR 看 X 變異,PLS 看 X 與 y 相關。**金融預測上 PLS 幾乎總是贏 PCR**,論文版用 PCR 是當 baseline 對比。

**沒有對位的部分**:無原生 PCA 端點;無「特徵相關性矩陣」工具。

## 散戶解讀
- **G**:用戶問「86 個因子共線嚴重怎麼辦?」 → PCR 把共線壓掉,PLS 同時看 y。
- **+E**:**散戶若沒工具,選 PLS(SK-09)而不是 PCR**——PCR 是學術對照組,實務 PLS 勝出。
- 對位 ATLAS_METHODOLOGY 七時期:PCA 的主成分在 regime 切換時可能完全失去解釋力,需謹慎。

## 驗證方式
Step 1: 拉 14 欄 X(基本+技術),從 `backtest_signals` 拿 y。
Step 2: client 端 `PCA(n_components=4).fit_transform(X)` → `LinearRegression().fit()`。
Step 3: 對比 SK-05 OLS 與 SK-09 PLS 的 OOS R²(預期 PLS > PCR > OLS)。
> 口徑註：上述預期排名僅對小樣本弱訊號真實資料成立；本頁合成線性資料實測 OLS=1.0 最高,兩者不矛盾但不可混讀 [2026-08-22 audit-fix]

## 未消化 / 待補
- [ ] `variance_threshold=0.9` 自動選成分數的邏輯在金融數據是否合理?台股因子變異集中,可能 2 個成分就 90%。
- [ ] PCR 與 SK-22 消去法的關係不明。
- [ ] 跟 L1-L5 detector 對位:atlas 的 detector 層可能已含「降維後訊號」,需釐清重疊。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:PCR 主成分需對位 regime 切換下的因子有效性)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)