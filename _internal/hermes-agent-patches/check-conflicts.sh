#!/usr/bin/env bash
# check-conflicts.sh — 本地快速檢查 fork 與 upstream 衝突
#
# 用途：定期跑或 CI 觸發，確認 Plan F 改動是否與 NousResearch 新版本衝突。
#
# 用法：
#   bash check-conflicts.sh                # 預設檢查 5 個改動檔案
#   bash check-conflicts.sh --all          # 檢查所有檔案
#   bash check-conflicts.sh --json         # JSON 輸出（給 CI 用）

set -euo pipefail

HERMES_AGENT_DIR="$HOME/.hermes/hermes-agent"
HERMES_AGENT_DIR="${HERMES_AGENT_DIR/#\~/$HOME}"

if [[ ! -d "$HERMES_AGENT_DIR/.git" ]]; then
    echo "❌ 找不到 hermes-agent"
    exit 1
fi

cd "$HERMES_AGENT_DIR"

# 解析參數
MODE="default"
for arg in "$@"; do
    case "$arg" in
        --all) MODE="all" ;;
        --json) MODE="json" ;;
    esac
done

# fetch upstream
git fetch origin --quiet 2>&1 || echo "⚠️ fetch origin failed"

# 5 個關鍵檔案
DEFAULT_FILES=(
    "agent/prompt_builder.py"
    "cron/scheduler.py"
    "hermes_cli/main.py"
    "hermes_cli/prompt_size.py"
    "hermes_cli/subcommands/prompt_size.py"
)

if [[ "$MODE" == "all" ]]; then
    # 比對所有 .py 檔案
    FILES=$(git diff --name-only origin/main...HEAD | grep "\.py$")
else
    FILES="${DEFAULT_FILES[@]}"
fi

echo "→ 衝突檢查（mode=${MODE}）"
echo ""

CONFLICTED=()
OUR_HEAD=$(git rev-parse HEAD)
ORIGIN_HEAD=$(git rev-parse origin/main)
MERGE_BASE=$(git merge-base HEAD origin/main 2>/dev/null || echo "")

for f in $FILES; do
    OUR_HASH=$(git ls-tree HEAD -- "$f" 2>/dev/null | awk "{print \$3}")
    ORIGIN_HASH=$(git ls-tree origin/main -- "$f" 2>/dev/null | awk "{print \$3}")

    if [[ -z "$OUR_HASH" || -z "$ORIGIN_HASH" ]]; then
        STATUS="removed-by-upstream"
        continue
    fi

    if [[ "$OUR_HASH" == "$ORIGIN_HASH" ]]; then
        STATUS="same"
    elif [[ -z "$MERGE_BASE" ]]; then
        STATUS="unknown"
    else
        # merge-base 三方比較：只有「雙方都改了同一檔案」才算衝突
        BASE_FILE_HASH=$(git ls-tree "$MERGE_BASE" -- "$f" 2>/dev/null | awk "{print \$3}")
        if [[ -z "$BASE_FILE_HASH" ]]; then
            # 上游新增檔案（base 沒有）
            STATUS="added-by-upstream"
        elif [[ "$BASE_FILE_HASH" == "$OUR_HASH" ]]; then
            STATUS="changed-by-upstream-only"
        elif [[ "$BASE_FILE_HASH" == "$ORIGIN_HASH" ]]; then
            STATUS="changed-by-us-only"
        else
            STATUS="conflict"
            CONFLICTED+=("$f")
        fi
    fi

    if [[ "$MODE" == "json" ]]; then
        printf "{\"file\": \"%s\", \"status\": \"%s\"}\n" "$f" "$STATUS"
    else
        case "$STATUS" in
            same) echo "  ✅ $f" ;;
            conflict) echo "  ❌ $f (衝突)" ;;
            added-by-upstream) echo "  ⚠️ $f (上游新增)" ;;
            removed-by-upstream) echo "  ⚠️ $f (上游刪除)" ;;
            changed-by-upstream-only) echo "  ℹ️ $f (上游改動)" ;;
            changed-by-us-only) echo "  ℹ️ $f (我們改動)" ;;
            *) echo "  ? $f ($STATUS)" ;;
        esac
    fi
done

echo ""
if [[ ${#CONFLICTED[@]} -gt 0 ]]; then
    echo "⚠️ 發現 ${#CONFLICTED[@]} 個衝突"
    echo "建議：bash sync-hermes-agent.sh --rebase"
    exit 2
else
    echo "✅ 無衝突"
    exit 0
fi
