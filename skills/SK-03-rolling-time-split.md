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
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 pandas 三段式滾動切分完成(train 168 月 1994-01~2007-12 / valid 24 月 2008-01~2009-12 / test 144 月 2010-01~2021-12),atlas 端 universe_get_sessions 147 sessions 對位;atlas 端未暴露 first_train_end/valid_length_years/step_years 三軸,需 `parameters_get` 或源碼確認;論文 1994-2022 規格以 test 結束 2021-12 簡化(2022-04 為單月切尾)。
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

**沒有對位的部分**:SK-03 的 `valid_length_years=2` 與 `step_years=1` 兩個獨立參數在 atlas 沒有外部暴露欄位,只能從 `universe_get_session_detail` 反推。

## 散戶解讀(GROW+ 引用點)
- **R 段(現狀)**:用戶問「為什麼回測看起來好、實盤卻虧損」→ 多半是「只看 test 段、沒看 valid 段」造成的過擬合錯覺。SK-03 提醒:valid 段才是策略真正「驗收」的考試。
- **+E 段(風險)**:強調「滾動是必須,不是可選」——若每年只回測一次、不滾動,2020 疫情或 2022 升息這種 regime 切換會被錯過。
- 對位 ATLAS_METHODOLOGY 七時期:每次滾動對應一次「時期重判」,valid 段是 regime 切換壓力測試。

## 驗證方式
Step 1: 呼叫 `universe_get_sessions` 確認近 90 天 session 數量與切分頻率(月/季/半年)。
Step 2: 抽一個 session,呼叫 `universe_get_session_detail` 確認 train/valid/test 三段日期範圍與 SK-03 定義是否一致(預期 valid 在 test 之前、test 跨年)。
Step 3: 呼叫 `risk_get_metrics` 比對該 session 樣本外指標(drawdown、Sharpe)是否反映 valid+test 兩段,而不是只看 test。

## 未消化 / 待補
- [ ] atlas 是否允許自訂 `step_years`?目前 `backtest_signals` 回傳的 active_signals 沒暴露此參數,需查 `parameters_get` 或源碼確認。
- [ ] `universe_get_session_detail` 對 valid 段是否有獨立的 metrics(不是 test 段的子集)?若無,「valid 沒過就停下」的 SOP 在 atlas 沒有對位工具。
- [ ] SK-03 預設 `first_train_end=2007-12-31` 對台股是否太舊?散戶資料深度通常不到 2007,需評估預設值是否該下修到 2015。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:時序切分需對位 7 時期切換,不同時期最佳滾動窗口不同)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)