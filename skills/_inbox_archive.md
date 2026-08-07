---
title: atlas-skill-inbound Inbox Archive
type: archive
status: archived
created: 2026-08-07
archived_from: skills/_inbox.md (v6.52)
amendable_by: kaecer
sources:
  - skills/_method.md §第七條例外(line 177-183)歸檔觸發
  - skills/_inbox.md v6.52 之前
---

# atlas-skill-inbound Inbox Archive(2026-08-07 歸檔 v1.0)

> **用途**:本檔承接 `_inbox.md` 在 2026-08-07 15201B 超 12000B 上限後的歷史段歸檔。
> **對位**:`_method.md` §第七條例外 line 178-182「歷史段歸檔觸發」。
> **保留**:本檔留 2026-08-07 之前的所有結算記錄、L3 數據快照、擱置區、變更記錄;**主檔 `_inbox.md` 只留最新 2 版本結算**。

---

## 1. 2026-08-07 v6.52 主檔撤銷外推全文

(以下內容摘自 `_inbox.md` v6.52 line 110-153 撤銷外推後的內部化配套清單)

### 擱置區 — 內部化配套(2026-08-07 v6.52 撤銷 owner 移交)

對位 SOUL §3.7.3 例外邊界第 6 條(_method.md / SKILL.md 規範本體修改 → 走 task-governance)。

| 提案 ID | 內容 | 提案來源 | 預期影響 | 移交對象 | 狀態 |
|---|---|---|---|---|---|
| ENV-CR-2026-08-07 | **v6.52 撤銷外推,改內部化**:agent 從 session context 推導 audience,預設 `user`;若未來 hermes runtime 升級提供 `HERMES_AUDIENCE` env,改雙層架構 | _manifest_coverage_routing.md v1.0 §2 題 3 + §3.3 Day 3 + 2026-08-07 v6.52 kaecer「我們自己把事做完,不外推」拍板 | atlas-wiki / atlas-notes agent 自扛 audience 識別 | atlas-wiki 內部約定 | 部分落地 |

### 配套落地追蹤
- ✅ SK-33-audience-routing frontmatter v6.52 已修語意
- ⏳ financial-advisor-coach §X 待寫
- 已撤銷 hermes owner 移交、issue link、不再外推

---

## 2. 歷史結算記錄(2026-08-04 ~ 2026-08-07)

### v6.45 / 2026-08-07 02:10
- 0 新頁 + 1 頁誤判翻正
- SK-22 draft → active(L3 四步全綠:`experiment_history` 200/18 筆、`experiment_diff?experiment_id=` 200、`universe-overlap` 200、`backtest_signals` 200)
- 結構性誠實:舊 blocker「待 atlas 暴露 experiment_list」為誤判——端點一直都在
- 證偽 eval_metrics 欄位(18/18 experiment 皆無)
- by-factor ablation 仍 ❌ = 真結構性缺口,不翻轉

### v6.44 / 2026-08-04 14:10
- Fugle 修復鏈 4 PR 全 merge 端到端驗收(PR #1445/#1446/#1448/#1449)

### v6.43 / 2026-08-04
- `stock_get_quote` ✅(Fugle→TWSE fallback + PR #1445 merge + burst 5 + 429 retry)

### v6.50 / 2026-08-07 19:18
- HERMES_AUDIENCE env 提案從 `_inbox_deferred.md` 提升至主檔 §擱置區

### v6.52 / 2026-08-07 19:35
- 撤銷外推,改內部化(kaecer 第五輪訊息)
- 同步修 4 檔:`SK-33`、`_inbox_deferred.md`、`_inbox.md`、`_manifest_coverage_routing.md`
- T3-A275 預備落 governance-log

---

## 3. 歷史 L3 端點實跑快照(2026-08-01 23:15)

### 個股層(2330 台積電)
- `stock_get_fundamentals`:PE 30.19 / PB 9.57 / DividendYield 1.1% / Sector=semiconductor
- `stock_get_technical`:close 2200 / sma20 2398.5 / sma50 2363.4 / RSI14 30.08(超賣)
- `stock_get_quote`:2026-08-04 v6.43 已修(200, source=fugle)

### 風險層
- `backtest_signals`:CIRCUIT_BREAKER / drawdown 0.72 / sharpe_long 0.27 / sharpe_short 0.49
- `risk_get_metrics`:data_provenance=live / 150 sessions / var_95 -38.7%
- `risk_get_drawdown`:not_available(風險引擎尚未完成首輪模擬)
- `risk_get_correlation_matrix`:20×20 產業相關矩陣
- `report_get_tax_snapshot`:simulated 0(需真實持倉)
- `risk_get_commentary`:not_available(atlas 端風險決策機制未啟動)

### 總經層
- `macro_get_snapshot_latest`:current_period=consolidation / taiex 43119.75 / vix 15.99
- `universe_get_sessions`:150 sessions(2026-08-02 20:40 重跑確認,先前 147 sessions 為舊版計數)
- `universe_get_universe_overlap`:28 個 agent overlap matrix

### 產業層
- `industry_sector_list`:38 個產業
- `industry_sector_lookup`(2330):半導體 sector, 12 個成分股

---

## 4. 歷史待辦總表(跨 SK)

### 已完成(本 session 一次性 100% 落地)
- [x] 第一輪 HIGH 5 頁(SK-01/16/18/20/29)
- [x] HIGH 補 3 頁(SK-03/19/22)
- [x] MED 8 頁
- [x] LOW 16 頁
- [x] SK-00 索引
- [x] 規範分歧修(SKILL.md 6000→9000 bytes, 4 處同步)
- [x] L3 端點實跑 12/14
- [x] 觸發模板 12 → 13(2026-08-04 v6.43:`trigger-2330-tsmc-swing`)

### 已撤 blocker
- ~~SK-22 等 atlas 暴露 experiment_list~~ → 2026-08-07 解除(端點一直都在,參數名誤傳)
- ~~L3 端點 #2 stock_get_quote 503~~ → 2026-08-04 v6.43 已修
- ~~L3 端點 #14 失敗需真 experiment_id~~ → 2026-08-07 完全翻正

---

## 5. 變更記錄(對位 _inbox.md line 151-153)

| 版本 | 時間 | 變更內容 |
|---|---|---|
| v6.50 | 2026-08-07 19:18 | HERMES_AUDIENCE env 提案提升至主檔 §擱置區 |
| v6.52 | 2026-08-07 19:35 | 撤銷外推,改內部化(kaecer 第五輪訊息);同步修 4 檔 |

---

## 歸檔觸發條件

對位 `_method.md` §第七條例外 line 178-182:
- 連 2 次 session append 後 > 12000 → 啟動歷史段歸檔評估
- 2026-08-07 session 驗證:15201B > 12000B → 觸發歸檔 → 本檔建立

**未來 append 流程**:新結算資料寫主檔 `_inbox.md` 最新 2 版本;歷史段移到本檔 append。

amendable_by: kaecer
archive_owner: agent(autonomous)