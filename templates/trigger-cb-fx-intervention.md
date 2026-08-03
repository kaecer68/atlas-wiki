# 台灣央行(央行/中央銀行/TW-CBC)匯市干預預警觸發模板

**觸發條件(單日)**:USD_TWD > 32.3(接近台灣央行防線 32.5)
**對位**:ATLAS_METHODOLOGY.md §二 Layer 1(外匯/台灣央行)
**對位 strategy**:cb-fx-intervention-warning(L4, hit_rate 0, sample 0)

## 為什麼台灣央行干預 = 台股警訊?
- **台灣央行職責**:新台幣匯率政策 + 進場拋匯阻升
- **央行防線**:USD_TWD 32(市場心理關線)+ 32.5(央行實際干預區)
- **央行干預**= 後續熱錢效應消退 = 出口股成本競爭力下滑 = 觸發 L4 `usd-twd-32-managed-float` 同向邏輯

## Step 1:信號捕捉(對位真實 2026-08-03)
- **USD_TWD 32.38** ✅(> 32.3,接近台灣央行防線)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(usd_twd)

## Step 2:自動跑端點
- mcp__atlas_mcp__capital_flow_summary(台灣央行 govt_flow_net = 0)
- mcp__atlas_mcp__risk_get_metrics

## Step 3:建議
- USD_TWD > 32.3 接近 32.5(觸發)→ **減外銷/出口導向股 5%**
- USD_TWD < 32.3(未觸發)→ 觀望

## Step 4:落 §6 + Telegram
