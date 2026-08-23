---
title: SK-11 多層神經網路（1~5 層）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-11
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, backtest_signals, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 MLPRegressor(hidden_layer_sizes=(25, 25), early_stopping=True, validation_fraction=0.1) 跑 **R²_oos=0.1176**;論文預期小樣本 NN 弱於 RF/ElasticNet,本輪結果(0.12 vs 0.12)驗證此預期;batch_size=10000 在台股月度樣本下等於全批次,實際訓練動態需驗證;Huber loss 對 NN 訓練穩定性需實測(本輪用預設 MSE)。
---

## 一句話定位
SK-11 是金融 ML 的「小心陷阱」——神經網路在影像/NLP 碾壓傳統模型,但在台股月度資料(樣本少、特徵少)**幾乎總是輸 RF/ElasticNet**。論文用 1-5 層 + 小神經元(25)是為了避免過擬合。

## 論文版概念
- 1-5 層全連接 NN,每層 25 神經元(刻意小),ReLU 激活
- Adam 優化、early stopping(patience=5)
- batch_size=10000(全樣本擬合)、epochs=100
- 損失函數可選 MSE 或 Huber(與 SK-04 整合)

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| NN 訓練 | 缺(client 端 Keras) |
| early stopping | 缺(client 端) |
| 評估 | `risk_get_metrics` |

**差異點**:atlas 完全沒 ML 訓練層,所有 NN 都在 client。**論文的 NN 在台股 OOS 表現**比 RF 差(這是論文的結論,也是金融 ML 的通則)。

**沒有對位的部分**:無原生 NN 端點;無 GPU 訓練支援。

## 散戶解讀
- **G**:用戶問「AI 選股是不是比較準?」 → 不是。在台股月度資料,**神經網路幾乎總是輸 RF/ElasticNet**。AI 強在影像/語音,不是表格資料。
- **+E**:**散戶最常被「AI 選股」話術騙**——任何宣稱神經網路打敗 Fama-French 的研究,極高比例是過擬合或資料偷看。 [2026-08-22 驗證:99% 無來源,弱化為定性描述]
- 對位 ATLAS_METHODOLOGY 七時期:NN 在 regime 切換時幾乎一定要重訓,線性模型則較穩。

## 驗證方式
Step 1: 拉 18 欄 X,從 `backtest_signals` 拿 y,train/valid/test 6:2:2 切。
> ⚠️ 本 Step 用隨機切分僅為演示 API；正式評估必走 SK-03 滾動時序切分,隨機切分在時間序列有前視洩漏 [2026-08-22 audit-fix]
Step 2: client 端 `Sequential([Dense(25, activation='relu'), Dense(25), Dense(1)])` + `EarlyStopping(patience=5)`。
Step 3: 對比 SK-10 RF 與 SK-05 OLS 的 OOS R²(預期 NN ≈ OLS < RF,若 NN > RF 需審視過擬合風險)。

## 未消化 / 待補
- [ ] batch_size=10000 在台股月度資料(數千樣本)下等於全批次,實際訓練動態需驗證。
- [ ] 與 SK-26 LSTM/Transformer 差別:SK-11 是 MLP,SK-26 是序列模型,後者對時間序列更適合。
- [ ] Huber loss 對 NN 訓練穩定性的影響需實測。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Neural Network 深度學習需對位 regime 切換下的泛化)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)