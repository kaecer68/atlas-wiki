---
title: WP-8 量化 SK 驗證（B+D 類）— 驗證證據與結論
type: audit-workpackage-evidence
created: 2026-08-22
created_by: wp8-verify-sk（量化 SK 驗證工人）
scope: VERIFICATION-BACKLOG B 類 12 條 + D 類 2 條（誇飾弱化 + 內部經驗值標註）
status: done
---

# WP-8 量化 SK 驗證（B+D 類）— 結論與依據

> 驗證方法：atlas backend :18080 未通（connection refused,2026-08-22）,改以 atlas 源碼
> （~/workspace/atlas,唯讀）對照 + sklearn 1.8.0（system python3）合成實驗實跑。
> 每條狀態與 backlog 狀態欄同步（✅ 已驗證/修正｜❌ 查無或無法證實,維持原樣並標註）。

## B1. SK-01 樣本 340 vs 336（❌ 未註明）

- 期間 1994-01-01 ~ 2022-04-30 理論月數 = 28×12 + 4 = **340 個月**；frontmatter 宣稱 336 樣本,差 4 月。
- SK-01 內文無任何剔除說明（僅 2026-08-22 audit-fix 註記「336 月 vs 理論 340 月…定義待註」）。
- 頁面 8996B / 上限 9000B（_method.md 第六條 + validate-wiki.yml size-check）,無空間增補 → 維持未註明,結論寫回 backlog。

## B2. SK-01 對位率 60-70% vs 90%+（❌ 兩口徑未解）

- frontmatter「綜合對位率 ≈ 60-70%」= **2 paper 對位率**（Fama-French 1993 3/4 + Jegadeesh-Titman 1993 100%）。
- 正文「86 因子 ≈ 90%+ 對位主流+在地+國際學術」= **7 框架全對位率**。
- 兩口徑確屬矛盾且未定義;頁面近上限無法增補,維持 audit-fix 註記。

## B3. SK-02「12 個總經變數」含 AAPL/MSFT/NVDA（✅ 已加註）

- atlas 源碼確認：`internal/marketdata/us_tech_provider.go` — AAPL/MSFT/NVDA 為 **Yahoo Finance 美股報價 provider**,掛在 `MacroDataSnapshot`（json: aapl/msft/nvda）下。
- 現行快照 `internal/fubonproxy/data/state/macro/latest.json` = **31 條序列**（含 aapl/msft/nvda、tsm_adr、spx/ndx/dji、sox 等）;「12 個」為 2026-08-01 當下口徑。
- `stock_get_quote` tool 定義 = Taiwan stock symbol only（"Coverage: TWSE-listed common stocks primarily"）,AAPL/MSFT/NVDA 不可由此查。
- 結論：分類「總經變數」為 misnomer（實為美股報價）,但端點事實正確 → SK-02 frontmatter 已加註。

## B4. SK-05 OLS R²_oos -0.05~0.10（❌ 需回測,維持猜測標註）

- backend 未通,`backtest_signals` 無法實跑;client 端 R²_oos 需完整因子面板 + SK-03 切分,本次不可得。
- 既有 2026-08-02 實測為合成線性資料（OLS R²=1.0）,不可代表真實台股。
- SK-05 已加口徑註「維持猜測標註,需回測確認」。

## B5. SK-06「L1 把 86 因子縮到 ~10-20 個」（❌ 非固定,已改寫）

- 合成實驗（sklearn 1.8.0,86 相關因子×336 月,真實訊號 12 因子,noise 0.8）：
  - ElasticNetCV：l1_ratio=0.1 → 非零 **79** 個;0.5 → **55**;0.9 → **37**。
  - 固定 l1_ratio=0.5：alpha=0.001 → 85;0.01 → 72;0.05 → 47;0.1 → 31。
- 結論：非零個數高度依賴 alpha/l1_ratio,「~10-20 個」非固定性質 → SK-06 已改「非固定」並附實驗證據。

## B6. SK-08「2-3 主成分就 90% 變異」（❌ 缺實證,維持論文猜測標註）

- 合成 86 相關因子（7 家族,組內相關 0.3/0.5/0.7/0.9/0.95）：前 2-3 主成分累積變異
  11.9% / 27.3% / 41.8% / 48.1% / 49.2%;達 90% 需 **7~19** 個主成分。
- 結論：「2-3 個成分就 90%」在合理相關結構下不成立（除非近完全共線）;維持「論文 v0.9 結論」標註,SK-08 frontmatter 已加驗證註。

## B7. SK-12 R²_oos 零均值基準變體（✅ 文件修正）

- 公式 `R²_oos = 1 - Σ(y-ŷ)²/Σy²` 分母為 Σy² = **uncentered（零均值基準）變體**,非標準 Σ(y-ȳ)²;兩者數值不同。
- SK-12 公式行已加註,引用時需註明基準。

## B8. SK-17「value-weighted 夏普通常較高」（✅ 已修正）

- 主流文獻：等權組合因小股曝險,毛報酬/Sharpe 通常**較高**;value-weighted 優點為換手低、可執行性高、容量大（SK-17 論文版概念 2026-08-22 audit-fix 已先修正）。
- 殘留矛盾：驗證方式 Step 3「預期 Sharpe 高 0.1-0.3,drawdown 略小」與文獻相反 → 已改「不預設勝負」並註明修正原因。

## B9. SK-18「-40% delta」（✅ 數值修正）

- 數值驗證：baseline=-1.7483 → optimized=0 → (0-(-1.7483))/|-1.7483| = **+100%**（對 |baseline|）;對 baseline 符號為 -100%,但語意為改善。
- 任何定義均非 -40% → SK-18 frontmatter 已改「+100% delta,對 |baseline|」。

## B10. SK-21「電子 80% < 20 元 / 金融 80% > 20 元」+ 第 20 百分位 10-15 元（❌ 需實跑）

- backend 未通,無法以 stock_get_quote 全 universe 實跑價格分布;本地無股價快照（fubonproxy state 僅 macro/sector_index/capital_flow/margin）。
- SK-21 已加口徑註「需實跑確認」,原文維持。

## B11. SK-23 產業數 + 「電子/金融 > 50%」（✅ 產業數 / ❌ 市值比）

- atlas 源碼 `internal/industry/sector.go`：`AllSectors()` = **38 個**（20 L1 + 18 L2;`sector_test.go` `const want = 38` 註明「20 L1 + 18 L2」）。
- tool 描述「full 20-sector taxonomy」為 L1 口徑;SK-20「18」= B5-3 SectorIndexReader 舊口徑;論文「47」= Fin-Skills 口徑;三數並存,SK-23 已加口徑註。
- 「電子/金融合計 > 50%」無本地市值快照,需實跑 → 標註維持。

## D1. SK-11/13/25/26/28/36 誇飾數字（✅ 已弱化,查無來源）

| 檔 | 原文 | 改後 |
|----|------|------|
| SK-11 | 「99% 是過擬合或資料偷看」 | 「極高比例是…」 |
| SK-25 | 「Sharpe 可能差 3 倍」 | 「可能差異巨大（數倍）」 |
| SK-25 | 「9 成是 reward 函數設計錯」 | 「大多是…」 |
| SK-26 | 「這類研究 99% 在日內/高頻資料」 | 「極高比例…」 |
| SK-28 | 「99% 是 reward 與 Sharpe 錯配」 | 「極高比例…」 |
| SK-28 | 「9 成機率 Spearman < 0.3」 | 「多數情況下…」 |
| SK-36 | 「訓練成本 100 倍於 SL」 | 「數量級高於 SL（論文用 100k steps,未給實測倍數）」 |

- SK-13：無「99%/9 成/3 倍/100 倍」類數字（grep 全檔無命中）,無需修改。

## D2. n_estimators=500 足夠（✅ 標內部經驗值）

- 實際位置為 **SK-10** frontmatter（backlog 原寫 SK-06 有誤,已於 backlog 更正）。
- 已標「內部經驗值,提到 1000 不顯著改善」並附 [2026-08-22 驗證] 註。

## 檔案變更清單（skills/ 15 檔 + backlog + 本證據檔）

- 修改（加驗證註/弱化）：SK-02, SK-05, SK-06, SK-08, SK-10, SK-11, SK-12, SK-17, SK-18, SK-21, SK-23, SK-25, SK-26, SK-28, SK-36（各附 .bak.20260822-verify-sk,gitignored）
- 未動：SK-01（8996B 近上限）、SK-13（無誇飾）、AGENTS.md、entities/、concepts/ 受保護檔、templates/
- backlog：B 類 12 條 + D 類 2 條狀態已更新（✅×7 / ❌×7,含 SK-10 位置更正）
