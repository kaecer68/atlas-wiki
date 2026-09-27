---
title: SK-23 產業輪動環境建構
description: "問「該重壓電子還是金融」、要看產業輪動時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-23
sources:
  - "TWSE MI_INDEX https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX（2026-09-27 實測 200）"
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [industry_sector_list, industry_sector_lookup, stock_get_quote, stock_get_fundamentals, macro_get_snapshot_latest]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active（快照）:industry_sector_list 38 個產業、industry_sector_lookup 2330→半導體 12 成分股、macro_get_snapshot_latest。[2026-09-27 batch#5 複驗（9 端點,全 200/1 端點 found:false）:atlas 產業數**雙證 38 = 20 L1 + 18 L2**（源碼常數＋live 端點同日回 38、其中 20 個有代表股）;**原「macro 確認 current_period=consolidation」不成立**（該 payload 43 條序列無 period/regime 欄位）;`stock_get_fundamentals` 只有 PE 30.19/PB 9.57/DividendYield/Sector、**無 market_cap** ⇒「市值加權」無資料基礎;產業時序**資料層已存在**（TWSE MI_INDEX/FinMind 類指數 → 磁碟 106 個日檔、排程 `macro_cache_twse_sector_index`）但**無 MCP/HTTP 端點**;`/api/stock/industry_winrate` 首次實跑 = 20 個 L1 產業勝率（含 Wilson 區間）,只覆蓋 96/854 檔代表股。見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b5）
l3_endpoints_probed:
  - "/api/industry/sectors → 200 (2026-09-27T20:26:19+08:00)"
  - "/api/industry/sector-lookup?symbol=2330 → 200 (2026-09-27T20:26:19+08:00)"
  - "/api/industry/sector-lookup?symbol=9999 → 200 (found:false) (2026-09-27T20:27:16+08:00)"
  - "/api/stock/quote?symbol=2330 → 200 (2026-09-27T20:26:19+08:00)"
  - "/api/stock/fundamentals?symbol=2330 → 200 (2026-09-27T20:26:19+08:00)"
  - "/api/macro/snapshot/latest → 200 (2026-09-27T20:26:19+08:00)"
  - "/api/stock/industry_winrate?condition_id=momentum-20d-positive → 200 (2026-09-27T20:27:42+08:00)"
  - "/api/dashboard/sector-allocation-plan → 200 (no_simulation_session) (2026-09-27T20:27:24+08:00)"
  - "/api/scheduler/status → 200 (2026-09-27T20:26:25+08:00)"
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §四(七大資金勢力行為)+ §五(策略矩陣:產業輪動 env 需對位 3+2+2 錢潮雷達 + 策略三分類)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

> 口徑註：atlas 產業數 = 38（20 L1 + 18 L2,2026-09-27 雙證,見 §驗證方式）;SK-20「18」為 B5-3 SectorIndexReader 舊口徑、論文「47」為 Fin-Skills 口徑,三數並存各註明;「電子/金融合計 > 50%」2026-08-22 時無快照,需實跑確認 [2026-08-22 驗證]
> [2026-08-23 TWSE 實測] 上市+上櫃 2026-08-21 收盤 × 股本全量市值 158.9 兆:電子 80.4% + 金融 7.0% = 87.4%（原「>50%」斷言大幅成立）;分市場:上市 87.9%、上櫃 81.0% [2026-08-23 實測:成立]

## 一句話定位
SK-23 在 atlas 是「從個股走到產業」——把個股聚合成產業面板（論文版 47 類;atlas 端定案 **38 個產業 = 20 L1 + 18 L2**,2026-09-27 雙證）,讓強化學習(SK-24)在「選哪個產業」這個決策粒度上學習,而非「選哪 100 檔個股」(維度太高學不動)。

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
| 47 個產業 | `industry_sector_list`(atlas 實回 **38**:20 L1 + 18 L2,2026-09-27) |
| 股票→產業映射 | `industry_sector_lookup` |
| 個股價格 | `stock_get_quote` |
| 市值 | `stock_get_fundamentals` |
| 總經 | `macro_get_snapshot_latest` |

**差異點**:論文是純 Python 組裝,atlas 已有現成產業端點。**這是 atlas 對位完整的 SK 之一**。

**沒有對位的部分**（2026-09-27 更正）:無「產業指數時序」**對外端點**——但資料層**已有**原生類股指數時序（TWSE MI_INDEX/FinMind → `data/state/sector_index/` 日檔,本機 106 檔,＋排程 `macro_cache_twse_sector_index`）;無「市值加權」端點。

## 散戶解讀
- **G**:用戶問「該重壓電子還是金融?」 → SK-23 給產業層級訊號,搭配 SK-16 的十分位多空,在「產業」+「個股」兩層做決策。
- **+E**:**產業數對散戶太多**——atlas 端 38（20 L1 + 18 L2）,而 `industry_winrate` 只給 20 個 L1;台股實務 10-15 個大類就夠,散戶先用 20 個 L1 再合併。
- 對位 ATLAS_METHODOLOGY 七時期:產業輪動在 regime 切換時最明顯(電子→生技→金融循環),這是 SK-23 主要的 alpha 源。

## 驗證方式
Step 1: 呼叫 `industry_sector_list` 確認產業清單,call `industry_sector_lookup` 抽個股確認歸屬。
Step 2: 產業市值佔比**今日 client 端算不出來**（`stock_get_fundamentals` 無 `market_cap`,2026-09-27）;需要市值時改用 TWSE 已發布類股指數（`data/state/sector_index/`）或外部來源並標替代。
Step 3: 產業層訊號品質直接用 `/api/stock/industry_winrate?condition_id=momentum-20d-positive`（20 個 L1 產業,含 Wilson 區間與扣成本前瞻報酬）,不需 client 端聚合。

### L3 端點實跑（2026-09-27）

| 端點 | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/industry/sectors` | 200 | **38** 個產業（20 個有代表股、18 個空清單 ⇒ 對上源碼 20 L1＋18 L2） | 2026-09-27T20:26:19+08:00 |
| `/api/industry/sector-lookup?symbol=2330` | 200 | `found=true`、`semiconductor`、**12** 檔成分股 | 2026-09-27T20:26:19+08:00 |
| `/api/industry/sector-lookup?symbol=9999` | 200 | `found=false`＋warning（未知代號不報錯） | 2026-09-27T20:27:16+08:00 |
| `/api/stock/quote?symbol=2330` | 200 | `last=2475`、`volume=12989000`、`is_tradable=true`、`trading_day=false` | 2026-09-27T20:26:19+08:00 |
| `/api/stock/fundamentals?symbol=2330` | 200 | 只有 `PE 30.19`／`PB 9.57`／`DividendYield 1.1`／`Sector`;**無 `market_cap`** | 2026-09-27T20:26:19+08:00 |
| `/api/macro/snapshot/latest` | 200 | **43** 條序列（法人/總經/指數,含 `taiex`）;**無 `current_period`/`period`/`regime`** | 2026-09-27T20:26:19+08:00 |
| `/api/stock/industry_winrate?condition_id=momentum-20d-positive` | 200 | **20** 個 L1 產業勝率（obs 68–612、Wilson 上下界、扣成本前瞻報酬）;金融 0.603 最高、營建 0.218 最低;`symbol_coverage_pct=11.24`（96/854 檔） | 2026-09-27T20:27:42+08:00 |
| `/api/dashboard/sector-allocation-plan` | 200 | `target/current/delta` 皆 `null`、`applied=false`、`fallback_reason=no_simulation_session`（端點在、今日未生效） | 2026-09-27T20:27:24+08:00 |
| `/api/scheduler/status` | 200 | 110 jobs;`macro_cache_twse_sector_index` enabled（900 s,last_run 2026-09-27T12:26:09Z）、`auto_symbol_industry` enabled | 2026-09-27T20:26:25+08:00 |

**更正（2026-09-27）**

1. 「無『產業指數時序』單一端點（需 client 端組裝）」只對一半:資料層**已有**原生類股指數時序 —— `adapter_twse_sector_index.go`（TWSE MI_INDEX／FinMind,`TAISEMI`）＋ `cmd/backfill-sector-index` 寫入 `data/state/sector_index/`（本機 **106** 個日檔,2026-06-03 → 2026-09-24,每檔 **20** 個 L1 key 的 `index`＋`return_pct`）。**缺對外端點,不是資料**。
2. 「47 個產業」定案 **38 = 20 L1 + 18 L2**:`internal/industry/sector.go` 的 20 個 `SectorID` 常數＋`internal/sectormap/canonical.go`（`canonicalL1`/`canonicalL2`）,與 live 端點同日一致。
3. 「client 端用 `stock_get_fundamentals` × `industry_sector_list` 算市值加權」**無資料基礎**:今日無 `market_cap`（2026-09-27T20:26:19+08:00）,與 SK-20／SK-37 的 2262 欄 field-contract 0 命中一致。
4. 「macro 確認 `current_period=consolidation`」**不可重現**:該端點回 43 條序列,無任何 period/regime 欄位（2026-09-27T20:26:19+08:00）。時期真值改查 PeriodDetector 出口,不要用 macro snapshot 反推。
5. 產業層訊號品質**不必 client 端算**:`/api/stock/industry_winrate` 直接回 20 個 L1 產業勝率＋Wilson 區間＋扣成本前瞻報酬;**但只覆蓋 96/854 檔代表股**（11.24%,2026-09-27T20:27:42+08:00）,不可當全市場結論。

## 未消化 / 待補

已解（2026-09-27）:atlas `industry_sector_list` 與論文 47 類**不一致**——atlas 定案 38（20 L1 + 18 L2）;論文正本不在本機,逐類比對不可行。
- [ ] 產業指數的「市值加權」是否要排除 ETF 持倉重複計算?需釐清。
- [ ] 與 SK-24 PPO 整合:RL 環境(state, action, reward)的具體設計待補。
