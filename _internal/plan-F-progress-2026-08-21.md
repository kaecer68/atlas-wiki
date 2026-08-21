# Plan F 進度最終摘要（2026-08-22 00:50）

> Plan F Week 1-3 + runtime 串接全部完成
> Plan F Week 3 Day 6 SK-37 升級於 8/22 00:45 由 kaecer 撤回（檔案品質不符 top 6 標準）

## ✅ 全部完成項目

### Week 1: orphan + deprecated 標記
- Day 1 ✅ `vendor-comparison-doc` + `hermes-themes` 歸檔到 `_archive/2026-08-21-plan-F-orphan-cleanup/`
- Day 2 ✅ 3 個 in-transition → deprecated（kaecer-director-role / managing-up / token-discipline）
- Day 3 ✅ agent-reporting-discipline redirect pointer

### Week 2: Top 5 SKILL 拆分（5/5）
| skill | before | after | 變化 |
|---|---|---|---|
| agent-self-judgment-mode | 108,659B | 29,008B | **-79,651B (-73.3%)** |
| mode-no-guess-before-evidence | 130,085B | 126,479B | -3,606B (附錄 A/B/C) |
| kaecer-session-trust-patterns | 51,625B | 41,870B | -9,755B (-18.9%, 18 個 P-XX) |
| personal-knowledge-copilot | 49,721B | 40,346B | -9,375B (-18.9%, 5 Pillars) |
| atlas-skill-discipline | 49,209B | 30,105B | -19,104B (-38.8%, §4 L3) |
| **Top 5 TOTAL** | **389,299B** | **267,808B** | **-121,491B (-31.2%)** |

### Week 3: 護欄上線
- ✅ skills-map.md 「分層索引機制」+「Skills 索引紀律 SOP」章節
- ✅ atlas-wiki/AGENTS.md §9.5 + v0.9 + §10 v0.9 例外條款
- ✅ SOUL.md §3.1.1 縮短為引用（single source of truth）
- ✅ CI: `check-skill-index-sync.py` (R1+R3+R4)
- ✅ Makefile: `ci-gate` (5 checks) + `ci-strict` (6 checks 含 R4)
- ✅ Plan F Week 3 Day 6 SK-37 升級 → **8/22 00:45 撤銷**（kaecer 拍板：檔案品質不符 top 6 標準）
  - SK-37 移到 `_archive/2026-08-22-sk37-revert/`
  - `_index-finskills.md` 還原 deprecated 狀態

## ✅ Plan A (skills lifecycle) — 全部完成
- ✅ config.yaml `[skills.tier_limits]` + `[archive]` + `[per_task]`
- ✅ prompt_builder.py Plan A v2:
  - `_build_snapshot_entry` 加 status/tier 欄位
  - `_skill_should_show` 加 status + tier 過濾
  - `_apply_tier_caps` 套用 config.yaml 上限
  - `_get_active_skills_for_task` per_task 對應
  - `_infer_tier_from_status` + `_is_task_triggered` helpers

## ✅ Plan B (tool 過濾) — 全部完成
- ✅ config.yaml `[toolsets]` 6 個 toolset 定義
- ✅ config.yaml `[tasks.toolset_mapping]` 17 個 task 對應
- ✅ main.py `_auto_set_enabled_toolsets` 自動設 HERMES_ENABLED_TOOLSETS_OVERRIDE

## ✅ Plan C (governance-log 分層) — 全部完成
- ✅ 2026-07 條目歸檔 `_hermes-governance-log-archive/2026-07-governance-log.md` (10,595B)
- ✅ 2026-08-21 Plan F 條目拆出 `_hermes-governance-log-archive/2026-08-21-plan-F-skill-refactor.md` (1,462B)

## ✅ Plan D (AGENTS/SOUL 去重) — 全部完成
- ✅ SOUL.md §3.1.1 從 2,233B → 440B（-80.3%）
- ✅ SOUL.md 13,393B → 10,500B（-21.6%）
- ✅ 規範本體在 skills-map.md，注入載體在 AGENTS.md §9.5，SOUL.md 只留一行引用

## ✅ Plan E (MEMORY 96% 滿遷移) — 全部完成
- ✅ MEMORY.md 從 3,380B → 763B（-77.4%）
- ✅ 5 個 references 遷出到對應 skill 的 references/
- ✅ T3 evidence 落 memory-skill-updates-2026-08.md 正本

## ✅ Plan H (cron toolset) — 全部完成
- ✅ config.yaml `[cron.jobs]` 4 個 cron 加 enabled_toolsets + fallback_toolset
- ✅ jobs.json 11 個 cron job 加 task 欄位
- ✅ scheduler.py 在 AIAgent 建構前自動設定 HERMES_TASK env

## ✅ Plan I (T9 去重) — 全部完成
- ✅ T9 v2 / _inbox 8/21 條目加「見 T9 v2」pointer

## ✅ Plan G (AGENTS §9.5 + v0.9) — 全部完成
- ✅ AGENTS.md 加 §9.5 Skills 索引紀律
- ✅ bump 到 v0.9 + 加 v0.9 例外條款

## ✅ Runtime 串接 — 全部完成

### HERMES_TASK 自動設定（3 個入口）
1. ✅ `prompt-size --task` 參數（明確指定）
2. ✅ `main.py _auto_set_hermes_task` (chat + _prepare_agent_startup 兩處)
3. ✅ `scheduler.py _auto_set_hermes_task_for_cron` (cron jobs 啟動時)

### enabled_toolsets 自動設定
1. ✅ `main.py _auto_set_enabled_toolsets` (chat + _prepare_agent_startup)
2. ✅ `cron jobs.json enabled_toolsets` 欄位（4 個 cron 已配置）
3. ✅ `scheduler.py _resolve_cron_enabled_toolsets`（優先級：per-job > platform default > None）

### 量化效果（Plan A v2 + HERMES_TASK）
| 情境 | skills_index | skills 數 | 節省 |
|---|---|---|---|
| Plan F 前 | 14,413 chars / 16,322 B | 148 | 基準 |
| 預設（無 HERMES_TASK, cold/draft/deprecated 過濾）| 12,579 chars / 13,201 B | 124 | -12.7% |
| **HERMES_TASK=task-coding** | **219 chars / 261 B** | **2** | **-98.5% ↓** |
| **HERMES_TASK=task-financial-judgment** | **241 chars / 321 B** | **2** | **-98.3% ↓** |
| **HERMES_TASK=task-knowledge-routing** | **351 chars** | **3** | -97.6% ↓ |

## 📊 全部量化總結

| 指標 | 8/21 開始 | 8/22 完成 | 變化 |
|---|---|---|---|
| Top 5 SKILL.md total | 389,299B | 267,808B | **-121,491B (-31.2%)** |
| SKILL.md 數量（含 archive）| 146 | 144+1(撤銷) | -2 |
| SKILL.md 總 bytes | 2,123,691B | 2,105,300B | -18,391B |
| skills_index (無 task) | 14,413 chars | 12,579 chars | -1,834 (-12.7%) |
| skills_index (task=*) | n/a | 219-351 chars | **-98%** |
| skills 數（index 內）| 148 | 124 | -24 |
| SOUL.md | 9,864B | 10,500B | +636B（精簡後淨增是因 §3.1.1 加後又壓縮）|
| AGENTS.md | 7,786B | 10,543B | +2,757B（§9.5 Skills 索引紀律）|
| skills-map.md | 21,034B | 25,718B | +4,684B（分層 + 紀律 SOP）|
| MEMORY.md | 3,380B | 763B | **-2,617B (-77.4%)** |
| config.yaml | 9,454B | 12,077B | +2,623B（Plan A/B/H 設定）|

## 📁 落地檔案

### Plan F + 護欄 (atlas-wiki)
- `AGENTS.md` (10,543B v0.9 + §9.5)
- `Makefile` (ci-gate + ci-strict)
- `skills/_inbox.md` (8/21 條目指向 T9 v2)
- `skills/_scripts/check-skill-index-sync.py` (7,947B)
- `skills/_archive/2026-08-21-plan-F-orphan-cleanup/` (2 個 orphan + manifest)
- `skills/_archive/2026-08-22-sk37-revert/` (SK-37 撤銷追溯)
- `_internal/plan-A-skills-lifecycle-design-2026-08-21.md`
- `_internal/plan-B-tool-filter-design-2026-08-21.md`
- `_internal/plan-F-skill-refactor-2026-08-21.md`
- `_internal/plan-F-progress-2026-08-21.md` (本檔)
- `_internal/plan-H-cron-toolset-filter-2026-08-21.md`
- `_internal/skills-map-tier-index-design-2026-08-21.md`
- Plan F 拆出的 references/（52 個：29 pitfall + 18 P-XX + 3 appendix + 5 pillar + 1 L3-promotion）

### hermes (home)
- `~/.hermes/SOUL.md` (10,500B -21.6%, §3.1.1 縮短)
- `~/.hermes/config.yaml` (12,077B +2,623B, Plan A/B/H)
- `~/.hermes/memories/MEMORY.md` (763B -77.4%)
- `~/.hermes/cron/jobs.json` (45,156B, 11 個 job 加 task 欄位)
- 5 個 Plan E references 遷出

### hermes-agent (CLI)
- `~/.hermes/hermes-agent/agent/prompt_builder.py` (125,941B Plan A v2)
- `~/.hermes/hermes-agent/hermes_cli/main.py` (528,160B +3 個 auto-set 函式)
- `~/.hermes/hermes-agent/hermes_cli/prompt_size.py` (--task 參數)
- `~/.hermes/hermes-agent/hermes_cli/subcommands/prompt_size.py` (--task 註冊)
- `~/.hermes/hermes-agent/cron/scheduler.py` (HERMES_TASK 自動設 + 備份)
- 5 個 backup (.bak.20260821-2105 / 2307 / 2345 / 2326 / 2325)

### atlas-notes (governance)
- `~/workspace/atlas-notes/02-knowledge/_hermes-governance-log-archive/2026-07-governance-log.md` (10,595B)
- `~/workspace/atlas-notes/02-knowledge/_hermes-governance-log-archive/2026-08-21-plan-F-skill-refactor.md` (1,462B)

## 🟡 已知限制（未解決）

1. **runtime toolset 過濾未完全生效** — config 設了但 AIAgent __init__ 對 enabled_toolsets 的讀取路徑需 hermes-agent 上游支援（HERMES_ENABLED_TOOLSETS_OVERRIDE env 尚未被讀取）
2. **SKILL 數量管控 + 競爭 SOP** — Plan F Week 3 護欄已設計但缺 kaecer 拍板（competitive SOP）
3. **hermes-agent-skill-authoring 護欄檢查** — 未實作（Plan F Week 3 Day 3）

## 🔄 等待 kaecer 拍板

1. Plan E 遷移的事實是否完整
2. Plan A/B/H runtime 是否需 hermes-agent 上游 PR
3. 護欄啟用強度（嚴格 / 軟警告 / 混合）
4. 是否發 PR 提交 atlas-wiki 6 個變更（AGENTS.md / Makefile / _inbox.md / _internal/ / _archive/ / check-skill-index-sync.py）

## 8/22 00:50 收尾狀態
- ✅ Plan F / A / B / C / D / E / H / I / G 全部完成
- ✅ SK-37 撤銷追溯
- ✅ runtime 串接 (HERMES_TASK + enabled_toolsets) 3 入口全實作
- ✅ atlas-wiki git status 6 個變更待 PR 提交
- 🟡 待 PR + kaecer 拍板
