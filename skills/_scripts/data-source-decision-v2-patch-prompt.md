# 派工 Prompt — data-source-decision v1.0 → v2.0 patch

> **target file**: `~/.hermes/skills/data-source-decision/SKILL.md`
> **authorizing**: kaecer 拍板 Day 2 Task A(2026-08-07)+ manifest v1.0 §2 題 1 + §3.1 CR-1
> **context**: `_manifest_coverage_routing.md` v1.0 §2 題 1 + `_inbox_deferred.md` v1.0 + SK-00 + 既有 AGENTS.md §11 內容歸檔規範

## 結論先講

把 v1.0 的 §1 (三層架構) + §2 (端點對位表) + §7 (故障應變流程) **橫向擴兩個新段**:
- **§11 Out-of-Universe Symbol Routing**(對位題 1 結論)
- **§12 Web Fallback Decision**(對位題 2 結論)

**不新建獨立 skill**(對位內容歸檔守則「一個段落只屬於一個檔案,找不到適合就開新,不硬塞」——data-source-decision v1.0 §1 三層架構就是為這層目的設計,擴它最乾淨)。

## 第一段:Target(精確改動範圍)

**只動**:`~/.hermes/skills/data-source-decision/SKILL.md` 這個檔,共兩個新增段。
**不動**:data-source-decision v1.0 既有 9 段(§1~§9 + §10)的任何一行
**不動**:任何 .py 檔、任何 atlas-go 後端檔、任何 wiki 檔
**path-traversal hardening**:本機端檔案(在 `/Users/kaecer/.hermes/skills/`)= 絕對路徑,不接受環境變數覆寫

## 第二段:Change(步驟 — 每步帶驗證)

### 步驟 1 — 備份

```bash
cp ~/.hermes/skills/data-source-decision/SKILL.md \
   ~/.hermes/skills/data-source-decision/SKILL.md.bak.2026-08-07-v2.0
wc -l ~/.hermes/skills/data-source-decision/SKILL.md
```

預期:備份成功 + 印出 v1.0 既有行數(對位 §5.1 SOP)。

### 步驟 2 — 讀檔確認結構

```bash
cat ~/.hermes/skills/data-source-decision/SKILL.md
```

確認:§1~§10 段落齊全(共 10 個 `## `)、frontmatter 9 欄齊全(title / name / description / version / author / license / platforms / created / created_by / triggered_by / sources / related / metadata)。**任一項缺失立即停**——非本派工範圍,落 T3 evidence 退回。

### 步驟 3 — append §11

**用 heredoc append**(對位 `_method.md` §5 SOP)。**verbatim 內容**:

```markdown
## §11 Out-of-Universe Symbol Routing(v2.0 2026-08-07)

### 觸發條件
任何 atlas-mcp `stock_get_*`、`industry_sector_*`、`risk_*`、`*_get_*` 端點 symbol 參數時,**先判斷是否在 atlas universe**:

| symbol 類 | 判斷規則 | atlas 狀態 |
|---|---|---|
| TWSE 集中市場 | 4-5 碼非 80/60/30/50 開頭 | in-universe ✅ |
| TPEx 上櫃市場 | 80 / 60 / 30 / 50 開頭 | in-universe ⚠️(部分覆蓋) |
| 興櫃市場 | 30 / 50 開頭,無 enrich 資料 | out-of-universe ❌ |
| 海外 / 非 TW 標的 | 非 4-5 碼純數字 | out-of-universe ❌ |

### 路由決策
- **in-universe ✅**:走 atlas-mcp 端點(對位 v1.0 §1 三層架構 L1 cache → L2 channel)
- **in-universe ⚠️**:試 atlas-mcp,**失敗走 §12 Web Fallback**
- **out-of-universe ❌**:**直接走 §12 Web Fallback**,不浪費 atlas-mcp 配額

### 對位 wiki
- `~/workspace/atlas-wiki/concepts/atlas-mcp-failover-policy.md` v1.0 §3 4 級 fallback 鏈
- `~/workspace/atlas-wiki/skills/SK-33-audience-routing.md` v1.0 §atlas 對位 tier 表
- `~/workspace/atlas-wiki/skills/_manifest_coverage_routing.md` §2 題 1 + §3.1 CR-1
```

### 步驟 4 — append §12

**verbatim**:

```markdown
## §12 Web Fallback Decision(v2.0 2026-08-07)

### 觸發條件
當 §11 路由到 out-of-universe **或** atlas-mcp 失敗時,依序嘗試 5 個 Web 替代源(對位 `concepts/atlas-mcp-failover-policy.md` v1.0 §4 5 個替代源)。

### 替代表達紀律(對 user audience)
失敗 / 找不到資料時,**禁止表達**:「API 故障」「資料庫錯誤」「根據我的知識」「我建議」。
**唯一合規表達**:`[來源: <站名> @ <URL> @ <ISO 8601 timestamp>]` 格式戳記,**不裝懂、不推估、不外漏 error code**。

### 對位 wiki
- 同 §11 對位清單
- `~/workspace/atlas-wiki/concepts/atlas-mcp-failover-policy.md` v1.0 全部 9 段
```

### 步驟 5 — version bump

frontmatter `version: 1.0.0` → `version: 2.0.0`

### 步驟 6 — change log append(append-only)

在檔尾 append:

```markdown
## Change Log
- v2.0 / 2026-08-07:新增 §11 Out-of-Universe Symbol Routing + §12 Web Fallback Decision(對位 `~/workspace/atlas-wiki/skills/_manifest_coverage_routing.md` v1.0 §2 題 1 + §3.1 CR-1;wiki 詳 `concepts/atlas-mcp-failover-policy.md` + `SK-33-audience-routing.md`)
```

### 步驟 7 — SOP 驗證

```bash
wc -l ~/.hermes/skills/data-source-decision/SKILL.md
# 預期:比 v1.0 多約 35-50 行(§11 + §12 + change log)

diff <(head -N ~/.hermes/skills/data-source-decision/SKILL.md) \
     ~/.hermes/skills/data-source-decision/SKILL.md.bak.2026-08-07-v2.0
# 預期:diff 應為 **no output**(v1.0 內容 byte-perfect 保留)

grep -c "^## " ~/.hermes/skills/data-source-decision/SKILL.md
# 預期:12(v1.0 的 10 + §11 + §12)
```

### 步驟 8 — 對位 fallback source L3 ad-hoc test(若時間允許)

每個 Web 替代源 URL 跑一次 curl,確認 200 + 內容可解析:
- TWSE 公開:`https://mis.twse.com.tw/stock/fibest.jsp?stock=2330`
- TPEx 公開:`https://www.tpex.org.tw/web/stock/after_trading/index.php?l=zh-tw`
- Goodinfo:`https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=2330`
- 公司 IR:跳過(每家不一,無統一 URL pattern)
- 公開新聞:跳過(L3 觸發率低)

每個 200 → log → 截圖證據。不要求全綠,但記錄實跑結果。

## 第三段:Acceptance(可驗收條件)

- [ ] v1.0 既有 10 段 byte-perfect 保留(diff 空輸出)
- [ ] §11 + §12 兩段完整 append,verbatim 內容一致
- [ ] frontmatter version 2.0.0
- [ ] change log 一段 append
- [ ] 5 個替代源 L3 ad-hoc test 跑過(N 條 200 / 失敗率透明)
- [ ] **不是**:不得動 v1.0 既有任何一行
- [ ] **不是**:不得建立新 skill 檔
- [ ] **不是**:不得在 atlas-go 後端、wiki 內、atlas-notes 內落任何字

## 第四段:已禁止事項

對位 SOUL §5 紅線 + AGENTS.md §11 內容歸檔:
- ❌ 「等 hermes owner 回覆」拖延(v6.52 已撤銷 owner 移交,全部在 atlas-wiki 內完成)
- ❌ 把 SKILL v1.0 整檔 rewrite 而非 append
- ❌ 不驗 diff 結果就宣布完成
- ❌ 不附 L3 截圖就跑完

## 第五段:回報格式

對位 AGENTS.md §4(總監對總裁) + _self-audit §6 v6.x:
- 首段一句話:已 patch 完成 / 已卡 / 已退回(具體狀態)
- 3-5 個粗體 bullet,每個附 evidence 路徑 + diff 驗證結果
- 風險單獨列(任何 spec 偏離宣告)
- 不要「請您挑」「是否」「下一步如何」式問句

---

## 變更記錄

- **v1.0 / 2026-08-07 Day 2 A**:首次建立(對位 `_manifest_coverage_routing.md` §3.1 CR-1 + `concepts/atlas-mcp-failover-policy.md` v1.0 + `SK-33-audience-routing.md` v1.0)
