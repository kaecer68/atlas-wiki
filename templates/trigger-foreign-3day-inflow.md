---
description: 外資現貨連續 3 日累計買超 >+100 億台幣時載入本模板。
last_verified: 2026-10-22
verify_by: l3_endpoint
l3_run_at: 2026-10-22T02:30:00+08:00
l3_endpoints_probed:
  - mcp__atlas__capital_flow_summary
  - mcp__atlas__macro_get_snapshot_latest
---

# 外資買超觸發模板(3日版)[2026-08-22 audit-fix]

**觸發條件(3日)**:外資現貨連續 3 日累計買超 > +100 億台幣(對位 concepts/taiwan-chip-flow-analysis.md「單日 100 億以上為大動作」口徑)[2026-08-22 audit-fix]
**對位**:ATLAS_METHODOLOGY.md §二 Layer 4 + §四 外資
**對位 strategy**:foreign-3day-inflow(L2, hit_rate 0.37, 17/46；hit_rate 為**舊單日 +20 億條件快照 [2026-08-22 audit-fix]**)

## Step 1:信號捕捉(L3 實跑 2026-10-22T02:30:00+08:00)
- **foreign_investor_net.value = 3.64528245 hundred_million_shares = +3.65 億張**(2026-10-22 實跑單日值,recorded_at=1792607302,ts=2026-10-22T01:48:22+08:00;as_of_trading_date=2026-10-22;**已翻正為買超**,vs 2026-10-02 實跑 -16.81 億張 = **反向翻轉**)
- **foreign_futures_oi_net = -89748 contracts**(2026-10-20;vs 2026-10-02 實跑 -78151,**期貨未平倉淨額進一步走空**,現貨買超 vs 期貨偏空 = **背離**)
- **current_period = turnaround_down(轉折下壓)**(2026-10-22;vs 2026-10-02 實跑 consolidation,**結構由盤整再翻轉下壓**)
- **capital_flow_summary**:dominant_actor=foreign / dominant_force=foreign / dominant_signal=futures;foreign z_score=0.68(bullish)/ leading_z=-1.607(futures,bearish);behavioral=mixed(opposing=retail);quality_label=strong_inflow(quality_score 1.98)
- **3 日累計 >+100 億門檻未觸發**:單日 +3.65 億張遠低於門檻,**現貨單日規模不足以確認觸發**
- 對位端點:mcp__atlas__capital_flow_summary(as_of_trading_date=2026-10-22;date=2026-10-21T18:28:22Z)+ mcp__atlas__macro_get_snapshot_latest(recorded_at=1792607302)

## Step 2:自動跑端點
- mcp__atlas__macro_get_snapshot_latest(current_period turnaround_down)
- mcp__atlas__capital_flow_summary(foreign dominant_actor; futures dominant_signal)

## Step 3:建議
- 觸發成功 + RISK_ON → **加碼權值股 5%**
- 觸發成功 + RISK_OFF → 觀望(護盤警訊)
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram
