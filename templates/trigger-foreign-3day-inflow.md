# 外資買超觸發模板(單日版)

**觸發條件(單日)**:foreign_investor_net > +20 億台幣
**對位**:ATLAS_METHODOLOGY.md §二 Layer 4 + §四 外資
**對位 strategy**:foreign-3day-inflow(L2, hit_rate 0.37, 17/46)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **foreign_investor_net +21.83 億** ✅(觸發 > 20)
- 對位端點:mcp__atlas_mcp__capital_flow_summary(外資 z_score 2.489)

## Step 2:自動跑端點
- mcp__atlas_mcp__macro_get_snapshot_latest(foreign_futures_oi_net -82515)
- mcp__atlas_mcp__mcp_quickstart(8/3 turnaround_down / RISK_ON)

## Step 3:建議
- 觸發成功 + RISK_ON → **加碼權值股 5%**
- 觸發成功 + RISK_OFF → 觀望(護盤警訊)
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram
