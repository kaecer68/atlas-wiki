# 維護 SOP — hermes-agent fork 日常維護

> 維護範圍：Plan F 護欄 + Plan B runtime 改動的日常維護、監控、衝突解決。

## 維護角色

| 角色 | 負責 | 頻率 |
|---|---|---|
| prime-agent (我) | 衝突檢查、rebase 腳本、CI 維護 | 自動 |
| kaecer | Issue 回應、最終 PR 批准 | 事件觸發 |

## 維護清單

### 每日（自動）
- GitHub Actions：`hermes-agent-sync.yml` 每週一 02:00 UTC 自動跑
- 若有衝突 → 自動開 Issue
- 若無衝突 → 自動 rebase + push

### 每週（自動 + 建議人工 review）
- 跑 `bash check-conflicts.sh` 看 fork 與 upstream 差距
- 看 PR #91951 是否有 reviewer comments
- 檢查 Plan F 護欄是否仍生效（`make ci-strict`）

### 每月（人工 review）
- 看 NousResearch/hermes-agent 是否有 Plan F 對應功能被官方採納
- 若有 → 考慮合併 PR 或關閉 fork 改用上游
- 看是否有新 skill/任務類型需要加 per_task 對應

### 季度（戰略 review）
- Plan F 護欄啟用強度檢討（hard_cap / soft_warning 觸發率）
- Plan B runtime 是否達到 98% token 節省目標
- 競爭 SOP 運作成效

## 監控指標

| 指標 | 目標 | 監控方式 |
|---|---|---|
| skills_index chars（預設）| < 14,000 | `hermes prompt-size` |
| skills_index chars（task=）| < 500 | `hermes prompt-size --task task-coding` |
| skill 總數 | < 160（hard cap）| `find ~/.hermes/skills -name SKILL.md \| wc -l` |
| core skills 數 | < 10 | grep status:core ~/.hermes/skills/*/SKILL.md |
| 衝突 PR 解決時間 | < 7 天 | GitHub Issue `plan-f-conflict` |
| hermes-agent 落後 upstream 多少 | < 50 commits | `git log --oneline HEAD..origin/main \| wc -l` |

## 衝突處理 SOP

### 衝突自動開 Issue（GitHub Actions）

`.github/workflows/hermes-agent-sync.yml` 會自動：
1. 比對 5 個關鍵檔案
2. 若有衝突 → 開 Issue（含衝突清單）
3. Issue 標 `plan-f-conflict` label

### 人工處理流程

```bash
# 1. 看 Issue 內容（衝突清單）
gh issue list --label plan-f-conflict

# 2. 本機跑衝突檢查
bash check-conflicts.sh

# 3. rebase + 解衝突
bash sync-hermes-agent.sh --rebase
# 若有衝突 → 編輯衝突檔案
git add <file>
git rebase --continue

# 4. 跑 ci-strict
cd /Users/kk/workspace/atlas-wiki
make ci-strict

# 5. push + close Issue
bash sync-hermes-agent.sh
gh issue close <issue-number> --comment "Fixed in <commit-sha>"
```

## 自動 rebase 失敗處理

GitHub Actions 自動 rebase 失敗時（衝突）：
1. Job 失敗 → 自動開 Issue
2. Issue 標 `plan-f-conflict`
3. 不會自動 push（避免覆蓋本地改動）

處置：
1. 看 Issue
2. 本機 rebase + 解衝突
3. push
4. close Issue

## 升級觸發點

### 自動觸發
- 每週一 02:00 UTC（`hermes-agent-sync.yml`）

### 手動觸發
- 我看到 NousResearch 有重要 PR
- Issue 通知衝突
- 你（kaecer）說「升級」

## 緊急處理

### Scenario A：Plan F 完全壞掉（hermes 啟動失敗）

```bash
# 還原到 Plan F 安裝前
BACKUP=$(ls -t ~/.hermes/hermes-agent/.plan-f-backup/ | head -1)
rm -rf ~/.hermes/hermes-agent
git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent
bash /Users/kk/workspace/atlas-wiki/_internal/hermes-agent-patches/install.sh
```

### Scenario B：NousResearch 大改 `_apply_tier_caps`

1. 取消 `sync-hermes-agent.sh` 的 rebase
2. 手動從 backup `.plan-f-backup/` 取 Plan F 版本
3. 套用上游新結構（手動 patch）
4. 整合 Plan F 邏輯到新位置
5. 跑 ci-strict 驗證

### Scenario C：Plan F 跟上游衝突太多（無法 rebase）

考慮：
1. 放棄我們的 Plan F 改動
2. 改用 NousResearch 未來可能內建的功能
3. 或：建立 plugin（`hermes_cli/plugins/plan_f_guard/`）

## 文件結構

```
/Users/kk/workspace/atlas-wiki/_internal/hermes-agent-patches/
├── 0001-feat-runtime-Plan-F-Plan-B-runtime-toolset-SOP.patch  ← 主力 patch
├── install.sh                                                ← 一鍵安裝
├── sync-hermes-agent.sh                                      ← 一鍵 rebase + push
├── check-conflicts.sh                                        ← 一鍵衝突檢查
├── PR-TEMPLATE.md                                            ← 上游 PR 模板
├── PR-STATUS.md                                              ← PR #91951 狀態
├── FORK-PUSH-TROUBLESHOOTING.md                              ← Push 故障排除
├── INSTALL.md                                                ← 本文件（安裝）
├── UPGRADE.md                                                ← 升級 SOP
└── MAINTENANCE.md                                            ← 維護 SOP（本文件）
```

## 與 CI 的關係

| 流程 | 觸發 | 工具 |
|---|---|---|
| 衝突檢查 | 每週一 02:00 UTC | `hermes-agent-sync.yml` |
| 安裝驗證 | PR 開啟時 | `atlas-wiki ci-strict` |
| 升級驗證 | push 後 | `sync-hermes-agent.sh` 內 ci-strict |
| 文檔同步 | PR merge 時 | 自動 commit 文件到 atlas-wiki |

### CI 前置條件：HERMES_FORK_TOKEN secret（2026-08-22 已建）

`hermes-agent-sync.yml` 依賴 atlas-wiki repo 的 Actions secret **`HERMES_FORK_TOKEN`**
（PAT with `repo` + `workflow` scope，可寫 `kaecer68/hermes-agent` fork）。

**若 secret 失效 / 換 token（每月例行檢查）：**

1. 開 https://github.com/kaecer68/atlas-wiki/settings/secrets/actions
2. 編輯 `HERMES_FORK_TOKEN` → 貼上新的 `gho_` / `ghp_` token
   - 取得方法：iMac 跑 `gh auth token`（印出目前 gh CLI token）
   - 或 GitHub 網頁 → Settings → Developer settings → Tokens (classic) 建 PAT
3. 按 **Update secret**

**無此 secret 的影響**：workflow checkout fork 那步失敗 → 不會自動 rebase/push；
不影響其他流程（衝突不會被誤判為無衝突——job 直接失敗並顯示在 Actions 頁面）。

**驗證 secret 是否就緒：**

```bash
gh secret list -R kaecer68/atlas-wiki   # 應看到 HERMES_FORK_TOKEN
```

## 與 NousResearch 上游的關係

- 我們的改動 patch 存在 `0001-feat-runtime-Plan-F-Plan-B-runtime-toolset-SOP.patch`
- PR #91951 已開，等 reviewer 批准
- 若 merge → 未來 NousResearch 的 release 會包含我們的改動
- 若拒絕 → 永久 fork 維護
- 若部分 merge → 需要 follow-up PRs

## 聯絡窗口

- **prime-agent**：本機 hermes-agent 維護
- **kaecer**：策略決策、PR 批准
- **NousResearch**：上游維護（不可控）

## 緊急聯絡

若 hermes 完全壞掉：
1. 跑 `bash install.sh`（重新安裝 Plan F）
2. 若仍壞 → 還原 backup：`cp -r ~/.hermes/hermes-agent/.plan-f-backup/<latest>/* ~/.hermes/hermes-agent/`
3. 若仍壞 → 重灌 hermes-agent：`rm -rf ~/.hermes/hermes-agent && git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent && bash install.sh`
