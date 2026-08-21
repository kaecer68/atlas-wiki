# Plan A — Skills Lifecycle 落實（2026-08-21）

## §1 設計正本

完整設計見：
- `~/workspace/atlas-wiki/_internal/skills-map-tier-index-design-2026-08-21.md`
- `~/.hermes/skills/skills-map.md` 「分層索引機制」段（已落地）

## §2 落地優先序

### Week 3 Day 1-5

1. **Day 1（已完成）**: skills-map.md 加分層索引機制段
2. **Day 2**: config.yaml `[skills]` 加 `tier_limits` + `archive` 設定
3. **Day 3**: hermes-agent-skill-authoring 加護欄 SOP
4. **Day 4**: 144 個 SKILL.md 跑貢獻度評判 SOP 分層
5. **Day 5**: 示範 1 次「新增 skill 跑競爭 SOP」

## §3 config.yaml 提案

```yaml
# ~/.hermes/config.yaml
skills:
  creation_nudge_interval: 15
  tier_limits:
    core: 10
    active: 50
    cold: 100
    total_max: 160
  archive:
    enabled: true
    threshold_days: 90
    auto_archive: false  # 軟警告，需 kaecer 拍板
  evaluation:
    dimensions: [engineering, business, management, currency]
    cadence_days: 30
```

## §4 hermes-agent-skill-authoring 加 SOP

新增 skill 必跑：
1. 搜尋現有 144 個 skill 找 70% 重疊
2. 有重疊 → 寫 references/ 子檔
3. 無重疊 → 寫 1 段提案給 kaecer 拍板

落地方式：append 章節到現有 SKILL.md 「## How to Run」。

## §5 144 個 SKILL 分層（Day 4 跑）

按 §2 評估 SOP 逐個跑，輸出 `skills-tier-classification-2026-08-21.md`。

