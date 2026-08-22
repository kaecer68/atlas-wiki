# Skill 競爭 SOP 設計（2026-08-22）

> **目標**:防止 skills 膨脹失控，每個新增 skill 必須先通過「競爭 SOP」才能落地。
> **來源**:kaecer 8/22 拍板「Skill 競爭 SOP」必須實作（Plan F Week 3 Day 4）
> **規範本體**:本檔（_internal 設計文件）
> **注入載體**:§10 加進 atlas-wiki/AGENTS.md v0.9.2 + hermes-agent-skill-authoring SKILL.md

## §1 競爭 SOP 流程（5 步）

### Step 1: 搜尋現有 skills（必跑）
- 用 `~/.hermes/skills/` grep 找相似功能
- 比對 description / 觸發條件 / frontmatter
- 輸出：「找到 N 個候選（同類型）」

### Step 2: 70% 重疊判定
- **有重疊**（≥ 70%）→ 走「擴充既有 skill」路徑（Step 3a）
- **無重疊**（< 70%）→ 走「新增 skill」路徑（Step 3b）
- 70% 計算方式：description 文字重疊 + 觸發場景重疊 + mcp_tools_used 重疊

### Step 3a: 擴充既有 skill（同類型結合）
- 在既有 SKILL.md 的 references/ 子目錄加新條目
- 既有 SKILL.md frontmatter 加 reference 連結
- **不新增** SKILL.md 檔案
- 觸發條件 merge 到既有 skill
- 例如：新的「cron-error-diagnostics」應寫入 `mcp-tool-interpretation/references/`，不開新檔

### Step 3b: 新增 skill（無法結合）
- 寫 1 段提案給 kaecer 拍板
- 提案含：功能描述 + 對位 mission + 為何不結合既有 skill
- kaecer 拍板通過才落地 SKILL.md
- 否則寫入 `_archive/` 標 `rejected`

### Step 4: 拍板 SOP
- kaecer 拍板紀錄寫到 governance-log
- 若拍板通過：建立 SKILL.md（符合 frontmatter + size ≤ 9000B + status/tier）
- 若拍板拒絕：寫到 `_archive/<date>-rejected-skill-name.md` 保留 audit trail

### Step 5: 上線檢查
- 跑 ci-strict（check-skill-index-sync R1+R3+R4）
- 確認 skills-map.md routing 對應
- 確認 AGENTS.md §9.5 索引紀律同步
- 確認本專案 task routing 對應

## §2 同類型結合優先（重要原則）

> **kaecer 8/22 21:15 拍板**:「若有同類型的 skill 可以在裏面增加條文，而不一定同類可以結合的 skill 要多一個文件，無法在 skill 的才在數量管控下競爭。」

實作：
- Step 1 搜尋結果有 ≥ 70% 重疊 → **強制**走 Step 3a（不允許跳過）
- 即使是「方便管理」理由，若有 70% 重疊也必須結合
- 例外：kaecer 明確拍板「分開」（記錄到 governance-log）

## §3 數量管控（混合模式）

> **kaecer 8/22 拍板**: 護欄啟用強度 = **混合模式**（hard_cap + soft_warning 並行）

- **硬上限**: core 10 / active 50 / cold 100 / total_max 160
  - 超過上限的 skill 不顯示在 always-on index
  - 但不自動 archive（需 kaecer 拍板）
- **軟警告**: 警告注入 system prompt，LLM 可建議但不執行
- **90 天沒引用**: 硬上限自動 archive（config.yaml auto_archive=true）

新 skill 通過競爭 SOP 但仍超上限：
- 提示「需先 archive 一個舊 skill 才能新增」
- 列出建議 archive 候選（90 天沒引用）

## §4 SOP 落實清單

### 4.1 寫到 atlas-wiki/AGENTS.md §10
- 加 v0.9.2 版本守則
- §10 改版守則補：每次新增 skill 必跑競爭 SOP

### 4.2 寫到 hermes-agent-skill-authoring SKILL.md
- 在「How to Run」加 Step 0：跑競爭 SOP
- 連結到本設計文件

### 4.3 CI 護欄擴充
- check-skill-index-sync.py 加 R5：新增 SKILL.md 必含 competition_sop_decision frontmatter 欄位（kaecer 拍板日期 + 理由）
- 若缺 R5 欄位 → 違規

### 4.4 skills-map.md 同步
- 新增 skill 必同步加到 skills-map.md routing table
- AGENTS.md §9.5 也同步

## §5 範例

### 範例 A：新增「cron-error-handling」skill（70% 重疊）
- Step 1: grep 找到 `mcp-tool-interpretation`（含 cron error 處理）
- Step 2: 計算重疊度 = 85% ≥ 70%
- Step 3a: 在 `mcp-tool-interpretation/references/cron-error-handling.md` 加條目
- **不新增** SKILL.md

### 範例 B：新增「quantum-portfolio」skill（無重疊）
- Step 1: grep 找到無相關 skill
- Step 2: 計算重疊度 = 0%
- Step 3b: 寫提案給 kaecer 拍板
- kaecer 拍板通過 → 建立 SKILL.md
- 寫到 skills-map.md routing + AGENTS.md §9.5

### 範例 C：超 total_max (160) 上限
- 假設已有 160 個 skill，新提案想新增第 161 個
- Step 3 通過後 Step 5 觸發「需先 archive」
- 列出 90 天沒引用的 5 個 skill 給 LLM 建議
- LLM/kaecer 拍板 archive 其中一個 → 才落地新 skill

## §6 與 Plan F 護欄對齊

| 計畫 | 內容 | 對齊 |
|------|------|------|
| Plan F Week 3 護欄 | 硬上限 + 軟警告 | §3 數量管控 |
| Plan F Week 3 護欄檢查 (R1/R3/R4) | CI 強制 | §4.3 擴充 R5 |
| skill 競爭 SOP（本計畫）| 新增前必跑 | §1-§2 |
| hermes-agent-skill-authoring | 撰寫 SKILL.md | §4.2 連結 |

## 8/22 02:00 完成狀態

- ✅ §1-§6 設計完成
- ⏳ §4.1 AGENTS.md §10 待更新（v0.9.2）
- ⏳ §4.2 hermes-agent-skill-authoring SKILL.md 待寫入（限 hermes-agent repo）
- ⏳ §4.3 check-skill-index-sync.py R5 待實作
- ⏳ §4.4 skills-map.md 同步待驗證
