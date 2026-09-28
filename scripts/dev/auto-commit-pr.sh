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

# === Step 6.5: 治理檔／規模閘門（2026-09-27 kaecer 拍板；對位 git-merge-protocol §6.4.2）===
# 觸碰治理檔、或規模超標（>5 檔 / >300 行）⇒ 只開 PR，**不自動 merge**，等 kaecer review。
# 治理檔清單＝單一來源（skills/_scripts/governance-files.txt），勿在此硬編第二份
GOV_LIST="$(dirname "$0")/../../skills/_scripts/governance-files.txt"
if [ ! -f "$GOV_LIST" ]; then echo "❌ 找不到治理檔清單 ${GOV_LIST}（不得靜默放行）"; exit 1; fi
# 取 base ∪ head（base 版取自 BASE_REF）：head 刪掉某行不得解除保護（2026-09-28 審查 F2）
GOV_TMP="$(mktemp)"; GOV_BASE="${GOV_TMP}.base"
git show "origin/${BASE}:skills/_scripts/governance-files.txt" > "$GOV_BASE" 2>/dev/null || : > "$GOV_BASE"
cat "$GOV_BASE" "$GOV_LIST" > "$GOV_TMP"
# 清單檔路徑寫死（不可由清單內容移除；base 取不到視為空，避免引進本檔的 PR 自我死結）
GOV_RE="^(skills/_scripts/governance-files\.txt|$(grep -vE '^[[:space:]]*(#|$)' "$GOV_TMP" | sort -u | paste -sd'|' -))"
rm -f "$GOV_TMP" "$GOV_BASE"
# BASE 以「遠端」為準：本地 main 可能落後 origin/main，用本地名會把別人的 commit 算進本 PR
# （2026-09-27 實測：本地落後 3 個 commit 時，真實 2 檔的 routine PR 被判成 24 檔 + 治理檔）
if ! git fetch -q origin "$BASE" 2>/dev/null; then
    echo "⚠️  無法 fetch origin/${BASE}（離線或遠端不可用）⇒ 以本地既有的 origin/${BASE} 判斷；若它已過期，規模判定可能失真。"
fi
BASE_REF="origin/$BASE"
if ! git rev-parse --verify -q "$BASE_REF" >/dev/null 2>&1; then BASE_REF="$BASE"; fi
# base 解析不到就 fail-closed（否則 diff 為空 ⇒ 會被誤判成 routine 而自動 merge）
if ! git rev-parse --verify -q "$BASE_REF" >/dev/null 2>&1; then
    echo "❌ 找不到可比較的 base ref（試過 origin/${BASE} 與 ${BASE}）— 無法判定變更規模，停止，不 merge。"
    exit 1
fi
# 用 --name-status -M：rename 會同時給出舊路徑與新路徑（--name-only 只給新路徑 ⇒ 可繞過閘門）
if ! CHANGED_FILES="$(git diff --name-status -M "$BASE_REF...HEAD" 2>/dev/null \
                       | awk -F'\t' 'NF>1 {for (i=2; i<=NF; i++) print $i}')"; then
    echo "❌ git diff 失敗（BASE_REF=${BASE_REF}）— 停止，不 merge。"
    exit 1
fi
N_FILES="$(printf '%s\n' "$CHANGED_FILES" | grep -c . || true)"
N_LINES="$(git diff --numstat -M "$BASE_REF...HEAD" 2>/dev/null | awk '{a+=$1; d+=$2} END {print a+d+0}')"
if ! printf '%s' "${N_FILES:-}" | grep -qE '^[0-9]+$' || ! printf '%s' "${N_LINES:-}" | grep -qE '^[0-9]+$'; then
    echo "❌ 無法判定變更規模（BASE_REF=${BASE_REF}，N_FILES='${N_FILES:-}' N_LINES='${N_LINES:-}'）— 停止，不 merge。"
    exit 1
fi
if [ "${N_FILES:-0}" -eq 0 ]; then
    echo "❌ diff 為空（BASE_REF=${BASE_REF}）— base 可能選錯或分支無變更；停止，不 merge。"
    exit 1
fi
GOV_HITS="$(printf '%s\n' "$CHANGED_FILES" | grep -E "$GOV_RE" || true)"
MAJOR=0
[ -n "$GOV_HITS" ] && MAJOR=1
[ "${N_FILES:-0}" -gt 5 ] && MAJOR=1
[ "${N_LINES:-0}" -gt 300 ] && MAJOR=1

if [ "$MAJOR" = "1" ]; then
    echo ""
    echo "🛑 偵測到「重大變更」（§6.4.2）— 只開 PR，不自動 merge："
    if [ -n "$GOV_HITS" ]; then
        echo "   治理檔："
        printf '     - %s\n' $GOV_HITS
    fi
    echo "   規模：${N_FILES} 檔 / ${N_LINES} 行（門檻 5 檔、300 行）"
    echo "   PR：$(gh pr view "$PR_NUM" --json url --jq .url 2>/dev/null || echo "#$PR_NUM")"
    echo "   ⇒ 請 kaecer review 後人工 merge（本腳本不再自動 merge 治理檔 PR）。"
    exit 0
fi

# === Step 7: Squash merge（2026-09-27 起移除 --admin：必須 required checks 全綠才可 merge）===
echo "🔀 squash merge PR #$PR_NUM"
if ! gh pr merge "$PR_NUM" --squash --delete-branch; then
    echo "❌ merge 失敗（required checks 未過／遭 branch protection 阻擋，或需要 review）。"
    echo "   PR 保持開啟，請人工處理：$(gh pr view "$PR_NUM" --json url --jq .url 2>/dev/null || echo "#$PR_NUM")"
    exit 1
fi

# === Step 8: 切回 base + pull ===
echo "🔄 切回 $BASE + pull"
git checkout "$BASE"
git pull origin "$BASE"

echo ""
echo "✅ 完整流水線完成:改動 → ci-gate → commit → push → PR → CI → merge → 清分支"
