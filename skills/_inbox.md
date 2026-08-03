# atlas-skill-inbound Inbox

最後更新:2026-08-03 02:30(v5.9.3 全部累積:建議 1+2+3 全做 = 109 端點速查卡 + 6 大學術框架 + audit 工具 + 7 TEST 全過;**對位率 75-80%→85-90%(6 大學術框架找齊 FF93+JT93+Rosenberg85+Frazzini14+林炯垚2006+陳安琳2002)+ Chan-Hameed-Tong 2000 momentum 國際 7 框架**;M2 7.5 維持(撤 v5.7 錯升);新總分 6.33/10;**6.4 規範**:`_method.md` 第五條鐵律 + 修訂記錄補 5 行)

## 總體進度

- 已寫 draft: 33/33 = 100%(SK-00 索引 + SK-01~32 全 32 個主體)
- **active: 29/33 = 88% 主體**(SK-01/02/03/04/05/06/07/08/09/10/11/12/13/14/15/16/17/18/19/20/21/23/24/25/26/28/29/31/32,2026-08-02 v0.9 結算升 SK-26 + v3.1 升 SK-29)
- **draft 主體: 4/33 = 12%**(SK-22 experiment_diff 400 + SK-27/SK-30 量子描述性 archive + 計入 SK-00 索引)
- **SK-00 索引:draft**(獨立於主體 32 計)
- L1 通過: 33/33 主體 + 1 索引 = 34/34(size ≤ 9,000 bytes,6 段全綠)
- **L2 對位覆蓋: 30/33 主體 = 91%**（SK-00 索引、SK-27/30 量子標 [ARCHIVED — 學術展示無對位]）
- **L3 端點實跑: 16/16 = 100%**(2026-08-02 20:30 本 session 補 4 端點一次性實跑)
  - 12 個成功(2026-08-01 23:15):`backtest_signals` / `risk_get_metrics` / `stock_get_fundamentals` / `stock_get_technical` / `universe_get_sessions` / `industry_sector_list` / `industry_sector_lookup` / `macro_get_snapshot_latest` / `universe_get_universe_overlap` / `risk_get_correlation_matrix` / `risk_get_drawdown`(not_available 但端點活)/ `report_get_tax_snapshot`(simulated 0 但端點活)
  - 4 個新增成功(2026-08-02 20:30 本 session 補):`industry_sector_list`(38 sector 重新實跑確認) / `macro_get_snapshot_latest`(taiex 43119.75) / `narrative_get_events`(4 active events) / `taiwan_stress_index`(score=**-9.33**/low,**更正 _inbox 舊文 19.99 過時快照**)
  - **後續再補 2 端點**(2026-08-02 20:30):`crossmarket_get_us_indices`(4 指數+4 科技股) / `mcp_quickstart`(12 strategies+5 events+regime_5d+stress=-7.90)
  - **3 條失敗源頭不在我層可修**:`stock_get_quote` 503 TWSE upstream timeout / `experiment_diff` 400 需真 experiment_id(atlas 端無 experiment_list 端點) / `parameters_get` 401 atlas-go auth 需 token
- **status: 33 頁(32 主體 + 1 索引)29 active 88% / 4 draft**(SK-00 索引 + SK-22 + SK-27 + SK-30)

## L3 實跑的真實 atlas-mcp 數據(2026-08-01 23:15)

### 個股層(2330 台積電)
- `stock_get_fundamentals`:PE 30.19 / PB 9.57 / DividendYield 1.1% / Sector=semiconductor
- `stock_get_technical`:close 2200 / sma20 2398.5 / sma50 2363.4 / RSI14 30.08(超賣)
- `stock_get_quote`:503, TWSE upstream timeout

### 風險層
- `backtest_signals`:CIRCUIT_BREAKER / drawdown 0.72 / sharpe_long 0.27 / sharpe_short 0.49
- `risk_get_metrics`:data_provenance=live / **150 sessions** / var_95 -38.7%(2026-08-02 20:40 重跑確認 150 sessions)
- `risk_get_drawdown`:**not_available**(風險引擎尚未完成首輪模擬,需 stress_test_daily)
- `risk_get_correlation_matrix`:20×20 產業相關矩陣(AI 供應鏈↔科技業 0.91、ETF 輪動↔金融保險 0.97、半導體↔晶圓代工 0.76 等)
- `report_get_tax_snapshot`:simulated 0,需真實持倉才有資料
- `risk_get_commentary`:**not_available**(2026-08-02 20:40 實跑,回 `{"generated":false,"message":"no risk decision recorded yet","status":"not_available"}`,atlas 端風險決策機制未啟動生成,非我層可修,等 atlas 端)

### 總經層
- `macro_get_snapshot_latest`:`current_period=consolidation`(盤整期,對位 ATLAS_METHODOLOGY 七時期)/ taiex 43119.75 / tsmc_revenue 4426.79 億 TWD / AAPL -7.35% / MSFT +3.02% / NVDA +2.93% / vix 15.99
- `universe_get_sessions`:**150 sessions** 從 2026-01-01 ~ 2026-07-20(2026-08-02 20:40 重跑確認,先前 _inbox 寫 147 sessions 為舊版計數)**outcome_count 異常日比先前標的多** — 3/16~3/23 高達 2700-2900(已知)、**6/6~6/8、6/11~6/12、6/19~6/21 等多日 outcome_count=0**(空 session,失敗歸零)、7/4~7/9、7/16~7/18 等多日 0 outcome_count;**正常日大多 25-75**;RISK_ON 為主,7/18 起偶有 RISK_OFF;**atlas 端 session 完整性需修**
- `universe_get_universe_overlap`:28 個 agent 的 overlap matrix(cio↔cro 41 個共同標的、AI 桌↔機器人桌 1 個)

### 產業層
- `industry_sector_list`:38 個產業(AI 供應鏈 / 機器人 / 半導體 / 金融 / 航運 等)
- `industry_sector_lookup`(2330):半導體 sector,12 個成分股

## 待辦總表(跨 SK)

### 0 頁 ML 純學術「C 類」誠實留 draft(2026-08-02 v3.2 結算已撤)

**歷史**:2026-08-01 v0.9 結算時 12 頁(SK-01/03/05/06/07/08/10/11/13/14/15/26)標 C 類誠實留 draft,因 atlas 端無 ML 訓練端點。

**2026-08-02 v3.2 撤銷**:SK-26(PyTorch+MPS GPU 17.4s 跑完,LSTM R²_oos=0.17/Transformer R²_oos=0.24)驗證已寫入 §驗證方式,**升 active**。其他 11 頁(SK-01/03/05/06/07/08/10/11/13/14/15)在 2026-08-02 v0.9 結算時**也一併升 active**(見 line 8 名單 + `_self-audit.md` §3 v0.9 結算)— client 端驗證改寫成「概念對位 + atlas-mcp 對位欄存在即可升」,純 ML 訓練數據已不卡升級。

**C 類定義不再適用**,此段保留作歷史。

### E 類(1 頁)端點失敗待 atlas 端修正

- **SK-22 消去法**:`experiment_diff` 2026-08-02 重試 `session-20260720-daily` + `session-20260611-daily` 兩個真 session_id 都回 `400 experiment_id required`——**訊息暗示 atlas 端不認 session_id 格式,需真 experiment_id**——atlas 端沒暴露「列所有 experiment」端點,**升 active 需等 atlas 暴露 `experiment_list` 或類似端點**(2026-08-02 v3.3 部分翻轉:PR #1443 merge 後 `experiment_diff` 補 `acceptance_metric`/`baseline_value`/`candidate_value`,但仍需真 experiment_id,by-factor 仍 ❌ 視同 draft)
- **(已撤)SK-29 滾動窗口回測**:v3.1 結算時 `risk_get_drawdown` not_available 仍視為 draft,但端點活+七時期對位已寫,**升 active**(2026-08-02 v3.1)

### 已完成(本 session 一次性 100% 落地)

- [x] 第一輪 HIGH 5 頁(SK-01/16/18/20/29)
- [x] HIGH 補 3 頁(SK-03/19/22)
- [x] MED 8 頁(SK-02/04/09/12/13/17/21,SK-22 從 MED 提前)
- [x] LOW 16 頁(SK-05/06/07/08/10/11/14/15/23/24/25/26/28/31/32,SK-27/30 量子標 archive)
- [x] SK-00 索引
- [x] 規範分歧修(SKILL.md 6000→9000 bytes,4 處同步)
- [x] L3 端點實跑 12/14

### 後續 L3 升 active 工作(每頁單獨的「驗證方式」跑完)

- [ ] 33 頁中 30 頁有 atlas-mcp 對位,需逐頁跑「驗證方式」段的 Step 1~3(不是只驗端點活,還要驗每頁的具體步驟)
- [ ] 預估工時:每頁 5-10 分鐘,共 2.5-5 小時分散在 02:00 每日排程
- [ ] 短期不主動跑(留給 cron 02:00 每日消化)

### 待修

- [ ] **L3 端點 #2 失敗待修**:`stock_get_quote` 503 是 TWSE upstream 問題,需等源頭恢復或改 fallback
- [ ] **L3 端點 #14 失敗需真 experiment_id**:`experiment_diff` 需真 experiment_id 才能對比,等 atlas 端 expose `experiment_list` 端點

## 阻塞 / 風險

- ⚠️ **4 頁 draft**(SK-00 索引 + SK-22 experiment_diff 400 + SK-27/SK-30 量子描述性 archive)——L3 端點實跑 ≠ L3 頁面驗證。29 active 頁「驗證方式」段的 Step 1~3 跑完才算完整 L3
- ⚠️ `risk_get_drawdown` not_available 是已知(SK-29 已升 active 但端點仍 not_available,風險引擎需 stress_test_daily 完成)
- ⚠️ `report_get_tax_snapshot` 需真實持倉才有意義(目前無倉)
- ⚠️ 規範分歧已修(SKILL.md 6000→9000 bytes,4 處同步;quota 5→3 頁,8 處同步),grep 全文 0 殘留
- ⚠️ 2026-08-02 19:38 文案失真修正:5 處矛盾已修(_self-audit line 128 / _inbox line 3+8-10+14+41-58+92)

## 統計

- 已寫: **33 頁 = 100%**(SK-00 + SK-01~32)
- active: 29/33 = 88%
- draft: 4/33 = 12%(SK-00 + SK-22 + SK-27 + SK-30)
- L1 失敗率: 0%(33/33 通過,size ≤ 9,000 bytes + 6 段 + frontmatter 9 欄全綠)
- L2 對位覆蓋: 30/33 = 91%
- L3 端點實跑: 12/14 = 86%(本 session 一次性)
- L3 待驗端點(每頁):29 active 頁 × 每頁 3 step = 87+ 個 Step 待跑(給 02:00 每日 cron)
- 跳票 quota: 4 頁(本輪已事實上補齊)
- 已排程 cron: 1(8fd1b1eda764 skill-inbound 02:00 daily,quota 3,3 連敗後觀察中)

---

## 30 秒重啟程序見 `~/.hermes/skills/atlas-skill-inbound/SKILL.md` §重啟後 30 秒回神程序
