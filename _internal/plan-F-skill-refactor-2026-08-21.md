
# Plan F — Top 5 SKILL.md 拆分 + 未來護欄（執行計畫）

## §0 計畫摘要

**目標**：
1. Top 5 巨型 SKILL.md 拆分（references 子目錄化）
2. 刪除 orphan + 標記 deprecated
3. 設計未來 skill 護欄（lifecycle + 上限 + 競爭）
4. 改用「按需索引」載入（取代 always-on 全量）

**時間**：Week 1-2 執行 + Week 3 護欄上線
**影響**：SKILL.md 平均 size 砍半（14.5KB → 7KB），總 skills 從 146 → ≤ 100
**風險**：拆分時 reference 連結斷裂 → 需 curl 驗證 200

---

## §1 現況盤查（8/21 prime-agent 量化）

### 1.1 量化（146 個 SKILL.md）
- 總 bytes: **2,123,691 B (2.07 MB)**
- 平均 size: 14,545 B
- 最大單個: 130KB (mode-no-guess)
- 完全沒被引用 (orphan): 2 個（vendor-comparison-doc 11.5KB + hermes-themes 7.1KB）
- 無 status 標記: 114 個（78%）
- 已 deprecated: 2 個
- 已 in-transition: 3 個

### 1.2 Top 5 SKILL.md 引用次數 + 拆分現況
| skill | size | 引用 | 已有 references | 拆分候選 |
|---|---|---|---|---|
| mode-no-guess-before-evidence | 130KB | 120 | 5 | appendices A/B/C 拆出 |
| agent-self-judgment-mode | 108KB | 128 | 8 | **Pitfall 53KB 拆出 (53,325 chars)** |
| kaecer-session-trust-patterns | 51KB | 6 | 3 | case-by-case 拆出 |
| personal-knowledge-copilot | 49KB | 187 | 6 | 結構 OK，保留 |
| atlas-skill-discipline | 49KB | 15 | 6 + 1 子 SKILL | 結構 OK，保留 |

### 1.3 需去重 / 刪除清單
| 動作 | skill | 理由 |
|---|---|---|
| **刪除** | vendor-comparison-doc (11.5KB) | orphan 完全沒引用 |
| **刪除** | hermes-themes (7.1KB) | orphan 完全沒引用 |
| **標 deprecated** | kaecer-director-role | skills-map.md 已標 in-transition → task-governance |
| **標 deprecated** | kaecer-managing-up | skills-map.md 已標 in-transition → mode-escalation |
| **標 deprecated** | kaecer-token-discipline | skills-map.md 已標 in-transition → task-knowledge-routing |
| **加 redirect pointer** | agent-reporting-discipline | skills-map.md 已標 → mode-reporting，但 SKILL.md 缺欄位 |

---

## §2 拆分設計（按需載入模式）

### 2.1 拆分原則
- **SKILL.md 只留「何時載入 + 觸發條件 + 工作流骨架 + 必要警告」**（≤ 30KB）
- **細節拆到 references/pitfall-XX.md 或 references/case-XX.md**
- **SKILL.md 開頭加 frontmatter: `index: [references/pitfall-XX.md, references/case-YY.md]`** 給 LLM 索引

### 2.2 Top 5 拆分藍圖

#### (1) agent-self-judgment-mode (108KB → ≤ 30KB)
- 拆出: Pitfall 1~9 → references/pitfall-1.md ~ pitfall-9.md
- SKILL.md 留: 觸發條件 + 必跑流程 + 紅線 + Pitfall index
- 預估: SKILL.md 108KB → 25KB（-77%）

#### (2) mode-no-guess-before-evidence (130KB → ≤ 40KB)
- 拆出: 附錄 A/B/C → references/appendix-A-redo.md / appendix-B-design-vs-bug.md / appendix-C-gap-extrap.md
- SKILL.md 留: 失敗原型 + 紅線 + recipe + pitfall 索引
- 預估: SKILL.md 130KB → 40KB（-69%）

#### (3) kaecer-session-trust-patterns (51KB → ≤ 25KB)
- 拆出: P-F2 / P-5layers / P-2axis / P-3options / P-7layers / P-self-use / P-stub-vs-real / P-trigger-not / P-acted / P-verify / P-summary → references/p-XX.md
- SKILL.md 留: 失策模式清單 + 何時 patch + 自驗清單
- 預估: SKILL.md 51KB → 25KB（-51%）

#### (4) personal-knowledge-copilot (49KB → 維持)
- 結構已 OK，保留
- 但 5 Pillars 內文可拆成 references/pillar-1.md ~ pillar-5.md

#### (5) atlas-skill-discipline (49KB → 維持)
- 結構已 OK，保留
- §4 L3 升 active 流程可拆成 references/l3-promotion-sop.md

### 2.3 「按需索引」載入機制（取代 always-on 全量）

#### 現況問題
- skills index 注入 148 個 skill 名字 + 描述 = 14,385 chars = 5,754 tokens
- 不分場景全量注入

#### 提案（Plan A 範圍）：
- **核心層 (core)**: 5-10 個永遠注入（SOUL/AGENTS/task 路由）
- **活躍層 (active)**: 20-30 個，依任務類型觸發（task-coding / mode-debug 等）
- **冷卻層 (cold)**: 100+ 個，按 skill_view 命令按需載入

---

## §3 未來 Skill 護欄（防止膨脹）

### 3.1 分級上限（config.yaml + SOUL）

```yaml
# config.yaml 提案
skills:
  creation_nudge_interval: 15
  tier_limits:
    core: 10          # 永遠注入
    active: 30        # 任務觸發
    cold: 100         # 按需載入
    total_max: 140    # 總上限（軟警告）
  archive:
    enabled: true
    threshold_days: 90  # 90 天沒被引用 → 自動 archive
```

### 3.2 競爭機制（新增 skill 前必走）

**規則**：
- 新增 skill 前必須跑「競爭 SOP」：
  1. 搜尋現有 146 個 skill 看是否有 70% 重疊
  2. 若有重疊 → 寫成現有 skill 的 references/ 子檔
  3. 若無重疊 → 寫新增提案（1 段）給 kaecer 拍板
  4. 拍板通過才落地 SKILL.md

### 3.3 Lifecycle 自動化管理

- **created**: 新建立
- **draft**: 0-30 天，未驗證（紅標）
- **active**: 30+ 天，有引用（綠標）
- **in-transition**: 60+ 天，路由表標遷移（黃標）
- **deprecated**: 90+ 天，沒引用（灰標）
- **archived**: 180+ 天，移到 `_archive/` 目錄

### 3.4 護欄位置

- **新增護欄 SKILL**: `skills/software-development/hermes-agent-skill-authoring/SKILL.md` §X
- **治理層**: `~/.hermes/skills/skills-map.md` 加「Skill lifecycle 章節」
- **驗證層**: hermes-agent-skill-authoring 加 lifecycle 檢查

---

## §4 執行步驟（Week 1-3）

### Week 1（cheap wins）
1. **Day 1**: 刪除 2 個 orphan（vendor-comparison-doc + hermes-themes）
2. **Day 2**: 標記 3 個 in-transition skill 為 deprecated
3. **Day 3**: agent-reporting-discipline 加 redirect pointer
4. **Day 4-5**: agent-self-judgment-mode Pitfall 拆分（最大優先，53KB → 9 files）

### Week 2（Top 5 拆分完成）
1. **Day 1-2**: mode-no-guess appendices A/B/C 拆分
2. **Day 3**: kaecer-session-trust-patterns P-XX case 拆分
3. **Day 4-5**: personal-knowledge-copilot 5 Pillars references 拆分

### Week 3（護欄上線）
1. **Day 1**: config.yaml 加 tier_limits 設定
2. **Day 2**: skills-map.md 加 lifecycle 章節
3. **Day 3**: hermes-agent-skill-authoring 加 lifecycle 檢查 SOP
4. **Day 4**: 新增 skill 時跑競爭 SOP（示範 1 次）
5. **Day 5**: 寫 `~/.hermes/SKILL_LIFECYCLE.md` 統一規範

---

## §5 驗收條件

### 5.1 拆分驗收
- 每個拆出檔案用 curl 驗證連結 200 OK
- agent-self-judgment-mode Pitfall 章節讀取不報錯
- mode-no-guess appendices 引用正確
- kaecer-session-trust-patterns P-XX 編號連續

### 5.2 護欄驗收
- config.yaml tier_limits 生效
- 114 個無 status skill 標記完成
- 新增 skill 跑競爭 SOP（測試 1 次）
- lifecycle 章節 hermes-skills 認得

### 5.3 量化驗收
- **拆分後 Top 5 總 size**: 387KB → ≤ 180KB（-54%）
- **全 SKILL.md 總 size**: 2,124KB → ≤ 1,500KB（-30%）
- **active skill 數量**: 6 → 30+（標記完成）
- **orphan + deprecated 比例**: 5/146 (3.4%) → ≤ 1/100 (1%)

---

## §6 派工建議

| 工作 | 執行者 | 理由 |
|---|---|---|
| Week 1 Day 1-3（orphan + deprecated 標記） | **hermes 自做** | 純檔案操作，零拍板 |
| Week 1 Day 4-5 + Week 2（Top 5 拆分） | **prime-agent 拆 + hermes review** | 拆分品質需 agent 判斷 |
| Week 3 護欄 config 改動 | **kaecer 拍板 + hermes 實作** | config 改動是治理級 |

---

## §7 風險與回退

### 風險
- 拆分時 reference 連結斷裂 → skill_view 載入失敗
- 護欄啟用後誤刪有效 skill

### 回退
- 每個拆分都做 backup：`SKILL.md.bak.YYYYMMDD-HHMM`
- 護欄啟用先走 7 天 dry-run，只警告不執行
- kaecer 拍板前不啟用自動 archive

---

## §8 與其他計畫的對位

- **Plan A (skills lifecycle 設計)**: 本計畫 §3 已包含，是 Plan F 的子集
- **Plan B (tool 過濾)**: 不在本計畫範圍，獨立執行
- **Plan H (cron 過濾)**: 不在本計畫範圍，獨立執行
