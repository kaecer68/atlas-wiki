# ETF 換股 / MSCI 調整 觸發模板(事件日曆型)[2026-08-22 audit-fix]

**觸發條件(事件日曆型)**:ETF 成份股調整**公告日**觸發 → **生效日前 5 個交易日佈局**(原「市場成交量 > 0」恆真條件已刪除 [2026-08-22 audit-fix])
**對位**:ATLAS_METHODOLOGY.md §二 Layer 7(事件錯價)
**對位 strategy**:無對位(事件型)

## Step 1:信號捕捉(對位真實 2026-08-03,舊快照)
- market_volume 7253.13 億(舊快照；成交量 > 0 不再作為觸發條件 [2026-08-22 audit-fix])
- etf_net_subscription 0 **[PENDING — ETF 申購資料 API 未提供]**
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(market_volume)

## Step 2:自動跑端點
- mcp__atlas_mcp__event_calendar(ETF 換股日 / MSCI 生效日)
- mcp__atlas_mcp__capital_flow_summary(ETF 申購贖回)

## Step 3:建議
- ETF 成份股調整公告 → **生效日前 5 個交易日佈局**(被動買盤)
- 成交量 < 3000 億 → **觀望**

## Step 4:落 §6 + Telegram

**說明**:本模板為**事件日曆型,非資料觸發型**;ETF 申購資料 API 未提供,無法以資料驗證觸發,以事件日曆為觸發源 [2026-08-22 audit-fix]
