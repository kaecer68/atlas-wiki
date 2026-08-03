# NVDA+TSM 觸發模板(單日版)

**觸發條件(單日)**:NVDA > +2.0% 漲幅
**對位**:ATLAS_METHODOLOGY.md §二 Layer 2(美股科技動能)
**對位 strategy**:nvidia-tsmadr-confirm(L3, hit_rate 0.30)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **NVDA +2.93%** ✅(觸發 +2.0%)
- TSM ADR +0.23%(未觸發 0.3%)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(nvda/change_pct)

## Step 2:自動跑端點
- mcp__atlas_mcp__risk_get_correlation_matrix(半導體 ↔ 散熱 0.96)
- mcp__atlas_mcp__capital_flow_summary(半導體 80% inflow)

## Step 3:建議
- 觸發成功 → **加碼 AI 鏈 5%**
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram
