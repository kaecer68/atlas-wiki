# DXY 弱觸發模板(單日版)

**觸發條件(單日)**:DXY < 100
**對位**:ATLAS_METHODOLOGY.md §二 Layer 1(外匯/利率) + §5 #1 美台資金開關觀測框架（v1.1 §3↔§5 角色對位：DXY 是 4 元件之一，寬鬆觀測，非 §3 權威判別條件）
**對位 strategy**:dxy-weak-us10y-down(L1, hit_rate 0.68, rank 2)

> **v1.1 對位說明**:DXY 在 §5 #1「美台資金開關」是 US10Y/DXY/USD-JPY/台灣壓力指數 四元件之一，屬「寬鬆觀測框架」，**不直接改變 current_period**（v1.1 §3↔§5 角色對位）。本模板保留「DXY < 100」為信號捕捉，但應明確標示其角色為觀測觸發，非時期判別條件。

## Step 1:信號捕捉(對位真實 2026-08-03)
- **DXY 99.74** ✅(觸發 < 100,屬 §5 #1 美台資金開關觀測之 DXY 元件)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(dxy/value)

## Step 2:自動跑端點
- mcp__atlas_mcp__mcp_quickstart(regime RISK_ON)
- mcp__atlas_mcp__capital_flow_summary(quality_score 4.02)

## Step 3:建議
- 觸發成功 → **加碼半導體至 60%**(亞洲資產重估;對位 §5 #1 觀測觸發,非 §3 時期切換)
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram
