# `_internal/` — 內部紀錄索引

> 本目錄放 **wiki 任務以外**的內部紀錄：設計計畫、稽核報告、跨專案 redirect。
> 這些檔案不屬知識引擎內容（AGENTS.md §0 mission），所以不放進 `skills/` 或知識頁；
> 但需要 git 追蹤與**可查找性**，故集中在此並由本檔索引。
>
> CI **不檢查** `_internal/`（`audit-file-index-sync.py` 的 scope 不含本目錄），
> 所以本檔是這裡**唯一**的索引，新增文件時手動加列。
>
> 最後更新：2026-09-27

## 設計計畫（Plan A/B/F/H）

| 檔案 | 一句話 |
|------|--------|
| `plan-A-skills-lifecycle-design-2026-08-21.md` | Plan A — Skills 生命週期落實設計（2026-08-21） |
| `plan-B-tool-filter-design-2026-08-21.md` | Plan B — Tool 過濾機制設計（2026-08-21） |
| `plan-F-skill-refactor-2026-08-21.md` | Plan F — Top 5 SKILL.md 拆分 + 未來護欄（執行計畫） |
| `plan-F-progress-2026-08-21.md` | Plan F Week 1–3 + runtime 串接進度最終摘要（2026-08-22 00:50） |
| `plan-H-cron-toolset-filter-2026-08-21.md` | Plan H — Cron Toolset 過濾（2026-08-21） |
| `skills-map-tier-index-design-2026-08-21.md` | Skills Map 分層索引機制（三層索引架構）設計 |
| `skill-competitive-sop-design-2026-08-22.md` | Skill 競爭 SOP 設計（防 skills 膨脹失控） |

## 跨專案 redirect（內容正本不在本 repo）

| 檔案 | 一句話 | 內容正本 |
|------|--------|----------|
| `hermes-agent-maintenance-redirect.md` | hermes-agent fork 安裝／維護／升級工作已遷移（2026-08-22） | `~/.hermes/hermes-agent/` 相關文件 |
| `hermes-gateway-multiplex-migration-2026-09-27.md` | hermes gateway 收斂至單一 default multiplexer 的遷移紀錄（2026-09-27） | `~/workspace/atlas-notes/03-system-health/hermes-gateway-multiplex-migration-2026-09-27.md` |

## 稽核報告

| 目錄 | 一句話 |
|------|--------|
| `audit-2026-08-22-financial/` | 2026-08-22 金融內容稽核（**已結案**）：保留 4 份持久產出 —— `AUDIT-REPORT-main.md`（主報告）、`DECISION-BRIEFS-iter2.md`、`IMPROVEMENT-PLAN.md`、`VERIFICATION-BACKLOG.md`（38/38 已結案）。<br>2026-09-27 瘦身：移除 12 份過程工件（`child-A/B`、`wp-1..8`，合計 133,433 B）—— 全 repo 無任何引用（`grep` 0 命中），結論已收斂在 4 份主檔；取回方式：`git show 9a8f5e4:_internal/audit-2026-08-22-financial/<檔名>` |

## 維護規則

1. 新增 `_internal/` 文件時，**同步在本檔加一列**（含一句話用途與日期）。
2. 內容正本在別的專案時，這裡只放 **redirect**（指向 SSOT），不複製全文。
3. 快照型數值（PID、版本、計數）必須附**取樣時間**（第五條鐵律，見 `skills/_method.md`）。
4. 本目錄**不是**知識頁：不得放 `SK-*`、`concepts/`、`entities/` 之類的內容，也不納入 SK 索引。
