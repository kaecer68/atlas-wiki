---
title: Iter-2 裁決簡報：E05 資金分類 + L1-L5 命名衝突
created: 2026-08-22
type: decision-brief
status: E05 已裁決（發現）/ L1-L5 採 Option A 執行
---

# Iter-2 裁決簡報（2026-08-22）

## 一、E05 資金勢力分類 — 調查結論：裁決已存在,殘留是過時文件

### 時間線（ground truth）
- **2026-07-17 atlas spec v1.0** `docs/specs/capital-flow-seven-dimension-spec.md`：「**決策狀態：設計已由業主接受**」;「取代語意：取代『七大勢力皆為同級資金主體』**及『五大主體、另兩項僅為待刪除資料』兩種過度簡化說法**」
- 2026-07-18 wiki E05 提案（concepts/funding-forces-taxonomy-e05-pending-approval.md）：5 主體共振方案 — **正是 spec D-CF-03 明文拒絕的方案**（官股/散戶無官方日資料品質,不能假裝同質主體）
- 2026-07-22 spec mtime（內容含 D-CF-03/04/05 + participates_in_actor_consensus 機制）

### 已被接受的設計（3+2+2）
- 官方法人（3）= 外資/投信/自營（T86 第一方）→ **共振模型只看這層**
- 行為代理（2）= 官股/散戶 → 缺資料不補 0,不進共振
- 領先/跨市場訊號（2）= 外資期貨 OI / TSM ADR → 非資金主體

### 殘留處置
1. **wiki E05 檔**：標「已被 atlas spec 取代（業主 7/17 接受 3+2+2）」— 事實性文件修正,Iter-2 自主執行
2. **atlas product-positioning.md §7 仍標「⚠️ 待業主簽核」= 過時標記**（與 spec「已由業主接受」矛盾）→ atlas 目錄對 MacBook 唯讀,**移交 kaecer/iMac hermes 修**
3. **唯一真正待裁決小題**：E05 原案的 VIX / USD_TWD「情緒調整層」概念未被 spec 收編（spec 7 維無此兩項;VIX 僅存於 janus regime 公式）。要不要情緒層 = 產品決策 → **保留給 kaecer,但可下次再議,不阻塞**

## 二、L1-L5 命名衝突 — 四個命名空間,採 Option A 修復

### 證據：「L1-L5」在四處不同意義
| # | 命名空間 | 出處 | 內容 |
|---|---------|------|------|
| N1 | L1-T 範式系列 | entities/l1-t*（kaecer 拍板,2026-07） | L1=真實驅動層→L5=散戶情緒;T.1~T.6 子範式 |
| N2 | 憲章因果傳導鏈 | ATLAS_METHODOLOGY.md §二 | **中文**「第〇~六層」（第六層=散戶情緒）;憲章本身不用英數 L 標記 |
| N3a | wiki 策略分類 L1-L5 | concepts/atals-strategy-taxonomy.md §4（2026-08-02 wiki 自建） | L1 總經驅動/L2 資金流向/L3 國際連動/L4 市場結構/L5 地緣風險 |
| N3b | **atlas 代碼 canonical** | internal/strategy_techniques/enums.go | L1 全球流動性/L2 外資行為/L3 產業催化/L4 匯率籌碼/L5 地緣政治 |

**N3a ≠ N3b**：wiki 策略分層名稱與生產代碼不一致（L3/L4 全錯）— 這是事實錯誤,不是風格問題。
**N2 污染**：2026-08-22 新建兩頁用了英數 L2/L6 標記指因果鏈層級,與代碼 L2（外資行為）撞名。

### Option A（已採用執行）
1. **L1-L5 標籤所有權歸 atlas 代碼**（strategy_techniques.Layer,生產 canonical）
2. wiki 策略文件（N3a）對齊代碼定義（N3b）— 事實修正,11 檔
3. 憲章因果鏈一律用中文「第〇~六層」;修正 Iter-1 兩新頁的英數標記
4. N1 L1-T 範式系列保留歷史名稱（kaecer 拍板過）,各檔加一行消歧註

### 裁決點
Option A 無需改名任何 kaecer 拍板過的產物,純文件對齊代碼 ground truth → **依「繼續派工解決」授權自主執行**。
若 kaecer 要不同裁決（如因果鏈改用 C0-C6、L1-T 改名）,回退點 = 本批 commit。
