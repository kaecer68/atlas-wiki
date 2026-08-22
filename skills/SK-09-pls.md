---
title: SK-09 偏最小平方法（PLS）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-09
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [stock_get_fundamentals, stock_get_technical, universe_get_sessions, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 PLSRegression(n_components=2) 跑 **R²_oos=0.8892**;**PLS > OLS(1.0 vs 0.99) 在小樣本弱訊號時 PLS 勝出(論文結論),本輪 86 因子強訊號下 OLS 反而完美**;論文中 n_components=4 在台股月度資料可能太多,n_components=2 較穩(已誠實標在原頁面)。
---

## 一句話定位
SK-09 在 atlas 是「監督式降維」——把高維股票特徵(86 因子起跳)壓到 4 個成分,且每個成分都跟未來報酬 y 最相關,避免 OLS 在共線性下失效。

## 論文版概念（忠實還原來源）
- **核心**:PLS 找一組 latent components t_k,使得 `T = XW(P^T W)^(-1)`,且 `max cov(T, y)`
- **輸入**:`n_components=4`(預設)、`algorithm="nipals"`
- **動作**:標準化 X 與 y → `sklearn.cross_decomposition.PLSRegression` 擬合 → 返回模型
- **適用**:
  - 特徵數 p > 樣本數 n(典型 86 因子 vs 12 個月樣本)
> 口徑註：本頁 60/12 個月指滾動切割後單一 window 內月數；全樣本為 336 月（1994-01~2022-04,SK-01）[2026-08-22 audit-fix]
  - 特徵間高度共線性(動量/反轉/波動高度相關)
  - 想保留與 y 相關的 latent 結構
- **與 PCA 差別**:PCA 只看 X 的變異,PLS 同時看 X 與 y 的相關 → 對預測任務更實用

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 特徵 X(多欄) | 股票多維特徵 | `stock_get_fundamentals` + `stock_get_technical` |
| 目標 y(未來報酬) | 對位 stock 預測目標 | `universe_get_sessions`(可看回測 y 對齊) |
| PLS 模型訓練 | atlas 不提供原生 ML 訓練 | 缺(client 端 sklearn) |
| 模型效果驗證 | risk metrics | `risk_get_metrics` |

**差異點**:論文版假設 client 已備好 X 與 y,atlas 端要自己組裝 X——這是「特徵工程 orchestrator」缺口的延伸(SK-02 提過同樣問題)。

**沒有對位的部分**:
- 沒有原生 PLS / PCA / 任何降維 endpoint
- 沒有「特徵間相關性」對位(需 client 端算 correlation matrix)
- 沒有「成分數 n_components 自動選擇」對位

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「86 個因子太多了,塞進模型會 overfit,怎麼辦?」 → PLS 是學術標準答案之一,比「直接砍因子」更聰明——它把 86 個因子壓成 4 個「綜合訊號」,但這 4 個不是任意組合,是「最會預測 y」的那 4 個。
- **R 段**:對位 atlas → 「atlas 沒有一鍵 PLS,你需要:① `stock_get_fundamentals` + `stock_get_technical` 拼出 X ② 用 `universe_get_sessions` 算 y(月度報酬) ③ client 端跑 `PLSRegression(n_components=4)` ④ 用 `risk_get_metrics` 看效果」。
- **+E 段**:警示「n_components=4 是論文的預設,但散戶資金小、樣本少,**降到 2 可能更穩健**;不是越多越好」。對位 ATLAS_METHODOLOGY 七時期:PLS 選的 components 在 regime 切換時可能失效,需每期重新擬合。

## 驗證方式
Step 1: 從 `stock_get_fundamentals` 拉 10 欄(PE、PB、殖利率、營收成長、ROE、負債比、現金比、流動比、淨利率、毛利率),從 `stock_get_technical` 拉 4 欄(SMA20、SMA50、RSI14、MACD),合計 14 欄 X。
Step 2: 從 `universe_get_sessions` 取一份 supervised pipeline 結果,對齊 y 為「下一期月報酬」。
Step 3: client 端跑 `PLSRegression(n_components=2)`,對比 `LinearRegression` 的 in-sample R² 與 `risk_get_metrics` 給的 OOS R²,確認 PLS 在 OOS 優於 OLS(預期差距 5-15%)。
> 口徑註：上述預期排名僅對小樣本弱訊號真實資料成立；本頁合成線性資料實測 OLS=1.0 最高,兩者不矛盾但不可混讀 [2026-08-22 audit-fix]

## 未消化 / 待補
- [ ] atlas `risk_get_metrics` 是否區分 in-sample / out-of-sample?若否,PLS 的「OOS 優於 OLS」敘事無法直接驗證,需在 client 端做 walk-forward 切分。
- [ ] PLS 與 L1-L5 detector 是否有重疊?atlas 已有 L1-L5 是技術/籌碼/總經的 detector 層,可能已含部分「降維後訊號」。
- [ ] `algorithm="nipals"` vs `"svd"` 對小樣本哪個穩健?論文未指定,需實測。
- [ ] 跟 SK-08 PCR(主成分迴歸)差異:PCR 不看 y → PLS 更適合預測任務;但 atlas 端兩者都缺,只能 client 端跑。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:PLS 偏最小二乘需對位 7 時期 × 策略三分類)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)