# T9 修復任務清單 — hermes 可執行 (2026-08-15)

> 來源: 2026-08-15 prime-agent 對 atlas-wiki skills 的 T9 技能轉化審查
> 執行者: iMac hermes (已承接 atlas-wiki 任務)
> 位置: /Users/kk/workspace/atlas-wiki/
> 原則: 對位 _method.md 六條鐵律 (不搬運/不瞎寫/不裝完成/不違憲章/派工備份/size ≤9000B)

---

## 審查結論 (背景)

35 個 SK 頁四層結構 (論文/atlas/散戶/驗證) 36/37 完整, 憲法對位 37/37, size 全合規。
真正待辦集中在 2 個 SK + 1 個已知批次工作:

---

## Task 1: SK-34 draft → active (最高優先)

**檔案**: `skills/SK-34-listed-otc-routing.md` (status: draft, 5465B)

**目標**: 完成 L1/L2/L3 端點實跑驗證, 升 status: active

**必須完成** (frontmatter verification 欄的 checkbox):
- [ ] L1: `stock_get_fundamentals`(2330/6488) → 200
- [ ] L1: `stock_get_quote`(6488 上櫃) → 200, 確認 TPEx 範圍
- [ ] L1: `industry_sector_lookup`(6488) → 200, sector=半導體
- [ ] L2: Yahoo Finance(NVDA) curl 測試 → 有回應
- [ ] L2: TPEx 興櫃公開 curl 測試 → 有回應
- [ ] L3: 未知標的 → agent 回 `[來源: 不知道]` + 引導

**未消化待補項** (記錄真實狀態, 不裝完成):
- [ ] TPEx 上櫃是否 100% 在 atlas 範圍 (查 industry_sector_list 38 sector)
- [ ] Yahoo Finance rate limit 測試
- [ ] 加密貨幣可靠公開源確認
- [ ] 公司名稱模糊解析對照表 (目前缺)

**驗證通過條件**: L1 三項全 200 → status: active + verification 更新為實跑結果

---

## Task 2: SK-31 二擇一衝突解決

**檔案**: `skills/SK-31-ai-investment-cycle-2026.md` + `skills/SK-31-sl-vs-rl.md`

**背景**: SK-00 index 標記「SK-31 二擇一衝突待解決」——兩個檔案共用 SK-31 編號。

**必須完成**:
- [ ] 讀兩檔, 確認各自定位 (ai-investment-cycle vs sl-vs-rl)
- [ ] 決定: (a) 合併為一頁 (b) 重新編號其中一個 (c) 保留雙頁但 index 明確說明
- [ ] 更新 SK-00 index 的 SK-31 條目, 消除「衝突待解」標記
- [ ] 確保兩檔都符合四層結構 + size 上限

---

## Task 3: 90 個 L3 待驗端點批次執行

**背景**: `_inbox.md` 記錄「30 active 頁 × 3 step = 90 個 Step 待跑」(給 02:00 每日 cron)

**目標**: 逐頁驗證 L3 端點, 更新各 SK 的 verification 欄

**執行方式**:
- 依 _inbox.md 既定排程 (02:00 每日 cron) 批次跑
- 每頁: 確認 verification 欄的 L3 端點可達 (atlas-mcp 200)
- 完成一頁 → 更新該頁 verification + _inbox 進度
- 不做「假驗證」— 端點不通就標待驗, 不裝完成 (對位鐵律 3)

---

## Task 4 (可選): SK-35 補「論文版」段

**檔案**: `skills/SK-35-mcp-failover.md`

**背景**: 缺「論文版概念」層, 但它源於 hermes 內部 skill (data-source-decision §3), 非 Fin-Skills 論文。

**評估**: 若維持「源於 hermes skill」定位, 可加一段「起源說明」而非論文對位; 若需對位論文, 找對應學術概念 (容錯/備援設計)。

**不做也行** — 記錄評估結論即可, 不強制補。

---

## 執行原則

1. **所有改動前後備份** (對位鐵律 5: 派工備份, byte-perfect)
2. **size 檢查**: 改後 `wc -c` ≤ 9000 bytes
3. **CI 對位**: 改完跑 `make ci-gate` (atlas-wiki 本地驗證)
4. **commit + push + PR**: 依 atlas-wiki 既有流程 (完成後 PR 給 kaecer review)
5. **不裝完成**: L3 沒實跑 = 保持 draft, 如實標註
