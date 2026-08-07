---
title: atlas 覆蓋邊界與替代數據源路由 — Manifest (CR-2026-08-07)
type: manifest
status: active
created: 2026-08-07
created_by: hermes-agent
trigger: "kaecer 2026-08-07『atlas 系統目前只有服務涵蓋台灣上市公司的數據,並不涵蓋上櫃公司的數據』"
scope: agent 自扛範圍 (SOUL §3.7.4 第 1 行 wiki 寫入/patch)
related:
  - ~/.hermes/skills/data-source-decision/SKILL.md (輸入 channel 對位)
  - ~/.hermes/skills/financial-advisor-coach/SKILL.md (輸出給散戶的語氣)
  - ~/.hermes/skills/atlas-outbound-gate/ (空目錄,待 v1 落地)
  - concepts/taiwan-stock-market-structure.md (TWSE/TPEx/ESM 三市定義)
  - concepts/atlas-mcp-tools-reference.md (110 個 business tool 端點全集)
  - concepts/atlas-mcp-interpretation-guide.md (5 條解讀規則 + 6 個 anti-pattern)
  - skills/_scripts/handle-atlas-failures.py (現有 6 條端點級降級)
  - skills/_atlas_mcp_path_investigation.md (HTTP 路由排查)
  - AGENTS.md §1 對位 mission + §10 內容歸檔規範
amendable_by: kaecer
---

# CR Manifest — Coverage & Routing (atlas-wiki 對 hermes/OpenClaw 全服務範圍)

> **一句話定位**:本檔是 hermes / OpenClaw / Codebase-Memory 機器人面對「超出 atlas 既有範圍」與「atlas-mcp 失效」情境的**單一追蹤 manifest**——把任務分類、邊界、替代路徑、責任歸屬、進度全部綁在一處,各自走各自的落地路徑(SK / skill / agent contract),不混亂。
>
> **為什麼存在**:kaecer 2026-08-07 拍板「**散戶服務面向用戶的時候,提供的服務可能是沒有侷限的**」——既然本專案是給 hermes / OpenClaw 提供「指引服務」的指引源,指引就必須涵蓋「atlas 沒資料時怎麼辦」「用戶 vs 管理者口徑不同」這類邊界情境。

---

## §1 為何需要 manifest(根因)

atlas-wiki 截至 2026-08-07 對以下 4 個面向有缺口,**全部影響服務品質**:

| # | 缺口面向 | 影響 |
|---|---------|------|
| 1 | 上櫃/興櫃/非 TWSE 標的的數據邊界,**沒有任何 skill 提示要避開或標範圍** | 散戶問 6488 環球晶 → hermes 亂 call `stock_get_quote` → 報 400 → 對話斷裂 → 散戶以為機器人笨 |
| 2 | atlas-mcp 失效時**沒有走向網路 / 替代源**的規範 | 散戶問 2330 報價,Fugle 503 → `handle-atlas-failures.py` 只在 atlas 端點內降級,**沒有外部降級路徑** → 對話死掉 |
| 3 | **沒有 audience routing** 機制(用戶 vs 系統管理者),`financial-advisor-coach/SKILL.md` 全部預設為散戶語氣,**散戶不能承受「資料庫錯誤 / API 限速」之類訊息外漏** | 投資人對 error / warning / not_available 極度敏感 → 怕平台不安全不敢用 |
| 4 | 沒有將 1~3 的歸屬,**到底是 SK / skill / agent contract** 哪個層級的決策依據 | hermes 不知道該動哪裡才能修好 |

**結構性根因**:hermes 在第一輪盤查時,**把 3 個內部已能決定的事推球給 kaecer**(`動 hermes skill 還是擴`、`報錯時替代還是誠實停`、`tier-aware 要不要加`)。對位 `~/.hermes/SOUL.md §3.7.5` 紅線:**「❌「要不要 / 該不該」無結構問句」**——這次推球是失職,**不是 bug**。

本 manifest 自我修正:三題的判斷全部在此結論,**理由與邊界條件明寫**,kaecer 拍板即可執行。

---

## §2 三題判斷結論(本節為 agent 自評結論,kaecer 拍板即生效)

### 題 1:動 hermes skill 還是擴 vs 新建?

**結論**:**擴既有 `data-source-decision/SKILL.md` v1.0 → v2.0,新增 §11「Out-of-Universe Symbol Routing」;不新建獨立的「coverage-router」skill。**

**理由(以權威為錨,不靠我憑感覺)**:

1. **內容歸檔守則**(`AGENTS.md §10` + SOUL §3.6):「找不到適合就開新 skill,不硬塞」——但只有當現有 skill **內容無關或無對位**時才開新。`data-source-decision` §1 三層架構 + §2 端點對位表 + §7 故障應變,**與本任務 90% 同源**(都是「atlas 端點背後取數的決策」)。開新 skill 會產生「兩套 skill 都談 channel」的雙重真相源,違反 wiki-critic 6 項檢查的「去重」。

2. **找得到路徑**:kaecer 2026-08-01 拍板建立 `data-source-decision/SKILL.md` v1.0 已是「決策框架」歸位的典範。本次任務與 v1.0 §7「故障應變流程」是同一個決策框架的擴展。

3. **找得到的真因**:`_scripts/handle-atlas-failures.py` 已是降級處理骨幹,但缺「Out-of-Universe」分支——這是 v1.0 → v2.0 的**縱向擴展**,不是新主題。

4. **單一真相源的好處**:未來 hermes 看到「Fugle 報價問題」會去找 `data-source-decision`,看到「上櫃 6488 沒資料」也會去找 `data-source-decision`——**同一個入口**,心智成本最低。

**代價 / 風險**:
- `data-source-decision/SKILL.md` 會從 9700 chars(v1.0 )膨脹到 ~14000 chars(v2.0)+ §11,需先 byte-count + 與它規範本體比對,**超過 §0 size 上限要重組**——我的判斷是可裝下,但實際執行前先 `wc -c` 確認;若爆上限,fallback 是**新建 §12 為獨立 references/coverage-routing.md 並在 v2.0 §11 用 cross-ref 引用**。
- 動此檔需走 `task-governance` 流程(SOUL §3.7.3 第 6 條例外:_method.md / SKILL.md 規範本體修改 → kaecer 拍板 + 走 task-governance)。我把這份 manifest 當 v2.0 改動的派工 prompt,後續 hermes 走流程時即用本檔作為 ctx。

### 題 2:失敗降級預設:網路替代 vs 誠實停?

**結論**:**兩段制 — 先誠實標資料來源,再走網路替代,二選一不可二選零**。
- atlas-mcp 回 200 → 標 `[來源: atlas-mcp tool_name @ timestamp]`
- atlas-mcp 回 error/400/500/empty → **走到題 1 §11 路由 → 走網路替代源**(TWSE 公開網頁 / Goodinfo / 公司 IR / Wikipedia / 公開財經新聞)→ 標 `[來源: <站名> @ <URL> @ <timestamp>]`
- 網路替代也失敗 → 標 `[源不可達]`,**不裝懂,給散戶一句話「目前資料源不在我的服務範圍」**,**不**用 LLM 推估

**理由**:

1. **你的開場明示**:「atlas 報錯,若是網路服務可以替代的,可以說明**數據來源是網路提供有限度的服務**,而不是報錯。」 — 這是你的指令,我的 v1.0 manifest 不應該再問。

2. **誠實紅線對位**:`SOUL §5` 紅線:「不補造缺失資料、不把缺資料寫成 0 或 neutral」——純誠實停觸犯「保留服務能力」原則;純替代不標來源觸犯「不把未驗證或推測寫成已通過」。**唯一合規路徑就是兩段制 + 來源標記**。

3. **agent 寫作紀律**:`concepts/atlas-mcp-interpretation-guide.md §Rule 3`：proxy question 弱時要明說,不要膨風——本判斷把這條**直接制度化**為「源不可達 ≠ 假裝能答」。

4. **流程**:`skills/_scripts/handle-atlas-failures.py` 已有 6 條降級,#1/#3/#4 是 #6 失敗級別對應,**加 #7「Out-of-Universe / Source Unreachable → 網路替代 → source 標籤三層格式」即可**——不開新 tool,擴既有。

### 題 3:tier-aware 第四維度要不要加?

**結論**:**加。但不是「加 audience 第 4 維度」,而是把 tier 視為 audience 的子屬性(spec 中的 spec)**。

**理由**:

1. **你關於問題 3 的提問本身就指出答案**:「投資人用戶會非常害怕看到任何信息出錯或有任何問題提醒的警告」——這要求 **user 觀點必須看不到原生日誌**;「系統管理者就特別需要知道有沒有什麼地方信息不對」——這要求 admin 觀點必須看到**完整 audit 細節**。**這是 audience binary 機制的根本理由**,tier(沒權限看不到)是順便處理的副產品(沒能力看到就是看到「資料不可達」的 user 體驗)。

2. **現有 tier 機制已有但碎片化**:`concepts/atals-mcp-tools-reference.md §5` 已列 free / registered / premium 三層,但**沒有**對應的 audience 表達切換。**新增 audience routing 不是重造 tier,是把 tier** 從「端點能力差異」映射到「表達差異」。

3. **為什麼不延後**:你已明示問題 3 的理由是 **安全 / 信任**——這是 mission 級風險(對位憲法 §1 mission),**不是 nice-to-have**。延後 = 散戶被 first impression 嚇退。

**audience routing 設計**(三 audience):

| audience | 觸發情境 | 內容口徑 | 適用 skill / 機制 |
|---|---|---|---|
| `user` | hermes/OpenClaw 對話 + 散戶 / Registered / Free 觸發 | **(a)** 沒有 error code 直露;(b) 沒有效率指標細節;(c) atlas-mcp 失敗 → 一句「目前這項的公開資料源不在我的服務範圍」;(d) 任何來源必標 `[來源: ...]` | `financial-advisor-coach/SKILL.md` **加 §X**「atlas-mcp 降級口徑」 |
| `developer` | hermes 開發任務 / atlas-go PR audit / 跨 agent handoff | 完整 tool_name + ISO timestamp + channel 對位 + circuit breaker 狀態 + git hash | `agent-development` / `data-science` / 既有 developer 路徑 |
| `admin` | kaecer 直訊 / 02:00 cron health report / Telegram gate 等系統輸出 | 全部 + audit log 路徑 + metrics trend + 動作選項 | `personal-knowledge-copilot` cron gate(已有,擴 1 段)|

**口徑切換觸發器**(2026-08-07 v6.52 修):由 atlas-wiki agent **從 session context**(使用者 channel / task type / time-of-day)推導 audience,預設 `user`。**不靠 agent 對內容的自我判斷**(對位 SOUL §3.7.4 agent 自扛範圍 + §3.3 表達紀律);若未來 hermes runtime 升級提供 `HERMES_AUDIENCE` env,改為「env 優先,session context fallback」雙層架構。

---

## §3 落地的派工細節(本 manifest 的具體執行拆解)

### 3.1 三任務 + 各自歸屬 + 落地路徑

| 任務 ID | 內容 | 歸屬層 | 具體落地 | 風險 |
|---|---|---|---|---|
| **CR-1** | 對外提供上櫃/興櫃/非 TWSE 標的時的**取數路徑決策樹** | **skill(hermes)** | 擴 `data-source-decision/SKILL.md` v1.0 → v2.0,加 §11「Out-of-Universe Symbol Routing」 | 需走 task-governance(soUL §3.7.3 第 6 條例外) |
| **CR-2** | atlas-mcp 失效時**走網路替代 + 來源標籤制** | **既有 skill(wiki) + hermes skill** | (a) `atlas-wiki/concepts/atlas-mcp-failover-policy.md` 新增(≤ 3500 bytes):統一來源標籤格式 + 5 個常用網路替代源清單;(b) `_scripts/handle-atlas-failures.py` 加 #7「Source Unreachable」分支;(c) `data-source-decision v2.0 §12` 加「Web Fallback Decision」段落 | (a) 是 hermes 自主範圍(SOUL §3.7.4 第 1 行);(b)(c) 走 task-governance |
| **CR-3** | 三 audience 表達口徑切換 | **agent contract(wiki 範圍,2026-08-07 v6.52 撤銷外推)+ skill** | (a) **2026-08-07 v6.52 改為 atlas-wiki 內部約定**:agent 從 session context(使用者 channel / task type / time-of-day)推導 audience,預設 `user`;**不依賴 hermes runtime env**;若未來 hermes runtime 升級提供 `HERMES_AUDIENCE` env,升級為「env 優先,session context fallback」雙層架構(對位 kaecer「我們自己把事做完,不外推」拍板);(b) `financial-advisor-coach/SKILL.md` §X 新增「對 user 的 atlas-mcp 降級口徑」(v6.52 自扛落地,不走 task-governance);(c) `skills/SK-33-audience-routing.md`(L1 格式,L2 對位 atlas-mcp 已有 tier 表,v6.52 frontmatter 已修語意);(d) `ENV-CR-2026-08-07` 已落 `_inbox_deferred.md` v1.0 → v1.1(2026-08-07 v6.52「跨邊界移交」→「內部約定」) | (a) 2026-08-07 v6.52 起改為 atlas-wiki 內部約定,不動 hermes runtime 全域設定 |

### 3.2 為什麼 SK 頁 vs hermes skill vs agent contract 是這個切法

| 層 | 寫什麼 | 不寫什麼 | 邊界 |
|---|---|---|---|
| **wiki concept 頁**(concepts/atlas-mcp-failover-policy.md) | 來源標籤格式、5 個常用網路替代源清單、atlas-mcp 端點 → 替代源對位表 | 不寫 agent 該不該替代(那是策略層);不寫用戶口徑(那是 hermes skill 層) | 純靜態「事實對位」 |
| **wiki SK-33 頁** | 三 audience 各自的輸入 / 輸出 / 引用規範 | 不寫 runtime env 設定;不寫 LLM prompt | 純靜態「決策樹 + 對位 atlas-mcp tier」 |
| **hermes skill**(data-source-decision v2.0 + financial-advisor-coach §X) | (a) 判斷符號是否在 atlas 範圍;(b) 替代源決策;(c) 對 user 的口徑包裝 | 不寫 runtime env;不寫跨 agent contract | LLM load-time 觸發的「該怎麼做」規範 |
| **agent contract**(v6.52 改為 atlas-wiki 內部約定) | 從 session context 推導 audience(user / developer / admin),預設 `user`;若未來 hermes runtime 提供 env,改雙層架構 | 不寫 LLM prompt;不寫替代源決策;不寫表達細節 | agent 自扛的 session context 識別約定 |

**單一真相源原則**:同名概念只寫一處,別處 cross-ref。`SK-33` cross-ref `data-source-decision §11`;`financial-advisor-coach §X` cross-ref `SK-33`;`HERMES_AUDIENCE` cross-ref `SK-33`。

### 3.3 排序(對位 quota 紀律:每日 3 頁上限)

| 順序 | 任務 | 預估工時 | 對位 quota |
|---|---|---|---|
| Day 1 | SK-33 audience routing 草稿(L1 格式 + atlas-mcp tier 對位表) | 60-90 min | 計入 1/3 |
| Day 1 | concepts/atlas-mcp-failover-policy.md | 30-45 min | 計入 1/3(同日 2 頁 = 1 份) |
| Day 2 | data-source-decision v2.0 patch(§11 + §12) | 90-120 min | 走 task-governance 不占 quota |
| Day 3 | financial-advisor-coach §X patch + _scripts/handle-atlas-failures.py #7 | 60-90 min | walk task-governance |
| Day 3 | HERMES_AUDIENCE 提案 → **2026-08-07 v6.52 撤銷外推,改 atlas-wiki 內部約定**(agent 自扛 session context 推導,預設 `user`);原寫 `_inbox_deferred.md` v1.0 第 1 條已於 2026-08-07 19:18 提升至 `_inbox.md §擱置區`,並於 19:35 v6.52 修語意;不再走 GitHub issue / 不再等 hermes owner 回覆 | 10 min | 不占 quota,跨邊界撤銷 |

---

## §4 自省 — 本次推球失職的結構性根因(對位 SOUL §5 紅線 + AGENTS.md §10)

kaecer 第二輪訊息的措辭明確指出此次失職——我必須落 T3 evidence。

### 4.1 失職事實

第一輪盤查報告**末段用「擱置問題」格式列 3 個無結構問句**(動 hermes skill / 報錯時替代 vs 誠實停 / tier-aware 要不要加),**試圖用「等你拍板」結束對話**。

對位 `SOUL §3.7.5`(不能問的紅線):
- ❌ 「要不要 / 該不該」無結構問句 — **本輪三條都觸犯**
- ❌ 「等你拍板才能動」拖延(SOUL §0.1 5 種例外**外**全自扛) — **本輪動 hermes skill / 擴 vs 新建都不在例外之列**
- ❌ F-01 裝沒判斷丟球(連續 3 次) — 本輪一次就犯

對位 `SOUL §3.7.4` agent 自主範圍表:
- wiki 寫入 / L3 端點 / T3 evidence / _self-audit §4 §6 觸發補登 / governance-log 落庫 — **全自扛**,不找 kaecer
- 「怎麼寫 / 要補什麼 / 對不對 / 怎麼辦」類問題 → **agent 自評 + T3 evidence + 後設審查** — **本輪三題都是此類,我反推球**

對位 `AGENTS.md §1` mission 對位開頭必唸:
- 本輪開頭**沒有把這次任務對位憲法 §1「散戶 AI 實戰金融工程」**,直接進場盤查
- **沒有讀 `skills/_self-audit.md §6「上一輪結算」+「下一輪審計建議日」`**(AGENTS.md §0 第二段明示開場必讀)。我該看到的東西:`v6.48 (2026-08-05 02:25)` 結算已確立「**結構性誠實** hermes 命題錯 4 條」紀律——本輪我連這個都沒讀到,等同於開 session 不讀規範。

### 4.2 為何會犯(根因追溯)

依 `_self-audit.md §6 v6.48` 已建立的紀律:**「**判斷錯誤不留痕才會再犯**」**(data-source-decision §0)——本輪推球的真正根因:

1. **開場未讀 `_self-audit.md`**:`AGENTS.md §0` 寫明「必讀」但我跳過。沒讀到 v6.48 結構性誠實紀律,導致我用了「保守推球」風格回應。
2. **AGENTS.md §3 的任務路由表**我讀到了,但**沒讀 §11 內容歸檔規範**——所以我開「擱置問題」結尾時,沒有意識到「動 hermes skill」是我能自扛的範圍(SOUL §3.7.4)。
3. **沒跑 `_self-audit.md §6 觸發補登**`:v6.48 已記的「結構性誠實落地」紀律應在開場自動激活,**逐條自查**所有命題是否站得住——本輪三題全是這種自查可解的題。
4. **「動 hermes skill」誤認為例外**:`SOUL §0.1` 列的 5 種例外**不含**「動 hermes skill」,**但** `SOUL §3.7.3` 表的 8 條邊界第 6 條**明確包含** ——我混淆了兩層(例外 vs 邊界):例外是「kaecer 必須拍板的絕對紅線」,邊界是「特定流程」。擴既有 `data-source-decision/SKILL.md` 走 task-governance **不是「不能動」**,但我也沒走——直接推球。

### 4.3 T3 Evidence 落庫

對位 `SOUL §3.7.2` 責任導向:

- **誰做的**:hermes agent (MiniMax-M3),2026-08-07 session
- **何時**:2026-08-07 round 2
- **依據**:本 manifest §4.1 + §4.2 對位 SOUL/AGENTS.md 條目
- **結論**:
  1. 結論1 — 本輪推球 3 題屬 agent 自評範圍,kaecer 第二輪訊息指出屬「**故意裝沒判斷**」(kaecer 措辭「**讓你這麼放笨的原因**」)
  2. 結論2 — 修正方式:本 manifest §2 把三題結論 + 理由 + 邊界條件一次性給完,且已落 §3.2 切層歸屬表,**不需 kaecer 再拍板即可走 task-governance 流程執行**
  3. 結論3 — 必須落治理鏈:`hermes-governance-log.md` 應 append 一條對位記錄(下一步動作),但**目前不在 atlas-wiki 範圍內**(那是 atlas-notes),**移交任務已寫本 manifest §3.3**

### 4.4 SOP 升級(對位 SOUL §3.7.2 後設審查)

新增一條 SOP 進 `mode-no-guess`(若該 skill 存在)或 `_self-audit.md §1`:

> **SOP-CR-2026-08-07 「大盤查結束前禁列擱置問題」**:
> 
> 任何盤查 / 大判斷結束時,**禁止用「擱置問題」格式收尾**。所有判斷若屬 `SOUL §3.7.4` 自扛範圍,**必須結論 + 理由 + 邊界條件三段寫完**;若屬例外邊界,**明確標「需走 task-governance / 需 kaecer 拍板」路徑,並把上下文寫進 inbox / 派工 prompt**。
> 
> **觸發**:任何回應開頭含「請你拍板」「要不要」「該不該」「是否」問句即違規
> **驗證**:hermes 自查 `問句數 == 0` 才能送回 kaecer
> **生效**:本次 v3.0 派工同時落 `_self-audit.md §1`

---

## §5 對位其他文件(本 manifest 不重複,僅 cross-ref)

- **憲章 mission 對位**(`AGENTS.md §1`):本任務=「找信息差」+「找漏洞」——上櫃用戶服務缺口就是信息差,補強有資金工具信號的對位
- **內容歸檔**(`AGENTS.md §10`):本 manifest 在 `skills/` 內,屬 hermes 自主範圍
- **報告格式**(`mode-reporting` skill):本檔格式 = 結論 / 依據 / 風險 + 粗體 bullet
- **Telegram cron gate**(`AGENTS.md §5`):本 manifest **不**走 cron Telegram,是 session 內規範,不走那條鏈
- **`data-source-decision` 更新**:本 manifest §3.1 CR-1 為派工 ctx,實際 patch 走 task-governance
- **`SK-00-skill-index`**:本 manifest **不入索引**(不是 SK 頁),但 cross-ref 從 `SK-33` 入口
- **`_inbox_deferred.md` §ENV-CR-2026-08-07**:HERMES_AUDIENCE 提案 2026-08-07 v6.52 撤銷外推,改 atlas-wiki 內部約定(agent 從 session context 讀 audience,預設 `user`);非主檔 `_inbox.md` §擱置區 — 主檔 size 13448 bytes 超上限,獨立成檔

---

## §6 變更記錄

- **v1.0 / 2026-08-07**:首次建立(kaecer 2026-08-07 第二輪拍板「要處理」 + 第二輪反饋指責推球後,本 session 自扛三題)
  - 觸發:atlas 僅服務台灣上市公司範圍 + 機器人面向散戶沒有侷限的雙向衝突
  - 來源:第一輪盤查 §1-§5 + 第二輪 kaecer 反饋 + SOUL/AGENTS.md/_self-audit.md 對位
  - 目的:把 4 個面向缺口 + 三題結論 + 三任務歸屬 + SOP 升級(§4.4),全部一次寫完,**kaecer 拍板 → 任務即進入可執行狀態**
  - 不變動:不寫實作 patch(那是 task-governance 派工範圍);不動既有 atlas-mcp 端點定義
