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

救活 32 個 Fin-Skills → atlas 可對位 wiki skill;對位憲法 §1 + mission「找信息差」。細節見 `_method_amendment_history.md` §起源。

## 六條鐵律(v6.37 kaecer 拍板:所有 .md ≤ 9000 bytes)

1. 不搬運,翻譯——每頁含論文/atlas/散戶三層
2. 不瞎寫——tool 不確定標 `待驗`
3. 不裝完成——L3 端點驗證沒跑 = draft
4. 不違背憲章——`ATLAS_METHODOLOGY.md` v1.0 真理源頭;七時期+3+2+2+三分類
5. 派工備份——改動前後各備份一次(byte-perfect 對位,§5.1 SOP)
6. **所有 .md 檔 ≤ 9000 bytes**(kaecer v6.37 拍板)— **例外**:
   - **SK 頁**(SK-*.md):必 ≤ 9000 bytes = 對位 CI size-check
   - **入口檔**(_consult-index.md):≤ 9000 bytes
   - **審計追蹤檔**(_methodology_alignment_audit*.md / _atlas_mcp_path_investigation.md):≤ 9000 bytes
   - **規範本體**(_method.md):≤ 9000 bytes
   - **規範附錄**(_method_amendment_history.md):≤ 5000 bytes(本附錄承接起源與演進 + M1-M9 升分表;_method.md 瘦身後 2026-08-07 增設)
   - **`_inbox.md`**:≤ 12000 bytes(對位第七條例外)+ size-check job 實作 warn-only 模式
   - **`_inbox_archive.md`**:無 size 上限(歷史承接,2026-08-07 增設)
   - **_self-audit.md 例外**:跨 session 累積審計日誌(不入 git,對位 .gitignore),**僅要求 ≤ 9000 bytes 透過 governance-log.md 分流**;如過度膨脹需重組審計紀錄格式而非精簡內容。

   對位 CI:`.github/workflows/validate-wiki.yml` `size-check` job 跑 `wc -c ≤ 9000`(SK 頁驗證)。


## 第五條鐵律(2026-08-02 k拍):快照值必附 timestamp

對位 SOUL §0.1 第 6 條邊界「_method 規範修改需拍板」,本條由 kaecer 2026-08-02 22:30 拍板新增:

- **觸發條件**:任何數字引用(session_count / sharpe / max_drawdown / universe_overlap 等)若**隨時間變動** = 必須附 `timestamp + 端點名稱`
- **正確格式**:`2026-08-01 23:15 結算 snapshot,risk_get_metrics session_count=147`(歷史快照)vs `2026-08-02 20:40 當下,risk_get_metrics session_count=150`(當下值)
- **不規範寫法**:`risk_get_metrics session_count=147`(沒附 timestamp,讀者無從判斷是歷史快照或當下值)
- **跨 session 同步**:發現新事實時必跑全文 `grep` 同步所有頁,**不盲目全改**;分「歷史快照保留」vs「當下值修」兩類處理
- **教訓**:2026-08-02 20:40 重跑確認 universe_get_sessions 150 sessions 後,SK-16/17/29 + _inbox 已修當下值,但 14+ 條 2026-08-01 23:15 結算時點的 session_count=147 殘留是**歷史快照,保留不修**(修壞會失真)
- **本條與第 4 條對位**:第 4 條「不違背憲章」是**內容對位**,第 5 條「快照值必附 timestamp」是**形式紀律**,兩條並列
- **降級觸發**:任何頁違反第 5 條 = M7 結算分降 1
- **升級觸發**:全 33 頁跑 Python 結構驗證全綠(快照值都附 timestamp) = M7 結算分 +1

**每日驗證收尾檢查清單(必跑 6 項)**:

- [ ] 每頁 `wc -c` ≤ 9,000 bytes
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

對位 SOUL §0.1 例外 6 + kaecer 2026-08-04「B+C 才是正確的」拍板。

- **觸發條件**:對位 narrative model 之 `hit_rate` / `weight` 引用,必附 (a) 報告來源 + (b) release 日期 + (c) PDF link
- **5 錨點**(對位 `templates/trigger-equipment-capex-external-report-cycle.md`):
  1. UNCTAD WIR(annual,5-7 月)
  2. Stanford HAI AI Index(annual,4 月)
  3. BIS Annual Economic Report(annual,6 月)
  4. IMF WEO(semi-annual,4/10 月)
  5. HKS M-RCBG WP(irregular)
- **正確格式**:`UCTAD WIR 2026 (5/21/2026 release, ISBN 978-92-1-154998-0): 5 年半導體 greenfield CAGR +54%`;未命中即標「未達觸發條件」,**禁止編造**
- **與第 5 條對位**:第 5 條「快照值必附 timestamp」= 形式紀律;第 6 條「外部權威報告週期稽核」= 內容紀律(雙層)
- **降級觸發**:narrative model 對位不到外部報告來源 = M7 結算分降 1
- **升級驗收**:2027 年 4 月 WIR + HAI 同步 release → 命中 + hit_rate 改善 ≥5% = M1 升 1


---

## 重啟 30 秒程序(2026-07-28 k拍)

每次 session 開頭執行三步:
1. `skill_view name="atlas-skill-inbound"`
2. 讀本檔確認規範
3. `ls SK-*.md + cat _inbox.md` 看現況

自動歸位:6 段格式 / 9 欄 frontmatter / Quota(3 頁)/ 路徑(憲法在 atlas-notes)/ 命名(atlas = atlas,不是 atlas-go)/ 精選優先序(SK-01 → 16 → 18 → 20 → 29)。

**權威等級 = 憲法 §1**。

---

## 第七條例外(2026-08-07 kaecer 拍板):`_inbox.md` size 上限擴充

- **規範**:`_inbox.md` ≤ 12000 bytes
- **CI**:`validate-wiki.yml` size-check job = SK ≤ 9000 嚴格 fail + _inbox.md ≤ 12000 warn-only
- **歸檔 SOP**:連 2 次 session append 後 > 12000,agent 自動評估把 §6 §6.1 §6.2 完成段落移 `_inbox_archive.md`,主檔只留最新 2 版本結算

---

**附錄**:起源與演進 + 升分綁定(M1-M9)見 `_method_amendment_history.md`。