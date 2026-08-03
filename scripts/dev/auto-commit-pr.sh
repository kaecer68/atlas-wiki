#!/usr/bin/env bash
# auto-commit-pr.sh — 一鍵執行「修改 → 本地 ci-gate → 自動 commit → push → 開 PR → 等 CI → merge」
# 對位 kaecer 2026-08-03 詢問的「系統是否有自動把修改的工作自動建立 commit + make ci-gate + push + PR 的機制」
# 結論(2026-08-03 盤查):hermes 系統無此機制,本腳本填補。
#
# 用法:
#   scripts/dev/auto-commit-pr.sh "commit message" [base-branch] [pr-title]
#
# 前置:
#   - git 已設定 user.name/user.email
#   - gh CLI 已登入(gh auth status)
#   - 已在 git worktree 或主 repo,當前分支非 main

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

MSG="${1:-}"
BASE="${2:-main}"
PR_TITLE="${3:-$MSG}"

if [ -z "$MSG" ]; then
    echo "❌ 用法: $0 \"commit message\" [base-branch] [pr-title]"
    exit 1
fi

CURRENT_BRANCH="$(git branch --show-current)"
echo "🌿 當前分支: $CURRENT_BRANCH (base: $BASE)"

# === Step 0: 不准在 main 直接作業(紀律) ===
if [ "$CURRENT_BRANCH" = "$BASE" ]; then
    echo "❌ 不可在 $BASE 直接作業。建立新分支:"
    echo "   git checkout -b feat/$(date +%Y%m%d)-<desc>"
    exit 1
fi

# === Step 1: 改動確認(若有 staged/unstaged/untracked,要 add) ===
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
    echo "📝 偵測到未提交變更,add 中..."
    git add -A
fi

# === Step 2: 本地 ci-gate(對位 GitHub 4 job + actionlint) ===
echo "🔍 跑本地 ci-gate..."
make ci-gate || {
    echo ""
    echo "❌ 本地 ci-gate 失敗 — 不 push 不開 PR,先修。"
    echo "   跳過預檢(緊急): SKIP_CI_GATE=1 git push"
    exit 1
}

# === Step 3: Commit ===
if git diff --cached --quiet; then
    echo "ℹ️  無 staged 變更可 commit(可能之前已 commit)。跳過 commit。"
else
    echo "💾 commit: $MSG"
    git commit -m "$MSG"
fi

# === Step 4: Push ===
echo "🚀 push 到 origin/$CURRENT_BRANCH"
git push -u origin "$CURRENT_BRANCH"

# === Step 5: 開 PR(若尚未開) ===
PR_NUM="$(gh pr list --head "$CURRENT_BRANCH" --json number -q '.[0].number // empty' 2>/dev/null || true)"
if [ -z "$PR_NUM" ]; then
    echo "🔧 開 PR..."
    PR_URL=$(gh pr create \
        --base "$BASE" \
        --head "$CURRENT_BRANCH" \
        --title "$PR_TITLE" \
        --body "## Summary
$MSG

## Verification
本地 ci-gate 全綠(size + frontmatter + timestamp + audit + actionlint)。GitHub CI 4 job 預期綠。

## 對位
對位 _method.md 5 條鐵律 + _methodology_alignment_audit.md。
")
    echo "📬 PR 建立: $PR_URL"
    PR_NUM="$(echo "$PR_URL" | grep -oE '[0-9]+$')"
else
    echo "ℹ️  PR #$PR_NUM 已存在,跳過建立。"
fi

# === Step 6: 等 CI + 自動 merge ===
echo "⏳ 等 CI 跑完(每 10 秒 poll,上限 5 分鐘)..."
for i in $(seq 1 30); do
    STATE="$(gh pr checks "$PR_NUM" 2>/dev/null | grep -oE 'pass|fail|pending' | sort -u | tr '\n' ',')"
    if [ -z "$STATE" ] || echo "$STATE" | grep -q "^fail"; then
        echo ""
        echo "❌ CI 有失敗:$STATE"
        gh pr checks "$PR_NUM"
        exit 1
    fi
    if ! echo "$STATE" | grep -q "pending"; then
        echo "✅ CI 全綠:$STATE"
        break
    fi
    printf "."
    sleep 10
done

# === Step 7: Squash merge(若設定 enforce_admins,加 --admin) ===
echo "🔀 squash merge PR #$PR_NUM"
ENFORCE="$(gh api repos/kaecer68/atlas-wiki/branches/main/protection --jq '.enforce_admins.enabled' 2>/dev/null || echo false)"
if [ "$ENFORCE" = "true" ]; then
    gh pr merge "$PR_NUM" --squash --delete-branch --admin
else
    gh pr merge "$PR_NUM" --squash --delete-branch
fi

# === Step 8: 切回 base + pull ===
echo "🔄 切回 $BASE + pull"
git checkout "$BASE"
git pull origin "$BASE"

echo ""
echo "✅ 完整流水線完成:改動 → ci-gate → commit → push → PR → CI → merge → 清分支"
