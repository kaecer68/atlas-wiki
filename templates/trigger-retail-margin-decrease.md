# 散戶融資大減 觸發模板(衰竭訊號版)[2026-08-22 audit-fix]

**觸發條件**:融資餘額較近 60 日高點減少 > 15%,且近 5 日不再大減(對位 ATLAS_METHODOLOGY.md §三 低迷期指標「融資餘額 | 較高點減少 > 15%,且近 5 日不再大減」)[2026-08-22 audit-fix]
**對位**:ATLAS_METHODOLOGY.md §二 Layer 6 + §四 散戶
**對位 strategy**:margin-balance-extreme(L4, hit_rate 0.62, 50/81)

## Step 1:信號捕捉(對位真實 2026-08-03,舊快照)
- **retail_margin_balance 5074.63 億**(2026-08-03 舊高水位快照,未做 60 日高點減幅判定 [2026-08-22 audit-fix])
- **retail_short_balance 1.88 億**(短線對沖)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(retail_margin_balance + retail_short_balance)

## Step 2:自動跑端點
- mcp__atlas_mcp__capital_flow_summary(retail_signal)
- mcp__atlas_mcp__risk_get_metrics(var_95 -38.69%)

## Step 3:建議
- 觸發(融資較近 60 日高點 -15% 且近 5 日不再大減)→ **衰竭訊號:低迷末端布局參考**(對位 trigger-margin-350b 反向)
- 未觸發 → 觀望

## Step 4:落 §6 + Telegram

**與 trigger-margin-350b 的差異**:350b 是融資高水位**過熱警訊(多頭末端)**;本檔是融資大幅縮減的**衰竭訊號(低迷末端布局參考)**。方向相反,不可混用 [2026-08-22 audit-fix]

參見:[[concepts/retail-sentiment-indicators]]（L6 散戶情緒反向指標——衰竭/斷頭潮判讀）[2026-08-22 audit-fix 接線]
