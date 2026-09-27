# Atlas Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format:`## [YYYY-MM-DD] action | subject`

## 歸檔記錄（2026-09-27，依 kaecer 指示按月份切分）

> `log.md` 原本累積 46,017 B / 24 段（2026-07-15 起）。2026-09-27 把 **2026-07 與 2026-08 的段落原文搬移**到
> `_archive/log-2026-07.md`（38,644 B）與 `_archive/log-2026-08.md`（5,729 B）；本檔保留**當月（2026-09 起）**與後續新增。
> 搬移為**逐段原文**（未改字）；需要舊檔原文可用 `git show <SPLIT_PREV_SHA>:log.md` 取回。
> 分派規則：**每月初**把上月段落搬進 `_archive/log-YYYY-MM.md`（同日誌 `_self-audit.md`／`_inbox.md` 的「主檔留現行、歷史歸檔」慣例，對位 `_method.md` 第七條精神）。

---

## 2026-09-27 — `_internal/` 稽核過程工件瘦身（16 檔 → 4 檔，−133,433 B）

- **做了什麼**：`_internal/audit-2026-08-22-financial/` 移除 12 份過程工件（`child-A-sk-quant`、`child-B-concepts-templates`、`wp-1`…`wp-8-verify-sys`，合計 133,433 B），保留 4 份持久產出（`AUDIT-REPORT-main` 22,767／`DECISION-BRIEFS-iter2` 4,591／`IMPROVEMENT-PLAN` 3,645／`VERIFICATION-BACKLOG` 8,127，合計 39,130 B）。
- **為什麼**：該稽核已結案（`VERIFICATION-BACKLOG` 38/38 closed）；過程工件全 repo **0 引用**（實測 `grep -rn 'child-A-sk-quant|child-B-concepts-templates|wp-1-report|wp-7-|wp-8-verify'` 在 `_internal/audit-2026-08-22-financial/` 以外 0 命中）⇒ 屬「無持久保存價值」的重複層，留存只是稀釋可查找性。
- **取回**：`git show 9a8f5e4:_internal/audit-2026-08-22-financial/<檔名>`（本條目前一個 commit = 9a8f5e4）。
- **不動**：`skills/_archive/_methodology_alignment_audit*` 三檔**刻意保留** —— `AUDIT-REPORT-main.md:117` 明文把它們列為稽核基準（`_VERBATIM` 10,726／`_with_fileline` 30,522），是審計出處不是重複。
- **量測脈絡**：全 repo tracked `.md` = 150 檔 / 1,212,899 B，其中 >9,000 B 者 36 檔 / 642,948 B（53.0%）。本條只清「已結案的過程工件」，未動 `concepts/`（13 檔 206,480 B，兩兩 line-set Jaccard <5% ⇒ 各自獨立，非重複）與 `entities/`（5 檔 69,048 B，5–10% 重疊僅為頁面樣板）。

- 2026-09-27：`_internal/` 7 份已結案計畫（Plan A/B/F/F-progress/H ＋ 分層索引 ＋ 競爭 SOP，35,845 B）合併為 `_internal/_completed-plans-2026-08.md`（5,436 B，−30,409 B）；原文取回 `git show b4f9524:_internal/<檔名>`。同步更新 3 處引用（`_internal/README.md`、`skills/_inbox.md`、`skills/_scripts/check-skill-index-sync.py` 的 R5 註解）＋ `~/.hermes` 內 2 處（`skills/skills-map.md:61`、`agent-self-judgment-mode/references/skill-competitive-sop-2026-08-22.md:3`）。
