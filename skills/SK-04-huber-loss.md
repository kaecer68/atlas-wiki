---
title: SK-04 Huber 損失異常值處理
description: "問「崩盤把回測夏普弄得很難看怎麼辦」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-04
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics]
verification: "2026-09-27 L3 端點實跑 4 端點全 200（http_code + timestamp 見 `l3_endpoints_probed`;明細見 §驗證方式）。實測更正:(1) 頁內「risk_get_metrics live session_count=147」已過時——`/api/dashboard/risk` 今日回 **session_count 210**（第五條鐵律:快照值需附時戳）;(2) `risk_get_metrics`（`/api/dashboard/risk`）今日 **無 sharpe 欄位**（鍵只有 `degraded/gate_mode/risk_snapshot/session_count/source/var_gate`）;`risk_snapshot` 的 `var_95`/`var_99`/`cvar_95` 皆 **0** 但 `insufficient_data=1`（0 = 資料不足，非零風險）,`backtest_signals` 今日 `active_signals: null` 且全 0 → §驗證方式原 Step 1（取 raw_return 序列）與 Step 3（比較處理前後 Sharpe）**今日不可由此兩端點完成**;可用的最近替代是 `/api/backtest/snapshots`（今日 200,20 筆日快照 2026-08-25~09-23,17 筆 `sharpe_short` 非 0,例 2026-08-30 = 2.0948）;(3) **源碼級代理驗證**:`atlas/internal/ml/elasticnet.go` 實作 Huber **重加權**（`UseHuber` 預設 false、`Xi` 預設 **0.9**,與論文 xi=0.9 相同;權重 `w = 1 (|r|≤xi)` / `xi/|r| (|r|>xi)`）,但 MCP／HTTP／`cmd/backtest-pipeline` 皆未暴露該開關、repo 內 0 個測試引用 → 「atlas 端不能做 loss 替換」在 **MCP 視角成立、repo 視角不成立**。歷史:2026-08-01 v0.9 結算跑過 L3 升 active。"
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b1）
l3_endpoints_probed:
  - "/api/dashboard/risk → 200（session_count 210;**payload 無 sharpe 欄位**;`risk_snapshot` = var_95/99、cvar_95 皆 0（`insufficient_data=1`）、max_drawdown_pct 0.722）（2026-09-27T19:27:54+08:00）"
  - "/api/backtest/signals → 200（active_signals null，全 0）（2026-09-27T19:27:54+08:00）"
  - "/api/backtest/snapshots → 200（20 筆日快照,17 筆 sharpe_short 非 0）（2026-09-27T19:30:53+08:00）"
  - "/api/events/calendar → 200（事件日曆可用）（2026-09-27T19:27:54+08:00）"
  - "源碼級代理（無 HTTP 端點）: atlas/internal/ml/elasticnet.go（UseHuber/Xi）（2026-09-27T19:30+08:00）"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Huber 損失需對位 regime 切換,不同 regime 異常值定義不同)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-04 在 atlas 是「異常報酬處理」——把極端市場事件(2020 疫情、2022 升息)的影響從回測序列中按比例壓低,讓長期夏普估計更貼近常態市場。

> ⚠️ **警示 [2026-08-22 audit-fix]**:對回測報酬序列事後變形再算 Sharpe,衡量的是**變形後序列**,不是策略真實可實現 Sharpe。

## 論文版概念（忠實還原來源）
- **核心**:把模型的損失函數從 MSE 換成 Huber Loss:`L_δ(y, ŷ) = 0.5(y-ŷ)² if |y-ŷ|≤δ, else δ(|y-ŷ|−0.5δ)`
- **輸入**:閾值 `xi=0.9`、基底模型 `base_model ∈ {'linear','elasticnet','glm'}`
- **動作**:定義 `huber_loss(y_true, y_pred, xi)` → 替換基底模型損失 → 訓練 → 返回模型
- **適用**:異常值比例 < 50% 的回歸問題;δ→0 時 Huber 趨近 L1(對異常值**最穩健**),δ 越大越接近 MSE(對異常值越敏感) [2026-08-22 audit-fix]
- **論文未提但實務重要**:Huber 處理的是「訓練時異常」,但回測序列的「異常報酬」需另處理(用 winsorize 或 shrinkage)

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 訓練時 Huber Loss | atlas 沒有原生模型訓練 pipeline | 缺(ML 訓練不在 atlas-mcp 範圍) |
| 回測時異常處理 | backtest 序列中可事後處理 | `backtest_signals` |
| 效果驗證 | 對比處理前後 risk metrics | `risk_get_metrics` |
| 閾值 xi | 異常偵測參數 | 缺(無原生 endpoint) |

**差異點**:論文版是 ML 訓練階段的 loss function,atlas-mcp **不提供模型訓練**——atlas 主要是「策略產生器 + 回測引擎」,ML 訓練屬於 client 端責任。SK-04 對 atlas 的真實價值在「回測序列的後處理」(壓平極端報酬),不是訓練階段。

**沒有對位的部分**:
- atlas-mcp 沒有「loss function 替換」能力
- 沒有「異常值偵測」endpoint(需自己算 z-score 或 IQR)
- 「Huber-style 加權」套件:**更正（2026-09-27）** atlas Go 套件層有（`internal/ml/elasticnet.go` 的 `UseHuber`/`Xi`）,但 MCP／HTTP／CLI 皆未暴露,故由 MCP 視角仍為「沒有」

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「2020 3 月大崩盤把我的回測夏普搞得很難看,怎麼辦?」 → Huber 思路:把極端值按比例壓低,讓估計反映「常態市場表現」。
- **R 段**:對位 atlas → 「`backtest_signals` 拿 raw_return 序列 → 自己用 Python 寫 `huber_smooth(return, xi=0.9)` → 再丟 `risk_get_metrics` 算新夏普」。
- **+E 段**:警示「不要過度壓平,xi 太小會把真實崩盤也抹平,風險被低估。**散戶最常犯的錯:為了『夏普好看』而壓平,結果實盤遇到同樣事件沒準備**」。

## 驗證方式
Step 1: 呼叫 `backtest_signals` 取最近一次 supervised pipeline 結果,看 raw_return 序列是否有 |return| > 3σ 的極端值(預期 2020-03、2022 年中會有)。**2026-09-27 實測:此端點今日回 `{"active_signals":null,"var_95":0,"var_99":0,"sharpe_short":0,"sharpe_long":0,"drawdown_pct":0}`,沒有任何報酬序列 → Step 1 今日不可行。** 替代:`/api/backtest/snapshots`（日快照,含 `portfolio_value` 與 sharpe,可用來找極端日,但非逐筆報酬）。
Step 2: client 端實作 `huber_smooth(r, xi=0.9)` 分段 Huber:`|r|≤δ` 為二次方段 `0.5r²`;`|r|>δ` 為線性段 `δ(|r|−0.5δ)`,損失對 |r| 線性增長(相對二次方壓平極端值) [2026-08-22 audit-fix]。
Step 3: 對比 `risk_get_metrics` 在處理前後的 Sharpe / max_drawdown 變化(預期 Sharpe 微升、drawdown 微降,但變化不應過大)。**2026-09-27 實測:`/api/dashboard/risk` 今日**無 sharpe 欄位**（Sharpe 只在 `/api/backtest/signals`／`/api/backtest/snapshots`）→ 端點活著但本步不可行;`max_drawdown_pct`=0.722、`session_count`=210。**

### L3 端點實跑（2026-09-27,本 PR;帶 `X-API-Key`,timeout 6s）

| # | 端點（GET） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/dashboard/risk` | 200 | session_count 210；**無 sharpe 欄位**；risk_snapshot: var_95/99、cvar_95 = 0（insufficient_data=1）、max_drawdown_pct 0.722 | 2026-09-27T19:27:54+08:00 |
| 2 | `/api/backtest/signals` | 200 | active_signals null，其餘全 0 | 2026-09-27T19:27:54+08:00 |
| 3 | `/api/backtest/snapshots` | 200 | 20 筆日快照（2026-08-25~09-23）;17 筆 sharpe_short 非 0（2026-08-30 = 2.0948） | 2026-09-27T19:30:53+08:00 |
| 4 | `/api/events/calendar` | 200 | 7 筆事件（對位 §未消化「實盤事件量化」項） | 2026-09-27T19:27:54+08:00 |

**非 HTTP 的代理驗證（2026-09-27,源碼）**
- `atlas/internal/ml/elasticnet.go`:ElasticNet 座標下降內建 Huber 重加權——`UseHuber`（預設 `false`）、`Xi`（預設 **0.9**,與本頁論文 xi=0.9 相同）,權重 `w = 1 if |r| ≤ xi, else xi/|r|`。
- 該開關在 `cmd/atlas-mcp`、HTTP handlers、`cmd/backtest-pipeline` 皆 **0 引用**,repo 內 `*_test.go` 亦 0 引用 → 能力在 Go 套件層存在,但今日**不可由 MCP／HTTP／CLI 觸發**。
- 因此本頁的 client 端路徑（huber_smooth）今日仍是唯一可執行路徑;若 atlas 之後接線,此頁可直接改指向該模型。

## 未消化 / 待補
- [ ] atlas `backtest_signals` 是否有「異常值標記」欄位?若有可省 client 端計算。（2026-09-27 實測:今日回傳 null/0,無任何序列或標記欄位;改問 `/api/backtest/snapshots` 是否該補 raw return 序列）
- [ ] 論文 xi=0.9 的「90% 分位」表述待釐清——δ 是**尺度參數不是分位數**;實務該用 z-score 動態閾值;atlas 是否暴露分位計算? [2026-08-22 audit-fix]
- [ ] 「實盤遇到同樣事件沒準備」風險的量化方法論:在 atlas `event_calendar` 對位?（2026-09-27 實測:`/api/events/calendar` 200、今日 7 筆事件,欄位含 `expected_flow_impact`/`decay_days`;仍未驗證這些欄位能否量化極端事件,故維持未結）
- [ ] Huber 與 SK-21 排除仙股的關係:兩者都是「樣本穩健性」,是否可共用 endpoint?
