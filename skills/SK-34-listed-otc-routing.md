---
title: SK-34 上市/上櫃分流判斷與備援(2026-08-07 D4 v1.0)
type: skill-inbound
source: hermes skill data-source-decision §3 三層架構
ingested_at: 2026-08-07
status: draft
tier: T2
confidence: medium
atlas_go_relevance: high
mcp_tools_used: []
verification: 本頁為路由骨架,實際 L3 端點驗證需跑 `industry_sector_lookup`(已有,上市/上櫃通用)+ `stock_get_quote`(Fugle→TWSE fallback 已 v6.43 修復);**無 atlas 範圍外**端點,因此 L3 走 hermes `data-source-decision` §3 第二層網路備援(尚未實跑)
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §三(對外發布規範)
related:
  - summaries/_division_of_labor_skills_vs_agent.md(分工藍圖)
  - skills/SK-33-audience-routing.md(audience 表達切換)
  - concepts/atlas-mcp-failover-policy.md(4 級 fallback)
  - ~/.hermes/skills/data-source-decision/SKILL.md(三層架構)
---

<!-- methodology_alignment_tip: 三 audience(user/developer/admin)/ 上市 vs 上櫃分流 / 4 級 fallback;對位 SK-00 §1 + SK-33 §五 audience 切換 -->

## 一句話定位

判斷股票代號是否為 atlas 範圍內(上市/上櫃),**對**在範圍內走 atlas-mcp,**對**範圍外(興櫃/未公開/海外)走 hermes `data-source-decision` §3 第二層網路備援 + 標示來源。

## 問題定義(2026-08-07 D4 v1.0)

atlas 系統目前**只涵蓋台灣上市公司 + 上櫃公司**;atlas-wiki 是提供 hermes/OpenClaw 等機器人指引服務的專案,機器人面向用戶時需要服務可能無範圍限制。當用戶問上櫃/興櫃/海外標的時,**不該啞口無言,也不該假裝在 atlas 範圍內**。

對位 hermes `data-source-decision` §3 三層架構:
1. **L1 atlas-mcp**(確定在範圍):直接調用,標 `[來源: atlas-mcp <tool> @ <ISO>]`
2. **L2 網路備援**(確定不在範圍):走 Yahoo Finance / 公開網站 / 政府開放資料,標 `[來源: <站名> @ <URL> @ <ISO>]`
3. **L3 不知道**:誠實標 `[來源: 不知道]` + 引導用戶補資料

## atlas 對位

| 用戶提問 | 判斷路徑 | 動作 |
|---|---|---|
| **上市股票**(4 位數字代碼, TWSE 掛牌,如 2330/2317) | L1 atlas-mcp | 調 `stock_get_fundamentals` / `stock_get_quote` / `stock_get_technical` / `stock_get_chips` |
| **上櫃股票**(4 位數字代碼, TPEx 掛牌,如 6488) | L1 atlas-mcp | 同上市(Fugle v6.43 + TWSE fallback 已含 TPEx 範圍) |
| **興櫃股票**(4 位數字代碼,但未上櫃) | L2 網路備援 | 標 `[來源: TPEx 興櫃 @ <URL> @ <ISO>]`,Yahoo Finance 公開報價 |
| **海外股票**(美股 / 港股 / 大陸股) | L2 網路備援 | 標 `[來源: Yahoo Finance <symbol> @ <URL> @ <ISO>]`,atlas 無資料 |
| **非股票標的**(ETF 期權 / 加密貨幣 / 期貨) | L2 網路備援 | 標 `[來源: <對應站名> @ <URL> @ <ISO>]`,atlas 無資料 |
| **公司名稱模糊**(用戶說「台積電」而非代碼) | L0 名稱解析 | 先解析為代號 2330(可調 `industry_sector_lookup` 對位名單 + 常見對照表),再走 L1/L2 |
| **無對應資料** | L3 不知道 | 標 `[來源: 不知道]`,引導用戶補代碼 / 補來源 |

## 4 級 fallback 鏈(對位 failover-policy.md §4)

1. **L1 atlas-mcp**(上市/上櫃,範圍內)
2. **L2-A TPEx 公開網站**(興櫃,範圍外)
3. **L2-B Yahoo Finance / Investing.com**(海外 / 一般)
4. **L3 不知道**(誠實標示 + 引導)

每個引用都必須附 `[來源: ...@ ISO 8601]`,對位 SK-33 audience-routing §五(user 看不到 error code,admin 看完整 audit 細節)。

## 散戶解讀

- **散戶提問**:「我想看 6488(環球晶)」→「這是上櫃股票,在 atlas 範圍內,我幫你查」→ 走 L1
- **散戶提問**:「我想看 XYZ(興櫃)」→「這是興櫃,atlas 沒有即時報價,我從 TPEx 公開網站幫你查,資料可能有 15 分鐘延遲」→ 走 L2-A,標明延遲
- **散戶提問**:「我想看 NVDA」→「這是美股,atlas 不含海外,我從 Yahoo Finance 幫你查,資料時效以美股交易時間為準」→ 走 L2-B
- **散戶提問**:「我想看 比特幣」→「這不是股票,atlas 沒有,我從 Investing.com 幫你看即時價」→ 走 L2-B
- **開發者提問**:「6488 在 atlas 嗎?」→ 直接答「在,Fugle→TWSE fallback 已含 TPEx v6.43」+ 給 source code 路徑
- **管理者提問**:「6488 為什麼 fallback 到 TWSE?」→ 給完整 audit:`Fugle 503 → circuit_breaker → TWSE 200 source=twse timestamp=2026-08-04`

## 驗證方式

### L1 端點實跑(2026-08-07)
- [ ] `stock_get_fundamentals`(2330/6488)→ 200(已 v6.43 修)
- [ ] `stock_get_quote`(6488 上櫃)→ 200(已 v6.43 Fugle 修,需確認 TPEx 也含)
- [ ] `industry_sector_lookup`(6488)→ 200 sector=半導體

### L2 端點實跑(2026-08-07)
- [ ] Yahoo Finance(NVDA)→ curl https://query1.finance.yahoo.com/v8/finance/chart/NVDA
- [ ] TPEx 興櫃公開(任一 4 位代碼)→ curl https://www.tpex.org.tw/web/stock/afterhour/emerging/

### L3 驗證
- [ ] 用戶問未知標的 → agent 回 `[來源: 不知道]` + 引導補資料

## 未消化 / 待補

- [ ] TPEx 上櫃是否 100% 在 atlas 範圍內(需查 `industry_sector_list` 38 sector 是否含所有 TPEx 類股)
- [ ] Yahoo Finance 公開端點是否有 rate limit(若被擋,備援 = 公開網站 + 政府開放資料)
- [ ] 加密貨幣的可靠公開源(Investing.com / CoinGecko / 其他)
- [ ] 公司名稱模糊解析的常見對照表(目前缺,需建)
- [ ] SK-34 與 SK-33 audience-routing 整合優先序

amendable_by: kaecer