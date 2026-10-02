---
description: ETF 成份股調整公告日，或生效日前 5 個交易日時載入本模板。
last_verified: "2026-10-03"
verify_by: pending
l3_run_at: 2026-10-03T02:30:00+08:00
l3_run_by: "@cio (atlas-skill-inbound §CIO-1543 補強)"
l3_endpoints_probed:
  - "mcp__atlas__macro_get_snapshot_latest → http_code=200, 4325B (2026-10-03T02:30 CST); etf_net_subscription.value=0, change_pct=0, timestamp=0 (PENDING)"
  - "mcp__atlas__event_calendar → http_code=401 unauthorized (atlas-mcp 端 channel auth 不通過,結構性已知)"
l3_verdict: "verified-fail: 事件型觸發源無 atlas 端資料對位,改走 event_calendar 事件日曆(本 tick 401)"
---

# ETF 換股 / MSCI 調整 觸發模板(事件日曆型)[2026-08-22 audit-fix]

**觸發條件(事件日曆型)**:ETF 成份股調整**公告日**觸發 → **生效日前 5 個交易日佈局**(原「市場成交量 > 0」恆真條件已刪除 [2026-08-22 audit-fix])
**對位**:ATLAS_METHODOLOGY.md §二 Layer 7(事件錯價)
**對位 strategy**:無對位(事件型)

## Step 1:信號捕捉(對位 2026-10-03 L3 實跑,事件型)
- **L3 探測**:`macro_get_snapshot_latest` → `etf_net_subscription={value:0, change_pct:0, timestamp:0}` (PENDING) + `event_calendar` → http_code=401(以 `X-API-Key: atlas-mcp-shared-secret-2026` 探測;channel auth 不通過,結構性已知,需@qc 排程修)
- 判定:**事件日曆型觸發,atlas 端無 etf_net_subscription 資料對位**;**仍依 `event_calendar` 觸發**(原 [2026-08-22 audit-fix] 結論不變,本 tick 補上 L3 探測 timestamp)
- 對位端點:mcp__atlas_mcp__event_calendar(事件日曆,401 待修) + mcp__atlas_mcp__macro_get_snapshot_latest(market_volume,本觸發已不用)

## Step 2:自動跑端點
- mcp__atlas_mcp__event_calendar(ETF 換股日 / MSCI 生效日)
- mcp__atlas_mcp__capital_flow_summary(ETF 申購贖回)

## Step 3:建議
- ETF 成份股調整公告 → **生效日前 5 個交易日佈局**(被動買盤)
- 成交量 < 3000 億 → **觀望**

## Step 4:落 §6 + Telegram

**說明**:本模板為**事件日曆型,非資料觸發型**;ETF 申購資料 API 未提供,無法以資料驗證觸發,以事件日曆為觸發源 [2026-08-22 audit-fix]
