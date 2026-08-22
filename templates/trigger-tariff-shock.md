# 對中/台晶片關稅 觸發模板(單日版)

**觸發條件(單日,主條件)**:narrative detector `tariff_shock` 觸發(關稅新聞事件)[2026-08-22 audit-fix]
**確認條件(降格)**:USD_TWD > 32 + 出口電子指數 > 0(對位 export 風險;主條件成立後作確認)[2026-08-22 audit-fix]
**對位**:ATLAS_METHODOLOGY.md §二 Layer 5(關稅衝擊)
**對位 strategy**:us-tariff-shock-tech(L5, hit_rate 0.85)

## Step 1:信號捕捉(對位真實 2026-08-03,舊快照)
- **USD_TWD 32.38 > 32** ✅(確認條件成立)
- **export_electronics +14.96%** ✅(月增,確認條件成立)
- tariff_shock 事件主條件:需以 narrative detector 驗證(2026-08-03 快照未含關稅事件判定 [2026-08-22 audit-fix])
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(usd_twd + export_electronics)

## Step 2:自動跑端點
- mcp__atlas_mcp__capital_flow_summary(出口股資金)
- mcp__atlas_mcp__risk_get_correlation_matrix(半導體 ↔ 出口)

## Step 3:建議
- 觸發成功(tariff_shock 事件 + 確認條件成立)→ **半導體短期受壓,加碼防禦性 5%**
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram

**說明**:原觸發條件(USD_TWD > 32 + 出口電子指數 > 0)不含任何關稅變數,名實不符;2026-08-22 修正為 tariff_shock 新聞事件主條件 + 經濟變數確認條件 [2026-08-22 audit-fix]
