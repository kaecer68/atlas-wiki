# 中國經濟放緩 觸發模板(單日版)

**觸發條件(單日)**:銅價 + 0.5% 以上(中國是銅大消費國,銅價上漲 = 中國需求強;銅價跌 = 中國需求弱)
**對位**:ATLAS_METHODOLOGY.md §二 Layer 5 + §四 出口
**對位 strategy**:china-slowdown-export-pressure(L5, hit_rate 0.58)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **copper +1.63%** ✅(> 0.5%,中國需求強訊號,放緩訊號未觸發)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(copper/change_pct)

## Step 2:自動跑端點
- mcp__atlas_mcp__risk_exposure(sector exposure)
- mcp__atlas_mcp__risk_get_correlation_matrix(電子 ↔ 塑化)

## Step 3:建議
- 銅價 +1.63% > 0(中國需求強)→ **觀望出口股下修風險**
- 銅價 -0.5%(中國放緩)→ **減塑化/出口股 5%**

## Step 4:落 §6 + Telegram
