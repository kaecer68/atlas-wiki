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
| 8 | `_method.md` 規範本體重構(F 路徑) | `skills/_method.md` + `skills/_method_amendment_history.md` + `summaries/manifests/_method_amendment_D4_oct_review_prompt.md`(superseded) | [x] kaecer 拍 F 路徑(非原 A/B/C):line 41 還原 9000B + 5 維度重構(精簡 4 段廢話 + 合併 3 段冗余 + 第七條例外精簡 815B→469B + 起源與演進移到附錄)。最終 `_method.md` 6577B(原 9724B,-32%)≤ 9000B 規範本體自限示範 ✓;附錄 `_method_amendment_history.md` 2783B ≤ 5000B;派工 prompt 標 `status: superseded` |
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
## 對位 `_method.md` 第七條例外(2026-08-07 kaecer 拍板)

`_inbox.md` ≤ 12000 bytes 例外上線;本檔 size 監控由 agent 每次 append 前 `wc -c` 確認 ≤ 12000;超限觸發歸檔(本檔本次即觸發)。

---

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

## 歸檔記錄(2026-08-21 v1.1)

**觸發**:連 6 天 [FAILED] 累積 (8/16, 8/17, 8/18, 8/19, 8/21) + 8/20 cron 卡死復盤 → `_inbox.md` = 22282B 超 12000B 上限 86%

**搬移** (對位 `_method.md` §第七條例外 + `_inbox_archive.md` 歸檔觸發 SOP):
- 6 個 `[FAILED*]` 條目 (5 個 [FAILED] + 1 個 [FAILED—復盤]) → `_inbox_archive.md` §6
- `_inbox.md` 從 22282B → 瘦身 (目標 < 6000B)
- 變更量: 淨變更 0 (搬移),但 `_inbox.md` 結構性縮短

**對位** (對位 `docs/git-merge-protocol.md` §6.4.1 routine merge):
- 變更範圍: `skills/_inbox.md` + `skills/_inbox_archive.md` (限 SK 頁)
- 不觸碰治理檔
- 變更量: +243/-243 (淨 0,邊緣 case 仍 routine)
- CI 全綠 (本地 ci-gate 5 項 + GitHub CI 4 job)

**對位** (對位 `_method.md` §5 SOP 備份):
- `_inbox.md.bak.20260821T-pr29-prearchive` (md5 byte-perfect)
- `_inbox_archive.md.bak.20260821T-pr29-prearchive` (md5 byte-perfect)

**執行**: prime-agent (2026-08-21 16:35 CST) 從 hermes 8/16~8/21 累積 + 8/20 探查 + PR #27 merge 後整合歸檔

**誠實標記**: 本次歸檔是 hermes 8/16 起累積的 5 個 [FAILED] 條目首次 commit 後的歸檔動作 (PR #27 已 merge commit 5 個條目 + 8/20 復盤),歸檔 _inbox.md 不涉及內容修改,純結構性搬移。
---

## atlas-skill-inbound cron 2026-08-22 04:01 結算 — 無工可派,源頭失聯

**狀態**:`[NOOP]` — 不是 failure,是 void state
**T3 對位**:誰=hermes;何時=2026-08-22T04:01:00+08:00(LLM session);依據=`ls /Users/kk/workspace/Fin-Skills/ 2>/dev/null` 失敗(`FAIL: Fin-Skills.md not found`)+ ls atlas-wiki/skills = 37 個 SK-*.md(SK-00~SK-36)+ 35 active/2 archived(SK-27/SK-30 quantum)/0 draft,quota 全飽和

**診斷**:
- **源頭**:`~/workspace/Fin-Skills/Fin-Skills.md` 路徑不存在(連整個 `~/workspace/Fin-Skills/` 目錄都找不到,8/22 04:00 起 ls 失敗)
- **已寫**:SK-00 索引 + SK-01~33 + SK-34(8/12 新增上市上櫃分流)+ SK-35(8/12 failover-policy)+ SK-36(SL vs RL),共 37/37 = 100%
- **active 比例**:35/37 = 94.6%(SK-27/SK-30 量子標 archive);**draft:0**(待 L3 升 active 為零)

**判斷**:
- 此非 LLM 失敗,是「任務前置條件消失」:源頭檔不在了,翻譯對象不存在
- 不寫 = 不偽造 L3 通過
- 跳過 = 不硬湊 quota

**升級 kaecer 待辦**(2026-08-22 新發現):
- [ ] Fin-Skills 源頭檔去哪了?(~/workspace/Fin-Skills/ 整個目錄不在;macOS 26.6.2 環境;無 git log 可追;atlas-notes/02-knowledge/ 亦無對應章節)
- [ ] 若是刻意刪除(換新來源):新 fin-skills 框架落地後再開新一輪 atlas-skill-inbound
- [ ] 若是意外刪除:從備份恢復(`atlas-backups/` 目錄 8/15 16:13 最後寫入,有可能)
- [ ] cron 排程暫停:無源頭期間不要每天空跑浪費 token;kaecer 拍板再啟
- [ ] 替代方案:若有新版 fin-skills,直接補進 `atlas-notes/02-knowledge/fin-skills/§SK-XX.md` 走 knowledge-harvest 三日循環掃描,而非 atlas-skill-inbound cron

**Telegram**:`[SILENT]` — 對位 Telegram gate Rule 3 + Rule 4:無新工可派就不發,避免「0/0 頁」無意義通知干擾
**改動**:本文 append 1 段(無其他 atlas-wiki/ 治理檔被動)
