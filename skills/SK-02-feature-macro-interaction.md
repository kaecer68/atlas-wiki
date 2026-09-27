---
title: SK-02 特徵擴充：股票-總經交互作用
description: "問「同一檔股在升息年與降息年走勢差這麼多」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-02
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [macro_get_snapshot_latest, stock_get_fundamentals, universe_get_sessions]
verification: 2026-09-27 L3 端點實跑 4 端點全 200（http_code + timestamp 見 `l3_endpoints_probed`;明細與更正見 §驗證方式）。實測更新（第五條鐵律:頁內舊值皆為當日快照）:(1) `macro_get_snapshot_latest` 今日回 **41** 條序列（2026-08-01 記 12、08-22 記 31）,含 taiex/us10y/dxy/vix/usd_twd/oil/gold/jpy 與小寫 `aapl`/`msft`/`nvda`（美股 Yahoo 報價,非總經變數——2026-08-22 註已驗證）;(2) `macro_get_snapshot_history`（`/api/macro/snapshot/timeline`）今日回 2026-08-29~2026-09-27 **30 天連續日頻**快照、`missing_dates` 為 null → 「atlas 無日頻 macro 序列」的待補項已解（移出 §未消化,2026-09-27）;(3) `stock_get_fundamentals` 2330 今日仍回 PE 30.19/PB 9.57/DY 1.1,與 2026-07-30 快照完全相同,而同期 `stock_get_quote` last 由 2395（2026-08-12 SK-34）升至 2475 → fundamentals 為**靜態快照、不隨價更新**,對外引用必標時點;(4) `universe_get_sessions` 今日 90 sessions（2026-08-01 記 147）。歷史:2026-08-01 v0.9 結算跑過 L3 升 active（macro_get_snapshot_latest 當時 12 變數、stock_get_fundamentals 2330 PE 30.19/PB 9.57、universe_get_sessions 147 sessions）。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b1）
l3_endpoints_probed:
  - "/api/macro/snapshot/latest → 200（41 序列）（2026-09-27T19:27:54+08:00）"
  - "/api/macro/snapshot/timeline → 200（30 天日頻、missing_dates null）（2026-09-27T19:29:39+08:00）"
  - "/api/stock/fundamentals?symbol=2330 → 200（PE 30.19/PB 9.57/DY 1.1）（2026-09-27T19:27:52+08:00）"
  - "/api/stock/quote?symbol=2330 → 200（last 2475）（2026-09-27T19:28:18+08:00）"
  - "/api/dashboard/sessions → 200（90 sessions）（2026-09-27T19:27:54+08:00）"

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:特徵工程需對位 7 時期 × 策略三分類,跨 regime 表現可能天差地別)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-02 在 atlas 是「把 SK-01 的 86 個股票因子 × 12 個總經變數,做笛卡兒積展開成 1,118 個交互特徵」,對應 mission「找信息差」的關鍵原料層。

## 論文版概念（忠實還原來源）
- **輸入**:`factor_panel`(SK-01 輸出,MultiIndex [日期,股票])、`macro_df`(日期索引的總經時序)、`include_original=True`(預設保留原始因子)
- **核心動作**:
  1. 對齊 factor_panel 與 macro_df 的日期索引
  2. 對每個 macro_k,廣播到所有股票(同一天所有股票共享 macro 值)
  3. 對每個股票因子 f_j,計算 `f_j × macro_k` → 新欄位命名 `f_j_m_macro_k`(例 `mom12m_m_infl`)
  4. 水平合併原始因子 + 所有交互項 → MultiIndex DataFrame
  5. 可選對交互項標準化
- **預設規模**:86 × 12 = 1,032 個交互項;若 `include_original=True` 則 1,032 + 86 = 1,118 特徵欄
- **關鍵假設**:macro 對所有股票同日同值(無個股 macro 暴露)——若未來要 sector-specific macro 需擴充介面

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 86 個股票因子 | 從 SK-01 因子庫對位的 tool 集合 | `stock_get_fundamentals` / `stock_get_quote` / `stock_get_technical` / `stock_get_chips` |
| 10 個總經變數 | 總經快取(利率/通膨/GDP/匯率) | `macro_get_snapshot_latest` |
| 總經日頻時序 | 30 天日頻快照窗（2026-09-27 實測新增對位） | `macro_get_snapshot_history` |
| 因子時序 | 監管因子層的 session 輸出 | `universe_get_sessions` |
| 交互項命名 | atlas 沒有原生特徵工程層,需外接特徵工程工具 | 缺(待補) |
| 標準化 | atlas 沒有原生特徵標準化 | 缺(待補) |

**差異點**:論文版是純 Python DataFrame 操作,atlas 沒有對應的「特徵工程 orchestrator」,需呼叫底層工具取得原始欄位後,在 client 端(腳本層)做交叉相乘。**這是 atlas 工具鏈的缺口**。

**沒有對位的部分**:
- 沒有原生的「交互特徵 orchestrator」endpoint
- 沒有「特徵標準化」(winsorize / z-score)endpoint
- 沒有「每日 macro 廣播到所有股票」endpoint

## 散戶解讀（GROW+ 引用點）
- **G 段(目標)**:用戶問「為什麼同樣是台積電,在 2022 升息年跟 2019 降息年走勢差這麼多?」 → 這就是 macro × stock factor 的交互項在解的問題。
- **R 段(現狀)**:對位 atlas → 「目前 atlas 沒有一鍵算交互特徵,你需要自己寫腳本:`macro_get_snapshot_latest` 拿 macro × `stock_get_fundamentals` 拿因子,在本地相乘」。
- **+E 段(風險)**:警示「1,118 個特徵若直接餵模型,樣本外會崩——這就是 SK-22 消去法要驗的事」。**對散戶:不要看到 1,118 個特徵就以為資訊更多,過擬合風險同步放大**。

## 驗證方式
Step 1: 呼叫 `macro_get_snapshot_latest` 確認回傳至少 12 個總經變數(利率/通膨/GDP/匯率/股價指數等),記錄欄位名稱。（2026-09-27 實測:41 條,見下表）
Step 2: 呼叫 `universe_get_sessions` 取一份含 100+ 股票的 universe,逐檔呼叫 `stock_get_fundamentals` 抓 PE/PB/殖利率/市值,湊出 86 個股票因子的子集(至少 5 個代表)。
Step 3: 在 client 端做 `f_j × macro_k` 笛卡兒積,確認生成欄位數 ≈ 5 × 12 = 60 個交互項(簡化版),命名格式遵循 `f_j_m_macro_k`。（今日 macro 已 41 條,同法為 5 × 41 = 205）

### L3 端點實跑（2026-09-27）與更正

| # | 端點（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/macro/snapshot/latest` | 200 | 41 條序列 | 2026-09-27T19:27:54+08:00 |
| 2 | `/api/macro/snapshot/timeline` | 200 | 30 天日頻（2026-08-29~09-27），missing_dates null | 2026-09-27T19:29:39+08:00 |
| 3 | `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19 / PB 9.57 / DY 1.1 | 2026-09-27T19:27:52+08:00 |
| 4 | `/api/stock/quote?symbol=2330` | 200 | last 2475（source fugle，trading_day false） | 2026-09-27T19:28:18+08:00 |
| 5 | `/api/dashboard/sessions` | 200 | 90 sessions（滾動窗） | 2026-09-27T19:27:54+08:00 |

- **更正 1（時效）**:第 3 列 PE/PB/DY 與 2026-07-30 記錄逐字相同,但第 4 列 last 已由 2395（2026-08-12 SK-34 記錄）變為 2475 → `stock_get_fundamentals` 是**靜態快照**,不會隨報價重算。任何 PE/PB 引用都要附時點。
- **更正 2（解掉一個待補項）**:第 2 列證明 atlas **有**日頻 macro 序列（`macro_get_snapshot_history` → `/api/macro/snapshot/timeline`,30 天窗、`missing_dates` 為 null、每筆 41 條序列）。原待補項「atlas macro 是否支援日頻」已解,移出 §未消化。
- **仍未解**:交互項 orchestrator 與標準化端點仍不存在（第 1 列的 2262 欄 field-contract 中亦無 normalization／cross-product 端點;SK-01 同日實測）。client 端仍是唯一路徑。

## 未消化 / 待補
- [ ] atlas 沒有「特徵工程 orchestrator」端點,需評估是否要提案給 atlas-go 開新 tool。
- [ ] 86 個完整因子清單需 `data_get_field_contract` 對位驗證(已在 SK-01 待補清單)。
- [ ] 交互項標準化(z-score / winsorize)應在哪一層做?atlas 端 vs client 端需決策。
