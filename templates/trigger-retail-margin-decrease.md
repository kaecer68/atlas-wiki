---
description: 融資餘額較近 60 日高點減少 >15% 且近 5 日不再大減時載入本模板。
last_verified: 2026-10-23
verify_by: l3_endpoint
l3_run_at: 2026-10-23T02:31:00+08:00
l3_endpoints_probed:
  - mcp__atlas__capital_flow_summary
  - mcp__atlas__macro_get_snapshot_latest
sources:
  - mcp__atlas__macro_get_snapshot_latest (retail_margin_balance, L3 live 實測 2026-10-23T02:31:00+08:00)
  - mcp__atlas__capital_flow_summary (retail force, source_id SRC-TWSE-MARGN, L3 live 實測 2026-10-23T02:31:00+08:00)
---

# 散戶融資大減 觸發模板(衰竭訊號版)[2026-08-22 audit-fix]

**觸發條件**:融資餘額較近 60 日高點減少 > 15%,且近 5 日不再大減(對位 ATLAS_METHODOLOGY.md §三 低迷期指標「融資餘額 | 較高點減少 > 15%,且近 5 日不再大減」)[2026-08-22 audit-fix]
**對位**:ATLAS_METHODOLOGY.md §二 Layer 6 + §四 散戶
**對位 strategy**:margin-balance-extreme(L4, hit_rate 0.62, 50/81)

## Step 1：信號捕捉（L3 實跑 2026-10-23T02:31:00+08:00；⚠️ atlas backend 重算敏感值）

> **⚠️ atlas backend 結構性重算偵測（H-RG-02，§CIO-1411 precedent 第 3 次確認）**：本頁 `retail z_score` 於 **24 小時內由 -1.599（bearish）翻正為 +1.631（bullish）**，詳見下方「重算軌跡」。本模板的判讀基礎正是散戶方向，**該值翻轉直接改變結論方向，數值穩定前僅供方向參考**。

**今日 live（recorded_at=1792693476 = 2026-10-23T02:24:36+08:00；as_of_trading_date=2026-10-23）**：

- **retail_margin_balance = 6338.80174 億**（2026-10-23 實跑，ts=1792693480）
  - vs 2026-10-22 實跑 6443.74 億 → **-104.94 億（-1.63%）**
  - vs 2026-08-03 舊高水位 5074.63 億 → **+24.88%**
  - ⇒ **距觸發門檻（較近 60 日高點減少 >15%）仍極遠，且今日為回落方向**
- **retail_short_balance = 2.16539 億**（2026-10-23 實跑；vs 10-22 實跑 1.926 億 → **+12.43%**，空單回補）
- **margin_maintenance_ratio = 191.819**（ts=1790771992，**欄位自 2026-06 前未更新，不可用作當期訊號**）
- **capital_flow_summary retail**：raw_value=**+10.802081909838057** pct_composite，trend=**bullish**，z_score=**+1.631**，sample_count=66（source=SRC-TWSE-MARGN）
  - assessment.behavioral：direction=**bullish**，aligned=[government, retail]（10-22 為 mixed + opposing=retail，**已翻轉**）

**重算軌跡（同一 template、跨 3 個 tick）**：

| tick | retail_margin_balance | retail z_score | 方向 | behavioral |
|---|---|---|---|---|
| 2026-08-03（原始） | 5074.63 億 | — | — | — |
| 2026-10-02 | 6298.67 億 | — | — | — |
| 2026-10-22 | 6443.74 億 | **-1.599** | bearish | mixed（opposing=retail） |
| **2026-10-23** | **6338.80 億** | **+1.631** | **bullish** | **bullish** |

⇒ Δz_score = **+3.23**（方向翻轉）、Δmargin = **-104.94 億**（三個 tick 首次回落）。**融資餘額雖回落 1.63%，距 -15% 門檻仍極遠，觸發條件未成立**；但 `z_score` 翻正代表**散戶當日轉為偏多情緒**，與「衰竭訊號」方向相反，須待 backend 數值穩定後複驗。

**對位端點**：mcp__atlas__macro_get_snapshot_latest(recorded_at=1792693476) + mcp__atlas__capital_flow_summary(retail z_score +1.631；as_of_trading_date=2026-10-23)

## Step 2:自動跑端點
- mcp__atlas__capital_flow_summary(retail_signal bullish z=+1.631)
- mcp__atlas__risk_get_metrics(var_95)

## Step 3:建議
- 觸發(融資較近 60 日高點 -15% 且近 5 日不再大減)→ **衰竭訊號:低迷末端布局參考**(對位 trigger-margin-350b 反向)
- 未觸發 → 觀望

## Step 4:落 §6 + Telegram

**與 trigger-margin-350b 的差異**:350b 是融資高水位**過熱警訊(多頭末端)**;本檔是融資大幅縮減的**衰竭訊號(低迷末端布局參考)**。方向相反,不可混用 [2026-08-22 audit-fix]

參見:[[concepts/retail-sentiment-indicators]]（L6 散戶情緒反向指標——衰竭/斷頭潮判讀）[2026-08-22 audit-fix 接線]
