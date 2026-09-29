---
description: SOX 單日 >+1.5% 且站回 50 日線、當日外資買超 >50 億時載入本模板。
last_verified: "2026-09-30"
verify_by: pending
l3_run_at: 2026-09-30T02:30:00+08:00
l3_run_by: "@cio (atlas-skill-inbound §CIO-1404 補強)"
l3_endpoints_probed:
  - "mcp__atlas__macro_get_snapshot_latest → sox_index.value=12648.198, change_pct=1.47, timestamp_unix=1790706100 (2026-09-30T02:21:40+08:00)"
  - "mcp__atlas__macro_get_snapshot_latest → foreign_investor_net.value=-3.418389 hundred_million_shares, change_pct=3.595, timestamp_unix=1790611200 (2026-09-30)"
  - "mcp__atlas__capital_flow_summary → foreign z_score=-0.797, trend=bearish (2026-09-29T18:26:35Z)"
---

# SOX+外資買超 觸發模板(單日版)

**觸發條件(單日)**:SOX 單日 > +1.5% 且站回 50 日線 + 當日外資買超 > 50 億(對位憲章 §五「SOX 在 50 日線下不做多」)[2026-08-22 audit-fix]
**對位**:ATLAS_METHODOLOGY.md §二 Layer 2(美股科技動能)
**對位 strategy**:sox-foreignflow-semiconductor(L2, hit_rate 0.33；hit_rate 為**舊 SOX > 0% 條件快照 [2026-08-22 audit-fix]**)

## Step 1:信號捕捉(對位真實 2026-09-30,L3 實跑)
- **SOX +1.47%**(2026-09-30T02:21:40+08:00,value 12648.198;**接近但未達** +1.5% 門檻,差 0.03pp)
- **foreign_investor_net -341.84 億**(2026-09-30,value -3.418389 hundred_million_shares × 100 = -341.84 億;**反向** > +50 億門檻)
- **觸發判定**:**未觸發**(兩腿皆未達)
- 對位端點:mcp__atlas_mcp__macro_get_snapshot_latest(sox_index/change_pct + foreign_investor_net)
- **待查**:SOX 50 日線站回狀態 — atlas-mcp 無歷史序列端點(`macro_get_snapshot_history` 僅回總經指標,不含個股指數時序),**結構性缺口,待 client 端 quote polling 累積**(對位 _inbox.md D6「SK-20 60 日歷史端點缺口」)

## Step 2:自動跑端點
- mcp__atlas_mcp__capital_flow_summary(L3 實跑 2026-09-30:foreign z=-0.797 / futures z=-1.251 / dealer z=-1.506 / govt z=+0.89 / retail z=+1.249;**勢力對抗**,strong_outflow)
- mcp__atlas_mcp__risk_get_correlation_matrix(半導體 ↔ 散熱 0.96;**待實跑驗證舊值**,2026-09-30 未跑)

## Step 3:建議
- 觸發成功 → **加碼半導體 5%**
- 觸發失敗(2026-09-30 狀態)→ 觀望

## Step 4:落 §6 + Telegram
