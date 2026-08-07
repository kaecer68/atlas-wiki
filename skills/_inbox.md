# atlas-skill-inbound Inbox

最後更新:2026-08-07 D4 session 結算(`_inbox.md` size 15201B > 12000B 上限 → 啟動第七條例外歷史段歸檔 → 歷史段 5261B 移至 `_inbox_archive.md` v1.0,主檔縮為 3589B); 前次更新:2026-08-07 16:50 (CR-2026-08-07 擱置區邊移 → v6.52 撤銷外推,改內部化)

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

amendable_by: kaecer
session_count_tracking: agent(autonomous, see _self-audit.md)
archive_owner: agent(autonomous, see _inbox_archive.md)