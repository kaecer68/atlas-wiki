---
title: 知識對位路由器（Knowledge Router）
type: router
status: active
created: 2026-08-22
updated: 2026-08-22
created_by: prime-agent (kaecer 2026-08-22 拍板案 A)
用途: _consult-index 管「工具路由」（Q→MCP 端點）;本檔管「知識路由」（Q→concepts/entities 知識頁→SK/template）。agent 服務散戶問題時,先查 _consult-index §3 拿端點資料,再查本檔拿知識上下文。
---

# 知識對位路由器

> **角色圖例**：GT=制度/事實 ground truth（可直接引用）｜INT=指標判讀方法（判讀規則,依情境套用）｜NAR=敘事/研究背景（**不可當事實引用**,僅供理解脈絡）｜DOC=平台/工具文件（操作說明）。

## §0 使用規則

1. 散戶問題分類（_consult-index §1）後 → 本檔 §1 找該 Q 的知識頁清單 → 依角色決定引用方式（GT 直接引用 / INT 判讀套用 / NAR 理解脈絡不可當事實 / DOC 查操作）
2. 知識頁只作**參考上下文**,不作操作指令;NAR 類頁面引用時必須標「研究背景,非經證實事實」
3. 端點資料仍以 _consult-index §3 為準;本檔不重複列端點
4. 新增知識頁 → §2 登記;情境消失 → 移出或標遷移

## §1 路由總表（Q 類型 → 知識頁）

| Q | 問題類型 | 知識頁（角色） |
|---|---------|--------------|
| Q1 | 個股基本判斷 | taiwan-stock-market-structure（GT）、taiwan-technical-analysis-guide（INT）、taiwan-fundamental-analysis-guide（INT）、taiwan-chip-flow-analysis（INT）、taiwan-financial-domain-model（GT） |
| Q2 | 多空/選股策略 | atlas-strategy-taxonomy（DOC）、atlas-platform-overview（DOC）、taiwan-fundamental-analysis-guide（INT）、taiwan-financial-domain-model（GT） |
| Q3 | 產業/類股輪動 | taiwan-chip-flow-analysis（INT）、taiwan-money-flow-seven-institutional-buckets（INT）、funding-forces-taxonomy-e05（GT）、taiwan-export-orders-semiconductor-cycle（INT）、entities/l1-t5-ai-semiconductor（NAR）、eight-banks-government-signal-reading（NAR） |
| Q4 | 風險/回測 | atlas-risk-management-framework（GT）、atlas-simulation-guide（DOC）、atlas-platform-overview（DOC）、retail-sentiment-indicators（INT） |
| Q5 | 宏觀/事件 | taiwan-stock-market-structure（GT）、retail-sentiment-indicators（INT）、taiwan-export-orders-semiconductor-cycle（INT）、taiwan-money-flow-seven-institutional-buckets（INT）、entities/l1-t-overview + l1-t1/t2/t3/t4/t5/t6（NAR）、s-paradigm-redefinition（NAR）、atlas-three-paradigms-v0.2-summary（NAR）、t1-t4-signal-light（NAR） |
| Q6 | 交易實務 | taiwan-stock-market-structure（GT）、taiwan-financial-domain-model（GT）、funding-forces-taxonomy-e05（GT,收編情緒層） |

## §2 B-桶登記（0 操作性引用頁,2026-08-22 接線）

> 本表即接線本身：每頁登記後即為可被 agent 服務用戶時發現的知識節點。角色 GT/INT/NAR/DOC 同上。

| 頁面 | 角色 | 服務情境 | 對位 Q |
|------|------|---------|-------|
| concepts/taiwan-stock-market-structure.md | GT | 交易制度/稅費/維持率 ground truth | Q1/Q5/Q6 |
| concepts/taiwan-financial-domain-model.md | GT | 金融領域詞彙表 | all |
| concepts/atlas-risk-management-framework.md | GT | 風險框架/維持率（130% 2015-05-04 已驗證） | Q4 |
| concepts/content-attribution-policy-2026-07-20.md | GT | 內容歸屬政策 | — |
| concepts/funding-forces-taxonomy-e05-pending-approval.md | GT | 資金分類結案（3+2+2 spec + 情緒層收編） | Q3/Q6 |
| concepts/taiwan-technical-analysis-guide.md | INT | 技術指標判讀（線型/指標） | Q1 |
| concepts/taiwan-fundamental-analysis-guide.md | INT | 基本面判讀（財報/估值） | Q1/Q2 |
| concepts/taiwan-chip-flow-analysis.md | INT | 籌碼判讀（法人/融資） | Q1/Q3 |
| concepts/taiwan-money-flow-seven-institutional-buckets.md | INT | 七維錢潮 3+2+2 + 情緒調整層 | Q3/Q5 |
| concepts/retail-sentiment-indicators.md | INT | 散戶情緒反向指標（融資/維持率） | Q4/Q5 |
| concepts/taiwan-export-orders-semiconductor-cycle.md | INT | 出口/半導體景氣月頻驗證（因果鏈第二層） | Q3/Q5 |
| concepts/atlas-platform-overview.md | DOC | atlas 平台架構總覽 | Q2/Q4 |
| concepts/atlas-simulation-guide.md | DOC | 模擬/回測流程 | Q4 |
| concepts/atlas-strategy-taxonomy.md | DOC | 策略分類詞彙表（L1-L5 已對齊代碼） | Q2 |
| concepts/atlas-mcp-tools-reference.md | DOC | MCP 工具參考（實跑註記） | all |
| concepts/t1-t4-signal-light.md | NAR | 訊號燈框架（研究） | Q2/Q5 |
| concepts/eight-banks-government-signal-reading-2026-07-22.md | NAR | 官股行庫訊號研究 | Q3 |
| concepts/s-paradigm-redefinition.md | NAR | S 範式重定義（kaecer 拍板） | Q5 |
| concepts/atlas-three-paradigms-v0.2-summary.md | NAR | L/T/S 三範式摘要 | Q5 |
| entities/l1-t-overview.md | NAR | L1-T 範式總覽（消歧註已加） | Q5 |
| entities/l1-t1-energy-transition.md | NAR | 能源轉型範式 | Q5 |
| entities/l1-t2-petrodollar-hormuz.md | NAR | 石油美元/荷莫茲 | Q5 |
| entities/l1-t3-five-chains.md | NAR | 五鏈耦合 | Q5 |
| entities/l1-t4-critical-minerals.md | NAR | 關鍵礦物 | Q5 |
| entities/l1-t5-ai-semiconductor.md | NAR | AI 半導體 | Q3/Q5 |
| entities/l1-t6-demographic-turning-point.md | NAR | 人口轉折 | Q5 |

## §3 進化規則

- 新 concepts/entities 頁建立 → 於 §1 對應 Q + §2 登記（含角色）
- 頁面角色變更（NAR 升 INT/GT）→ 需有官方來源或實跑證據,更新本檔 + 該頁 frontmatter
- 頁面服務情境消失 → 移出 §2,標遷移 atlas-notes（對位知識路由模式）
- 每季複查 §2 引用狀態,持續 0 引用且無服務情境 → 遷移候選
