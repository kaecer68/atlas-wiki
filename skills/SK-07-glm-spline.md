---
title: SK-07 廣義線性模型（樣條非線性）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-07
ingested_at: 2026-08-01
status: active
tier: T3
confidence: medium
atlas_go_relevance: low
mcp_tools_used: [stock_get_fundamentals, backtest_signals, risk_get_metrics]
verification: 2026-09-27 L3 端點實跑 (http_code + timestamp 見 `l3_endpoints_probed`;明細見 §驗證方式):3 個 HTTP 端點全 200,**無任何端點回 R²_oos** → 本頁 `R²_oos=0.0745` 為 2026-08-02 client 端 sklearn 快照,今日無法由 atlas 複驗。新增:**atlas repo 內有原生樣條 GLM**(`internal/ml/spline.go` 的 `GLMSpline`:truncated-power basis、degree 3、節點取**資料分位數**、家族 gaussian/poisson/gamma、法方程加 ridge),可用 `cmd/backtest-pipeline -model glm` 實跑 → 今日 `-synthetic` exit 0、**R²_OOS +0.9992（PASS,R²>0.9）**,推翻「atlas 完全沒有 ML 訓練端點、SK-07 為 100% client 端責任」;**Group Lasso 兩邊都沒有**(`git grep -i grouplasso` 在 atlas 0 命中)。歷史:2026-08-02 v0.9 結算跑過 L3 升 active（client 端 sklearn 1.8.0 SplineTransformer(degree=2, knots=[0.25,0.5,0.75]) + Lasso(alpha=0.1),R²_oos=0.0745;GroupLasso sklearn 無原生,該輪以 Spline+Lasso 替代）。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b2）
l3_endpoints_probed:
  - "/api/stock/fundamentals?symbol=2330 → 200（PE 30.19/PB 9.57/DY 1.1;論文的 PE/PB 型 U 型關係需更細欄位,X 端點今日只回 4 欄）（2026-09-27T20:02:26+08:00）"
  - "/api/backtest/signals → 200（active_signals null;無 OOS y）（2026-09-27T20:02:26+08:00）"
  - "/api/dashboard/risk → 200（session_count 210;無 R² 欄位）（2026-09-27T20:02:26+08:00）"
  - "CLI 代理（無 HTTP 端點）: atlas repo `-synthetic -model glm` → R²_OOS +0.9992（PASS）（2026-09-27T20:02:28+08:00）"
---

## 一句話定位
SK-07 引入「非線性」+「群組稀疏」——本益比對報酬的關係可能不是直線(可能是 U 型),SK-07 用樣條捕捉;群組 Lasso 把同因子的多個基函數當一組,避免「只保留某因子的部分基」。

## 論文版概念
- 樣條非線性:對每個數值特徵用 `degree=2` 二次樣條展開,節點 `[0.25, 0.5, 0.75]` 分位數
- Group Lasso:每個原始特徵的基函數為一組,整組進整組出
- 結果:模型可學到「PB 太高/太低都不好,中間最好」這類 U 型關係

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 樣條基函數 | MCP／HTTP 缺;**repo 內有原生樣條 GLM**(`internal/ml/spline.go`,`-model glm`,2026-09-27 實跑) |
| Group Lasso | 缺(client 端);**atlas repo 亦無**(`git grep -i grouplasso` 0 命中,2026-09-27) |
| 特徵來源 | `stock_get_fundamentals` |
| 評估 | `risk_get_metrics` |

**差異點**:**更正（2026-09-27）**:MCP／HTTP 面確實沒有 ML 訓練端點,但 repo 內有原生樣條 GLM(`GLMSpline`)可用 `-model glm` 實跑 → SK-07 **不是** 100% client 端責任;client 端只在「換真實台股資料、以及做 SHAP/PDP 視覺化」時必須自建。**但捕捉非線性在金融預測上極有價值**——散戶常誤信線性關係。

**沒有對位的部分**:無樣條 / Group Lasso 的 **HTTP** 端點（原生實作僅在 repo 內）;無「非線性視覺化」(SK-14 PDP 需另做)。

## 散戶解讀
- **G**:用戶問「PE 越低越好嗎?」 → 不是。PE 太低可能是夕陽產業,太高可能是成長股,中間有甜蜜點——這就是 U 型,SK-07 學得到。
- **+E**:**散戶最常忽略「U 型關係」**,只看線性係數會錯失甜蜜點,看 permutation importance 又會低估(因為線性切割)。**非線性是金融建模的隱藏 alpha**。
- 對位 ATLAS_METHODOLOGY 七時期:U 型的甜蜜點在 regime 切換時會移動,需每期重訓。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` 拉 8 欄 X(PE/PB/殖利率/市值/營收成長/ROE/負債比/淨利率),從 `backtest_signals` 拿 y。
Step 2: client 端 `SplineTransformer(degree=2, knots=[0.25,0.5,0.75])` + `GroupLasso`。
Step 3: 對比 OLS / ElasticNet 的 OOS R²,確認 SK-07 優於線性模型(預期差距 10-20%)。

### L3 端點實跑 + CLI 代理（2026-09-27,本 PR）

| # | 目標（GET,帶 `X-API-Key`） | http_code | 實測結果 | timestamp（UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19 / PB 9.57 / DY 1.1 / sector semiconductor（僅 4 欄） | 2026-09-27T20:02:26+08:00 |
| 2 | `/api/backtest/signals` | 200 | `active_signals` null、var/sharpe 全 0 → 無 OOS y | 2026-09-27T20:02:26+08:00 |
| 3 | `/api/dashboard/risk` | 200 | session_count 210；無 R² 欄位 | 2026-09-27T20:02:26+08:00 |
| 4 | CLI（非 HTTP）:`cmd/backtest-pipeline -synthetic -model glm` | exit 0 | 500 samples × 2 features；**R²_OOS +0.9992 → PASS** | 2026-09-27T20:02:28+08:00 |

- **更正（2026-09-27）**:第 4 列推翻本頁「atlas 完全沒有 ML 訓練端點／SK-07 100% client 端責任」——`internal/ml/spline.go` 有原生樣條 GLM,CLI 可直接跑（與 SK-05 發現的 `-model` 清單 `ols/pcr/pls/elasticnet/glm/rf` 同一條路徑）。仍**不在 MCP／HTTP 面**。
- Step 1 今日只完成一半:X 端點只回 4 欄（PE/PB/DY/Sector）,本頁要的 8 欄(殖利率、市值、營收成長、ROE、負債比、淨利率)今日無法由單一端點湊齊;`backtest_signals` 無 OOS y。
- Step 2 設定差異:本頁用 `degree=2 + 固定節點 [0.25,0.5,0.75]`,atlas 原生 `GLMSpline` 用 `degree=3` + **由資料分位數自動取節點**（`computeKnots`）→ 兩者不是同一組基函數,數值不可直接互比。

## 未消化 / 待補
- [ ] Group Lasso 在 sklearn 沒有原生,需自寫或用 `celer` 套件。（2026-09-27 實測:atlas repo 亦無 Group Lasso,`git grep -i grouplasso` 0 命中 → 兩端都缺,此項無 atlas 對位可借）
- [ ] 樣條節點位置 [0.25, 0.5, 0.75] 是論文的預設,台股分位可能不同(如 PE 分位高度右偏)。（2026-09-27 實測:atlas 原生 `GLMSpline` 的 `computeKnots` 直接從資料取等距分位數(degree 3 → 2 個內節點),不需硬編 → 「固定節點是否合台股」這個問題在 atlas 原生路徑不存在;但要驗證的是「分位數節點 vs 論文節點」何者在台股更穩,仍需真實資料）
- [ ] 與 SK-14 PDP 的關係:SK-07 學完後用 SK-14 視覺化「PE vs 預期報酬」曲線,確認 U 型假設。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:GLM Spline 需對位非線性關係跨 regime 表現)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)