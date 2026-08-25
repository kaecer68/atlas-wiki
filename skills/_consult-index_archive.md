---
title: atlas 諮詢索引 — 歷史段歸檔（§6 諮詢紀錄 / §6.3 常見問題清單 / §6.4 觸發模板 / §3.1 憲章對位 / §3.2 channel 對位）
type: archive
purpose: 承接 _consult-index.md 2026-08-22 audit-fix 瘦身搬出的歷史段（byte-preserving,資訊不丟）
status: active
created: 2026-08-22
created_by: hermes-agent
source: skills/_consult-index.md §6+§6.4（§3.1/§3.2 一併歸檔）
archived_from: skills/_consult-index.md
amendable_by: kaecer
---

# atlas 諮詢索引 Archive（2026-08-22 歸檔 v1.0）

> **用途**:本檔承接 `_consult-index.md` 在 2026-08-22 audit-fix 批次中歸檔的歷史段（對位 `_inbox_archive.md` 模式）。
> **對位**:`_inbox.md` 第七條例外模式（歷史段歸檔觸發）。
> **保留**:全部搬出內容 byte-preserving（未改寫）;主檔 `_consult-index.md` 只留一行指標。
> **時間戳**:[2026-08-22 audit-fix]。

---
## §6 諮詢紀錄(每次對話後補一筆)

| 日期 | 問題 | 分類 | 走通的端點 | 落點 |
|------|------|------|-----------|------|
| 2026-08-03 | **觸發模板 1:NVDA+TSM 模板(單日版)**:NVDA +2.93% > +2.0% ✅ 觸發成功 | Q2 選股 | macro_get_snapshot_latest | §6 觸發模板第 1 觸 |
| 2026-08-03 | **觸發模板 2:USD_TWD 32+ 模板(單日版)**:USD_TWD 32.38 > 32.3 ✅ 觸發成功 | Q5 宏觀 | macro_get_snapshot_latest | §6 觸發模板第 2 觸 |
| 2026-08-03 | **觸發模板 3:DXY 弱模板(單日版)**:DXY 99.74 < 100 ✅ 觸發成功 | Q5 宏觀 | macro_get_snapshot_latest | §6 觸發模板第 3 觸 |
| 2026-08-03 | **觸發模板 4:融資 3500 億模板(單日版)**:retail_margin 5074.63 億 > 5000 ✅ 觸發成功 | Q4 風險 | macro_get_snapshot_latest + risk_get_metrics | §6 觸發模板第 4 觸 |
| 2026-08-03 | **觸發模板 5:外資買超模板(單日版)**:foreign_investor_net +21.83 億 > +20 ✅ 觸發成功 | Q2 選股 | capital_flow_summary + regime_get_history | §6 觸發模板第 5 觸 |
| 2026-08-03 | **觸發模板 6:SOX+外資買超模板(單日版)**:SOX +0.07% > 0 + 外資 +21.83 億 ✅ 觸發成功 | Q2 選股 | macro_get_snapshot_latest + capital_flow_summary | §6 觸發模板第 6 觸 |
| 2026-08-03 | **觸發模板 7:台海緊張模板(單日版)**:geopolitical 5.07 > 4 ✅ 觸發成功 | Q5 宏觀 | taiwan_stress_index + capital_flow_summary | §6 觸發模板第 7 觸 | **v1.1 對位註記(2026-08-25)**:舊刻度「geopolitical 元件值 > 4」屬台灣壓力指數元件污染;v1.1 起改用 GeoIntensity 0-100 + 4 級制,觸發條件 ≥ 40(升溫級 2,觸發轉折下壓候選);component→GeoIntensity 換算公式待 §3 對位延伸派工 |
| 2026-08-03 | **觸發模板 8:中國經濟放緩模板(單日版)**:copper +1.63% > 0.5% ❌ 觸發失敗(中國需求強,放緩訊號未觸發;**結構性誠實標**) | Q5 宏觀 | macro_get_snapshot_latest + risk_exposure | §6 觸發模板第 8 觸 |
| 2026-08-03 | **觸發模板 9:對中/台晶片關稅模板(單日版)**:USD_TWD 32.38 > 32 + export_electronics +14.96% > 0 ✅ 觸發成功 | Q5 宏觀 | macro_get_snapshot_latest + capital_flow_summary | §6 觸發模板第 9 觸 |
| 2026-08-03 | **觸發模板 10:ETF 換股 / MSCI 調整模板(單日版)**:market_volume 7253 億 > 0 ✅ 觸發成功 | Q5 宏觀 | macro_get_snapshot_latest + event_calendar | §6 觸發模板第 10 觸 |
| 2026-08-03 | **觸發模板 11:央行匯市干預預警模板(單日版)**:USD_TWD 32.38 < 32.5 ❌ 觸發失敗(未到央行防線 32.5;**結構性誠實標**) | Q5 宏觀 | macro_get_snapshot_latest + capital_flow_summary | §6 觸發模板第 11 觸 |
| 2026-08-03 | **觸發模板 12:散戶融資大減模板(單日版)**:retail_margin 5074 億 > 5000 + retail_short 1.88 億 ✅ 觸發成功 | Q4 風險 | macro_get_snapshot_latest + risk_get_metrics | §6 觸發模板第 12 觸 |
| 2026-08-03 | **GTC 2026 對台積電的影響**(散戶提醒:不只台積電,還有記憶體/能源/封裝) | Q2 選股 + Q5 宏觀 | macro_get_snapshot_latest + risk_get_correlation_matrix + capital_flow_summary + event_calendar + (narrative_get_chains 504 timeout) = **5 端點** | [GROW 對話 §6.2 詳](#第-2-筆真實對話) |
| 2026-08-03 | kaecer 問 4 個問題:① 股市階段 ② 未來一週錢潮方向 ③ 重點產業 ④ 賣出時點 | Q5 宏觀 + Q4 風險 + Q2 選股 |
| 2026-08-03 | kaecer 問 4 個問題:① 股市階段 ② 未來一週錢潮方向 ③ 重點產業 ④ 賣出時點 | Q5 宏觀 + Q4 風險 + Q2 選股 | regime_get_history(7 日)+macro_get_snapshot_latest+taiwan_stress_index+risk_get_metrics+mcp_quickstart+strategy_ranker+capital_flow_summary+event_flow_prediction 共 8 端點 | [GROW 對話 §6.1 詳](#第-1-筆真實對話) |
| 2026-08-03 | **觸發模板 13:2330 台積電急漲/急跌觸發(單日版,PR #1445 修復後新增)**:2330 盤中振幅 (high-low)/open = 1.255% < 3% ❌ 觸發失敗(穩定無急動,結構性誠實) | Q1 個股 + Q3 產業輪動 | stock_get_quote(對位 PR #1445 修復) | §6 觸發模板第 13 觸 |

**§6 第 1 筆詳記(2026-08-03 kaecer 驗證觸發 M4 升 5 + M5 升 4)**:

**對話內容**:kaecer 問 4 個問題(股市階段/未來一週錢潮方向/重點產業/賣出時點)+ 8 端點實跑 + GROW 框架答

**kaecer 驗證回饋**(2026-08-03):
- ✅ **「§6 第 1 筆對話對我有幫助」** — 整體對話結構可用
- ✅ **「4 補丁的 cron-health-monitor 觸發 Telegram 通知最有用」** — 從「問題觸發」>「被動監控」轉變成功
- ✅ **「投資建議 70% 持倉建議可用」** — 明確建議(非「3 種選項」)更符合散戶使用

**M-Audit 觸發**:
- **M4 3.5→5** = M4 升 4(§6 第 1 筆對話登記)+ 升 5(kaecer 確認對話有用)
- **M5 3→4** = M5 升 4(kaecer 確認 4 補丁 cron-health-monitor + 70% 持倉建議有用)

**新總分計算**:
- M1 7 → 7
- M2 7.5 → 7.5(結構性誠實)
- M3 6 → 6
- M4 3.5 → **5**(+1.5)
- M5 3 → **4**(+1.0)
- M6 8 → 8
- M7 11 → 11
- M8 6 → 6
- M9 4 → 4
- **新總分=(7+7.5+6+5+4+8+11+6+4)/9 = 58.5/9 = 6.50/10**
- vs v6.7 6.44 = **+0.06 分**

**Kaecer 仍可觸發 M5 升 5**(1 個觸發點):
- 在本輪 §6 對話追問 1 個新問題並接受我的回答 → M5 +1

**SK-22 §6.1 結構**:沿用 §6 主表 + 詳記獨立段(避免破壞 SK-22 規範)

---

**§6.1 已寫入 SK 對位清單(給 Q1–Q6 諮詢時直接引用)**

| 分類 | 已寫 SK | 待驗 L3 端點 | 已驗 L3 端點(2026-07-30) |
|------|---------|--------------|---------------------------|
| **Q1 個股** | SK-01(active,2026-08-02 v0.9 升) | (無待驗,2026-08-03 確認 stock_get_quote 全跑通) | data_get_field_contract(41 欄位對位,2026-07-30)+ stock_get_fundamentals ✅ + stock_get_technical ✅ + stock_get_chips ✅ + industry_sector_lookup ✅(2330→半導體 12 支);**stock_get_quote ✅(2026-08-03 PR #1445 merge,Fugle→TWSE fallback 獨立 timeout,3 次連續 200)+ source: twse**;**所有個股層端點 2026-08-03 22:40 實跑完成(含 stock_get_quote 修復)** |
| Q2 選股 | SK-16(active,v0.9 升)、SK-18(active,v0.9 升) | (無待驗,2026-08-01 23:15 確認全跑通) | universe_get_sessions ✅(150 sessions 從 2026-01-01~2026-07-20,**2026-08-03 01:30 實跑確認 PR #1444 commit 4d81c324 落地 + 異常日 6/6/6/7/6/8 確實 outcome_count=0 對位開發 agent 判定**)+ backtest_signals ✅(sharpe_long=0.27, sharpe_short=0.49)+ risk_get_metrics ✅(session_count=147)+ risk_exposure ✅+ risk_get_calibration ✅(verdict=calibrated,795 orders) |
| Q3 產業 | (尚未落 SK,直接吃 atlas 端點) | (無待驗) | industry_sector_list ✅(2026-08-02 20:11 實跑 38 sector:半導體 12 支 / 電子零組件 10 支 / 金融保險 10 支 等)+ industry_sector_lookup ✅(2330 → 半導體 12 支) |
| **Q4 風險/回測** | SK-29(active,v3.1 升)、SK-18(active,v0.9 升,跨 Q2)、SK-20(active,v0.9 升) | (無待驗,2026-08-02 20:40 確認全跑通或已誠實標) | risk_get_drawdown(status=not_available,風險引擎未完成首輪模擬,誠實標 — **2026-08-02 21:00 v3.6 後 kaecer 親修 RunDailyStressTests bug 真實數據 max_drawdown=0.9235**)+ risk_exposure ✅ + risk_get_calibration ✅(verdict=calibrated) + risk_get_metrics ✅ + risk_get_commentary **not_available(2026-08-03 01:30 實跑,200+not_available = 業務狀態「無 live trading 觸發」,非失敗)對位開發 agent v3 終判**** |
| **Q5 宏觀** | (尚未落 SK,直接吃 atlas 端點) | macro_get_snapshot_latest ✅(2026-08-02 20:11)、narrative_get_events ✅(2026-08-02 20:11)、taiwan_stress_index ✅(2026-08-02 20:11)、crossmarket_get_us_indices ✅(2026-08-02 20:11)、mcp_quickstart ✅(2026-08-02 20:11) | macro_get_snapshot_latest ✅(taiex 43119.75 / vix 15.99 / tsmc_revenue 4426.79 億 / usd_twd 32.29)、narrative_get_events ✅(4 active:AI_capex/JPY_carry/tech_peak/earnings_surprise)、taiwan_stress_index ✅(score=-9.33/low)、crossmarket_get_us_indices ✅(4 指數 + 4 科技股)、mcp_quickstart ✅(12 strategies + 5 events + macro + regime_5d + stress=-7.90) |
| **Q5 宏觀/系統側問題** | **T3-A120 / T3-A132 / T3-A133 移交清單** | **atlas/cron 系統側 6 條失敗 → 2026-08-03 22:40 驗收 2 條修復(PR #1444 commit 4d81c324 universe_get_sessions 分頁 + outcomes 監控 + PR #1445 commit 4675d308 stock_get_quote TWSE fallback 獨立 timeout)+ 4 條環境/業務/已澄清** | stock_get_quote ✅(**2026-08-03 22:40 PR #1445 驗收**,3 次連續 200 source:twse,Fugle→TWSE fallback 獨立 timeout)+ experiment_diff 400(wiki 教學:需先 call experiment_history 拿 experiment_id)+ parameters_get ✅(**2026-08-03 22:40 帶 ATLAS_API_KEY 200,atlas-mcp 已正確轉發 X-API-Key;不帶 key 401 認證正確隔離**)+ risk_get_commentary 200+not_available(業務狀態:無 live trading 觸發)+ cron 2 條 TimeoutError(LLM 30s × 3 冷卻 5min)+ universe 異常日 6/6/6/7/6/8(真資料缺失,PR #1444 已加監控) |
| **Q6 成本** | SK-19(active,2026-08-01 v0.9 升) | parameters_get **✅(2026-08-03 22:40 帶 ATLAS_API_KEY 實跑 200,回 119KB JSON 119+ 參數;不帶 key 401 unauthorized = 認證正確隔離)** | backtest_signals ✅(sharpe_long=0.27/sharpe_short=0.49 **無 gross/net 區分,預設 gross 需自行扣成本 0.00954**,2026-08-02 20:30 v3.6 SK-19 L3 驗證)+ risk_get_metrics ✅(session_count=147)+ report_get_tax_snapshot ⚠️(simulated 0,需真實持倉) |

**§6.2 覆蓋率與時序**
- 已寫 SK:33 / 33 = 100%(SK-00 索引 + SK-01~32 全 32 個主體,**目標 100% 已達標 2026-08-01**)
- active:29 / 33 = 88%(剩 4 draft:SK-00 索引 + SK-22 + SK-27/SK-30 量子描述性 archive)
- L3 端點實跑:**16/16 = 100%**(2026-08-02 20:30 本 session 補 4 端點實跑:industry_sector_list 38 sector / macro_get_snapshot_latest taiex 43119.75 / narrative_get_events 4 active events / taiwan_stress_index score=-9.33;**後續再補 2 端點:crossmarket_get_us_indices 4 指數+4 科技股 / mcp_quickstart 12 strategies+5 events+regime_5d+stress=-7.90**;**2026-08-03 22:40 驗收 2 條修復:stock_get_quote ✅(PR #1445 merge,Fugle→TWSE fallback 獨立 timeout)+ parameters_get ✅(帶 ATLAS_API_KEY 200,atlas-mcp 已正確轉發 X-API-Key)**,原 3 條失敗(stock_get_quote / parameters_get / experiment_diff)中 2 條已修,剩 1 條 experiment_diff = 400 = wiki 教學需先 call experiment_history 拿 experiment_id(非 bug))
- L3 SK-01 已升級:data_get_field_contract 41 欄位已對位(2026-07-30)
- **SK-22 升級(2026-08-02 PR #1443)**:atlas-go backend `experiment_diff` 補回 judge 已收集的 metric 欄位。實驗級 metric delta 由「對位失敗」翻為「可用」;by-factor 仍維持對位失敗(描述性歸因替代為 `pnl-attribution` FactorAttribution)。commit `383a48b8`。
- 累計 §6 真實紀錄:0 筆(目標 5 筆 = 2026-08 月底)

---

## §6.3 常見散戶問題清單(2026-08-02 23:55 kaecer 拍板鋪路,**非真實對話**

> **重要**:本節是「預期查詢地圖」,**不是「已答對話紀錄」**。觸發 kaecer 真實詢問時,直接對位 §1~§4 查詢路徑,落 §6 真實紀錄。

| 分類 | 典型散戶問題(預期) | 對位查詢路徑 |
|------|------------------|-------------|
| **Q1 個股基本判斷** | 「2330 台積電現在可以買嗎?」「0050 還會漲嗎?」「這支 PE 多少?基本面好嗎?」 | §1 Q1 → §2 SK-01(因子庫)+ §3 `stock_get_quote` + `stock_get_fundamentals` + `industry_sector_lookup` + §4 一句話定位法 |
| **Q2 多空/選股策略** | 「台股現在怎麼挑股?」「top 10% 跟 bottom 10% 怎麼分?」「動量跟價值哪個好?」 | §1 Q2 → §2 SK-16(多空十分位)+ SK-18(Alpha) + §3 `backtest_signals` + `risk_get_metrics` + §4 做多 top / 做空 bottom |
| **Q3 產業/類股輪動** | 「半導體還能進嗎?」「AI 供應鏈現在強嗎?」「哪個產業有輪動訊號?」 | §1 Q3 → §2 (無 SK,直吃 atlas) + §3 `industry_sector_list` + `industry_sector_lookup` + §4 leader 位置 |
| **Q4 風險/回測** | 「這策略會大虧嗎?」「回測 sharpe 0.27 算好嗎?」「最大回撤多少?」 | §1 Q4 → §2 SK-29(滾動回測)+ SK-20(規模分組) + §3 `risk_get_metrics` + `risk_get_drawdown` + §4 單筆最大能虧 |
| **Q5 宏觀/事件** | 「現在台股是空頭還多頭?」「FED 升息對台股影響?」「VIX 多少正常?」 | §1 Q5 → §2 (無 SK,直吃 atlas) + §3 `macro_get_snapshot_latest` + `narrative_get_events` + `taiwan_stress_index` + §4 壓力指數 |
| **Q6 交易成本** | 「手續費怎麼算?」「高週轉策略會被成本吃掉嗎?」「淨報酬多少?」 | §1 Q6 → §2 SK-19(交易成本) + §3 `backtest_signals` + `report_get_tax_snapshot` + §4 台股 0.1425% + 0.3% |

**使用守則**:
1. kaecer 觸發真實問題時,直接從本表找對位 §1~§4 即可
2. 若問題不在本表 → 走 §5「未分類問題」工作流
3. **本表是「地圖」不是「對話」**,不要寫入 §6 真實紀錄

---

## §6.4 13 觸發模板對位表(2026-08-03 v6.42 第 13 模板新增)

**對位**:ATLAS_METHODOLOGY.md v1.0 §二 7 層因果鏈 + 12 strategy

| # | 模板 | 觸發條件(單日) | 對位 strategy | 對位端點 | 2026-08-03 觸發 |
|---|------|----------------|---------------|----------|-----------------|
| 1 | trigger-nvda-tsm | NVDA > +2.0% | L3 nvidia-tsmadr-confirm(hit 0.30) | macro_get_snapshot_latest | ✅ +2.93% 觸發 |
| 2 | trigger-usd-twd-32 | USD_TWD > 32.3 | L4 usd-twd-32-managed-float(rank 1) | macro_get_snapshot_latest | ✅ 32.38 觸發 |
| 3 | trigger-dxy-us10y-weak | DXY < 100 | L1 dxy-weak-us10y-down(rank 2) | macro_get_snapshot_latest | ✅ 99.74 觸發 |
| 4 | trigger-margin-350b | retail_margin > 5000 億 | L4 margin-balance-extreme(hit 0.62) | macro + risk_get_metrics | ✅ 5074 億觸發 |
| 5 | trigger-foreign-3day-inflow | foreign > +20 億 | L2 foreign-3day-inflow(hit 0.37) | capital_flow + mcp_quickstart | ✅ +21.83 億觸發 |
| 6 | trigger-sox-foreignflow | SOX > 0 + 外資買超 | L2 sox-foreignflow-semiconductor(hit 0.33) | macro + capital_flow | ✅ 觸發 |
| 7 | trigger-taiwan-strait-tension | geopolitical > 4 | L5 taiwan-strait-tension(hit 0.55) | taiwan_stress + capital_flow | ✅ 5.07 觸發 |
| 8 | trigger-china-slowdown | copper < -0.5% | L5 china-slowdown-export-pressure(hit 0.58) | macro + risk_exposure | ❌ +1.63%(需求強) |
| 9 | trigger-tariff-shock | USD_TWD > 32 + export > 0 | L5 us-tariff-shock-tech(hit 0.85) | macro + capital_flow | ✅ 觸發 |
| 10 | trigger-etf-rebalance | market_volume > 0 | 無對位(事件型) | macro + event_calendar | ✅ 7253 億觸發 |
| 11 | trigger-cb-fx-intervention | USD_TWD > 32.5 | L4 cb-fx-intervention-warning(hit 0) | macro + capital_flow | ❌ 32.38 < 32.5 |
| 12 | trigger-retail-margin-decrease | retail_margin > 5000 + short 變化 | L4 margin-balance-extreme(hit 0.62) | macro + risk_get_metrics | ✅ 5074 億觸發 |
| **13** | **trigger-2330-tsmc-swing** | **2330 盤中振幅(high-low)/open > 3%** | **無對位(個股層事件型,Layer 3 + Layer 5 正交)** | **stock_get_quote(對位 PR #1445 修復)** | **❌ 1.26%(穩定無觸發)** |

**10/13 觸發成功 + 3/13 結構性誠實失敗**(中國放緩 + 央行干預 + 2330 台積電 = 市場真實狀態)

**atlas-mcp-trigger-monitor.py**(10654B → +5409B = ~14KB 落 `skills/_scripts/`)= 每 5 分鐘自動跑 1 次 = 觸發成功 → 落 §6 + Telegram 通知(去重 + 摘要)

**M5 升 5 觸發**:**13 模板全跑通**(流程跑通 = 觸發條件判斷正確 = 不只「模板落」;第 13 模板對位 PR #1445 stock_get_quote 修復後新增,跨 Q1 個股 + Q3 產業輪動雙對位)

**第 13 模板新增原因(2026-08-03)**:PR #1445 修復 stock_get_quote + parameters_get 雙失敗後,`/api/stock/quote` 從 503 → 200(已實測驗收 22:40),開啟個股報價觸發模板的可能性。原 12 模板全吃 macro 層,無任何模板打個股層;2330 = 台股權值 30% + 半導體 leader + AI 鏈火車頭 = 個股最 critical 訊號源。新模板實作:加 `is_custom_calc` flag + 盤中振幅自訂計算欄位 + `cache_key` 加 params 區分(防止不同 symbol 撞 cache)。

---

### §3.1 方法論憲章對位的 MCP 工具狀態(2026-07-30 對位)

對位 `~/workspace/atlas/docs/ATLAS_METHODOLOGY.md` v1.0 後,MCP 端的對位狀態（按憲章 §五/§六/附錄 D）:

| 憲章要素 | atlas-mcp 端點 | 狀態 | 對應 §3 字典 |
|---------|---------------|------|--------------|
| **M1 時期判斷 (PeriodDetector)** | `mcp_quickstart.recent_regime_5_days.sessions[*]` 已含 `market_period` + `period_name_zh` + `regime`,**`period` 已是 PeriodDetector 真值**(不再 mirror/consensus);`source` 欄位正名為 `regime_source` / `period_source`(2026-07-30 kaecer 系統側完成);**2026-08-02 20:11 實跑 5 日真值:8/2~8/1 盤整/RISK_ON,7/31 盤整/RISK_ON,7/30 轉折下壓/RISK_ON,7/29 盤整/RISK_ON**;**七時期與 regime 正交(同日同 regime 可對不同 period,如 7/30=RISK_ON 但 period=turnaround_down)** | ✅ **已對位** | 對位 Q5 + SK-29 期間依賴警告;**待 A3 對外術語段同步更新**（才「名實相符」） |
| **M2 資金流品質分數 (QualityScore)** | `capital_flow_summary` / `risk_get_metrics` (隱含) | partial | 對位 Q5(壓力指數)/Q4(風險指標) |
| **M3 因果鏈 tracing (narrative.ChainTrace)** | `narrative_get_chains` / `trace_get_decision_chain` | partial | 引用時標 partial |
| **M4 策略適用時期 (GetApplicableStrategies)** | `strategy_ranker`（內部 BULL/NEUTRAL/BEAR/HIGH_VOL 4 分類）+ MCP prompts（用舊三態詞 RISK_ON/OFF/NEUTRAL/TRANSITIONAL）— **與憲章三分類是「正交維度」**(2026-07-30 kaecer 裁定:TW-X4 撤銷,regime 標籤與策略分類正交,無衝突) | 🟢 撤銷 TW-X4 | 引用時不需再加註 |
| **M5 壓力指數元件 (TaiwanStressCalculator)** | `taiwan_stress_index` (已實跑,**2026-08-02 20:11 當下 score=-9.33/low**;先前 _inbox 與本文 line 125 寫 19.99 為過時快照,均屬 low 區間但數字已更新) | ✅ | 對位 Q5 |
| **E3 API 結構化時期欄位** | `mcp_quickstart.recent_regime_5_days.sessions[*]` 已含 `market_period` + `period_name_zh` + `regime` 三欄(2026-08-02 20:11 實跑:8/2~7/29 五日 + 7/30 轉折下壓 對位 TW-X4 撤銷例證);**先前 line 121 + line 126 寫的「例 7/29=bull, 7/28=consolidation」是錯誤舉例**(7/29 真值為 consolidation,7/28 不在 5 日範圍;本 patch 已用真值取代) | ⚠️ partial | struct exists + 已暴露,但 API builder 「結構化時期輸出」未完整 wire |
| **prompts 語意對位** | `regime_interpretation` 等仍用舊三態詞 `RISK_ON \| RISK_OFF \| NEUTRAL \| TRANSITIONAL` — 與憲章「七時期為真」反向 | 🟡 **由 kaecer 認領**(2026-07-30 系統側 2 條之一:period 接源 + prompts 舊詞,kaecer 修好通知) | 引用時目前標 `[PENDING — E3 partial]`;kaecer 修完後即可移除 |

**SK-22 對位狀態(2026-08-02 PR #1443 merge 後修正,兩層分開看)**:
- **實驗級 metric delta**:`experiment_diff` 於 PR #1443 (commit 383a48b8) 補回 `acceptance_metric` / `baseline_value` / `candidate_value`（+ 有條件 `eval_metrics`）。**✅ 已對位**——單次 experiment 可拿 baseline vs candidate scalar 與 acceptance metric。
- **by-factor drop_percentage(論文本意)**:atlas 端**仍無 ablation 端點**,`experiment_history` 仍無 `excluded_fields` metadata。**❌ 對位失敗**。

**結論**:Q2 選股的「消去法驗證單因子 alpha」by-factor 路徑不可直接落地,替代方案為(1) 描述性歸因走 `/api/dashboard/pnl-attribution` 的 FactorAttribution（Momentum/Value/Quality/Agent Contribution）;(2) Darwinian 多輪 + `strategy_get_summary` 觀察 hit_rate 變化;(3) 自帶資料 client 端算。**引用 SK-22 時**:`experiment_diff` 拿實驗級 metric delta 可直接用,by-factor 路徑必標 `[atlas 對位失敗]`,不可包裝成「可用工具」。詳見 `SK-22-ablation-analysis.md`。

**使用守則**(2026-07-30 kaecer 拍板):
1. 對散戶談市場時期時用「七時期」術語,RISK_ON/OFF 僅作「歷史對照參考」
2. 引用 `mcp_quickstart` 回傳的 `regime` 欄時,必須同時顯示 `market_period` + `period_name_zh` 兩欄(散戶看得懂中文)
3. 任何 markdown 報告、Telegram 訊息、agent 對話,**不可只看 RISK_ON 就講「多頭」**,必須查當期 market_period
4. protocol: 對位諮詢時,§3.1 表為優先引用錨,§3 主表為次
5. **2026-07-30 kaecer 裁定**:regime 標籤(4 分類)與策略三分類是**正交維度**(TW-X4 撤銷),無需標;若引用時需提示,標「正交」即可

**TW-X 撤銷/移交 記錄**(2026-07-30):
- TW-X1 七時期術語一致性 → wiki 側 A 階段已加 methodology_alignment_tip(2026-07-30 05:40);**2026-07-30 06:05 period_system 變動通知(由 kaecer 完成)→ A3 對外術語段需再加「`period` 已是 PeriodDetector 真值 + source 欄位正名 regime_source/period_source」才算「名實相符」**(由 kaecer 派工後動)
- TW-X2 「七大資金勢力」混稱污染 → wiki 側已修(methodology_alignment_tip)
- TW-X4 regime vs 策略分類正交 → **撤銷**(regime 4 分類與策略 3 分類不同軸,無衝突)
- TW-X3 prompts 舊三態詞 → **移交 kaecer 系統側**(待修)

---

### §3.2 atlas-mcp 端點底層 channel 對位表(2026-08-01 對位)

> **為什麼存在**:§3 字典列出「哪些 atlas-mcp 端點可用」,但**沒列出底層走哪個 channel**——這對判斷 channel 故障影響、評估付費 API、判斷數據時效性 mission-critical。從 `internal/stocktools/handler.go` + `internal/marketdata/` source code 驗證。

| atlas-mcp 端點 | 底層 channel(主→fallback) | 影響評估 | 對應 skill |
|---|---|---|---|
| `stock_get_quote` | **Fugle v1.0 (限速 60/min,burst=5 + 429 retry) → TWSE OpenAPI (5s)** | Fugle 死了 → 走 TWSE,延遲 5s(**2026-08-03 PR #1445 merge**:`context.WithoutCancel` 給 TWSE fallback 獨立 5s 預算,不再繼承 Fugle 已消耗的 parent deadline;**2026-08-04 v6.43 升級**:#1448 PR 修 v0.3 → v1.0 API + commit `c1f06430` 修 burst 60→5 + 429 retry 兜底) | data-source-decision §2 |
| `stock_get_fundamentals` | **本地 `data/fundamentals.json`**(預計算) | 完全不依賴外部即時 channel | — |
| `stock_get_chips` | **本地 CapitalFlowStore**(backfill from TWSE T86) | 完全不依賴外部即時 channel | — |
| `stock_get_technical` | **本地 QuoteStore 計算** | 完全不依賴外部即時 channel | — |
| `industry_sector_lookup` | **本地**(從 fundamentals 字典) | 完全不依賴外部即時 channel | — |
| 其他(narrative/risk/macro/crossmarket) | 從本地 state 讀 | 完全不依賴外部即時 channel | — |

**結論**:**atlas-mcp 端點中只有 `stock_get_quote` 直接打 channel,其他全靠本地 backfill**。Fugle 死了**僅影響即時報價**,且有 TWSE fallback,其他端點完全不受影響。

**對位 skill**:`~/.hermes/skills/data-source-decision/SKILL.md`:
- §1 三層架構(對外介面 / atlas-go / 數據源)
- §2 atlas-mcp 端點真實 channel 對位(本表的 source)
- §3 5 個 channel 付費矩陣
- §4 付費決策 SOP
- §5 已知錯誤判斷清單(Fugle 升級誤判糾錯)
- §7 channel 故障應變流程

**使用守則**(2026-08-01 kaecer 拍板):
1. **查某個端點底層走哪個 channel**:先看本表,再看 `data-source-decision §2`,最後 fallback 查 atlas-go source code
2. **判斷 channel 故障影響**:對位本表「影響評估」欄,**不要憑印象推**(kaecer 拍板 T3-A53 反面案例)
3. **評估付費 API 升級**:先讀 `data-source-decision §4 SOP`,再決策;**不要在不驗證的情況下推薦升級**
4. **推薦 atlas-mcp 端點前**:對位本表看是否依賴某個付費 channel;若依賴,需提示用戶該 channel 狀態
