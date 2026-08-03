# SOX+外資買超 觸發模板(單日版)

**觸發條件(單日)**:SOX change > 0%(收紅)+ 當日外資買超
**對位**:ATLAS_METHODOLOGY.md §二 Layer 2(美股科技動能)
**對位 strategy**:sox-foreignflow-semiconductor(L2, hit_rate 0.33)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **SOX +0.07%** ✅(change_pct > 0)
- **foreign_investor_net +21.83 億** ✅(當日買超)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(sox_index/change_pct)

## Step 2:自動跑端點
- mcp__atlas_mcp__capital_flow_summary(半導體 80% inflow)
- mcp__atlas_mcp__risk_get_correlation_matrix(半導體 ↔ 散熱 0.96)

## Step 3:建議
- 觸發成功 → **加碼半導體 5%**
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram
