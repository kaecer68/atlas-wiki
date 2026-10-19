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
make ci-gate   # 對位 GitHub CI 10 job（9 驗證 + notify-telegram；2026-09-28 實測）+ actionlint，本地 0.5-1s
```
GitHub `validate-wiki` **10 job** 會在 push 後跑（9 驗證：治理檔治理標籤閘門 / timestamp / atlas 端點 audit / size / frontmatter / 內檔索引同步 / SK 結構（含 S2/S3/S5/S6/S7 步驟）/ 12 觸發模板存在 / 12 觸發模板對位端點；＋ notify-telegram）。

## 本機操作陷阱（2026-10-19 實測；先讀再動手）

1. **`pre-push` hook 會拒絕任何「純 ref 操作」** ✗ —— hook 依 **PR-only** 設計（每個 `local_sha` 必須屬於某個 **OPEN PR** 的 head）
   ⇒ `git push --delete origin <branch>`、`git push origin :<branch>` **必然被拒** ✗（與內容無關）。清 ref 請走 API：
   `gh api -X DELETE repos/kaecer68/atlas-wiki/git/refs/heads/<branch>`
2. **`check-actionlint` 在 baseline 即紅** ✗ —— `.github/workflows/validate-wiki.yml:37` 有**既有** shellcheck `SC2086:info`
   ⇒ 本機 `make ci-gate` **恆為 rc≠0**（`make: *** [check-actionlint] Error 1`），**不是你的改動造成** ✓。
   ⇒ 判紅燈一律用**差異法**：同一組檢查先在 baseline（暫存 clone 的 main）跑一次，**兩邊都紅**的才算既有 ✓。
   GitHub CI **不跑 actionlint** ✓。
3. **同機一次只跑一個 CI** ✗ —— 多 lane 同時在同一台跑 `ci-full`／`ci-gate` 會互相搶資源造成**假紅** ✓
   （同族實例：atlas-go `parallel golangci-lint` 非併發安全 ⇒ 已立案 `FU-20261019-06` ✓）。

> 同源教訓（跨 repo 通用）：
> - 判定「分支是否已落地」**不可**只看 `git rev-list --count main..branch` ✗（**squash 合併**會讓它永遠 >0）；
>   看 **PR 是否 MERGED** 或**內容是否已在 main** ✓。
> - 掃 secret 必須**同時**掃三處：**檔案內容 ＋ 歷史 diff ＋ commit message** ✗（`git log -p` 會帶出訊息）；
>   且掃描器要先跑**陽性對照**（先證明抓得到已知值，才可信陰性結果 ✓）。
