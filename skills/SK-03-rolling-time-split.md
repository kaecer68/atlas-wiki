---
title: SK-03 時間序列滾動切割
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-03
ingested_at: 2026-07-31
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [universe_get_sessions]
verification: 2026-09-27 L3 端點實跑 7 端點（http_code + timestamp 見 `l3_endpoints_probed`;明細見 §驗證方式）。實測更正與新證據:(1) `universe_get_sessions` 今日回 **90** sessions（滾動窗 2026-06-25~2026-09-27）,頁內「147 sessions 對位」為 2026-08-02 當日快照（第五條鐵律）;(2) `universe_get_session_detail` 真實路徑 = `/api/dashboard/sessions/{session_id}`（今日 session-20260927-daily → 200,outcome_count 24、summary.position_count 5）;canary 值 `/api/dashboard/sessions/latest` → **404**（與 SK-37 同日一致,路徑陷阱）;(3) `parameters_get` 1669 keys 中 **0 個**命中 step_year / valid_length / first_train / test_end / split →「atlas 未由 HTTP 暴露 SK-03 三軸」由待查升為**已驗證的否定**;(4) **源碼級代理驗證（atlas 無此 HTTP 端點）**:`atlas/internal/backtest/rolling_split.go` 明寫「following the SK-03 specification」,預設 FirstTrainEnd=2007-12-31 / ValidLengthYears=2 / StepYears=1 / TestEnd=2022-04-30 / stopYear=2020 **與本頁規格逐項相同**,並由 `atlas/cmd/backtest-pipeline` 的 `-first-train-end/-valid-years/-step-years/-test-end` 旗標暴露 → 三軸存在,只是不在 MCP／HTTP 面;(5) `risk_get_metrics` 今日 session_count **210**、`sharpe_short/long` 與 var 皆 0 → 仍無法由此端點做 valid/test 分段績效對比。歷史:2026-08-02 v0.9 結算跑過 L3 升 active（client 端 pandas 三段式 train 168 月 / valid 24 月 / test 144 月）。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b1）
l3_endpoints_probed:
  - /api/dashboard/sessions → 200（90 sessions）（2026-09-27T19:27:54+08:00）
  - /api/dashboard/sessions/session-20260927-daily → 200（outcome_count 24）（2026-09-27T19:28:05+08:00）
  - /api/dashboard/sessions/latest → 404（canary 對照值,路徑陷阱）（2026-09-27T19:27:54+08:00）
  - /api/dashboard/risk → 200（session_count 210;sharpe_short/long 皆 0）（2026-09-27T19:27:54+08:00）
  - /api/backtest/status → 200（last_auto_date 2026-09-23）（2026-09-27T19:27:54+08:00）
  - /api/backtest/signals → 200（active_signals null）（2026-09-27T19:27:54+08:00）
  - /api/parameters → 200（1669 keys;step_year/valid_length/first_train/test_end 皆 0 命中）（2026-09-27T19:27:54+08:00）
  - /api/backtest/snapshots → 200（20 筆日快照 2026-08-25~09-23,17 筆 sharpe_short 非 0）（2026-09-27T19:30:53+08:00）
  - 源碼級代理（無 HTTP 端點）: atlas/internal/backtest/rolling_split.go + atlas/cmd/backtest-pipeline（2026-09-27T19:30:33+08:00）

---

## 一句話定位
在 atlas 中,SK-03 提供「訓練 / 驗證 / 測試」三段式時間滾動切片的工程基礎,直接對位 `universe_get_sessions` 的 session 結構。

## 論文版概念(忠實還原來源)
- **三段式切分**:train(從資料起點到 `first_train_end`) / valid(`first_train_end` 之後 `valid_length_years` 年) / test(驗證集結束到固定 `test_end`)
- **滾動機制**:每次向前推進 `step_years`(預設 1 年),重新切分
- **預設切片錨點**:`first_train_end=2007-12-31`、`valid_length_years=2`、`test_end=2022-04-30`、`step_years=1`
- **停止條件**:驗證集起始年 > 2020(避免切片跨入無標籤區間)
- **資料契約**:DataFrame 必須含日期索引,需先 sort 取得 unique dates

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 滾動切分產出 session list | universe 跑出的歷次回測 session(每個 session = 一次 fit→score 週期) | `universe_get_sessions` |
| valid_length_years=2 驗證窗 | session 內 validation window 配置 | `universe_get_session_detail` |
| test_end 固定截止 | 系統時序上的 last_auto_date / last_backtest 截止 | `backtest_status` |
| step_years=1 滾動步進 | universe 的 rolling_period 設定 | `backtest_signals` |
| 樣本外評估(R²/夏普) | 樣本外績效總表 | `risk_get_metrics` |

**差異點**:atlas universe 是「策略 × 期間」的笛卡兒積(session 數通常 50+),SK-03 是純「時段切片」單一軸;atlas 多了「策略 ID」維度,SK-03 沒提。

**更正（2026-09-27）**:原寫「`valid_length_years` 與 `step_years` 在 atlas 沒有外部暴露欄位」**不成立** —— `atlas/internal/backtest/rolling_split.go` 已依 SK-03 規格實作三軸,`atlas/cmd/backtest-pipeline` 以旗標暴露。正確說法:**不在 MCP／HTTP 面**（`/api/parameters` 0 命中,且 session 端點不回三段日期）。

## 散戶解讀(GROW+ 引用點)
- **R 段(現狀)**:用戶問「為什麼回測看起來好、實盤卻虧損」→ 多半是「只看 test 段、沒看 valid 段」造成的過擬合錯覺。SK-03 提醒:valid 段才是策略真正「驗收」的考試。
- **+E 段(風險)**:強調「滾動是必須,不是可選」——若每年只回測一次、不滾動,2020 疫情或 2022 升息這種 regime 切換會被錯過。
- 對位 ATLAS_METHODOLOGY 七時期:每次滾動對應一次「時期重判」,valid 段是 regime 切換壓力測試。

## 驗證方式
Step 1: 呼叫 `universe_get_sessions` 確認近 90 天 session 數量與切分頻率(月/季/半年)。
Step 2: 抽一個 session,呼叫 `universe_get_session_detail` 確認 train/valid/test 三段日期範圍與 SK-03 定義是否一致(預期 valid 在 test 之前、test 跨年)。今日實測:session 只有 `recorded_at`/`regime`/`outcome_count`/`summary`,**沒有 train/valid/test 三段日期** → 步驟本身不可由 HTTP 完成（見下）。
Step 3: 呼叫 `risk_get_metrics` 比對該 session 樣本外指標(drawdown、Sharpe)是否反映 valid+test 兩段,而不是只看 test。今日實測:`/api/dashboard/risk` 的 `sharpe_short`/`sharpe_long`/`var_95` 皆 0,分段對比不可行;可用的最近替代是 `/api/backtest/snapshots`（20 筆日快照、17 筆 `sharpe_short` 非 0）。

### L3 端點實跑（2026-09-27,本 PR;帶 `X-API-Key`,timeout 6s）

| # | 端點（GET） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/dashboard/sessions` | 200 | 90 sessions（滾動窗 2026-06-25~2026-09-27） | 2026-09-27T19:27:54+08:00 |
| 2 | `/api/dashboard/sessions/session-20260927-daily` | 200 | outcome_count 24 / summary.position_count 5 | 2026-09-27T19:28:05+08:00 |
| 3 | `/api/dashboard/sessions/latest` | **404** | canary 對照值（路徑陷阱） | 2026-09-27T19:27:54+08:00 |
| 4 | `/api/dashboard/risk` | 200 | session_count 210；sharpe_short/long、var_95 皆 0 | 2026-09-27T19:27:54+08:00 |
| 5 | `/api/backtest/status` | 200 | last_auto_date 2026-09-23 | 2026-09-27T19:27:54+08:00 |
| 6 | `/api/backtest/signals` | 200 | active_signals null，全 0 | 2026-09-27T19:27:54+08:00 |
| 7 | `/api/backtest/snapshots` | 200 | 20 筆日快照 2026-08-25~09-23，17 筆 sharpe_short 非 0 | 2026-09-27T19:30:53+08:00 |
| 8 | `/api/parameters` | 200 | 1669 keys；step_year/valid_length/first_train/test_end 各 0 命中 | 2026-09-27T19:27:54+08:00 |

**非 HTTP 的代理驗證（2026-09-27）**
- `atlas/internal/backtest/rolling_split.go`（讀原始碼）註解明寫「following the SK-03 specification」,且 `NewRollingWindowSplit()` 預設值 **FirstTrainEnd=2007-12-31 / ValidLengthYears=2 / StepYears=1 / TestEnd=2022-04-30 / stopYear=2020** 與本頁 §論文版概念 逐項相同。
- `atlas/cmd/backtest-pipeline` 以旗標 `-first-train-end / -valid-years / -step-years / -test-end` 暴露同一組三軸。
- 結論修正:**三軸不是「atlas 沒有」,而是「不在 MCP／HTTP 面」** —— MCP 與 `/api/parameters` 皆無此三軸,要走 CLI 或直接呼叫 `internal/backtest` 套件。

**更正（2026-09-27）**
- 頁內「147 sessions 對位」為 2026-08-02 快照;今日端點回 90（滾動窗）。
- `universe_get_session_detail` 的真實路徑是 `/api/dashboard/sessions/{session_id}`;`.../latest` 回 404（與 SK-37 同日同結論）。

## 未消化 / 待補
- [ ] `universe_get_session_detail` 對 valid 段是否有獨立的 metrics(不是 test 段的子集)?若無,「valid 沒過就停下」的 SOP 在 atlas 沒有對位工具。
- [ ] SK-03 預設 `first_train_end=2007-12-31` 對台股是否太舊?散戶資料深度通常不到 2007,需評估是否下修到 2015（2026-09-27 實測:atlas `rolling_split.go` 預設同為 2007-12-31,故此問同樣適用 atlas）。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:時序切分需對位 7 時期切換,不同時期最佳滾動窗口不同)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)