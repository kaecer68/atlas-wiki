# ETF 換股 / MSCI 調整 觸發模板(單日版)

**觸發條件(單日)**:市場成交量 > 0 + ETF 淨申購變化顯著
**對位**:ATLAS_METHODOLOGY.md §二 Layer 7(事件錯價)
**對位 strategy**:無對位(事件型)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **market_volume 7253.13 億** ✅(> 0,當日交易活躍)
- etf_net_subscription 0(API 未提供即時)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(market_volume)

## Step 2:自動跑端點
- mcp__atlas_mcp__event_calendar(ETF 換股日 / MSCI 生效日)
- mcp__atlas_mcp__capital_flow_summary(ETF 申購贖回)

## Step 3:建議
- 成交量 > 5000 億 + ETF 申購顯著 → **加碼權值股 5%**(被動買盤)
- 成交量 < 3000 億 → **觀望**

## Step 4:落 §6 + Telegram
