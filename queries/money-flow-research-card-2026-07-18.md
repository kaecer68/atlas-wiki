---
title: 台灣法人錢潮追蹤研究排程卡
created: 2026-07-18
updated: 2026-07-18
type: query
tags: [T, signal, hypothesis, strategy]
sources:
  - concepts/taiwan-money-flow-seven-institutional-buckets.md
  - concepts/t1-t4-signal-light.md
  - atlas-mcp:capital_flow_daily
  - atlas-mcp:backtest_signals
confidence: low
contested: false
contradictions: []
---

# 台灣法人錢潮追蹤研究排程卡

## 研究問題

哪一種「資金目的 × 公開代理」組合，最早且最穩定地辨識台灣錢潮從 SUSPECTED 進入 CONFIRMED，再進入 EXTENDING 或 DISTRIBUTING？

## 第一輪只測三個假說

- **H1 方向一致性**：外資現貨、外資期貨、TSM ADR／SOX、台幣同向，是否比外資連買天數更有預測力？
- **H2 乾淨承接**：機構買超、融資不升或下降，是否較容易延續到第 3／5／10 交易日？
- **H3 資金目的誤判**：投信／ETF／期現套利事件日，是否顯著提高「看似流入、實際短命」的比例？

## 事件表欄位

```text
event_id
signal_date
asset_or_index
institution_bucket
proxy_source
proxy_zscore
spot_direction
futures_direction
adr_sox_direction
fx_direction
retail_margin_direction
etf_flow_context
event_context
state_at_detection
return_d1
return_d3
return_d5
return_d10
state_after_d5
failure_reason
```

## 判定規則（研究版，不是交易門檻）

- **SUSPECTED**：一個 proxy z-score 超過歷史第 90 百分位。
- **CONFIRMED**：至少兩個不同市場／不同資金目的 proxy 同向，且沒有 T1／T2 反向衝突。
- **EXTENDING**：第 3 日仍有至少兩個 proxy 同向，且價格沒有跌回事件日區間下方。
- **DISTRIBUTING**：價格仍強，但機構、融資、期現或 ETF 流向至少兩組分歧。
- **EXITED**：確認條件消失，或 `CIRCUIT_BREAKER` 啟動。

## 不採用的直接規則

- 外資連買 5 天 = 安全 7–14 天
- 主力成本線 ±3% = 護盤區
- 借券增加 + 股價上漲 = 對沖建倉
- 期貨淨多 20,000 口 = 強烈看多

這些先當成待驗證候選，不當作系統規則。

## 預期產物

下一輪建立 `queries/money-flow-event-replay-<date>.md`，只放真實事件回放結果，不先寫理論性安全窗口。
