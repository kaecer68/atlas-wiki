# `_internal/` 已結案計畫彙整（2026-08-21 ~ 08-22）

> 2026-09-27 將 7 份已結案計畫文件合併為本檔（原合計 35,845 B）。原文取回方式見 §4。
> 本檔是**摘要**（lossy，刻意），現行規範一律以 §2 的「落地位置」為準。

## §1 結論

2026-08-21/22 的 skill 生命週期 × tool 過濾改造（Plan A / B / F / H ＋ 分層索引 ＋ 競爭 SOP）**全部結案**。
拆分成果與護欄留在 atlas-wiki（`skills/`、`Makefile`、`AGENTS.md` §9.5）；runtime 設定留在 `~/.hermes/`。

**2026-09-27 查核（重點 drift）**：現行 `~/.hermes/config.yaml`（`_config_version: 46`）**已無**
`[skills.tier_limits]`、`[toolsets]`、`[tasks.toolset_mapping]` 區塊。Plan A/B 的 config 提案屬**已退役**；
留下的外部規範是 `~/.hermes/skills/skills-map.md`「分層索引機制」段，以及 `cron.jobs.*.enabled_toolsets`（Plan H）。

## §2 各計畫最終結果（2026-09-27 對 repo 與 live 設定查核）

| 計畫（日期） | 原本要做的 | 最終結果 | 現在活在哪裡 |
|---|---|---|---|
| **Plan A** skills 生命週期（08-21） | 三層索引 ＋ 上限護欄，落地 config | **多數完成；config 區塊已退役** | `~/.hermes/skills/skills-map.md`「分層索引機制」段；`AGENTS.md` §9.5；`skills/_method.md` 第九條 |
| **Plan B** tool 過濾（08-21） | 24 個 tool schema 分 6 個 task toolset，降 always-on | **部分／被取代**：`[toolsets]` 與 task 對映不在現行 config | `~/.hermes/config.yaml` `platform_toolsets`（現行機制）；`cron.jobs.*.enabled_toolsets` |
| **Plan F** Top 5 SKILL 拆分 ＋ 護欄（08-21） | 拆 references、orphan 清理、護欄、按需索引 | **完成** | `~/.hermes/skills/**/references/`（外部，58 個 pitfall-/p-/appendix-/pillar- 檔）；`skills/_scripts/check-skill-index-sync.py`；`Makefile` `ci-gate`；`AGENTS.md` §9.5 |
| **Plan F-progress** 進度最終摘要（08-22 00:50） | 記錄 Week 1–3 ＋ runtime 串接狀態 | **完成；部分量化已過時** | 本檔 §2/§3；量化數字見 §3 註 |
| **Plan H** cron toolset 過濾（08-21） | 4 個 cron job 各自 `enabled_toolsets` | **完成（config 仍在）** | `~/.hermes/config.yaml` `cron.jobs.{atlas-skill-inbound,trigger-monitor,session-self-check,schedule-health-audit}` |
| **skills-map 分層索引設計**（08-21） | 三層索引 ＋ 四維度貢獻度評判 SOP | **完成** | `~/.hermes/skills/skills-map.md`「分層索引機制」；`AGENTS.md` §9.5 |
| **skill 競爭 SOP 設計**（08-22） | 新增 skill 前必跑 70% 重疊競爭流程 | **部分完成（規範落地；CI 未強制）** | 本檔 §3；`skills/_scripts/check-skill-index-sync.py` R5（已實作但**軟性、未啟用**）；`AGENTS.md` §9.5 |

補充（同批結案、非本次檔案範圍）：orphan 清理結果在 `~/.hermes/skills/_archive/2026-08-21-plan-F-orphan-cleanup/`；
SK-37 升級於 2026-08-22 00:45 由 kaecer 撤回（品質不符 top 6 標準），追溯留在 repo `skills/_archive/2026-08-22-sk37-revert/`。

## §3 耐久設計決策（值得留的 rationale）

1. **三層索引 ＋ 硬上限**：core 10 / active 50 / cold 100（總上限 160，軟警告）。core always-on，
   active 任務觸發，cold 需 `skill_view`。護欄強度＝**混合模式**：硬上限生效，但 archive **不自動執行**，需 kaecer 拍板。
2. **分層不看引用次數**，看四維度：工程價值 E / 業務價值 B / 管理價值 M / 時效性 T（任意 high→core 或 active；
   T low→archive）。理由：純數字會誤殺治理型 skill。
3. **同類型結合優先（08-22 21:15 kaecer 拍板，強制）**：新需求先搜既有 skill；≥70% 重疊 → **必須**寫進既有
   skill 的 `references/`，不開新檔；<70% 才寫 1 段提案給 kaecer 拍板；被拒絕者留 `_archive/<date>-rejected-<name>.md` 作 audit trail。
4. **拆分原則**：SKILL.md 只留「何時載入 ＋ 觸發條件 ＋ 流程骨架 ＋ 紅線 ＋ references 索引」，細節下沉 `references/`；
   拆完必驗連結有效（原計畫要求 curl 200）。
5. **tool 過濾**：task skill 需帶 toolset，並備 `fallback_toolset: general-toolset` 防過窄；cron job 也各自指定
   `enabled_toolsets` ＋ fallback。toolset 概念沿用至今（`platform_toolsets`）。
6. **量化目標（當日基準，非現值）**：Top 5 SKILL.md 389,299 B → 267,808 B（−31.2%）；
   `skills_index` 有 `HERMES_TASK` 時 219–351 chars（−98%）；MEMORY.md 3,380 B → 763 B（−77.4%）。
   這些數字是 2026-08-22 快照，**已不代表現況**，勿直接引用。

## §4 已退役原文

本檔合併後，以下 7 檔已由 git 移除；原文（去重前）可由移除前一版取回：

| 已移除檔案 | 大小 |
|---|---|
| `plan-A-skills-lifecycle-design-2026-08-21.md` | 1,405 B |
| `plan-B-tool-filter-design-2026-08-21.md` | 3,885 B |
| `plan-F-skill-refactor-2026-08-21.md` | 7,992 B |
| `plan-F-progress-2026-08-21.md` | 8,357 B |
| `plan-H-cron-toolset-filter-2026-08-21.md` | 1,501 B |
| `skill-competitive-sop-design-2026-08-22.md` | 5,109 B |
| `skills-map-tier-index-design-2026-08-21.md` | 7,596 B |

取回指令（`b4f9524` = 移除前一版 HEAD）：

```bash
git show b4f9524:_internal/plan-F-skill-refactor-2026-08-21.md
# 或一次列出全部 7 檔
git show b4f9524 --stat -- _internal/
```
