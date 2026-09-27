---
title: SK-22 消去法（排除特定因子集）
description: "問「拿掉某因子策略會不會變差」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-22
ingested_at: 2026-08-01
last_updated: 2026-09-18
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [experiment_diff, experiment_history, universe_get_universe_overlap, backtest_signals]
verification: L3 四步全綠(2026-08-07),四端點 200（快照）。實驗級 metric delta ✅(sharpe_like 0.00507→0.00642);by-factor 邊際貢獻 ❌ 結構性缺口(atlas 無 ablation 端點)。[2026-09-27 batch#4:實驗路徑**仍不可用**（diff 404、history 空、signals 全 0）;替代路徑 strategy-ranker／regime/history／darwinian/status 皆 200。見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b4）
l3_endpoints_probed:
  - /api/experiment/history → 200 (2026-09-27T20:13:26+08:00)
  - /api/experiment/diff?experiment_id=exec-growth-momentum-01-1775435882 → 404 (2026-09-27T20:13:26+08:00)
  - /api/dashboard/universe-overlap → 200 (2026-09-27T20:13:26+08:00)
  - /api/backtest/signals → 200 (2026-09-27T20:13:25+08:00)
  - /api/strategy-ranker/rank → 200 (2026-09-27T20:13:54+08:00)
  - /api/regime/history → 200 (2026-09-27T20:13:54+08:00)
  - /api/synergy/darwinian/status → 200 (2026-09-27T20:14:47+08:00)
  - /api/parameters → 200 (2026-09-27T20:13:26+08:00)
---

## 一句話定位

SK-22 在 atlas 是「**因子對策略的邊際貢獻驗證**」——拿掉某因子,看策略績效掉多少。

**重要結論**:atlas **無原生 ablation／`drop_percentage` 工具**(2026-08-02 開發 agent 報告 v2 §C「不新增」);等價能力只到「實驗級 prompt mutation metric delta」,**不是** by-factor 排除。**分流**:散戶看 §散戶解讀;開發者看 §atlas 對位;審計看 §驗證方式 + §未消化。

## 論文版概念（忠實還原 Fin-Skills）

- **輸入**:X(特徵矩陣) + y(目標) + model_constructor + `excluded_factors`
- **動作**:完整 X 訓練 → 評估 → 刪 `excluded_factors` → 重訓 → 算 `drop_percentage = (full − reduced) / full × 100%`
- **輸出 JSON**:`{full_model_performance, reduced_model_performance, drop_percentage}`（預設排除動量 `mom12m`／`mom1m`）
- **論文未提但實務重要**:recursive elimination、交叉驗證下平均 drop、控制其他因子後單獨拿掉。

## atlas 對位

### 對位表

| 論文概念 | atlas 對位 | 工具 |
|---------|-----------|------|
| by-factor `drop_percentage` | ❌ 無 ablation 端點 | — |
| `excluded_fields` metadata | ❌ audit log 無此欄 | experiment_history |
| 實驗級 baseline vs candidate | ✅ PR #1443(383a48b8)後 | experiment_diff |
| 因子集 overlap 評估 | ✅（30 agents／87 warnings,2026-09-27） | universe_get_universe_overlap |
| backtest aggregate metric | ✅ partial(無 by-factor;2026-09-27 全 0) | backtest_signals |

### 論文 vs atlas 關鍵差異

- **論文**:同模型內換 X,算 R² drop;**atlas**:`experiment_diff` 換 prompt,judge 做 scalar 對比。
- **PR #1443 翻轉範圍**只到**實驗級 prompt mutation delta**;by-factor／`excluded_fields`／recursive elimination／fold 平均**均未翻轉**。

### 沒有對位的部分(替代路徑)

| 論文概念 | 替代路徑 |
|---------|---------|
| by-factor `drop_percentage` | pnl-attribution 描述性歸因（`skills/SK-38-pnl-attribution-workflow.md`）／自帶資料 |
| recursive elimination | Darwinian 多輪 + judge |
| cross-validation fold 平均 | `universe_get_sessions` 跨期平均 |
| 與 SK-18 的關係 | 合併為「因子有效性驗證」組合 skill（待立,見 §未消化） |

## 散戶解讀（GROW+ 引用點）

- **G 段**:用戶問「這策略真的有效嗎?」→ 反問「拿掉某個因子,績效會不會掉?」= ablation 對位。
- **R 段(現狀)**:實驗級 metric delta 曾可用（2026-08-07）,**2026-09-27 實測已不可用**;**by-factor ablation 不提供**,走下方替代路徑或 PnL FactorAttribution 描述性歸因。
- **+E 段(風險)**:核心警示「**實驗級 delta ≠ factor alpha**」——prompt mutation 的 delta 可能來自 confounding 因子,須分 regime 看;散戶常犯「回測掉很少就以為該因子不重要」。
- **對位七時期**:消去法用來驗證「regime 切換下哪些因子失效」——RISK_OFF 期動量 drop 遠大於 RISK_ON。

### 替代路徑:Darwinian-ablation(by-factor 不提供時的散戶實務做法)

**前提**:atlas 無 by-factor `drop_percentage` 端點;要觀察「策略何時失效」只能走 Darwinian 多輪 + 跨 regime 對照——**不是嚴格 ablation,但最接近的實務近似**。

| Step | 工具 | 看什麼 | 散戶解讀 |
|------|------|--------|---------|
| 1 觀察期 | `strategy_ranker` | strategies 的 `tier`／`score`／`win_rate`／`alpha_score` | `tier` = Darwinian 生命週期（premium 已驗證／free 觀察中） |
| 2 驗證期 | `strategy_ranker` 跨日連跑 | 特定 strategy `alpha_score` 演化 | 高 alpha 掉到 0 = **支撐它的環境條件變了**（ablation 的近似） |
| 3 歸因期 | `regime_get_history` | 當期 regime／period vs strategy rank 變化 | RISK_OFF 期 rank 急降 = 依賴的因子在熊市失效（間接證據） |

**SOP**:觀察期 → 驗證期 → 歸因期。**已知不可達**:嚴格排除某因子看 delta、跨 fold 交叉驗證、per-symbol factor score（皆需自帶資料 + client 端 ablation）。

## 驗證方式

**舊跑（快照 2026-08-07,不得當現值;明細見 [`_atlas-endpoint-cards/experiment-diff.md`](_atlas-endpoint-cards/experiment-diff.md)）**:①`/api/experiment/history` 200、18 條、18/18 無 `excluded_fields`;②`/api/experiment/diff?experiment_id=exec-growth-momentum-01-1775435882` 200,sharpe_like 0.0050727→0.0064193;③`/api/dashboard/universe-overlap` 200（29 agents／29 rows／86 warnings）;④`/api/backtest/signals` 200（drawdown 0.7220、sharpe_long 0.2689）。

**⚠️ 參數名陷阱(根因)**:`?id=` → `400 experiment_id required`;`?experiment_id=` → 200 ⇒ 400 若明寫欄位名,先試該名再宣告端點缺失（當初誤傳 `session_id` 才誤判「等 atlas 暴露 experiment_list」,端點一直在）。

**⚠️ 2026-09-27**:實驗路徑不可用（見下表）,是**資料不在**非端點消失;描述性歸因替代頁 `skills/SK-38-pnl-attribution-workflow.md`。

### L3 端點實跑（2026-09-27,本 PR;每列附 http_code 與 UTC+0800 時戳）

| 端點（GET 127.0.0.1:18080） | http_code | 今日實測結果 | timestamp |
|---|---|---|---|
| `/api/experiment/diff?experiment_id=exec-growth-momentum-01-1775435882` | **404** | `{"error":"experiment result not found"}`（08-07 為 200） | 2026-09-27T20:13:26+08:00 |
| `/api/experiment/history` | 200 | `{"history":[]}`（08-07 為 18 條） | 2026-09-27T20:13:26+08:00 |
| `/api/dashboard/universe-overlap` | 200 | **30 agents／30 rows／87 warnings**（08-07 為 29/29/86） | 2026-09-27T20:13:26+08:00 |
| `/api/backtest/signals` | 200 | **全 0**（active_signals=null、drawdown 0、sharpe 0）⇒ 08-07 數值不得當現值 | 2026-09-27T20:13:25+08:00 |
| `/api/strategy-ranker/rank` | 200 | top1 `us-tariff-shock-tech`（premium,win_rate 0.85）;多條 alpha_score=0 | 2026-09-27T20:13:54+08:00 |
| `/api/regime/history` | 200 | 今日 regime=RISK_ON、period=consolidation（盤整） | 2026-09-27T20:13:54+08:00 |
| `/api/synergy/darwinian/status` | 200 | 21 agents（多數 dormant） | 2026-09-27T20:14:47+08:00 |
| `/api/parameters` | 200 | 2465 鍵;excluded／ablation／drop_percentage 各 0 命中 | 2026-09-27T20:13:26+08:00 |

**今日結論（皆 2026-09-27 實跑）**
1. **by-factor ablation 缺口不變（第二次獨立複驗）**:atlas 源碼（commit b5108fb）與 `/api/parameters` 2465 鍵對 `ablation`／`drop_percentage`／`excluded_factors` 皆 **0 命中** ⇒ 結構性缺口成立,非參數名問題。
2. **替代路徑今日全部可跑**:strategy-ranker → regime/history → darwinian/status 三步皆 200（§替代路徑 首次 L3 實跑）。

## 未消化 / 待補

- [ ] 與 SK-18 因子 Alpha 合併為「因子有效性驗證」組合 skill(待立)

> **2026-09-27 結案（移出本段）**:「`parameters_get_metadata` 是否支援 user-defined `excluded_fields`」→ **不支援**（`/api/parameters` 2465 鍵,`excluded`／`ablation`／`drop_percentage` 各 0 命中）;候選因子集仍須走 `experiment_promote`。
- [ ] 「交叉驗證下平均 drop」無對位:`experiment_diff` 只回 1 個 id,跨期平均不可用
- [ ] by-factor 排除式邊際貢獻仍 ❌:**結構性缺口**,非參數問題。**2026-09-27 第二次複驗**:源碼 + 參數表皆 0 命中,且 diff 404／history 空 ⇒ 連實驗級 delta 也不可得。替代頁 `skills/SK-38-pnl-attribution-workflow.md`。
