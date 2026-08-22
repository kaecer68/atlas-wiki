# 安裝 SOP — Plan F runtime patch 一鍵安裝

> 對新機器 / 重灌環境時，把 Plan F 護欄 + Plan B runtime + 軟警告 +
> 競爭 SOP 一次性套用到 `~/.hermes/hermes-agent/`。

## 前置需求

- macOS / Linux
- `bash` 4.0+ / `python3` 3.9+
- `hermes-agent` 已 clone 在 `~/.hermes/hermes-agent/`
- `atlas-wiki` 在 `/Users/kk/workspace/atlas-wiki/`（用於讀取 patch）

## 使用場景（重要）

install.sh 適合**新機器 / 重灌環境**，且 hermes-agent 是**全新 clone**（尚未被改動）
或**已含 Plan F** 時使用。

⚠️ 若 hermes-agent 是上游最新版且上游已改動這 5 個檔案：
先跑 `bash check-conflicts.sh` 確認無衝突，或改用 `bash sync-hermes-agent.sh --rebase`
（rebase 保留上游改動 + 套用 Plan F）。

## 安裝流程

### 1. 一鍵安裝（推薦）

```bash
bash /Users/kk/workspace/atlas-wiki/_internal/hermes-agent-patches/install.sh
```

腳本會自動：
1. 備份現有檔案到 `~/.hermes/hermes-agent/.plan-f-backup/<timestamp>/`
2. 套用 patch（修改 5 個檔案）
3. 更新 `~/.hermes/config.yaml`（加 [skills] + [tasks] 區塊）
4. 更新 `~/.hermes/cron/jobs.json`（每個 job 加 task 欄位）
5. 重啟 hermes gateway

### 2. 預覽模式（不安裝）

```bash
bash /Users/kk/workspace/atlas-wiki/_internal/hermes-agent-patches/install.sh --dry-run
```

### 3. 自訂路徑

```bash
bash install.sh /path/to/hermes-agent
```

## 影響範圍

| 檔案 | 改動 | 用途 |
|---|---|---|
| `~/.hermes/hermes-agent/agent/prompt_builder.py` | 加 status/tier 過濾 | Skills 索引按任務過濾 |
| `~/.hermes/hermes-agent/cron/scheduler.py` | HERMES_TASK 自動設 | Cron 任務自動觸發 |
| `~/.hermes/hermes-agent/hermes_cli/main.py` | _auto_set_* 函式 | Chat 入口自動套用 |
| `~/.hermes/hermes-agent/hermes_cli/prompt_size.py` | --task 參數 | 驗證工具 |
| `~/.hermes/hermes-agent/hermes_cli/subcommands/prompt_size.py` | argparse | CLI 介面 |
| `~/.hermes/config.yaml` | [skills] [tasks] 區塊 | 任務→skill 對應 |
| `~/.hermes/cron/jobs.json` | 每 job 加 task 欄位 | Cron 觸發 |

## 驗證

```bash
# 1. 跑 prompt-size 確認按需索引生效
HERMES_TASK=task-coding hermes prompt-size --task task-coding
# 預期: skills_index ~219 chars / 2 skills

# 2. 跑 atlas-wiki ci-strict
cd /Users/kk/workspace/atlas-wiki
make ci-strict
# 預期: all 6 checks passed

# 3. 跑 hermes gateway 重啟
SIGHUP $(pgrep -f "hermes_cli.main gateway" | head -1)
```

## 回滾

```bash
# 找到最近的備份
ls -la ~/.hermes/hermes-agent/.plan-f-backup/

# 還原
BACKUP=$(ls -t ~/.hermes/hermes-agent/.plan-f-backup/ | head -1)
cp -r ~/.hermes/hermes-agent/.plan-f-backup/$BACKUP/* ~/.hermes/hermes-agent/

# 手動移除 config.yaml 的 [skills] [tasks] 區塊
# 手動移除 jobs.json 的 task 欄位

# 重啟 hermes gateway
```

## 故障排除

| 錯誤 | 原因 | 處置 |
|---|---|---|
| `❌ 找不到 hermes-agent` | 路徑錯 | 用 `--hermes-agent-dir` 指定 |
| `❌ 找不到 patch 檔` | patch 沒下載 | 從 atlas-wiki clone 取得 |
| `❌ git working tree 不乾淨` | 有未 commit 改動 | 提交 / stash 那些改動 |
| `❌ patch apply failed` | 程式碼已大幅變動 | 手動 apply 或 sync-hermes-agent.sh |

## 與升級 / 維護的關係

- **首次安裝**：跑 `install.sh`
- **後續升級 NousResearch**：跑 `sync-hermes-agent.sh`
- **衝突檢查（CI）**：每週一 GitHub Actions 自動跑

詳見 [UPGRADE.md](UPGRADE.md) 與 [MAINTENANCE.md](MAINTENANCE.md)。
