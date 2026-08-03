---
title: Day 2 — L1-T.3 三層框架應用（MCP 補驗）
created: 2026-07-17
updated: 2026-07-17
type: query
tags: [L, query, three-layers, framework, signal, hypothesis, time-anchor]
sources:
  - raw/papers/atlas-original-paper-v0.1-L1T3-five-chains.md
  - concepts/atlas-mcp-interpretation-guide.md
  - entities/l1-t3-five-chains.md
  - atlas-mcp:mcp_quickstart
  - atlas-mcp:capital_flow_summary
  - atlas-mcp:narrative_get_bundle
  - atlas-mcp:event_calendar
confidence: medium
contested: true
contradictions: [entities/l1-t3-five-chains]
---

# Day 2 — L1-T.3 三層框架應用（MCP 補驗）

> **一句話**：MCP 已恢復，但它沒有替 L1-T.3 證明「五鏈同步收斂」；反而顯示「AI 資本支出流入」與「日圓套利平倉／台股資金流出」同時存在，現在比較像 S 型訊號紊亂，不是可直接交易的單方向確認。

## 1. 補驗時間錨與資料邊界

- MCP 回傳資料時間：2026-07-16 21:26–21:29 UTC（台灣時間 2026-07-17 凌晨）。
- 本頁不是「當天完整市場真相」：工具資料有不同 timestamp，且 `mcp_quickstart`、`capital_flow_summary` 的摘要並不完全一致。
- 因此本頁把原本 `confidence: low` 升為 **medium**，但把矛盾標為 `contested: true`，不升為 high。

## 2. MCP 層：看到的不是單一方向

### 支持 L1-T.3「鏈正在被觸發」的證據

- narrative bundle 偵測到 `AI_capex_surge`：confidence 0.95、severity high，資本流方向是科技資本支出流入，預計至 2026-07-23。
- 同一 bundle 偵測到 `JPY_carry_unwind`：confidence 約 0.664、方向是全球流動性收縮，預計至 2026-07-21。
- 事件日曆同時有法說會旺季、除權息旺季與期貨結算，表示台股存在互相拉扯的事件背景，不是乾淨的單一 regime。

### 反駁「已經收斂」的證據

- `capital_flow_summary` 判定 `strong_outflow`、`resonance_dir: bearish`，主導力量是 TSM ADR，TSM ADR -2.32%、SOX -4.29%。
- 台股法人流向亦偏弱：dealer -3.13、domestic fund -0.235；散戶反向偏多，形成「機構弱、散戶強」的分歧。
- quickstart 的 active strategy 仍列 AI 資本支出與外資連買等偏多策略，但最新流向沒有確認這些策略已在現貨層兌現。

## 3. 三層整合判斷

| 層 | 目前讀法 | 可支持的結論 | 不能支持的結論 |
|---|---|---|---|
| MCP | AI capex 強，但 ADR/法人流出、日圓套利風險並存 | L1-T.3 的部分鏈條正在動 | 五鏈已收斂、可直接進場 |
| 學術 | 跨市場、能源、資金與風險狀態可互相傳導 | 物理耦合機制合理 | 精確判斷本週哪條鏈主導 |
| barbaric signals | 機構賣、散戶接、夜盤科技指標弱，但 AI 資本支出敘事仍強 | 市場正在做方向選擇 | 判定最終 L2 路徑 |

**目前最合理的讀法**：L1 結構仍成立，L2 正在分叉；「AI capex」是局部強鏈，「流動性／機構撤退」是反向鏈。按照 kaecer 的 S 定義，這應標成訊號紊亂，等待 T1→T2→T3 收斂，而不是把 narrative 的高 confidence 當成可獲利概率。

## 4. 對四個待驗證假說的更新

| 假說 | 補驗結果 | 狀態 |
|---|---|---|
| 五鏈 30 天內同步觸發 | MCP 只直接看到 AI capex、JPY、科技旺季等部分鏈；無法證明五鏈同步 | **未證明，low** |
| L1-T.3 轉入 T 的訊號 | AI capex 與流動性收縮同時出現；目前不是轉換確認 | **候選訊號，low** |
| 72 小時解讀差可量化 | 本次只得到一個截面，沒有歷史對照或交易結果 | **未驗證，low** |
| 主導鏈是哪條 | 最新 MCP 將主導力量指向 TSM ADR / 流動性，而非氣候或糧食 | **暫時改判為流動性鏈，low** |

## 5. 新漏洞：同一系統內的語義與時間矛盾

這次補驗最有價值的不是「AI 資本支出看多」，而是發現三個漏洞：

1. **摘要矛盾**：先前 `daily_report` 曾給「外資、dealer 偏多／資金 moderate inflow」，但同時 `global.status=RISK_OFF`；本次 `capital_flow_summary` 則是 `strong_outflow`。這不能直接拼成一個方向。
2. **策略與現貨脫節**：active strategy 的 hit rate 是歷史條件統計，不代表本次事件已通過 T1→T2→T3；AI supercycle model 的近期 `recent_error=1` 更不能被忽略。
3. **時間戳不一致**：日曆事件、macro snapshot、narrative bundle 並非完全同一時間截面；若不保留 timestamp，會把先後關係誤讀成因果關係。

## 6. 可執行的觀察，不是交易結論

接下來只追三個收斂條件：

- **T1**：SOX、TSM ADR 是否止跌並重新同步轉強。
- **T2**：外資是否連續轉為淨買，且不是只有單日反彈。
- **T3**：dealer／投信是否停止賣超，與外資方向一致。

三者沒有同時出現前，本頁只支持「等待 L2 路徑選擇」，不支持把 AI capex 事件直接轉成台股買入訊號。

## 相關頁面

- [[entities/l1-t3-five-chains]]
- [[entities/l1-t-overview]]
- [[concepts/atlas-mcp-interpretation-guide]]
- [[concepts/s-paradigm-redefinition]]
- [[concepts/t1-t4-signal-light]]

## 來源

- atlas-mcp `mcp_quickstart`，2026-07-16 snapshot
- atlas-mcp `capital_flow_summary`，2026-07-16 21:26 UTC
- atlas-mcp `narrative_get_bundle`，2026-07-16 21:29 UTC
- atlas-mcp `event_calendar`
- `raw/papers/atlas-original-paper-v0.1-L1T3-five-chains.md`
