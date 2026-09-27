---
title: SK-13 排列重要性（變數重要性）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-13
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, backtest_signals, risk_get_metrics, experiment_diff]
verification: 2026-09-27 L3 端點實跑（明細見 §驗證方式）:5 個端點群中 3 個 200、2 個非 200。**更正（2026-09-27）:原句「atlas 端沒『特徵排名』端點,需評估是否提案開 `feature_importance` endpoint」低估現況**——permutation importance **已在 repo 內完整實作**（`internal/eval/importance.go` ＋ `internal/experiment/importance.go`）,且已掛進 judge（`nRepeats=5`、特徵固定 `close／volume／return_1d`）,寫入 `importance_result` ⇒ 提案縮小為「暴露既有實作」。**已驗證負面**:端點面 0 出口（grep 只命中無關的 `systemic_importance`）;今日 `history` 空、`diff` 404 ⇒ `importance_result` 取不到。歷史:2026-08-02 v0.9 結算升 active（client 端 sklearn permutation_importance(OLS, n_repeats=10),top10 首位 f32 0.252、末位 f05 0.122;當日快照）。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b3）
l3_endpoints_probed:
  - "/api/stock/fundamentals?symbol=2330 與 /api/stock/technical?symbol=2330&days=10 → 皆 200（前者僅 4 欄;後者 rsi14／sma20／sma50 皆 0 ⇒ 不供應因子值）（2026-09-27T20:12:12+08:00）"
  - "/api/backtest/signals → 200（active_signals null ⇒ 無 OOS y）（2026-09-27T20:12:12+08:00）"
  - "/api/dashboard/risk → 200（session_count 210;無 importance／R² 欄位）（2026-09-27T20:12:12+08:00）"
  - "/api/dashboard/correlation-matrix → 200（20 個策略／類股標的,非特徵層）（2026-09-27T20:12:13+08:00）"
  - "/api/experiment/history → 200（空）;diff 缺 id／不存在 id → 400／404（2026-09-27T20:12:13+08:00）"
  - 源碼代理（無 HTTP 端點）＝ internal/eval/importance.go ＋ internal/experiment/importance.go ＋ judge 掛載;`go test ./internal/eval/` → 22 PASS／0 FAIL（含 TestPermutationImportance）（2026-09-27T20:12:14+08:00）
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Permutation Importance 排列重要性需對位 regime 內 vs 跨 regime 差異)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-13 在 atlas 是「哪個因子真有用」的黑盒問答——把每個因子打亂看模型掉多少分,比線性係數更可靠,且適用任何模型(不只線性)。

## 論文版概念（忠實還原來源）
- **核心**:permutation importance =「基準分數 − 打亂某特徵後的分數」,重複 n_repeats 次平均
- **輸入**:已訓練 model、X_test、y_test、`n_repeats=5`、`metric='R2'`
- **動作**:算基準分數 → 對每個特徵 j 重複 n_repeats 次（打亂 j 列 → 算新分數 → importance[j] += score_base − new_score）→ 平均並排序
- **輸出**:DataFrame(feature, importance, rank)
- **優於線性係數**:不假設線性關係、不受特徵尺度影響
- **缺點**:對高度共線特徵 importance 會被低估(打亂一個共線特徵另一個還能撐住)

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 已訓練 model | **更正（2026-09-27）:atlas 有原生 ML 層**（OLS／PCR／PLS／ElasticNet／GLM-spline／RF,無 NN）;permutation 的 model 仍只在 judge 內部（用 OLS） | 缺(端點) |
| X_test 多欄特徵 | 股票多維特徵 | `stock_get_fundamentals` + `stock_get_technical` |
| y_test 真實報酬 | backtest 序列 OOS y | `backtest_signals` |
| 評估指標分數 | risk metrics（2026-09-27:無 R²／sharpe 欄位） | `risk_get_metrics` |
| 因子刪除後效果 | atlas 無原生 by-factor ablation(SK-22,2026-08-02):實驗級 metric delta 用 `experiment_diff`（2026-09-27 實測:history 空、diff 404 ⇒ 今日不可達）,排除式邊際貢獻不提供;替代 = `/api/dashboard/pnl-attribution` 或 Darwinian + `strategy_ranker`(詳見 `SK-22-ablation-analysis.md`) |

**差異點**:論文是「模型已存在 → 算重要性」,atlas 是「client 端訓練 → atlas 端供資料 → client 端算 importance」。**更正（2026-09-27）**:「importance 只在 client 端」半錯——repo 內有原生 `PermutationImportance`（judge 路徑）,只是沒端點。

**沒有對位的部分**:
- **端點面**沒有「模型訓練」;原生 ML 層只在 repo 內（SK-05～10）
- **端點面**沒有「permutation importance」／「特徵排名」（2026-09-27:原生實作存在,僅 judge 內部使用）
- **SHAP / LIME 個股層級解釋**(2026-09-27 實測):atlas 源碼 grep `shap／lime／shapley` = **0 命中**,且**無模型訓練端點** ⇒ per-prediction 解釋既無輸入也無輸出;permutation（global）是唯一可跑路徑,SHAP／LIME 只能 client 端自帶模型。

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「86 個因子真的每個都有用嗎?」 → 反問「打亂某因子,模型掉分多 = 真有用;分數不動 = 雜訊」。permutation 是「對模型說實話」的方式。
- **R 段**:對位 atlas → 「client 端用 sklearn 訓練模型 → 用 `backtest_signals` 拿 OOS y 對齊 X → 跑 `permutation_importance(n_repeats=10)` → 看 top-10 因子」。
- **+E 段**:警示「**top-1 若是你聽過的因子(像本益比) = 可能是公開 alpha,機構已搶完,實盤會被套利磨平**;top-1 若是冷門因子(像『過去 12 個月最大回撤』)才有可能是真 alpha」。**這是散戶最常忽略的「因子新鮮度」訊號**。
- 對位 ATLAS_METHODOLOGY 七時期:同一因子的 importance 在不同 regime 差很多,**散戶要的是「這個 regime 下最重要的因子」,不是「全期平均 top-10」**。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` + `stock_get_technical` 拼出 18 欄 X,從 `backtest_signals` 拿 OOS y,client 端 train/test split 8:2。
> ⚠️ 本 Step 用隨機切分僅為演示 API；正式評估必走 SK-03 滾動時序切分,隨機切分在時間序列有前視洩漏 [2026-08-22 audit-fix]
Step 2: client 端跑 `permutation_importance(model, X_test, y_test, n_repeats=10, scoring='r2')`。
Step 3: 看 top-10 因子,**人工檢查是否有「冷門訊號」在前 5 名**;若 top-5 全是本益比/殖利率/MACD 這類大路貨,在 wiki 標「public alpha,實盤可能失效」。

### L3 端點實跑 + 源碼代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/stock/fundamentals?symbol=2330` | 200 | 只回 PE／PB／DY／Sector 4 欄 → **不是因子矩陣** | 2026-09-27T20:12:12+08:00 |
| 2 | `/api/stock/technical?symbol=2330&days=10` | 200 | `rsi14`／`sma20`／`sma50` 皆 **0** → 端點不供應可用的 X 欄 | 2026-09-27T20:12:12+08:00 |
| 3 | `/api/backtest/signals` | 200 | `active_signals` null → 無 OOS y | 2026-09-27T20:12:12+08:00 |
| 4 | `/api/dashboard/risk` | 200 | session_count 210;無 importance／R² 欄位 | 2026-09-27T20:12:12+08:00 |
| 5 | `/api/dashboard/correlation-matrix` | 200 | 20 個**策略／類股**標的 → 不是特徵層 | 2026-09-27T20:12:13+08:00 |
| 6 | `/api/experiment/history`／`diff` | 200／**400、404** | history 空 → `importance_result` **今日無實例**;diff 今日不可達 | 2026-09-27T20:12:13+08:00 |
| 7 | 源碼代理:`internal/eval/importance.go`＋judge | exit 0 | `go test ./internal/eval/` → **22 PASS／0 FAIL**（含 `TestPermutationImportance`） | 2026-09-27T20:12:14+08:00 |

- **更正（2026-09-27）**:第 7 列推翻「atlas 沒有 permutation importance」——實作**已存在且被 judge 使用**,缺的只是端點。
- **原生與本頁設定不同**:judge 是 `nRepeats=5` × 3 欄特徵,本頁 client 端是 `n_repeats=10` × 18 欄 ⇒ **數值不可互相引用**;本頁 2026-08-02 top10 為該日快照,今日無法複驗。

## 未消化 / 待補
- [ ] n_repeats=5 預設值是否足夠?學術建議 30-50 次,需實測確認。

> **2026-09-27 已解並移出本段（2 項）**:①「atlas 沒有『特徵排名』端點,需提案」→ **評估完成**:原生實作已存在（`internal/eval/importance.go`）並已掛進 judge;提案縮小為「暴露既有實作」。②「共線性能否用相關矩陣篩冗餘」→ **端點不可行**:`risk_get_correlation_matrix` 是策略／類股層（今日 20 個標的）。另註:atlas 原生 judge 用 `nRepeats=5`,與本頁建議 30-50 有落差（2026-09-27 實證）。

> **2026-09-27 校正**:原「與 SHAP / LIME 的差異…atlas 端缺」已實測結案(atlas 0 命中),移出本段;結論併入 §atlas 對位。
