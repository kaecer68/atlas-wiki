---
title: 重啟後接手指南
created: 2026-07-19
updated: 2026-07-19
type: summary
tags: [framework, time-anchor]
sources:
  - atlas-notes/04-daily/2026-07-14-session-handoff.md
  - atlas-wiki/log.md
  - atlas/docs/specs/capital-flow-seven-dimension-spec.md
confidence: high
contested: false
contradictions: []
---

# 重啟後接手指南（給下一個 hermes session）

> 用途：你說要重啟 hermes agent。這份是給重啟後那個新 session 看的「第一張地圖」。寫死三件事：mission 立場、當前在哪、不能動什麼。

## 1. Mission 立場（不要再懷疑這層）

- **Mission**：散戶 AI 實戰金融工程
- **對象**：有軟件專業 + 善用 AI 的散戶小資金
- **態度**：悶聲賺小錢、拒絕文縐縐、找漏洞
- **不是**：華爾街、學術金融工程、散戶平均值
- **不裝 finlab / graphify**
- **不寫 v0.5 / v0.6**
- **不倉促下結論**

如果新 session 在這層動搖，請直接刪除整個 session。

## 2. 三範式（L→T→S）

- **L 鐵律**：1 天到 18 月，事件必發生時間帶；會用 AI 散戶靠 72 小時解讀時間差賺錢。
- **T 微趨勢**：0.5–3 年，制度、產業與資金趨勢。
- **S 演化**：不是盤整期，是「訊號紊亂狀態」；S 期間「不輸就是贏」、「等 L2 收斂」。

## 3. 訊號燈 T1→T4

- **T1 美股 = 信號燈**
- **T2 外資 = 引信**
- **T3 其他法人 = 真正指標**
- **T4 散戶 = 鏡像 / 韭菜**

四層不是平等的：T1 是真相源頭，T2 是傳遞者，T3 是對殺者，T4 是落後鏡像。

## 4. 錢潮追蹤：3+2+2 七維分層（不要用五主體共振）

這一段在 2026-07-19 之前的舊概念（5 主體、7 勢力同級）**已過時**。

以 `docs/specs/capital-flow-seven-dimension-spec.md` 為唯一正本：

```text
七維錢潮雷達
├── 官方法人資金流（3）official_actor
│   ├── foreign
│   ├── institutional
│   └── dealer
├── 行為代理資金流（2）behavioral_proxy
│   ├── government（資料需 data quality gate）
│   └── retail（融資融券變化 proxy）
└── 領先／跨市場訊號（2）
    ├── futures（TAIFEX 外資期貨 OI，positioning_indicator）
    └── tsm_adr（cross_market_signal）
```

關鍵規則：

- **actor consensus 只用 3 個 official_actor**
- **futures / TSM ADR 不進 actor consensus**
- **3 個 official_actor 也不能視為同質主體**，因 dealer 含避險
- **官股必須 data quality gate 達標才能用**
- **融資融券只是散戶代理**，非完整自然人交易流
- **T86 是股數除以 1e8，不是新台幣億元**
- **期貨口數不能與 T86 億股直接加權**
- **legacy `weight = abs(raw)/sum(abs(raw))` 不可當勢力權重**
- **缺資料不寫 0，不解讀為 neutral**
- **API 讀取必須純讀**，不能 push rolling window
- **每個 dimension 每天最多一個 rolling sample**

## 5. 工具紀律

- atlas-mcp 共 111 個 tool，預設啟用。
- 每次 tool call 前先回答三個問題：用戶要決定什麼？好答案長什麼樣？最低證據是什麼？
- Tool 0.5 confidence = 不知道，不要美化。
- 永遠 3 段結構：證據 / 我的解讀 / 我沒把握的。
- 6 個月 forward 問題用三層 framework：MCP + 學術 + barbaric signals。
- barbaric signals 是主戰場，學術層只解釋 live signal 為什麼有意義。

## 6. 排程

- 主要 cron：`6a96a1298428`，每日 `0 0 * * *`，名稱「atlas-wiki 夜間研究：錢潮追蹤與事件回放」。
- Deprecated cron：`f04231a80f02` 已 pause。
- 交接提示詞裡明確寫到：
  - E05 尚未通過業主簽核，cron 不得改正式權重。
  - 只能做研究、事件回放、資料品質檢查。

## 7. 互動格式（拍板不可改）

- 一句結論 + 3–5 個粗體 bullet + 風險單列
- 不長篇大論
- 不在回報前請示「是否需要拍板」
- 確認問題（Rule 8）只回答 yes/partial/no + 一行證據，不變成清單

## 8. 當前在哪（next session 應知道的事實）

- **已落地（語意層）**：3+2+2 分層已在活體輸出觀察到；API 契約欄位齊全。
- **未完成（invariant 層）**：
  - CF-INV-04 純讀性待單元測試驗證
  - CF-INV-06 `government` 缺資料寫 0 的狀況需處理
  - CF-INV-08 QualityAssessment 跨 daily / summary 一致性
  - CF-INV-12 `runtime.commit: "unknown"` 需對帳部署 commit
- **E06 收尾後才能正式說「E05 已修正完」**。
- **SA11 dark launch 達標條件**：≥20 sessions。
- **資料源異常**：`us_yahoo`（circuit breaker）、`twse_replay`（timeout）。
- **回測快照過舊**：`backtest_stale: true`，window 仍是 2026-07-14，但 replay 已到 2026-07-18。

## 9. 接手時的 5 步檢查（請新 session 嚴格照做）

1. **讀這份**與 `atlas-wiki/index.md`、`atlas-wiki/log.md` 末三條。
2. **先確認 atlas-mcp 可用**：`hermes mcp test atlas-mcp`。若 110 個以下或 120 個以上，視為工具清單漂移，停下回報。
3. **拉一次 `daily_report` 與 `capital_flow_daily`**，對照 spec §6 與 §7 的欄位，不符停下回報。
4. **檢查 cron**：`cronjob action=list`，確認 `6a96a1298428` 仍在、prompt 仍提到「不得修改正式權重」。
5. **不要先打開任何 wiki page 改內容**。先給用戶一句「接手完成，現況是 X」報告，等用戶指示再動 wiki。

## 10. 新 session 不該主動做的事

- 不要重新發明 E05 框架。
- 不要把「五主體」或「七大勢力同級」當成新說法。
- 不要把 model 的 confidence 當成功率。
- 不要把融資融券當成完整散戶流。
- 不要把 T86 億股直接當資金金額。
- 不要把 futures / TSM ADR 寫成資金主體。
- 不要為了 0.95 confidence 就把 AI capex 寫成可交易訊號。
- 不要在 7 維之外再加新的「獨立勢力」。

## 11. 遇到卡關時的求助路徑

- 工具欄位對不上：先看 `docs/specs/capital-flow-seven-dimension-spec.md` §6/§7。
- 找不到原因：先看 `atlas-wiki/concepts/atlas-mcp-interpretation-guide.md`。
- 分類爭議：先看 `atlas-wiki/concepts/funding-forces-taxonomy-e05-pending-approval.md`（注意：標 contested 為待業主簽核，cron 不得改正式權重）。
- L/T/S 範式：先看 `atlas-wiki/comparisons/l-t-s-three-paradigms-comparison.md`。
- 七維分層：直接看 `docs/specs/capital-flow-seven-dimension-spec.md` §6/§7/§9/§14。

## 12. 對用戶的提醒

- 你說重啟 hermes agent。
- 重啟後，新 session 會看不到這次 session 的 context、message 與 tool 狀態。
- atlas-wiki 已落地的內容會保留。
- 重啟前若要我幫忙補某個 wiki page，現在告訴我。
