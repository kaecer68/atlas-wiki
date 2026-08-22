# 融資 3500 億觸發模板(單日版)

**觸發條件(單日)**:retail_margin_balance > 5000 億台幣
**對位**:ATLAS_METHODOLOGY.md §二 Layer 6 + §四 散戶
**對位 strategy**:margin-balance-extreme(L4, hit_rate 0.62, 50/81)

## Step 1:信號捕捉(對位真實 2026-08-03)
- **retail_margin_balance 5074.63 億** ✅(觸發 > 5000)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(retail_margin_balance/value)

## Step 2:自動跑端點
- mcp__atlas_mcp__risk_get_metrics(var_95 -38.69%)
- mcp__atlas_mcp__risk_exposure(sector exposure)

## Step 3:建議
- 觸發成功 → **減倉 30% + 避開中小型股/題材股**
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram

> 註:檔名 350b（3500 億）為舊門檻,現條件 > 5000 億（2026 市值水位校準）;檔名保留以相容引用 [2026-08-22 audit-fix]
> 參見:[[concepts/retail-sentiment-indicators]]（L6 散戶情緒反向指標——融資水位判讀規則）[2026-08-22 audit-fix 接線]
