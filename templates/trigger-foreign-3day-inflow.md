# 外資買超觸發模板(3日版)[2026-08-22 audit-fix]

**觸發條件(3日)**:外資現貨連續 3 日累計買超 > +100 億台幣(對位 concepts/taiwan-chip-flow-analysis.md「單日 100 億以上為大動作」口徑)[2026-08-22 audit-fix]
**對位**:ATLAS_METHODOLOGY.md §二 Layer 4 + §四 外資
**對位 strategy**:foreign-3day-inflow(L2, hit_rate 0.37, 17/46；hit_rate 為**舊單日 +20 億條件快照 [2026-08-22 audit-fix]**)

## Step 1:信號捕捉(對位真實 2026-08-03,舊快照)
- **foreign_investor_net +21.83 億**(2026-08-03 單日值,未達 3 日累計 +100 億新門檻；舊單日 +20 億判定已廢除 [2026-08-22 audit-fix])
- 對位端點:mcp__atlas_mcp__capital_flow_summary(外資 z_score 2.489)

## Step 2:自動跑端點
- mcp__atlas_mcp__macro_get_snapshot_latest(foreign_futures_oi_net -82515)
- mcp__atlas_mcp__mcp_quickstart(8/3 turnaround_down / RISK_ON)

## Step 3:建議
- 觸發成功 + RISK_ON → **加碼權值股 5%**
- 觸發成功 + RISK_OFF → 觀望(護盤警訊)
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram
