---
title: atlas-mcp 工具解讀指南
created: 2026-07-15
updated: 2026-07-15
type: concept
tags: [framework, signal, methodology]
sources:
  - "外部來源: hermes skill mcp-tool-interpretation (2026-07-15 讀)"
  - "外部來源: hermes skill mcp-server-integration"
  - "外部來源: ~/workspace/atlas/cmd/atlas-mcp/README.md"
confidence: high
contested: false
contradictions: []
---

# atlas-mcp 工具解讀指南

> **一句話**:**atlas-mcp 給的是「資料」,我(MiniMax-M3)給的是「判斷」**。MCP 層資料是必要不充分條件 — 沒有資料不能判斷,但有資料也未必能判斷。

這是 2026-07-15 從 hermes 的 `mcp-tool-interpretation` skill 學到的工作紀律。

---

## 為什麼這個指南存在?

之前 v0.4 訊號燈階段我犯過:
- 把 MCP 工具回傳的數字**直接搬給用戶**(bullet dump anti-pattern)
- 把 model 的 0.5 confidence 解讀成「有 50% 機率」(其實是「**不知道**」)
- 多個 tool 同意就推「all-in」(其實是同一個 model 用不同管道在講話)

這些都是 `mcp-tool-interpretation` skill 明確警告的 anti-pattern。

---

## 5 條解讀規則(每次用 MCP 前必讀)

### Rule 1 — 診斷 before fetch
**先答這 3 個問題再 call tool**:
1. **用戶實際要決定什麼?**
2. **「好答案」長什麼樣?(10 分鐘後他會用這個答案做什麼?)**
3. **最低證據是什麼?**

**如果答不出來,先問用戶澄清問題,不要亂 call tool**。
**Tool calls 不是進度,是證據蒐集。沒有問題的證據是浪費。**

### Rule 2 — 引用改變判斷的數字,其他不搬
只有這 3 種數字該出現:
- **(a) 定錨判斷的數字**(「stress index 17 = regime low,不是 moderate」)
- **(b) 反直覺的數字**(「地緣 component 13 = 主導風險不是 selloff 是 tail event」)
- **(c) 用戶實際想要的數字**(具體日期、具體代號)

其他「看起來厲害但不改變決策」的數字 → audit log,不要 response。

### Rule 3 — 明說 tool 答的是 proxy question
| 用戶問 | Tool 答 | 真正意思 |
|------|------|------|
| 「下週會不會漲?」| `event_flow_prediction` confidence 0.5 | **model 自己不知道**。不要美化 |
| 「2330 該不該進?」| `stock_get_quote` + `stock_get_chips` | 末升段 + 散戶擠兌 ≠ 自動買 |
| 「哪個 strategy 最好?」| `strategy_ranker` 分級列表 | free/registered/premium 是商業分級,不是訊號強度 |

**Proxy answer 弱時要明說,不要膨風**。

### Rule 4 — 永遠 3 段結構(證據 / 我的解讀 / 沒把握的)
- **Raw evidence**:錨定下一步的最低引用
- **My reading**:「我注意到 X 暗示 Y,跟 headline 反過來...」
- **What I'm NOT confident about**:「stress index 的 components 可能 mis-weighted,event expiration 7/17 沒校正」

**用戶能修我中間那段(我的解讀),修不了我給的一大堆 data。**

### Rule 5 — 永遠提供 meta-loop
結尾必須有:
- **澄清問題**(「你的時間尺度是一週還是一季?」)
- **或 offer 深入**(「要不要我把這幾條 chain 拉出來 + historical hit rate 對照?」)

**只回答「半導體看好」然後停 = 用戶必須一直 re-prompt。**

---

## atlas-mcp 工具解讀細節(2026-07-15 從 notes 整理)

### `event_flow_prediction`(5 日預測)
- `direction: "neutral"` + `confidence: 0.5` = **沒訊號**。**明說「backend 不承諾方向」**。
- `confidence: 0.7+` = model 在 commit。**仍然要 hedge**(歷史相似事件樣本可能很小)
- `predicted_forces: []` = 空。**model 沒看到 driver,或 driver 的 tag 不在 force vocabulary**。**用 `narrative_get_events` 確認**。

### `macro_get_stress_index_current`
- **Regime bands 是 non-linear**:**「low」≠「沒 stress」**。數字比 label 重要。
- **Component breakdown > 總分**:**一個 component(例 `geopolitical: 13`)可能主導,total 看起來是「low」**。永遠 surface 哪個 component 佔比最大。
- **對照 `narrative_stress_index_thresholds`**:知道單一 component 是否在 alert territory。

### `regime_get_history`
- **Regime flips 是 episodic,不是 continuous**。**一天多次 micro-flip(RISK_ON → RISK_OFF 每 2 秒) 是 data-quality 或 replay artifact,不是市場現實**。**看到這個要在引用 regime 前先提**。
- **Current regime 才是用戶決策用的;history 是看「穩定度」**。

### `narrative_get_bundle`
**這是最豐富的 tool**,每個 entry 有:
- `events[]`:active narrative events with `confidence`, `hit_rate`, `expires_at`。**`expires_at` 是黃金欄位** — 告訴你「**conviction 何時到期**」。**`event_flow_prediction` 的日期要跟 `expires_at` 對照**。
- `chains[]`:causal chains。每個有 `affected_sectors` + `avoided_sectors` + `score`。**多個 chain 在同 sector 重疊 = 訊號比單 chain 強**。
- `models[]`:weighted interpretation models。**`weight` 是 model 當前在 meta-model 的 allocation。`recent_error` 告訴你「最近錯多兇」**。**高 weight + 高 recent_error 的 model 不要信**。
- `seasonal`:monthly/seasonal packets with `historical_accuracy`(0-1)。**`expectations[]` 的 `already_priced_in` 旗標**告訴你「**這個 season 預期了,但市場還沒 priced in**」 — 這是 contrarian 訊號。
- `templates[]`:可重複使用的 cause-effect templates,**含 references**(Ball & Brown, BIS, Hamilton 1983 等)。**當 template 的 `required_region` 跟 active event 的當前 `region` 吻合 → template 強化訊號**。

### Capital flow tools
- `capital_flow_summary`:7 forces with `raw_value`, `trend`, `z_score`。**只有 z-score 是訊號,raw values 雜亂且不能跨 force 比較**。
- `quality_score` ≥ 0 = model 願意為 decomposition 背書;= 0 = decomposition 是 noise。

### Stock tools (`stock_get_*`)
- `stock_get_quote` 需 server 端 FUGLE_API_KEY。**如果返回空,是 server 端 config 問題,不是 agent 的問題**。
- `stock_get_technical` 是 days-bounded(max 365)。**多月趨勢用 days=180 或 365**。
- **Symbol normalization server 端處理**(per `docs/specs/stock-api-contract.md`,4-6 位 TWSE codes)。**不要預先 normalize**。

---

## 三層 framework(MCP 層 / 學術層 / barbaric signals 層)

**完整答案需要 3 層,不是只有 MCP 層**:

1. **MCP 層**:結構化資料告訴你什麼(atlas regime, narrative, stock quotes)
2. **學術層**:peer-reviewed 說什麼(2-5 年 lag)
3. **Barbaric signals 層**:活的非學術世界在做什麼(央行買金 / OFAC 制裁 / 衝突事件 / 商品流 / 政策扭曲 / 財富集中)

**Pairing rule**:**6 個月 forward 問題,lead with MCP reading,但永遠 cross-check 學術 + barbaric signals**。

**範例**:
- MCP 說 RISK_ON
- 學術說 HMM transition probability rising
- barbaric 說央行買金創高 + OFAC 升級
- **真實答案不是「RISK_ON is fine」**
- **真實答案是「MCP 層 RISK_ON,但 barbaric 層在閃,淨讀是『RISK_ON with a tail risk MCP 看不到』」**

**Anti-regularity check**:**Papers summarize the mean。用戶的 edge 在 tail**。**送 MCP-based 答案前先問:「MCP reading 跟 consensus 學術觀一致嗎?若一致,consensus 哪裡可能錯?」**然後看 barbaric signals 看 consensus 是否被 live data 挑戰。

**kaecer 偏好**:「**散戶 AI 實戰金融工程**」= **barbaric signals 層為主,不是學術層為主**。「**學術綁死就不用玩了**」。

---

## 6 個 Anti-patterns(絕對不做)

1. **Bullet-Point Dump** — 把所有數字列給用戶(terminal 比 agent 快)。如果不能 add reading,**停下,問用戶實際要決定什麼**。
2. **Pseudo-Quantitative** — 「81% 命中率代表下週半導體大概會漲」(**錯**)。要寫成:**「if 條件 X 持續,81% historical hit rate 說條件相似時 semi-tilted exposures historically outperformed — 條件是 regime 不 flip,而 7/17 是 AI Capex event 過期日」**。
3. **無 Context 的答案** — 「下週偏正向,但不強烈」— 對持 70% 小型股的人 hedge 的人不知 regime 是什麼的人都沒用。
4. **Over-Citation Cover** — 引用 `narrative_get_bundle` 內部欄位名 = 假裝在思考。**translate 成 plain claims + 引用理由**。
5. **忘記用戶 Loop** — 寫完不問下一步 = 失敗。**Build loop backwards from 用戶的下一個問題**。
6. **Polling health tool** — 連續 call 5 次 `system_get_health` 期待 stale channel warning 改變 = 失敗。**Health tool 是 clue generator 不是 verification endpoint**。**去看 source code / underlying system**。

---

## 「**解讀**」與「**翻譯**」的根本差別

| | 翻譯(失敗模式) | 解讀(成功模式) |
|---|------|------|
| 角色 | 搬運工 — 把 tool 輸出變中文 | 廚師 — 給用戶一道菜 |
| 輸出 | 6 個 tool call + 1 個 Markdown table | 「regime=RISK_ON 但 geopolitical component 13 在 alert,淨讀 RISK_ON with tail」 |
| 用戶行動 | 還要自己讀 | 看到判斷可以立刻決策 |

**用戶付 agent 錢,是付「**synthesis**」,不是付「**parallel structured-data fetching**」**。

---

## Confidence 標記說明

| 段落 | Confidence | 原因 |
|------|------------|------|
| 5 條規則 + 6 個 anti-patterns | **high** | hermes skill 官方文件,社群共識 |
| atlas-mcp 工具細節 | **high** | 從 hermes 的 `atlas-mcp-interpretation-notes.md` 整理,設計上對位的 notes |
| 三層 framework | **high** | skill 明確寫的「用戶付 synthesis 不是付 fetching」 |
| 我的 anti-pattern 反思(v0.4 階段)| **medium** | 我自己有犯過,但沒系統化清單 |

---

## 待驗證的假說

- [ ] 5 條規則在台股研究中的「實戰可用度」需要看 1-2 個真實案例
- [ ] 三層 framework 在 6 個月 forward 問題中是否真的比單 MCP 層準?
- [ ] 我的 v0.4 階段犯的 anti-pattern(特別是 bullet dump)是否還會重犯?

---

## 相關 entities / concepts

- [[concepts/t1-t4-signal-light]] — T1→T4 訊號燈四層驅動結構
- [[concepts/s-paradigm-redefinition]] — S 範式重新定義
- [[entities/l1-t3-five-chains]] — L1-T.3 五鏈耦合鐵律

---

## 來源

- hermes skill: `mcp-tool-interpretation/SKILL.md`
- hermes skill: `mcp-tool-interpretation/references/atlas-mcp-interpretation-notes.md`
- hermes skill: `mcp-server-integration` (未深入讀,Day 2-3 視需要)
- 外部: `~/workspace/atlas/cmd/atlas-mcp/README.md`(atlas-go 官方)
