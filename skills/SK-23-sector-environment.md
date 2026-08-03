---
title: SK-23 產業輪動環境建構
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-23
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [industry_sector_list, industry_sector_lookup, stock_get_quote, stock_get_fundamentals, macro_get_snapshot_latest]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:industry_sector_list 38 個產業(ai_supply_chain/auto/biotech/electronics/semiconductor 等);industry_sector_lookup(2330→半導體 12 成分股);macro_get_snapshot_latest 確認當前 current_period=consolidation(盤整期)+ 4 大法人/產業桌 universe;**atlas 沒有「市值加權產業指數」端點,需 client 端用 stock_get_fundamentals × industry_sector_list 算**(端點活+骨架齊全);47 個產業 vs 38 個 atlas 產業對位需驗證。
---

## 一句話定位
SK-23 在 atlas 是「從個股走到產業」——把 1000+ 股票聚合成 47 個產業指數,讓強化學習(SK-24)在「選哪個產業」這個決策粒度上學習,而不是「選哪 100 檔個股」(後者維度太高學不動)。

## 論文版概念
- 輸入:stock_data(個股)+ industry_map(股票→產業,47 類)
- 動作:
  1. 每月算產業市值佔比
  2. 對每個產業算市值加權價格序列
  3. 算技術指標(SMA10/20、MOM5、VOL20)
- 輸出:二維表 (日期 × 產業_指標)

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 47 個產業 | `industry_sector_list`(直接給清單) |
| 股票→產業映射 | `industry_sector_lookup` |
| 個股價格 | `stock_get_quote` |
| 市值 | `stock_get_fundamentals` |
| 總經 | `macro_get_snapshot_latest` |

**差異點**:論文是純 Python 組裝,atlas 已有現成產業端點。**這是 atlas 對位完整的 SK 之一**。

**沒有對位的部分**:無「產業指數時序」單一端點(需 client 端組裝);無「市值加權」單一端點。

## 散戶解讀
- **G**:用戶問「該重壓電子還是金融?」 → SK-23 給你產業層級的訊號,搭配 SK-16 的十分位多空,在「產業」+「個股」兩層做決策。
- **+E**:**47 個產業對散戶太多**,台股實務上 10-15 個大類就夠(電子/金融/傳產/生技/...),散戶應先合併再用 SK-23。
- 對位 ATLAS_METHODOLOGY 七時期:產業輪動在 regime 切換時最明顯(電子→生技→金融循環),這是 SK-23 主要的 alpha 源。

## 驗證方式
Step 1: 呼叫 `industry_sector_list` 確認 47 個產業清單,call `industry_sector_lookup` 抽 10 檔個股確認歸屬正確。
Step 2: client 端算每月產業市值佔比,確認電子/金融合計 > 50%(台股常態)。
Step 3: 算 1 個產業(例如半導體)的市值加權 MOM5 序列,call `risk_get_metrics` 看走勢合理性。

## 未消化 / 待補
- [ ] atlas `industry_sector_list` 與論文的 47 類是否完全一致?需對位。
- [ ] 產業指數的「市值加權」是否要排除 ETF 持倉重複計算?需釐清。
- [ ] 與 SK-24 PPO 整合:RL 環境(state, action, reward)的具體設計待補。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §四(七大資金勢力行為)+ §五(策略矩陣:產業輪動 env 需對位 3+2+2 錢潮雷達 + 策略三分類)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)