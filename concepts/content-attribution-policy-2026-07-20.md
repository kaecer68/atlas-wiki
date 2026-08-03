---
title: 內容歸屬守則 — wiki vs notes 邊界（2026-07-20）
created: 2026-07-20
updated: 2026-07-20
type: concept
tags: [framework, governance, content-attribution, signal, time-anchor]
sources:
  - atlas-wiki/SCHEMA.md
  - atlas-notes/00-INDEX.md
  - atlas/docs/documentation-standard.md
  - atlas/docs/documentation-map.md
confidence: medium
contested: false
contradictions:
  - "mistakes/log-of-placing-investigations-into-atlas-wiki 2026-07-20 之前從沒分離過"
---

# 內容歸屬守則 — wiki vs notes 邊界

> **這頁存在的理由**：kaecer 2026-07-20 白班明示，hermes agent 把「盤查報告 / 待修復問題 / 真相挖掘」放在 `atlas-wiki/queries/` 會造成**知識污染**（未定型的事實被當成已成型的知識處理），同時允許接手修 atlas 的 agent 也寫到 `atlas-wiki/` 等於**越界代回填負責人專區**。
>
> 這頁**對位** atlas 的 `docs/documentation-standard.md`（atlas 規範「**不同內容類型歸屬不同位置**」），把它整理成 hermes + kaecer 雙專案可遵循的內容邊界。

---

## 1. 三層歸屬（總原則）

| 層 | 路徑 | 寫入資格 | 內容特徵 | 升級條件 |
|----|------|---------|---------|---------|
| **A. `~/workspace/atlas-notes/`** | raw 源文件、盤查、決策紀錄 | kaecer + hermes agent **主責**；接手 agent 在「白名單子目錄」白名單授權 | **未定型**事實、**進行中**根因追蹤、**單一時間錨**事件報告 | 升 B 條件：cross-page wikilink ≥ 2 條 + confidence ≥ medium |
| **B. `~/workspace/atlas-wiki/`** | LLM wiki 整理後知識圖譜 | kaecer + hermes agent **主責**；**接手 agent 一律不准**（這條是最常被違反的） | **已成型的跨頁知識**、**穩定的概念定義**、**LLM wiki 索引體系本身** | 升 C 條件：6 個月內被多 source 引用過 |
| **C. `~/workspace/atlas/`** | 規範、reference、playbook、stable spec | **接手 agent 可在 atlas 內改 backend**，但不能在 `atlas-notes/` 與 `atlas-wiki/` 寫任何東西 | **規範與憲法、跨模組 reference** | 不用升，這層已是 canonical |

> **atlas 的 `docs/investigations/` 機制**（`docs/investigations/YYYY-MM-DD-symptom.md`）對應到 A 層的 `atlas-notes/03-system-health/investigations/`——**atlas 已經規範「根因調查不是 knowledge」**，hermes 端之前違反了。

---

## 2. 各工作類型的歸屬規則

### 2.1 「**盤查**」與「**真相挖掘**」（您點名的第一類）

- ❌ **錯**：寫到 `atlas-wiki/queries/` 或 `atlas-wiki/concepts/`
- ✅ **對**：
  - 根因調查 → `atlas-notes/03-system-health/investigations/YYYY-MM-DD-{slug}.md`
  - 待辦但還沒動 → `atlas-notes/06-backlog/{slug}.md`
  - 系統稽核對比 → `atlas-notes/03-system-health/known-issues.md`（同一檔累積）

### 2.2 「**知識概念**」與「**跨頁對位**」

- ❌ **錯**：把單一事件的盤查報告包裝成 concept
- ✅ **對**：`atlas-wiki/concepts/` 收的是**跨頁引用的概念**（例如「七維錢潮分層」、「T1→T4 訊號燈」），不是單一事件的報告
- **升 wiki 的觸發點**：當你發現同一概念被 3 條以上 wikilink 引用、且 confidence ≥ medium、`contested: false` → 才考慮升 wiki

### 2.3 「**事實陳述**」vs「**判斷 / 觀點**」

- 事實陳述（repro 指令、API 觀察、git 狀態）→ A 層
- 判斷 / 觀點（建議方案、風險評估、誰來動）→ A 層（仍在盤查階段）
- 成型的「**最佳實踐 / 規範**」才升 B 層

### 2.4 「**接手 agent 的產出**」

- ❌ **錯**：讓接手 agent（OpenCode CLI / Atlas Maintenance）寫 `atlas-wiki/`
- ✅ **對**：
  - 寫入位置由「**事實類型**」決定，不是由「**誰寫**」決定
  - 接手 agent 若有「**盤查結論**」要記錄 → 寫 `atlas-notes/03-system-health/investigations/`
  - 接手 agent 若有「**待辦事項**」 → 寫 `atlas-notes/06-backlog/`
  - 接手 agent **不寫**任何 wiki 內容 — 由 kaecer / hermes 整理後才升

---

## 3. 邊界判定決策樹（總監寫作前的 4 個問題）

寫任何檔案之前先問這 4 題，順序不能亂：

```
1. 這份內容是事實記錄還是成型概念？
   - 事實記錄 → 進 Q2
   - 成型概念 → 進 Q3

2. 這事實記錄是「單一時間單一事件」 還是「跨頁結論已成型」 ？
   - 單一事件 → A 層（notes 對位路徑）
   - 跨頁結論 → Q3

3. 這個概念被「跨頁 wikilink ≥ 2 條」引用嗎？
   - 是、且 confidence ≥ medium → B 層（wiki/concepts 或 wiki/entities）
   - 否、單一頁引用 → A 層

4. 這個 wiki page 的 inbound wikilink ≥ 1 條嗎？
   - 是 → 保留 B 層
   - 否（orphan）→ 退回 A 層（它屬於盤查或待辦，不該在 wiki）
```

> 違反這決策樹的典型症狀就是 2026-07-20 白班發現的 — `wiki-open-work-inventory` 是盤查不該在 wiki、`atlas-vs-hermes-governance-gap` 是治理對位盤查不該在 wiki。

---

## 4. 對接手 agent 的權限邊界（與 `atlas-maintainer-prompt-template` 對位）

| 路徑 | 接手 agent 可寫？ | 為什麼 |
|------|----------------|------|
| `~/workspace/atlas/` 內（handler / spec / test） | ✅ 是 | 接手 agent 的核心工作 |
| `~/workspace/atlas-notes/03-system-health/investigations/` | ✅ 是 | 接手 agent 的盤查交付位置 |
| `~/workspace/atlas-notes/06-backlog/` | ✅ 是 | 接手 agent 的待辦交付位置 |
| `~/workspace/atlas-notes/05-decisions/` | ⚠️ 需 spec | 重大決策要 hermes / kaecer 拍板才落 |
| `~/workspace/atlas-notes/02-knowledge/` | ❌ 否 | 純 atlas 知識 + reference，沒 audit 權 |
| `~/workspace/atlas-notes/04-daily/` | ❌ 否 | kaecer / hermes 的日記專區 |
| `~/workspace/atlas-notes/01-frameworks/` | ❌ 否 | 框架層，hermes 主責 |
| `~/workspace/atlas-wiki/`（任何子目錄） | ❌ 否 | **負責人專區，不許越界代回填** |

---

## 5. 自驗清單

每次寫之前、跑這清單：

- [ ] Q1：事實/概念分類完了嗎？
- [ ] Q2：這頁有「**cross-page wikilink ≥ 2 + confidence ≥ medium**」嗎？
- [ ] Q3：承接頁、log.md 都有更新嗎？
- [ ] Q4：接手 agent 的產出歸位對了嗎？（未成型 → notes 白名單；成型 → wiki，**但由 kaecer / hermes 寫，不是接手 agent**）
- [ ] Q5：探測是否會污染既有跨頁知識？若是 → 退回 A 層或拆成子頁

未通過任何一題 = 不能寫入，找 kaecer 拍板。

---

## 6. 自驗（這頁自己的 KYC）

- ✅ 對位 atlas documentation-standard 3 層歸屬原則
- ✅ 把接手 agent 的權限寫成**反向禁止清單**（DO/DON'T 比對）
- ✅ 包含決策樹與寫前清單
- ✅ 給升 wiki / 退回 notes 的具體條件
- ✅ 與 `atlas-maintainer-prompt-template` 對位
- ✅ 對位 kaecer-director-role + kaecer-managing-up 兩 skill
- ✅ confidence medium，contested：false（一次對齊）

— 落款：2026-07-20 02:55 CST，content-attribution-policy v1.0，kaecer + hermes agent 白班指示所建；對應 wiki 結構 8 條歸屬守則。