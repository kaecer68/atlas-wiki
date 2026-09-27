# Git Merge Protocol — atlas-wiki

> 完整規範:branch → commit → push → PR → CI → merge → 後處理。
> 對位 CLAUDE.md「分支與 PR 紀律」+ 開源 repo 標配 + 本地 ci-gate 預檢。

## 0. 為什麼需要這份規範

- GitHub Actions 跑一次完整 CI 約 **30-60 秒**。失敗一次需修 → push → 等 30-60 秒 → 失敗再修。3 輪 = 3-5 分鐘空等 + 大量 token 消耗。
- 本地跑 `make ci-gate` 一次約 **0.5-1 秒**。失敗立即看、修、重跑——**比 GitHub CI 快 60-120 倍**。
- 結論:**本地預檢 + push 後只跑一次 CI** 是最省資源的策略。

## 1. Branch 紀律

### 1.1 禁止在 main 直接作業

來源:`~/.claude/CLAUDE.md`「禁止直接 push 到 `main`」 + `AGENTS.md` §0。

例外(只能出現在 repo 初始化時):
- 空 repo 第一次 commit(沒有 base 可 PR,結構性限制)
- 緊急 hotfix(SKIP_CI_GATE=1 git push,後續需補 commit 註明原因)

### 1.2 分支命名

| 類型 | 命名 | 用途 |
|------|------|------|
| feat | `feat/YYYYMMDD-<desc>` | 新功能 / 新 SK 頁 / 新 script |
| fix | `fix/YYYYMMDD-<desc>` | bug 修正 |
| docs | `docs/YYYYMMDD-<desc>` | 純文檔 |
| ci | `ci/YYYYMMDD-<desc>` | CI / workflow 變更 |
| refactor | `refactor/YYYYMMDD-<desc>` | 重構 |

日期前綴防止與其他 worktree / agent 分支混淆。

## 2. Commit 規範

### 2.1 Conventional Commits

```
<type>(<scope>): <subject>

<body>

<footer>
```

**type**:`feat` / `fix` / `docs` / `ci` / `refactor` / `chore` / `test` / `perf`
**scope**(可選):`skills` / `scripts` / `workflow` / `wiki` / `infra`

### 2.2 備份 checkpoint(對位 _method.md 第 5 條備份)

修改 SK 頁或 script **前**備份 `<file>.bak.<YYYY-MM-DD-HHMM>`,修改**後**再加備份——`git diff` 兩個備份 byte-perfect 對位是查改動源頭的標準做法。

## 3. Push 前預檢(本地 ci-gate)

### 3.1 標準流程

```bash
make ci-gate        # 7 項檢查全綠才 push
```

7 項（2026-09-27 依 `Makefile` ci-gate 依賴實測;舊記 5 項）:
`check-timestamp`（第 5 條鐵律;**實測全 37 頁合規,舊記 33**）／`check-audit`（端點 audit,**實測 115 端點,舊記 109**）／`check-size`（SK 頁 ≤9,000B;類別表 = `_method.md` 六條鐵律 6）／`check-skill-structure`（結構,SSOT `skill-page-schema.json`）／`check-frontmatter`（10 欄）／`check-actionlint`（若已裝 actionlint）／`check-skill-index-sync`（**R1+R3+R4**；2026-09-27 起 R4 已補完並併入 ci-gate，`check-skill-index-sync-basic` 降為逃生口 = 只跑 R1+R3）。

### 3.2 預檢 hooks(自動版)

安裝一次,之後全自動:

```bash
make pre-commit-install   # 裝 pre-commit + pre-push hook
```

行為:
- **pre-commit**:若 `skills/SK-*.md` 或 `.github/workflows/*.yml` 變更,在 commit 前跑對應檢查
- **pre-push**:在 push 前跑完整 `make ci-gate` —— 紅燈時 **push 被擋下**

跳過(僅緊急):
```bash
SKIP_CI_GATE=1 git push   # pre-push hook 跳過;push 後 GitHub CI 仍會跑(最終防線)
```

解除 hook:
```bash
make uninstall-hooks
```

### 3.3 一鍵流水線(全自動)

```bash
scripts/dev/auto-commit-pr.sh "feat(skills): 新增 SK-XX" main "PR title"
```

執行:改動偵測 → add → **ci-gate** → commit → push → 開 PR → 等 CI → squash merge → 切回 base + pull。
任一步失敗立即中止。

## 4. PR 規範

### 4.1 PR body 三段(強制)

每個 PR body MUST 含三段(對位 CLAUDE.md「PR body 必含 Summary / Root Cause / Verification」):

```markdown
## Summary
1-3 句描述這個 PR 做什麼 + 為什麼做。對位 _method.md 第 1 條鐵律 spirit。

## Root Cause / 動機
為什麼需要?引用 T3 evidence / issue / 對話節錄 / GitHub commit 引用。

## Verification
- 本地 `make ci-gate` 5 項全綠
- push 後 GitHub CI 9 job(8 驗證 + 通知)全綠
- 對位 _method.md 5 條鐵律清單
```

### 4.2 變更類型 checkbox

PR template(`.github/PULL_REQUEST_TEMPLATE.md`)提供 6 類 checkbox,contributor 必勾一項。

### 4.3 不可停留

PR 建立後 **不可停留**在「compare & pull request」未完成狀態。要嘛 merge、要嘛明確 close 加說明。

## 5. CI 規範

### 5.1 GitHub Actions 觸發

- `push: branches: [main]` → push 到 main 觸發 validate-wiki.yml
- `pull_request: branches: [main]` → 任何 PR 到 main 觸發

### 5.2 10 個 job（2026-09-27 實測 `validate-wiki.yml`:驗證 9 + 通知 1;舊記 4）

驗證:`governance-review-gate`（治理檔需 `kaecer-reviewed` 標籤,見 §6.4.2）／`validate-timestamp-rule`（第 5 條鐵律）／`audit-atlas-endpoints`（atlas-go 稀疏 checkout;**實測 115 端點,舊記 109**）／`skill-structure-check`（段名/段序/禁用標記＋S2/S3/S5/S6/S7 步驟）／`size-check`（SK 頁 ≤9,000B）／`frontmatter-check`（10 欄）／`audit-file-index-sync`（索引同步）／`trigger-template-existence`／`trigger-endpoint-validation`;第 10 個 `notify-telegram`（`if: failure()`）任一失敗才發 Telegram。

### 5.3 Branch protection

- `required_status_checks`:**9 條**(2026-09-27 實測;含 `governance-review-gate`)；`enforce_admins=true`
- `enforce_admins: true` — admin 也要守 linear history
- `required_linear_history: true` — 禁止 merge commit 製造非線性歷史
- `allow_force_pushes: false` — 禁止 force push
- `allow_deletions: false` — 禁止刪 main

### 5.4 Telegram 通知

需設定 GitHub Secrets:
- `TELEGRAM_BOT_TOKEN`(從 `~/.hermes/.env` `TELEGRAM_BOT_TOKEN` 取得)
- `TELEGRAM_CHAT_ID`(8387647295,已預設)

## 6. Merge 規範

### 6.1 Merge method

**只用 squash merge**(`mergeCommitAllowed: false` / `rebaseMergeAllowed: false` / `squashMergeAllowed: true` 已設)。

理由:
- 每 PR 一個 commit,history 乾淨
- revert 簡單(單一 commit revert)
- 避免 merge commit 製造混亂

### 6.2 Merge 流程

```bash
# 標準:squash + 刪分支(GitHub 已設 deleteBranchOnMerge=true,遠端會自動刪)
gh pr merge <N> --squash --delete-branch

# 若 enforce_admins=true 卡住(status check context 不匹配見 §7):
gh pr merge <N> --squash --delete-branch --admin
```

### 6.3 自我合併條件

允許自我合併的條件(全部需滿足):
1. `validate-wiki` 全綠(現 10 job) / 2. 本地 `make ci-gate` 全綠 / 3. PR body 三段(Summary·Root Cause·Verification) / 4. 變更 < 200 lines(超出留 24h 冷卻)。

例外(可立即合併): ~~docs／ci 變更~~ **已由 §6.4.2 取代**（治理檔一律人工 review）；**emergency fix** 仍可即時合併，但 24h 內補 incident report 到 `_self-audit.md`。

### 6.4 合夥人制自主合併（B 方案, 2026-08-15 kaecer 拍板）

> 拍板: kaecer 2026-08-15 決策 T11-B「合夥人制」——hermes 可自主 merge routine 產出, 重大變更走人工 review（原 §6.3 條件對 routine 過嚴）。

#### 6.4.1 Routine 產出（hermes 自主 merge, 不需人工 review）

符合以下**全部**條件的變更 = routine, hermes 可用 `scripts/dev/auto-commit-pr.sh` 一鍵 merge:

1. **變更範圍**限: `skills/SK-*.md`（SK 頁新增/修正）或 `concepts/` 或 `templates/` 或 `skills/_scripts/` 工具修正（**2026-09-27 修正路徑 typo**：舊記 `scripts/_scripts/` 不存在）
2. **CI 全綠**: 本地 `make ci-gate` + GitHub `validate-wiki` 10 job success
3. **變更量**: < 300 lines（比 §6.3 的 200 放寬, 因 SK 頁 quota 產出）
4. **不觸碰**: 憲法 / `_method.md` / `AGENTS.md` / `git-merge-protocol.md` / `.github/workflows/` / `SCHEMA.md`（這些是治理檔, 見 6.4.2）
5. **SK 頁品質**: 對位 `_method.md` 六條鐵律；size **依類別**（SK 9,000B／concepts+entities 30,000B／docs 12,000B／append-only 無硬上限）
6. **執行工具**: `scripts/dev/auto-commit-pr.sh "<msg>" main "<title>"`（自動: ci-gate → commit → push → PR → 等 CI → squash merge）

#### 6.4.2 重大變更（必須人工 review, hermes 只開 PR 不等 merge）

以下**任何一項**觸碰 = 重大變更, hermes **只開 PR**, 等 kaecer review 後 merge:

| 類別 | 檔路徑 |
|---|---|
| 憲法 | `atlas-notes/02-knowledge/constitution-mission.md` (若同步) |
| 規範本體 | `skills/_method.md` + `_method_amendment_history.md` |
| 專案 context | `AGENTS.md` |
| 治理 | `docs/git-merge-protocol.md` / `SCHEMA.md` |
| CI 設定 | `.github/workflows/*` |
| 規模 | 單 PR > 300 lines 或跨 > 5 檔案 |

重大變更流程: hermes 開 PR → 填 §4.1 三段 body → **不自行 merge** → Telegram 通知 kaecer → 等 review。

**2026-09-27 補牙（incident 後）**：本條原無機械強制；當日 **22 個觸碰治理檔的 PR 被自動合併**（慣犯路徑：`auto-commit-pr.sh` 無排除檢查＋`--admin`）。三道防線：**C** `validate-wiki.yml` 新增 `governance-review-gate`：觸碰治理檔而無 `kaecer-reviewed` 標籤 ⇒ 紅燈（已列 required checks）；**D** `auto-commit-pr.sh` Step 6.5：觸碰治理檔或 >5 檔／>300 行 ⇒ 只開 PR 不 merge，並移除 `--admin`；**A** `check-skill-index-sync.py` R3 收窄為「SK 頁新增/刪除 ⇒ 同步 `SK-00-skill-index.md`」（舊版強制改 `AGENTS.md` = 互撞根因）。

**限度（誠實）**：agent 共用單一帳號（`mergedBy` 一律 `kaecer68`）；`required reviewers`／`CODEOWNERS` 不可行（作者不可自審），標籤可被同 token 自貼 ⇒ 屬**留痕**非**授權**；真解需**第二個 bot 帳號**。

#### 6.4.3 合夥人制判斷速查

```
變更範圍 → 是 SK/concepts/templates/scripts 工具?
  ├─ 是 + <300 lines + CI 綠 → routine → auto-commit-pr.sh 自主 merge
  └─ 否 (憲法/規範/AGENTS/CI/SCHEMA) → 重大 → 開 PR 等 kaecer

    或 > 300 lines / 跨 > 5 檔案 → 重大 → 開 PR 等 kaecer
```

#### 6.4.4 後合併自驗（routine 也適用）

- merge 後 60 秒內: 切回 main + `git pull` 確認無衝突
- 每日結算: `_self-audit.md` 記錄當日自主 merge 數量 + 是否有漏 review 的重大變更

## 7. 後合併規範(merge 後動作)

### 7.1 立即動作(merge 後 60 秒內)

```bash
# 1. 切回 base + pull
git checkout main
git pull origin main

# 2. 驗 CI 在 main 上重跑結果
gh run list --limit 1   # 確認 post-merge CI 綠

# 3. 驗證 remote 分支已刪(deleteBranchOnMerge 自動)
git fetch --prune
```

### 7.2 5 分鐘內

| 動作 | 適用情境 |
|------|----------|
| bump tag(MAJOR/MINOR/PATCH) | 對位 §8 版本紀律 |
| 補 `_self-audit.md` 一行 | 跨 session 累積審計日誌 |
| 通知 hermes cron | 若 script 變更被 cron 引用 |

### 7.3 24 小時內

- [ ] PR comment 留 Kaecer 決策依據(若涉及規範變更)
- [ ] wiki index.md 更新(若新增 SK 頁 → 補入 SK-00 索引)
- [ ] `_inbox.md` 更新跨 SK 待辦(若變更影響其他頁)

## 8. 版本紀律(semver)

對位 README.md §版本:
- **MAJOR**(v1.0.0 → v2.0.0):憲章對位 / 鐵律變更 / 結構大改
- **MINOR**(v1.0.0 → v1.1.0):新增 SK 頁 / 新增索引 / 新增 script
- **PATCH**(v1.0.0 → v1.0.1):錯字 / 連結 / frontmatter 補欄 / bug 修

Tag 命名:`v<MAJOR>.<MINOR>.<PATCH>`(例:`v1.1.0`)
Tag 必含 commit 註明:範圍 / 對位 / 風險。

## 9. 緊急繞過

| 情境 | 命令 | 風險 |
|------|------|------|
| pre-push 紅燈但確認 false positive | `SKIP_CI_GATE=1 git push` | push 後 CI 仍跑,最終防線 |
| CI 全綠但 merge 被擋(enforce_admins 衝突) | `gh pr merge --admin` | 保護被覆寫,但保護對其他 PR 仍生效 |
| workflow 變更導致所有 run 壞掉 | `git revert HEAD` + push + 立即開 fix PR | 緊急修復,事後補 incident report |

## 10. 參考

- CLAUDE.md:分支與 PR 紀律、CI preflight gate、Binary freshness gate
- AGENTS.md:§0 開頭必唸、§2 目錄權限、§10 改版守則、§12 對位憲章（報告格式見 mode-reporting skill）
- _method.md:六條鐵律（含 size 類別上限）、frontmatter 10 欄
- hermes skill `github-pr-workflow`:gh CLI 與 git+curl fallback 完整流程
