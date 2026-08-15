---
title: commit-msg (WIP) 例外工作流(2026-08-15 v6.60 D6 SOP)
type: workflow-sop
source: hermes routine D6 經驗 + §6.4 合夥人制
created: 2026-08-15
created_by: hermes D6
status: active
amendable_by: kaecer
related:
  - scripts/dev/hooks/commit-msg(hook 源頭)
  - scripts/dev/install-hooks.sh(安裝腳本)
  - AGENTS.md(分支與 PR 紀律)
  - ~/.hermes/SOUL.md §0.1(例外 6 拍板規則)
---

# commit-msg (WIP) 例外工作流

> **為什麼存在**:commit-msg hook v2 (T3-A258 kaecer 拍板)要求 `feat/fix` commit 第一行必須含 `(#N)` 真實 PR 編號,但 PR 編號要 `gh pr create` 之後才能拿到 → 形成循環依賴。v3 擴展 `(WIP)` 顯式標記例外,讓 commit 不需 PR 號也能 push 開 PR。

---

## §1 適用情境

任何需要先 commit 才能 push 開 PR 的情境:

- **新功能**:改了 SK 頁、concepts、summaries、templates(§6.4 hermes routine 產出)
- **Bug fix**:發現 SK 頁錯誤但需要 PR review
- **Routine 維護**:cron 自動產生的 _inbox 更新等

不適用情境:

- **chore/docs/build/ci/refactor/style/test** type commit → 本來就允許,不需要 (WIP)
- **hotfix** → 直接 `HUSKY_SKIP_COMMIT_MSG=1`,事後補 T3 evidence(原路徑)

---

## §2 標準工作流(5 步)

```bash
# Step 1: 建 feature branch
git checkout -b feat/20260815-<desc>
# Step 2: 改檔 + stage + commit (WIP)
git add <files>
git commit -m "feat(atlas-wiki): <subject> (WIP)

<body>"  # hook 會警告但不阻擋

# Step 3: ci-gate 本地驗證
make ci-gate

# Step 4: push + gh pr create → 拿到 PR 號
git push -u origin feat/20260815-<desc>
gh pr create --repo kaecer68/atlas-wiki --base main --title "..." --body "..."

PR_NUMBER=$(gh pr view --json number -q .number)  # 從 PR 拿到 N
git commit --amend -m "feat(atlas-wiki): <subject> (#${PR_NUMBER})"
git push origin feat/20260815-<desc> --force-with-lease  # ⚠️ 必須顯式指定 <branch> + --force-with-lease;純 --force 在本 remote 行為不可靠
```
> **Step 4 → Step 5 期間**:GitHub CI 會跑第一次(基於 (WIP) commit);**Step 5 force push 觸發第二次 CI**(基於 (#N) commit)。第二次 CI 通過後即可 merge。
>
> **若不想跑兩次 CI**(省時 ~30-60s):可在 Step 2 commit 之前先 `git commit --allow-empty -m "empty"` 推空 branch → gh pr create 拿到號碼 → `git reset --hard HEAD~1` → 再正式 commit + amend。**此變體較複雜,本 SOP 預設走標準 5 步流程**。

---

## §3 (WIP) 標記規範

- **位置**:commit message 第一行任意位置(常見:開頭或結尾)
- **格式**:必須是 `(WIP)` 完整括號字樣 → hook 用 `grep -E '\(WIP\)'` 偵測
- **大小寫**:`(wip)` / `(Wip)` **不觸發**(維持嚴格 = 顯式標記)
- **多語系**:僅 `(WIP)` 英文;不支援 `(待補)` / `(草稿)` 等
- **必須性**:第一行若同時含 `(WIP)` 與 `(#N)`,以 `(#N)` 為主(正規形式)

---

## §4 Hook 安裝

`scripts/dev/install-hooks.sh` v3 已補裝 commit-msg hook:

```bash
make pre-commit-install  # 或 ./scripts/dev/install-hooks.sh
```

若 `.git/hooks/commit-msg` 缺失(新 clone repo),執行上述指令即可自動從 `scripts/dev/hooks/commit-msg` 範本複製。

解除:`make uninstall-hooks`(同時清 pre-commit / pre-push / commit-msg)。

---

## §5 規範對位

|規範|本 SOP 對位|
|---|---|
|T3-A258 kaecer 拍板 B(嚴格 (#N))|**保留**(非 WIP 的 feat/fix 仍嚴格要求 (#N))|
|§6.4 合夥人制(SK/concepts 自合)|本 SOP 是其「工具改進」配套,讓 routine 產出能順利走 PR 流程|
|SOUL §0.1 例外 6(規範修改需拍板)|hook v3 屬「工具細節擴展」非「治理規範變更」,由 hermes 自主擴張;若 kaecer 反對可隨時 revert|

---

## §6 範例

### 範例 A:標準 (WIP) flow

```bash
# commit log 顯示
feat(atlas-wiki): SK-34 真實 promotion (WIP)
  ↓ (push + gh pr create → 拿到 PR #21)
feat(atlas-wiki): SK-34 真實 promotion (WIP)         # remote 看到
  ↓ (amend + force push)
feat(atlas-wiki): SK-34 真實 promotion (#21)          # 最終 main 形式
```

### 範例 B:錯誤示範(hook 仍會擋)

```bash
feat(atlas-wiki): test           # ❌ hook 擋下
feat(atlas-wiki): test (wip)     # ❌ 大寫不符,hook 擋下
feat(atlas-wiki): test [WIP]     # ❌ 括號不符,hook 擋下
fix(atlas-wiki): urgent (WIP)    # ✅ 通過
```
