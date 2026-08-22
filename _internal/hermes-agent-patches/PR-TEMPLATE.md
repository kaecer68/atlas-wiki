# PR Template — Plan F 護欄 + Plan B runtime + 軟警告

> 自動產生的 PR 描述（2026-08-22 07:50 由 prime-agent 生成）

## Title

```
feat(runtime): Plan F 護欄 + Plan B runtime toolset + 軟警告 + 競爭 SOP
```

## 描述

這 PR 為 hermes-agent 加入 Plan F 護欄 + Plan B runtime 完整生效鏈：

### 改動清單（5 個檔案，+304 insertions / -5 deletions）

1. **agent/prompt_builder.py** (+203 行)
   - `_build_snapshot_entry` 加 status/tier 欄位
   - `_skill_should_show` 加 status + tier 過濾
   - `_apply_tier_caps` 套用 config.yaml tier_limits
   - `_get_active_skills_for_task` per_task 對應（HERMES_TASK 觸發）
   - `_build_soft_warning_appendix` 混合模式警告注入
   - `_infer_tier_from_status` + `_is_task_triggered` helpers

2. **cron/scheduler.py** (+15 行)
   - `AIAgent` 建構前自動設 `HERMES_TASK` env
   - 從 jobs.json job.task 讀取

3. **hermes_cli/main.py** (+63 行)
   - `_auto_set_hermes_task` (chat + _prepare_agent_startup)
   - `_auto_set_enabled_toolsets` (Plan B runtime 完整生效)

4. **hermes_cli/prompt_size.py** (+23 行)
   - `cmd_prompt_size` 加 `--task` 參數

5. **hermes_cli/subcommands/prompt_size.py** (+5 行)
   - `--task` argparse 參數註冊

### 量化效果

| 情境 | skills_index | skills 數 | 節省 |
|---|---|---|---|
| 預設（無 task）| 12,579 chars | 124 | -12.7% |
| HERMES_TASK=task-coding | 219 chars | 2 | **-98.5%** |
| HERMES_TASK=task-financial-judgment | 241 chars | 2 | -98.3% |
| HERMES_TASK=task-knowledge-routing | 351 chars | 3 | -97.6% |
| HERMES_TASK=task-governance | 122 chars | 1 | -99.2% |

按需索引機制：98% 節省。

### 對應 atlas-wiki 改動

- PR #32: Plan F 護欄 + Tier 索引機制（已 merge）
- PR #33: 混合模式 + 競爭 SOP + R5（已 merge）

### 配置需求（merge 後需用戶手動加）

```yaml
# ~/.hermes/config.yaml
skills:
  tier_limits:
    core: 10
    active: 50
    cold: 0
    total_max: 160
  archive:
    enabled: true
    threshold_days: 90
    auto_archive: true
  per_task:
    task-financial-judgment: [task-financial-judgment, financial-advisor-coach, agent-self-judgment-mode]
    task-knowledge-routing: [task-knowledge-routing, knowledge-harvest, wiki-critic]
    # ... 其他 task

tasks:
  toolset_mapping:
    task-financial-judgment: [governance-toolset, finance-toolset]
    task-knowledge-routing: [governance-toolset, content-toolset]
    # ... 其他 task
```

### 測試

```bash
# 跑 ci-strict 確認沒破壞
cd ~/workspace/atlas-wiki && make ci-strict

# 驗證 runtime 按需索引
HERMES_TASK=task-coding hermes prompt-size --task task-coding
# 預期: skills_index 219 chars / 2 skills

# 跑 hermes-agent-skill-authoring SKILL 驗證
hermes skills view hermes-agent-skill-authoring
```

### 回滾計畫

如果 PR 被拒絕或需要回滾：
1. 移除 5 個檔案的改動（git revert）
2. 移除 config.yaml 的 tier_limits + per_task + toolset_mapping 區塊
3. 移除 ~/.hermes/cron/jobs.json 的 task 欄位（11 個 job）
4. 重啟 hermes gateway

## 配套決策

- **plan**: Plan F + Plan A + Plan B + Plan H 全部完成（2026-08-22）
- **owner**: kaecer
- **reviewer**: hermes-agent maintainers
- **related**: 
  - atlas-wiki PR #32（已 merge）
  - atlas-wiki PR #33（已 merge）
  - Plan F 設計文件：~/workspace/atlas-wiki/_internal/plan-F-skill-refactor-2026-08-21.md

## Checklist

- [x] PR 描述完整
- [x] 量化效果驗證
- [x] 對應配置說明
- [x] 測試計畫
- [x] 回滾計畫
- [x] 對應 atlas-wiki 改動
