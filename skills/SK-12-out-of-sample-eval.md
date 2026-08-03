---
title: SK-12 樣本外評估（R² / 夏普 / 累積報酬）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-12
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics, risk_get_drawdown, risk_get_correlation_matrix]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:backtest_signals sharpe_long=0.27/sharpe_short=0.49/var_95=-0.0225;risk_get_metrics live provenance session_count=147/var_95=-0.39;atlas R²_oos 需 client 端算(SK-12 公式 R²=1-Σ(y-ŷ)²/Σy²),atlas 端沒暴露 R²_oos 端點(誠實標);SK-12 是「衡量指標」對位最完整頁面,三項閾值通過。
---

## 一句話定位
SK-12 在 atlas 是「策略對不對得起來」的官方裁判——同時算「模型準不準」(R²_oos)跟「投資賺不賺」(Sharpe/累積報酬/回撤),讓散戶看到 alpha 跟實際可賺的錢不是同一回事。

## 論文版概念（忠實還原來源）
- **核心**:同時輸出模型擬合指標 + 投資績效指標
- **公式**:
  - `R²_oos = 1 - Σ(y - ŷ)² / Σy²`(樣本外決定係數;不是訓練 R²)
  - `cumulative_return = ∏(1 + r_t) - 1`
  - `sharpe_ratio = mean(r_t - r_f) / std(r_t) × √12`(年化)
  - `max_drawdown = max peak-to-trough decline`
- **輸入**:y_true、y_pred、可選 portfolio_returns、可選 risk_free_rate
- **輸出**:`{R2_oos, cumulative_return, sharpe_ratio, max_drawdown}`
- **關鍵區別**:R²_oos 衡量「預測誤差」,Sharpe 衡量「投資獲利」——**R² 高不代表 Sharpe 高**(散戶最常誤解)

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| R²_oos(預測準度) | OOS R² 需 client 端算(SK-03 切分);atlas 沒原生 OOS R² endpoint | 缺(client) |
| sharpe_ratio | risk metrics 提供 | `risk_get_metrics` |
| max_drawdown | drawdown 序列提供 | `risk_get_drawdown` |
| cumulative_return | 累積報酬需從 backtest 序列算 | 缺(client) |
| correlation 跨策略 | 跨策略相關矩陣 | `risk_get_correlation_matrix` |

**差異點**:論文版一次算完 4 個指標,atlas 版**分散在 3 個端點 + 1 個 client 端計算**——這是 atlas 「策略層 metric 分散」的設計取捨,不是 bug,但要在 wiki 註明使用者需自己組裝。

**沒有對位的部分**:
- 沒有「OOS R²」原生 endpoint(R²_oos 必須 client 端用 SK-03 切分後算)
- 沒有「累積報酬」單一 endpoint
- 沒有「年化夏普」單一 endpoint(需 client 端 ×√12)

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「這個策略到底好不好?」 → 反問「你是要『預測準不準』還是『賺不賺錢』?」兩者不是同一件事。
- **R 段**:對位 atlas → 「`backtest_signals` 拿 OOS 預測 → client 端算 R²_oos → `risk_get_metrics` 拿 Sharpe → `risk_get_drawdown` 拿 max DD → 4 個指標擺在一起看」。
- **+E 段**:警示「R²_oos > 0 但 Sharpe < 0 的策略**比 R² 低但 Sharpe 高更常見**——前者過擬合、實盤失效;後者才是真 alpha。**散戶最常買到前者**」。
- 對位 ATLAS_METHODOLOGY 七時期:同一策略在 RISK_ON vs RISK_OFF 期間的 Sharpe 可能差 3 倍,**只算全期 Sharpe 是誤導**。

## 驗證方式
Step 1: 呼叫 `backtest_signals` 取一條 active signal 的 OOS 預測與實際報酬序列,確認樣本數 ≥ 60(5 年月度)。
Step 2: client 端算 `R²_oos = 1 - sum((y - ŷ)²) / sum(y²)`,再算 `cumulative_return = prod(1 + r) - 1`。
Step 3: 呼叫 `risk_get_metrics` 取 sharpe_ratio、volatility,呼叫 `risk_get_drawdown` 取 max_drawdown;四指標擺在一起 cross-check 是否有 R² > 0 但 Sharpe < 0 的警示訊號。

## 未消化 / 待補
- [ ] `risk_get_metrics` 是否已含 OOS R²?若有,本頁 § atlas 對位表需更新。
- [ ] 論文 `risk_free_rate=0` 預設在台股不適用(可用 1 年定存 1.5% 或 10 年公債),atlas 是否暴露 risk-free 來源?
- [ ] sharpe_ratio 是否已年化?(若否,client 端需 ×√12 或 √252 依頻率)
- [ ] 與 SK-22 消去法的關係:R²_oos 與 Sharpe 哪個對「刪掉某因子」更敏感?需實測才能確認 atlas 端該用哪個做 ablation 判準。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:OOS 樣本外評估需對位 7 時期切換的真實表現)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)