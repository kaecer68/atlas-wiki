# 散戶融資大減 觸發模板(單日版)

**觸發條件(單日)**:retail_short_balance 變化(短線對沖意願)
**對位**:ATLAS_METHODOLOGY.md §二 Layer 6 + §四 散戶
**對位 strategy**:margin-balance-extreme(L4, hit_rate 0.62, 50/81)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **retail_margin_balance 5074.63 億**(融資餘額高)
- **retail_short_balance 1.88 億**(短線對沖)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(retail_margin_balance + retail_short_balance)

## Step 2:自動跑端點
- mcp__atlas_mcp__capital_flow_summary(retail_signal)
- mcp__atlas_mcp__risk_get_metrics(var_95 -38.69%)

## Step 3:建議
- 融資 > 5000 億(觸發)→ **減倉 30% + 避開中小型股/題材股**
- 融資 < 5000 億(未觸發)→ 觀望

## Step 4:落 §6 + Telegram
