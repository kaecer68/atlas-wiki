---
title: atlas-wiki 金融知識庫改善/修正/優化迭代方案（依 2026-08-22 審計報告）
type: improvement-plan
created: 2026-08-22
created_by: prime-agent (MacBook)
based_on: _internal/audit-2026-08-22-financial/AUDIT-REPORT-main.md（7 HIGH / ~30 MED / ~60 LOW）
status: executing (iteration 1)
governance:
  - 鐵律 4 不違背憲章 / 鐵律 5 快照附 timestamp / 鐵律 6 size 上限
  - 派工備份 SOP：改動前 file.bak.20260822-audit-fix
  - 寫入前 wiki-critic 6 項自審（來源驗證/非猜測/結構化/去重/時效性/可操作性）
  - 合夥人制 §6.4：本批屬重大變更 → branch + PR，kaecer review 後 merge
---

# 改善迭代方案

## 迭代總覽

| 迭代 | 目標 | 內容 | 本 session |
|------|------|------|-----------|
| **Iter 1** | 止血 + 修復 | P0 七條 HIGH 事實修正、6 個失效 trigger、跨頁口徑矛盾、治理瘦身、2 個覆蓋缺口新頁 | ✅ 本次執行 |
| Iter 2 | 驗證 + 裁決 | 4 條爭議事實官方驗證（需網路）、E05 簽核裁決、L1-L5 定義統一裁決、size-check CI 擴充由 warn 轉 enforce | 下次 |
| Iter 3 | 優化 | 誇飾統計清理（99%/9成/3倍/100倍）、PDP 定義統一、.bak housekeeping、「轉折開高」操作手冊頁 | 之後 |

## Iter 1 工作包（WP）與派工

| WP | 內容 | 檔案 | worker | 驗收 |
|----|------|------|--------|------|
| **WP-1 P0 事實修正** | 維持率雙錯、ETF 稅制、外資上限虛構、半年報 45 天、台指期 5 契約月、SK-04 Huber | concepts/taiwan-stock-market-structure.md、atals-risk-management-framework.md、taiwan-chip-flow-analysis.md、taiwan-fundamental-analysis-guide.md、skills/SK-19、skills/SK-04 | child C | 每條 HIGH 對應段落改為正確事實 + timestamp |
| **WP-2 trigger 修復** | 6 失效/矛盾模板 + tsmc-swing 分類錯植 + megaproject 憲章用語 | templates/ 8 檔 | child D | 觸發條件有鑑別力、名實一致、格式不壞（atlas-mcp-trigger-monitor.py 相容） |
| **WP-3 口徑矛盾** | 樣本數/產業數/var_95/experiment_diff/SK-17 加權/SK-20 規模代理/SK-11/13 切分洩漏 | skills/ SK-01/06/09/11/13/17/20/32/36 | child E | 註時點口徑或改為一致；每頁 ≤9000B |
| **WP-4 覆蓋補課** | 新建 L2 + L6 兩頁 | concepts/taiwan-export-orders-semiconductor-cycle.md（新）、concepts/retail-sentiment-indicators.md（新） | child F | wiki-critic 6 項過；無來源數字標 [需驗證] |
| **WP-5 治理修復** | _consult-index 瘦身至 ≤9000B、README/index/log 補登、SK-31 快照 timestamp、審計衍生檔歸檔 | skills/_consult-index.md(+archive)、README.md、index.md、log.md、skills/SK-31 | child G | size 達標、資訊不丟（搬 archive 非刪除） |
| **QC + 落地** | diff 審查、wiki-critic、make ci-gate、commit、push、PR | 全部 | 主 agent（我） | ci-gate 5/5 + diff 無格式破壞 |

## 設計原則

1. **修錯不擴寫**：P0 是「改對」不是「重寫」——每條 HIGH 只動對應段落，保持頁面其餘 byte 穩定。
2. **爭議事實安全寫法**：未官方驗證的（當沖稅 0.25%/0.2%、T+3→T+2 年份、資券當沖減半、冷卻機制窗口）→ **刪除虛構斷言，保留已驗證核心 + 標 [待官方驗證]**，不換上新的未驗證斷言。
3. **size 鐵律**：SK 頁修改後必 ≤9000B（SK-01 8896/SK-22 8964/SK-33 8978 逼近上限,WP-3 註解用精簡一行式）。
4. **檔案互斥**：五個 WP 檔案集合互不重疊,可平行。
5. **新頁守門**：WP-4 新頁的數字只有兩類可入：(a) 憲章/現有 wiki 已有事實 (b) 標 [需驗證] 的通識。
