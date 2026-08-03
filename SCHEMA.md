# Wiki Schema

> **Domain**:散戶 AI 實戰金融工程
> **Owner**:kaecer
> **Maintainer**:hermes agent (MiniMax-M3)
> **Created**:2026-07-15
> **Last updated**:2026-07-15

## 為什麼用「散戶 AI 實戰金融工程」這個名字?

原名「草台班子實戰金融工程」是 kaecer 2026-07-15 拍板的 mission 描述,**但他自己覺得太難聽且容易誤解**,所以改名為「**散戶 AI 實戰金融工程**」。

新名字的三層含義:
- **散戶**:對象是「有軟件專業 + 知道如何善用 AI 的小資金投資人」,**不是機構、不是華爾街**
- **AI**:核心工具是 AI(LLM、Python 工具、資料視覺化),**不是金融工程的數學**
- **實戰**:真實可執行,**不是學術研究、不是教科書**

## 為什麼用 LLM wiki 模式?

從 Karpathy 2026/4 的 LLM wiki gist(5,000+ forks)而來,**3 個月實戰證明對個人研究累積最有效**:
- 不是 RAG(每次從頭合成)
- 不是 graphify(全掃,適合代碼不適合研究)
- 是「**人 + agent 共同策展,人在迴圈**」
- 結果是「**interlinked markdown**,永久累積**」

## Conventions(wiki 建構規則)

### 檔案命名
- **小寫 + 連字號**:`iron-law-3-layers.md` ✅,`IronLaw.md` ❌
- **entity 用實體名**:`l1-t3-five-chains.md`,`deepseek-audit-2026-07-15.md`
- **concept 用概念名**:`signal-light-t1-us.md`,`paradigm-iron-law.md`

### Frontmatter(必填,全檔)

```yaml
---
title: 頁面標題
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [從 taxonomy]
sources: [raw/...]
confidence: high | medium | low       # 草台班子預設 low
contested: true                       # 被推翻過的結論
contradictions: [其他頁面 slug]        # 跟其他頁面矛盾
---
```

### Wikilinks 規則
- **每頁至少 2 個 outbound `[[wikilinks]]`**
- **第一次提到 entity 時才連**(避免 over-linking,這是 LLM wiki 社群已知失敗模式)
- **不連不存在的頁面**(避免 dangling links)

### Confidence 規則(這是「紀律」的核心)

| Level | 含義 | 何時升上去 |
|------|------|----------|
| **high** | 多源驗證 + 歷史實證 + 共識 | 2 個以上 source 都這麼說 + 有 2021-2026 實證 |
| **medium** | 單源 + 邏輯推導 | 1 個 source + LLM 邏輯推理 + 無反例 |
| **low** | 假說 / 直覺 / 推估 | 草台班子預設,任何「**未驗證的觀察**」 |

**核心原則**:**草台班子預設 low,寧可保守也不要樂觀**。
LLM 預設的「**看起來合理**」**不夠**,必須有實證。

### Contested 規則
- 任何結論**被新 source 推翻** → 標 `contested: true`
- 任何兩個 source 對同一件事有矛盾說法 → 標 `contradictions: [其他頁面 slug]`
- **不要默默修改舊結論**,**保留舊結論 + 標 contested + 附新結論來源**

### 「多結論」原則(kaecer 拍板)

> 「在真實世界、真實情況,都是多結論的,只要時空變數一改變,過去說不對的事情,會忽然就變得對或可以用,只是沒有體系。」

**應用到 wiki**:
- 同一個事件,在不同時空可能結論不同 → **保留多個版本 + 標當時的時空**
- 不要「**最後一個觀點覆蓋前面**」
- 用 `time-anchor` 標記每個結論的時空(這是 L1→L2→L3→L4→L5 5 層敘事的核心)

## Tag Taxonomy(必須從這裡選)

### 範式標籤
- `L` — 鐵律(IronLaw,1 天到 18 月,事件必發生)
- `T` — 微趨勢(MicroTrend,0.5-3 年,中等強度)
- `S` — 演化(EvolutionSet,盤整期找反轉點)

### 主題標籤
- `event` — 具體事件
- `template` — 事件模板
- `signal` — 訊號(T1/T2/T3/T4)
- `strategy` — 策略(S1/S2/S3/S4)
- `anomaly` — 異常案例
- `hypothesis` — 待驗證的假說

### meta 標籤
- `audit` — 外部 AI 審計(DeepSeek / Kimi)
- `paper` — 研究論文
- `framework` — 框架文件
- `comparison` — 跨概念比較
- `contested` — 被推翻過的結論
- `time-anchor` — 有時空錨的結論

## Page Thresholds(什麼時候該建 wiki page)

- **Create page**:某 entity/concept 出現在 2+ source,或是某 source 的核心
- **Update page**:新 source 提到已存在的 entity/concept
- **DON'T create page**:只是 source 順帶提到、minor details

## Update Policy(當新 source 跟舊結論矛盾時)

1. **檢查日期** — 較新的 source 通常優先
2. **如果真的矛盾**:
   - 兩邊都保留,各標日期與 source
   - 舊頁面 `contested: true`
   - 在新頁面 `contradictions: [舊頁面 slug]`
   - 在 `log.md` 加 entry「contested detected: 舊頁面 vs 新頁面」
3. **不要 silent overwrite**

## Lint 規則(每週跑一次)

- **Orphan pages**:沒有 inbound `[[wikilinks]]` 的頁面
- **Broken wikilinks**:`[[links]]` 指向不存在的頁面
- **Index completeness**:每個 wiki page 必須在 index.md
- **Frontmatter validation**:每頁有必填欄位
- **Stale content**:90 天沒 update 的頁面
- **Contradictions**:`contested: true` 頁面清單
- **Source drift**:raw/ 的 sha256 變動
- **Page size**:>200 行的頁面(考慮 split)

## 為什麼不裝 graphify?

- 社群實證:graphify 對「**代碼**」是弊大於利(Threads, 2026)
- 我們的 corpus 是「**研究素材**」不是「**代碼**」,graphify 會跑不動
- LLM wiki 已經有 Obsidian Graph View(80% graphify 的功能)
- LLM wiki 的 frontmatter `confidence` + `contested` 是 graphify 沒有的「**不確定性結構化**」機制

## 為什麼 LLM wiki + Obsidian Graph View?

- **LLM wiki** 提供「**interlinked markdown**」+「**frontmatter 紀律**」
- **Obsidian Graph View** 提供「**看見全貌**」+「**互動式瀏覽**」
- **搭配起來** = **手動策展 + 視覺化** = 草台班子最需要的工作節奏

## 致謝

- kaecer 2026-07-15 拍板:mission 改名為「散戶 AI 實戰金融工程」+ 採用 LLM wiki 模式
- Andrej Karpathy 2026-4 LLM wiki gist(5,000+ forks)
- Kunal Ganglani 2026-7 「LLM Wiki Setup」社群實證回饋
- 不用 graphify 的決定來自 Reddit / Threads / CSDN 社群反饋


## 工作時段規則(kaecer 2026-07-15 拍板)

> **排程工作(自動跑)時段**:**凌晨 0:00 - 5:00**(離峰時段,資源/消耗較省)
> **回報工作(等用戶問)時段**:白天

**應用到本 wiki**:
- **Day 2+ 的「拉真實資料、跑 backtest、寫 wiki page」全部排在 0:00-5:00**
- **白天只做**:**回報型工作**(等 kaecer 問、寫簡短報告、被卡住才問)
- **若白天收到「立刻動」指令才動**,否則等凌晨
- **若當日凌晨已完成排程 → 白天不重複做**;只「**回報**」與「**紀律反思**」

**理由**:
- 離峰時段資源便宜
- 拉大量資料 / 跑 backtest 在白天會跟用戶的即時需求搶資源
- 凌晨執行,**白天有結果可呈報**,符合「**高級總監向總裁報告**」的節奏

**例外**:
- **若用戶在白天下達「立刻動」指令** → 不等凌晨,**立即做**
- **若排程卡住** → 不等凌晨,白天就問
- **若發現安全 / 緊急事件** → 不等凌晨,立即回報

## 每日 wiki page 數量限制的真實前提(kaecer 2026-07-19 修正)

> **不是機械式上限**,**是有前提的 token 防暴衝規則**。

### 為什麼有這條規則
- **真正目的**:防止在**未準備、未預期**的情況下突然產生大批 wiki page,造成 token 暴衝、版面膨脹、失去回顧節奏。
- **不適用於**:**已經知道、已經準備、明確要補缺口**的工作。

### 允許 1 天寫超過 1 個 wiki page 的情況
- **(a)已知缺口** — wiki 剛建立/重整,出現**大量馬上可處理的已知工作**,而且**不做會明確拖住後續生產力** → 在 kaecer**知情的情況下**,乾淨把缺口補齊,**不該機械式自踩上限**。
- **(b)對話中產出的高生產力淬鍊** — 在 agent 與 kaecer 對話過程中,**明顯有價值、能直接沉澱的知識** → 不該因為「上限到了」就停手。
- **(c)已知問題立案** — 發現 backend / backend-side 已知問題,必須立刻把「**疑點 + 證據 + repro 步驟 + 接手人**」落成 wiki page,讓 opencode / kaecer 之後接手有完整脈絡。
- **(d)緊急 / 安全事件** — 與前述「工作時段例外」一致,不因 wiki page 數量上限延遲回報。

### 紀律要求(可以破上限,但不能破紀律)
- 寫多頁時,每頁仍要符合 frontmatter + confidence + contested + contradictions 規則。
- 寫完多頁要在 log.md 加 1 條 entry,**誠實標今天寫了幾頁 + 為什麼要這麼多**。
- **不能破紀律**:寫多頁不代表降低 confidence、不標 contested、不列 contradictions。
- **事後不是默許**:若發現寫了「無價值的 page 撐數量」,仍要依 §Update Policy「保留多版本 + 標 contested」處理,**不悄悄刪除**。

### 觸發判斷(給 agent 自己用)
當問自己「現在要不要寫 wiki page」時:
1. **kaecer 知情嗎?** 若 kaecer 下指令、或明確在對話中討論 → 默認允許,不需要特別請示。
2. **這頁是真的有沉澱價值,還是「**為了符合上限的精神**」硬擠?** 若硬擠,改寫進 log.md 比硬開頁更好。
3. **不寫會不會延誤真正的後續工作?** 若會,寫。若只是 nice-to-have,排到凌晨或下次。
4. **token 暴衝的實質風險存在嗎?** 若頁數少且每頁 self-contained,風險極低;若一晚同時建 5 個互相依賴且需要互相 wikilink 的頁面,反而要分批。

> **一句話總結**:上限是用來擋「**失控的全自動生成**」,不是用來擋「**已知的、必要的、有價值的工作**」。
