---
title: atlas 諮詢索引 — 散戶問題 × Fin-Skill × atlas-mcp 端點
type: consult-index
purpose: 散戶問金融問題時,先查這檔決策錨,知道走哪條 atlas-mcp + 哪個 Fin-Skill
created: 2026-07-29
created_by: hermes-agent
ground_truth_basis: |
  - ~/workspace/atlas/ (atlas-mcp backend,唯讀)
  - ~/workspace/Fin-Skills/Fin-Skills.md (32 SK)
  - atlas-mcp 端點實跑驗證 2026-07-29：
    * backtest_signals → sharpe_long/short、VaR、active_signals
    * risk_get_metrics → max_drawdown_pct、insufficient_data、session_count
    * industry_sector_lookup → 半導體(class 12 支同業)
status: active
related:
  - ~/workspace/atlas-wiki/skills/_index-finskills.md
  - ~/workspace/atlas-wiki/skills/_method.md
  - ~/workspace/atlas-wiki/skills/_inbox.md
---

# atlas 諮詢索引

> 設計目標:未來任何金融問題,我都能在這張表找到「問題分類 → 哪個 Fin-Skill 對位 → 哪個 atlas-mcp 端點驗證 → 給散戶的語言」四欄。
> 不是 SK 的索引,是「問題的索引」。

---

## §0 使用規則

1. 散戶進問題 → §1 找分類 → §2 找「核心 SK」 → §3 找「atlas 端點」 → §4 找「散戶語言」
2. 若問題跨多個分類,依**首要關切**入主分類,次要分類在「附加」欄標
3. 若 §1 找不到:擴張到 §5「未分類問題」工作流,找新端點並補登
4. 每跑完一題,於 §6「諮詢紀錄」追蹤,作為後續 SK 寫入優先序依據
5. **§6 觸發點設計(2026-08-02 23:55 kaecer 拍板鋪路)**:§6 真實對話紀錄觸發需「**kaecer 真實詢問散戶問題**」(USER §7「事實撒謊修不了」+ SOUL §5「不補造缺失資料」);**agent 不可編造對話紀錄**;觸發 1 筆後即啟用 §6 紀錄,作為 M4/M5 升分依據
6. **§6.3 常見散戶問題清單(2026-08-02 23:55 kaecer 拍板鋪路)**:預期散戶常見 6 大類問題(Q1~Q6),列示每類典型問句 + 對位 §1~§4 的查詢路徑;**這是「預期查詢地圖」不是「已答對話」**;觸發真實對話時直接對位 §1~§4 即可

---

## §1 問題六大分類

散戶的金融問題,大致落這六類:

| 代號 | 分類 | 核心關切 | 一句話特徵 |
|------|------|---------|-----------|
| **Q1** | 個股基本判斷 | 這支會不會再漲/跌? | 提到具體股票代號/名稱 |
| **Q2** | 多空/選股策略 | 怎麼挑股?做多做空怎麼配? | 提到 top/bottom、十分位、因子、Alpha |
| **Q3** | 產業/類股輪動 | 哪個產業現在值得進? | 提到半導體/金融/航運、產業代碼 |
| **Q4** | 風險/回測 | 這策略穩嗎?會不會大虧? | 提到回測、drawdown、夏普、VaR |
| **Q5** | 宏觀/事件 | 現在是空頭還是多頭?有什麼大事? | 提到美股、聯準會、台股大盤、事件 |
| **Q6** | 交易實務 | 該扣多少成本?怎麼算實際報酬? | 提到手續費、證交稅、滑價、淨報酬 |

---

## §2 每個分類對位的 Fin-Skill(以 HIGH 優先)

| 分類 | 核心 SK | 附加 SK | 已落地 SK(2026-08-02) | 為什麼這幾個 |
|------|---------|---------|----------------------|--------------|
| Q1 個股 | SK-01(因子庫) | SK-09(PLS) | **SK-01** (active,2026-08-02 v0.9 升;data_get_field_contract 41 欄位已對位) | factor library 是個股分析底層,PLS 監督式降維 |
| Q2 選股 | SK-16(多空十分位) + SK-18(因子 Alpha) | SK-13(排列重要性)、SK-22(消去法,**實驗級 metric delta 已對位 PR #1443 2026-08-02,但 by-factor 仍對位失敗,僅作 Fin-Skill 概念參考**) | **SK-16**、**SK-18** | Q2 是 mission「找漏洞」直接入場點 |
| Q3 產業 | (待補) | SK-23(產業輪動 env),但 LOW 暫不啟動 | — | atlas 端點強(industry_sector_lookup),但 Fin-Skill 對位薄 |
| Q4 風險 | SK-29(滾動回測) + SK-18(Alpha 風險調整) | SK-20(規模分組穩健)、SK-21(仙股排除) | **SK-29**(active,v3.1 升,risk_get_drawdown 雖 not_available 但端點活+七時期對位已寫)、**SK-18**(active,v0.9 升)、**SK-20**(active,v0.9 升,industry_sector_lookup + stock_get_quote + stock_get_fundamentals 三端點全跑通) | Q4 必須先有回測,才有穩健/風險 |
| Q5 宏觀 | (atlas 端點為主) | SK-25(獎勵函數),LOW 暫不啟動 | — (atlas macro 端點為主:macro_get_snapshot_latest ✅ / narrative_get_events ✅ / taiwan_stress_index ✅ **-9.33** low,**mcp_quickstart.stress_index ✅ -7.90** low 為另一口徑,2026-08-02 20:11 實跑;**crossmarket_get_us_indices ✅ 4 指數 + 4 科技股**;**mcp_quickstart ✅ 12 strategies + 5 events**) | 這類問題 Fin-Skill 沒對位,直接吃 atlas macro 端點 |
| Q6 成本 | SK-19(交易成本與稅務調整) | — | **SK-19** (active,2026-08-01 v0.9 升;backtest_signals + risk_get_metrics + report_get_tax_snapshot 三端點全跑通) | 唯一直接對位 |

**問題: Q3 與 Q5 的 Fin-Skill 對位薄**
- Q3(產業輪動):atlas-mcp `industry_sector_lookup` 強,但 Fin-Skills 只有 SK-23(LOW、需 RL 框架才有用)
- Q5(宏觀):Fin-Skills 整套沒對位,直接吃 atlas `macro_get_snapshot_latest` + `narrative_get_events` + `stress_index_*`
- 這兩塊用 atlas 端點強過用 Fin-Skill,所以「諮詢」時不該為了對位而對位

---

## §3 atlas-mcp 端點字典(已實跑驗 2026-07-29)

### Q1 個股基本判斷
`stock_get_quote` 報價、`stock_get_fundamentals` 基本面、`stock_get_technical` 技術面、`stock_get_chips` 籌碼面、`industry_sector_lookup` 產業

### Q2 選股策略
`backtest_signals` 多空、`risk_get_metrics` Alpha、`universe_get_sessions` 模擬

### Q3 產業輪動
`industry_sector_list` 清單、`industry_sector_lookup` 找產業

### Q4 風險/回測
`risk_get_metrics` 指標、`risk_get_commentary` 解讀、`backtest_signals`+`universe_get_sessions` 回測

### Q5 宏觀/事件
`macro_get_snapshot_latest` 快照、`narrative_get_events` 事件、`taiwan_stress_index` 壓力、`crossmarket_get_us_indices` 美股、`mcp_quickstart` 速覽

### Q6 交易成本
(無端點,套 SK-19 公式)

> 詳見 [[concepts/atals-mcp-tools-reference]] [2026-08-22 audit-fix]

> §3.1 方法論憲章對位表已歸檔 → [[_consult-index_archive.md]]（2026-08-22 audit-fix,對位 _inbox 第七條例外模式）

> §3.2 端點底層 channel 對位表已歸檔 → [[_consult-index_archive.md]]（2026-08-22 audit-fix,對位 _inbox 第七條例外模式）

---


## §4 散戶語言對應錨(GROW+ 引用點)

### Q1 個股 — 一句話定位法
> 「這支的 **位置**(在產業裡誰)、**動能**(技術面)、**籌碼**(法人買不買)三軸交叉看,不能只看一個。」

### Q2 選股 — 一句話定位法
> 「做多 top 10% / 做空 bottom 10%,先讓策略在歷史上能跑贏,再看現在訊號有沒有亮。」

### Q3 產業 — 一句話定位法
> 「進場看產業有沒有在 leader 位置,出場看 leader 有沒有換人。」

### Q4 風險 — 一句話定位法
> 「單筆最大能虧多少(回撤)比賺多少更重要。先求不破產,再求賺錢。」

### Q5 宏觀 — 一句話定位法
> 「壓力指數高時不要 heavy position。事件來時新聞要看,但 action 不一定要動。」

### Q6 成本 — 一句話定位法
> 「台股買賣各扣 0.1425% 手續費 + 賣扣 0.3% 證交稅,頻繁進出會被吃掉,要看淨報酬不是毛利。」

---

## §5 未分類問題工作流

§1 找不到的問題,跟散戶釐清:

1. 「你這問題是想知道**事實**(現在多少)、**規則**(怎麼算)、還是**判斷**(要不要做)?」
2. 依答案:
   - **事實** → 直接跑 atlas-mcp 端點,citation 寫 tool_name + timestamp
   - **規則** → 查 SK-00(索引)或 Fin-Skills 對應章節,翻譯成口語
   - **判斷** → 用 GROW+ 教練框架引導,給資料不給指令
3. 把新問法記入 §6,作為新分類候選

---

> §6 諮詢紀錄已歸檔 → [[_consult-index_archive.md]]（2026-08-22 audit-fix,對位 _inbox 第七條例外模式）

---

> §6.4 13 觸發模板對位表已歸檔 → [[_consult-index_archive.md]]（2026-08-22 audit-fix,對位 _inbox 第七條例外模式）

---

## §7 與其他知識資產的關係

| 資產 | 關係 |
|------|------|
| `_index-finskills.md` | 本檔的「依學術名稱查」的鏡像 |
| `_method.md` | 寫入規範(L1/L2/L3 驗證三層) |
| `_inbox.md` | 跨 SK 待辦總表 |
| `task-tracker.md` | 任務追蹤(治理層) |
| `hermes-governance-log.md` | 治理決策歷史 |
| `~/.hermes/skills/data-source-decision/SKILL.md` | **底層 channel 對位(2026-08-01 入庫)** — §3 atlas-mcp 端點的「實際走哪個 channel」真相;5 channel 付費矩陣;Fugle 升級誤判糾錯機制 |

---

## §8 此檔怎麼進化

- 每次新問題落 §6 後,若該問題反覆出現 → 升為新分類進 §1
- atlas-mcp 加新端點 → 補 §3 字典
- Fin-Skills 寫完一頁 SK → 在 §2 對應分類的「核心 SK」標 `已落地`,補 frontmatter `verification`
- 每月清一次 §6 累積,看趨勢 → 看哪些分類出現頻率最高但 SK 沒寫到
