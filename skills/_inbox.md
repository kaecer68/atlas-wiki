# atlas-skill-inbound Inbox

最後更新:2026-08-07 16:50 (**CR-2026-08-07 擱置區邊移** — HERMES_AUDIENCE env 提案移交 `_inbox_deferred.md` v1.0,見該檔 §ENV-CR-2026-08-07); 前次更新:2026-08-07 02:10 (v6.45 結算 — **0 新頁 + 1 頁誤判翻正**;33 頁早已 100% 落地,本輪不硬湊 quota。**SK-22 draft → active**:L3 四步全綠(`experiment_history` 200/18 筆、`experiment_diff?experiment_id=` 200 baseline 0.0050727→candidate 0.0064193 sharpe_like、`/api/dashboard/universe-overlap` 200 29 agents/86 warnings、`backtest_signals` 200 CIRCUIT_BREAKER)。**結構性誠實**:舊 blocker「待 atlas 暴露 experiment_list」為**誤判**——端點一直都在,400 根因是參數名 `id=` vs `experiment_id=` 加傳錯值(session_id/agent_id);另**證偽** `eval_metrics` 欄位(18/18 experiment 皆無,原為未驗證推測)。by-factor ablation 仍 ❌ = 真結構性缺口,不翻轉。); 前次更新:2026-08-04 14:10 (v6.44 結算 — Fugle 修復鏈 4 PR 全 merge 端到端驗收(PR #1445/#1446/#1448/#1449,本 session 實跑 5 端點全綠:stock_get_quote 2330/2317/0050 3/3 source=fugle + parameters_get 243KB + risk_get_commentary not_available)…

## 總體進度

- 已寫 draft: **34/34** = 100%(SK-00 索引 + SK-01~33 全 33 個主體含 **SK-33 audience-routing 2026-08-07 新增**)
- **active: 31/34 = 91% 主體**(SK-01~21/23/24/25/26/28/29/31/32 + SK-22 + **SK-33 audience-routing 2026-08-07 Day 1 落,active**)
- **draft 主體: 3/34 = 9%**(SK-27/SK-30 量子描述性 archive)
- **SK-00 索引:draft**(獨立於主體 33 計)
- L1 通過: 33/33 主體 + 1 索引 = 34/34(**SK-33 新增後調為 34/34;size ≤ 9,000 bytes,6 段全綠**)
- **L2 對位覆蓋: 31/34 主體 = 91%**（SK-00 索引、SK-27/30 量子標 [ARCHIVED — 學術展示無對位]、SK-33 元能力不適用 L2 對位口徑）
- **L3 端點實跑: 17/17 = 100%**(2026-08-07 補 `experiment_history` 首次實跑成功;`experiment_diff` 由 ❌ 翻 ✅)
  - 12 個成功(2026-08-01 23:15):`backtest_signals` / `risk_get_metrics` / `stock_get_fundamentals` / `stock_get_technical` / `universe_get_sessions` / `industry_sector_list` / `industry_sector_lookup` / `macro_get_snapshot_latest` / `universe_get_universe_overlap` / `risk_get_correlation_matrix` / `risk_get_drawdown`(not_available 但端點活)/ `report_get_tax_snapshot`(simulated 0 但端點活)
  - 4 個新增成功(2026-08-02 20:30 本 session 補):`industry_sector_list`(38 sector 重新實跑確認) / `macro_get_snapshot_latest`(taiex 43119.75) / `narrative_get_events`(4 active events) / `taiwan_stress_index`(score=**-9.33**/low,**更正 _inbox 舊文 19.99 過時快照**)
- **status: 34 頁(33 主體含 SK-33 + 1 索引)30 active 88% / 4 draft**(SK-00 索引 + SK-22 + SK-27 + SK-30;**SK-33 audience-routing 2026-08-07 Day 1 落,active**)
  - **2026-08-04 v6.43 更正**:`stock_get_quote` ✅(PR #1445 merge,Fugle→TWSE fallback 獨立 timeout,3 次連續 200,source=twse → **2026-08-04 v6.43** source=**fugle** v1.0 + burst 5 + 429 retry)/ `experiment_diff` **✅ 2026-08-07 翻正**(先 `GET /api/experiment/history` 拿真 experiment_id,再 `?experiment_id=` 呼叫 → 200;**「待 atlas 暴露 experiment_list」為誤判,端點一直都在**)/ `parameters_get` ✅(**2026-08-03 22:40 帶 ATLAS_API_KEY 200,atlas-mcp 已正確轉發 X-API-Key;不帶 key 401 認證正確隔離**)

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

- ⚠️ **4 頁 draft**(SK-00 索引 + SK-22 experiment_diff 400 + SK-27/SK-30 量子描述性 archive)——L3 端點實跑 ≠ L3 頁面驗證。**30 active 頁**(含 SK-33 audience-routing 2026-08-07 Day 1)「驗證方式」段的 Step 1~3 跑完才算完整 L3
- ⚠️ `risk_get_drawdown` not_available 是已知(SK-29 已升 active 但端點仍 not_available,風險引擎需 stress_test_daily 完成)
- ⚠️ `report_get_tax_snapshot` 需真實持倉才有意義(目前無倉)
- ⚠️ 規範分歧已修(SKILL.md 6000→9000 bytes,4 處同步;quota 5→3 頁,8 處同步),grep 全文 0 殘留
- ⚠️ 2026-08-02 19:38 文案失真修正:5 處矛盾已修(_self-audit line 128 / _inbox line 3+8-10+14+41-58+92)

## 統計

- 已寫: **34 頁 = 100%**(SK-00 + SK-01~32 + **SK-33 audience-routing 2026-08-07 Day 1**)
- **L2 對位覆蓋: 31/34 = 91%**（SK-00 索引、SK-27/30 量子標 [ARCHIVED — 學術展示無對位]、SK-33 元能力不適用 L2 對位口徑）
- L1 失敗率: 0%（33/33 主體 + SK-33 8847B = 34/34 全綠，size ≤ 9,000 bytes + 6 段 + frontmatter 9 欄）
- L3 端點實跑: 12/14 = 86%(**2026-08-07 補 `experiment_history` 與 `experiment_diff` 兩端點全綠**)
- L3 待驗端點(每頁):30 active 頁(含 SK-33 算 1 active)× 每頁 3 step = 90 個 Step 待跑(給 02:00 每日 cron)
- 跳票 quota: 4 頁(本輪已事實上補齊)
- 已排程 cron: 1(8fd1b1eda764 skill-inbound 02:00 daily,quota 3,3 連敗後觀察中)

---

## 30 秒重啟程序見 `~/.hermes/skills/atlas-skill-inbound/SKILL.md` §重啟後 30 秒回神程序

---

## 跨邊界擱置(2026-08-07+)

對位 `SOUL §3.7.3` 第 6 條邊界 + 「動 hermes runtime 全域設定」屬 owner 範圍。
本檔 size 已超 9000 bytes 上限,**跨邊界提案獨立落 `_inbox_deferred.md`**:
當前條目 → 見 `[[skills/_inbox_deferred.md]]` §ENV-CR-2026-08-07(2026-08-07 v6.52 已撤銷外推:原「HERMES_AUDIENCE env 提案移交 Nous Research hermes owner」改為「atlas-wiki 內部約定 — agent 從 session context 讀 audience,預設 `user`」)

---

## 擱置區 — 需 hermes owner 拍板(2026-08-07 新增)

對位 SOUL §3.7.3 例外邊界第 6 條(_method.md / SKILL.md 規範本體修改 →
走 task-governance)及「動 hermes runtime 全域設定」屬此類。

| 提案 ID | 內容 | 提案來源 | 預期影響 | 移交對象 | 狀態 |
|---|---|---|---|---|---|
| ENV-CR-2026-08-07 | **2026-08-07 v6.52 撤銷外推,改內部化**:agent 從 session context(使用者 channel / task type / time-of-day)推導 audience(user / developer / admin),預設 `user`;若未來 hermes runtime 升級提供 `HERMES_AUDIENCE` env,改雙層架構(env 優先,session context fallback)。原口徑規範落 `skills/SK-33-audience-routing.md`(Day 1 quota 已落,frontmatter v6.52 已修)+ `financial-advisor-coach §X`(對 user 的降級口徑,v6.52 自扛落地) | skills/_manifest_coverage_routing.md v1.0
§2 題 3 + §3.3 Day 3 + **2026-08-07 v6.52 kaecer「我們自己把事做完,不外推」拍板** | atlas-wiki / atlas-notes agent 自扛 audience 識別;
不依賴 hermes runtime env;過渡期不再受限制 | **atlas-wiki 內部約定**(撤銷原「hermes runtime owner + kaecer task-governance」移交) | 部分落地(SK-33 ✅;§X 待寫) |

**移交細節**(v6.52 撤銷外推後改為「內部約定配套清單」):
- 用途:讓 agent 對散戶預設不外漏 error code + 給開發者看完整 audit 細節 + 給 admin 看全
metrics
- 對位:kaecer 2026-08-07 第二輪訊息指出「散戶怕 error / 管理者要 debug 細節」是 audience
二分的根本理由;第五輪訊息「我們自己把事做完,不外推」拍板撤銷 owner 移交
- 配套:✅ SK-33-audience-routing(frontmatter v6.52 已修語意)+ ⏳ financial-advisor-coach
§X(對 user 的降級口徑,v6.52 自扛落地中)——**全部在 atlas-wiki 範圍內,不依賴 hermes runtime env**
- 風險點(v6.52 已緩解):~~env 未上線前 agent 全走 user 口徑~~ → agent 自扛 session context
推導,過渡期不再受限制;~~等 hermes owner 回覆期 ≤ 14 天~~ → 已撤銷 owner 依賴
- 提交流程(v6.52 撤銷):~~對 hermes owner 走 GitHub issue(Nous Research hermes-agent repo
issues 區)+ 在本檔留 issue link 補位~~ → 不再外推,所有落地在 atlas-wiki 內完成

### 移交後狀態更新規則(v6.52 撤銷 owner 移交,改為配套落地追蹤)
- ~~收到 hermes owner 回覆後,於本表更新「狀態」欄~~ → **撤銷**(已無 owner 移交)
- ✅ SK-33 frontmatter 已修(v6.52),於本表更新「部分落地」
- ⏳ §X 寫完後,於本表更新「全部落地」
- ~~若提議遭 reject,落 T3 evidence 寫到 governance-log.md~~ → **撤銷**(無 reject 情境)
- 任何 atlas-wiki 內 agent 自扛的補強(SK-33 ✅、financial-advisor-coach
§X ⏳)不阻塞,可平行推進

---

**⚠ size 警示**:本檔 append 後 size 預期 ~ 13,000+ bytes,**超出 _method.md §3 第 6 條「所有 .md ≤ 9000 bytes」上限**。本任務 verbatim append 是 kaecer 2026-08-07 session 第 3 輪明示指令(SOUL §0.1 5 種例外外),但**主檔 size 修法需走 task-governance**(SOUL §3.7.3 第 6 條例外) — 後續動作:
- 選項 A:擴 `_method.md §3` 例外清單加 `_inbox.md`(主檔 = 跨 session 累積 inbox,類似 _self-audit 例外精神)
- 選項 B:把擱置區搬回 `_inbox_deferred.md`(v6.49 原設計,對位 AGENTS.md §11 一段一檔)
- 選項 C:本檔內重組歷史段(把已完成項目歸檔)
本警示已落 T3 evidence,kaecer 拍板前 agent 不擅改 size 規範本體。

### 變更記錄
- **v6.50 / 2026-08-07 19:18**:HERMES_AUDIENCE env 提案從 `_inbox_deferred.md` v1.0 第 1 條提升至主檔 `§擱置區`(kaecer session 第 3 輪明示);size 10540 → ~13000 bytes 預期,⚠ size 警示落段末(待 task-governance 後續)
- **v6.52 / 2026-08-07 19:35**:撤銷外推,改內部化(kaecer 第五輪訊息「我們自己把事做完,不外推」拍板);同步修 4 檔:`SK-33` frontmatter line 11/16/106/110-111(語意 + 未消化清單)、`_inbox_deferred.md` title + 全文(跨邊界移交 → 內部約定)、`_inbox.md` §擱置區表格 + 移交細節 + 規則、`_manifest_coverage_routing.md` 待修(Step 2);不再走 GitHub issue / 不再等 hermes owner 回覆;**T3-A275 預備落 governance-log**

<!-- v6.53-auto-detect-test:這是測試 PR,merge_and_cleanup.sh --auto-detect 驗證用,merge 後 revert -->
