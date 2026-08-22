#!/usr/bin/env bash
# sync-hermes-agent.sh — 從 NousResearch/hermes-agent 拉最新 → rebase → push
#
# 用途：當 NousResearch/hermes-agent:main 有新 commit，需要把我們的
#      Plan F 改動與之同步。流程：fetch → rebase → 跑 ci-strict → push。
#
# 用法：
#   bash sync-hermes-agent.sh              # 完整同步流程
#   bash sync-hermes-agent.sh --check      # 只檢查衝突，不實際 rebase
#   bash sync-hermes-agent.sh --rebase    # 只 rebase，不 push
#   bash sync-hermes-agent.sh --force      # 強制 force push（會覆蓋上游）
#
# 退出碼：
#   0  成功（無衝突 / 已解決 / 已 push）
#   1  找不到 hermes-agent
#   2  找不到 fork remote
#   3  rebase 衝突（需手動解）
#   4  ci-strict 失敗
#   5  push 失敗

set -euo pipefail

# 解析參數
ACTION="full"  # full | check | rebase
FORCE=0
HERMES_AGENT_DIR=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --check)
            ACTION="check"
            shift
            ;;
        --rebase)
            ACTION="rebase"
            shift
            ;;
        --force)
            FORCE=1
            shift
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

# 定位 hermes-agent
if [[ -z "$HERMES_AGENT_DIR" ]]; then
    HERMES_AGENT_DIR="$HOME/.hermes/hermes-agent"
fi
HERMES_AGENT_DIR="${HERMES_AGENT_DIR/#\~/$HOME}"

if [[ ! -d "$HERMES_AGENT_DIR/.git" ]]; then
    echo "❌ 找不到 hermes-agent git 目錄: $HERMES_AGENT_DIR" >&2
    exit 1
fi

cd "$HERMES_AGENT_DIR"

# 檢查 remotes
if ! git remote get-url fork >/dev/null 2>&1; then
    echo "❌ 沒有 fork remote。請先加 fork：" >&2
    echo "   git remote add fork https://github.com/<你的帳號>/hermes-agent.git" >&2
    exit 2
fi

OUR_BRANCH=$(git symbolic-ref --short HEAD)
echo "→ hermes-agent: $HERMES_AGENT_DIR"
echo "→ branch: $OUR_BRANCH"
echo "→ action: $ACTION"

# Step 1: fetch upstream
echo "→ fetch origin + fork"
git fetch origin 2>&1 | tail -3
git fetch fork 2>&1 | tail -3

# Step 2: 檢查衝突（用 diff-tree）
echo ""
echo "→ 衝突預檢"
OUR_HEAD=$(git rev-parse HEAD)
FORK_MAIN=$(git rev-parse fork/main)
ORIGIN_MAIN=$(git rev-parse origin/main)

# 比對 5 個改動檔案
FILES=(
    "agent/prompt_builder.py"
    "cron/scheduler.py"
    "hermes_cli/main.py"
    "hermes_cli/prompt_size.py"
    "hermes_cli/subcommands/prompt_size.py"
)

CONFLICTED=()
for f in "${FILES[@]}"; do
    OUR_HASH=$(git ls-tree HEAD -- "$f" | awk "{print \$3}")
    ORIGIN_HASH=$(git ls-tree origin/main -- "$f" | awk "{print \$3}")
    if [[ -z "$OUR_HASH" || -z "$ORIGIN_HASH" ]]; then
        continue
    fi
    if [[ "$OUR_HASH" != "$ORIGIN_HASH" ]]; then
        # 檢查是改動 vs 改動（衝突）或只是 origin 新增
        if git merge-tree "$ORIGIN_MAIN" "$OUR_HEAD" "$ORIGIN_MAIN" > /tmp/merge-tree 2>/dev/null; then
            if grep -q "^changed in both" /tmp/merge-tree; then
                CONFLICTED+=("$f")
            fi
        fi
    fi
done
rm -f /tmp/merge-tree

if [[ ${#CONFLICTED[@]} -gt 0 ]]; then
    echo ""
    echo "⚠️ 發現衝突檔案（${#CONFLICTED[@]} 個）："
    for f in "${CONFLICTED[@]}"; do
        echo "  - $f"
    done
    if [[ "$ACTION" == "check" ]]; then
        echo ""
        echo "結論：有衝突。建議："
        echo "  1. cd ~/.hermes/hermes-agent"
        echo "  2. git rebase origin/main"
        echo "  3. 解衝突（編輯衝突檔案、git add、git rebase --continue）"
        echo "  4. 跑測試：hermes prompt-size --task task-coding"
        exit 3
    fi
else
    echo "  ✅ 無衝突"
fi

# Step 3: rebase
if [[ "$ACTION" == "full" || "$ACTION" == "rebase" ]]; then
    echo ""
    echo "→ rebase origin/main"
    if ! git rebase origin/main 2>&1 | tail -10; then
        echo ""
        echo "❌ rebase 衝突。請手動解：" >&2
        echo "  1. 編輯衝突檔案" >&2
        echo "  2. git add <file>" >&2
        echo "  3. git rebase --continue" >&2
        exit 3
    fi
    echo "  ✅ rebase 成功"
fi

# Step 4: 跑 ci-strict（從 atlas-wiki）
echo ""
echo "→ 跑 atlas-wiki ci-strict"
ATLAS_DIR="/Users/kk/workspace/atlas-wiki"
if [[ -d "$ATLAS_DIR" ]]; then
    cd "$ATLAS_DIR"
    if ! make ci-strict 2>&1 | tail -15; then
        echo "❌ ci-strict 失敗" >&2
        exit 4
    fi
    echo "  ✅ ci-strict 通過"
    cd "$HERMES_AGENT_DIR"
fi

# Step 5: push 到 fork
if [[ "$ACTION" == "full" ]]; then
    echo ""
    echo "→ push 到 fork"
    if [[ $FORCE -eq 1 ]]; then
        git push fork "$OUR_BRANCH" --force-with-lease
    else
        git push fork "$OUR_BRANCH"
    fi
    echo "  ✅ pushed"
fi

echo ""
echo "✅ 同步完成"
echo ""
echo "下一步："
echo "  1. 驗證：hermes prompt-size --task task-coding"
echo "  2. 若有改動：hermes 重啟"
echo "  3. 若已 push 到 fork：gh pr create --repo NousResearch/hermes-agent --base main --head kaecer68:<branch>"
