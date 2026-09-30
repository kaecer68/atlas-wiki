# atlas-skill-inbound Inbox

最後更新:2026-09-27 S6 時效宣告補完(18 頁未宣告 → 0)＋ `待複驗` 工作佇列 9 頁;前次更新:2026-09-27 模板類 quota 拍板結案(不計入;條文入 `_method.md:121`);前次更新:2026-09-27 模板狀態校正 ＋ templates quota 條文查核（同日另段:結清兩項長期待辦）;前次更新:2026-08-21 v2 session 修補(8/21 補登（見 T9 v2）— 共同根因: A1 execute_code 會員權限 + A2 terminal 180s timeout, 修復任務 A1+A2 已寫入 hermes-governance-log T3-A493 條目請 hermes 下次 trigger 處理, 詳見 _inbox_archive.md §6 8/21 條目);前次更新:2026-08-21 歸檔 session(PR #29);前前次更新:2026-08-12 D6 session 結算(SK-34 真實 promotion + v6.59 overclaim 修正);前前前次更新:2026-08-07 D4 session 結算(`_inbox.md` size 15201B > 12000B 上限 → 啟動第七條例外歷史段歸檔 → 歷史段 5261B 移至 `_inbox_archive.md` v1.0,主檔縮為 3589B); 前前次更新:2026-08-07 16:50 (CR-2026-08-07 擱置區邊移 → v6.52 撤銷外推,改內部化)

> 2026-08-07 D4 結算段（總體進度 ＋ 最後更新對位事實,2,816B）已於 2026-09-27 依 `_method.md` 第七條例外移入 `_inbox_archive.md`。


---
## 對位 `_method.md` 第七條例外

規範**唯一來源**＝`_method.md` 第七條例外（v1.0，2026-09-02 拍板更新）：本檔上限 ≤ 12000 bytes，append 前 `wc -c` 自查，超限即依該條歸檔 SOP 移 `_inbox_archive.md`。

## 30 秒重啟程序

見 `~/.hermes/skills/atlas-skill-inbound/SKILL.md` §重啟後 30 秒回神程序

---

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
