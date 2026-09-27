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
verification: 2026-09-27 L3 端點實跑（http_code + timestamp 見 `l3_endpoints_probed`,明細見 §驗證方式）:4 個 HTTP 端點全 200,無一端點提供 NN 訓練或 R²_oos。**更正（2026-09-27）**:原句「atlas 完全沒 ML 訓練層」不成立——atlas repo `internal/ml/` 有原生 ols／pcr／pls／elasticnet／glm-spline／randomforest ＋ `trainer.go`,CLI `-synthetic` 實跑 exit 0;正確敘述是「**原生 ML 層存在,但沒有 NN**」:NN 相關識別字(neural／MLP／hidden_layer／backprop／relu) `git grep` **0 命中**,CLI `-model nn` 被拒(`unknown model "nn"`)。今日本頁唯一可取的是模型層檢查:-model ols R²_OOS +0.9992、-model rf +0.9909(**合成資料＋未固定種子 ⇒ 不可當市場結論**,見 §驗證方式)。歷史:2026-08-02 v0.9 結算跑過 L3 升 active(client 端 sklearn 1.8.0 MLPRegressor(hidden_layer_sizes=(25, 25), early_stopping=True, validation_fraction=0.1),R²_oos=0.1176;論文預期小樣本 NN ≈ ElasticNet 成立,該值為當日快照)。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b3）
l3_endpoints_probed:
  - /api/stock/fundamentals?symbol=2330 → 200（PE 30.19／PB 9.57／DY 1.1;與 2026-07-30 快照逐字相同）（2026-09-27T20:12:12+08:00）
  - /api/stock/technical?symbol=2330&days=10 → 200（close 2475、date 2026-09-24;rsi14／sma20／sma50 皆 0）（2026-09-27T20:12:12+08:00）
  - /api/backtest/signals → 200（active_signals null ⇒ 無 OOS y 可取）（2026-09-27T20:12:12+08:00）
  - /api/dashboard/risk → 200（session_count 210;無 NN／R² 欄位）（2026-09-27T20:12:12+08:00）
  - 源碼代理（無 HTTP 端點）＝ atlas `git grep -i` neural／MLP／hidden_layer／backprop／relu → 0 命中;`ls internal/ml/` ＝ ols／pcr／pls／elasticnet／randomforest／spline／trainer（2026-09-27T20:12:14+08:00）
  - CLI 代理 ＝ `go run ./cmd/backtest-pipeline -synthetic -model nn` → exit 1 被拒;-model ols R²_OOS +0.9992、-model rf +0.9909（2026-09-27T20:12:13+08:00）
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
| NN 訓練 | **原生無 NN**（2026-09-27 `git grep` 0 命中、CLI `-model nn` 被拒）;NN 只能在 client（Keras／sklearn） |
| early stopping | 缺（client 端） |
| 評估 | `risk_get_metrics`（2026-09-27:無 R²／sharpe 欄位,只有 `var_95` 等 risk_snapshot） |

**差異點**:atlas **沒有 NN 訓練層**,所以 NN 只能在 client;**更正（2026-09-27）**:原句「atlas 完全沒 ML 訓練層」不成立——repo 內 `internal/ml/` 有原生 OLS／PCR／PLS／ElasticNet／GLM-spline／RandomForest 與 `trainer.go`（皆不在 MCP／HTTP 面,見 SK-05～10）。**論文的 NN 在台股 OOS 表現**比 RF 差(這是論文的結論,也是金融 ML 的通則)。

**沒有對位的部分**:無原生 NN 端點（NN 識別字 0 命中,2026-09-27 已驗證負面）;無 GPU 訓練支援。

## 散戶解讀
- **G**:用戶問「AI 選股是不是比較準?」 → 不是。在台股月度資料,**神經網路幾乎總是輸 RF/ElasticNet**。AI 強在影像/語音,不是表格資料。
- **+E**:**散戶最常被「AI 選股」話術騙**——任何宣稱神經網路打敗 Fama-French 的研究,極高比例是過擬合或資料偷看。 [2026-08-22 驗證:99% 無來源,弱化為定性描述]
- 對位 ATLAS_METHODOLOGY 七時期:NN 在 regime 切換時幾乎一定要重訓,線性模型則較穩。

## 驗證方式
Step 1: 拉 18 欄 X,從 `backtest_signals` 拿 y,train/valid/test 6:2:2 切。
> ⚠️ 本 Step 用隨機切分僅為演示 API；正式評估必走 SK-03 滾動時序切分,隨機切分在時間序列有前視洩漏 [2026-08-22 audit-fix]
Step 2: client 端 `Sequential([Dense(25, activation='relu'), Dense(25), Dense(1)])` + `EarlyStopping(patience=5)`。
Step 3: 對比 SK-10 RF 與 SK-05 OLS 的 OOS R²(預期 NN ≈ OLS < RF,若 NN > RF 需審視過擬合風險)。

### L3 端點實跑 + 源碼／CLI 代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19／PB 9.57／DY 1.1（與 2026-07-30 逐字相同 → 靜態快照） | 2026-09-27T20:12:12+08:00 |
| 2 | `/api/stock/technical?symbol=2330&days=10` | 200 | close 2475、date 2026-09-24;`rsi14`／`sma20`／`sma50` 皆 0 | 2026-09-27T20:12:12+08:00 |
| 3 | `/api/backtest/signals` | 200 | `active_signals` null ⇒ 無 OOS y 可取 | 2026-09-27T20:12:12+08:00 |
| 4 | `/api/dashboard/risk` | 200 | session_count 210;無 NN／R² 欄位 | 2026-09-27T20:12:12+08:00 |
| 5 | 源碼代理（無 HTTP 端點）:NN 識別字 `git grep -i` | **0 命中** | neural／MLP／hidden_layer／backprop／relu 皆無 → 原生 NN **已驗證負面** | 2026-09-27T20:12:14+08:00 |
| 6 | 源碼代理:`ls internal/ml/` | — | ols／pcr／pls／elasticnet／randomforest／spline ＋ `trainer.go` → **原生 ML 層存在** | 2026-09-27T20:12:14+08:00 |
| 7 | CLI 代理:`-synthetic -model nn` | **exit 1** | `unknown model "nn"; choose: ols, pcr, pls, elasticnet, glm, rf` | 2026-09-27T20:12:13+08:00 |
| 8 | CLI 代理:同指令 `-model ols` / `-model rf` | exit 0 | R²_OOS **+0.9992** / **+0.9909**（模型層檢查,非市場結論） | 2026-09-27T20:12:13+08:00 |

- **更正（2026-09-27）**:第 5／6／7 列合起來推翻原句「atlas 完全沒 ML 訓練層」。正確講法:atlas 有**原生非 NN 的 ML 層**,但**沒有 NN**。
- **不可當市場結論（合成路徑的兩個坑）**:`-synthetic` 用 500×2 合成線性資料,其 `R²_OOS` 實為**對同一批 `X` 的擬合分數**（原始碼是 `model.Fit(X, y)` 後 `Predict(X)`）,且 `math/rand` **未固定種子** ⇒ 同日重跑 rf 得 +0.9909／+0.9919／+0.9920／+0.9928。此欄只能證明「模型路徑可跑」,末位數字不可跨日比較。
- 本頁 `R²_oos=0.1176` 維持 2026-08-02 client 端 sklearn 快照;atlas 端今日**無任何**可複驗 NN 的端點。

## 未消化 / 待補
- [ ] batch_size=10000 在台股月度資料(數千樣本)下等於全批次,實際訓練動態需驗證。
- [ ] 與 SK-26 LSTM/Transformer 差別:SK-11 是 MLP,SK-26 是序列模型,後者對時間序列更適合。
- [ ] Huber loss 對 NN 訓練穩定性的影響需實測。

> **2026-09-27 補充**:本段三項今日皆**未能由 atlas 端量測**（atlas 無 NN 實作可跑,見 §驗證方式）,故全部維持未消化;本頁今日新增的是 NN 側的**已驗證負面**（識別字 0 命中＋CLI 拒收）。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Neural Network 深度學習需對位 regime 切換下的泛化)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)