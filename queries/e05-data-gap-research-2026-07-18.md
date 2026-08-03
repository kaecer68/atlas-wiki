---
title: E05 五主體共振的資料斷層研究：先驗、確認與未知狀態
created: 2026-07-18
updated: 2026-07-18
type: query
tags: [T, signal, hypothesis, framework, contested]
sources:
  - concepts/funding-forces-taxonomy-e05-pending-approval.md
  - concepts/taiwan-money-flow-seven-institutional-buckets.md
  - concepts/t1-t4-signal-light.md
  - user-provided: E05 修復進度說明（2026-07-18）
confidence: low
contested: false
contradictions: []
---

# E05 五主體共振的資料斷層研究

> **狀態：研究中，不等待系統修復完成，也不提前修改正式 E05。**

## 研究問題

當五個主體的資料不同步、缺失或延遲時，E05 應如何區分：

- 真正的中性；
- 資料尚未到達；
- 不同市場的反向交易；
- 主體內部的多目的交易；
- 模型根本不應該做方向判斷的狀態。

## 目前最重要的斷層

### 1. 主體分類與資料取得不同步

外資、投信、自營商通常有每日公開流向；官股行庫與散戶的資料可能是代理估計、延遲或以不同口徑發布。若直接把五類放進同一個共振公式，資料完整度差異會被誤讀成力量差異。

**研究原則**：共振計算需要同時保存 `observed_at`、`data_date`、`source`、`latency`、`quality`；沒有這些欄位，不應產生高信心共振。

### 2. `unknown` 被誤當 `neutral`

這是最危險的資料斷層之一：

- `neutral` = 有資料，觀察到方向接近零。
- `unknown` = 資料缺失、過期、未覆蓋或口徑不明。

兩者不能共用數值 0。否則缺資料的主體會被假裝成「沒有意見」，整體共振看起來比實際更穩定。

### 3. 外資兩個維度的時間角色不同

- T86 現貨：已成交結果，較慢，但較接近實際配置。
- TAIFEX 未平倉：可能領先，但混合方向、避險、套利、展期。

因此不能只做簡單平均。研究上至少要拆成：

```text
外資現貨 = confirmation channel
外資期貨 = leading / hedge-sensitive channel
```

### 4. 情緒特徵可能提前，但不一定代表台灣錢已進出

TSM ADR、VIX、USD/TWD 能提前反映風險偏好或換匯壓力，但它們是輸入特徵，不是主體。它們可以改變外資方向的先驗信心，不能直接增加外資的共振票數。

## 暫定資料狀態機

```text
MISSING
  → STALE（有資料但超過允許延遲）
  → OBSERVED（資料到達但尚未判方向）
  → DIRECTIONAL（標準化後有方向）
  → CONFIRMED（跨維度一致）
  → CONFLICTED（維度反向）
```

### 建議解讀

- `MISSING` / `STALE`：不計入共振，降低整體 confidence。
- `OBSERVED`：只代表資料可用，不代表方向。
- `DIRECTIONAL`：可作單一主體的暫定方向。
- `CONFIRMED`：同一主體的現貨／期貨或不同可靠維度一致。
- `CONFLICTED`：不取平均抹平矛盾，標記外資內部分歧或避險可能。

## 五主體共振不應只有一個分數

建議 E05 至少輸出三個結果：

1. **主體方向矩陣**：五個主體各自的方向與資料品質。
2. **共振方向**：只使用可比、非 unknown 的主體。
3. **可相信程度**：受資料完整度、延遲、來源可靠度與主體間衝突調整。

示意：

```text
subject_direction = {
  foreign: {direction: bullish, state: conflicted, quality: medium},
  mutual_funds: {direction: unknown, state: stale, quality: low},
  dealers: {direction: bearish, state: directional, quality: medium},
  government_banks: {direction: unknown, state: missing, quality: low},
  retail: {direction: bullish, state: directional, quality: medium}
}

resonance_direction = mixed
resonance_confidence = low
```

這比輸出一個看似精確的 `resonance=1` 更誠實，也更能支持後續追蹤。

## 對目前 atlas 快照的研究套用

2026-07-16/17 的資料曾同時出現：

- TSM ADR 偏弱；
- dealer、institutional 偏弱；
- retail 偏多；
- foreign raw value 接近零或 trend neutral；
- narrative 有 AI capex inflow 與 JPY carry unwind；
- backtest signals 啟動 `CIRCUIT_BREAKER`。

按照修正版分類，不能把這些拼成「五主體共振偏空」或「AI 資金流入」。比較合理的狀態是：

> **外部情緒與部分法人維度偏弱，外資主體內部證據未完成確認，散戶反向偏多；整體為 conflicted / low-confidence，而非單一方向。**

## 待修復完成後的驗證清單

- [ ] 五主體各自的 canonical source 與資料 freshness 定義。
- [ ] T86、TAIFEX 的 data_date／observed_at 對齊規則。
- [ ] 官股行庫資料是否為主體資料或代理估計。
- [ ] 散戶方向是融資、現貨、ETF 申贖還是複合 proxy。
- [ ] `unknown`、`neutral`、`conflicted` 在 API schema 中是否分開。
- [ ] ADR、VIX、USD/TWD 是否只進先驗模型，不進主體共振。
- [ ] 權重是否依歷史回放估計，而不是手工指定。
- [ ] CIRCUIT_BREAKER 是否覆蓋共振輸出，避免研究訊號被誤當交易訊號。

## 暫時結論

系統目前最需要的不是再增加一個訊號，而是補上「資料狀態與可信度」這一層。沒有它，五主體分類即使概念正確，也可能被缺失資料、延遲資料與代理共線重新污染。

## 相關頁面

- [[concepts/funding-forces-taxonomy-e05-pending-approval]]
- [[concepts/taiwan-money-flow-seven-institutional-buckets]]
- [[concepts/atlas-mcp-interpretation-guide]]
- [[queries/money-flow-research-card-2026-07-18]]
