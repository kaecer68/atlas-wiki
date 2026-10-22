---
description: 外資現貨連續 3 日累計買超 >+100 億台幣時載入本模板。
last_verified: 2026-10-23
verify_by: l3_endpoint
l3_run_at: 2026-10-23T02:31:00+08:00
l3_endpoints_probed:
  - mcp__atlas__capital_flow_summary
  - mcp__atlas__macro_get_snapshot_latest
sources:
  - mcp__atlas__macro_get_snapshot_latest (foreign_investor_net, L3 live 實測 2026-10-23T02:31:00+08:00)
  - mcp__atlas__capital_flow_summary (foreign/dealer force, L3 live 實測 2026-10-23T02:31:00+08:00)
---

# 外資買超觸發模板(3日版)[2026-08-22 audit-fix]

**觸發條件(3日)**:外資現貨連續 3 日累計買超 > +100 億台幣(對位 concepts/taiwan-chip-flow-analysis.md「單日 100 億以上為大動作」口徑)[2026-08-22 audit-fix]
**對位**:ATLAS_METHODOLOGY.md §二 Layer 4 + §四 外資
**對位 strategy**:foreign-3day-inflow(L2, hit_rate 0.37, 17/46；hit_rate 為**舊單日 +20 億條件快照 [2026-08-22 audit-fix]**)

## Step 1：信號捕捉（L3 實跑 2026-10-23T02:31:00+08:00；⚠️ atlas backend 重算敏感值）

> **⚠️ atlas backend 結構性重算偵測（H-RG-02，§CIO-1411 precedent 第 3 次確認）**：本頁數值於 **24 小時內兩度反轉**，詳見下方「重算軌跡」。**任何量化結論在 backend 數值穩定前僅供方向參考**。

**今日 live（recorded_at=1792693476 = 2026-10-23T02:24:36+08:00；as_of_trading_date=2026-10-23）**：

- **foreign_investor_net.value = -2.84113812 hundred_million_shares = -2.84 億張（賣超）** — 2026-10-23 實跑；ts=1792598400
- **foreign_futures_oi_net = -86072 contracts**（as_of_trading_date=2026-10-21）
- **current_period = turnaround_down（轉折下壓）**（與 10-22 同，未翻轉）
- **capital_flow_summary**：dominant_actor=**dealer**／dominant_force=**dealer**／dominant_signal=futures；quality_label=**strong_outflow**（quality_score -2.99）；resonance_dir=**bearish**；summary=「資金強勁流出，校準中。」
- 外資 force：trend=bearish，z_score=**-0.67**，leading_z=-1.438（futures，bearish）
- 自營商 force：raw_value=-15.53936358 億張，z_score=**-2.343**（本輪最弱 force）

**重算軌跡（同一 template、跨 3 個 tick，證明數值非穩定）**：

| tick | foreign_investor_net | quality_label | dominant_actor | retail z_score |
|---|---|---|---|---|
| 2026-08-03（原始） | +21.83 億 | — | — | — |
| 2026-10-02 | -16.81 億 | — | — | — |
| 2026-10-22 | **+3.65 億（買）** | strong_inflow | foreign | -1.599 bearish |
| **2026-10-23** | **-2.84 億（賣）** | **strong_outflow** | **dealer** | **+1.631 bullish** |

⇒ **Δforeign_investor_net 10-22 → 10-23 = -6.49 億張**，遠超 §8.2 門檻 3 億張；且 `dominant_actor`、`quality_label`、`retail z_score` **三項同日翻轉**。`current_period` 唯一維持 turnaround_down ＝ 結構面（regime）未變，變動集中在資金流向面。

**觸發判定**：單日 -2.84 億張遠低於 +100 億（3 日累計）門檻，**觸發條件未成立**。

**對位端點**：mcp__atlas__macro_get_snapshot_latest(recorded_at=1792693476) + mcp__atlas__capital_flow_summary(as_of_trading_date=2026-10-23；date=2026-10-22T18:29:44Z)

## Step 2:自動跑端點
- mcp__atlas__macro_get_snapshot_latest(current_period turnaround_down)
- mcp__atlas__capital_flow_summary(dealer dominant_actor; futures dominant_signal)

## Step 3:建議
- 觸發成功 + RISK_ON → **加碼權值股 5%**
- 觸發成功 + RISK_OFF → 觀望(護盤警訊)
- 觸發失敗 → 觀望

## Step 4:落 §6 + Telegram
