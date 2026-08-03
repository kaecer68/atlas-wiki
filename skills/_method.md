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

Fin-Skills(5/29 入庫的 32 個學術 SK)是死的——沒人引用、沒人實作、Hermes 載入不到。每天花 5 個額度把它「救活」,改寫成 atlas 可對位、可驗證、可散戶解讀的 wiki skill 頁。

對位憲法 §1「金融工程根據」、mission「找信息差、找漏洞」。

## 四條鐵律

1. **不搬運,翻譯**——每頁必須含「論文版概念 / atlas 對位 / 散戶解讀」三層,缺一層即不合格
2. **不瞎寫**——atlas-mcp tool 名稱不確定就標 `待驗`,不準拼湊
3. **不裝完成**——L3 端點驗證沒跑過,status 永遠是 draft
4. **不違背憲章**——`~/workspace/atlas/docs/ATLAS_METHODOLOGY.md` v1.0 (2026-07-27) 為全專案唯一真理源頭;每頁必須對位:七時期(非三態)、七維錢潮雷達 3+2+2(非「七大資金勢力」混稱)、策略三分類正名「跟隨聰明錢／事件套利／資金對抗」(2026-07-30 kaecer 拍板裁定)。本條由 kaecer 2026-07-30 拍板補充,對位依據見 `_methodology_alignment_audit_with_fileline.md` 附錄 H「裁決狀態」段。
5. **派工執行前後必做備份 checkpoint**(2026-08-01 kaecer 拍板)——任何 SK 頁改動**前**備份 `<檔名>.bak.<YYYY-MM-DD-HHMM>`;改動**後**再加備份一次。中間任何編輯事件需落在兩個備份之間,事後追查改動源頭時**用兩個備份 byte-perfect 對位**。**教訓**:atlas-wiki 非 git 管理(2026-08-01 確認),7/30 05:57 → 8/1 00:28 之間 19 小時無 SK 頁備份,period_system 附註/tip 源頭不可追蹤(T3-A40)。

## 規範速查

| 項目 | 規格 |
|------|------|
| 路徑 | `~/workspace/atlas-wiki/skills/` |
| 命名 | `SK-<原編號>-<slug>.md` |
| 單頁大小 | ≤ 9,000 bytes (2026-07-30 kaecer 拍板:bump 自 6000→9000,涵蓋 5 個 SK + 2 個索引/字典) |
| 結構 | 6 段(一句話定位 / 論文版 / 對位 / 散戶解讀 / 驗證 / 未消化) |
| frontmatter | 9 欄(title / type / source / ingested_at / status / tier / confidence / atlas_go_relevance / mcp_tools_used / verification) |
| Quota | D1 示範 1 頁 → D2+ 每日 3 頁上限（2026-07-29 kaecer 拍板降標 A 方案,見 `skill-inbound-quota-decision-history.md`） |
| 精選門檻 | 三題:對位 mission? / 有 atlas-mcp tool? / 散戶能一句話理解? |
| 完成定義 | L1 格式 + L2 對位 + L3 端點三層全過才升 active |

## 每日驗證收尾清單

- [ ] 每頁 `wc -c` ≤ 9,000 bytes
- [ ] 每頁 6 段俱全
- [ ] frontmatter 9 欄齊全
- [ ] 至少 1 頁 L3 真跑過
- [ ] `_inbox.md` 已更新跨 SK 待辦
- [ ] 對應 Fin-Skills 段落完整讀過(非略略讀)

## 第五條鐵律(2026-08-02 kaecer 拍板):快照值必附 timestamp

對位 SOUL §0.1 第 6 條邊界「_method 規範修改需拍板」,本條由 kaecer 2026-08-02 22:30 拍板新增:

- **觸發條件**:任何數字引用(session_count / sharpe / max_drawdown / universe_overlap 等)若**隨時間變動** = 必須附 `timestamp + 端點名稱`
- **正確格式**:`2026-08-01 23:15 結算 snapshot,risk_get_metrics session_count=147`(歷史快照)vs `2026-08-02 20:40 當下,risk_get_metrics session_count=150`(當下值)
- **不規範寫法**:`risk_get_metrics session_count=147`(沒附 timestamp,讀者無從判斷是歷史快照或當下值)
- **跨 session 同步**:發現新事實時必跑全文 `grep` 同步所有頁,**不盲目全改**;分「歷史快照保留」vs「當下值修」兩類處理
- **教訓**:2026-08-02 20:40 重跑確認 universe_get_sessions 150 sessions 後,SK-16/17/29 + _inbox 已修當下值,但 14+ 條 2026-08-01 23:15 結算時點的 session_count=147 殘留是**歷史快照,保留不修**(修壞會失真)
- **本條與第 4 條對位**:第 4 條「不違背憲章」是**內容對位**,第 5 條「快照值必附 timestamp」是**形式紀律**,兩條並列
- **降級觸發**:任何頁違反第 5 條 = M7 結算分降 1
- **升級觸發**:全 33 頁跑 Python 結構驗證全綠(快照值都附 timestamp) = M7 結算分 +1

## 跟其他 skill 互動

- 寫入時 → `wiki-critic` 跑 6 項檢查
- 三日循環 → `knowledge-harvest` 自動掃 `skills/` 變動
- 重大決策(規範修改、退場)→ `task-governance`
- 散戶解讀段 → 語言紀律跟 `financial-advisor-coach` 一致

## 卡住升級規則

| 情況 | 動作 |
|------|------|
| 找不到對位 tool | 跳過此 SK,挑下一個,不硬寫 |
| 概念太學術(三題門檻全跳過) | 標 `[ARCHIVED — 學術展示無對位]`,放入 `skills/_archive/` |
| 5 個湊不滿 | **不硬湊**——3 頁高品質 > 5 頁混充 |
| L3 跑不動 | 維持 draft,絕不偽造通過 |

## 修改守則

- 修改本檔 / SKILL.md 走 `task-governance` 流程
- 兩檔內容必須同步(SKILL.md 為主,本檔鏡像)
- 連續 3 天未產出 → kaecer 拍板是否廢除

## 起源與演進

| 日期 | 事件 |
|------|------|
| 2026-05-29 | Fin-Skills.md 入庫(32 個 SK,沒人引用) |
| 2026-07-28 | kaecer 拍板「每日 5 個進修」方針,本方法誕生,SK-01 寫成示範 |
| 2026-07-28 | 規範固化進 `~/.hermes/skills/atlas-skill-inbound/` + 本檔 |
| 2026-07-30 | kaecer 拍板 A 階段:加第四條鐵律「對位 ATLAS_METHODOLOGY.md v1.0」+ 5 HIGH SK 加 methodology_aligned 標 |
| 2026-08-01 | kaecer 拍板 B5 階段(部分) + write_file SOP 強制綁定(避免覆蓋事故) |
| 2026-08-02 22:30 | **kaecer 拍板第五條鐵律「快照值必附 timestamp」新增**(對位 SOUL §0.1 第 6 條邊界);規範 session_count / sharpe / max_drawdown 等隨時間變動的數字引用必附 timestamp + 端點名稱,區分歷史快照 vs 當下值 |
| 2026-08-02 23:25 | kaecer 核准 B 階段 24/24 全部完成(methodology_aligned 對位率 17.9%→100% active) |
| 2026-08-02 23:55 | kaecer 拍板 _consult-index §0 加 2 條規則(§6 觸發點設計 + §6.3 常見問題地圖),鋪路 M4/M5 升分 |
| 2026-08-02 23:59 | kaecer 拍板 M6 規範修改(主動糾正觸發反向達標,kaecer「請自行」紀律落實) |
| 2026-08-03 00:00 | kaecer 開放自主盤查 4 條該做未做全修;v5.2 6.17/10 |
| 2026-08-03 01:35 | A 路徑:2 新 paper(Rosenberg85+Frazzini14)+ validate-timestamp-rule.py(2968B)+ wiki 系統側標;T3-A134/135/136 |
| 2026-08-03 01:40 | ad-hoc 驗證 1.0 = 4 TEST 全過;修 bug「中文段標題不觸發 in_real_run」;T3-A137/138 |
| 2026-08-03 01:50 | 建議 1+2+3 = 109 端點速查卡(7060B)+ 2 paper + audit-atlas-endpoints.py(2408B);**端點 116→109 + M2 8→7.5**;T3-A139/140 |
| 2026-08-03 02:00 | v5.9.1:SK-01 精簡 9571→8796 |
| 2026-08-03 02:10 | ad-hoc 驗證 2.0 = 7 TEST 全過;T3-A141 |
| 2026-08-03 02:20 | 路徑修正(`/private/tmp/`→`/private/var/folders/.../T/`);T3-A142 |
| 2026-08-03 02:30 | **v6.0** = SK-01 加 Chan-Hameed-Tong 2000(7 框架)+ 對位率 90%+;T3-A143 |

## 索引

- 程式本體:`~/.hermes/skills/atlas-skill-inbound/SKILL.md`
- 人類可讀:本檔
- 示範頁:`~/workspace/atlas-wiki/skills/SK-01-factor-library.md`
- 跨頁總表:`~/workspace/atlas-wiki/skills/_inbox.md`
- 來源:`~/workspace/Fin-Skills/Fin-Skills.md`

---

## 重啟後 30 秒回神程序(2026-07-28 kaecer 拍板「不要做了一天兩天就忘記怎麼做」)

每次 session 開頭,無論之前進度到哪,執行以下三步即可回到工作狀態:

```bash
# 1. 載入 atlas-skill-inbound skill(agent 必須)
skill_view name="atlas-skill-inbound"

# 2. 讀本檔,確認規範沒變(若 SKILL.md 更新了,本檔也要同步)
read_file path="~/workspace/atlas-wiki/skills/_method.md"

# 3. 看現況:已寫幾頁、quota 還剩多少、有沒有 _inbox 待辦
ls ~/workspace/atlas-wiki/skills/SK-*.md
cat ~/workspace/atlas-wiki/skills/_inbox.md 2>/dev/null || echo "_inbox.md 尚未建立"
```

30 秒做完上面三步,所有今天拍板的決策都會自動歸位:
- 規範(6 段格式、frontmatter 9 欄、三層驗證)
- 命名(atlas = atlas,不是 atlas-go)
- 路徑(憲法在 `~/workspace/atlas-notes/`,不在 `~/workspace/atlas/`)
- Quota(D1 示範 1 頁 → D2+ 每日 3 頁,2026-07-29 kaecer 拍板降標)
- 精選優先序(SK-01 → 16 → 18 → 20 → 29 第一輪)

**這條規則的權威跟憲法 §1 同級**——可被「禮貌」「怕打擾」覆蓋的話,規範就會被破壞掉。