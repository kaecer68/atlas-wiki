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
verification: "2026-09-27 L3 端點實跑 (http_code + timestamp 見 `l3_endpoints_probed`;明細見 §驗證方式):4 個 HTTP 端點全 200,但**皆無 R²_oos／係數欄位** → 本頁 `R²_oos=0.9996` 為 2026-08-02 client 端 sklearn 快照,今日無法由 atlas 複驗。新增:**atlas repo 內有原生 ElasticNet**(`internal/ml/elasticnet.go`,座標下降 + 標準化 + 內建 `AlphaAuto` 3-fold CV,另有 `UseHuber`/`Xi` 穩健加權),可用 `cmd/backtest-pipeline -model elasticnet` 實跑 → 今日 `-synthetic` exit 0 但 **R²_OOS +0.6406（✗ WARN;同批同 binary 的 OLS 為 +0.9992）**,原因是 CLI 的 `newModel(\"elasticnet\")` 傳入 `AlphaAuto: false, Alpha: 1.0` 固定值 → **本頁「alpha 由 CV 自動選」在 CLI 路徑不成立**;`UseHuber` 全 repo 無任何呼叫者啟用（只有 `internal/ml/elasticnet.go` 自身引用）。歷史:2026-08-02 v0.9 結算跑過 L3 升 active（client 端 sklearn 1.8.0 ElasticNetCV,l1_ratio=[0.1,0.5,0.9],R²_oos=0.9996）。"
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b2）
l3_endpoints_probed:
  - "/api/stock/fundamentals?symbol=2330 → 200（PE 30.19/PB 9.57/DY 1.1,X 來源）（2026-09-27T20:02:26+08:00）"
  - "/api/backtest/signals → 200（active_signals null,無 OOS y）（2026-09-27T20:02:26+08:00）"
  - "/api/dashboard/risk → 200（session_count 210;無 R²／係數欄位）（2026-09-27T20:02:26+08:00）"
  - "/api/field-contract → 200（2262 欄;r2 / r_squared 0 命中）（2026-09-27T20:03:56+08:00）"
  - "CLI 代理（無 HTTP 端點）: atlas repo `-synthetic -model elasticnet` → R²_OOS +0.6406（WARN;同批 OLS +0.9992）（2026-09-27T20:02:28+08:00）"
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
| ElasticNet 訓練 | MCP／HTTP 缺;**repo 內有原生 ElasticNet**(`internal/ml/elasticnet.go`,座標下降;CLI `-model elasticnet`,2026-09-27 實跑) |
| CV 選 alpha | 原生 `AlphaAuto` 內建 3-fold CV,但 CLI 路徑關閉(`newModel("elasticnet")` 固定 `Alpha 1.0,AlphaAuto false`;2026-09-27 實跑 R²_OOS +0.6406) |
| 評估 | `risk_get_metrics` |
| 與 SK-04 整合 | Huber ElasticNet 在 client 端即可組合 |

**差異點**:論文版是單純 sklearn 流程;**HTTP 面** atlas 端需 client 自組（repo 內有原生實作,`-model elasticnet`）;**ElasticNet 的 L1 特性會把 86 個因子壓縮到少數非零係數（具體個數取決於 alpha/l1_ratio,非固定 ~10-20 個;2026-08-22 驗證(合成實驗):86 相關因子×336 月,CV 選出非零 37-79 個）,這與 SK-13 permutation importance 互補——前者看「模型覺得哪些因子有用」,後者看「打亂後掉分多少」**。

**沒有對位的部分**:無原生 ElasticNet 的 **HTTP** 端點（原生實作只在 repo 內,`-model elasticnet`）。

## 散戶解讀
- **G**:用戶問「86 個因子太多怎麼辦?」 → ElasticNet 是 Lasso + Ridge,自動選重要因子且平滑處理共線。
- **+E**:**`l1_ratio` 選 0.5 是平衡點,但散戶若因子數 << 樣本數,選 0.2(Ridge 為主)更穩**——學術預設不一定是最佳。
- 對位 ATLAS_METHODOLOGY 七時期:ElasticNet 選的因子在 regime 切換時可能完全換一批,**散戶要的是「這個 regime 下 ElasticNet 選哪些」,不是「全期平均 top-10」**。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` + `stock_get_technical` 拉 18 欄 X,從 `backtest_signals` 拿 OOS y。
Step 2: client 端跑 `ElasticNetCV(l1_ratio=[0.1,0.5,0.9], alphas=np.logspace(-4,0,20))`。
Step 3: 對比 SK-05 OLS 與 SK-09 PLS 的 OOS R²,確認 ElasticNet 優於 OLS 但不優於 PLS(預期差距 5-15%)。
> 口徑註：上述預期排名僅對小樣本弱訊號真實資料成立；本頁合成線性資料實測 OLS=1.0 最高,兩者不矛盾但不可混讀 [2026-08-22 audit-fix]

### L3 端點實跑 + CLI 代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19 / PB 9.57 / DY 1.1 → X 來源可用 | 2026-09-27T20:02:26+08:00 |
| 2 | `/api/backtest/signals` | 200 | `active_signals` null、var/sharpe 全 0 → 無 OOS y | 2026-09-27T20:02:26+08:00 |
| 3 | `/api/dashboard/risk` | 200 | session_count 210、`insufficient_data` 1；無 R² 欄位 | 2026-09-27T20:02:26+08:00 |
| 4 | `/api/field-contract` | 200 | 2262 欄；`r2` / `r_squared` 0 命中 | 2026-09-27T20:03:56+08:00 |
| 5 | CLI（非 HTTP）:`cmd/backtest-pipeline -synthetic -model elasticnet` | exit 0 | 500 samples × 2 features；**R²_OOS +0.6406 → ✗ WARN**（同批 OLS +0.9992） | 2026-09-27T20:02:28+08:00 |

- **更正（2026-09-27）**:第 5 列推翻兩句舊敘述 ——(a)「ElasticNet 訓練缺、atlas 端需 client 自組」在 repo 層不成立:`internal/ml/elasticnet.go` 有原生座標下降實作,`cmd/backtest-pipeline -model elasticnet` 可直接跑;(b)「alpha 由 CV 自動選」只在 `AlphaAuto=true` 時成立,CLI 的 `newModel` 傳固定 `Alpha: 1.0` → 合成線性 DGP 上明顯 under-fit（+0.6406 對比 OLS +0.9992）。
- **`use_huber` 更正**:`internal/ml/elasticnet.go` 有 `UseHuber`/`Xi` 穩健加權實作,但 `git grep -n UseHuber` 顯示全 repo 只有該檔自身引用、預設 false,沒有任何呼叫者啟用 → atlas 端今日無啟用途徑,本頁「需實測」仍成立。
- Step 1 今日只完成一半:X 端點可用（2330 PE/PB/DY）,但 `/api/backtest/signals` 回 `active_signals: null` 全 0 → **無 OOS y**。Step 3 亦不可由 atlas 完成（第 3 列無 R² 欄位）。

## 未消化 / 待補
- [ ] `alpha` CV 範圍是否足夠?學術建議 logspace(-6, 2, 50)。（2026-09-27 實測:atlas 原生 `AlphaAuto` 只做 3-fold 網格且 CLI 關閉該路徑 → 固定 α 在合成資料 R²_OOS 僅 +0.6406,是「α 選不好即崩」的直接證據;真實台股 α 範圍仍待 client 端實測）
- [ ] use_huber=True 對小樣本的影響需實測。（2026-09-27 實測:`internal/ml/elasticnet.go` 有 `UseHuber`/`Xi`,但全 repo 無呼叫者啟用 → atlas 端今日無法以 CLI 實測,仍須 client 端自組）
- [ ] ElasticNet 與 SK-22 消去法的因果關係:理論上若 SK-22 顯示某因子刪掉後掉分很多,ElasticNet 應該把該因子的係數保留下來——可交叉驗證。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Elastic Net 正則化需對位 7 時期 × 策略三分類)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)