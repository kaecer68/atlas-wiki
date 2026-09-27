---
title: SK-26 經典策略網路（LSTM/Transformer）
description: "問「用 LSTM／Transformer 預測股價準不準」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-26
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active（快照,client 端 PyTorch 2.13.0 + M1 MPS,200 epochs／17.4 s）:LSTM R²_oos=0.1747（2 層 hidden=128,論文對位）、Transformer R²_oos=0.2419（d_model=128／nhead=4／num_layers=2／dropout=0.1）。[2026-09-27 batch#5 複驗（5 端點:4×200、1×404＋CLI）:「atlas 無原生 LSTM/Transformer」今日**成立**（`\blstm\b`/`\btransformer\b` 在 `*.go` 0 命中;`internal/ml/` 只有 ols/pcr/pls/elasticnet/glm/spline/rf＋`trainer.go`(KFoldSplitter);CLI `-model nn` exit 1）;2026-08-02 的兩個 R²_oos **今日不可重現**（訓練腳本不在本 repo,且未附 OOS 切分協定）⇒ 只能當 client 端快照,不可當 atlas 能力證據;`risk_get_metrics` **無 Sharpe 欄位**,Sharpe 走 `/api/dashboard/agent-observatory`。見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b5）
l3_endpoints_probed:
  - "/api/backtest/signals → 200（全 0/null） (2026-09-27T20:26:19+08:00)"
  - "/api/dashboard/risk → 200（無 Sharpe 欄位） (2026-09-27T20:26:19+08:00)"
  - "/api/dashboard/agent-observatory → 200（5 scorecards） (2026-09-27T20:26:24+08:00)"
  - "/api/scheduler/status → 200（110 jobs） (2026-09-27T20:26:25+08:00)"
  - "/api/rl/status → 404 route not found (2026-09-27T20:26:25+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Policy Network 策略網絡需對位 7 時期切換)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

## 一句話定位
SK-26 是 PPO 用的「策略網路」——LSTM/Transformer 比 MLP(SK-11)更能捕捉時序依賴,**但在金融月度資料上 LSTM 容易過擬合,Transformer 需要極大樣本**。

## 論文版概念
- LSTM(2 層,hidden=128)或 Transformer(num_heads=4, dropout=0.1)
- 輸入:過去 N 期產業特徵(SK-23 輸出)
- 輸出:當期 47 個產業的動作 logits + 價值（47 = 論文口徑;atlas 端 38 桶 = 20 L1 + 18 L2,見 SK-23）
- 與 PPO 整合(SK-24)

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| LSTM/Transformer 訓練 | 完全 client 端(PyTorch) |
| 評估 | `backtest_signals` + `/api/dashboard/agent-observatory`（`risk_get_metrics` 無 Sharpe 欄位,2026-09-27） |

**差異點**:論文版用 LSTM,實務金融樣本量下 Transformer 幾乎一定過擬合。**散戶若樣本 < 1000 期,LSTM 也不行,回去用 MLP**。

**沒有對位的部分**（2026-09-27 複驗成立）:無原生 LSTM/Transformer 端點;無 PyTorch 整合;`internal/ml/` 只有 ols/pcr/pls/elasticnet/glm/spline/rf,無序列模型。

## 散戶解讀
- **G**:用戶問「AI 用哪種模型?」 → LSTM/Transformer 是時序標準答案,但**金融樣本通常不夠撐起這類模型**。
- **+E**:**散戶最常被「Transformer 預測股價」話術騙**——這類研究極高比例在日內/高頻資料(月度樣本不夠),用在月度選股幾乎必輸。 [2026-08-22 驗證:99% 無來源,弱化為定性描述]**樣本量決定模型上限,不是模型決定上限**。
- 對位 ATLAS_METHODOLOGY 七時期:LSTM 對 regime 切換的反應慢(2-3 期才反應過來),Transformer's attention 可能抓錯歷史 regime。

## 驗證方式
Step 1: client 端用 PyTorch 建 `nn.LSTM(input_size=47*4, hidden_size=128, num_layers=2)`,整合到 SK-24 PPO。
Step 2: 訓練 50k steps,call `backtest_signals` 拿序列（今日該端點 `active_signals=null`,2026-09-27T20:26:19+08:00,故序列只能 client 端自產）。
Step 3: 對比 SK-11 MLP-based PPO 的 Sharpe,若 LSTM 沒顯著優於 MLP,代表台股月度樣本不足以支撐 LSTM(預期差距 < 10%)。

### L3 端點實跑（2026-09-27,本 PR）

| 端點 | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/backtest/signals` | 200 | 全 0/null（`active_signals=null`）⇒ 報酬序列今日無處可取 | 2026-09-27T20:26:19+08:00 |
| `/api/dashboard/risk` | 200 | 無 Sharpe 欄位;`session_count`=210 | 2026-09-27T20:26:19+08:00 |
| `/api/dashboard/agent-observatory` | 200 | **5** scorecards（layer 含 `sector`×3／`style`／`superinvestor`）,全部 `overfit_warning=true` | 2026-09-27T20:26:24+08:00 |
| `/api/rl/status` | **404** | `route not found` ⇒ 無 RL/策略網路狀態面 | 2026-09-27T20:26:25+08:00 |
| `/api/scheduler/status` | 200 | **110** jobs,無 LSTM/Transformer/RL job | 2026-09-27T20:26:25+08:00 |
| CLI `go run ./cmd/backtest-pipeline -synthetic -model nn` | **exit 1** | `unknown model "nn"; choose: ols, pcr, pls, elasticnet, glm, rf` | 2026-09-27T20:27 |

**更正（2026-09-27）**

1. 「無原生 LSTM/Transformer 端點;無 PyTorch 整合」**成立**:Go 源碼 `\blstm\b`／`\btransformer\b` **0 命中**;`internal/ml/` 只有 6 個監督式模型＋`trainer.go`（`Model` 介面 `Fit`/`Predict`＋`KFoldSplitter`）;CLI 模型白名單 `ols/pcr/pls/elasticnet/glm/rf`（`-model nn` exit 1）。
2. 2026-08-02 的「LSTM R²_oos=0.1747／Transformer R²_oos=0.2419」**今日不可重現**:訓練腳本不在本 repo,頁面未附 OOS 切分協定 ⇒ 標為 **client 端快照**（不可當 atlas 能力證據,亦不可當可複驗的 OOS 結論;對位 recipe §10 的 in-sample 警告）。
3. 「評估用 `backtest_signals` + `risk_get_metrics`」需改口徑:今日 `backtest_signals` 無序列、`risk` 無 Sharpe（2026-09-27T20:26:19+08:00）⇒ Sharpe 走 `/api/dashboard/agent-observatory`。
4. 「atlas 有 5 個 scorecard agent」為今日唯一可用的模型層評估出口,且全部 `overfit_warning=true`、`statistically_significant=false`（2026-09-27T20:26:24+08:00）—— 引用「模型有效」時必須帶這兩個旗標。

## 未消化 / 待補
- [ ] Transformer 在金融樣本下的最優 num_heads、hidden_size 需 tune。
- [ ] 與 SK-27 量子網路對比:論文已警告量子實務效能更差,SK-26 不引入量子。
- [ ] LSTM hidden_size=128 是論文預設,可能太大,實務 32-64 較穩。
