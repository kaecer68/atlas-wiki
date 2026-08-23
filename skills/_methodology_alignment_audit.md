---
title: atlas-wiki 對位 ATLAS 方法論憲章 — 違背清單與處理草案（2026-07-30）
type: methodology-alignment-audit
purpose: 經 atlas-mcp 實跑 + 憲章本體讀取，找出 atlas-wiki 與 v1.0 憲章的違背點並列草案，等 kaecer 拍板後落地
created: 2026-07-30
created_by: hermes-agent
ground_truth_basis:
  - ~/workspace/atlas/docs/ATLAS_METHODOLOGY.md v1.0 (2026-07-27)
  - ~/workspace/atlas/docs/ATLAS_CONSTITUTION_AUDIT.md v1.0 (22 項差距,19✅/1⚠️/2⬜)
  - ~/workspace/atlas/docs/ATLAS_SYSTEM_STATE.md (21 Wave 全 ✅)
  - ~/workspace/atlas/docs/reference/product-positioning.md v1.0
  - atlas-mcp mcp_quickstart (2026-07-30 實跑回傳,7/28 consolidation/RISK_ON,7/29 bull/RISK_ON)
status: draft (待 kaecer 拍板 → 落地為各頁 transformation)
related:
  - ~/workspace/atlas-wiki/skills/_method.md
  - ~/workspace/atlas-wiki/skills/_consult-index.md
  - ~/workspace/atlas-wiki/skills/_inbox.md
  - ~/workspace/atlas-wiki/skills/_index-finskills.md
updated: 2026-08-22
---

# atlas-wiki 對位憲章 — 違背清單與處理草案

> **目的**：對位 ATLAS 方法論憲章 v1.0，把違背的知識過濾（刪/標 transit）或轉化（加 cite/補段）。
> **決策**：本檔是草案，等 kaecer 拍板動哪些、做哪些；動工前不做任何 wiki 改動。

---

## §0 對位方式

**對位口徑 5 條**（mode-no-guess §大判斷鏈條）：

1. **七時期優先**：對散戶談時期用「七時期」；RISK_ON/OFF/NEUTRAL 三態是向下相容層
2. **七維錢潮雷達 3+2+2 = 三層分開**：官方法人 / 行為代理 / 領先跨市場；不同分母不可加權平均（CF-INV-07）
3. **策略三分類**：Defensive / Aggressive / Tactical（事件套利），非憲章前 4 策略分類
4. **MCP 端點真值**：atlas-mcp 跑的數字 = 真值；wiki 寫的是「對位的參考」；不平起平坐
5. **E3 partial 標記**：時期判斷 MCP 端點（M1）尚未公開 → 引用此功能時標 `[PENDING — M1 endpoint unavailable]`

---

## §1 違背清單（12 條 + 4 條策略性違背;原始全文 → _archive 附錄 A）

- **1.1 _method.md（HIGH,✅ A1）**：鐵律未提憲章對位 → 已加第四條「不違背憲章」+ 第五條「快照值必附 timestamp」
- **1.2 SK-18（MED,✅ B1）**：alpha 未串七時期 → 已加「期間適用性（七時期 × 三分類）」段
- **1.3 SK-20（MED,✅ B2）**：市值分組未對位產業/3+2+2 → 已加「產業 × 市值」雙軸 + CF-INV-07 加權警示
- **1.4 SK-16（MED,✅ B3）**：CIRCUIT_BREAKER 舊語意 + 未提時期過濾 → 已加「七時期 × 信號可用性」表
- **1.5 SK-29（MED,✅ B4）**：max_drawdown 未標期間依賴 → 已加警告
- **1.6 SK-01（LOW）**：B5-3 產業映射未更新 → 待補一句（下一輪）
- **1.7 _consult-index §3（MED,✅ A4/TW-X3）**：E3 partial + M1 pending 未標 → 已標
- **1.8 _index-finskills（LOW）**：預評表未引 §五 → 待補（下一輪）
- **1.9 _inbox（LOW）**：缺 cross-ref → 待補（下一輪）
- **1.10 策略性違背 4 條**：
  - **TW-X1（HIGH,✅）**：七時期術語一致性 → A2/A3 tip 已落地 5 頁 SK
  - **TW-X2（MED,✅ 2026-08-22 iter2）**：資金面「七大資金勢力」舊語意 → SK-16/18/20 已加「3+2+2 分層,不可加權平均」術語備註
  - **TW-X3（MED,✅）**：MCP prompts 舊三態詞 → _consult-index §3 已標 E3 partial
  - **TW-X4（MED,✅ 撤銷）**：strategy_ranker 4 分類 vs 憲章三分類 → 2026-07-30 kaecer 裁定正交,附註已加

---

## §2 處理動作（A/B 全數落地 2026-07-30~08-02;原始表 → _archive）

- **階段 A（✅ 2026-07-30）**：A1 _method 第四條鐵律 / A2 5 頁 SK frontmatter 對位標 / A3 一句話定位術語備註 / A4 _consult-index E3+M1 標記
- **階段 B（✅ 2026-08-02 24/24）**：B1 SK-18 期間適用性 / B2 SK-20 雙軸 / B3 SK-16 對位承諾 / B4 SK-29 警告 / B5 SK-16/18 TW-X4 附註（後裁定撤銷）/ B6 _index-finskills §五
- **階段 C（2026-08-22 iter2 複查）**：
  - C1「period × strategy 對位需 M1 MCP 公開」→ **解除**：M1 ✅（macro_get_snapshot_latest.current_period）+ M4 ✅（strategy_for_period）
  - C2「strategy_ranker 加 period 欄同步補 _consult-index §3」→ **部分**：ranker 仍無 period 欄（2026-08-22 源碼複查）;改用 strategy_for_period,補註已落地 concepts/atlas-mcp-tools-reference.md §2.7（_consult-index §3 無空間 8995B,指標行已存在）
  - C3 cron 9a9aa3 prompt 七時期重設計 → 待 kaecer 排（已送歷史不能改）

---

## §3 風險與限制

- **未驗證風險**：本檔違背點是「讀憲章 + 讀 wiki」靜態對照；未跑 ground truth（沒辦法跑 wiki 內容本身的對錯測試）
- **依賴 MCP 升級**：TW-X3/TW-X4 等需要 `strategy_ranker`/`prompts` 後端改才能根除；不是 wiki 動得了
- **cross_file 同步債**：本檔改了 5 個 SK 是「拉動」，需要 5 個獨立 frontmatter patch — patch 工具已知有「換行吃字」bug，需小心逐個做
- **kaecer 拍板未到**：本檔全段是草案，未經 kaecer 同意就落地 = F-02 同類違規
- **跨任務衝突**：本任務做完後，Fin-Skill 轉化對位必須用本檔為基準 — 不能跳過拍板直接動 Fin-Skill

---

## §4 附錄：違背點與處理建議等級一覽

| # | 違背檔案 | 等級 | 動作階段 |
|---|---------|------|---------|
| 1 | _method.md 三條鐵律 | HIGH | A1 |
| 2 | TW-X1 七時期術語一致性 | HIGH | A2+A3 |
| 3 | SK-18 alpha 期間適用性 | MED | B1 |
| 4 | SK-20 產業映射對位 | MED | B2 |
| 5 | SK-16 Advisor 對位 | MED | B3 |
| 6 | SK-29 期間依賴 | MED | B4 |
| 7 | SK-16/18 strategy_ranker 附註 | MED | B5 |
| 8 | _consult-index §3 E3 partial | MED | A4 |
| 9 | _index-finskills 對位 §五 | LOW | B6 |
| 10 | _inbox.md cross-ref | LOW | (下一輪) |
| 11 | SK-01 B5-3 補充 | LOW | (下一輪) |
| 12 | TW-X3 prompts 引用 | MED | (與 A4 合) |

---

## §5 執行狀態總結（2026-08-22 iter2 結案）

- **A 階段（2026-07-30）✅**：A1-A4 全落地（含 TW-X1/X3/X4 附註）
- **B 階段（2026-08-02）✅**：24/24 active 頁 methodology_aligned（§5.2 對位表全文 → _archive）
- **TW-X1 ✅ / TW-X3 ✅ / TW-X4 ✅**（A/B 階段含;TW-X4 為 kaecer 裁定正交撤銷）
- **TW-X2 ✅（2026-08-22 iter2）**：SK-16/18/20 加「資金面 = 七維錢潮雷達 3+2+2 分層,不可加權平均」術語備註
- **C 階段複查（2026-08-22）**：M1 ✅ + M4 ✅ → C1 解除;C2 部分（補註 → atlas-mcp-tools-reference §2.7）;C3 待排
- **執行記錄全文（§5.1-§5.5 + §1 原始違背清單）→ [[_archive/_methodology_alignment_audit_20260802_execution.md]]**

> **最後更新**: 2026-08-22 (iter2 結案 — TW-X2 落地 + C 階段複查 + §5 歸檔)
> **採納決策權**: kaecer（第五條鐵律已拍,B 階段執行已核准;2026-08-22 指令「繼續派工解決 Iter 2 待辦」授權本結案批次）

