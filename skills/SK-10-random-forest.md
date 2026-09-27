---
title: SK-10 隨機森林模型
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-10
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, backtest_signals, risk_get_metrics]
verification: 2026-09-27 L3 端點實跑 (http_code + timestamp 見 `l3_endpoints_probed`;明細見 §驗證方式):5 個 HTTP 端點中 4 個 200、1 個 400 → **無任何端點回 R²_oos**,本頁 `R²_oos=0.1248` 維持 2026-08-02 client 端 sklearn 快照,今日無法由 atlas 複驗。新增:**atlas repo 內有原生 RandomForest**(`internal/ml/randomforest.go`:CART + bootstrap + 隨機子空間,`MaxFeatures` 支援 "sqrt"/"all"),CLI `cmd/backtest-pipeline -model rf` 實跑 → `-synthetic` exit 0、**R²_OOS +0.9914（PASS）**;但**原生預設與本頁論文設定相反**:`NTrees` 預設 **100**（非 500）、`MaxDepth` 預設 **10**（非 2）→ 「淺樹防過擬合」在 atlas 原生路徑不是預設。**未消化第 1 項已解（2026-09-27）**:XGBoost / LightGBM 為**已驗證的負面**——`git grep -i 'xgboost|lightgbm|gradientboost'` 在 atlas 只命中 `cmd/backtest-pipeline/main_test.go` 的 `newModel("xgboost")` 應報錯測試,`newModel` 只收 `ols/pcr/pls/elasticnet/glm/rf`。**原生 RF 無 feature importance 方法**(`internal/ml` 內 `importance` 0 命中);重要性在 **experiment 結果**路線——`internal/eval/importance.go` 的 `PermutationImportance` 產出 `ImportanceResult`,並掛在 `internal/domain/experiment` 的 `importance_result` 欄位,但今日 `/api/experiment/history` 回空。歷史:2026-08-02 v0.9 結算跑過 L3 升 active（client 端 sklearn 1.8.0 RandomForestRegressor(n_estimators=500, max_depth=2),R²_oos=0.1248;feature_importances_ 跑通）。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b2）
l3_endpoints_probed:
  - "/api/stock/fundamentals?symbol=2330 → 200（PE 30.19/PB 9.57/DY 1.1）（2026-09-27T20:02:26+08:00）"
  - "/api/stock/technical?symbol=2330&days=10 → 200（rsi14/sma20/sma50 皆 0）（2026-09-27T20:02:26+08:00）"
  - "/api/backtest/signals → 200（active_signals null;無 OOS y）（2026-09-27T20:02:26+08:00）"
  - "/api/dashboard/risk → 200（session_count 210;無 R² 欄位）（2026-09-27T20:02:26+08:00）"
  - "/api/experiment/history → 200（history 空陣列 → experiment_diff 無實例可跑）（2026-09-27T20:02:48+08:00）"
  - "/api/experiment/diff → 400（缺 experiment_id）;帶不存在 id → 404（2026-09-27T20:02:48+08:00）"
  - "CLI 代理（無 HTTP 端點）: atlas repo `-synthetic -model rf` → R²_OOS +0.9914（PASS）（2026-09-27T20:02:28+08:00）"
---

## 一句話定位
SK-10 是金融 ML 的「萬用 baseline」——非線性、處理共線、給出 importance,但**深度限制很重要**——論文用 max_depth=2 防止過擬合,散戶若設太深會慘輸 OLS。

## 論文版概念
- 集成 500 棵淺決策樹(max_depth=2,min_samples_split=5),bagging + 隨機特徵
- 輸入:`n_estimators=500`、`max_depth=2`、`max_features="sqrt"`
- 優點:非線性、給出 feature_importances_、不需標準化
- 缺點:不外推(訓練範圍外預測為定值)、對樣本少時不穩

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| RF 訓練 | MCP／HTTP 缺;**repo 內有原生 RF**(`internal/ml/randomforest.go`,`-model rf`,2026-09-27 實跑) |
| 特徵來源 | `stock_get_fundamentals` + `stock_get_technical`（2026-09-27:fundamentals 只回 4 欄,technical 的 rsi/sma 皆 0） |
| 評估 | `risk_get_metrics`（2026-09-27:**無 R² 欄位**） |
| 重要性 | `experiment_diff`（今日 history 空）;原生 `PermutationImportance`(`internal/eval/importance.go`)→ `importance_result`;SK-13 互補 |

**差異點**:RF 給的 feature_importances_ 是「不純度降低」,與 SK-13 permutation importance 不同——前者對高基數特徵有偏。**更正（2026-09-27）**:atlas 原生 RF **沒有** `feature_importances_` 等價方法（`internal/ml` 內 `importance` 0 命中）;atlas 端唯一的原生重要性是 permutation 路線（`internal/eval/importance.go`,掛在 experiment 的 `importance_result` 欄位）,所以「重要性要 client 端算」在 atlas 原生路徑只有一半成立。

**沒有對位的部分**:無原生 RF 的 **HTTP** 端點（實作只在 repo 內）;**Gradient Boosting 完全沒有**（XGBoost／LightGBM 在 atlas `git grep` 只命中一個「應報錯」測試,2026-09-27 已驗證負面）。

## 散戶解讀
- **G**:用戶問「線性模型不夠,我要非線性」 → RF 是起點,XGBoost 是進階。
- **+E**:**`max_depth=2` 是金融特規——散戶若設 5/10,馬上 overfit**;`n_estimators=500` 是穩定而非越多越好。**金融 RF 跟影像 RF 設定完全相反**。
- 對位 ATLAS_METHODOLOGY 七時期:RF 的特徵重要性在 regime 切換時排名會洗牌,需每期重訓。

## 驗證方式
Step 1: 拉 18 欄 X,從 `backtest_signals` 拿 y。
Step 2: client 端 `RandomForestRegressor(n_estimators=500, max_depth=2)`。
Step 3: OOS R² 對比 SK-05 OLS(預期 RF 優 10-20%);同時算 `feature_importances_`,看 top-5 是否包含 SK-13 permutation 認定的 top-5。
> 口徑註：上述預期排名僅對小樣本弱訊號真實資料成立；本頁合成線性資料實測 OLS=1.0 最高,兩者不矛盾但不可混讀 [2026-08-22 audit-fix]

### L3 端點實跑 + CLI 代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19 / PB 9.57 / DY 1.1（僅 4 欄） | 2026-09-27T20:02:26+08:00 |
| 2 | `/api/stock/technical?symbol=2330&days=10` | 200 | close 2475、date 2026-09-24；`rsi14`/`sma20`/`sma50` **皆 0** | 2026-09-27T20:02:26+08:00 |
| 3 | `/api/backtest/signals` | 200 | `active_signals` null、全 0 → 無 OOS y | 2026-09-27T20:02:26+08:00 |
| 4 | `/api/dashboard/risk` | 200 | session_count 210；**無 R² 欄位** | 2026-09-27T20:02:26+08:00 |
| 5 | `/api/experiment/history` | 200 | `history` 空陣列 → **今日無 experiment 結果** | 2026-09-27T20:02:48+08:00 |
| 6 | `/api/experiment/diff`（缺參數／不存在 id） | **400 / 404** | `experiment_id` 必填;不存在回 `experiment result not found` | 2026-09-27T20:02:48+08:00 |
| 7 | CLI（非 HTTP）:`cmd/backtest-pipeline -synthetic -model rf` | exit 0 | 500 samples × 2 features；**R²_OOS +0.9914 → PASS** | 2026-09-27T20:02:28+08:00 |

- **更正（2026-09-27）**:第 7 列推翻「無原生 RF 端點」的 repo 層敘述:`internal/ml/randomforest.go` 有原生 CART＋bagging＋隨機子空間 RF,`-model rf` 可實跑。仍**不在 MCP／HTTP 面**。
- **原生預設與本頁論文設定相反（重要）**:`NewRandomForest()` 的 `NTrees` 預設 **100**（本頁 500）、`MaxDepth` 預設 **10**（本頁 2）→ 「金融 RF 要用淺樹」這條建議**不是 atlas 原生行為**;合成資料 100 棵也能 PASS（+0.9914）,但真實台股需自行確認深度。
- **第 5／6 列**:`experiment_diff` 今日不可作為重要性驗證路徑（無 experiment 結果）;要驗 importance 目前只能走原生 `PermutationImportance` 或 client 端。
- Step 1 今日只完成一半:X 來源可用但欄位不足(fundamentals 4 欄;technical 的 RSI/SMA 皆 0),`backtest_signals` 無 OOS y。Step 3 的 `feature_importances_` 對照在 atlas 端無對位方法(原生 RF 無此輸出)。

## 未消化 / 待補
- [ ] `n_estimators=500` 在台股月度資料是否足夠?可能需 1000。（2026-09-27 實測:atlas 原生預設 `NTrees=100`,合成資料 100 棵即 PASS（R²_OOS +0.9914）→ 「100 是否夠」在合成 DGP 上成立,真實台股月頻仍需 client 端驗）
- [ ] RF 對 regime 切換的適應性比線性差,需監控特徵重要性穩定性。

已解（2026-09-27）:XGBoost / LightGBM 是否有 atlas 對位 → **已驗證負面**:`git grep -i 'xgboost|lightgbm|gradientboost'` 只命中 `cmd/backtest-pipeline/main_test.go` 的 `newModel("xgboost")` 應報錯測試;`newModel` 白名單僅 `ols/pcr/pls/elasticnet/glm/rf` → atlas 端無任何梯度提升實作。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Random Forest 非線性需對位 regime 切換)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)