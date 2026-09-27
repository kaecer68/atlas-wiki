---
title: SK-09 偏最小平方法（PLS）
description: "問「因子太多塞進模型會 overfit 嗎」、要用 PLS 降維時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-09
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, universe_get_sessions, risk_get_metrics]
verification: 2026-09-27 L3 端點實跑 (http_code + timestamp 見 `l3_endpoints_probed`;明細見 §驗證方式):8 個 HTTP 端點全 200,**但無任何端點回 R²_oos** → 本頁 `R²_oos=0.8892` 維持 2026-08-02 client 端 sklearn 快照,今日無法由 atlas 複驗。**atlas repo 內有原生 PLS**(`internal/ml/pls.go`,NIPALS／PLS1),CLI `-synthetic -model pls` → **R²_OOS +0.9993 PASS**。未消化第 1、2 項結案(明細見 §驗證方式)。同日負面:CLI 真實資料路徑不可用(`stopYear` 硬編 2020)。歷史:2026-08-02 v0.9 結算升 active（client 端 sklearn PLSRegression,R²_oos=0.8892）。**2026-09-27 更正**：`-synthetic` 的 `R²_OOS` 實為 in-sample（`runSynthetic` 對同一份 X 先 Fit 後 Predict，~382–388 行）且 `rand.Float64()` 未設 seed ⇒ 同日重跑即變動（rf +0.9909～+0.9928）。此列只證明模型可跑，**不可當 OOS 證據**。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b2）
l3_endpoints_probed:
  - "/api/stock/fundamentals?symbol=2330 → 200（PE 30.19/PB 9.57/DY 1.1）（2026-09-27T20:02:26+08:00）"
  - "/api/stock/technical?symbol=2330&days=10 → 200（rsi14/sma20/sma50 皆 0）（2026-09-27T20:02:26+08:00）"
  - "/api/dashboard/sessions → 200（90 sessions）（2026-09-27T20:03:05+08:00）"
  - "/api/dashboard/risk → 200（無 R²/Sharpe → 不區分 IS/OOS）（2026-09-27T20:02:26+08:00）"
  - "/api/dashboard/agent-observatory → 200（含 is_sharpe/oos_sharpe/is_oos_ratio/overfit_warning）（2026-09-27T20:05:30+08:00）"
  - "/api/parameters → 200（oos_window_days 30、walk_forward_embargo_days 5）（2026-09-27T20:03:04+08:00）"
  - "/api/strategies/layers → 200（L1:1/L2:2/L3:2/L4:4/L5:3）（2026-09-27T20:02:48+08:00）"
  - "CLI（非 HTTP）: `-synthetic -model pls` → R²_OOS +0.9993（PASS;實為 in-sample,非 OOS）（2026-09-27T20:02:28+08:00）"
  - "CLI 真實資料（負面）: `-model pls -data data/replay/merged.csv -symbol 0050.TW` → EXIT 1（stop_year=2020 / empty training data）（2026-09-27T20:05:30+08:00）"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:PLS 偏最小二乘需對位 7 時期 × 策略三分類)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-09 在 atlas 是「監督式降維」——把高維股票特徵(86 因子起跳)壓到 4 個成分,且每個成分都跟未來報酬 y 最相關,避免 OLS 在共線性下失效。

## 論文版概念（忠實還原來源）
- **核心**:PLS 找一組 latent components t_k,使得 `T = XW(P^T W)^(-1)`,且 `max cov(T, y)`
- **輸入**:`n_components=4`(預設)、`algorithm="nipals"`
- **動作**:標準化 X 與 y → `sklearn.cross_decomposition.PLSRegression` 擬合 → 返回模型
- **適用**:
  - 特徵數 p > 樣本數 n(典型 86 因子 vs 12 個月樣本)
> 口徑註：本頁 60/12 個月指滾動切割後單一 window 內月數；全樣本為 336 月（1994-01~2022-04,SK-01）[2026-08-22 audit-fix]
  - 特徵間高度共線性(動量/反轉/波動高度相關)
  - 想保留與 y 相關的 latent 結構
- **與 PCA 差別**:PCA 只看 X 的變異,PLS 同時看 X 與 y 的相關 → 對預測任務更實用

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 特徵 X(多欄) | 股票多維特徵 | `stock_get_fundamentals` + `stock_get_technical` |
| 目標 y(未來報酬) | 對位 stock 預測目標 | `universe_get_sessions`（今日 90 sessions,2026-09-27） |
| PLS 模型訓練 | **repo 內有原生 PLS**(`internal/ml/pls.go`,NIPALS/PLS1);MCP／HTTP 面仍缺 | CLI `cmd/backtest-pipeline -model pls`（2026-09-27 實跑 +0.9993） |
| 模型效果驗證 | `risk_get_metrics` **無 R²/Sharpe 欄位**（2026-09-27）;IS/OOS 分離改看 `agent-observatory` | `risk_get_metrics` + `/api/dashboard/agent-observatory` |

**差異點**:**更正（2026-09-27）**:「atlas 不提供原生 ML 訓練」只對 MCP／HTTP 面成立;`internal/ml/pls.go` 有原生 NIPALS PLS1。論文版假設 client 備好 X／y;atlas 端要自組 X——「特徵工程 orchestrator」缺口(SK-02 同問題)。

**沒有對位的部分**(HTTP 面):
- 無原生 PLS / PCA / 降維 endpoint
- 無「特徵間相關性」(需 client 端算 correlation matrix)
- 無「成分數 n_components 自動選擇」

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「86 個因子太多,塞進模型會 overfit?」 → PLS 把 86 個因子壓成 4 個「綜合訊號」——不是任意組合,是最會預測 y 的那 4 個。
- **R 段**:對位 atlas → 「HTTP 面沒有一鍵 PLS:① 拼 X(見 §atlas 對位) ② 算 y ③ client 端跑 `PLSRegression` ④ 效果看 `agent-observatory` scorecard,不是 `risk_get_metrics`」。
- **+E 段**:警示「n_components=4 是論文預設,但散戶資金小、樣本少,**降到 2 可能更穩健**,不是越多越好」。對位憲章七時期:PLS components 在 regime 切換時可能失效,需每期重擬。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` 拉 10 欄(PE/PB/殖利率/營收成長/ROE/負債比/現金比/流動比/淨利率/毛利率)+ `stock_get_technical` 4 欄(SMA20/SMA50/RSI14/MACD),合計 14 欄 X。
Step 2: 從 `universe_get_sessions` 取一份 supervised pipeline 結果,對齊 y 為「下一期月報酬」。
Step 3: client 端跑 `PLSRegression(n_components=2)`,對比 `LinearRegression` 的 in-sample R² 與 `risk_get_metrics` 給的 OOS R²,確認 PLS 在 OOS 優於 OLS(預期差距 5-15%)。
> 口徑註：上述預期排名僅對小樣本弱訊號真實資料成立；本頁合成線性資料實測 OLS=1.0 最高,兩者不矛盾但不可混讀 [2026-08-22 audit-fix]

### L3 端點實跑 + CLI 代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19 / PB 9.57 / DY 1.1 | 2026-09-27T20:02:26+08:00 |
| 2 | `/api/stock/technical?symbol=2330&days=10` | 200 | close 2475、date 2026-09-24;`rsi14`/`sma20`/`sma50` **皆 0** | 2026-09-27T20:02:26+08:00 |
| 3 | `/api/dashboard/sessions` | 200 | 90 sessions（最新 `session-20260927-daily`；RISK_ON） | 2026-09-27T20:03:05+08:00 |
| 4 | `/api/dashboard/risk` | 200 | 僅 degraded/gate_mode/risk_snapshot/session_count/source/var_gate → **無 R²、無 Sharpe** | 2026-09-27T20:02:26+08:00 |
| 5 | `/api/dashboard/agent-observatory` | 200 | 5 張 scorecard 皆含 `is_sharpe`/`oos_sharpe`/`is_oos_ratio`/`overfit_warning`（例 `etf-rotation-01`:0.0717／-1.3685／0.0524／true） | 2026-09-27T20:05:30+08:00 |
| 6 | `/api/parameters` | 200 | `experiment.oos_window_days` 30、`walk_forward_embargo_days` 5 | 2026-09-27T20:03:04+08:00 |
| 7 | `/api/strategies/layers` | 200 | L1:1/L2:2/L3:2/L4:4/L5:3 = 12（strategy frame 分層,非降維訊號） | 2026-09-27T20:02:48+08:00 |
| 8 | CLI（非 HTTP）:`-synthetic -model pls` | exit 0 | 500 samples × 2 features；**R²_OOS +0.9993 → PASS（實為 in-sample,非 OOS）** | 2026-09-27T20:02:28+08:00 |
| 9 | CLI 真實資料（負面）:`-model pls -data data/replay/merged.csv -symbol 0050.TW` | EXIT 1 | `no windows produced (... stop_year=2020)`／`has empty training data` | 2026-09-27T20:05:30+08:00 |

- **更正（2026-09-27）**:第 8 列推翻「atlas 不提供原生 ML 訓練」（`internal/ml/pls.go` 有 NIPALS PLS1,`NComponents` 預設 4、CLI 用 3）;仍**不在 MCP／HTTP 面**,「client 端自組 X」不變。
- **第 4／5 列結案未消化第 1 項**:`risk_get_metrics` 無 R²／Sharpe,談不上區分 IS/OOS;**IS/OOS 分離改看 `agent-observatory` scorecard**,OOS 窗長／embargo 在 `parameters`;Step 3 改用 scorecard。
- **第 9 列為同日負面結果（勿重踩）**:`rolling_split.go` 的 `stopYear` 硬編 2020 → 2024-07 起的 replay 檔產不出 window;**今日只有 `-synthetic` 能做 L3**。

## 未消化 / 待補
- [ ] `algorithm="nipals"` vs `"svd"` 對小樣本哪個穩健?（2026-09-27:atlas 原生 PLS 只有 NIPALS,`-model pls` 無 algorithm 旗標 → SVD 變體無對位,只能 client 端比）
- [ ] 跟 SK-08 PCR 差異:PCR 不看 y → PLS 更適合預測任務。（2026-09-27 更正:「atlas 端兩者都缺」只對 MCP／HTTP 面成立,repo 內 `-model pcr` / `-model pls` 都可跑 → 兩者可直接對比）

已解（2026-09-27）:IS/OOS 區分、L1–L5 重疊 → 見 L3 表第 4–7 列。
