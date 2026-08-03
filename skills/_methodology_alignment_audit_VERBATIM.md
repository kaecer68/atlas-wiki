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

## §1 違背清單（draft 草案,12 條 + 4 條策略性違背）

### 1.1 _method.md — 高價違背（HIGH）

**事實**：
- _method.md 是「下蛋的雞」—所有 SK 寫入規範本體
- 規範速查表「Quota:D1 示範 1 頁 → D2+ 每日 3 頁上限」沒提「對位 ATLAS 方法論憲章」
- 三條鐵律（不搬運/不瞎寫/不裝完成）已存在但沒強調「以憲章 v1.0 為對位真理源頭」

**處理（建議）**：在 §3 三條鐵律加第四條「對位 ATLAS_METHODOLOGY.md v1.0 為真理源頭」；規範速查表「精選門檻」三題之外加「對位憲章 §五散戶策略矩陣?」
**反例/風險**：加第四條會讓 iron rule 清單變長；可能與現有 Quota 規則搶位
**等級**：HIGH（影響所有後續 SK 寫入）

---

### 1.2 SK-18 — 中度缺漏（MED）

**事實**：
- §3 atls 對位表寫「FF3+FF5 美股因子 → atlas 可能用在地化台股因子」未對位具體欄位
- 沒提「alpha 顯著性在七不同時期下表現可能天差地別」 — 違反憲章 §五「策略矩陣：不同時期下的散戶優先策略」
- 散戶解讀：「如果最大回撤 + VaR 在 -30% 以上,即使 alpha 顯著也別重押」寫得對，但沒串到「高原期 -30% 可接受，轉折下壓期 -30% 不可」

**處理**：文末加「期間適用性」段，引憲章 §五策略矩陣
**等級**：MED

---

### 1.3 SK-20 — 中度衝突（MED）

**事實**：
- 「Big/Small 切分」沒區分「市值是 dimension 還是 behavior_proxy 層」
- atlas 後端實際有 8+18 產業映射（from B5-3 PR-A/B）；但 wiki 寫的「市值分位」是横向切，未與產業映射互鎖
- 與憲章「七維錢潮雷達 3+2+2」沒掛上

**處理**：轉化為「產業 × 市值」雙軸；加 cite canonical spec D-CF-04（capital-flow-seven-dimension-spec.md §4）
**風險**：產業映射下游對位變動多，過度耦合 wiki 與後端 schema
**等級**：MED

---

### 1.4 SK-16 — 中度缺漏（MED）

**事實**：
- §3 對位寫「回傳 CIRCUIT_BREAKER」 — 與憲章 B1「管線重排 MacroFlow 前置」衝突（舊語意「訊號觸發」vs 新語意「時期觸發」）
- 沒提「Advisor.AllowedStrategies(regime)」時期過濾 — 即使 MCP 尚未公開，這頁是給 kaecer 的對位承諾

**處理**：加一段「`backtest_signals` 在不同時期下的信號可用性」表（保守 vs 攻擊 vs 中性期各有不同意義）
**等級**：MED

---

### 1.5 SK-29 — 中度缺漏（MED）

**事實**：
- §3 提到「session_count=147 / max_drawdown_pct=1」但沒說此 session 落在七時期哪一期
- atlas-mcp 實跑能拿 period / regime 兩個欄位（B5-2 補強後）— wiki 應該引導對 agent 拿這個交叉看

**處理**：在 §3 加「期間依賴性警告：max_drawdown=1% 在高原期可能正常,在黑天鵝期可能異常」
**等級**：MED

---

### 1.6 SK-01 — 低度過期（LOW）

**事實**：
- 「論文版 86 因子 vs atlas 約 10-15 個核心欄位」已寫 ✅
- 但「行業中位數填補」段說「atlas 用 industry_sector_lookup 取產業歸屬」沒升級 — B5-3 PR-A/B 後有 sector_index_reader 與政府資金 per-broker 對位

**處理**：補一句「atlas 8+18 產業映射已存在（B5-3）」作 update 標註
**等級**：LOW（保持原內容準確,僅補一句）

---

### 1.7 _consult-index.md — 中度違背（MED）

**事實**：
- §3 atlas-mcp 端點字典完全沒提「時期判斷 MCP 工具（M1 已⬜）」
- §6.1 L3 狀態表沒提「reining 工具降級：E3 API partial 已記錄但未更新 §3」

**處理**：§3 加新 row「[`PENDING`]`strategy_ranker` 暴露七時期資料」(雖然 strategy_ranker 內部 regime 仍用 BULL/NEUTRAL/BEAR/HIGH_VOL 4 分類,不一致是 MCP 端的問題)
**等級**：MED

---

### 1.8 _index-finskills.md — 低度過期（LOW）

**事實**：
- 32 SK 預評表對位 mission 可讀
- 但 §1 預評標準「對位 mission『找信息差/找漏洞』」沒引憲章 §五「散戶跟隨座標」
- 與新憲章對位最弱：策略類別欄全空（沒標每個 SK 對位 Defensive/Aggressive/Tactical）

**處理**：§1 加「對位 ATLAS_METHODOLOGY.md §五策略矩陣」+ 預評表加欄位「策略類別(預)」
**等級**：LOW

---

### 1.9 _inbox.md — 低度過期（LOW）

**事實**：沒提對位憲章是底線
**處理**：加 cross-reference 到 _methodology_alignment_audit.md
**等級**：LOW

---

### 1.10 重大策略違背 — 4 條

#### TW-X1：對散戶的「Regime 三態 / 七時期」一致性
- wiki 所有 SK 頁面對外「術語」沒標明「Regime = 三態向下相容層」 — 看的人會誤認 RISK_ON 為唯一真值
- 處理：在 5 頁 SK 的「一句話定位」段加「本檔術語：七時期為 PeriodDetector 真值；RISK_ON/OFF/NEUTRAL 為向下相容」
- 等級：HIGH

#### TW-X2：「七大資金勢力」舊語意污染
- 雖然 5 頁 SK 都沒直接寫「七大資金勢力」，但「資金流相關敘述」仍可能誤指
- 處理：對 SK-16/18/20 加備註「atlas 後端 = 七維錢潮雷達 3+2+2 分層,不可加權平均」
- 等級：MED

#### TW-X3：MCP prompts 的 E3 partial 對外承諾缺口
- list_prompts 顯示 prompts 仍用舊三態詞,但 wiki 沒標明
- 處理：在 _consult-index §3 末加引用：`prompts:` `regime_interpretation` 等仍用舊三態詞 RISK_ON/OFF/NEUTRAL/TRANSITIONAL — 屬 E3 partial,等 atlas-mcp 升級
- 等級：MED

#### TW-X4：MCP `strategy_get_summary` 等內部 regime 用 BULL/BEAR/HIGH_VOL/NEUTRAL — 非憲章策略
- 與憲章三分類不一致
- 處理：SK-16/18 對位表加附註「atlas 後端 strategy_ranker 內部 regime = 4 分類(BULL/NEUTRAL/BEAR/HIGH_VOL),與憲章三分類(Defensive/Aggressive/Tactical)不同層次
- 等級：MED

---

## §2 處理動作（草案 → 待 kaecer 拍板）

### 階段 A：高優先 (建議立刻動，1 session 完成)

| 動作 | 動哪檔 | 動作細節 |
|------|--------|---------|
| A1 | _method.md §3 | 加第四條「對位 ATLAS_METHODOLOGY.md v1.0」到三條鐵律 |
| A2 | 5 個 SK 頁 frontmatter | 加 `methodology_aligned: true/false` + `atlas_constitution_ref: §X.XX` |
| A3 | 5 個 SK 頁「一句話定位」段 | 加「本檔術語：七時期為真值」備註 |
| A4 | _consult-index.md §3 + §6.1 | 加 E3 partial 與 M1 pending 標記 |

### 階段 B：中優先 (下一 session，~30 分鐘)

| 動作 | 動哪檔 | 動作細節 |
|------|--------|---------|
| B1 | SK-18 §3 | 加「期間適用性」段 |
| B2 | SK-20 §1 | 加產業 × 市值雙軸說明 |
| B3 | SK-16 §3 | 加 Advisor.AllowedStrategies() 對位承諾 |
| B4 | SK-29 §3 | 加期間依賴性警告 |
| B5 | SK-16/18 對位表 | 加 TW-X4 附註 |
| B6 | _index-finskills.md §1 | 加對位憲章 §五 |

### 階段 C：觀察 (等 atlas-mcp 升級後再動)

| 動作 | 動哪檔 | 動作細節 |
|------|--------|---------|
| C1 | 5 頁 SK 升 active 條件 | 加「period × strategy 對位需 M1 MCP 工具公開」 |
| C2 | _consult-index §3 | `strategy_ranker` 加 period 欄時同步補 |
| C3 | 各 cron 9a9aa3 prompt | 重設計時對位七時期語意（已送歷史不能改） |

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

> **最後更新**: 2026-07-30 04:00 (草案)
> **採納決策權**: kaecer
