---
title: SK-13 排列重要性（變數重要性）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-13
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, backtest_signals, risk_get_metrics, experiment_diff]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 sklearn.inspection.permutation_importance(OLS 模型,n_repeats=10) 跑 top10 重要因子:**f32(0.252)/f11(0.221)/f42(0.214)/f59(0.211)/f20(0.207)/f25(0.192)/f39(0.164)/f02(0.127)/f29(0.124)/f05(0.122)**;台股月度 + n_repeats=5 預設值不夠,建議 30-50(誠實標);atlas 端沒「特徵排名」端點,需評估是否提案給 atlas-go 開 `feature_importance` endpoint。
---

## 一句話定位
SK-13 在 atlas 是「哪個因子真有用」的黑盒問答——把每個因子打亂看模型掉多少分,比線性係數更可靠,且適用任何模型(不只線性)。

## 論文版概念（忠實還原來源）
- **核心**:permutation importance =「基準分數 − 打亂某特徵後的分數」,重複 n_repeats 次平均
- **輸入**:已訓練 model、X_test、y_test、`n_repeats=5`、`metric='R2'`
- **動作**:
  1. 算基準分數 score_base
  2. 對每個特徵 j,重複 n_repeats 次:隨機打亂 j 列 → 算新分數 → importance[j] += (score_base - new_score)
  3. 平均 importance,排序
- **輸出**:DataFrame(feature, importance, rank)
- **優於線性係數**:不假設線性關係、不受特徵尺度影響
- **缺點**:對高度共線特徵 importance 會被低估(打亂一個共線特徵另一個還能撐住)

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 已訓練 model | atlas 沒原生 ML 訓練 → client 端 sklearn 訓練 | 缺(client) |
| X_test 多欄特徵 | 股票多維特徵 | `stock_get_fundamentals` + `stock_get_technical` |
| y_test 真實報酬 | backtest 序列 OOS y | `backtest_signals` |
| 評估指標分數 | risk metrics | `risk_get_metrics` |
| 因子刪除後效果 | **atlas 無原生 by-factor ablation**(SK-22 部分對位,PR #1443,2026-08-02):實驗級 metric delta 可用(`experiment_diff` 回 acceptance_metric/baseline_value/candidate_value/+eval_metrics),by-factor 排除式邊際貢獻仍不提供;替代路徑 = `/api/dashboard/pnl-attribution` FactorAttribution(描述性歸因)或 Darwinian 多輪 + `strategy_ranker` 觀察 hit_rate(詳見 `SK-22-ablation-analysis.md`) |

**差異點**:論文是「模型已存在 → 算重要性」,atlas 是「client 端訓練模型 → 用 atlas 端工具組裝 X 與 y → client 端算 importance」。**factor library 在 client 端,importance 也在 client 端,atlas 端只負責資料供應**。

**沒有對位的部分**:
- 沒有「模型訓練」endpoint(client 端 sklearn / xgboost / lightgbm)
- 沒有「permutation importance」endpoint
- 沒有「特徵排名」單一 endpoint

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「86 個因子真的每個都有用嗎?」 → 反問「打亂某個因子,如果模型掉分很多,代表該因子真有用;如果分數不動,代表是雜訊」。permutation 是「對模型說實話」的方式。
- **R 段**:對位 atlas → 「client 端用 sklearn 訓練模型 → 用 `backtest_signals` 拿 OOS y 對齊 X → 跑 `permutation_importance(n_repeats=10)` → 看 top-10 因子」。
- **+E 段**:警示「**top-1 因子若是你聽過的(像本益比),代表你用的可能是公開 alpha,機構已經搶完,實盤 alpha 會被套利磨平**;top-1 若是冷門因子(像『過去 12 個月最大回撤』),才有可能是真 alpha」。**這是散戶最容易忽略的「因子新鮮度」訊號**。
- 對位 ATLAS_METHODOLOGY 七時期:同一因子的 importance 在不同 regime 差很多,**散戶要的是「這個 regime 下最重要的因子」,不是「全期平均 top-10」**。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` + `stock_get_technical` 拼出 18 欄 X,從 `backtest_signals` 拿 OOS y,client 端 train/test split 8:2。
> ⚠️ 本 Step 用隨機切分僅為演示 API；正式評估必走 SK-03 滾動時序切分,隨機切分在時間序列有前視洩漏 [2026-08-22 audit-fix]
Step 2: client 端跑 `permutation_importance(model, X_test, y_test, n_repeats=10, scoring='r2')`。
Step 3: 看 top-10 因子,**人工檢查是否有「冷門訊號」在前 5 名**;若 top-5 全是本益比/殖利率/MACD 這類大路貨,在 wiki 標「public alpha,實盤可能失效」。

## 未消化 / 待補
- [ ] atlas 沒有「特徵排名」端點,需評估是否要提案給 atlas-go 開 `feature_importance` endpoint。
- [ ] 共線性問題:SK-13 在高共線特徵下 importance 會被低估,atlas 端能否提供「相關性矩陣」快速篩掉冗餘?`risk_get_correlation_matrix` 是策略層,不是特徵層。
- [ ] 與 SHAP / LIME 的差異:permutation 是 global importance,SHAP 是 per-prediction;散戶需不需要 SHAP?atlas 端缺。
- [ ] n_repeats=5 預設值是否足夠?學術建議 30-50 次,需實測確認。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Permutation Importance 排列重要性需對位 regime 內 vs 跨 regime 差異)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)