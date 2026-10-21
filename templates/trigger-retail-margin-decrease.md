---
description: 融資餘額較近 60 日高點減少 >15% 且近 5 日不再大減時載入本模板。
last_verified: 2026-10-22
verify_by: l3_endpoint
l3_run_at: 2026-10-22T02:30:00+08:00
l3_endpoints_probed:
  - mcp__atlas__capital_flow_summary
  - mcp__atlas__macro_get_snapshot_latest
sources:
  - mcp__atlas__macro_get_snapshot_latest (retail_margin_balance, L3 live 實測 2026-10-22T02:30:00+08:00)
  - mcp__atlas__capital_flow_summary (retail force, source_id SRC-TWSE-MARGN, L3 live 實測 2026-10-22T02:30:00+08:00)
---

# 散戶融資大減 觸發模板(衰竭訊號版)[2026-08-22 audit-fix]

**觸發條件**:融資餘額較近 60 日高點減少 > 15%,且近 5 日不再大減(對位 ATLAS_METHODOLOGY.md §三 低迷期指標「融資餘額 | 較高點減少 > 15%,且近 5 日不再大減」)[2026-08-22 audit-fix]
**對位**:ATLAS_METHODOLOGY.md §二 Layer 6 + §四 散戶
**對位 strategy**:margin-balance-extreme(L4, hit_rate 0.62, 50/81)

## Step 1:信號捕捉(L3 實跑 2026-10-22T02:30:00+08:00)
- **retail_margin_balance 6443.73559 億**(2026-10-22 實跑,recorded_at=1792607302,ts=2026-10-22T01:48:22+08:00;vs 2026-10-02 實跑 6298.67 億 **+2.30% 續升**;vs 2026-08-03 舊高水位 5074.63 億 **+26.98%**,**遠未觸發「較近 60 日高點減少 >15%」衰竭訊號**)
- **retail_short_balance 1.92598 億**(2026-10-22 實跑,vs 2026-10-02 實跑 2.33322 億 **-17.46%**)
- **margin_maintenance_ratio 191.819**(2026-10-22 實跑,ts=1790771992;與 2026-10-02 實跑同值,欄位未更新)
- **capital_flow_summary retail**:raw_value=-9.814772879579053 pct_composite,trend=bearish,z_score=-1.599,sample_count=65(as_of_trading_date=2026-10-22,source=SRC-TWSE-MARGN);behavioral direction=mixed,**散戶為 opposing 方**
- 對位端點:mcp__atlas__macro_get_snapshot_latest(recorded_at=1792607302)+ mcp__atlas__capital_flow_summary(retail z_score -1.599)

## Step 2:自動跑端點
- mcp__atlas__capital_flow_summary(retail_signal bearish z=-1.599)
- mcp__atlas__risk_get_metrics(var_95)

## Step 3:建議
- 觸發(融資較近 60 日高點 -15% 且近 5 日不再大減)→ **衰竭訊號:低迷末端布局參考**(對位 trigger-margin-350b 反向)
- 未觸發 → 觀望

## Step 4:落 §6 + Telegram

**與 trigger-margin-350b 的差異**:350b 是融資高水位**過熱警訊(多頭末端)**;本檔是融資大幅縮減的**衰竭訊號(低迷末端布局參考)**。方向相反,不可混用 [2026-08-22 audit-fix]

參見:[[concepts/retail-sentiment-indicators]]（L6 散戶情緒反向指標——衰竭/斷頭潮判讀）[2026-08-22 audit-fix 接線]
