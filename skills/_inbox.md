# atlas-skill-inbound Inbox

最後更新:2026-10-21 atlas-skill-inbound tick（§CIO-2010；C 項 `wc -c` 二次量測結案 = 不需 split；`check-stale` 91.5h 未提交項處置 + §第七條 v1.1 歸檔 5,806 B，主檔收為 8,911 B）;前次更新:2026-10-16 週末 lint 解讀（Stale 4 條首進 l1-t4/l1-t5）;前次更新:2026-09-27 模板類 quota 拍板結案(不計入;條文入 `_method.md:121`);前次更新:2026-09-27 模板狀態校正 ＋ templates quota 條文查核（同日另段:結清兩項長期待辦）;前次更新:2026-08-21 v2 session 修補(8/21 補登（見 T9 v2）— 共同根因: A1 execute_code 會員權限 + A2 terminal 180s timeout, 修復任務 A1+A2 已寫入 hermes-governance-log T3-A493 條目請 hermes 下次 trigger 處理, 詳見 _inbox_archive.md §6 8/21 條目);前次更新:2026-08-21 歸檔 session(PR #29);前前次更新:2026-08-12 D6 session 結算(SK-34 真實 promotion + v6.59 overclaim 修正);前前前次更新:2026-08-07 D4 session 結算(`_inbox.md` size 15201B > 12000B 上限 → 啟動第七條例外歷史段歸檔 → 歷史段 5261B 移至 `_inbox_archive.md` v1.0,主檔縮為 3589B); 前前次更新:2026-08-07 16:50 (CR-2026-08-07 擱置區邊移 → v6.52 撤銷外推,改內部化)

> 2026-08-07 D4 結算段（總體進度 ＋ 最後更新對位事實,2,816B）已於 2026-09-27 依 `_method.md` 第七條例外移入 `_inbox_archive.md`。


---
## 對位 `_method.md` 第七條例外

規範**唯一來源**＝`_method.md` 第七條例外（v1.0，2026-09-02 拍板更新）：本檔上限 ≤ 12000 bytes，append 前 `wc -c` 自查，超限即依該條歸檔 SOP 移 `_inbox_archive.md`。

## 30 秒重啟程序

見 `~/.hermes/skills/atlas-skill-inbound/SKILL.md` §重啟後 30 秒回神程序

---

## 待辦（active；本文以下至「已結案」標題前，預算 ≤ 8,000 B）

## 2026-10-21 atlas-skill-inbound tick — C 項 `wc -c` 二次量測結案（§CIO-2010）

**C 項已實測結案 = 不需 split。** 2026-10-16 清單 C 項要求「需 `wc -c` 二次量測才能下『需 split』結論」,本 tick 實跑完成:

| 頁 | lint 行數 | 實測 bytes | 類別上限(`_method.md:42`) | 判定 |
|---|---|---|---|---|
| `concepts/atlas-mcp-tools-reference.md` | 482 | **23,834 B** | 30,000 B/頁 | ✅ 預算內,無需 split |
| `concepts/taiwan-financial-domain-model.md` | — | 28,779 B | 30,000 B/頁 | ✅ 全 concepts+entities 最大值,仍在預算內 |
| `entities/l1-t2-petrodollar-hormuz.md` | — | 25,831 B | 30,000 B/頁 | ✅ 預算內 |

**關鍵更正**:C 項原文「逼近硬上限」的前提**不成立**。`_method.md` 第七條表列 concepts/entities 為**per-page 30,000 B**(「參考/資料型勿硬砍;最大 28,029」),非 namespace 加總;實測最大頁 28,779 B < 30,000 B。lint 只報行數不報 bytes,以行數推 size 是錯誤量測單位(對位 USER §1 第 2 條「禁止單一 evidence 直接寫結論」)。⇒ **原建議「先處理 `atlas-mcp-tools-reference` split」撤銷**,13 條 >200 行頁全部列為觀察區,不開 split PR。

**L1 gate 實跑**:`make ci-gate` 全綠(16 項),`make check-size` 40/40 頁 ≤9000 B,`check-source-tiers`(S3)0 缺口,`check-freshness`(S6)0 缺口 0 逾期,`[待驗]` marker 0 條 ⇒ 主任務「6 段/evidence gap filling」本日 0 可關缺口。

**check-stale 發現並處置**:`skills/_inbox.md` + `_inbox_archive.md` 工作區未提交 91.5h(門檻 48h,違 `_method.md` 第九條)。本次落地即為該項修復:移出過期 WIP branch `fix/trigger-margin-350b-l3-2026-09-28`(落後 origin/main 27 commits),改走新 branch `ci/inbox-archive-2026-10-21`。備份 `inbox-main-backup-20261021.md` md5 `5482d8b497a7109525dcc474d6dfdef7`(7,402 B)實存。

**§第七條歸檔**:append 後主檔 14,717 B > 12,000 B 上限 ⇒ 依 v1.1 將 D6 待辦 / 結清兩項長期待辦 / 2026-09-27 S6 待複驗佇列 / 已結案段(5,806 B)移入 `_inbox_archive.md` §[2026-10-21 自 _inbox.md 歸檔],主檔收為 **8,911 B**(含本 tick 段)。S6 待複驗 9 頁佇列為 active 未結項,已原文保留於 archive 未刪。

**對位**:`make ci-gate` / `make check-size` / `make check-stale` 2026-10-21 CST / `_method.md:39-45` size 表 + 第七條 v1.1 + 第九條 / USER §1 第 2 條 Hard NOs / SOUL §4.1 自己判斷立即執行。

---

## 已結案（近期；預算 ≤ 4,000 B，超出即移 `_inbox_archive.md`）

- **C 項「`atlas-mcp-tools-reference` 482 行需 split」→ 撤銷**（2026-10-21 實測 23,834 B < 30,000 B/頁上限，§CIO-2010）。原建議基於 lint 行數推 size，量測單位錯誤。
- 2026-09-27 模板狀態校正（SK-31）＋ 模板類 quota 條文查核（**已拍板結案**）⇒ 原文已歸檔 `_inbox_archive.md` §[2026-09-30 自 _inbox.md 歸檔]（2026-09-30）
