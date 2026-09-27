---
title: SK-38 PnL 歸因工作流(描述性歸因 vs 消去法)
description: "問「這個月賺的錢是哪來的、拿掉某因子會少賺多少」時載入。"
type: skill-inbound
source: Fin-Skills.md §SK-22 未消化缺口(pnl-attribution 替代路徑 / ablation 結構性缺口)
ingested_at: 2026-09-27
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [universe_get_session_detail, strategy_get_attribution, data_get_field_contract, experiment_diff, experiment_history]
verification: 2026-09-27 L3 實跑 5 端點(附 http_code 與 UTC timestamp,§驗證方式);`/api/dashboard/pnl-attribution` 200 且 `factor_attribution` 非空(session-20260927-daily);**誠實界線** —— 不可宣稱「拿掉因子 X ⇒ 少賺 Y」(ablation grep 0 命中)
l3_run_at: 2026-09-27
l3_run_by: prime-agent(PR feat/20260927-sk37-liquidity-and-attribution)
l3_endpoints_probed:
  - "/api/dashboard/pnl-attribution → 200（2026-09-27T16:56:24+08:00）"
  - "/api/strategies/foreign-3day-inflow/attribution → 200（2026-09-27T16:56:24+08:00）(attribution 為空)"
  - "/api/field-contract → 200（2026-09-27T16:56:23+08:00）"
  - "/api/experiment/diff?experiment_id=exec-growth-momentum-01-1775435882 → 404（2026-09-27T16:56:54+08:00）"
  - "/api/experiment/history → 200（2026-09-27T16:56:54+08:00）(history 為空)"
related:
  - skills/SK-22-ablation-analysis.md(缺口來源頁;本 PR 同步更新其未消化條目)
  - skills/SK-13-permutation-importance.md(排列重要性 vs 歸因)
  - skills/SK-18-factor-alpha.md
---

## 一句話定位

問「這個月賺的錢是哪來的」→ atlas 只能給**描述性歸因**;問「**拿掉**某個因子會少賺多少」→ atlas **答不出來**(無 ablation 端點,結構性缺口)。本頁把「能問」與「不能問」的界線釘死。

## 論文版概念

- **描述性歸因(performance attribution)**:把**已實現**損益按因子 / 產業 / 標的拆開,回答「貢獻來自哪裡」。它是相關性描述,**不是**因果。
- **消去法(ablation)**:移除因子 X 重跑,比較 metric delta,回答「沒有 X 會差多少」。它需要**能重跑**,才可能有因果解讀。
- 兩者不可互換。SK-22 論文要的是後者。

| 問題 | 方法 | atlas 支援 |
|---|---|---|
| 錢是誰賺的 / 誰賠的? | 描述性歸因 | ✅ dashboard 端點 |
| 少了這個因子會怎樣? | ablation | ❌ 結構性缺口 |
| 哪個特徵最重要? | permutation importance | 見 SK-13(另一條路) |

## atlas 對位

| 用戶問題 | atlas 路徑 | 現況(2026-09-27 實跑) |
|---|---|---|
| session 的損益拆解 | `GET /api/dashboard/pnl-attribution` | ✅ 200,資料非空 |
| 某策略的歸因 | `strategy_get_attribution` | ⚠️ 200 但 `{"attribution":[]}`,且**性質不同**(見下) |
| 拿掉因子 X 的邊際貢獻 | — | ❌ 源碼 grep `ablation|drop_percentage|excluded_factors` = 0 命中 |
| 實驗級 metric delta | `experiment_diff` / `experiment_history` | ⚠️ 今日 404 / 空 |

**可用來源 = `/api/dashboard/pnl-attribution`(2026-09-27 實跑)**:回傳 `snapshot_time`、`session_id`、`starting_value`、`current_value`、`cumulative_pnl`、`cumulative_return_pct`,以及四組歸因陣列:`agent_attribution` / `sector_attribution` / `factor_attribution` / `symbol_attribution`。

**必讀警語(本頁最重要的對位)**:`factor_attribution` 的 `contribution` **就等於** `avg_score × avg_return`,而且四個因子(momentum / value / quality / agent)的 `avg_return` **完全相同**(本 session 皆 −0.0009157257981763292)。代數驗算:`contribution / avg_return = avg_score`,四個因子與 `total` 皆成立到浮點精度 ⇒ 因子之間貢獻的差異**只反映分數高低**,不是各因子各自的實得損益。另外 `total.contribution`(−0.000275848) **不等於**四因子之和(−0.001204330)。⇒ **不可**把 `contribution` 讀成「這個因子賺了多少」。

**`strategy_get_attribution` 的空值不是 bug,是另一種東西**:handler 回 `{"id":…, "attribution": f.Attribution}`,而 `StrategyFrame.Attribution` 的型別是 `[]string`(`internal/strategy_techniques/frame.go`),內容是歸因**標籤/mode**(`rule_based` | `llm_annotated`),不是損益數字。空 = 該策略沒有 feedback attribution 記錄。⇒ **MCP 工具名稱會誤導**,它不是績效歸因。

**結構性缺口(本 PR 重確認)**:`~/workspace/atlas` 全源碼 grep `ablation|drop_percentage|excluded_factors` → **0 命中**(2026-09-27)。SK-22 的 ❌ 成立,且不因再試參數名而翻轉。

## 散戶解讀

- **可以問**:「這個 session 的錢被哪些標的 / 產業吃掉?」→ 用 `symbol_attribution` / `sector_attribution`。
- **不可以問**:「拿掉 quality 因子我會少賺多少?」→ atlas 沒這個能力;任何這類數字都是編的。
- 看到 `factor_attribution.quality.contribution` 最大,**不等於**「quality 賺最多」——它只是 `avg_score` 較高乘上同一個 `avg_return`。
- 看到 `strategy_get_attribution` 回空,**不要**推論「這策略沒歸因」;它本來就是標籤清單,不是數字。
- 本 session 實測值(2026-09-27 snapshot):`starting_value` 2998577.80 → `current_value` 3096513.80,`cumulative_return_pct` 3.266%;而 `agent_attribution` 只有 etf-rotation-01(9 筆,`total_return` −2.198%)。兩者口徑不同,**不可相加**。

## 驗證方式

### L3 端點實跑(2026-09-27,本 PR;每列附 http_code 與 UTC timestamp)

| # | 端點(GET) | http_code | UTC timestamp | 回傳要點 |
|---|---|---|---|---|
| 1 | `/api/dashboard/pnl-attribution` | 200 | 2026-09-27T08:56:24Z | `session_id=session-20260927-daily`;`snapshot_time=2026-09-27T03:19:19Z`;`factor_attribution` 5 key 非空 |
| 2 | `/api/strategies/foreign-3day-inflow/attribution` | 200 | 2026-09-27T08:56:24Z | `{"attribution":[],"id":"foreign-3day-inflow"}`(空) |
| 3 | `/api/field-contract` | 200 | 2026-09-27T08:56:23Z | 含 `factor_attribution` / `symbol_attribution` / `sector_attribution` / `agent_attribution` |
| 4 | `/api/experiment/diff?experiment_id=exec-growth-momentum-01-1775435882` | **404** | 2026-09-27T08:56:54Z | `{"error":"experiment result not found"}` |
| 5 | `/api/experiment/history` | 200 | 2026-09-27T08:56:54Z | `{"history":[]}` |

- 第 4 列的 404 是**今日實況**:SK-22 記載的 `experiment_id` 今日查不到結果 ⇒ 實驗級 delta 這條路徑本日不可用(不是端點消失,是資料不在)。
- ablation 零命中(源碼 grep,2026-09-27):`grep -rniE 'ablation|drop_percentage|excluded_factors' ~/workspace/atlas --include='*.go' --include='*.yaml' | wc -l` → 0。
- 第 1 列的 `symbol_attribution` 共 7 列,全部 `side: "BUY"`。

### 可重現步驟

Step 1: `curl -s http://127.0.0.1:18080/api/dashboard/pnl-attribution` → 讀 `factor_attribution`。
Step 2: 驗代數:`jq '.factor_attribution | to_entries | map({key: .key, ratio: (.value.contribution / .value.avg_return), score: .value.avg_score})'` → `ratio` 應等於 `score`。
Step 3: `curl -s http://127.0.0.1:18080/api/strategies/foreign-3day-inflow/attribution` → 觀察空陣列,勿當成「無歸因」。
Step 4: 任何 ablation 數值一律標「atlas 無此能力」。

## 未消化 / 待補

- [ ] ablation 端點仍缺(結構性);若 atlas 未來新增,本頁需改寫成正面數值頁。
- [ ] `strategy_get_attribution` 為何空的**根因**(FeedbackStore 是否從未寫入 attribution)本頁只證到 handler 回 `f.Attribution`,未查寫入端。
- [ ] `contribution = avg_score × avg_return` 是本次由實跑值**反推**的代數關係;atlas 文件未定義該欄位語意,待 atlas 端確認。
- [ ] `agent_attribution` / `sector_attribution` 與 `cumulative_return_pct` 的口徑差異未定義(−2.198% vs +3.266%)。
