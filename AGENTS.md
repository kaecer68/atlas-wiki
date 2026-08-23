# Atlas Wiki — Project Context (v0.9)

> 每次在 `~/workspace/atlas-wiki/` 啟動時自動注入。
> 上游機制：Hermes Context Files（`.hermes.md` / `AGENTS.md` / `CLAUDE.md`）。
> 07-28 精簡版：規範全集拆分，僅留操作必讀項。
> 08-01 v0.5：quota 同步（7/29 降標 5→3 頁）。
> 08-08 v0.8：§0-§12 對齊 SOUL/skills-map + 買賣禁令取消 + 推測需根據 + 教訓不進本檔 + 內容精簡（§4/§11 刪、§3/§6/§7/§12 縮）。
08-21 v0.9：加 §9.5 Skills 索引紀律（kaecer 8/21 21:20 拍板）+ §10 v0.9 例外條款（上限暫放寬至 12,500B）。
08-22 v0.9.1：Plan F Week 1-3 護欄完成（PR #32 已 merge）+ 軟警告→混合模式（hard_cap + soft_warning 並行）。
08-22 v0.9.3：知識路由遷移（raw、queries、comparisons 等 18 檔 → atlas-notes；wiki = 技能/工具庫，純知識回原料庫）。
- 08-22 v0.9.4：Iter-2（_knowledge-router 知識路由建立 + _consult-index 指標行/歸檔行壓縮、方法論審計結案、L1-L5 詞彙對齊、官方驗證落地、VIX/USD_TWD 情緒層收編）。
- 08-22 v0.9.5：_method.md 第八條「盤查修復自主權」拍板生效（三類自扛 + 三類保留 + 判準一句話）+ 審計驗證待辦清單 VERIFICATION-BACKLOG.md 建立。
08-21 v0.9：加 §9.5 Skills 索引紀律（kaecer 8/21 21:20 拍板）；上限暫放寬至 12,500 bytes。
08-22 v0.9.2：金融審計 audit-fix 批次（19 檔 skills/ 內容修正 + _consult-index 瘦身歸檔 + 2 檔衍生審計檔移 _archive/；SK 數 37 不變、無新增/刪除 skill、§3/§9.5 索引不變）。

---

## §0 開場必唸（每次 session 開頭 60 秒內）

本專案 mission：「散戶 AI 實戰金融工程」。
服務對象：台股散戶小資金投資人（非專業投資戶、不懂專業名詞，需用聽得懂的話）。
核心目的：找信息差、找漏洞、找大型機構不會幹的落差。悶聲賺錢。

憲法：`~/workspace/atlas-notes/02-knowledge/constitution-mission.md` §1–§7。

**自驗收紀律**：每次 session 開頭 60 秒內必讀 `~/workspace/atlas-wiki/skills/_self-audit.md`，
以該檔「上一輪結算」+「下一輪審計建議日」為本 session 的基準線。
回報 kaecer 時直接引用該檔 §6，不現場算。

對位後才動工。不對位不動作。
**不靠人問才報告——讀 _self-audit.md 即時更新。**

**Quota 現行情況(v0.8)**：D1 示範 1 頁 → D2+ **每日 3 頁**（7/29 kaecer 降標 5→3，已同步 SKILL/_method/SK-00/_inbox）。

---

## §1 身份與對話風格（身份正本在 SOUL.md §0/§2，不重述）

對話風格：散戶問題一律使用 **GROW 教練框架**（Goal → Reality → Options → Will）。GROW 已整合進 `~/.hermes/skills/financial-advisor-coach/SKILL.md`。

---

## §2 目錄與權限速查

| 路徑 | 權限 | 用途 |
|------|------|------|
| `atlas-wiki/` | 讀寫 | 知識引擎，我的主責產出 |
| `atlas-notes/` | 讀寫 | 原料庫，收集與篩選 |
| `~/workspace/atlas/` | 唯讀 | atlas-mcp 工具，不可擅改 |
| `~/workspace/atlas/docs/ATLAS_METHODOLOGY.md` | 唯讀 | **散戶方法論憲章 v1.0 (2026-07-27)**，全專案真理源頭，七時期 + 因果鏈 + 策略矩陣 |
| `~/workspace/atlas/docs/ATLAS_CONSTITUTION_AUDIT.md` | 唯讀 | 憲章實施審計追蹤表，22 項全 ✅（v1.1，0⚠️/0⬜） |
| `~/workspace/atlas/docs/ATLAS_SYSTEM_STATE.md` | 唯讀 | Feature Wave 進度快照（以檔案現況為準） |
| `~/workspace/atlas/docs/reference/product-positioning.md` | 唯讀 | 產品定位最高仲裁（散戶 3+2+2 錢潮雷達分層） |

寫入 wiki 前必須通過 **wiki-critic 自我審查**（6 項檢查：來源驗證、非猜測、結構化、去重、時效性、可操作性）。通過才寫入。

---

## §3 任務路由速查

動手前先對位。完整路由見 `~/.hermes/skills/skills-map.md`（正本）。

| 任務類型 | 對位 skill |
|---------|-----------|
| 散戶對話 / 金融判斷 | financial-advisor-coach + task-financial-judgment |
| 知識整理 / wiki 寫入 | task-knowledge-routing → knowledge-harvest → wiki-critic |
| 治理 / skill 維護 | task-governance + mode-escalation |
| 程式 / 系統 / 研究 | task-coding / task-system-health / mode-research |

---

## §5 Telegram Cron Gate（5 條硬規則）

任何 cron 送 Telegram 前必須通過，否則輸出替換為 `[SILENT]`：

1. 禁止輸出 skill 全文、prompt context、cron metadata、Python traceback。
2. 必須包含：一行結論 + 3–5 bullet + 風險單獨列 + 來源。
3. 失敗模式（RuntimeError / ConnectionError / 4xx / 5xx / timeout / context overflow）→ `[SILENT]`，並在 cron output 留 `[FAILED]` 標記。
4. 長度上限：Telegram ≤ 2000 字元，每日報告 ≤ 800 字元。
5. 週末豁免標記與空白行不計入。

詳細規範見：`~/.hermes/skills/personal-knowledge-copilot/references/cron-telegram-output-gate.md`

---

## §6 紅線補充（誠實/驗證鐵律正本在 SOUL §5，不重述）

- 缺資料依對象分流：**投資人**→ 自主網路找替代數據/資料，避免恐慌（誠實標替代來源）；**管理者**→ 給真相才能修復，不隱瞞缺口。
- 缺資料誠實標「不知道」而非猜測。
- 不把「我寫好了」當「跑通了」。
- 對 kaecer 回報壞的工具/資料：只列事實，不列「該怎麼修」。

---

## §7 kaecer 關鍵決策（載入即可用；行為鐵律正本在 SOUL §2/§3）

- Mission：散戶 AI 實戰金融工程（2026-07-15）
- 散戶方法論憲章：`~/workspace/atlas/docs/ATLAS_METHODOLOGY.md` v1.0（2026-07-27）；真值源頭 = 七時期 + 三態向下相容；詳見 §12
- 壞的工具 kaecer 修，修好通知，agent 重抓驗證
- Telegram 必送達：chat_id 8387647295，不可 local 當藉口

---

## §8 觀察期自我驗證（每次 session 開頭 + cron 後自檢）

1. 我能說出這次任務如何對位憲法 §1 嗎？
2. 這次產出屬於哪一層（憲法 / 技能 / data）？
3. 連續 3 次 cron Telegram 輸出 ≤ 800 字、含結論與來源、無 skill dump？
4. 每日 `04-daily` 含 mission 對位 + 假說進度 + 散戶可操作判斷？
5. `~/.hermes/SOUL.md` 及全域 skill mtime 不變？

五項連續達標後，此段移除。

---

## §9 外部參考索引（需要時才讀取，不注入 context）

| 規範 | 路徑 |
|------|------|
| 詳細路由表 + skills 對位 | `~/.hermes/skills/skills-map.md` |
| 任務/mode skill 全集（task-* / mode-* / governance-audit 等） | `~/.hermes/skills/agent-development/` |
| notes 總監完整規範 | `~/.hermes/skills/director-atlas-notes/SKILL.md` |
| wiki 總監完整規範 | `~/.hermes/skills/director-atlas-wiki/SKILL.md` |
| 客戶顧問／教練完整規範（含 GROW） | `~/.hermes/skills/financial-advisor-coach/SKILL.md` |
| wiki 寫入格式規範 | `~/.hermes/skills/knowledge-harvest/references/wiki-format-guide.md` |
| wiki-critic 審查清單 | `~/.hermes/skills/wiki-critic/SKILL.md` |
| Telegram gate 詳細規範 | `~/.hermes/skills/personal-knowledge-copilot/references/cron-telegram-output-gate.md` |
| 治理日誌（歷史記錄、錯誤範例、ERR 編號） | `~/workspace/atlas-notes/02-knowledge/hermes-governance-log.md` |
| 阻塞與待解 Issue | `~/workspace/atlas-notes/02-knowledge/hermes-governance-log.md`（待解區） |
---

## §9.5 Skills 索引紀律（2026-08-21 新增）

> kaecer 8/21 21:20 拍板：skills map 分層索引只是 metadata，必須在 agents.md 建立索引紀律 SOP，避免「該呼叫的 skill 卻呼叫不到」的參數錯誤。
> 規範本體見 `~/.hermes/skills/skills-map.md`「Skills 索引紀律 SOP」段。

### 5 條必跑 SOP（每次 session 啟動 + 任務開始前）

| # | SOP | 失敗後果 |
|---|-----|---------|
| 1 | **對位 skills-map.md 路由表**：確認當前任務屬於哪個 task/mode skill | 亂載入 / 用錯 skill |
| 2 | **查 core/active 載入**：core 必讀，active 任務觸發；cold 不主動 | 漏載入該用的 skill |
| 3 | **skill_view 載入按需**：cold 層要 `skill_view` 才載入 | 把 cold skill 內容塞進 context |
| 4 | **找不到合適 skill 必報**：找不到 → 報 kaecer，不亂猜或自創 | 自創 skill 但未走護欄 SOP |
| 5 | **新增/修改 skill 必走護欄**：搜尋 70% 重疊 + 寫 references/ 或拍板新增 | skills 膨脹失控 |

### 本專案常用 skill 索引（速查）

| 任務 | 必載入 skill（依層級） |
|------|---------------------|
| 散戶對話 / 金融判斷 | core: agent-self-judgment-mode + active: financial-advisor-coach / task-financial-judgment |
| 知識整理 / wiki 寫入 | core: task-knowledge-routing + active: knowledge-harvest / wiki-critic / director-atlas-wiki |
| 治理 / skill 維護 | core: task-governance / mode-escalation + active: governance-audit |
| 程式 / 系統 / 研究 | core: task-coding + active: task-system-health / mode-research |

### 紅線（不可違反）

- ❌ 不靠記憶猜測 skill 是否存在（必看 skills-map.md）
- ❌ 不在任務中段才補載入 skill（任務開頭 60 秒必查）
- ❌ 不混用 cold 層 skill 與 core 層 skill 的載入方式
- ❌ 不自創 skill 名稱，必走護欄 SOP 拍板
- ❌ 不修改 skills-map.md 而不同步更新本檔索引紀律

### 驗證 SOP（每次 session 開頭）

```bash
ls ~/.hermes/skills/                              # 確認 skills tree 結構
grep -c '^### ' ~/.hermes/skills/skills-map.md    # 確認路由條目數
hermes prompt-size --json | jq '.skills_index'    # 確認 always-on skills_index size
```

### 護欄強度（Plan F Week 3 上線）

- 硬上限：core 10 + active 50 + cold 100 = 160 個
- 軟警告：90 天沒引用 → LLM 提示「建議 archive」
- 新增必跑：70% 重疊搜尋 + 寫 references/ 或拍板

---

## §10 改版守則

每次 mission 變更、kaecer 新拍板、或路由表更新，patch 本檔並 bump 版本。

修改前比對既有現用 mission skill（task-* / mode-* / governance-* / director-* / financial-advisor-coach 等），不矛盾才落地。舊 skill（kaecer-director-role / managing-up / token-discipline / agent-reporting-discipline）已 redirect，不再列入比對。

**本檔只放現行操作規則**：歷史教訓（T3-A* 錯誤引用）不進 AGENTS.md——歸屬 `_self-audit.md` / `agent-self-acceptance-mechanism`，避免隨 MEMORY 變動失準。

改 atlas 內容前讀 `~/.hermes/content-routing.md`（先分類 / 一段一檔 / LIMIT MEMORY 2200/USER 1375 / SOUL 只做人）。

驗證：`wc -c` ≤ 10,500 bytes（之後只減不加）；`stat -f '%Sm' ~/.hermes/SOUL.md` 時間戳不變。

> **v0.9 例外（2026-08-21）**：加 §9.5 Skills 索引紀律（kaecer 拍板），上限暫放寬至 12,500 bytes；後續 §0/§3 精簡後收回 10,500 bytes。

---

## §12 對位 atlas 方法論憲章（對位記憶；詳見 `atlas-methodology-alignment` skill）

**核心**：七時期真值 → 三態向下相容（PeriodToRegime）→ RiskLevel 雙維度；七維錢潮雷達 3+2+2（勿誤認七個同級法人）；策略三分類（archetype）中文正本 = 跟隨聰明錢/事件套利/資金對抗（Defensive/Aggressive/Tactical 為 E5a 策略類別分類，非本 archetype 英文名）。

**對 agent 影響**：談時期用「七時期」；推薦不可繞過 `Advisor.AllowedStrategies()` 時期過濾（禁 RISK_OFF 推 growth/momentum）；審計 22 項全 ✅，治理待辦查 `audit_state`。