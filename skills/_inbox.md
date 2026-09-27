# atlas-skill-inbound Inbox

最後更新:2026-09-27 模板類 quota 拍板結案(不計入;條文入 `_method.md:121`);前次更新:2026-09-27 模板狀態校正 ＋ templates quota 條文查核（同日另段:結清兩項長期待辦）;前次更新:2026-08-21 v2 session 修補(8/21 補登（見 T9 v2）— 共同根因: A1 execute_code 會員權限 + A2 terminal 180s timeout, 修復任務 A1+A2 已寫入 hermes-governance-log T3-A493 條目請 hermes 下次 trigger 處理, 詳見 _inbox_archive.md §6 8/21 條目);前次更新:2026-08-21 歸檔 session(PR #29);前前次更新:2026-08-12 D6 session 結算(SK-34 真實 promotion + v6.59 overclaim 修正);前前前次更新:2026-08-07 D4 session 結算(`_inbox.md` size 15201B > 12000B 上限 → 啟動第七條例外歷史段歸檔 → 歷史段 5261B 移至 `_inbox_archive.md` v1.0,主檔縮為 3589B); 前前次更新:2026-08-07 16:50 (CR-2026-08-07 擱置區邊移 → v6.52 撤銷外推,改內部化)

> 2026-08-07 D4 結算段（總體進度 ＋ 最後更新對位事實,2,816B）已於 2026-09-27 依 `_method.md` 第七條例外移入 `_inbox_archive.md`。


---
## 對位 `_method.md` 第七條例外

規範**唯一來源**＝`_method.md` 第七條例外（v1.0，2026-09-02 拍板更新）：本檔上限 ≤ 12000 bytes，append 前 `wc -c` 自查，超限即依該條歸檔 SOP 移 `_inbox_archive.md`。

## 30 秒重啟程序

見 `~/.hermes/skills/atlas-skill-inbound/SKILL.md` §重啟後 30 秒回神程序

---

## D6 新增待辦(2026-08-12,跨 SK 性質)

### SK-34 路徑 drift 系統化紀錄(2026-08-12 新發現)
- `/api/industry/sector-list` → **404**
- `/api/industry/sectors` → **200**(正確 path)
- 推論:atlas-mcp wrapper 與 atlas-go HTTP path 可能不一致,後續所有 SK 寫的 atlas-mcp tool 名稱 commit 前必須 `curl` 探一次實際 HTTP path
- 待辦:在 `summaries/atlas-http-path-drift.md` 集中記錄所有發現的 path drift,給 atlas dev agent 修 wrapper

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

## 2026-09-27 prime-agent 查核結算（幽靈 SSOT 落地／T9 Task 3／CI 假綠）

**1. 幽靈 SSOT 已落地**：`summaries/atlas-http-path-drift.md`（2026-09-27 建；本檔 `:54`／`SK-34:113` 長期指向但從未存在）。當日實測：**`/api/system/health` 已 404**（8/29 日誌記 200）⇒ 無時間戳的「正確路徑」不可信；判 route 必帶 key（不帶回 401）。`SK-29` 另有死引用 `docs/archive/2026-07-20-…-drift.md`（未修）。

**2. T9 Task 3 = 從未執行**：37 頁僅 SK-34 有 `l3_*`（2026-08-12）；`git log --since=2026-08-21 -- skills/SK-` 空；cron `atlas-skill-inbound` job 已移除。詳見 `_t9-repair-tasks-20260821.md`。

**3. 🚨 CI 假綠**：`audit-file-index-sync.py:19` 的 `ROOT` 硬編 `~/workspace/atlas-wiki` ⇒ runner 上 glob 全空、恆印 `✅ 0/0`；本機實跑真相 = **rc=1、64 檔未索引**。

**Telegram**：`[SILENT]`（人工查核）


---

## 2026-09-27 結清兩項長期待辦 — Fin-Skills 來源查核 (i) ＋ SK-37+ 優先序決策簡報 (ii)

**範圍**：結清本檔 9/2 段（原 line 96-101）與 9/15 段（原 line 129-133）兩項 D24+ 待辦。**只查核與提案,未動任何 SK 頁。**

### (i) Fin-Skills 源頭查核 → **判定：全機不存在,且本機無法復原**

2026-09-27 實跑證據（Mac Mini;`/Users/kk`→`/Users/kaecer` symlink ⇒ 舊紀錄同樹）：
- `ls -d ~/workspace/Fin-Skills ~/workspace/Fin-Skills/Fin-Skills.md` → No such file or directory
- `find / -maxdepth 4 -iname '*Fin-Skills*' 2>/dev/null` → **0 命中**（全碟;`~/workspace/Fin-Skills` 深度 4 在範圍內）
- `find ~ -maxdepth 5 -iname '*fin*skill*'` → 13 命中,**全為本 repo 產物**（`_index-finskills.md` ＋ 2 個 .bak）與 hermes 的 `find-skills` skill 目錄,無來源目錄
- `mdfind -name 'Fin-Skills'`（Spotlight 全索引）→ 2 命中,皆 `skills/`
- `ls /Volumes` → 僅 `Macintosh HD` ＋ `Recovery`（**無 Time Machine／外接卷**）
- `~/.config/atlas-backup/` 與 `~/workspace/atlas-backups/`（僅 `atlas-env, data-state, notes, pg, wiki`）⇒ **備份標的從不含 workspace 層其他目錄**
- atlas-notes 備份 8 檔（9/19–9/27 tarball,各 ~1.1GB）逐檔列名 grep `finskills|fin-skills` → **8×0 命中**
- `git log --all -S 'Fin-Skills'` → 最早命中 `2315bf6`(2026-08-03 repo 初始 commit) ⇒ **repo 自建立起只有引用、從無來源檔**
- `~/.Trash` 被 macOS TCC 擋（Operation not permitted）;8/25 追查已記 Trash 內僅 `_index-finskills.md`(1,334B),非來源檔

串接 8/25 追查（`hermes-governance-log.md` T3-A707:`find /Users/kk -maxdepth 4` 0 命中＋8/18 notes 備份解壓 0 命中）全數複驗成立 ⇒ **維持「8/15 之前已永久消失」**。

**對檔內原兩選項的判定**：「刻意刪除」vs「意外刪除（從備份恢復）」**已無操作差異**——Trash 無、備份標的不含、Spotlight 全索引無 ⇒ 恢復不可行。**建議改記第三態「來源不可考」**。是否曾存在於他機（MacBook）**本機不可證**（未 ssh）;唯一相關紀錄＝`_inbox_archive.md:582` 的 E 條「查 Spotlight／Time Machine,需 kaecer 在 MacBook 操作」⇒ **該條仍待 kaecer**。

**新發現（未結矛盾,需拍板）**：`_index-finskills.md` frontmatter 稱「原 Fin-Skills.md **從未建立**（8/21 探查）」並指向**不存在的 §0**（幽靈引用）;但 `_method.md` 的 `sources:` 與 `_consult-index.md` 的 `ground_truth_basis:` 仍列 `~/workspace/Fin-Skills/Fin-Skills.md (32 SK)`。⇒「從未存在」與「存在後遺失」兩說未對齊,影響 37 頁來源可追溯性。**修檔待 kaecer 拍板。**

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

## 2026-09-27 模板狀態校正（SK-31）＋ 模板類 quota 條文查核（**已拍板結案**）

**A. 模板狀態校正（stale → 已改檔）**

2026-09-27 `ls -l templates/` 實測:`templates/trigger-*.md` = **20 檔**（`templates/` 全 21 檔 = 20 trigger ＋ `audit-report.md`）。
- **已存在（非「未落」）**:`trigger-megaproject-2-quarter-lag.md`（9,996B;立此日期 2026-08-04）= #14;`trigger-equipment-capex-external-report-cycle.md`（7,465B;立此日期 2026-08-04,`template_number: 15`）= #15。
- **仍未存在**:`templates/trigger-renewable-energy-divergence.md`（`ls` → No such file;全 repo grep 僅 2 處待辦文字）= #16。
- ⇒ 原「SK-31 未落模板 ×3」**實為 ×1**。已修 `SK-31:53,54`（對位表兩列改「已存在 ✅ 已落」＋補 #16 一列）、`SK-31:107,108`（兩條「落模板」移出 §未消化）;`SK-31` 改後 8,967B ≤ 9,000B。

**B. 「模板類是否佔 quota」→ **已拍板結案（2026-09-27 kaecer）**：`templates/trigger-*.md` **不計入**每日 3 頁 quota（結清本檔 9/27 (ii) 待拍板 ②）。**
- 拍板入 SSOT:`skills/_method.md:121` 新條文「templates = cron 觸發定義(非知識頁) → 不計入 3 頁;**交換義務** = 結算記 trigger 模板現數」;同檔 `:120` 量詞明示「Quota(3 頁 **SK**)」。
- **記錄義務**:每次結算記 trigger 模板現數實測值（2026-09-27 = **20 檔**;`ls templates/trigger-*.md | wc -l` 實跑）。
- **反例照實留**:`_manifest_coverage_routing.md:134` 曾把 `concepts/` 頁記「計入 1/3」——不推翻,因 templates 是**觸發定義**(cron 產物),與知識頁不同類。
- **其他 quota 宣告實查**:`README.md:50`（本檔舊記 :48,實為 :50）／`AGENTS.md:27`／`docs/git-merge-protocol.md:183`／`_manifest_coverage_routing.md:129` 皆以「頁」為單位,無矛盾。

**Telegram**:`[SILENT]`（人工查核）
**改動**:本檔 append 本段;為容納本段,原 **2026-08-07 D4 結算段（`## 總體進度` ＋ `## 最後更新對位事實`,2,816B）原文移入 `_inbox_archive.md`**（append,含出處標頭）;實測 11,792 B ≤ 12,000B。
**改動(quota 結案)**:B 小節改寫（**−113B**）,無新歸檔;實測 **11,965 B ≤ 12,000B**。
**移段時仍 OPEN 的項**:D4 段「L3 待驗端點 90 個 Step」為 2026-08-07 快照,實際範圍已於 T9 Task 3 更新為 105 步且查核為「從未執行」（未消失）。
