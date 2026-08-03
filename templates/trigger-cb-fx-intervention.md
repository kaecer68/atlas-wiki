# 央行匯市干預 觸發模板(單日版)

**觸發條件(單日)**:USD_TWD > 32.5(央行干預防線)
**對位**:ATLAS_METHODOLOGY.md §二 Layer 1(外匯/央行)
**對位 strategy**:cb-fx-intervention-warning(L4, hit_rate 0, sample 0)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **USD_TWD 32.38** ❌(< 32.5,**未觸發** — 結構性誠實標)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(usd_twd)

## Step 2:自動跑端點
- mcp__atlas_mcp__capital_flow_summary(央行 govt_flow_net = 0)
- mcp__atlas_mcp__risk_get_metrics

## Step 3:建議
- USD_TWD > 32.5(觸發)→ **減外銷/出口導向股 5%**
- USD_TWD < 32.5(未觸發)→ **觀望**

## Step 4:落 §6 + Telegram
