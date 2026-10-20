

---

## [2026-10-21 自 _inbox.md 歸檔] D6 待辦 / 結清兩項長期待辦 / 2026-09-27 S6 待複驗佇列 / 已結案段（依 _method.md 第七條 v1.1；主檔 append 後 14,717B > 12,000B 上限）

## D6 新增待辦(2026-08-12,跨 SK 性質)

### v6.59 overclaim 真因(2026-08-12 復盤)
- v6.59 session 聲稱「SK-34 升 active」但實際主檔未變更(SHA256 byte-perfect 相同)
- 根因假說:LLM 工具調用錯誤,把「備份已建立」誤報為「升 active 完成」
- 待辦:hermes 排查 LLM tool call 故障,避免下次類似 silent failure

### SK-20 60 日歷史端點缺口(2026-08-12 L3 探測)
- `/api/stock/history` `/ohlc` `/ohlcv` `/daily` `/price-history` `/quote/history` `/history` 全部 404
- 推論:atlas 無原生歷史端點,SK-20 Step 3 需 client 端 quote polling + 累積
- 待辦:規劃 client 累積報價(每日定時跑 quote 並寫入本地 DB)

### M9 升分條件(沿用 v6.58,v6.60 不自升)
- 待 kaecer 拍板升分(cron 自升違規)

amendable_by: kaecer
session_count_tracking: agent(autonomous, see _self-audit.md)
archive_owner: agent(autonomous, see _inbox_archive.md)

---

## 待辦（active；本文以下至「已結案」標題前，預算 ≤ 8,000 B）

### 結清兩項長期待辦（原標題；其中 (i) Fin-Skills 查核已於 2026-09-28 歸檔）

**範圍**：結清本檔 9/2 段（原 line 96-101）與 9/15 段（原 line 129-133）兩項 D24+ 待辦。**只查核與提案,未動任何 SK 頁。**

### (ii) SK-37+ 優先序決策簡報 → **提案,待 kaecer 拍板**

現況實測：`ls skills/SK-*.md | wc -l`=37;active 35／archive 2（SK-27、SK-30）／draft 0 ⇒ **quota 飽和屬實**。候選全部取自現存缺口清單,非新構想：

1. **pnl-attribution 歸因工作流頁** — SK-22 未消化:「by-factor 排除式邊際貢獻 ❌＝atlas 無 ablation 端點,屬結構性缺口」「pnl-attribution 尚未寫成獨立 SK」。缺口:散戶問「哪個因子在賺錢」目前只有替代路徑。力度:1 頁 ＋ L3 實跑端點。
2. **放空成本模型頁** — SK-19 未消化:「融券借券費沒在預設內,需查 `strategy_ranker` short 覆蓋率」;SK-16 未消化:「融券限額與流動性折扣,atlas 也沒對位」⇒ **兩個 HIGH 頁同指此缺**。力度:1 頁 ＋ 查端點覆蓋。
3. **流動性／買賣價差篩選頁** — SK-21 未消化:「無流動性分位篩選,應加 `stock_get_chips` 對位」「無 spread 資料源」。力度:1 頁 ＋ L3 實跑 chips。
4. 組合權重變體（min_var／max_div／risk_parity）— SK-17 未消化;atlas 端缺 ⇒ 薄頁風險。
5. SHAP／LIME 個股層級解釋 — SK-13 未消化;atlas 端只有 global importance。
6. SK-31 未落模板 ×3（#14 `trigger-megaproject-2-quarter-lag`／#15 `trigger-equipment-capex-external-report-cycle`／#16 `trigger-renewable-energy-divergence`）— SK-31 未消化明文待產;且 SK-31 六層因果鏈未全勾 → 未達升 active。屬 `templates/`;**quota 已拍板不計入(2026-09-27,見 §B),但須記模板現數**。

**非新頁但缺口更大（另案）**：T9 Task 3「L3 批次 105 步」本日查核**從未執行**（37 頁僅 SK-34 有 `l3_*`）;`_inbox.md` D6 的「SK-20 60 日歷史端點缺口」＝SK-03/12/29 的共同前置依賴。

**建議排序（提案,需核可）**：**1 → 2 → 3**。理由:三者皆結構性缺口（不會因再試參數而消失）、且直對 mission（找漏洞／成本誠實／流動性風險）。
**不建議重提**：`_archive/2026-08-22-sk37-revert/SK-37-fin-skill-decision-index.md`——kaecer 2026-08-22 00:45 已以「品質不符 top 6 標準」撤回（`_internal/_completed-plans-2026-08.md`）。

**待 kaecer 拍板（未自作決定）**：① 候選 1–3 是否開頁、編號自 SK-37 起 ② ~~模板類是否佔 quota~~ **已結案 2026-09-27(不計入,見 §B)** ③ (i) 的「來源不可考」定調 ＋ 兩處幽靈引用是否修 ④ 來源是否在他機（E 條）。

**Telegram**：`[SILENT]`（人工查核,非 cron）
**改動**：依 `_method.md` 第七條歸檔 SOP（主檔只留最新 2 版結算）,原 **9/2 段（2,885B）＋ 9/15 段（2,868B）原文移入 `_inbox_archive.md`**（append,含出處標頭）＋ 本檔 append 本段;**實測 11,990B ≤ 12,000B**。
**移段時仍 OPEN 的項**：9/15 段「cron prompt 內嵌缺口清單 stale → 走 task-governance 更新 SKILL.md／_method.md」未結,隨段入 `_inbox_archive.md`（未消失）。

---

## 2026-09-27 S6 `待複驗` 佇列(9 頁;check-freshness 18→0)

下列 9 頁的日期＋量化快照行只有**資料日／舊快照／負面查核**,查無可引核對事件 ⇒ 標 `last_verified: "待複驗（2026-09-27）"` ＋ `verify_by: pending`。**關閉＝真跑來源或端點並把結果寫回該頁證據段**,才可改實日期(另 9 頁有頁內核對事件,已寫實日期)。

- `concepts/t1-t4-signal-light.md`:4 成 vs 25–35% 待查;09-27 實測僅負面(無該欄位)
- `concepts/taiwan-chip-flow-analysis.md`:標記行只有 audit-fix／實務慣例註,40–45% 未附來源
- `templates/trigger-etf-rebalance.md`:08-03 舊快照,僅 audit-fix
- `templates/trigger-foreign-3day-inflow.md`:08-03 舊快照 `+21.83 億`,hit_rate 為舊條件
- `templates/trigger-hbm-cycle-cooling.md`:08-04／08-09 舊資料日;08-09 unreachable
- `templates/trigger-margin-350b.md`:08-03 舊快照;「> 5000 億」無核對事件
- `templates/trigger-msci-rebalance-pressure.md`:04-30 權重資料日;08-09 unreachable
- `templates/trigger-retail-margin-decrease.md`:08-03 舊高水位 5074.63 億
- `templates/trigger-sox-foreignflow.md`:08-03 舊快照(SOX +0.07%)

## 已結案（近期；預算 ≤ 4,000 B，超出即移 `_inbox_archive.md`）

## 已結案（近期；預算 ≤ 4,000 B，超出即移 `_inbox_archive.md`）

- 2026-09-27 模板狀態校正（SK-31）＋ 模板類 quota 條文查核（**已拍板結案**）⇒ 原文已歸檔 `_inbox_archive.md` §[2026-09-30 自 _inbox.md 歸檔]（2026-09-30）


## [2026-10-21 自 _inbox.md 歸檔] 2026-10-16 週末修復清單全段（A–G，7,261 B；依 _method.md 第七條 v1.1 active 區 ≤8,000B 超限；唯一實質未結項 C 項已於同日 §CIO-2010 實測結案，其餘待 @atlas-dev / @kaecer 拍板）

## 2026-10-16 週末修復清單 (來源: `wiki-friday-lint 2026-10-16 23:00 CST` / `/tmp/atlas-wiki-lint-2026-10-16.md`)

**範圍**:`wiki-friday-lint` 2026-10-16 23:00 CST 跑出的 253 行報告 (93 pages scanned / 120 unique slugs)。本次解讀只列 🔴/🟡 結構性項目;⚪ noise (缺 title/created/updated/type/sources) 大量落在 SK-00..SK-19 與 templates/ = 已知 2026-09-27 修 lint 後的歷史遺留,**不計入本週末清單**,下次 tool owner 走 PR 校正 schema enum 一併收斂。**與上週(2026-10-10)報告同結構同 schema**,不是新一輪漏洞 = 結構穩定;本次浮現的是同類 false positive,待 lint tool owner 一併解。

**A. 🔴 Broken contradiction refs (23 條)**

- 結構與上週一致:多為 `contradictions: [[]]` 空 list(顯示「還有 3 條未列」截尾 = lint script `head -N` 截尾未修);有實質描述的僅 3 條:`s-paradigm-redefinition` (vs v0.1/v0.2-three-paradigms)、`l1-t-overview` (vs v0.1-L1T-multi 舊詮釋)、`taiwan-money-flow-seven-institutional-buckets` (七類核心機構 vs atlas spec 3+2+2 七維錢潮雷達,沿袭 2026-08-22 裁定以 atlas spec 為主)。
- 修復建議:1) `contradictions: [[]]` 空 list 批次視為 false positive → 走 PR 改 SOP「空 list 不報」(同上週建議,本週 lint 仍未修);2) `s-paradigm-redefinition` 與 `l1-t-overview` 真衝突依 `atlas-wiki-quality §1.1` 走 page-level CORRECTION 段;3) `taiwan-money-flow-seven-institutional-buckets` 已有裁定 = 在頁首加「裁定 2026-08-22=atlas spec 3+2+2 為主」一行即可收斂(同上週建議,本週仍未動)。
- **誤判收斂**:`contradictions: [[]]` 空 list 23 條中絕大多數 = false positive = 本週末不動 wiki 本體(對位 SOUL §Mission 7「不擅自動 wiki」);等 lint tool owner 修。
- 對位:`references/quality-standard.md` 矛盾處理程序 + SOUL §3.1 fabric-free + §CIO-1601 撞號防護 SOP。

**B. 🟡 Orphan + 未列於 index (1 條: `audit-report`)**

- 頁面:`templates/audit-report.md` 無任何 inbound wikilink + 不在 `index.md`。同 2026-10-10 週報同名單。
- 建議:**誤判 + 同上週結論** — 該檔是 trigger atlas-skill-inbound 三日 vault 對位底稿,**設計為孤立觸發器模板** = 應保留 orphan,改 lint 工具排除 `templates/audit-*` 不算 orphan。本週 lint 仍未處理 = 同累積待 lint tool owner 解。
- 對位:`atlas-wiki-quality §1.1 「orphan ≠ 該刪」`。

**C. 🟡 Pages >200 行 (13 條)**

- 同 2026-10-10 週報同名單,行數完全一致(482/477/462/424/414/385/361/295/270/260/247/217/208) = **wiki 內容本週未變動,純 lint 二次跑出的同樣結果**。
- 結構性影響:超 200 行頁 = 大多逼近而非 wash 硬上限(SK 頁 9000B / 入口 9000-12500B);但本 lint 沒報 size 只報 lines,**需 `wc -c` 二次量測才能下「需 split」結論**(對位 USER §1 第 2 條「禁止單一 evidence 直接寫結論」)。
- 修復建議:1) 走 worktree 跑 `find . -name "*.md" -exec wc -c {} + | awk '$1>8000'` 二次量測,只對**已超 8000B** 的頁 split;2) 先處理 `atlas-mcp-tools-reference`(482 行 工具參考,合理 split 為 endpoint/讀寫/錯誤碼三段);3) 其餘 12 條若 wc 仍在預算內 = 觀察區。
- 對位:`atlas-wiki-quality §4.4` size 預算 + USER §1 第 2 條 Hard NOs。

**D. 🟡 contested: true (6 條人工複檢)**

- 同 2026-10-10 週報同名單:`atlas-three-paradigms-v0.2-summary` / `funding-forces-taxonomy-e05-pending-approval` / `s-paradigm-redefinition` / `t1-t4-signal-light` / `taiwan-chip-flow-analysis` / `taiwan-money-flow-seven-institutional-buckets`。**wiki 內容本週未變動 = contested 清單穩定**。
- 修復建議:1) `contested` 標記依規定 v1.1 不動;2) 列為下次 quarterly 複檢 priority list(本週不處理);3) `funding-forces-taxonomy-e05-pending-approval` 名字含 `pending-approval` = 等業主拍板中,等他拍,本 bot 不擅自。
- 對位:`_method.md` 第九條① (禁止為過關補空殼)。

**E. 🟡 Stale >90 天 (4 條)**

- 同 2026-10-10 週報未列;`attachments/l1-t4-critical-minerals` 與 `l1-t5-ai-semiconductor` 兩條本週首次進入 stale 區(2026-07-17 → 2026-10-16 = 91 天);另外兩條 `atlas-three-paradigms-v0.2-summary` (2026-07-17) 與 `s-paradigm-redefinition` (2026-07-15) 沿袭先前 stale 區。
- 修復建議:1) 走 PR 評估是否需重 anchor (對位 `time-anchor` tag);2) `l1-t4` 與 `l1-t5` 是 critical-minerals 與 ai-semiconductor 主題 = L1 macro 結構 = 應有定期 refresh SOP(每季?),本 bot 不擅自寫 SOP,先記待補;3) 其餘 2 條已在 contested 清單(D),等下季複檢一併處理。
- 對位:`atlas-wiki-quality §3 S6 時效` + `_method.md` 第九條②。

**F. 🟡 tag 未在 SCHEMA taxonomy (29 條)**

- 同 2026-10-10 週報結構:出現的非標準 tag(`source-attribution` / `time-anchor` / `topdown` / `contrarian` / `content-attribution` / `comparison` / `event` / `L6` / `L2` / `hypothesis`)與上週同名單一致。
- 修復建議:1) 走 PR 把這些常用 tag 加進 SCHEMA taxonomy(治理檔 → 需 `kaecer-reviewed` 標籤,本 bot 不擅自);2) 上週已列建議,本週仍未動 = 同累積待 kaecer 拍板;3) 本週末只列名單,**不擅自動 SCHEMA**。
- 對位:`skills/_scripts/governance-files.txt` SSOT + USER §2.3 工作流偏好(kaecer 處理治理檔)。

**G. ⚪ Skip (不入週末清單;下次 tool owner PR 一併修)**

- 缺 title (22) / 缺 created (62) / 缺 updated (64) / 缺 type (20) / 缺 tags (64) / 缺 sources (51) / type 不在 enum (64):同 2026-10-10 週報同名單,絕大多數集中在 `skills/SK-*.md` 與 `templates/trigger-*.md`;lint schema 對 template 與 SK 頁的 enum 太嚴(已知 2026-09-27 修 lint 後遺留)。
- 建議:**誤判**收斂 — 走 tool owner PR 把 template/SK 頁 enum 鬆綁(template 只需最小欄: title + type; SK 頁沿袭既有 5 段 schema),不為過 lint 補空欄位(對位 USER §6.1 第 5 條「禁止道歉代替結構性修正」)。

**對位**:`wiki-friday-lint 2026-10-16 23:00 CST` → `/tmp/atlas-wiki-lint-2026-10-16.md` (253 行,15.5KB) / SOUL §Mission 2 + §Mission 7「不擅自動 wiki」 / USER §1 第 2 條 Hard NOs(單一 evidence 不結論)/ atlas-wiki-quality §1.1 + §4 / `_method.md` 第七條 v1.1 + 第九條①② / §CIO-1601 撞號防護 SOP / 上週 2026-10-10 週末清單段(同名單結構穩定 = 本週末純觀察)。

**後續派單判斷(本任務不擅自分派)**:
- @atlas-dev:走 PR 修 lint script `head -N` 截尾(23 → 全列)+ SK/template enum 鬆綁(對位 A + G);若修完,下次週報應自動歸 0
- @kaecer:走 PR 拍板 SCHEMA taxonomy 新 tag(F)+ `atlas-mcp-tools-reference` 482 行 split 拍板(C)+ Stale 4 條 refresh SOP 拍板(E)
- @atlas-skill-inbound owner:處理 23 條 contradictions 中 3 條實質衝突(A)的 page-level CORRECTION 段(同上週)
- @consultant(kaecer 拍板後才走):散戶語言化(本周無 C 項純散戶可消化 → 不派)
- @reporter(kaecer 拍板後才走):日報/Daily 不消化 lint 細節 → 不派

**信心度**:low (這是 lint observation,**不是已診斷 bug**);A 項中實質衝突僅 3 條(其餘 false positive);E 項 Stale 4 條需評估是否 refresh 而非簡單「更新 mtime」。

---

