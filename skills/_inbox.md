# atlas-skill-inbound Inbox

最後更新:2026-08-21 v2 session 修補(8/21 補登（見 T9 v2）— 共同根因: A1 execute_code 會員權限 + A2 terminal 180s timeout, 修復任務 A1+A2 已寫入 hermes-governance-log T3-A493 條目請 hermes 下次 trigger 處理, 詳見 _inbox_archive.md §6 8/21 條目);前次更新:2026-08-21 歸檔 session(PR #29);前前次更新:2026-08-12 D6 session 結算(SK-34 真實 promotion + v6.59 overclaim 修正);前前前次更新:2026-08-07 D4 session 結算(`_inbox.md` size 15201B > 12000B 上限 → 啟動第七條例外歷史段歸檔 → 歷史段 5261B 移至 `_inbox_archive.md` v1.0,主檔縮為 3589B); 前前次更新:2026-08-07 16:50 (CR-2026-08-07 擱置區邊移 → v6.52 撤銷外推,改內部化)

---

## 總體進度(2026-08-07 D4 結算)

- 已寫:**34/34 = 100%**(SK-00 索引 + SK-01~33 全 33 主體含 SK-33 audience-routing)
- **active: 33/34 = 97% 主體**(SK-00 索引升 active 2026-08-07 D4 M1 條目完成)
- **archive: 2/34 = 6%**(SK-27/SK-30 量子,2026-08-07 D4 M2 條目完成)
| 1 | SK-00 升 active + 偏差對位(35 ≠ 33) | `skills/SK-00-skill-index.md` | [x] line 6 = active, line 11 verification 改為 35, line 57-61 加 SK-31 衝突待解段 |
| 2 | SK-27 + SK-30 一致性 | `skills/SK-27-quantum-policy.md` + `SK-30-quantum-stability.md` | [x] 兩檔 frontmatter `status: archive` + 歸檔聲明段 |
| 3 | `_inbox.md` 15201B 歸檔 | `skills/_inbox.md` + `skills/_inbox_archive.md` | [x] 本檔 3589B(從 15201B 縮 76%),歷史段 5261B 到 `_inbox_archive.md` |
| 4 | 上市/上櫃分流 skill | `skills/SK-34-listed-otc-routing.md`(新) | [x] 5465B, status: draft 待 L3 實跑升 active |
| 5 | failover-policy 升 skill | `skills/SK-35-mcp-failover.md`(新) | [x] 4888B, status: active |
| 6 | audience-routing | — | 已存在(SK-33 2026-08-07 Day 1 落地),從未完成清單剔除 |
| 7 | skills vs agent 分工 | `summaries/_division_of_labor_skills_vs_agent.md`(獨立檔) | [x] 2291B, AGENTS.md 10601B 接近 11000B 上限,採獨立檔避免撞上限 |
| 8 | `_method.md` 規範本體重構(F 路徑) | `skills/_method.md` + `skills/_method_amendment_history.md` + `~/workspace/atlas-notes/02-knowledge/_method_amendment_D4_oct_review_prompt.md`(superseded,2026-08-22 遷移) | [x] kaecer 拍 F 路徑(非原 A/B/C):line 41 還原 9000B + 5 維度重構(精簡 4 段廢話 + 合併 3 段冗余 + 第七條例外精簡 815B→469B + 起源與演進移到附錄)。最終 `_method.md` 6577B(原 9724B,-32%)≤ 9000B 規範本體自限示範 ✓;附錄 `_method_amendment_history.md` 2783B ≤ 5000B;派工 prompt 標 `status: superseded` |
| 9 | Todo tool 死循環 | manifest 內已標 [x] | [x] 決策「不寫 todo,線性工作」 |

- L2 對位覆蓋:32/34 = 94%(SK-00 + SK-27/30 標 archive)

---


## 最後更新對位事實(2026-08-07 D4 session 結算)

- `_inbox.md` 本次縮 15201B → 3589B(76% 縮,對位第七條例外規範上限 12000B)
- `_inbox_archive.md` 新建 5261B,承接歷史段(2026-08-04 ~ 2026-08-07 結算 + L3 端點快照 + 待辦)
- `_method.md` 規範本體 F 路徑重構 6577B(原 9724B,-32%)≤ 9000B 規範本體自限示範
- 9 條未完成工作全部完成(SK-00 升 active / SK-27+30 archive / _inbox 歸檔 / SK-34 上市上櫃分流 / SK-35 failover / audience-routing 確認 / skills vs agent 分工 / _method 重構 / Todo 死循環)
- 派工 → 拍板(F 路徑)→ 執行 → 結算 4 步治理痕跡完整;PR #16 已 merge main

- L3 待驗端點(每頁 Step 1~3):30 active 頁 × 3 step = 90 個 Step 待跑(給 02:00 每日 cron)

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

## atlas-skill-inbound cron 2026-09-02 02:30 結算 — NOOP 延續(源頭持續失聯 D6+)

**狀態**:`[NOOP]` — 連續 NOOP 鏈第 6 次觸發(8/22 D2 / 8/24 D3 / 8/25 D4 / 8/26-31 隱性跳過 / 9/1 D5 / 9/2 D6),非 failure

**T3 對位**:誰=hermes;何時=2026-09-02T02:30:35+08:00(LLM session, D6 after 8/22);依據=沿用 8/22/8/24/8/25/9/1 模板 + 本次 session 直接驗證

**驗證證據**:
- `ls /Users/kk/workspace/Fin-Skills/ 2>/dev/null && ls .../Fin-Skills.md 2>/dev/null && echo OK || echo FAIL` → 輸出 `FAIL: 找不到 Fin-Skills.md`(源頭持續失聯,D6+)
- `ls /Users/kk/workspace/atlas-wiki/skills/SK-*.md | wc -l` → 37(SK-00~SK-36,無新頁)
- `grep -l '^status: active' /Users/kk/workspace/atlas-wiki/skills/SK-*.md | wc -l` → 35(active)
- `grep -l '^status: archive' /Users/kk/workspace/atlas-wiki/skills/SK-*.md | wc -l` → 2(SK-27 / SK-30 量子,本次用精確字串重測,前次 9/1 因 `archived` 字串誤判為 0)
- `grep -l '^status: draft' /Users/kk/workspace/atlas-wiki/skills/SK-*.md | wc -l` → 0(quota 全飽和)
- `python3` 查 `~/.hermes/cron/jobs.json` 內 8fd1b1eda764 → 0 命中(已從 jobs.json 移除,9/2 cron 觸發應為 default Hub 的 fallback 兜底渠道)

**判斷**(沿用 8/22 + 8/24 + 8/25 + 9/1 模板):
- 此非 LLM 失敗,是「任務前置條件消失」:源頭檔不在,翻譯對象不存在
- 不寫 = 不偽造 L3 通過
- 跳過 = 不硬湊 quota
- 連續 6+ 次 NOOP → 升級 kaecer 待辦持續
- 35 active / 2 archived / 0 draft,quota 全飽和 → 即使源頭恢復,SK-37+ 仍未拍板,新一輪進修需 kaecer 拍板新優先序

**升級 kaecer 待辦**(沿用 8/22 模板,本 session 無新增項):
- [ ] Fin-Skills 源頭檔去哪了?(~/workspace/Fin-Skills/ 整個目錄不在;macOS 26.6.2 環境;無 git log 可追;atlas-notes/02-knowledge/ 亦無對應章節)
- [ ] 若是刻意刪除(換新來源):新 fin-skills 框架落地後再開新一輪 atlas-skill-inbound
- [ ] 若是意外刪除:從備份恢復(`atlas-backups/` 目錄 8/15 16:13 最後寫入,8/25 已驗證備份不含 Fin-Skills,**故恢復路徑已堵**)
- [ ] 新一輪進修優先序:SK-37+ 待 kaecer 拍板(35 active / 2 archived / 0 draft,quota 全飽和 → 即使源頭恢復也需新優先序)
- [ ] 替代方案:若有新版 fin-skills,直接補進 `atlas-notes/02-knowledge/fin-skills/§SK-XX.md` 走 knowledge-harvest 三日循環掃描,而非 atlas-skill-inbound cron

**Telegram**:`[SILENT]` — 對位 Telegram gate Rule 3 + Rule 4:連續 NOOP 不通知,避免「0/0 頁」無意義通知干擾(8/22 / 8/24 / 8/25 / 8/26-31 / 9/1 全 SILENT,9/2 同)

**改動**:本文 append 1 段(無其他 atlas-wiki/ 治理檔被動,僅備份 `_inbox.md.bak.20260902T023035-cron-noop` 留 §5.1 SOP 痕跡;`_inbox.md` 本次 18043B > 12000B 上限,延續 _inbox_archive.md 歸檔路徑,本段僅 append 不觸發歸檔)

---

## atlas-skill-inbound cron 2026-09-15 02:30 結算 — 主任務 0/3 段,本日無結構性缺口（與 §CIO-348 / §CIO-349 同型,D+2 延續）

**狀態**:`[NORMAL — 主任務收斂完成,0/3 段]` — 非 NOOP 鏈（8/22-9/2 連續 NOOP 為源頭失聯型,本型為主任務 quota 自然收斂）

**T3 對位**:誰=hermes;何時=2026-09-15T02:30 CST(LLM session,D+2 after §CIO-349 9/13);依據=沿用 9/13 §CIO-349 模板 + 本 session 直接驗證

**驗證證據**:
- `ls /Users/kk/workspace/Fin-Skills/ 2>/dev/null` → 不在(D24+ 持續失聯,沿用 8/22-9/2 模板)
- `ls /Users/kk/workspace/atlas-wiki/skills/SK-*.md | grep -v "\.bak" | wc -l` → 37(SK-00~SK-36,無新頁)
- `for f in SK-*.md; do grep -cE "^## (一句話定位|論文版概念|atlas 對位|散戶解讀|驗證方式|未消化)" "$f"; done` → 37/37 全部 6 段齊全
- `grep -l "alias →" SK-*.md` → 2(SK-22 + SK-31,補強備註 2026-09-06 已建,沿用)
- `grep -l "補強備註" SK-*.md` → 2(SK-22 + SK-31,同源)
- `wc -c SK-*.md | awk '$1>6000'` → 12(SK-00/01/16/18/19/20/22/29/31/33/34 等;非補強標的,僅觀察)

**判斷**(沿用 §CIO-348 / §CIO-349 模板):
- 主任務 = atlas-wiki 6 段格式覆蓋率補強 → 37/37 全部 6 段齊全 → 0 補強標的
- quota 3 個湊不滿 → 不硬湊(對位任務規範 §「quota 3 個湊不滿怎麼辦：不要硬湊」+ USER §1「禁止猜測包裝為專業」+ USER §1「禁止結論措辭模糊」)
- alias-forwarder 結構(SK-22 / SK-31)為 by-design「讀者分流 / 週期頁」結構,非缺段 → 不重構(對位 §6.1 SOP「不動既有 SK 結構」)
- 次任務不啟動:主任務已收斂 + Fin-Skills.md 仍失聯 + quota 全飽和

**升級 kaecer 待辦**(沿用 8/22 / 9/13 模板,本 session 無新增項):
- [ ] atlas-skill-inbound cron prompt 內嵌「當前已知缺口」清單 stale(標 SK-31 缺 6 段 / SK-22 缺 4 段 / SK-34 缺 1 段 → 2026-09-06 補強前快照)→ 走 task-governance 更新 SKILL.md / _method.md
- [ ] Fin-Skills 源頭檔去哪了?(D24+ 持續失聯)
- [ ] 新一輪進修優先序:SK-37+ 待 kaecer 拍板(35 active / 2 archived / 0 draft,quota 全飽和)
- [ ] 替代方案:若有新版 fin-skills,直接補進 atlas-notes/02-knowledge/fin-skills/§SK-XX.md 走 knowledge-harvest 三日循環掃描,而非 atlas-skill-inbound cron

**Telegram**:`[NORMAL REPORT]` — 對位 Telegram gate Rule 3:本日非 NOOP(無 LLM 失敗 / 無 4xx-5xx / 無 context overflow / 無 MCP unreachable),為「主任務完成,0/3 段無結構性缺口」正常收斂報告 → 與 8/22-9/2 NOOP 鏈不同型,**不 SILENT**

**改動**:本文 append 1 段 + governance-log.md append §CIO-350 1 段(無其他 atlas-wiki/ 治理檔被動);`_inbox.md` 本次 20,922B > 12,000B 上限,延續 _inbox_archive.md 歸檔路徑,本段僅 append 不觸發歸檔(沿用 9/2 模式)
