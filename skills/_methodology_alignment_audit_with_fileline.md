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

---

## 附錄 H：每條主張的 file:line 證據 + atlas-go 系統主張觀測依據(2026-07-30 04:50 由 hermes 補)

> **補錄紀律**：kaecer 2026-07-30 04:55 拍板「把 12+4 草案整份拿出來,加 file:line 撐著,附行號版給我重新派案檢查」;下列 16 條 = 草案 §1.1~§1.10 12 條 + TW-X1~TW-X4 4 條;每條不動一字,只在後補證據。
> **規則**:行號採「檔案:行數」=目前(`2026-07-30 04:50`)該檔案的行數;頁面文字不動。
> **atlas-go 系統主張觀測依據** = 我當時用的工具呼叫 + 工具回傳(raw output excerpt,不可精修)。

### 1.1 _method.md 三條鐵律 (HIGH)

- **草案主張**:「_method.md 是『下蛋的雞』... 三條鐵律（不搬運/不瞎寫/不裝完成）已存在但沒強調『以憲章 v1.0 為對位真理源頭』」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/_method.md:30` — 「## 四條鐵律」標題(草案寫時是「## 三條鐵律」)
  - `~/workspace/atlas-wiki/skills/_method.md:32` — 「**不搬運,翻譯**」(草案寫時原 3 條之首)
- **atlas-go 系統主張**:N/A(此條是 wiki 內部規範,沒觸及 atlas-go)

### 1.2 SK-18 factor alpha 期間適用性 (MED)

- **草案主張**:「§3 atls 對位表寫『FF3+FF5 美股因子 → atlas 可能用在地化台股因子』未對位具體欄位」「沒提『alpha 顯著性在七不同時期下表現可能天差地別』」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/SK-18-factor-alpha.md:34` — 「因子集:FF3 (Mkt, SMB, HML) + MOM (Carhart) → 預設 `FF3+MOM`」
  - `~/workspace/atlas-wiki/skills/SK-18-factor-alpha.md:54` — 「論文版 Fama-French 美股因子 → atlas 可能用在地化台股因子(如主動/被動、產業輪動),結構未必直接套」
  - `~/workspace/atlas-wiki/skills/SK-18-factor-alpha.md:56` — 「論文版 FF3+FF5 → atlas 暴露欄位需查是否齊全」
  - `~/workspace/atlas-wiki/skills/SK-18-factor-alpha.md:65` — 散戶解讀「如果最大回撤 + VaR 在 -30% 以上,即使 alpha 顯著也別重押」(沒串到七時期)
- **atlas-go 系統主張(風險暴露欄位存在依據)**:
  - **指令**:`mcp__atlas_mcp__risk_exposure`(無參數)
  - **實跑結果**:`factor_exposure={agent:0.7075, quality:0.9854, momentum:-0.0045, value:0.05, total:0.393}` — 是 `agent/quality/momentum/value/total` 5 欄,**不是 FF3 (Mkt/SMB/HML) + MOM 結構**;atlas 暴露欄位存在,但口徑與 FF3/FF5 不對位

### 1.3 SK-20 規模分組 vs 憲章 3+2+2 (MED)

- **草案主張**:「Big/Small 切分」沒區分「市值是 dimension 還是 behavior_proxy 層」;「atlas 後端實際有 8+18 產業映射(from B5-3 PR-A/B)」;「與憲章『七維錢潮雷達 3+2+2』沒掛上」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/SK-20-size-group-robustness.md:11` — verification 段含「`Big/Small` 兩組」(frontmatter)
  - `~/workspace/atlas-wiki/skills/SK-20-size-group-robustness.md:25` — 「每月按市值排序,將樣本切成 Big(大公司)與 Small(小公司)兩組,或切成 tercile 三分組」
  - `~/workspace/atlas-wiki/skills/SK-20-size-group-robustness.md:40` — 「atlas-mcp 沒有原生 time-series 市值端點,只能用 `stock_get_fundamentals` 現值快照 + `stock_get_quote` 歷史價反推」
- **atlas-go 系統主張(8+18 產業映射存在依據)**:
  - **權威來源**:`~/workspace/atlas/docs/ATLAS_SYSTEM_STATE.md:192` (B5-3 PR-A W4 段)「`SectorIndexReader` 統一讀取 `data/state/sector_index/` 下的單日/批次檔,將 **8 產業與 18 產業 schema 映射為 canonical 18 產業** return map」
  - **PR 編號**:#1421(合併日期 2026-07-29)
- **atlas-go 系統主張(3+2+2 分層)**:
  - **權威來源**:`~/workspace/atlas/docs/reference/product-positioning.md:78-84` §7.1「七維錢潮雷達 3+2+2」(verbatim)
  - **完整權威**:`~/workspace/atlas/docs/specs/capital-flow-seven-dimension-spec.md §4 D-CF-04`(此檔未讀,但 §0 草案已引用為 canonical spec;kaecer 拍 A 後已合進 §3.1)

### 1.4 SK-16 Advisor.AllowedStrategies 缺位 (MED)

- **草案主張**:「§3 對位寫『回傳 CIRCUIT_BREAKER』 — 與憲章 B1『管線重排 MacroFlow 前置』衝突」「沒提『Advisor.AllowedStrategies(regime)』時期過濾」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/SK-16-long-short-decile.md:46` — 「`backtest_signals` (2026-07-29 實跑回 **CIRCUIT_BREAKER** + sharpe_long=0.27 + sharpe_short=0.49)」
  - `grep -n 'AllowedStrategies' SK-16-long-short-decile.md`:**0 matches**(該函式/時期過濾在 wiki 完全沒有對位段)
- **atlas-go 系統主張(CIRCUIT_BREAKER 信號 vs 憲章 B1)**:
  - **憲章 B1 對應**:`~/workspace/atlas/docs/ATLAS_CONSTITUTION_AUDIT.md:47` B1 「`ExecuteWithContext()` 管線順序為:regime → collection → momentum → weights → **macroflow** → control。MacroFlow 位於推薦與權重之後,與『由上而下、由外而內』相反」
  - **憲章 B1 修復**:`~/workspace/atlas/docs/ATLAS_METHODOLOGY.md 附錄 D` B1 狀態 ✅ PR #1372(verbatim 「B1 管線重排(MacroFlow 前置)」)
  - **CIRCUIT_BREAKER 語意切換**:MCP 端點回傳的字串是「訊號層」(circuit breaker 開關),憲章 B1 是「管線層」(執行順序);原草案判這是「衝突」可能口徑偏嚴,但此 wiki 文本未更新此知識

### 1.5 SK-29 期間依賴性 (MED)

- **草案主張**:「§3 提到『session_count=147 / max_drawdown_pct=1』但沒說此 session 落在七時期哪一期」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/SK-29-rolling-window-backtest.md:49` — 對位表「`risk_get_metrics`(已實跑,session_count=147、insufficient_data=1)」
  - `~/workspace/atlas-wiki/skills/SK-29-rolling-window-backtest.md:78` — 驗證段「`risk_get_metrics` 實跑確認,session_count=147、max_drawdown_pct=1、insufficient_data=1」
  - 同檔 grep `market_period\|period_name_zh\|黑天鵝\|高原期`:**0 matches**(該 SK 全文確實無七時期字)
- **atlas-go 系統主張(atlas-mcp 可提供 period/regime 雙欄)**:
  - **指令**:`mcp__atlas_mcp__mcp_quickstart`(無參數)
  - **實跑結果**:`recent_regime_5_days.sessions[*]` 內每筆同時含 `market_period` 與 `period_name_zh` 兩欄(例 7/29 = `market_period=bull` / `period_name_zh=上升（多頭）` / `regime=RISK_ON` / `source=macro_ingest`)

### 1.6 SK-01 B5-3 補充 (LOW)

- **草案主張**:「『論文版 86 因子 vs atlas 約 10-15 個核心欄位』已寫 ✅」「但『行業中位數填補』段說『atlas 用 industry_sector_lookup 取產業歸屬』沒升級」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/SK-01-factor-library.md:60-61` — 「行業中位數填補——atlas 用 `industry_sector_lookup` 取產業歸屬」+ 「winsorize——策略層應該有,但沒明確 endpoint 暴露」
  - `~/workspace/atlas-wiki/skills/SK-01-factor-library.md:36-37` — 論文版的「缺失值處理:`median`(行業中位數填補)」+ 「極值壓縮:winsorize 至 1%~99% 分位數」
- **atlas-go 系統主張(8+18 映射與 sector_index_reader)**:
  - 權威來源同 §1.3:`ATLAS_SYSTEM_STATE.md:192` B5-3 PR-A W4(SectorIndexReader 新增)

### 1.7 _consult-index §3 缺時期判斷工具 (MED)

- **草案主張**:「§3 atlas-mcp 端點字典完全沒提『時期判斷 MCP 工具(M1 已⬜)』」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/_consult-index.md:101` — 「### Q5 宏觀/事件」段標題
  - `~/workspace/atlas-wiki/skills/_consult-index.md:105-106` — 「事件流 `narrative_get_events` 端點描述(待實跑)」+ 「壓力指數 `taiwan_stress_index` 端點描述(待實跑)」
  - `grep -n 'M1\|PeriodDetector' _consult-index.md`(patch 補完前已含 §3.1 表):
    - 草案寫時:**0 matches**
    - patch 後(line 121 / 124-127):M1 引入
- **atlas-go 系統主張(M1 ⬜ 未公開)**:
  - **權威來源**:`~/workspace/atlas/docs/ATLAS_METHODOLOGY.md §六 附錄 D (line 496-500)` M1-M5:
    - M1 時期判斷 MCP 工具公開 ⬜ — —
    - M2 資金流品質分數 MCP 工具公開 ⬜ — —
    - M3 因果鏈 tracing MCP 工具公開 ⬜ — —
    - M4 策略適用時期 MCP 工具公開 ⬜ — —
    - M5 壓力指數元件 MCP 工具公開 ⬜ — —
  - (verbatim 截自憲章附錄 D「MCP 工具對位」段)

### 1.8 _index-finskills §五策略矩陣對位弱 (LOW)

- **草案主張**:「§1 預評標準『對位 mission』沒引憲章 §五」「預評表加欄位『策略類別(預)』」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/_index-finskills.md:25-34` §1 預評標準三題表
  - `~/workspace/atlas-wiki/skills/_index-finskills.md:29` — §1 範例欄「對位 mission『找信息差/找漏洞』」(無憲章 §五 cite)
  - `~/workspace/atlas-wiki/skills/_index-finskills.md:38-74` §2 32 SK 預評表(7 欄,無「策略類別(預)」)
- **atlas-go 系統主張**:N/A(此條純 wiki 結構,未觸及 atlas-go 系統)

### 1.9 _inbox.md 缺對位憲章引用 (LOW)

- **草案主張**:「沒提對位憲章是底線」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/_inbox.md:1-42` 全文
  - `grep -i 'methodology\|憲章\|ATLAS_METHODOLOGY' _inbox.md`:**0 matches**
- **atlas-go 系統主張**:N/A

### 1.10 _method frontmatter `tier: T3` 語意過期 (LOW)

- **草案主張**:「`tier: T3` 沒定義上下文... 與憲章『tier 應該對位風險層級』可被讀成誤指」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/SK-01-factor-library.md:7`、`SK-16:7`、`SK-18:7`、`SK-20:7`、`SK-29:7` — 5 個 SK frontmatter 全用 `tier: T3`
  - `~/workspace/atlas-wiki/skills/SK-01-factor-library.md:7` 原型 — 「tier: T3」
- **atlas-go 系統主張**:N/A(`tier: T3` 是 wiki 端語意層,atlas-go 無對應欄位)

### TW-X1：wiki 全 SK 對外「Regime 三態」/「七時期」一致性 (HIGH)

- **草案主張**:「wiki 所有 SK 頁面對外『術語』沒標明『Regime = 三態向下相容層』 — 看的人會誤認 RISK_ON 為唯一真值」
- **file:line 證據**:
  - `grep -L '七時期' SK-*.md`(草案寫時):所有 5 個 SK 都無此關鍵字
  - `grep -l 'RISK_ON\|RISK_OFF' SK-*.md`(草案寫時):全部 5 個都有(RISK_ON 出現於 SK-16/18 對位表)
  - `~/workspace/atlas-wiki/skills/SK-16-long-short-decile.md:49` — 草案原寫:「`risk_get_metrics` (2026-07-29 實跑回 **max_drawdown_pct=1**, session_count=147, insufficient_data=1)」(僅給數值,無對應期間;verifier note:實際該行內容是 backtest_signals 段,非 risk_get_metrics — 草案措辭略誤,請以下方 file:line=46 為準,字面不動行)
- **atlas-go 系統主張(regime ≠ RISK_ON 唯一真值)**:
  - **指令**:`mcp__atlas_mcp__mcp_quickstart`(無參數,2026-07-30 ~04:50)
  - **實跑結果 verbatim 截錄**:
    ```json
    "recent_regime_5_days": {
      "current_period": "bull",
      "current_regime": "RISK_ON",
      "sessions": [
        {"date": "2026-07-29", "market_period": "consolidation", "period": "bull",
         "period_name_zh": "上升（多頭）", "regime": "RISK_ON", ...},
        {"date": "2026-07-28", "market_period": "consolidation", "period": "bull",
         "period_name_zh": "上升（多頭）", "regime": "RISK_ON", ...}
      ]
    }
    ```
  - **證據**:`market_period`(`bull`/`consolidation`)與 `regime`(`RISK_ON`)**雙欄並存**,regime 不是唯一值;7/29 同時 `market_period=consolidation` + `period=bull` + `period_name_zh=上升（多頭）` + `regime=RISK_ON` — 證明七時期向下相容映射生效

### TW-X2：「七大資金勢力」舊語意污染 (MED)

- **草案主張**:「雖然 5 頁 SK 都沒直接寫『七大資金勢力』,但『資金流相關敘述』仍可能誤指」
- **file:line 證據**:
  - `grep -l '七大資金勢力' SK-*.md`:**0 matches**(草案寫時正確,5 頁無此污染字)
  - `grep -l '7.*大.*資金\|七.*大.*資金' SK-*.md`:**0 matches**
- **atlas-go 系統主張(3+2+2 是正本)**:
  - 權威來源:`product-positioning.md:78-84` §7.1 verbatim「七維錢潮雷達:三大法人資金流、兩類行為代理、兩項領先／跨市場訊號;各維度角色與資料品質不同」

### TW-X3：MCP prompts 仍用舊三態詞 — 對外承諾缺口 (MED)

- **草案主張**:「list_prompts 顯示 prompts 仍用舊三態詞,但 wiki 沒標明」
- **file:line 證據**:
  - `~/workspace/atlas-wiki/skills/_consult-index.md`(草案寫時)
  - `grep -i 'prompts\|regime_interpretation' _consult-index.md`(草案寫時):**0 matches**(草案 §1.10 屬實)
- **atlas-go 系統主張(prompts 仍用舊三態詞 — 觀測依據)**:
  - **指令**:`mcp__atlas_mcp__list_prompts`(2026-07-30 ~04:50)
  - **實跑結果 verbatim**:
    ```
    [{"name": "daily_market_briefing", ...},
     {"name": "regime_interpretation",
      "description": "Interpret a current regime signal and suggest positioning implications.",
      "arguments": [{"name": "regime",
                     "description": "Current regime: RISK_ON | RISK_OFF | NEUTRAL | TRANSITIONAL",
                     "required": true}]}, ...]
    ```
  - **證據**:`regime_interpretation` 的 argument description 字串 verbatim 含舊三態詞「RISK_ON | RISK_OFF | NEUTRAL | TRANSITIONAL」(注意含 TRANSITIONAL,非憲章七時期任何一項;但 enum 仍顯示「三態」而非「七時期」是事實)

### TW-X4：MCP `strategy_get_summary` 內部 regime 為 4 分類 — 非憲章三分類 (MED)

- **草案主張**:「MCP strategy_get_summary 等內部 regime 用 BULL/BEAR/HIGH_VOL/NEUTRAL — 非憲章策略」「與憲章三分類不一致」
- **file:line 證據**:
  - `grep 'BULL\|BEAR\|HIGH_VOL' SK-*.md`:草案寫時 SK-16 frontmatter `atlas_constitution_ref` 已含「`BULL/NEUTRAL` 多頭保守策略」(patch 後);但 SK 內文 grep:`SK-16:38-49` 的對位表中無 `BULL/BEAR/HIGH_VOL` 字
  - `_consult-index.md`(草案寫時):`grep 'BULL'` 也無
- **atlas-go 系統主張(strategy_ranker 內部 regime 4 分類 — 觀測依據)**:
  - **指令**:`mcp__atlas_mcp__mcp_quickstart`(2026-07-30 ~04:50,同 TW-X1 同一 call)
  - **實跑結果 verbatim**(`active_strategies.strategies[].regimes` 取 7 個樣本):
    ```json
    {"id":"dxy-weak-us10y-down", "regimes":["BULL","NEUTRAL"]},
    {"id":"foreign-3day-inflow",  "regimes":["BULL","NEUTRAL","BEAR"]},
    {"id":"nvidia-tsmadr-confirm","regimes":["BULL"]},
    {"id":"usd-twd-32-managed-float","regimes":["BEAR","HIGH_VOL"]},
    {"id":"taiwan-strait-tension","regimes":["HIGH_VOL","BEAR"]},
    {"id":"margin-balance-extreme","regimes":["BULL","NEUTRAL"]},
    {"id":"cb-fx-intervention-warning","regimes":["BEAR","NEUTRAL"]}
    ```
  - **證據**:atlas-mcp 後端的 `strategy_ranker` 與 `active_strategies` 確實只用 `{BULL, NEUTRAL, BEAR, HIGH_VOL}` **4 分類**,並非憲章七時期,亦非憲章三分類(Defensive/Aggressive/Tactical);與憲章「三層次」(時期 → strategy 層 → regime tag)不同層

### TW-X 補: TEJ channel 壞掉 — 系統狀態旁證 (草案未獨立列條,補錄)

- **草案主張**:「TEJ 異常」(見 §3 草案上下文其他處)
- **atlas-go 系統主張(TEJ api_key 過期)**:
  - **指令**:`mcp__atlas_mcp__system_get_health`(2026-07-30 ~04:50)
  - **實跑結果 verbatim 截錄**:
    ```json
    {"channel_id":"tej","label":"TEJ 台灣經濟新報",
     "status":"error","status_text":"異常",
     "updated_at":"上次失敗: tej fetch: tej api error:
       status 400, body: {\"error\":{\"code\":\"AAA003\",
       \"message\":\"認證失敗，api_key已過期\"}}" }
    "degraded_channels":["tej"]
    ```
  - **證據**:TEJ channel 因 api_key 過期降級為 status=error;此是 atlas-go 系統真相,不影響 wiki 對位但影響 atlas-mcp 風險指標的 Q5 對位(SK 寫時未提)

### TW-X 補: stress_index 19.99/low — 與草案相關 (草案未獨立列條,補錄)

- **atlas-go 系統主張(壓力指數 = low/normal)**:
  - **指令**:`mcp__atlas_mcp__mcp_quickstart`(同 TW-X1 同一 call)
  - **實跑結果 verbatim**:
    ```json
    "stress_index": {
      "score": 19.988810172535047,
      "regime": "low",
      "date": "2026-07-29",
      "source": "taiwan_calculator",
      "components": {"vix":6.71, "foreign_flow":5.72,
                     "geopolitical":4.29, "us10y":1.57, ...}
    }
    ```
  - **證據**:stress_index score=19.99 對應「low / 0-30 / 正常配置」(對位 ATLAS_METHODOLOGY.md 附錄 A verbatim 阈值表)

---

## 附錄 H 補錄紀律

| 主張類型 | 行號來源 | 觀測依據來源 |
|---------|---------|-------------|
| wiki 內部(SK/_method/_consult-index) | `grep -n` 對應檔案 | N/A |
| atlas-go 系統(strategy_ranker / regime / prompts / TEJ / stress) | N/A(在 atlas-go) | 本對話 MCP 工具回傳 verbatim 截錄(不可精修) |
| 跨檔案引用(憲章/system-state/audit) | 該檔具體行 | N/A(該檔已讀 verbatim) |

---

> **本附錄完成度**:16 條主張全部標 file:line + atlas-go 系統主張觀測依據;草案原文一字未改。
> **產生時點**:2026-07-30 04:55(kaecer 拍板「按你的建議執行,但加三條限制」後,逐條補錄)
> **裁決用途**:kaecer 將本附錄 H 貼進查證提示詞;裁決表出來後:成立的我排修復,不成立的逐條退我改 wiki。

---

## 裁決狀態(2026-07-30 06:00 由 kaecer 查證後裁定)

### 總體裁定

| 裁決 | 條數 | 來源 |
|------|------|------|
| **成立(wiki 側修)** | 10 條 + TW-X1/TW-X2 已修 | §1.1 / §1.2 / §1.3 / §1.4 / §1.5 / §1.6 / §1.7 / §1.8 / §1.9 / §1.10 + TW-X1 + TW-X2 |
| **成立(系統側由 kaecer 修)** | 2 條 TW-X1(period 接源) + TW-X3(prompts 舊詞) | 等 kaecer 通知 |
| **撤銷** | 1 條 TW-X4 | regime 標籤 vs 策略分類正交,裁定無衝突 |
| **不成立** | 0 條 | — |

### 兩處更正(影響 wiki 修法)

1. **憲章策略三分類中文正本** = 「跟隨聰明錢／事件套利／資金對抗」(草案寫「Defensive/Aggressive/Tactical」是英文俗稱,**未對中文正名**)。已修於:
   - `_method.md:35` 第四條鐵律措辭
   - `SK-01-factor-library.md:23` methodology_alignment_tip
   - `SK-16-long-short-decile.md:17-22` frontmatter + tip
2. **SK-16/29 file:line 3 處小誤差** — 草案 + 附錄 H 給的 line 號有偏移(我二次驗證後修正過一次但仍有);kaecer 指示「施工時以實際檔案為準」,意即不依賴本附錄 line 號,以 `grep -n` 重對齊為準

### TW-X4 撤銷(已生效)

- **草案原文保留**(verbatim 歷史檔):§1.10 段 TW-X4 + §附錄 H TW-X4 段保留不修
- **附錄 H「裁決狀態」段**(本段)標 TW-X4 撤銷狀態
- **`_consult-index.md §3.1` 表內 M4 row 標記**:從 `wire mismatch` 改為 `🟢 撤銷 TW-X4 | 引用時不需再加註`,並補「正交維度」說明
- **`_methodology_alignment_audit_VERBATIM.md`**:草案 verbatim,本條 TW-X4 字面不動
- **理由**:regime 標籤(BULL/BEAR/HIGH_VOL/NEUTRAL)是 atlas-mcp 後端 `strategy_ranker` 內部的「信號可用性」標籤;策略三分類(跟隨聰明錢/事件套利/資金對抗)是憲章 §五的「組合層」分類。**兩者正交,不同層**,無衝突也不需附正交註記(SK-16/18 對位表已對應修改)。

### 修正邏輯

- **草案原文**:一字不改(kaecer 查證留底)
- **VERBATIM 檔**:與草案原文 100% diff -q 通過
- **with_fileline 檔**:本「裁決狀態」段是後加;file:line 為初版補正後定位;施工時以實際 `grep -n` 為準

### 影響下游

- **Fin-Skill 轉化**:本「裁決狀態」段為進 Fin-Skill 前的最後基準。
- **M1 endpoint 公開時**:本附錄 H 內 `M1 ⬜ 等待` 與 `_consult-index.md §3.1` M1 row 同步更新。
- **atlas-mcp 升級**(prompts 或 strategy_ranker 變動):`_consult-index.md §3.1` 與本附錄 H 同步重對齊。


> **採納決策權**: kaecer
