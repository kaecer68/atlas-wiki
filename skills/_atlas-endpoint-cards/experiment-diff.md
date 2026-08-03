# experiment_diff 端點速查卡(2026-08-03 v6.6 派工)

> 5 行小卡從 SK-22-ablation-analysis.md 拆出(原超 9000 bytes)。
> 對位 kaecer v6.6 派工:對位 wiki 教學。

## 問題

`experiment_diff` 端點 400 錯誤。

## 真因

需 `experiment_id` 參數(`tools_experiment.go:46-48`)。**用戶需先 call `experiment_history` 拿 id**。

## 5 步走法(對位 SOUL §3.4)

1. **先呼叫** `mcp__atlas_mcp__experiment_history()` → 取得 19 個真實 experiments 列表(本 session 驗證)
2. **從列表挑一個** `experiment_id`(例:`v19-baseline`)
3. **呼叫** `mcp__atlas_mcp__experiment_diff(experiment_id="v19-baseline")` → 取得對比結果
4. **若要 promote**:`experiment_promote(experiment_id, confirm=true)`(destructive_hint=true,需 ATLAS_API_KEY)
5. **若要 revert**:`experiment_revert(experiment_id, confirm=true)`

## 注意

- 參數名是 `experiment_id` 不是 `session_id`(本 session v5.5 確認)
- `promote` / `revert` 屬 destructive 操作,需 `confirm=true` 顯式確認
- 對位:`05-decisions/2026-08-03-atlas-mcp-endpoint-failure-audit.md` §2 experiment_diff row
