# atlas-skill-inbound Inbox

最後更新:2026-10-29 atlas-skill-inbound tick（§CIO-2564；指數通道恢復確認結案 + `twse_sector_index` 綠燈空檔新立 + `concepts/atlas-platform-overview.md` §2.1.1 落地 2,512 B）;前次更新:2026-10-24 CIO 夜間研究 tick（§CIO-2460；撤回 §CIO-2418「silver 歷史維度缺失」錯誤工單 + `decay_until` 掃描結案 223 .md/0 過期 + §第七條 v1.1 歸檔 §CIO-2278/§CIO-2364 兩段 4,573 B，主檔收為 4,440 B）;前次更新:2026-10-21 atlas-skill-inbound tick（§CIO-2278；C 項 `wc -c` 二次量測結案 = 不需 split；`check-stale` 91.5h 未提交項處置 + §第七條 v1.1 歸檔 5,806 B，主檔收為 8,911 B）;前次更新:2026-10-16 週末 lint 解讀（Stale 4 條首進 l1-t4/l1-t5）;前次更新:2026-09-27 模板類 quota 拍板結案(不計入;條文入 `_method.md:121`);前次更新:2026-09-27 模板狀態校正 ＋ templates quota 條文查核（同日另段:結清兩項長期待辦）;前次更新:2026-08-21 v2 session 修補(8/21 補登（見 T9 v2）— 共同根因: A1 execute_code 會員權限 + A2 terminal 180s timeout, 修復任務 A1+A2 已寫入 hermes-governance-log T3-A493 條目請 hermes 下次 trigger 處理, 詳見 _inbox_archive.md §6 8/21 條目);前次更新:2026-08-21 歸檔 session(PR #29);前前次更新:2026-08-12 D6 session 結算(SK-34 真實 promotion + v6.59 overclaim 修正);前前前次更新:2026-08-07 D4 session 結算(`_inbox.md` size 15201B > 12000B 上限 → 啟動第七條例外歷史段歸檔 → 歷史段 5261B 移至 `_inbox_archive.md` v1.0,主檔縮為 3589B); 前前次更新:2026-08-07 16:50 (CR-2026-08-07 擱置區邊移 → v6.52 撤銷外推,改內部化)

> 2026-08-07 D4 結算段（總體進度 ＋ 最後更新對位事實,2,816B）已於 2026-09-27 依 `_method.md` 第七條例外移入 `_inbox_archive.md`。


---
## 對位 `_method.md` 第七條例外

規範**唯一來源**＝`_method.md` 第七條例外（v1.0，2026-09-02 拍板更新）：本檔上限 ≤ 12000 bytes，append 前 `wc -c` 自查，超限即依該條歸檔 SOP 移 `_inbox_archive.md`。

## 30 秒重啟程序

見 `~/.hermes/skills/atlas-skill-inbound/SKILL.md` §重啟後 30 秒回神程序

---

## 待辦（active；本文以下至「已結案」標題前，預算 ≤ 8,000 B）

## 待補佇列（§CIO-2460 產出 — 2026-10-24）

1. **🔺 撤回：~~`silver` 歷史維度缺失（backend，`@qc` 歸屬）~~** — §CIO-2418（10-23）報「30 snapshots 全部無 `silver` 欄位皆 nan」**為錯誤結論**。§CIO-2460（10-24）逐筆實測：`macro_get_snapshot_history(days=30)` 的 **30/30 snapshots `silver` 欄位 value 與 change_pct 皆非 null（`bad: []`）**，symbol `SI=F`，值域 53.96~64.71 ⇒ **backend 無缺口，白銀條件可驗證**。原工單作廢，勿據此開 backend ticket。
2. **US10Y 雙源單位定義差異需寫入欄位契約**— `snapshot.us10y.value` = 殖利率百分點（4.9880），`stress_index.components.us10y` = 標準化壓力分數（1.6959）。兩者單位不同，Step 1.6 對位表易誤判為矛盾。建議於欄位契約頁標註兩者語義與不可比性。（§CIO-2418 產出，§CIO-2460 續留）
3. **cron prompt 的 MCP 參數需更新**— `event_calendar`、`narrative_get_events`、`narrative_get_chains` schema 為 `additionalProperties: false`，**不接受 `limit` / `days`**；`macro_get_stress_index_current` 不接受任何參數。現行 prompt 帶參數會被拒（§CIO-2418 導致事件對位未完成，§CIO-2460 去參數後已成功取回 5 chains）。
4. **✅ 已結案：`decay_until` 新鮮度全量掃描**（§CIO-2418 待查）— §CIO-2460 已補齊：`atlas-wiki/` + `atlas-notes/02-knowledge/` 共 **223 個 .md**，`decay_until` 標記 3 筆（2 筆 `never` + SK-31 `2027Q1-WIR-revision` 未過期），**過期 0 筆**。
5. **H-MK-01 條件耦合過嚴，須重設**（§CIO-2420，§CIO-2460 續留）— 條件「|oil Δ|>5% **且** US10Y +>8bp」在近 30 日 regime（US10Y 單日變動 −19.3~+5.6bp，**> +8bp 天數 = 0**）下**結構性不可達**。§CIO-2460 連 3 tick N=0 確認。建議改「**或**」並分別標記子條件；另建議以「**白銀跌幅 > 黃金跌幅**」作通膨重定價主導的替代判別式（30 日窗銀 −16.63% vs 金 −4.65%，銀跌幅為金 3.6 倍；10-22 已成立）。待拍板，本 cron 不執行改假說定義。
6. **方法論紅線（§CIO-2460 新增）**— 任何「某維度缺失」宣稱寫入 note 或開工單前，須附**當次實測的逐筆檢查輸出**（合格格式例：`bad: []` + 30/30 計數）。§CIO-2418 的 silver 缺口宣稱即缺此證據，是同一條紅線第 2 次觸發（第 1 次 8/21~8/27「backend 缺產業 chips API」連 4 份 note 繼承判斷）。

## 待補佇列（§CIO-2491 產出 — 2026-10-26）

1. **H-EV-01 全量重建（單一 event-date 定義）** — 本列「T+3 平均 −1.63%」無法由三事件（−1.77/+5.21/+2.70）重算（應為 **+2.05%**）；同一事件（6 月營收 442.68bn）在 registry 內同時標 **7/16**（line 105/227）與 **7/20**（line 185）。重建規則：event-date **一律用 TSMC 官方公告日**（IR 行事曆），並同時記錄 atlas ingest 日供比對。依據：`04-daily/2026-10-26.md` §3。
2. **atlas API 三項缺陷（走 governance PR，需 `kaecer-reviewed`，本 cron 不自行改）** — ① `capital_flow_summary.assessment.as_of_trading_date` 用**日曆日**而非交易日（10-26 光復節補假仍標為 as_of）；② 休市日 fill-forward **無旗標**，時間軸逐日建 row 造成「假凍結」；③ `stock_get_chips(date=…)` 靜默回退到前一日，response 無 `requested_date`/`fallback` 欄位。
3. **休市日半導體指數仍變動（`@qc` 歸屬）** — 2026-10-09（國慶補假休市）TAIEX 0.00%，`taiwan_semi_index` 1658.10 → 1677.95（**+1.20%**）⇒ 足以單獨製造 T+N 假超額。需確認該指數來源與交易日曆。
4. **✅ 已結案（2026-10-29 §CIO-2564）：指數通道恢復確認** — `channel_health`（2026-10-29T02:31+08:00）逐條：`taiex_index` ✅（`last_success_at=2026-10-28T18:30:53Z`；`taiex=47035.58`／`change_pct=2.04`）／`us_cpi` ✅（`2026-10-28T16:46:00Z`）／`finmind` ❌ 仍 error 但**根因翻轉**：HTTP 400 `Token is illegal`（`last_success_at=2026-10-23T03:29:55Z`），**非原判「402 額度耗盡 → 額度層 @mis」** ⇒ 改列憑證面（atlas-notes R151 已列 kaecer 待決，n=4）／`twse_sector_index` ⚠️ 通道 ok 但 10-28 日檔 `{}` ⇒ 追蹤項 7。落地：`concepts/atlas-platform-overview.md` §2.1.1。
5. **10-25（日）tick 缺漏** — `04-daily/2026-10-25.md` 不存在，根因 HTTP 429「Token Plan 用量上限」；`cron_incidents` `347efbfe14de`（rate_limit，first_seen 10-18 06:00，last_seen 10-25 06:00，**state=detected 未關閉**）。額度層 → `@mis`。
6. **方法論紅線（§CIO-2491 新增）** — 任何「資料斷流／停滯」判定寫入 note 前，必先跑**交易日曆對位**（TWSE 開休市表 + `data/state/capital_flow/` 檔名 + `data/replay/*.csv` 末列）；本 tick 初稿即因「值連續 4 列不變」誤判 T86 斷流，實為 10-23 薔琵颱風休市。
7. **`twse_sector_index` 綠燈空檔（atlas-go 潛在缺陷）**（§CIO-2564）— 源碼 `internal/marketdata/twse_sector_index_provider.go`：`fetchWithMapper`（L100-141）吞單日錯誤後仍 `saveToCache` 空 map 並回 `nil`；`fetchSingleDay` 解析 0 筆亦回空 map 不報錯 ⇒ 通道 `ok`、日檔 `{}`（10-28 實證）。**無空結果護欄**。修法建議「空 map → 回錯不覆寫」，改動走 governance PR + `kaecer-reviewed`；本 cron 不改 backend。
8. **SK-23「106 個日檔」已過時**（§CIO-2564）— 實測 = **1,693** 檔（最新有效為 10-27 檔，寫入 2026-10-28 11:06:54）;SK-23 現 8,987 B、上限 9,000 B ⇒ 須同段精簡後再改。

---

## 已結案（近期；預算 ≤ 4,000 B，超出即移 `_inbox_archive.md`）
