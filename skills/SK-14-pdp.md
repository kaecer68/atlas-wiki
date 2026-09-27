---
title: SK-14 部分相依圖（邊際效應）
description: "問「PE 對預期報酬的影響是什麼」、要看邊際效應曲線時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-14
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, backtest_signals, risk_get_metrics]
verification: 2026-09-27 L3 端點實跑（http_code + timestamp 見 `l3_endpoints_probed`,明細見 §驗證方式）:5 個端點全 200。**更正（2026-09-27）:原句「無原生 PDP」不成立**——atlas repo `internal/eval/pdp.go` 有原生 `PartialDependence(predictor, X, featureIdx, gridResolution)`,grid 取**觀測到的 min～max**（故曲線天然只覆蓋樣本內範圍,正好對應本頁 Step 2 的「範圍外是外推不可信」）;`internal/eval/interaction.go` 另有 1D／2D 聯合 PD 與 Friedman H 檢定。`go test ./internal/eval/` **22 PASS／0 FAIL**（含 `TestPartialDependence` 13 個子測,涵蓋 grid resolution 3／5／7／11／20）。缺的是**端點與繪圖**,不是演算法;ICE 仍 0 命中（已驗證負面）。**regime 對位（今日實測）**:`/api/regime/history?days=7` 200,回 5 筆（regime 全 RISK_ON;period = consolidation／turnaround_up／turnaround_down,含 `period_source` 欄位）⇒ 本頁「PDP 形狀需每期重畫」在資料面可支撐,但該端點是 **7 日滾動窗**。今日其他快照:`/api/stock/technical` 的 rsi14／sma20／sma50 皆 0;`/api/backtest/signals` `active_signals` null（無 y）;`/api/dashboard/risk` session_count 210、無 sharpe／R² 欄位。歷史:2026-08-02 v0.9 結算跑過 L3 升 active（client 端 sklearn 1.8.0 partial_dependence(OLS, grid_resolution=20),f32／f11／f42 三條 PDP 皆單調上升;每因子 ~5s;為當日快照）。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b3）
l3_endpoints_probed:
  - "/api/stock/fundamentals?symbol=2330 → 200（PE 30.19／PB 9.57／DY 1.1）（2026-09-27T20:12:12+08:00）"
  - "/api/stock/technical?symbol=2330&days=10 → 200（rsi14／sma20／sma50 皆 0）（2026-09-27T20:12:12+08:00）"
  - "/api/backtest/signals → 200（active_signals null ⇒ 無 y）（2026-09-27T20:12:12+08:00）"
  - "/api/dashboard/risk → 200（session_count 210;無 sharpe／R² 欄位）（2026-09-27T20:12:12+08:00）"
  - "/api/regime/history?days=7 → 200（5 sessions;regime 全 RISK_ON;period consolidation／turnaround_up／turnaround_down）（2026-09-27T20:12:13+08:00）"
  - 源碼代理（無 HTTP 端點）＝ internal/eval/pdp.go 的 PartialDependence;`go test ./internal/eval/` → 22 PASS／0 FAIL（含 TestPartialDependence）（2026-09-27T20:12:14+08:00）
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:PDP 部分依賴圖需對位跨 regime 因子效應)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
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
| PDP 計算 | **更正（2026-09-27）:原生實作存在**（`internal/eval/pdp.go`）;端點缺,client 端 sklearn 仍是唯一可交付路徑 |
| 背景數據 | `stock_get_fundamentals` + `stock_get_technical` |
| 評估 | `risk_get_metrics`（2026-09-27:無 sharpe／R² 欄位） |

**差異點**:PDP 是視覺化工具,**更正（2026-09-27）**:atlas 端有原生 PDP **計算**（`internal/eval/pdp.go`,經 `go test` 實跑通過）但沒原生繪圖、也沒有端點;**client 端一張圖仍是唯一能給散戶直覺的交付**。

**沒有對位的部分**:**端點面**無 PDP／ICE,無繪圖工具;**更正（2026-09-27）**:原生 PDP 計算存在（`internal/eval/pdp.go`＋`interaction.go`）,ICE **確認 0 實作**（已驗證負面）。regime 標籤可由 `/api/regime/history?days=7` 取得（今日 5 sessions）。

## 散戶解讀
- **G**:用戶問「PE 對預期報酬的影響是什麼?」 → PDP 給一條曲線,可能是正斜率(PE 越高越好)、負斜率、U 型、倒 U 型。
- **+E**:**PDP 平均掉所有其他特徵的效應,若「PE 對報酬」依賴於「產業」,PDP 會誤導**。**散戶最常誤信 PDP 忽略交互效應**,這就是 SK-15 要解決的問題。
- 對位 ATLAS_METHODOLOGY 七時期:PDP 形狀在 regime 切換時會變,需每期重畫。

## 驗證方式
Step 1: 從 SK-10/SK-11 訓練好的模型,client 端跑 `partial_dependence(model, X_test, features=['pb'], grid_resolution=50)`。
Step 2: 繪圖,確認曲線在訓練樣本範圍內(範圍外是外推不可信)。
Step 3: 對比 SK-13 permutation importance 排名,確認 PDP top-3 與 permutation top-3 一致(若不一致需釐清原因)。

### L3 端點實跑 + 源碼代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/stock/fundamentals?symbol=2330` | 200 | 只有 PE／PB／DY／Sector → 背景數據僅 4 欄 | 2026-09-27T20:12:12+08:00 |
| 2 | `/api/stock/technical?symbol=2330&days=10` | 200 | `rsi14`／`sma20`／`sma50` 皆 0 | 2026-09-27T20:12:12+08:00 |
| 3 | `/api/backtest/signals` | 200 | `active_signals` null → 無 y 可配 | 2026-09-27T20:12:12+08:00 |
| 4 | `/api/dashboard/risk` | 200 | session_count 210;無 sharpe／R² 欄位 | 2026-09-27T20:12:12+08:00 |
| 5 | `/api/regime/history?days=7` | 200 | 5 筆:regime 全 `RISK_ON`;period `consolidation`×2／`turnaround_up`×2／`turnaround_down`×1;有 `period_source` | 2026-09-27T20:12:13+08:00 |
| 6 | 源碼代理（無 HTTP 端點）:`internal/eval/pdp.go` | exit 0 | `go test ./internal/eval/` → **22 PASS／0 FAIL**;`TestPartialDependence` 13 子測全過（grid 3／5／7／11／20） | 2026-09-27T20:12:14+08:00 |

- **更正（2026-09-27）**:第 6 列推翻本頁「缺(client 端 sklearn)」的字面讀法——atlas **有**原生 PDP `PartialDependence(predictor, X, featureIdx, gridResolution)`;缺的是**端點**（`internal/monitoring/api/**` 與 `cmd/atlas-mcp/server/` grep PDP／partial dependence 皆 0 命中）。
- **Step 2 的「樣本內範圍」是結構保證**:原生實作的 grid 直接取該特徵觀測值的 min～max,不存在外推格點。
- **regime 對位落地**:第 5 列顯示 regime ＋ period 標籤可即時取得（含中文期名 `盤整`／`轉折開高`／`轉折下壓`）,故「每期重畫 PDP」不是空話;但端點為 7 日滾動窗,長序列需另外取。
- 本頁 2026-08-02 的三條 PDP 曲線（f32／f11／f42 皆單調上升）為**當日 client 端快照**,atlas 端今日無端點可複驗（該日 client 端為 OLS,PDP 單調為預期結果,不構成非線性證據）。

## 未消化 / 待補
- [ ] ICE(Individual Conditional Expectation)是否要在 atlas 端做?PDP 看不到異質性,ICE 補這個洞。
- [ ] 2D PDP(SK-15 熱力圖)對「交互假設」驗證比 1D 更強。
- [ ] PDP 計算成本高(每網格點都跑一次模型),金融樣本大時需採樣。

> **2026-09-27 補充**:本段三項今日皆**未解**。今日新增的是**已驗證負面**（ICE 0 實作）與**實作面更正**（原生 PDP 存在,缺端點與繪圖）,兩者已寫進 §atlas 對位 與 §驗證方式,不再重複列為待補。
