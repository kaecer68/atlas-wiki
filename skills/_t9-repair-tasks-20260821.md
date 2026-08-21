# T9 修復任務清單 v2 — 2026-08-21 更新盤點

> **版本**:v2 (2026-08-21 重新盤點, prime-agent 從 hermes 8/16→8/21 累積 + prime-agent 8/21 自身探查整理)
> **對位**:v1 = `_t9-repair-tasks-20260815.md` (保留作 audit trail, 8/15 原始審查背景)
> **執行者**:iMac hermes (已承接 atlas-wiki 任務) + prime-agent (8/21 探查協作)
> **位置**:`/Users/kk/workspace/atlas-wiki/`
> **原則**:對位 `_method.md` 六條鐵律 + v6.37 size ≤ 9000B 拍板
> **kaecer 拍板 (2026-08-21)**:T9 重新開新版 (v1 8/15 檔保留作 audit trail, 不刪除)

---

## v1 → v2 變更摘要

| 項目 | v1 (8/15) | v2 (8/21) |
|------|-----------|-----------|
| Fin-Skills.md 找不到 | 已是已知問題 (4 天 [FAILED] 累積) | 仍是問題, 升級為 **6 天 [FAILED] 累積** + 8/20 cron 卡死復盤 |
| Task 1 (SK-34 promotion) | 待辦 (status: draft) | ✅ **已完成** (PR #21, 2026-08-14) |
| Task 2 (SK-31 二擇一衝突) | 待辦 (SK-00 index 標「衝突待解」) | ❌ **未完成**, 仍待 kaecer 拍板 (rebrand vs merge vs 多編號) |
| Task 3 (L3 端點攻堅) | 90 個 Step 待跑 (30 頁 × 3) | ❌ **未完成**, 升級為 **105 個 Step 待跑** (35 頁 × 3, 對位 _inbox.md 8/17 條目) |
| Task 4 (SK-35 補論文版) | 可選, 未做 | ❌ **未做**, 未留評估記錄 |
| **新發現 (8/21 探查)** | — | 8/20 cron 卡死復盤 + 6 天嘗試失敗 (見 §新發現 A + §新發現 B) |

---

## Task 1: SK-34 draft → active ✅ 已完成

**狀態**:PR #21 (2026-08-14) `feat(atlas-wiki): SK-34 真實 promotion + L3 端點 5/5 200 + v6.59 overclaim 修正(D6 補登)` 已 merge main。

**實證**:`skills/SK-34-listed-otc-routing.md` frontmatter `status: active`。

**後續**:
- [x] L1: `stock_get_fundamentals`(2330/6488) → 200 — 對位 PR #21
- [x] L1: `stock_get_quote`(6488 上櫃) → 200, 確認 TPEx 範圍 — 對位 PR #21
- [x] L1: `industry_sector_lookup`(6488) → 200, sector=半導體 — 對位 PR #21
- [x] L2: Yahoo Finance(NVDA) curl 測試 → 有回應 — 對位 PR #21
- [x] L2: TPEx 興櫃公開 curl 測試 → 有回應 — 對位 PR #21
- [x] L3: 未知標的 → agent 回 `[來源: 不知道]` + 引導 — 對位 PR #21
- [ ] TPEx 上櫃是否 100% 在 atlas 範圍 (查 industry_sector_list 38 sector) — 未消化待補
- [ ] Yahoo Finance rate limit 測試 — 未消化待補
- [ ] 加密貨幣可靠公開源確認 — 未消化待補
- [ ] 公司名稱模糊解析對照表 (目前缺) — 未消化待補

---

## Task 2: SK-31 二擇一衝突 ✅ 已完成 (2026-08-21 kaecer 拍板方案 b renumber, kimi-for-coding 審查 8 步執行)

**狀態**:`SK-31-sl-vs-rl.md` 已重新編號為 `SK-36-sl-vs-rl.md`(2026-08-21 kaecer 拍板方案 b, kimi-for-coding 審查 8 步執行);`SK-31` 唯一對應 `SK-31-ai-investment-cycle-2026.md`(AI 投資週期)。

**執行 8 步**:
1. `git mv SK-31-sl-vs-rl.md → SK-36-sl-vs-rl.md` (PR #32) + 修 frontmatter `renumbered_from: SK-31`
2. 修 4 個引用: SK-32-reward-sensitivity.md / _methodology_alignment_audit.md / _index-finskills.md / SK-00-skill-index.md
3. 修 T9 v2 Task 2 段 (本段) + 驗證 grep

**結論**:✅ 衝突已解決, 36 個 SK-* 檔案 (原 35 + SK-36 新編號)。

---

## Task 3: L3 端點批次執行 ❌ 未完成 + 數字需 kaecer 拍板

**狀態**:`_inbox.md` line 35「90」(歷史) vs line 129「**105**」(現況, kaecer 拍板統一, 見拍板 1)。

**注意**:Task 3 **不需 Fin-Skills.md**, 與 Fin-Skills 6 天 [FAILED] 是**獨立問題**。

**建議執行**: 在 02:00 每日 cron 批次跑, 每頁 3 step 實跑, 不做「假驗證」, 完成 → 更新該頁 verification + _inbox 進度 + 統一 90 vs 105。

---

## Task 4: SK-35 補「論文版」段 ❌ 未做, 未留評估記錄

**狀態**:SK-35 從 8/7 commit (67e0433) 後**完全無變動**, 也未在 T9 v1 (8/15) 後做任何評估記錄。

**實證** (`git log -3 skills/SK-35-mcp-failover.md`):
> 「67e0433 2026-08-07 23:57:39 +0800 feat(atlas-wiki): v6.56 F 路徑重構 + 9 條未完成工作全完成 (#16)」

**建議決策** (kaecer 拍板):
- (A) 不做: 維持「源於 hermes skill」定位, SK-35 仍是 skill-inbound 性質, 不需對位學術論文
- (B) 做: 加一段「起源說明」+ 找對應學術概念 (容錯/備援設計, 如 failover pattern literature)

---

## 新發現 A (8/21 prime-agent 探查): 8/20 atlas-skill-inbound cron 卡死

**狀態**:8/20 04:00 atlas-skill-inbound cron 有觸發 (session `cron_8fd1b1eda764_20260820_040021`), 但**卡在 API call #6 的 `execute_code` 會員權限錯誤後, 無後續 log**, 沒完成到 _inbox.md append 步驟。

**詳細復盤**:見 `_inbox.md` §「[FAILED — 復盤] 2026-08-20 atlas-skill-inbound cron 卡死」條目 (PR #27 已 merge)。

**根因 (雙重)**:
1. **直接原因**: atlas-skill-inbound 在 `execute_code` 工具被會員權限擋後 LLM 卡死, 沒完成到 _inbox.md append 步驟
2. **補跑失敗**: 06:09 hermes 收到 SIGTERM 重啟, cron scheduler state 丟失, 未觸發 grace=7200s 補跑機制

**修復任務 (給 hermes 下次手動處理)**:
- [ ] **A1**: atlas-skill-inbound 應避免依賴 `execute_code` 工具 (需 basic 以上會員權限, 對位 hermes agent.log 8/20 WARNING)
- [ ] **A2**: hermes cron scheduler 應持久化 job state (避免 SIGTERM 重啟丟失 grace 補跑, 對位 8/15 補跑範例 vs 8/20 補跑失敗)

**PR #27 措辭衝突**: PR #27 寫「8/21 恢復正常」(指 cron 系統恢復, 對位 agent.log 8/21 04:00 觸發 + 04:04:12 completed), 但 8/21 [FAILED] 條目仍標失敗 (Fin-Skills 根因沒解)。**系統 vs 任務** 視角不同, 見「待拍板 2」。

---

## 新發現 B (8/21 探查): 8/16~8/21 連 6 天嘗試失敗 (5 天有 [FAILED] 紀錄 + 8/20 卡死)

**狀態**:8/16~8/21 atlas-skill-inbound **6 天嘗試 append `_inbox.md` 都失敗**, 但**只有 5 天有 [FAILED] 紀錄** (8/16, 8/17, 8/18, 8/19, 8/21); 8/20 cron 觸發但卡死, 無 _inbox.md append, 改記為 `[FAILED — 復盤]`。

**對位**:`_inbox.md` 5 個 [FAILED] 條目 (8/16, 8/17, 8/18, 8/19, 8/21) + 1 個 8/20 復盤條目 (PR #27 已 merge)。

**3 條路 (從 8/16 條目升級建議) 等 kaecer 拍板**:
- (A) 復原 Fin-Skills.md → 請貼路徑 / `git log` 證據, 本 cron 立刻可繼續
- (B) 切換 Phase 2 來源 → 對位 Tej / 永豐金 / 凱基 / 學術 journal (需 kaecer 拍板新來源)
- (C) 收口停掉此 cron → 現有 35 頁 active + 2 archive 為最終交付物

**8/18 kaecer out-of-band 指令對位** (從 _inbox.md 8/18 條目):
> 「已連續 2 天 [FAILED] 8/16 + 8/17,這是升級條件,請用最高總監級決策輸出最終陳述」
→ 8/18 結論: atlas-skill-inbound Phase 1 正式收口, 8/19 起改 on-call gate (只 [SILENT] + _inbox.md 留 [FAILED])
→ **8/21 觀察**: 8/19 ~ 8/21 沿用 on-call gate, 持續 [FAILED] 累積

**誠實標記** (8/21 prime-agent 評估): **atlas-skill-inbound Phase 1 實質收口**, 但 kaecer 仍未拍板 A/B/C, 需 kaecer 拍板才能結束 cron 阻塞。

---

## 執行原則 (對位 _method.md 第 5 條 SOP 備份)

1. **所有改動前後備份** (byte-perfect 對位)
2. **size 檢查**: 改後 `wc -c` ≤ 9000 bytes (本檔現況 8925B, 已用 99%, 後續編輯注意)
3. **CI 對位**: 改完跑 `make ci-gate` (atlas-wiki 本地驗證)
4. **commit + push + PR**: 依 atlas-wiki 既有流程, 對位 `docs/git-merge-protocol.md` §6.4.1 routine merge
5. **不裝完成**: L3 沒實跑 = 保持 draft, 如實標註 (對位鐵律 3)
6. **CLAUDE.md 引用遷移**: 待 kaecer 拍板 (見下方 §待 kaecer 拍板)

---

## 待 kaecer 拍板 (7 項)

1. **L3 攻堅範圍**: ✅ **kaecer 2026-08-21 拍板 = 105** (35 active × 3 step)。
2. **8/21 是否真的恢復**: PR #27 寫「cron 系統恢復」(對位 hermes agent.log 8/21 04:00 觸發 + 04:04:12 completed), 但 8/21 [FAILED] 條目仍標失敗 (Fin-Skills.md 找不到根因沒解)。**系統 vs 任務** 視角不同, 後續如何標記?
3. **Task 2 SK-31 衝突**: (a) 合併 / (b) renumber → SK-36 / (c) 保留雙頁? (預設 (b))
4. **Task 4 SK-35 論文版**: (A) 不做 / (B) 做? (8/21 評估: SK-35 屬 skill-inbound, 學術對位非必要, 預設 (A))
5. **新發現 B Fin-Skills.md 6 天找不到**: (A) 復原 / (B) 切 Phase 2 / (C) 收口停掉?
6. **CLAUDE.md 第 18 行引用遷移**: 從 8/15 改為 8/21? (治理檔變更, 按 §6.4.2 需人工 review)
7. **新發現 A 8/20 cron 卡死修復**: 派 hermes 處理 A1 + A2 兩項修復任務?
