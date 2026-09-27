---
title: atlas HTTP path drift 集中記錄（2026-09-27 建立）
description: 呼叫 atlas HTTP 端點前要確認路徑、參數或 auth 是否已漂移時載入。
type: reference
status: active
created: 2026-09-27
created_by: prime-agent（Mac Mini，讀取既有證據 + 當日實測）
amendable_by: kaecer
sources:
  - skills/SK-34-listed-otc-routing.md:104-113（sector-list 404 → sectors 200）
  - skills/_inbox.md:50-54（D6 待辦：本檔的建立來源，2026-08-12 提出、2026-09-27 落地）
  - skills/_self-audit.md（v6.25/v6.59/v6.60、§6.20/§6.22/§6.28/§6.34、R148、T3-A35/A36/A630 等日誌列）
  - concepts/atlas-mcp-tools-reference.md §2.11（system_get_health 的 HTTP 對位）
  - 2026-09-27 14:23 +0800 本機 curl 實測（逐列 probed_at）
scope: 集中記錄 atlas HTTP 路徑漂移；不取代 `concepts/atlas-mcp-tools-reference.md`（工具→路徑正本）
---

# atlas HTTP path drift 集中記錄（2026-09-27 建立）

> **一句話**：atlas 的 HTTP 路徑會變（404→200、參數名、auth、transport 假設），本檔集中記錄**每次發現**的漂移，
> 供 atlas dev agent 修 wrapper、供 SK 頁引用前查核。**每列必附 `probed_at` + `http_code`**（第五條鐵律：快照值必附 timestamp）。

---

## 1. 讀法（先讀這段，避免誤用）

- **驗證等級**三級：
  - **實測** = 2026-09-27 建立本檔時直接探測（`http://127.0.0.1:18080`，帶 `X-API-Key`）——可信度最高。
  - **日誌轉載** = 只來自 `_self-audit.md` 等日誌、**尚未重探**——引用前**必須**重探。
  - **待重探** = 來源本身已被後續 session 判定為 overclaim（例：v6.59），**不可當事實**。
- **「正確路徑」沒有時間戳就不可信**。本檔建立當天就抓到反例：`/api/system/health` 在 2026-08-29 日誌記 200（degraded），2026-09-27 實測已 **404**。
- **判 route 一定帶 key**：不帶 `X-API-Key` 時 auth middleware 先回 **401**，會把「路由不存在」誤讀成「只是沒授權」。實例見 §2 第 4 列。

---

## 2. 實測表（2026-09-27 14:23 +0800，Mac Mini，帶 `X-API-Key`）

| # | 錯的路徑 | 實測 | 正確／可用路徑 | 實測 | 備註 |
|---|----------|------|----------------|------|------|
| 1 | `/api/industry/sector-list` | 404 | `/api/industry/sectors` | 200（3155 B） | 對位 SK-34:104-105 |
| 2 | `/api/macro/stress-index/current` | 404 | `/api/narrative/stress-index/current` | 200（329 B） | 對位日誌 §6.20（2026-08-28） |
| 3 | `/api/regime/current` | 404 | `/api/regime/history?days=1` | 200（345 B） | 對位日誌 §6.20 |
| 4 | `/api/system/health` | **404**（帶 key）／**401**（不帶 key） | `/api/dashboard/system-health` | 200（3369 B，**免 key 亦 200**） | ⚠ 日誌 2026-08-29 記 200 degraded，**現已 404**；`concepts/atlas-mcp-tools-reference.md:170` 本來就指 `/api/dashboard/system-health`（正確） |
| 5 | `/system/health`、`/api/healthz`、`/healthz` | 404／401 | `/api/health` | 200（140 B，免 key；`{"status":"ok","ports":{...}}`） | liveness 用這條 |
| 6 | `/api/experiment/history` | 200 但 body 僅 15 B | （需帶參數，`experiment_id` 見 §3 第 7 列） | — | 提醒：**別只看 200**，要看 body |
| 7 | `/api/macro/snapshot/latest` | 200（4340 B） | — | — | 錨點（正常） |
| 8 | `/api/dashboard/universe-overlap` | 200（33518 B） | — | — | 錨點（正常） |
| 9 | `/api/backtest/signals` | 200（96 B） | — | — | 錨點（正常） |
| 10 | `/` | 200（10843 B） | — | — | 日誌曾記 301→`/client/`，現況 200 |

> 探測條件：`GET`、`headers={'X-API-Key': $ATLAS_API_KEY}`（`~/.hermes/.env`）、`timeout=6s`。

---

## 3. 日誌轉載（未重探；引用前必重探）

| # | 類 | 內容 | 來源（file:line ＋ 日期） | 狀態 |
|---|----|------|---------------------------|------|
| 11 | transport／route | `/mcp`、`/api/mcp`、`/api/mcp/tools/list`、`/api/mcp/tools/call`、`/api/v1/mcp` 全 404 ⇒ **無對外 MCP RPC**（atlas-mcp 走 stdio，經 hermes daemon pipe） | `_atlas_mcp_path_investigation.md:14`、`_archive/...history.md:145-170,196,198`、`_self-audit.md:691`（T3-A36） | **CLOSED**（架構事實，非 wrapper bug） |
| 12 | transport | `POST /mcp` 404 使 `daily-atlas-health.py` 8:30 失敗 | `_self-audit.md:690`（T3-A35, 2026-07-30） | **CLOSED**（根因＝錯誤 transport 假設） |
| 13 | 路徑 404→200 | 台海緊張端點 404 → `/api/taiwan/stress-index`（需 `X-API-Key`）200 | 修復 `_self-audit.md:847`（v6.25, 08-03）；路徑實證 `:961` | **CLOSED（fixed）** |
| 14 | route 層變動 | 8 條候選 `/api/...` 回 **400**（空 body）；`/api/` 401；`/health` 200 ⇒ 改走 MCP wrapper | `_self-audit.md:1079`（T3-A630, 08-24, R148） | **OPEN 但已被 §2 取代**：08-24=400、08-28=404、09-27 部分 200 ⇒ 再一次佐證「無時間戳的正確路徑不可信」 |
| 15 | 結構性缺口 | `/api/stock/history`／`/ohlc`／`/ohlcv`／`/daily`／`/price-history`／`/quote/history` 全 404 ⇒ **無原生歷史端點** | `_self-audit.md:324`（08-12）、`_inbox.md:62` | **OPEN**（SK-20 Step 3 阻塞；需 client 累積報價） |
| 16 | 參數名 | `experiment_diff?id=` → 400 `experiment_id required`；改用 `?experiment_id=<id>` → 200 | `SK-22:82-89`（08-07）、`_atlas-endpoint-cards/experiment-diff.md:12,24`、已回寫 `SK-32:11`／`SK-36:12` | **CLOSED** |
| 17 | wrapper 型別 | MCP `mcp__atlas_mcp__stock_get_quote` 拒收 string symbol（schema=string 被當 integer） | `_self-audit.md:322`（v6.59, 08-11） | **待重探**（**出自已被判定 overclaim 的 v6.59**，不得直接當事實） |
| 18 | auth | `parameters_get` 未帶 key → 401；帶 `ATLAS_API_KEY` → 200 | `_consult-index_archive.md:84-85`（08-03 驗收）、`_self-audit.md:783,875` | **CLOSED**（非路徑問題） |
| 19 | 預期行為 | `universe_get_session_detail` 回 404（session 不存在） | `concepts/atlas-mcp-tools-reference.md:382` | **EXPECTED**（列為排除項，避免誤判為 drift） |
| 20 | auth | `template_detector_status` → 401 ⇒ 走 REST fallback | `log.md:208` | **未結案**（查無後續紀錄） |

**可信度警語**：第 17 列（v6.59）與第 1 列的**矛盾註記**（`_self-audit.md:322` v6.59 曾記 `/api/industry/sector-list` 回 38 sectors，而 v6.59 整體已被認定 overclaim）⇒ 這兩個來源的數字**不可引用**，只能當「待重探」清單。

---

## 4. 清理佇列

1. **重探清單（依序）**：第 17 列（v6.59 型別問題）、第 20 列（template_detector_status auth）、第 14 列的 8 條候選路徑。
2. **atlas dev 端（wrapper 修復）**：第 1／2／3／4 列的正確路徑應寫進 wrapper（若尚未），並移除對死路徑的引用。
3. **驗證 SOP（本檔建立時的建議）**：任何 SK 頁寫入 atlas HTTP 路徑前，先 `curl` 探一次並記 `probed_at` + `http_code`（對位 `_inbox.md:53` 的結論）。
4. **結構性缺口（第 15 列）**：需產品決策（client 累積報價），非路徑修復。

---

## 5. 本檔維護

- 新發現**一律 append 一列**（含 `probed_at` + `http_code`）；不改寫歷史列。
- 修好後把狀態改 **CLOSED** 並附修復證據（commit／PR 編號）。
- 本檔被 `skills/SK-34-listed-otc-routing.md` 與 `skills/_inbox.md` 引用；改名須同步。
- 索引：本檔列於 `index.md` 的 Summaries 段（`audit-file-index-sync.py` 只看 `index.md`）。
