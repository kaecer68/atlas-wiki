# 升級 SOP — hermes-agent 與 NousResearch 上游同步

> 當 NousResearch/hermes-agent:main 有新 commit，需要把 Plan F 改動與之同步。

## 何時升級？

### 自動觸發

每週一 02:00 UTC（10:00 台北）GitHub Actions 自動跑 `hermes-agent-sync.yml`：
- 無衝突 → 自動 rebase + push + close Issue
- 有衝突 → 自動開 Issue 通知（label: `plan-f-conflict`）

### 手動觸發

到 GitHub Actions 頁面點 "Run workflow"。

### 什麼時候必須手動跑？

- Issue 通知「有衝突」
- NousResearch 發布新版本（release tag）
- 你看到 hermes-agent 有重要的 security / feature 更新

## 升級流程

### 1. 檢查衝突

```bash
bash /Users/kk/workspace/atlas-wiki/_internal/hermes-agent-patches/check-conflicts.sh
```

輸出範例：
```
→ 衝突檢查（mode=default）

  ✅ agent/prompt_builder.py
  ❌ agent/system_prompt.py (衝突)
  ℹ️  hermes_cli/banner.py (上游改動)

⚠️ 發現 1 個衝突
建議：bash sync-hermes-agent.sh --rebase
```

### 2. 重新 rebase（手動衝突解決）

```bash
bash /Users/kk/workspace/atlas-wiki/_internal/hermes-agent-patches/sync-hermes-agent.sh --rebase
```

腳本會：
1. fetch origin + fork
2. 預檢衝突（5 個關鍵檔案）
3. `git rebase origin/main`
4. 若有衝突 → 提示手動解衝突
5. 跑 atlas-wiki `make ci-strict`（驗證）

### 3. 手動解衝突

rebase 衝突時，git 會把衝突檔案標 `UU`（both modified）。

```bash
# 看衝突檔案
git status

# 編輯衝突檔案（保留 Plan F 的功能，採用上游的 bug fix）

# 加衝突解決後的檔案
git add <file>

# 繼續 rebase
git rebase --continue
```

### 4. 完整同步 + push

```bash
bash /Users/kk/workspace/atlas-wiki/_internal/hermes-agent-patches/sync-hermes-agent.sh
```

腳本會自動：
1. rebase
2. 跑 `make ci-strict`
3. push 到 fork
4. （可選）開新 PR

### 5. 驗證

```bash
HERMES_TASK=task-coding hermes prompt-size --task task-coding
# 應該顯示 219 chars / 2 skills
```

## 衝突處理原則

### 5 個關鍵檔案優先保留 Plan F 改動

| 檔案 | Plan F 改動 | 上游改動衝突時 |
|---|---|---|
| `agent/prompt_builder.py` | status/tier 過濾 + per_task | 保留 Plan F，解衝突時採用上游結構但保留功能 |
| `cron/scheduler.py` | HERMES_TASK 自動設 | 保留 Plan F，加到 scheduler.py 的 AIAgent 建構前 |
| `hermes_cli/main.py` | _auto_set_* 函式 | 保留 Plan F |
| `hermes_cli/prompt_size.py` | --task 參數 | 保留 Plan F |
| `hermes_cli/subcommands/prompt_size.py` | argparse 註冊 | 保留 Plan F |

### 若上游重構了同個函式

例如上游改了 `_apply_tier_caps`：
1. 先看上游改動（diff）
2. 把我們的 status/tier 邏輯移到上游的新位置
3. 跑 `make ci-strict` 驗證

### 若上游改了我們 patch 涵蓋的檔案

例如上游改了 `prompt_builder.py` 整個檔案：
1. 解衝突時，採用上游版本
2. 手動把我們的 Plan F 邏輯從 backup 重新套用
3. 跑 `make ci-strict`

## 升級後的 PR

衝突解決後：
```bash
# 若 push 到 fork，需要在 NousResearch 開新 PR（自動偵測）
gh pr create --repo NousResearch/hermes-agent   --base main --head kaecer68:plan-f-tier-index-runtime   --title "feat(runtime): rebase Plan F 護欄 to upstream <version>"   --body "自動 rebase 後的 PR"
```

## CI 整合

`.github/workflows/hermes-agent-sync.yml`：
- 排程：每週一 02:00 UTC
- 觸發：workflow_dispatch（手動）
- 衝突偵測：自動開 Issue
- 自動 rebase：無衝突時自動 push

權限需求：
- `secrets.HERMES_FORK_TOKEN`：GitHub PAT with `repo` scope（寫 fork 權限）

## 故障排除

| 症狀 | 原因 | 處置 |
|---|---|---|
| rebase 衝突太多 | 上游大量改動 | 從 backup `.plan-f-backup/` 還原，重新 cherry-pick 我們的 5 個檔案 |
| push 被拒 (non-fast-forward) | fork 與本地不同步 | `git pull fork plan-f-tier-index-runtime` |
| push 被拒 (workflow 權限) | GitHub Actions 沒 workflow scope | 在 Settings → Secrets 加 HERMES_FORK_TOKEN |
| ci-strict 失敗 | Plan F 與 atlas-wiki 規範不同步 | 看失敗訊息，更新 atlas-wiki |

## 與安裝的關係

- 首次安裝：`install.sh`
- 後續升級：`sync-hermes-agent.sh`
- 衝突檢查（CI）：自動

詳見 [INSTALL.md](INSTALL.md) 與 [MAINTENANCE.md](MAINTENANCE.md)。
