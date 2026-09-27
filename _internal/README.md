# `_internal/` — 內部紀錄索引

> 本目錄放 **wiki 任務以外**的內部紀錄：設計計畫、稽核報告、跨專案 redirect。
> 這些檔案不屬知識引擎內容（AGENTS.md §0 mission），所以不放進 `skills/` 或知識頁；
> 但需要 git 追蹤與**可查找性**，故集中在此並由本檔索引。
>
> CI **不檢查** `_internal/`（`audit-file-index-sync.py` 的 scope 不含本目錄），
> 所以本檔是這裡**唯一**的索引，新增文件時手動加列。
>
> 最後更新：2026-09-27

## 已結案計畫（Plan A/B/F/H ＋ 索引／競爭 SOP，2026-08-21~08-22）

| 檔案 | 一句話 |
|------|--------|
| `_completed-plans-2026-08.md` | 7 份已結案計畫合併摘要：skills 生命週期（Plan A）、tool 過濾（Plan B）、Top 5 SKILL 拆分＋護欄（Plan F/F-progress）、cron toolset（Plan H）、分層索引、競爭 SOP。含各計畫最終結果、落地位置、原文取回指令（2026-09-27 合併，原 35,845 B → 5,436 B） |

## 跨專案 redirect（內容正本不在本 repo）

| 檔案 | 一句話 | 內容正本 |
|------|--------|----------|
| `hermes-agent-maintenance-redirect.md` | hermes-agent fork 安裝／維護／升級工作已遷移（2026-08-22） | `~/.hermes/hermes-agent/` 相關文件 |
| `hermes-gateway-multiplex-migration-2026-09-27.md` | hermes gateway 收斂至單一 default multiplexer 的遷移紀錄（2026-09-27） | `~/workspace/atlas-notes/03-system-health/hermes-gateway-multiplex-migration-2026-09-27.md` |

## 操作程序（recipe）

| 檔案 | 一句話 |
|------|--------|
| `_l3-backfill-recipe.md` | SK 頁 L3 端點實跑回填做法（2026-09-27,batch #1 起用）:工具→端點 SSOT（`tools_canary_test.go` 的 `canaryRoutes`）、probe 範本、合格 L3 四條件、page 更新格式與 9,000 B 上限處理、claim 被推翻時的更正規則、批量與額度、已解／未解清單。消費端:`make structure-metrics` 指標 8（L3 覆蓋率＋watch list） |

## 稽核報告

| 目錄 | 一句話 |
|------|--------|
| `audit-2026-08-22-financial/` | 2026-08-22 金融內容稽核（**已結案**）：保留 4 份持久產出 —— `AUDIT-REPORT-main.md`（主報告）、`DECISION-BRIEFS-iter2.md`、`IMPROVEMENT-PLAN.md`、`VERIFICATION-BACKLOG.md`（38/38 已結案）。<br>2026-09-27 瘦身：移除 12 份過程工件（`child-A/B`、`wp-1..8`，合計 133,433 B）—— 全 repo 無任何引用（`grep` 0 命中），結論已收斂在 4 份主檔；取回方式：`git show 9a8f5e4:_internal/audit-2026-08-22-financial/<檔名>` |

## 維護規則

1. 新增 `_internal/` 文件時，**同步在本檔加一列**（含一句話用途與日期）。
2. 內容正本在別的專案時，這裡只放 **redirect**（指向 SSOT），不複製全文。
3. 快照型數值（PID、版本、計數）必須附**取樣時間**（第五條鐵律，見 `skills/_method.md`）。
4. 本目錄**不是**知識頁：不得放 `SK-*`、`concepts/`、`entities/` 之類的內容，也不納入 SK 索引。
