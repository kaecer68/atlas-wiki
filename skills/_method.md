---
title: atlas-skill-inbound 方法本體(人類可讀版)
type: skill-inbound-method
source: ~/.hermes/skills/atlas-skill-inbound/SKILL.md
ingested_at: 2026-07-28
status: active
tier: T2
maturity: stable
confidence: high
decay_until: never
sources:
  - kaecer 2026-07-28 拍板「每日 5 個進修」方針
  - ~/workspace/Fin-Skills/Fin-Skills.md (32 個 SK)
  - ~/workspace/atlas-wiki/skills/SK-01-factor-library.md (示範頁)
owner: kaecer
amendable_by: kaecer
---

# atlas-skill-inbound 方法本體

> 與 `~/.hermes/skills/atlas-skill-inbound/SKILL.md` 同源。
> 這份是人類可讀版,內容同步。修改以 SKILL.md 為準,本檔鏡像更新。

## 為什麼存在

救活 32 個 Fin-Skills → atlas 對位 wiki skill(憲法 §1 + mission「找信息差」);起源見 `_method_amendment_history.md`。

## 六條鐵律(v6.37 拍板;第 6 條 2026-09-27 改為類別制)

1. 不搬運,翻譯——每頁含論文/atlas/散戶三層
2. 不瞎寫——tool 不確定標 `待驗`
3. 不裝完成——L3 端點驗證沒跑 = draft
4. 不違背憲章——`ATLAS_METHODOLOGY.md` v1.0 真理源頭;七時期+3+2+2+三分類
5. 派工備份——改動前後各備份一次(byte-perfect 對位,§5.1 SOP)
6. **size 上限依類別**(2026-09-27 kaecer 拍板,取代 v6.37 全 .md ≤ 9000):

| 類別 | 上限 | 理由(量測 2026-09-27) |
|---|---|---|
| `skills/SK-*.md` | 9,000 B | CI **實檢**;最大 8,989 |
| 入口/索引 `SK-00`/`_knowledge-router`/`_consult-index`/`index.md`/`README.md` | 9,000 B | 只導向不承載內容;最大 8,851 |
| `AGENTS.md` | 12,500 B | §10 自訂(注入檔 token 預算);現 11,027 |
| `concepts/**`、`entities/**`、`_manifest_coverage_routing.md` | 30,000 B | 參考/資料型勿硬砍;最大 28,029 |
| `docs/**`、`SCHEMA.md`、`templates/**` | 12,000 B | 規格/產物型;最大 11,190(舊制誤判) |
| `_method.md`/`_method_amendment_history.md` | 9,000/5,000 B | 規範本體自限 |
| append-only `log.md`/`_self-audit*.md`/`_inbox.md`/`*_archive.md`/`_archive/**`+`skills/_archive/**` | 無上限 | 超門檻即歸檔/切月;`_inbox.md` ≤12,000 |
| `_internal/**` | 無上限 | 結案即瘦身(2026-09-27 示範 16→4 檔) |
| 未列 `*.md`(summaries/其餘 `skills/_*.md`) | 9,000 B | 舊制沿用 |

**強制**:CI `size-check` 只硬檢 SK 頁(`_inbox.md` warn-only);餘類別 advisory。明細/落差/驗收見 `_skill-structure-guard.md §size 分類上限`。


## 第五條鐵律(2026-08-02 k拍):快照值必附 timestamp

對位 SOUL §0.1 例外 6;2026-08-02 22:30 kaecer 拍板新增:

- **觸發條件**:任何數字引用(session_count / sharpe / max_drawdown / universe_overlap 等)若**隨時間變動** = 必須附 `timestamp + 端點名稱`
- **正確格式**:`2026-08-01 23:15 結算 snapshot,risk_get_metrics session_count=147`(歷史快照)vs `2026-08-02 20:40 當下,risk_get_metrics session_count=150`(當下值)
- **不規範寫法**:`risk_get_metrics session_count=147`(沒附 timestamp,不知是歷史快照或當下值)
- **跨 session 同步**:發現新事實時必跑全文 `grep` 同步所有頁,**不盲目全改**;分「歷史快照保留」vs「當下值修」兩類處理
- **教訓**:2026-08-02 重跑確認 session_count 150 後只改當下值;14+ 條 2026-08-01 23:15 的 147 屬歷史快照,保留不修(修壞失真)
- **本條與第 4 條對位**:第 4 條「不違背憲章」是**內容對位**,第 5 條「快照值必附 timestamp」是**形式紀律**,兩條並列
- **降級觸發**:任何頁違反第 5 條 = M7 結算分降 1
- **升級觸發**:全 SK 頁跑結構驗證全綠(快照值都附 timestamp) = M7 結算分 +1

**每日驗證收尾檢查清單(必跑 6 項)**:

- [ ] 每頁 `wc -c` ≤ 六條鐵律 6 類別上限
- [ ] 每頁 6 段俱全
- [ ] frontmatter 9 欄齊全
- [ ] 至少 1 頁 L3 真跑過
- [ ] `_inbox.md` 已更新跨 SK 待辦
- [ ] 對應 Fin-Skills 段落完整讀過(非略略讀)

## 跟其他 skill 互動

寫入時 → `wiki-critic`;三日循環 → `knowledge-harvest`;重大決策 → `task-governance`;散戶解讀 → `financial-advisor-coach`。

## 修改守則

- 修改本檔 / SKILL.md 走 `task-governance` 流程
- 兩檔內容必須同步(SKILL.md 為主,本檔鏡像)
- 連續 3 天未產出 → k拍是否廢除

**卡住升級規則(對應動作)**:

| 情況 | 動作 |
|------|------|
| 找不到對位 tool | 跳過此 SK,挑下一個,不硬寫 |
| 概念太學術(三題門檻全跳過) | 標 `[ARCHIVED — 學術展示無對位]`,放入 `skills/_archive/` |
| 5 個湊不滿 | **不硬湊**——3 頁高品質 > 5 頁混充 |
| L3 跑不動 | 維持 draft,絕不偽造通過 |


## 第六條鐵律(2026-08-04 T3-A248 k拍「B+C」):外部權威報告週期稽核

對位 SOUL §0.1 例外 6 + kaecer 2026-08-04「B+C」拍板。

- **觸發條件**:對位 narrative model 之 `hit_rate` / `weight` 引用,必附 (a) 報告來源 + (b) release 日期 + (c) PDF link
- **5 錨點**(對位 `templates/trigger-equipment-capex-external-report-cycle.md`):
  1. UNCTAD WIR(annual,5-7 月)
  2. Stanford HAI AI Index(annual,4 月)
  3. BIS Annual Economic Report(annual,6 月)
  4. IMF WEO(semi-annual,4/10 月)
  5. HKS M-RCBG WP(irregular)
- **正確格式**:`UCTAD WIR 2026 (5/21/2026 release, ISBN 978-92-1-154998-0): 5 年半導體 greenfield CAGR +54%`;未命中即標「未達觸發條件」,**禁止編造**
- **與第 5 條對位**:第 5 條=形式紀律,本條=內容紀律(雙層)
- **降級觸發**:narrative model 對位不到外部報告來源 = M7 結算分降 1
- **升級驗收**:2027 年 4 月 WIR + HAI 同步 release → 命中 + hit_rate 改善 ≥5% = M1 升 1


---

## 重啟 30 秒程序(2026-07-28 k拍)

每次 session 開頭執行三步:
1. `skill_view name="atlas-skill-inbound"`
2. 讀本檔確認規範
3. `ls SK-*.md + cat _inbox.md` 看現況

自動歸位:6 段格式 / 9 欄 frontmatter / Quota(3 頁 SK)/ 路徑(憲法在 atlas-notes)/ 命名(atlas≠atlas-go)/ 精選序(SK-01→16→18→20→29)。

**模板不佔 quota(2026-09-27 kaecer 拍板)**:`templates/trigger-*.md` = cron 觸發定義(非知識頁)→ 不計入 3 頁;**交換義務** = 結算記「trigger 模板現數」(2026-09-28:21 檔)。反例照實記:`_manifest_coverage_routing.md:134` 曾把 `concepts/` 頁記「計入 1/3」——不推翻,因 templates 是觸發定義非知識頁。

**權威等級 = 憲法 §1**。

---

## 第八條(2026-08-22 kaecer 拍板):盤查修復自主權 — 決策分類

為終結「什麼都要 k拍」的過度升級,訂決策分類:

**agent 自扛直接做(branch+PR 留痕 + 結果回報,不預先拍板)**:
- (a) 有明確 ground truth 的事實錯誤修復(官方文件 / atlas 源碼 / 實跑端點)
- (b) 工程方法選擇(修復方式、門檻設計、檔案結構、瘦身切點、router 設計)——盤查資訊在 agent 側的決策
- (c) 資訊不丟的搬移 / 歸檔(含 wiki→notes 知識路由)

**仍需 kaecer 拍板**:
1. 規範本體修改(本檔 / SKILL.md / SOUL / AGENTS 規則層)
2. 憲章對位裁決(E05 簽核、L1-L5 定義統一、情緒層收編等)
3. mission / 預算 / 對外發布 / 不可逆刪除

**判準一句話**:決策所需資訊不對稱在 agent 側 → agent 自決;在 kaecer 側(意圖 / 風險承受 / 金錢)→ 拍板。

對位:SOUL §0.1 例外 6(本條即經 2026-08-22 拍板)。

## 第七條例外（2026-09-02 kaecer 拍板，v1.0 修訂）：精確化

**邊界**（v1.0 精確化 + v1.1 兩區）：

- **規範**：`_inbox.md` ≤12,000 B（size 例外**只針對**§3 結算頻率／§5.3 觸發器／M10 健康度子項事實紀錄）
- **CI**：強制範圍見六條鐵律 6。
- **v1.1（2026-09-28）兩區**（總量仍 ≤12,000）：`## 待辦（active）` 標題前後合計 **≤8,000 B**、`## 已結案（近期）` **≤4,000 B**（`check-wiki-pages.py` 檢查）；append 前若該區將超限，先移最舊已結案條目到 `_inbox_archive.md`——**首次即超限亦同**。
- **v1.0 新增**：評分維度新增（= §2 結構變更，走 §2 修訂 SOP + 拍板）與 M10 evidence **均不適用**本例外

對位：SOUL §0.1 例外 6（本條即經 2026-09-02 拍板）。

---

## 第九條（2026-09-18 kaecer 拍板）：反補丁與內容歸屬

對位 SOUL §0.1 例外 6（配套見 `_skill-structure-guard.md`）。① **不得以滿足檢查器為目的新增空殼內容**（別名段／重複標題／行號指路／佔位段）——檢查器抓不到＝結構要重構（正名／重排），不是加標題。② **填入前先判歸屬層級**（SK 段／concepts／entities／endpoint card／templates／_inbox／_self-audit 等；判準＝`_manifest_coverage_routing.md §3.2`）。③ **落地＝語意最小重構**，不得貼上後不處理。④ **收尾義務**：須同 PR 完成結構修正，否則在 `_inbox.md` 立待辦（根因＋期限），不得留髒檔。

---

**附錄**:起源與演進 + 升分綁定(M1-M9)見 `_method_amendment_history.md`。