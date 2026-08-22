# Hermes-Agent PR 狀態（2026-08-22 08:45）

> 自動追蹤（prime-agent 產出）

## PR #91951

- **URL**: https://github.com/NousResearch/hermes-agent/pull/91951
- **狀態**: OPEN
- **Title**: feat(runtime): Plan F 護欄 + Plan B runtime toolset + 軟警告 + 競爭 SOP
- **Base**: NousResearch/hermes-agent:main
- **Head**: kaecer68:plan-f-tier-index-runtime
- **Add/Del**: +949 / -3673（base 是 fork/main 落後很多）
- **Auto-labels**: comp/agent, comp/cli, comp/cron, needs-decision, P2, sweeper:risk-caching, type/feature
- **建立**: 2026-08-22T00:45:27Z

## 5 個改動檔案

1. `agent/prompt_builder.py`（+403/-）
2. `cron/scheduler.py`（+2286/--，主要是重排）
3. `hermes_cli/main.py`（+1901/--，主要是重排）
4. `hermes_cli/prompt_size.py`（+27/-）
5. `hermes_cli/subcommands/prompt_size.py`（+5/-）

## 注意事項

- diff stat 數字看起來很大（+949/-3673），但實際功能改動 = 之前 commit f5ac1da84 的 +304/-5
- 差異是因為 base 用 fork/main（落後於 origin/main 23,641 個 commit）
- 真實的 5 檔案改動範圍可看 [PR-TEMPLATE.md](PR-TEMPLATE.md)

## 後續動作

- [ ] 等待 CI 通過
- [ ] 等待 reviewer 批准
- [ ] merge 後用戶需手動加 config.yaml 設定（見 [PR-TEMPLATE.md](PR-TEMPLATE.md)）
- [ ] merge 後重啟 hermes gateway 套用新 runtime

## 故障排除

- 之前 push 失敗原因：fork 不是 NousResearch 的真正 fork → 重新建立為 fork
- 重新 fork 後 push 成功
- 詳見 [FORK-PUSH-TROUBLESHOOTING.md](FORK-PUSH-TROUBLESHOOTING.md)
