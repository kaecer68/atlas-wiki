---
title: skills vs agent 系統文件分工(2026-08-07 D4)
type: reference
status: draft
created: 2026-08-07
amendable_by: kaecer
sources:
  - skills/SK-33-audience-routing.md(2026-08-07 Day 1 落地)
  - concepts/atlas-mcp-failover-policy.md(2026-08-07 v1.0)
  - AGENTS.md §11 內容歸檔規範
  - 對位 SOUL §3.7.3 跨邊界治理
---

# skills vs agent 系統文件分工(2026-08-07 D4 v1.0)

> **一句話**:對位 hermes / OpenClaw 等機器人面向用戶時,**資料與指引分離**——atlas-mcp 工具數據由 `skills/` 提供,使用者判斷與口徑由 agent 文件(`AGENTS.md` + `summaries/` + `~/.hermes/SOUL.md`)治理。

---

## 1. 三層分工

| 層 | 範圍 | 文件 | 治理者 |
|---|---|---|---|
| **L1 工具能力** | atlas-mcp 110+ 工具的調用方式、輸入輸出、約束 | `skills/SK-*.md`(SK-01~33)+ `concepts/atals-mcp-tools-reference.md` | kaecer + atlas owner |
| **L2 解讀紀律** | 工具回傳值如何解讀、何時該用、誤用警告 | `skills/SK-00-skill-index.md` + `concepts/atlas-mcp-interpretation-guide.md` + `concepts/atlas-mcp-failover-policy.md` | kaecer + agent |
| **L3 表達口徑** | 對誰說(user/developer/admin)、怎麼說(降級口徑 vs debug 細節) | `skills/SK-33-audience-routing.md` + `AGENTS.md` §1 角色定位 + `~/.hermes/skills/financial-advisor-coach/SKILL.md` §X | kaecer + hermes/OpenClaw owner |

---

## 2. 對位 9 條未完成工作(manifest-2026-08-07-D4-unfinished-9)

| 條目 | 適合層 | 解法 |
|---|---|---|
| 1. SK-00 升 active | L1 | skills/ 層改動 |
| 2. SK-27/30 archive | L1 | skills/ 層改動 |
| 3. _inbox 歸檔 | L2 | skills/ 規範層改動(第七條例外) |
| 4. 上市/上櫃分流 | L1+L2 | 新 SK-XX + 對位 agent 文件 |
| 5. failover-policy 升 skill | L1→L2 | 升 SK-XX + 對位 hermes `data-source-decision` |
| 6. audience-routing | **已存在**(SK-33) | — |
| 7. **本檔**(skills vs agent 分工) | L3 | 落 `summaries/`(AGENTS.md 已 10601B 接近 11000B 上限,不擴充) |
| 8. _method.md 越界擴充補救派工 | L2 | 走 task-governance |
| 9. Todo tool 死循環 | L3(系統) | 決策「不寫 todo,線性工作」(本檔) |

---

## 3. 邊界與治理

- **改 `skills/`**:kaecer + agent 可動,但**規範本體(_method.md / _SKILL.md)** 須 kaecer 拍板
- **改 `AGENTS.md`**:kaecer + agent 可動,但**自我上限**必須先擴(本檔採獨立檔替代,避免撞上限)
- **改 `~/.hermes/SOUL.md`**:僅 kaecer 可動(跨 session 靈魂檔)
- **改 hermes runtime 設定(env / config)**:hermes owner,atlas-wiki agent **不外推**(對位 v6.52 撤銷外推決策)

---

## 4. 條目 4-5 待續

- **條目 4 上市/上櫃分流 skill**:L1 工具能力層,新 SK-XX(命名建議:SK-34-listed-otc-routing),對位 hermes `data-source-decision` §3
- **條目 5 failover-policy 升 skill**:L2 解讀紀律層,新 SK-XX(命名建議:SK-35-mcp-failover),對位 SK-00 §1 三條 pipeline 之外的元能力

兩個新 SK 待 kaecer 拍板。

amendable_by: kaecer