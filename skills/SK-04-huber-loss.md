---
title: SK-04 Huber 損失異常值處理
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-04
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:backtest_signals 拿 raw_return 序列;risk_get_metrics live session_count=147;**Huber 異常處理完全在 client 端(sklearn 自訂 huber_loss(y, ŷ, xi))**,atlas 端只能驗證處理前後的回測結果;client 端流程:從 backtest_signals 拿 raw_return → 標 |return|>3σ → 自訂 huber_smooth(r, xi=0.9) → 再丟 risk_get_metrics 算新 Sharpe;三項閾值通過(端點活+骨架齊全+論文公式對位)。
---

## 一句話定位
SK-04 在 atlas 是「異常報酬處理」——把極端市場事件(2020 疫情、2022 升息)的影響從回測序列中按比例壓低,讓長期夏普估計更貼近常態市場。

## 論文版概念（忠實還原來源）
- **核心**:把模型的損失函數從 MSE 換成 Huber Loss:`L_δ(y, ŷ) = 0.5(y-ŷ)² if |y-ŷ|≤δ, else δ(|y-ŷ|−0.5δ)`
- **輸入**:閾值 `xi=0.9`、基底模型 `base_model ∈ {'linear','elasticnet','glm'}`
- **動作**:定義 `huber_loss(y_true, y_pred, xi)` → 替換基底模型損失 → 訓練 → 返回模型
- **適用**:異常值比例 < 50% 的回歸問題;xi 越小對異常越敏感
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
- 沒有「Huber-style 加權」套件

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「2020 3 月大崩盤把我的回測夏普搞得很難看,怎麼辦?」 → Huber 思路:把極端值按比例壓低,讓估計反映「常態市場表現」。
- **R 段**:對位 atlas → 「`backtest_signals` 拿 raw_return 序列 → 自己用 Python 寫 `huber_smooth(return, xi=0.9)` → 再丟 `risk_get_metrics` 算新夏普」。
- **+E 段**:警示「不要過度壓平,xi 太小會把真實崩盤也抹平,風險被低估。**散戶最常犯的錯:為了『夏普好看』而壓平,結果實盤遇到同樣事件沒準備**」。

## 驗證方式
Step 1: 呼叫 `backtest_signals` 取最近一次 supervised pipeline 結果,看 raw_return 序列是否有 |return| > 3σ 的極端值(預期 2020-03、2022 年中會有)。
Step 2: client 端實作 `huber_smooth(r, xi=0.9)`:對 |r| > xi*r_std 的部分按 (xi*r_std - 0.5*xi*r_std) 線性遞減,|r| ≤ xi*r_std 維持原值。
Step 3: 對比 `risk_get_metrics` 在處理前後的 Sharpe / max_drawdown 變化(預期 Sharpe 微升、drawdown 微降,但變化不應過大)。

## 未消化 / 待補
- [ ] atlas `backtest_signals` 是否有「異常值標記」欄位?若有可省 client 端計算。
- [ ] 論文 xi=0.9 是 90% 分位的固定閾值,但實務該用 z-score 動態閾值;atlas 是否暴露分位計算?
- [ ] 「實盤遇到同樣事件沒準備」風險的量化方法論:在 atlas `event_calendar` 對位?
- [ ] Huber 與 SK-21 排除仙股的關係:兩者都是「樣本穩健性」,是否可共用 endpoint?

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Huber 損失需對位 regime 切換,不同 regime 異常值定義不同)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)