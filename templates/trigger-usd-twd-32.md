# USD_TWD 32+ 觸發模板(單日版)

**觸發條件(單日)**:USD_TWD > 32.3
**對位**:ATLAS_METHODOLOGY.md §二 Layer 1(外匯/利率)
**對位 strategy**:usd-twd-32-managed-float(L4, hit_rate 0.62, rank 1)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **USD_TWD 32.38** ✅(觸發 > 32.3)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(usd_twd/value)

## Step 2:自動跑端點
- mcp__atlas_mcp__capital_flow_summary(外資期貨 -82515)
- mcp__atlas_mcp__risk_get_metrics(var_95 -38.69%)

## Step 3:建議
- 觸發成功 → **減半導體至 40% + 加金融/高股息至 35%**
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram
