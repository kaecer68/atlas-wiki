# Atlas Wiki Index

> 散戶 AI 實戰金融工程 知識圖譜
> 從 2026-07-15 開始建立
> Last updated: 2026-08-02 | Knowledge entries: 36 (this index) / Repo .md 總數: 91 / SK 知識頁: 33
> 2026-08-03 repo 公開化(MIT + v1.0.0 + CI validate-wiki)

## Entities
<!-- 從 raw/ 抽取的具體實體:事件、論文、audit 報告 -->

- [[entities/l1-t3-five-chains]] — L1-T.3 五鏈耦合鐵律(2026/4-7 真實事件)
- [[entities/l1-t-overview]] — L1-T 系列範式架構總覽(Day 3 補做,6 條子範式入口)
- [[entities/l1-t1-energy-transition]] — L1-T.1 能源轉型
- [[entities/l1-t2-petrodollar-hormuz]] — L1-T.2 石油美元與霍爾木茲
- [[entities/l1-t4-critical-minerals]] — L1-T.4 礦物資源斷供鏈
- [[entities/l1-t5-ai-semiconductor]] — L1-T.5 AI 與半導體科技奇點
- [[entities/l1-t6-demographic-turning-point]] — L1-T.6 人口轉折

## Concepts
<!-- 從 source 抽取的概念:範式、訊號、策略 -->

- [[concepts/s-paradigm-redefinition]] — S 範式重新定義(不等於盤整期)
- [[concepts/t1-t4-signal-light]] — T1→T4 訊號燈四層驅動結構
- [[concepts/atlas-mcp-interpretation-guide]] — atlas-mcp 工具解讀指南
- [[concepts/taiwan-money-flow-seven-institutional-buckets]] — 台灣法人錢潮追蹤：七類核心機構與散戶可觀測代理
- [[concepts/funding-forces-taxonomy-e05-pending-approval]] — 資金勢力分類學修正版（E05 待業主簽核）
- [[concepts/eight-banks-government-signal-reading-2026-07-22]] — 八大行庫買賣超 — 反推政府護盤訊號的實戰方法
- [[concepts/taiwan-financial-domain-model]] — 台股金融領域模型：十類核心術語與體系（2026-08-02 補入,系統性參考字典）
- [[concepts/taiwan-stock-market-structure]] — 台灣證券市場結構與交易制度（2026-08-02 補入）
- [[concepts/taiwan-technical-analysis-guide]] — 台股技術分析指南（2026-08-02 補入）
- [[concepts/taiwan-fundamental-analysis-guide]] — 台股基本面分析指南（2026-08-02 補入）
- [[concepts/taiwan-chip-flow-analysis]] — 台股籌碼面分析指南（2026-08-02 補入）
- [[concepts/atals-platform-overview]] — atals 平台概覽（2026-08-02 補入）
- [[concepts/atals-simulation-guide]] — atals 策略模擬指南（2026-08-02 補入）
- [[concepts/atals-mcp-tools-reference]] — atals MCP 工具參考（2026-08-02 補入）
- [[concepts/atals-strategy-taxonomy]] — atals L1-L5 策略分類體系（2026-08-02 補入）
- [[concepts/atals-risk-management-framework]] — atals 風險管理框架（2026-08-02 補入）

## Queries
<!-- 問過的好問題 + 答案(不是 trivial lookup,是 substantial) -->

- [[queries/day-2-L1T3-three-dimensions-2026-07-17]] — Day 2 三層 framework 應用(MCP 補驗,medium/contested)
- [[queries/week-1-summary-2026-07-21]] — Week 1 七日研究彙整
- [[queries/money-flow-research-card-2026-07-18]] — 台灣法人錢潮追蹤研究排程卡
- [[queries/e05-data-gap-research-2026-07-18]] — E05 五主體共振的資料斷層研究
- [[queries/H1-H2-H3-replay-2026-07-17]] — H 假說事件回放測試(2026-07-17 TAIEX -6.47%)
- [[queries/H1-H2-H3-extending-or-distributing-2026-07-18]] — H 假說 D+1 EXTEND 驗證(2026-07-18 對照 7/17,5 主體仍土洋對殺)
- [[queries/regime-flip-confirmation-2026-07-19]] — 7/19 regime RISK_OFF→RISK_ON 翻多是否可信(low/contested)
- [[queries/capital-flow-history-knowledge-gap-2026-07-19]] — atlas-mcp capital-flow/history 完全沒歷史(已知問題立案,6 條 CL)
- [[queries/atlas-mcp-capital-flow-history-truth-seeking-2026-07-19]] — 7/20 00:03 夜間研究 cron 跑完的真相盤查(根因:refresh 排程 tradingDate 推導 + UpsertDay + capacity 60 三者組合)
- [[queries/capital-flow-history-unresolved-2026-07-20]] — 7/20 01:48 A01+A02+A03 修復完成後的 5 條未解決 CL 交接(CL-2/3/4/5/6 + 邊界問題 + 推薦執行順序)
- [[atlas-notes/03-system-health/investigations/2026-07-20-open-work-inventory]]（已搬到 atlas-notes，10.7KB；屬盤查類不應留在 wiki）
- [[concepts/atlas-three-paradigms-v0.2-summary]] — L/T/S 三範式摘要(Stage 1C)

## Comparisons
<!-- 跨概念比較:L vs T vs S、S1 vs S2、0050 vs 00878 等 -->

- [[comparisons/l-t-s-three-paradigms-comparison]] — L/T/S 三範式對照表(Stage 1C 第二個小步,2026-07-17)

---

## 入口設計 / 找東西的方式

- **找某個事件**:到 `entities/` 用檔名搜尋
- **找某個概念**:到 `concepts/` 用檔名搜尋
- **找某個比較**:到 `comparisons/`
- **找某個研究問題**:到 `queries/`
- **看全貌**:用 Obsidian 打開這個目錄,看 Graph View

## 維護節奏(kaecer 拍板)

- 每天 1-3 個事件研究,**最多 3 個**
- 每個不超過 2 小時琢磨 + 30 分鐘寫 wiki page
- 每日結束前寫 log.md + 紀律反思
- 每週日跑一次 Lint(orphan / broken links / stale / contradictions)

## 排程(kaecer 拍板)

- **Day 1**(2026-07-15):Stage 1A + 4 wiki page ✅
- **Day 2**(2026-07-16 0:00):**排程失敗**,7/17 補做 ✅
- **Day 3**(2026-07-17 0:00):**排程失敗**,7/17 補做 ✅
- **Day 4-7**:L1-T.1/2/4/5/6 entity + MCP 補驗 + Week 1 summary ✅
- **Day 8+**:Stage 1C 三範式 summary + comparison
  - Stage 1C 第一步(2026-07-17 早):[[concepts/atlas-three-paradigms-v0.2-summary]] ✅
  - Stage 1C 第二步(2026-07-17 凌晨排程):[[comparisons/l-t-s-three-paradigms-comparison]] ✅
