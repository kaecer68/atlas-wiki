# CLAUDE.md — atlas-wiki 規則索引

@AGENTS.md

> **文件角色**：Claude Code（或任何讀 CLAUDE.md 的 agent）在 atlas-wiki 工作的入口索引。
> 跨工具權威來源 = [`AGENTS.md`](AGENTS.md)；本檔只放 Claude Code 專屬設定與速查，不重複 AGENTS.md 規則（One source of truth）。

## 語言強制規範

見 [`AGENTS.md`](AGENTS.md)（跨工具權威來源）。

## 快速路由

| 需求 | 參考位置 |
|------|---------|
| 專案 context（憲法/目錄/權限/任務路由） | [`AGENTS.md`](AGENTS.md)（v0.8） |
| 技能寫入規範（六條鐵律/size 上限） | [`skills/_method.md`](skills/_method.md) |
| 技能轉化審查任務（T9） | [`skills/_t9-repair-tasks-20260821.md`](skills/_t9-repair-tasks-20260821.md) |
| 雙機治理（iMac/hermes 角色、同步、衝突） | `~/workspace/a2a-dev/docs/governance/雙機治理憲章.md` |
| iMac 運維排障 | `~/workspace/a2a-dev/docs/operations/iMac-RUNBOOK.md` |
| git merge 協議（分支/PR/合夥人制） | [`docs/git-merge-protocol.md`](docs/git-merge-protocol.md) |

## 開工自檢（MUST）

開始任何變更前：

```bash
git branch --show-current
# 若在 main → 開 feature branch: git checkout -b feat/YYYYMMDD-<desc>
# 例行 SK 產出 → 依 git-merge-protocol §6.4 合夥人制
make ci-gate   # 本地 5 項檢查（快，push 前必跑）
```

## PR 與合夥人制速查

- **Routine 產出**（SK/concepts/templates <300 lines）：`scripts/dev/auto-commit-pr.sh "<msg>" main "<title>"` → 自主 merge
- **重大變更**（憲法/_method/AGENTS/CI/SCHEMA）：只開 PR 等 kaecer review，不自行 merge
- 詳見 [`docs/git-merge-protocol.md`](docs/git-merge-protocol.md) §6.4

## Token Efficiency Rules

- Scoped reads：先 `glob` 確認路徑再讀，避免大目錄掃描
- 不讀 `_inbox_archive.md`（歷史承接，無需載入）
- `/compact` 於獨立子任務之間

## CI 驗證（merge 前必跑）

```bash
make ci-gate   # 對位 GitHub 4 job + actionlint，本地 0.5-1s
```
GitHub `validate-wiki` 6 job 會在 push 後跑（timestamp/audit/size/frontmatter/index/triggers）。
