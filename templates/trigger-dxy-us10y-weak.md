# DXY 弱觸發模板(單日版)

**觸發條件(單日)**:DXY < 100
**對位**:ATLAS_METHODOLOGY.md §二 Layer 1(外匯/利率)
**對位 strategy**:dxy-weak-us10y-down(L1, hit_rate 0.68, rank 2)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **DXY 99.74** ✅(觸發 < 100)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(dxy/value)

## Step 2:自動跑端點
- mcp__atlas_mcp__mcp_quickstart(regime RISK_ON)
- mcp__atlas_mcp__capital_flow_summary(quality_score 4.02)

## Step 3:建議
- 觸發成功 → **加碼半導體至 60%**(亞洲資產重估)
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram
