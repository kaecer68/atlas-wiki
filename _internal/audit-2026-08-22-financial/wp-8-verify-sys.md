# WP-8 制度/命名驗證證據（verify-sys worktree, 2026-08-22）

> 工作樹：atlas-wiki-verify-sys（feat/20260822-verify-sys）。抓取日：2026-08-22。
> 範圍：VERIFICATION-BACKLOG A 類 1-4 + D 類 5 + E 類 6-9。

## A1 權證歐式/美式（taiwan-financial-domain-model §1）✅

- 結論：台股掛牌權證**非全歐式**，歐式與美式並存；外國標的權證限發行歐式。
- 引文（TWSE 官方 FAQ 認購(售)權證教育宣導）：「認購權證屬於買權，其持有人有權利在特定期間內(美式)或到期日(歐式)，以約定履約價格向發行人購入一定數量之標的證券…」；「投資以外國證券或指數為標的之權證…限發行以現金結算之歐式權證」；「價內權證若市場上流動性不佳，美式權證可直接申請履約」。
- 佐證：《認購(售)權證上市審查準則》§2 定義「於履約期間內或特定到期日」兩型並存（twse-regulation.twse.com.tw FID=FL007274）；權證上市公告 Excel 含「歐式/美式」欄位。
- URL：https://www.twse.com.tw/zh/page/products/securities/warrant/faq.html
- 套用：原文「分為歐式與美式」正確，加 [2026-08-22 驗證] 標記。

## A2 ETF 規模/受益人數/投信持有（taiwan-stock-market-structure §7.1/§9.2）✅

- 結論：三項斷言均獲官方統計支持（SITCA 投信投顧公會 ETF 專區統計資料,年頻）。
- 數據（全體 ETF）：
  - 基金規模：2023=38,542 億元(3.85 兆)、2024=63,819 億元(**6.38 兆**)、2025=75,382 億元(**7.54 兆**) → 「>4 兆」✅
  - 受益人數：2023=868 萬、2024=**1,436 萬**、2025=1,656 萬 → 「破千萬」✅（2024 起）
  - 投信持有：全體基金規模 2025=113,764 億元=11.38 兆（含海外部位），投信台股部位 5-8 兆屬合理量級（間接支持）
- URL：https://www.sitca.org.tw/ROC/SITCA_ETF/etf-section-stats.html（查詢頁 etf_beneficial.aspx,年全體）
- 套用：§7.1/§9.2 加 [2026-08-22 驗證] 校準數字。

## A3 瞬間價格穩定試撮間隔（taiwan-stock-market-structure §10.3）✅

- 結論：官方**無「30 秒試撮」**；瞬間價格穩定措施暫緩 2 分鐘期間之模擬撮合資訊揭露間隔=**每 10 秒**（證交所臺證交字第 1090200551 號函,109.02.26,盤中零股 109.10.26 實施）。盤中集合競價撮合循環秒數沿革 20→15→10→5 秒（TWSE 沿革：102/07 20→15 秒、103/02 15→10 秒、103/12 10→5 秒），現行 5 秒。「20 秒」為 2013 年前舊制集合競價循環秒數，「30 秒」無官方依據。
- URL：https://twse-regulation.twse.com.tw/TW/int/DAT01_print.aspx?FLCODE=FE337278 ; https://www.twse.com.tw/zh/about/company/history.html
- 套用：§10.3 加試算/揭露間隔說明行 [2026-08-22 驗證]。

## A4 集保大戶/散戶分級（taiwan-chip-flow-analysis §6.2；backlog 誤標 §4.4）✅

- 結論：「400 張以上大戶 / 20 張以下散戶」與 TDCC 集保戶股權分散表官方 15 級分級完全對應。
- 官方分級（單位=股）：1-999、1,000-5,000、5,001-10,000、10,001-15,000、15,001-20,000、20,001-30,000、30,001-40,000、40,001-50,000、50,001-100,000、100,001-200,000、200,001-400,000、**400,001-600,000**、600,001-800,000、800,001-1,000,000、1,000,001 以上。
  - 400 張 = 400,000 股 → 「400,001 股以上」= 400 張以上 ✅
  - 20 張 = 20,000 股 → 「20,000 股以下」（1-999~15,001-20,000 五級）= 20 張以下 ✅
- 實例：2330（資料日期 20260821）：1,000,001 股以上 1,479 人占 84.71%。
- URL：https://www.tdcc.com.tw/portal/zh/smWeb/qryStock
- 套用：§6.2 加官方分級對照 [2026-08-22 驗證]。

## D5 stress score 尺度（trigger-taiwan-strait-tension）✅

- 結論：「-7.66」與「29.92-34.74」為**同一指標（taiwan_calculator stress index）不同日期觀測值**，尺度一致（連續值,隨成分權重變動,可正可負）。
- 實跑：atlas_mcp macro_get_stress_index_current（backend http://100.68.42.72:18080）= 2026-08-23 **score 7.71（regime low）**，components：dxy 0.066 / foreign_flow -7.13 / geopolitical 7.80 / gold 0.286 / jpy 0.034 / oil 0.123 / us10y 1.61 / vix 4.92。
- 佐證：log.md 歷史值 29.92(low)/32.55(alert)/34.74(alert)；foreign_flow 成分可為負（-0.07→22 跳動紀錄）→ -7.66 為 2026-08-03 快照屬正常。
- 套用：模板加註 [2026-08-22 驗證]，原文數值保留（為當日快照）。

## E6 atals-*/atlas-* 拼字 ✅（正文統一；檔名留待裁決）

- 端點真名前綴實查結論：**atlas 端點無 atals_ 前綴**。
  - atlas-mcp tools/catalog：117 工具，0 個含 'atals'、0 個以 'atlas' 開頭；實際為功能域前綴（alert_/macro_/risk_/strategy_/capital_flow_/narrative_ 等）。
  - MCP server name = "atlas-mcp"（cmd/atlas-mcp/server/server.go:163）。
  - atlas 源碼純 Go 中 'atals' 0 次（僅 binary "runtime.fatalsignal" 子字串、gitnexus cache 註解 "fatals the test"）。
  - ⚠️ backlog 原註記「2026-08-22 已查:atlas 端點實際名為 atals_*,留待裁決」為**錯誤註記**，本次已更正。
- 套用：5 檔（atals-mcp-tools-reference / atals-platform-overview / atals-risk-management-framework / atals-simulation-guide / atals-strategy-taxonomy）正文獨立「atals」→「atlas」（18 處）；`[[concepts/atals-*]]` 連結目標與 frontmatter 路徑引用保留（84 處引用廣布 index/log/skills→檔名改名留待裁決）。

## E7 模板數量快照 ✅

- 實數：`ls templates/*.md` = **21 檔**。
- 自述不一致清單：現有 11（cb-emergency）、12（2330-tsmc-swing）、13（megaproject）、14（equipment-capex/hbm）、16（ai-capex/hedge-fund/msci）；序號第 16/17/18/19/20 模板。
- 套用：8 檔（trigger-2330-tsmc-swing / ai-capex-guidance-cut / cb-emergency-intervention / equipment-capex-external-report-cycle / hbm-cycle-cooling / hedge-fund-unwind / megaproject-2-quarter-lag / msci-rebalance-pressure）H1 後加 `> [2026-08-22 快照:21]` 註記；數字本身保留（歷史演進）。

## E8 興櫃 ESM 拼字 ✅

- 修正：`ESM（Emerving Stock Market）` → `ESM（Emerging Stock Market）`，加 [2026-08-22 驗證:Emerving→Emerging 拼字修正]。

## E9 trigger-margin-350b 註記確認 ✅

- 確認存在：「> 註:檔名 350b（3500 億）為舊門檻,現條件 > 5000 億（2026 市值水位校準）;檔名保留以相容引用 [2026-08-22 audit-fix]」。不需再改。

---
*WP-8 verify-sys 完工。修改留在 worktree（git 由主 agent 統一處理）。*
