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
verification: 2026-09-27 L3 端點實跑 (http_code + timestamp 見 `l3_endpoints_probed`;明細見 §驗證方式):4 個 HTTP 端點全 200,**無任何端點回 R²_oos／成分數** → 本頁 `R²_oos=0.028` 為 2026-08-02 client 端 sklearn 快照,今日無法由 atlas 複驗;「2-3 個成分就 90% 變異」仍為未實證猜測。新增:**atlas repo 內有原生 PCR**(`internal/ml/pcr.go`:SVD 取 V 前 k 欄、`NComponents` 預設 4、`VarianceThreshold>0` 時改為自動累積變異門檻選 k),可用 `cmd/backtest-pipeline -model pcr` 實跑 → 今日 `-synthetic`(CLI 用 `NComponents 5, VarianceThreshold 0.95` 自動選)exit 0、**R²_OOS +0.9993（PASS）** → 「atlas 無原生 PCA／降維端點」在 repo 層不成立,但仍不在 MCP／HTTP 面。**未消化第 3 項已解（2026-09-27）**:`/api/strategies/layers` 顯示 atlas 的 L1–L5 是 **strategy frame 分層**(L1:1/L2:2/L3:2/L4:4/L5:3,合計 12),`/api/detector/registry/list` 是 29 個事件主題 detector,**兩者都不是降維後訊號,與 PCA／PCR 無重疊**。歷史:2026-08-02 v0.9 結算跑過 L3 升 active（client 端 sklearn 1.8.0 PCA(n_components=4) + LinearRegression,R²_oos=0.028）。**2026-09-27 更正（本批發現）**：CLI `-synthetic` 印出的 `R²_OOS` **實為 in-sample**——`cmd/backtest-pipeline/main.go` 的 `runSynthetic` 對**同一份 X** 先 `Fit` 後 `Predict`（第 ~382–388 行），且 `rand.Float64()` 未設 seed ⇒ 同日重跑值即變動（rf +0.9909～+0.9928 實測）。⇒ 此列只能當「模型可跑」的存在性檢查，**不可當 OOS 證據**。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b2）
l3_endpoints_probed:
  - "/api/stock/fundamentals?symbol=2330 → 200（PE 30.19/PB 9.57/DY 1.1）（2026-09-27T20:02:26+08:00）"
  - "/api/backtest/signals → 200（active_signals null;無 OOS y）（2026-09-27T20:02:26+08:00）"
  - "/api/dashboard/risk → 200（session_count 210;無 R² 欄位）（2026-09-27T20:02:26+08:00）"
  - "/api/strategies/layers → 200（L1:1/L2:2/L3:2/L4:4/L5:3,total 12;strategy frame 分層）（2026-09-27T20:02:48+08:00）"
  - "/api/detector/registry/list → 200（29 個 theme detector,全 enabled）（2026-09-27T20:02:46+08:00）"
  - "CLI 代理（無 HTTP 端點）: atlas repo `-synthetic -model pcr` → R²_OOS +0.9993（PASS;實為 in-sample,非 OOS）（2026-09-27T20:02:28+08:00）"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:PCR 主成分需對位 regime 切換下的因子有效性)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
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
| PCA | MCP／HTTP 缺;**repo 內有原生 PCR**(`internal/ml/pcr.go` 以 SVD 做 PCA,`-model pcr`,2026-09-27 實跑) |
| OLS 殘層 | 缺(client 端);原生 PCR 在成分分數上自帶 OLS(`β=(ZᵀZ)⁻¹Zᵀy`) |
| 評估 | `risk_get_metrics` |

**差異點**:**更正（2026-09-27）**:「atlas 端兩者都缺」只對 MCP／HTTP 面成立,repo 內 PCR 與 PLS 都有原生實作且 CLI 可跑(`-model pcr` / `-model pls`)。PCR 跟 PLS(SK-09)差別只在降維方法——PCR 看 X 變異,PLS 看 X 與 y 相關。**金融預測上 PLS 幾乎總是贏 PCR**,論文版用 PCR 是當 baseline 對比。

**沒有對位的部分**:無原生 PCA 的 **HTTP** 端點(實作只在 repo 內);無「特徵相關性矩陣」工具。

## 散戶解讀
- **G**:用戶問「86 個因子共線嚴重怎麼辦?」 → PCR 把共線壓掉,PLS 同時看 y。
- **+E**:**散戶若沒工具,選 PLS(SK-09)而不是 PCR**——PCR 是學術對照組,實務 PLS 勝出。
- 對位 ATLAS_METHODOLOGY 七時期:PCA 的主成分在 regime 切換時可能完全失去解釋力,需謹慎。

## 驗證方式
Step 1: 拉 14 欄 X(基本+技術),從 `backtest_signals` 拿 y。
Step 2: client 端 `PCA(n_components=4).fit_transform(X)` → `LinearRegression().fit()`。
Step 3: 對比 SK-05 OLS 與 SK-09 PLS 的 OOS R²(預期 PLS > PCR > OLS)。
> 口徑註：上述預期排名僅對小樣本弱訊號真實資料成立；本頁合成線性資料實測 OLS=1.0 最高,兩者不矛盾但不可混讀 [2026-08-22 audit-fix]

### L3 端點實跑 + CLI 代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19 / PB 9.57 / DY 1.1 | 2026-09-27T20:02:26+08:00 |
| 2 | `/api/backtest/signals` | 200 | `active_signals` null、全 0 → 無 OOS y | 2026-09-27T20:02:26+08:00 |
| 3 | `/api/dashboard/risk` | 200 | session_count 210；無 R²／成分數欄位 | 2026-09-27T20:02:26+08:00 |
| 4 | `/api/strategies/layers` | 200 | L1:1 / L2:2 / L3:2 / L4:4 / L5:3,total 12（strategy frame 分層） | 2026-09-27T20:02:48+08:00 |
| 5 | `/api/detector/registry/list` | 200 | 29 個 theme detector（`US_rates_up`…`gold_rally`），全 enabled | 2026-09-27T20:02:46+08:00 |
| 6 | CLI（非 HTTP）:`cmd/backtest-pipeline -synthetic -model pcr` | exit 0 | 500 samples × 2 features；**R²_OOS +0.9993 → PASS（實為 in-sample,非 OOS）** | 2026-09-27T20:02:28+08:00 |

- **更正（2026-09-27）**:第 6 列推翻「無原生 PCA 端點／atlas 端兩者都缺」的 repo 層敘述:`internal/ml/pcr.go` 有原生 SVD 版 PCR（`NComponents` 預設 4,`VarianceThreshold>0` 時改為累積變異自動選 k）。仍**不在 MCP／HTTP 面**,所以 client 端自建的結論不變。
- **未消化第 3 項在此結案（2026-09-27）**:第 4、5 列證明 atlas 的 L1–L5 是 **strategy frame 的分層**(12 個策略框架),detector registry 是 **29 個事件主題** detector;兩者都不是「降維後訊號」,與 PCA／PCR 成分無重疊 → 此問已解,原項移出「未消化」。
- Step 1 今日只完成一半:X 端點只回 4 欄(本頁要 14 欄);`backtest_signals` 無 OOS y。Step 2／Step 3 需 client 端執行（atlas 無 HTTP 訓練端點）。

## 未消化 / 待補
- [ ] `variance_threshold=0.9` 自動選成分數的邏輯在金融數據是否合理?台股因子變異集中,可能 2 個成分就 90%。（2026-09-27 實測:atlas 原生 PCR 有 `VarianceThreshold` 自動選路徑,CLI 以 0.95 在合成資料跑通 PASS（in-sample） → 「自動選」機制本身可用;「台股需 2 個還是 19 個成分」仍無 atlas 資料可驗,維持 SK-01 的未實證標註）
- [ ] PCR 與 SK-22 消去法的關係不明。

已解（2026-09-27）:與 L1–L5 detector 的重疊問題 → `/api/strategies/layers` 回 L1–L5 為 strategy frame 分層（12 個）,`/api/detector/registry/list` 回 29 個事件主題 detector,皆非降維後訊號;詳見 §驗證方式 L3 表第 4、5 列。
