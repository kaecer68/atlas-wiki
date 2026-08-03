---
title: Week 1 — 散戶 AI 實戰金融工程研究彙整
created: 2026-07-17
updated: 2026-07-17
type: summary
tags: [L, T, S, framework, hypothesis, time-anchor]
sources:
  - entities/l1-t3-five-chains.md
  - queries/day-2-L1T3-three-dimensions-2026-07-17.md
  - concepts/s-paradigm-redefinition.md
  - concepts/t1-t4-signal-light.md
  - concepts/atlas-mcp-interpretation-guide.md
confidence: medium
contested: true
contradictions: [queries/day-2-L1T3-three-dimensions-2026-07-17]
---

# Week 1 — 研究彙整

## 一句話結論

第一週完成了知識骨架與第一輪 MCP 補驗；目前最可靠的成果不是「找到買點」，而是確認 **L1 結構可成立、L2 路徑未收斂、MCP 自身存在時間與語義矛盾**。

## Day 1–7 做了什麼

- **Day 1**：建立 atlas-wiki、SCHEMA、index、log；完成 L1-T.3 五鏈、S 範式、T1→T4、MCP 解讀指南。
- **Day 2**：先因 routing 失敗以 paper 推導，後在 MCP 恢復後補驗；新增「AI capex 與流動性收縮同時存在」的矛盾證據。
- **Day 3**：建立 L1-T overview 與 L1-T.1–T.6 raw symbolic link。
- **Day 4–6**：從 multi paper 抽出 L1-T.1、T.2、T.4、T.5、T.6 entity pages；保留原始資料並標示時間尺度限制。
- **Day 7**：本頁、lint 與排程修復完成。

## 目前學到的三個東西

1. **L1 不等於交易訊號**：能源、人口、礦物、AI 等是 3–50 年結構；落到台股前必須經過 L2 制度與 L3 資金。
2. **S 是紊亂，不是沒資料**：MCP 同時給 AI capex inflow、JPY carry unwind、TSM ADR 下跌、法人流出；這正是「等待 L2 收斂」的狀態。
3. **資料品質本身是研究對象**：`daily_report`、`capital_flow_summary`、`mcp_quickstart` 的方向摘要有差異；timestamp 不一致會製造假因果。

## 第一週保留的待驗證假說

- AI capex 強鏈是否能穿透 T1→T2→T3，形成外資與本土法人同步承接。
- `JPY_carry_unwind` 是短期雜訊，還是會壓過 AI capex 的流動性主導鏈。
- 「72 小時解讀差」能否用事件時間、首次 narrative 偵測時間、TSM ADR／外資／法人反應時間做量化。
- L1-T.4 礦物、L1-T.5 AI、L1-T.6 人口是否其實是同一條「人口／能源／算力瓶頸」耦合鏈，而非三個獨立主題。

## Week 2 排程方向

- **先做資料衛生**：所有 MCP 快照保存 UTC timestamp、source、tool name，避免跨時間拼接。
- **再做 L1-T.3 事件回放**：不追求漂亮 backtest，先建立「訊號首次出現 → T1/T2/T3 收斂或失敗」的小樣本事件表。
- **再進 Stage 1C**：建立 L/T/S 對比與三範式 summary，但不把它包裝成新版本號。
- **最後才決定是否擴充 raw**：只連與當週研究問題直接相關的 source，避免把整個 atlas-notes 變成噪音。

## 風險與未知道

- raw paper 中部分 2026 事件與數字仍是待外部核驗來源，不應直接當成已證實事實。
- entity pages 有部分超過 200 行；這是從原 paper 抽出的暫存 compiled page，後續若持續更新應拆成「結構」與「即時驗證」兩頁。
- MCP 的 confidence / hit rate 是模型欄位，不等於本次事件的成功概率。

## 相關頁面

- [[entities/l1-t-overview]]
- [[entities/l1-t3-five-chains]]
- [[queries/day-2-L1T3-three-dimensions-2026-07-17]]
- [[concepts/s-paradigm-redefinition]]
- [[concepts/t1-t4-signal-light]]
