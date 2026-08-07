---
title: manifest-2026-08-07-D4 未完成工作 9 條全部修復
type: manifest
status: in-progress
created: 2026-08-07
amendable_by: kaecer
sources:
  - skills/_method.md §第七條例外(line 177-183)
  - skills/_self-audit.md §6
  - AGENTS.md §7 kaecer 關鍵決策
---

# manifest-2026-08-07-D4 未完成工作 9 條全部修復

> **範圍**:本 session 盤查出的 9 條未完成工作,依序執行,每條附 SOP §5.1 驗證。
> **終位條件**:全部 9 條標 `done`,無 pending,無 blocked。
> **檔案命名**:`manifest-2026-08-07-<seq>-unfinished-9.md`,本日(D4)第二份 manifest。

---

## 工作清單(9 條)

| 序 | 工作 | 對位檔案 | 驗證方式 | 狀態 |
|---|---|---|---|---|
| 1 | SK-00 升 active + size 偏差(35 ≠ 33) | `skills/SK-00-skill-index.md` | grep `status: active` ✓ + line 51 驗證補上 | [ ] |
| 2 | SK-27 + SK-30 確認歸檔標一致性 | `skills/SK-27-quantum-policy.md`、`skills/SK-30-quantum-stability.md` | 兩檔 frontmatter `archive: true` + 內文一致 | [ ] |
| 3 | `_inbox.md` 15201B > 12000B 歸檔啟動 | `skills/_inbox.md` + `_inbox_archive.md` | wc -c ≤ 12000 + 歸檔段檔完成 | [ ] |
| 4 | 上市/上櫃分流 skill 撰寫 | `skills/SK-XX-listed-otc-routing.md`(新) | 6 段格式 + frontmatter 9 欄 + ≤ 9000 bytes | [ ] |
| 5 | failover-policy 接 hermes/OpenClaw skill + 升 active | `concepts/atlas-mcp-failover-policy.md` + 新 SK | 對位 hermes `data-source-decision` + active 標 | [ ] |
| 6 | 散戶 vs 系統管理員分眾機制 | `skills/SK-XX-audience-routing.md`(新,參考 SK-33) | frontmatter `audience: [user, admin]` + 雙層解讀 | [ ] |
| 7 | skills vs agent 文件分工(落 AGENTS.md) | `AGENTS.md`(新增段) | `## §X 文件分工` + 對位事項總表 | [ ] |
| 8 | `_method.md` line 41 越界擴充的補救派工 | `skills/_method.md` line 41 | 對位 SOUL §3.7.3 第 6 條邊界 + 派工記錄 | [ ] |
| 9 | Todo tool 死循環問題排除 | 系統層 | todo tool 改用「不寫 todo,直接線性工作」,並將決策落此 manifest | [x] |

---

## SOP §5.1 預設驗證項

- 每項完成:`grep -n` + `wc -c` + `head -N` 三項確認
- 每項變動前:`cp <file> <file>.bak.2026-08-07-D4-M<N>`(N = 條目編號)
- 每項變動後:`md5 -q` 確認 byte-perfect 對位備份

---

## 派工依賴

```
[4] → [5] → [6]   # 都需要先有「概念基礎」才能升 skill
[8] 獨立          # 規範本體對位,SOUL §3.7.3 第 6 條
[3] 獨立          # 歸檔 SOP,規範第七條例外
[1] [2] [7] [9] 獨立  # 各為檔案層修改
```

---

## 完成簽核

本 manifest 由 kaecer 2026-08-07 拍板,授權 agent 依序執行。
完成後請 agent 將每條 `[ ]` 改為 `[x]`,並補上對位 file path + bytes + timestamp。