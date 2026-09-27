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
verification: 2026-09-27 L3 端點實跑（http_code + timestamp 見 `l3_endpoints_probed`,明細見 §驗證方式）:5 個端點全 200。**更正（2026-09-27）:原句「無原生 2D PDP」不成立**——atlas repo `internal/eval/interaction.go` 有原生 `FriedmanH`（1D 邊際 PD ＋ 2D 聯合 PD → Friedman H 統計量;`HMatrix` n×n、`SignificantPairs` 依 H 降冪、`gridResolution` 夾在 2～50、`interpretH` 分級 <0.1 negligible／<0.3 weak／<0.5 moderate／≥0.5 strong）,`internal/eval/pdp.go` 另有 1D PDP。`go test ./internal/eval/` **22 PASS／0 FAIL**,含 **6 支 FriedmanH 測試**（Additive／Multiplicative／Threshold／ThreeFeatures／SingleFeature／EmptyInput）＋排序／分級 2 支。**本頁 2026-08-02 的「f32×f11 交互項確認有訊號」需降級（2026-09-27）**:2D PDP 的 `value_range` 大**不構成**交互證據;atlas 自帶測試 `TestFriedmanH_AdditiveModel` 明定「純可加模型 H 必須 < 0.1（negligible）」,而 OLS 是可加線性模型 ⇒ 同一對特徵在 OLS 上以原生 H 檢定**預期判為 negligible**。原句應改讀為「尚未以 H-statistic 檢定」。今日快照:`/api/strategies/layers` 12 筆（L1 1／L2 2／L3 2／L4 4／L5 3）;`/api/detector/registry/list` **29** themes;`/api/backtest/signals` `active_signals` null（Step 3 的股票池回測今日不可跑）;`/api/dashboard/risk` session_count 210。歷史:2026-08-02 v0.9 結算跑過 L3 升 active（client 端 sklearn 1.8.0 partial_dependence(OLS, features=[(f32, f11)], grid_resolution=10),2D shape (10,10)、value_range −289.81～312.01;每對 ~3s;為當日快照）。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b3）
l3_endpoints_probed:
  - /api/strategies/layers → 200（12 筆:L1 1／L2 2／L3 2／L4 4／L5 3）（2026-09-27T20:12:13+08:00）
  - /api/detector/registry/list → 200（29 themes）（2026-09-27T20:12:13+08:00）
  - /api/backtest/signals → 200（active_signals null ⇒ Step 3 不可跑）（2026-09-27T20:12:12+08:00）
  - /api/dashboard/risk → 200（session_count 210;無 sharpe／R² 欄位）（2026-09-27T20:12:12+08:00）
  - /api/stock/fundamentals?symbol=2330 與 /api/stock/technical?symbol=2330&days=10 → 皆 200（fundamentals 4 欄;rsi14／sma20／sma50 皆 0）（2026-09-27T20:12:12+08:00）
  - 源碼代理（無 HTTP 端點）＝ internal/eval/interaction.go 的 FriedmanH 與 partialDependence2D;`go test ./internal/eval/` → 22 PASS／0 FAIL（含 6 支 FriedmanH 測試）（2026-09-27T20:12:14+08:00）
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
| 2D PDP | **更正（2026-09-27）:原生實作存在**（`internal/eval/interaction.go` 的 `partialDependence2D` ＋ `FriedmanH`）;端點缺,client 端 sklearn 仍是唯一可交付路徑 |
| 背景數據 | `stock_get_fundamentals` + `stock_get_technical` |
| 評估 | `risk_get_metrics`（2026-09-27:無 sharpe／R² 欄位） |

**差異點**:2D PDP 計算成本是 1D 的 20 倍(網格 20×20 vs 50),金融大樣本需採樣。**更正（2026-09-27）**:atlas 原生 `FriedmanH` 是對**所有配對**算 H（`HMatrix` n×n）,grid 夾在 2～50 ⇒ 成本約 O(n²×grid²),與 client 端只挑一對的做法不同。

**沒有對位的部分**:**端點面**無 2D PDP、無熱力圖工具;**更正（2026-09-27）**:原生 2D 聯合 PD＋Friedman H 存在（缺端點）。三特徵以上的交互在 atlas 對位下**沒有替代路徑**——SHAP／LIME 於 repo 內 0 命中（2026-09-27 於 SK-13 已驗證）,原生只有 pairwise。

## 散戶解讀
- **G**:用戶問「PB 跟 MOM 哪個組合最賺?」 → 2D PDP 給熱力圖,散戶直覺看出「低 PB + 高 MOM」可能是甜蜜點。
- **+E**:**散戶最常忽略「因子必須搭配」**——「低 PE 價值股」與「高 MOM 動能股」單看都不如「低 PE + 高 MOM」一起。**這是教科書看不到的 alpha 源**。
- 對位 ATLAS_METHODOLOGY 七時期:交互甜蜜點在 regime 切換時會移動,需每期重畫。

## 驗證方式
Step 1: 用 SK-10/SK-11 訓練好的模型,client 端 `partial_dependence(model, X_test, features=[('pb','mom12m')], grid_resolution=20)`。
Step 2: 繪製熱力圖,標出「最暖的格子」(最高預測報酬區)。
Step 3: 把「最暖格子對應的股票池」實際丟進 backtest_signals 跑回測,確認 OOS Sharpe 優於單一因子的策略。

### L3 端點實跑 + 源碼代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/strategies/layers` | 200 | 12 筆:L1 1／L2 2／L3 2／L4 4／L5 3（**與 2D PDP／交互無重疊**） | 2026-09-27T20:12:13+08:00 |
| 2 | `/api/detector/registry/list` | 200 | **29** themes（`AI_capex_surge`／`tariff_shock`…）,非交互項 | 2026-09-27T20:12:13+08:00 |
| 3 | `/api/backtest/signals` | 200 | `active_signals` null → **Step 3「最暖格子丟回測」今日不可跑** | 2026-09-27T20:12:12+08:00 |
| 4 | `/api/dashboard/risk` | 200 | session_count 210;無 sharpe／R² 欄位 | 2026-09-27T20:12:12+08:00 |
| 5 | `/api/stock/fundamentals`＋`/api/stock/technical?symbol=2330` | 200／200 | fundamentals 只有 4 欄;`rsi14`／`sma20`／`sma50` 皆 0 | 2026-09-27T20:12:12+08:00 |
| 6 | 源碼代理（無 HTTP 端點）:`internal/eval/interaction.go` | exit 0 | `go test ./internal/eval/` → **22 PASS／0 FAIL**;6 支 FriedmanH 測試全過 | 2026-09-27T20:12:14+08:00 |

- **更正（2026-09-27,重要）**:第 6 列推翻本頁「無原生 2D PDP」;更關鍵的是**判準變了**——交互要用 **H-statistic** 判,不是看 2D PDP 的數值範圍。atlas 自帶 `TestFriedmanH_AdditiveModel` 把「純可加模型 ⇒ H < 0.1」寫成硬性預期,而 OLS 正是可加線性模型 ⇒ 本頁 2026-08-02 用 OLS 跑出的「交互有訊號」在原生判準下應改判 **negligible／未檢定**。
- **Step 3 保持未驗（今日）**:第 3 列 `active_signals` 為 null,無法把「最暖格子」丟進 backtest 驗 OOS Sharpe。
- 本頁 2026-08-02 的 2D shape (10,10)、value_range −289.81～312.01 為**當日 client 端快照**,非交互強度指標。

## 未消化 / 待補
- [ ] 網格大小 20×20 在台股樣本下可能雜訊大,需實測。
- [ ] 與 SK-02 特徵擴充的對應:SK-02 自動生成所有交互特徵,SK-15 是事後診斷「哪個交互值得保留」。

> **2026-09-27 已解並移出本段（1 項）**:「三特徵交互(3D)…實務上用 SHAP interaction values 替代」→ **atlas 無 SHAP**（`git grep` 0 命中,2026-09-27 於 SK-13 已驗證）,原生只有 pairwise `FriedmanH` ⇒ 3D 交互在 atlas 對位下**沒有替代路徑**,該項結案。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:特徵交互需對位 regime 切換下的交互效應變化)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)