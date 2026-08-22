# Atlas Wiki Index

> 散戶 AI 實戰金融工程 知識圖譜
> 從 2026-07-15 開始建立
> Last updated: 2026-08-22 | Knowledge entries: 36 (this index) / Repo .md 總數: 154（2026-08-22 快照,find 實測） / SK 知識檔: 37（36 編號 + 索引,SK-27/30 已 archive）
> 2026-08-03 repo 公開化(MIT + v1.0.0 + CI validate-wiki)
> 2026-08-22 知識路由：raw/queries/comparisons/summaries-handoff+manifests 共 18 檔遷移至 atlas-notes（純知識回原料庫）

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
- [[concepts/atals-strategy-taxonomy]] — atals L1-L5 策略分類體系（2026-08-02 補入；層名對齊 atlas internal/strategy_techniques/enums.go canonical [2026-08-22 iter2]）
- [[concepts/atals-risk-management-framework]] — atals 風險管理框架（2026-08-02 補入）

- [[concepts/atlas-three-paradigms-v0.2-summary]] — L/T/S 三範式摘要(Stage 1C)
- [[atlas-notes/03-system-health/investigations/2026-07-20-open-work-inventory]]（已搬到 atlas-notes，10.7KB；屬盤查類不應留在 wiki）

> 2026-08-22 知識路由：queries/ 8 檔 + comparisons/ 1 檔已遷移至 atlas-notes/02-knowledge/，此兩區從 wiki 移除（純知識回原料庫）。歷史條目見 git log 與 log.md。

## Skills
<!-- SK 知識頁索引:SK-00 索引 + SK-01~SK-36(37 檔,SK-27/30 已 archive;2026-08-22 audit-fix 快照) -->

- [[skills/SK-00-skill-index]] — SK 索引頁
- **8/7-8/21 新增**:
  - [[skills/SK-33-audience-routing]] — audience-routing（受眾路由）
  - [[skills/SK-34-listed-otc-routing]] — listed-otc-routing（上市/上櫃分流,8/15 真實 promotion,PR #21）
  - [[skills/SK-35-mcp-failover]] — mcp-failover（MCP 故障切換）
  - [[skills/SK-36-sl-vs-rl]] — sl-vs-rl（原 SK-31 renumber,PR #31）
  - [[skills/SK-31-ai-investment-cycle-2026]] — AI 投資週期 2026（SK-31 唯一對應）

---

## 入口設計 / 找東西的方式

- **找某個事件**:到 `entities/` 用檔名搜尋
- **找某個概念**:到 `concepts/` 用檔名搜尋
- **看全貌**:用 Obsidian 打開這個目錄,看 Graph View
- **研究盤查 / 比較 / 過程工件**:到 `~/workspace/atlas-notes/02-knowledge/`（原料庫，2026-08-22 知識路由遷移）

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
  - Stage 1C 第二步(2026-07-17 凌晨排程):comparisons/l-t-s-three-paradigms-comparison（已遷移至 atlas-notes/02-knowledge/, 2026-08-22 知識路由）✅
