# 中國需求強訊號觸發模板

**觸發條件(單日)**:TSMC 月營收 YoY > +50% + export_electronics 月增 > 0
**對位**:ATLAS_METHODOLOGY.md §二 Layer 5(出口需求)
**對位 strategy**:china-slowdown-export-pressure(L5, hit_rate 0.58)— **反向訊號**(需求強 = 機會)

## 為什麼中國需求強 = 台股利多?
- 台灣對中(含香港)出口佔總出口 **30-40%** = 最大單一客戶
- **半導體 40%+ 出口到中國**(TSMC/聯發科主要客戶是中國組裝廠)
- **中國需求強** = TSMC/電子出貨增 = 月營收增 = 結構性利多

## Step 1:信號捕捉(對位真實 2026-08-03)
- **TSMC 月營收 +67.87% YoY** ✅(> +50%,中國需求強訊號)
- **export_electronics +14.96%** ✅(> 0,月增)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(tsmc_revenue + export_electronics)

## Step 2:自動跑端點
- mcp__atlas_mcp__risk_exposure(sector exposure)
- mcp__atlas_mcp__risk_get_correlation_matrix(電子 ↔ 塑化)

## Step 3:建議
- 觸發成功(中國需求強)→ **加碼半導體至 60% + 減塑化/出口股 5%**
- 觸發失敗(中國需求弱)→ 觀望

## Step 4:落 §6 + Telegram
