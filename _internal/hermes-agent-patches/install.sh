#!/usr/bin/env bash
# install.sh — Plan F runtime patch 一鍵安裝到 hermes-agent
#
# 用途：對新機器 / 重灌環境時，把 Plan F 護欄 + Plan B runtime + 軟警告 +
#      競爭 SOP 一次性套用到 ~/.hermes/hermes-agent/。
#
# 用法：
#   bash install.sh                    # 自動偵測 hermes-agent 路徑
#   bash install.sh /path/to/hermes-agent
#   bash install.sh --dry-run          # 只預覽不實際改
#   bash install.sh --from <src-dir>   # 指定 payload 目錄
#
# 退出碼：
#   0  成功
#   1  找不到 hermes-agent
#   2  找不到 payload
#   3  git working tree 不乾淨
#   4  套用失敗

set -euo pipefail

DRY_RUN=0
HERMES_AGENT_DIR=""
FROM_DIR=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --from)
            FROM_DIR="$2"
            shift 2
            ;;
        --help|-h)
            sed -n '2,30p' "$0"
            exit 0
            ;;
        *)
            HERMES_AGENT_DIR="$1"
            shift
            ;;
    esac
done

if [[ -z "$HERMES_AGENT_DIR" ]]; then
    HERMES_AGENT_DIR="$HOME/.hermes/hermes-agent"
fi
HERMES_AGENT_DIR="${HERMES_AGENT_DIR/#\~/$HOME}"

if [[ ! -d "$HERMES_AGENT_DIR" ]]; then
    echo "❌ 找不到 hermes-agent 目錄: $HERMES_AGENT_DIR" >&2
    exit 1
fi

if [[ -z "$FROM_DIR" ]]; then
    FROM_DIR="/Users/kk/workspace/atlas-wiki/_internal/hermes-agent-patches/payload"
fi
if [[ ! -d "$FROM_DIR" ]]; then
    echo "❌ 找不到 payload 目錄: $FROM_DIR" >&2
    exit 2
fi

echo "→ hermes-agent: $HERMES_AGENT_DIR"
echo "→ payload: $FROM_DIR"
echo "→ dry-run: $DRY_RUN"

if [[ -d "$HERMES_AGENT_DIR/.git" ]]; then
    cd "$HERMES_AGENT_DIR"
    if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
        echo "❌ git working tree 不乾淨。請先 commit / stash 改動。" >&2
        git status --short
        exit 3
    fi
fi

# 5 個改動檔案 + 對應 payload 名稱
FILES=(
    "agent/prompt_builder.py"
    "cron/scheduler.py"
    "hermes_cli/main.py"
    "hermes_cli/prompt_size.py"
    "hermes_cli/subcommands/prompt_size.py"
)
PAYLOAD_NAMES=(
    "agent_prompt_builder.py"
    "cron_scheduler.py"
    "hermes_cli_main.py"
    "hermes_cli_prompt_size.py"
    "hermes_cli_subcommands_prompt_size.py"
)

for f in "${FILES[@]}"; do
    if [[ ! -f "$HERMES_AGENT_DIR/$f" ]]; then
        echo "❌ 找不到目標檔案: $f" >&2
        exit 1
    fi
done

for src in "${PAYLOAD_NAMES[@]}"; do
    if [[ ! -f "$FROM_DIR/${src}" ]]; then
        echo "❌ 缺少 payload 檔: $FROM_DIR/${src}" >&2
        exit 2
    fi
done

BACKUP_DIR="$HERMES_AGENT_DIR/.plan-f-backup/$(date +%Y%m%d-%H%M%S)"
echo "→ 備份到 $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

if [[ $DRY_RUN -eq 0 ]]; then
    for f in "${FILES[@]}"; do
        mkdir -p "$BACKUP_DIR/$(dirname "$f")"
        cp "$HERMES_AGENT_DIR/$f" "$BACKUP_DIR/$f"
    done
fi

# 覆蓋前警告：若目標檔案與 payload 不同且非 Plan F 版本，提醒先檢查衝突
NEED_OVERWRITE=0
for i in "${!FILES[@]}"; do
    f="${FILES[$i]}"
    src="$FROM_DIR/${PAYLOAD_NAMES[$i]}"
    if ! diff -q "$HERMES_AGENT_DIR/$f" "$src" > /dev/null 2>&1; then
        NEED_OVERWRITE=1
    fi
done
if [[ $NEED_OVERWRITE -eq 1 && $DRY_RUN -eq 0 ]]; then
    echo "⚠️ 部分目標檔案與 Plan F 版本不同，將被覆蓋。"
    echo "   若 hermes-agent 是上游最新版（含上游新改動），請先跑："
    echo "     bash check-conflicts.sh"
    echo "   確認無衝突後再安裝，或用 sync-hermes-agent.sh --rebase。"
    echo ""
fi

echo "→ 套用 5 個檔案"
cd "$HERMES_AGENT_DIR"

for i in "${!FILES[@]}"; do
    f="${FILES[$i]}"
    src="$FROM_DIR/${PAYLOAD_NAMES[$i]}"
    if [[ $DRY_RUN -eq 1 ]]; then
        if ! diff -q "$HERMES_AGENT_DIR/$f" "${src}" > /dev/null; then
            echo "  ℹ️  $f 將被更新（與現有差異）"
        else
            echo "  ✅ ${f}（已相同，無需更新）"
        fi
    else
        if ! diff -q "$HERMES_AGENT_DIR/$f" "${src}" > /dev/null; then
            cp "${src}" "$HERMES_AGENT_DIR/$f"
            echo "  ✅ $f 已更新"
        else
            echo "  = ${f}（已相同）"
        fi
    fi
done

CONFIG="$HOME/.hermes/config.yaml"
if [[ -f "$CONFIG" ]]; then
    echo "→ 更新 $CONFIG"
    if [[ $DRY_RUN -eq 0 ]]; then
        python3 <<'PYEOF'
import yaml, os
config_path = os.path.expanduser("~/.hermes/config.yaml")
with open(config_path) as f:
    cfg = yaml.safe_load(f) or {}

if "skills" not in cfg:
    cfg["skills"] = {}
if "tier_limits" not in cfg["skills"]:
    cfg["skills"]["tier_limits"] = {"core": 10, "active": 50, "cold": 0, "total_max": 160}
if "archive" not in cfg["skills"]:
    cfg["skills"]["archive"] = {
        "enabled": True, "threshold_days": 90,
        "auto_archive": True, "hard_cap": True, "soft_warning": True,
    }
if "per_task" not in cfg["skills"]:
    cfg["skills"]["per_task"] = {
        "task-financial-judgment": ["task-financial-judgment", "financial-advisor-coach", "agent-self-judgment-mode"],
        "task-knowledge-routing": ["task-knowledge-routing", "knowledge-harvest", "wiki-critic", "director-atlas-wiki", "agent-self-judgment-mode"],
        "task-governance": ["task-governance", "mode-escalation", "agent-self-judgment-mode"],
        "task-system-health": ["task-system-health", "mode-debug", "agent-self-judgment-mode"],
        "task-coding": ["task-coding", "mode-debug", "verify-manifest-claim", "agent-no-backload-discipline", "agent-self-judgment-mode"],
        "task-framework-to-mission-mapping": ["task-framework-to-mission-mapping", "mode-research", "knowledge-harvest"],
    }

if "tasks" not in cfg:
    cfg["tasks"] = {}
if "toolset_mapping" not in cfg["tasks"]:
    cfg["tasks"]["toolset_mapping"] = {
        "task-financial-judgment": ["governance-toolset", "finance-toolset"],
        "task-knowledge-routing": ["governance-toolset", "content-toolset"],
        "task-governance": ["governance-toolset"],
        "task-system-health": ["governance-toolset"],
        "task-coding": ["governance-toolset", "coding-toolset"],
        "task-framework-to-mission-mapping": ["content-toolset", "general-toolset"],
    }

if "toolsets" not in cfg:
    cfg["toolsets"] = {
        "governance-toolset": ["file", "delegation", "memory", "terminal", "todo"],
        "finance-toolset": ["session_search", "web", "memory", "file"],
        "content-toolset": ["file", "memory", "web", "session_search"],
        "coding-toolset": ["file", "terminal", "code_execution", "delegation"],
        "reporting-toolset": ["memory", "session_search", "vision", "delegation"],
        "general-toolset": ["session_search", "memory", "todo", "web"],
    }

with open(config_path, "w") as f:
    yaml.safe_dump(cfg, f, default_flow_style=False, sort_keys=False)
print("  config.yaml 已更新")
PYEOF
    fi
else
    echo "⚠️ 找不到 $CONFIG"
fi

JOBS="$HOME/.hermes/cron/jobs.json"
if [[ -f "$JOBS" ]]; then
    echo "→ 更新 $JOBS"
    if [[ $DRY_RUN -eq 0 ]]; then
        python3 <<'PYEOF'
import json, os
jobs_path = os.path.expanduser("~/.hermes/cron/jobs.json")
with open(jobs_path) as f:
    jobs = json.load(f)

skill_to_task = {
    "mcp-tool-interpretation": "task-financial-judgment",
    "task-knowledge-routing": "task-knowledge-routing",
    "task-system-health": "task-system-health",
    "atlas-skill-inbound": "task-knowledge-routing",
    "self-audit-reminder": "task-system-health",
}
name_to_task = {
    "lint": "task-system-health", "健康": "task-system-health",
    "研究": "task-financial-judgment", "followup": "task-system-health",
    "trigger-monitor": "task-system-health", "promotion-gate": "task-system-health",
    "品質": "task-system-health", "knowledge-harvest": "task-knowledge-routing",
}
default_task = "task-system-health"

for job in jobs.get("jobs", []):
    if "task" in job:
        continue
    skill = job.get("skill") or (job.get("skills") or [None])[0]
    name = job.get("name", "")
    task = skill_to_task.get(skill)
    if not task:
        for keyword, t in name_to_task.items():
            if keyword in name:
                task = t
                break
    if not task:
        task = default_task
    job["task"] = task

with open(jobs_path, "w") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=2)
print("  jobs.json 已更新")
PYEOF
    fi
else
    echo "⚠️ 找不到 $JOBS"
fi

if [[ $DRY_RUN -eq 0 ]]; then
    echo "→ 重啟 hermes gateway"
    GATEWAY_PID=$(ps -eo pid,command | grep "hermes_cli.main.*gateway run" | grep -v grep | awk '{print $1}' | head -1)
    if [[ -n "$GATEWAY_PID" ]]; then
        kill -HUP "$GATEWAY_PID"
        echo "  HUP sent to gateway PID $GATEWAY_PID"
    else
        echo "  ⚠️  gateway 未運行"
    fi
fi

echo ""
echo "✅ 安裝完成"
echo ""
echo "驗證："
echo "  HERMES_TASK=task-coding hermes prompt-size --task task-coding"
echo "  → 應該顯示 skills_index ~219 chars / 2 skills"
echo ""
echo "如需回滾："
echo "  cp -r $BACKUP_DIR/* $HERMES_AGENT_DIR/"
