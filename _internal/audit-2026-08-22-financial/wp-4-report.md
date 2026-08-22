---
title: WP-4 覆蓋補課報告（L2 台灣出口/半導體景氣 + L6 散戶情緒）
type: wp-report
created: 2026-08-22
created_by: child-F (WP-4 覆蓋缺口補課工人)
based_on: _internal/audit-2026-08-22-financial/AUDIT-REPORT-main.md §C（L2 近真空 / L6 偏薄）
branch: feat/20260822-financial-audit-fixes
---

# WP-4 覆蓋補課報告

## 一、改了什麼

| 檔案 | 狀態 | bytes 前 | bytes 後 | 內容 |
|------|------|---------|---------|------|
| concepts/taiwan-export-orders-semiconductor-cycle.md | 新建 | 0 | 6987 | 憲章因果鏈第二層補課頁：三大指標（出口訂單/台積電月營收/半導體設備進口）、L1↔L3 上下游關係、atlas 對位、散戶解讀、驗證與未消化 |
| concepts/retail-sentiment-indicators.md | 新建 | 0 | 6985 | 憲章因果鏈第六層補課頁：五個散戶情緒指標（融資+維持率/當沖佔比/散戶買賣超+集保分級/Google Trends/券商分點）、反向指標使用規則、3+2+2 分層對位、散戶解讀與未消化 |
| _internal/audit-2026-08-22-financial/wp-4-report.md | 新建 | 0 | （本檔） | 本報告 |

- 白名單外檔案一字未動；兩頁皆新建檔，依派工備份 SOP 不需 .bak（已確認未產生 .bak）。
- 未執行任何 git 命令（主 agent 統一 commit）。

## 二、wiki-critic 6 項自審

1. **來源驗證**：數字只來自兩類——(a) 憲章（ATLAS_METHODOLOGY.md v1.0：L2/L6 層原文、融資高點≈頭部/斷頭潮≈底部、3+2+2、資金對抗布局點、高原期當沖>35%、150% 訊號門檻）與現有 wiki 已有事實（130%/120% 維持率現制、當沖分級、集保 20/400 張研究慣例、分點警示、SK-31 週期鏈、margin-balance-extreme 策略）；(b) 通識標 [通識] / 未驗證標 [需驗證] / 待辦標 [待驗證]。未發明任何具體數字。
2. **非猜測**：出口訂單公布日 [公布日為通識, 需驗證]、設備進口管道 [管道需驗證]、Google Trends 管道 [資料管道待驗證]、集保公布節奏 [節奏需驗證]、領先月數 [待驗證]——全部標記，未硬給門檻。
3. **結構化**：兩頁均照任務書指定大綱（定位/指標表/上下游或使用規則/atlas 或 3+2+2 對位/散戶解讀/驗證未消化），frontmatter 照 concepts/ 慣例（title/created/updated/type/tags/sources/confidence/contested/contradictions）。
4. **去重**：先讀 taiwan-stock-market-structure.md、taiwan-chip-flow-analysis.md、SK-31、trigger-equipment-capex-external-report-cycle.md、taiwan-money-flow-seven-institutional-buckets.md、atals-mcp-tools-reference.md 再下筆；細節用 [[wiki-link]] 引既有頁（如維持率現制→市場結構 §5.2、當沖/集保→籌碼面 §5.3/§6.2、分點警示→七大資金勢力 §3），不重抄內容。
5. **時效性**：快照值全部附 [2026-08-22 audit-fix]（含 atlas-mcp tool catalog 盤查結果：`stock_get_monthly_revenue` 存在、無出口訂單/設備進口端點）。
6. **可操作性**：每指標給「公布節奏 + 哪裡看 + 散戶怎麼用」（出口訂單：每月 20 日/經濟部統計處；台積電：每月 10 日/公開資訊觀測站；融資：每日盤後/證交所；散戶讀法：3 個月 YoY 趨勢、百分位極端、行事曆化公布日）。

## 三、憲章對位（兩頁）

- 七時期為真值、RISK_ON/OFF/NEUTRAL 為向下相容層：兩頁各有一處明示（頁 1 §二、頁 2 §二 規則 3）。
- 因果鏈位置：新頁 1 = 第二層（台灣出口與半導體景氣）；新頁 2 = 第六層（散戶情緒與籌碼）。
- archetype 用語：僅用 跟隨聰明錢／事件套利／資金對抗（頁 2 §二 規則 3 用「資金對抗」），無 Defensive/Aggressive/Tactical。

## 四、驗收

- 兩頁各 4000–7000B：6987 / 6985 ✅
- wiki-critic 6 項自審 ✅
- 無來源數字標 [需驗證] ✅
- 全部 wiki-link 目標存在（兩頁互相引用，互引成立）✅

## 五、備註（供主 agent QC）

- 頁 1 §五 未消化：atlas 無出口訂單/設備進口端點 [2026-08-22 audit-fix 盤查 117 tools catalog 確認]，目前僅 `stock_get_monthly_revenue` 可代理台積電月營收。
- 頁 2 §一 Google Trends 行保留 [資料管道待驗證]，因本庫原 0 命中（審計 §C L6 判定），未敢擅自給管道。
