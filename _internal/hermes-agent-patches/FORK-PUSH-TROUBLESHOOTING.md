# Hermes-Agent Fork Push 故障排除指南

> 自動產生（2026-08-22 08:45）— kaecer 8/22 建立 `kaecer68/hermes-agent` 後 prime-agent 嘗試 push 失敗

## 問題摘要

`git push` 反覆失敗：
```
remote: fatal: did not receive expected object eb20188d2e5c40419c49f8f463061b2342945721
error: remote unpack failed: index-pack failed
```

## 根本原因

- `kaecer68/hermes-agent` 不是 NousResearch 的 fork（建立時沒用「Fork」按鈕）
- GitHub 內部記錄「first commit」hash 為 `eb20188d...`，但 fork 內實際不存在
- 後來用 API 加 README.md（建立 `e95c7b21c`）也無法覆蓋 GitHub cache
- merge unrelated histories 失敗（README.md 衝突）
- 任何 push 路徑都被擋下

## 三選一（推薦選項 1）

### 選項 1：手動刪 fork + 重新用「Fork」按鈕建立（推薦）

1. **GitHub UI** → `https://github.com/kaecer68/hermes-agent/settings`
2. 拉到最下「Danger Zone」→ 「Delete this repository」
3. 確認刪除（輸入 `kaecer68/hermes-agent`）
4. 訪問 `https://github.com/NousResearch/hermes-agent`
5. 右上「Fork」→ 選 owner `kaecer68` → 建立
6. 然後告訴 prime-agent 重新 push

之後 prime-agent 會跑：
```bash
cd ~/.hermes/hermes-agent
git remote remove fork
git remote add fork https://x-access-token:<gh-token>@github.com/kaecer68/hermes-agent.git
git push -u fork feature/20260822-plan-f-tier-index-runtime
gh pr create --repo NousResearch/hermes-agent --base main --head kaecer68:feature/20260822-plan-f-tier-index-runtime --title "..." --body-file PR-TEMPLATE.md
```

### 選項 2：用 gh CLI 拿 delete_repo scope

1. `gh auth refresh -h github.com -s delete_repo`
2. 同意瀏覽器授權
3. `gh repo delete kaecer68/hermes-agent --yes`
4. 然後 `gh repo fork NousResearch/hermes-agent --remote=false`
5. 然後 push

### 選項 3：保留 fork + 用 GitHub API 手動建立 commit（複雜）

```bash
# 1. 建立 blob（每個檔案一個）
# 2. 建立 tree
# 3. 建立 commit
# 4. 建立 ref
# 太複雜，不推薦
```

## 替代方案

如果 GitHub fork push 持續失敗，可以：

- **方案 A**: 把 `0001-feat-runtime-Plan-F-Plan-B-runtime-toolset-SOP.patch`（21,818B）給 kaecer，他自己手動套用
- **方案 B**: 在 atlas-wiki `_internal/hermes-agent-patches/` 開新 git repo，把 patch 與 PR 模板放著
- **方案 C**: 暫時跳過上游 PR，hermes-agent 端改動已在本地運作（`feature/20260822-plan-f-tier-index-runtime` branch）

## 補：本地 branch 狀態

```
~/.hermes/hermes-agent on branch feature/20260822-plan-f-tier-index-runtime
commit f5ac1da84 (5 files changed, +304 insertions)
branch 已 reset 回 f5ac1da84（merge --abort 已清理）
備份 .bak 已清掉
```
