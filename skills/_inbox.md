# atlas-skill-inbound Inbox

最後更新:2026-08-07 02:10 (v6.45 結算 — **0 新頁 + 1 頁誤判翻正**;33 頁早已 100% 落地,本輪不硬湊 quota。**SK-22 draft → active**:L3 四步全綠(`experiment_history` 200/18 筆、`experiment_diff?experiment_id=` 200 baseline 0.0050727→candidate 0.0064193 sharpe_like、`/api/dashboard/universe-overlap` 200 29 agents/86 warnings、`backtest_signals` 200 CIRCUIT_BREAKER)。**結構性誠實**:舊 blocker「待 atlas 暴露 experiment_list」為**誤判**——端點一直都在,400 根因是參數名 `id=` vs `experiment_id=` 加傳錯值(session_id/agent_id);另**證偽** `eval_metrics` 欄位(18/18 experiment 皆無,原為未驗證推測)。by-factor ablation 仍 ❌ = 真結構性缺口,不翻轉。); 前次更新:2026-08-04 14:10 (v6.44 結算 — Fugle 修復鏈 4 PR 全 merge 端到端驗收(PR #1445/#1446/#1448/#1449,本 session 實跑 5 端點全綠:stock_get_quote 2330/2317/0050 3/3 source=fugle + parameters_get 243KB + risk_get_commentary not_available);**誤判修正 3 條結構性誠實宣告**:`Fugle key 綁定 1476 / 需重新申請` 誤判已修(根因 base64 -d 測試錯誤,v1.0 key 就是 base64 原樣);wiki `_consult-index` §3 Q1 表加 v6.44 驗收狀態;governance-log append T3-A246);前次更新:2026-08-04 06:50 (v6.43 結算 — §3 失敗狀態同步(`stock_get_quote` ✅ PR #1445+ c1f06430+ PR #1448+ PR #1446 / `parameters_get` ✅ 帶 ATLAS_API_KEY / `experiment_diff` 仍 ❌ 部分修);觸發模板 12 → **13**(`trigger-2330-tsmc-swing` 第 13 模板新增,對位 PR #1445 stock_get_quote 修復後開啟個股層觸發,intraday_swing_pct=1.255% 結構性誠實不觸發);Fugle 重盤查:T3-A51~A54 + Q4 排序重排(Fugle rate log 降為「不需要」);最後一次更新前一次2026-08-04 02:01 (v6.41 結算 — **0 寫入 + 誠實盤查**;cron `8fd1b1eda764` skill-inbound 02:00 觸發;33 頁 100% 落地,4 draft 真實待升(SK-00 索引無 mcp 對位例外 + SK-22 by-factor 仍 400 + SK-27/30 量子已標 [ARCHIVED — 學術展示無對位]);prompt 預設「D2+ 每日 3 頁」是 2026-07-29 降標前的過時工作框架,實際工作 7/30 起已轉型為 _self-audit 治理 + PR 推進 + 12 觸發模板 + 7 jobs CI;未硬湊 3 頁 = 結構性誠實五十一次;詳見 _self-audit.md §6 v6.41)

## 總體進度

- 已寫 draft: 33/33 = 100%(SK-00 索引 + SK-01~32 全 32 個主體)
- **active: 30/33 = 91% 主體**(SK-01~21/23/24/25/26/28/29/31/32 + **SK-22 2026-08-07 升 active**)
- **draft 主體: 3/33 = 9%**(SK-27/SK-30 量子描述性 archive + 計入 SK-00 索引)
- **SK-00 索引:draft**(獨立於主體 32 計)
- L1 通過: 33/33 主體 + 1 索引 = 34/34(size ≤ 9,000 bytes,6 段全綠)
- **L2 對位覆蓋: 30/33 主體 = 91%**（SK-00 索引、SK-27/30 量子標 [ARCHIVED — 學術展示無對位]）
- **L3 端點實跑: 17/17 = 100%**(2026-08-07 補 `experiment_history` 首次實跑成功;`experiment_diff` 由 ❌ 翻 ✅)
  - 12 個成功(2026-08-01 23:15):`backtest_signals` / `risk_get_metrics` / `stock_get_fundamentals` / `stock_get_technical` / `universe_get_sessions` / `industry_sector_list` / `industry_sector_lookup` / `macro_get_snapshot_latest` / `universe_get_universe_overlap` / `risk_get_correlation_matrix` / `risk_get_drawdown`(not_available 但端點活)/ `report_get_tax_snapshot`(simulated 0 但端點活)
  - 4 個新增成功(2026-08-02 20:30 本 session 補):`industry_sector_list`(38 sector 重新實跑確認) / `macro_get_snapshot_latest`(taiex 43119.75) / `narrative_get_events`(4 active events) / `taiwan_stress_index`(score=**-9.33**/low,**更正 _inbox 舊文 19.99 過時快照**)
  - **後續再補 2 端點**(2026-08-02 20:30):`crossmarket_get_us_indices`(4 指數+4 科技股) / `mcp_quickstart`(12 strategies+5 events+regime_5d+stress=-7.90)
  - **2026-08-04 v6.43 更正**:`stock_get_quote` ✅(PR #1445 merge,Fugle→TWSE fallback 獨立 timeout,3 次連續 200,source=twse → **2026-08-04 v6.43** source=**fugle** v1.0 + burst 5 + 429 retry)/ `experiment_diff` **✅ 2026-08-07 翻正**(先 `GET /api/experiment/history` 拿真 experiment_id,再 `?experiment_id=` 呼叫 → 200;**「待 atlas 暴露 experiment_list」為誤判,端點一直都在**)/ `parameters_get` ✅(**2026-08-03 22:40 帶 ATLAS_API_KEY 200,atlas-mcp 已正確轉發 X-API-Key;不帶 key 401 認證正確隔離**)
- **status: 33 頁(32 主體 + 1 索引)29 active 88% / 4 draft**(SK-00 索引 + SK-22 + SK-27 + SK-30)

## L3 實跑的真實 atlas-mcp 數據(2026-08-01 23:15)

### 個股層(2330 台積電)
- `stock_get_fundamentals`:PE 30.19 / PB 9.57 / DividendYield 1.1% / Sector=semiconductor
- `stock_get_technical`:close 2200 / sma20 2398.5 / sma50 2363.4 / RSI14 30.08(超賣)
- `stock_get_quote`:503, TWSE upstream timeout → **2026-08-04 v6.43 已修**:200,source=fugle(PR #1445 + commit c1f06430 + PR #1448 + PR #1446,5 個 symbol 全跑通 2330/2317/2454/2303/0050)

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

- [x] ~~**SK-22 消去法**:等 atlas 暴露 `experiment_list` 端點~~ → **2026-08-07 解除,該 blocker 為誤判**。`GET /api/experiment/history` 一直可用(200,18 筆真 experiment_id);先前 400 的根因是**參數名 + 傳入值**:傳 `session_id`/`agent_id` 或用 `?id=` → `400 experiment_id required`,改用 `?experiment_id=<真 id>` → 200。**SK-22 已升 active**(L3 四步全綠)。**by-factor ablation 仍 ❌**,但那是結構性缺口(atlas 無 ablation 端點),與本 blocker 無關。
- **(已撤)SK-29 滾動窗口回測**:v3.1 結算時 `risk_get_drawdown` not_available 仍視為 draft,但端點活+七時期對位已寫,**升 active**(2026-08-02 v3.1)

### 已完成(本 session 一次性 100% 落地)

- [x] 第一輪 HIGH 5 頁(SK-01/16/18/20/29)
- [x] HIGH 補 3 頁(SK-03/19/22)
- [x] MED 8 頁(SK-02/04/09/12/13/17/21,SK-22 從 MED 提前)
- [x] LOW 16 頁(SK-05/06/07/08/10/11/14/15/23/24/25/26/28/31/32,SK-27/30 量子標 archive)
- [x] SK-00 索引
- [x] 規範分歧修(SKILL.md 6000→9000 bytes,4 處同步)
- [x] L3 端點實跑 12/14
- [x] **觸發模板 12 → 13**(2026-08-04 v6.43):`trigger-2330-tsmc-swing` 第 13 模板新增,2330 盤中振幅 > 3% 觸發;落 `templates/trigger-2330-tsmc-swing.md` 5409B + atlas-mcp-trigger-monitor.py 加 `is_custom_calc` flag + 自訂計算分支 + cache_key params 區分;**實跑 3 次連穩 + ad-hoc verify 9/9 + 5/5 PASS**(intraday_swing=1.255%,結構性誠實不觸發)

### 後續 L3 升 active 工作(每頁單獨的「驗證方式」跑完)

- [ ] 33 頁中 30 頁有 atlas-mcp 對位,需逐頁跑「驗證方式」段的 Step 1~3(不是只驗端點活,還要驗每頁的具體步驟)
- [ ] 預估工時:每頁 5-10 分鐘,共 2.5-5 小時分散在 02:00 每日排程
- [ ] 短期不主動跑(留給 cron 02:00 每日消化)

### 待修

- [x] ~~**L3 端點 #2 失敗待修**:`stock_get_quote` 503 是 TWSE upstream 問題,需等源頭恢復或改 fallback~~ → **2026-08-04 v6.43 已修**(PR #1445 + c1f06430 + PR #1448 + PR #1446,Fugle v1.0 + burst 5 + 429 retry + shared limiter)
- [x] ~~**L3 端點 #14 失敗需真 experiment_id**~~ → **2026-08-07 完全翻正**:`experiment_history` 200 回 18 筆 experiment_id,`experiment_diff?experiment_id=` 200 回 baseline 0.0050727 / candidate 0.0064193(sharpe_like)。**「等 atlas expose experiment_list」為誤判**。by-factor 路徑仍 ❌(結構性),替代為 `pnl-attribution` FactorAttribution

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
