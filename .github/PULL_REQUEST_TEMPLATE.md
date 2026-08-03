## Summary

<!-- 一到三句:這個 PR 做什麼、為什麼做。對位 _method.md 第 1 條鐵律「不搬運,翻譯」的 spirit:用三層語言描述。 -->

### 變更類型(必勾一個)

- [ ] 新增 SK 頁(對位 _method.md §1.1 + §4)
- [ ] 修訂 SK 頁(對位第 5 條鐵律:快照值必附 timestamp)
- [ ] 修索引/規範檔(_method.md / _inbox.md / _consult-index.md)
- [ ] 修 CI 工具或 workflow
- [ ] 修 README / 治理檔

## Root Cause / 動機

<!-- 為什麼需要這個變更?引用 T3 evidence / issue / 對話節錄。 -->

## Verification

<!-- 必勾 + 填寫證據。對位 _method.md 完成定義 + 第 5 條鐵律。 -->

- [ ] 本地 `make ci-gate` 風格手動驗證 4 項(timestamp / audit / size / frontmatter)全綠
  - 結果:
- [ ] 新增頁/變更頁的 frontmatter 10 欄齊全
- [ ] 單頁大小 ≤ 9,000 bytes
- [ ] L3 端點驗證(若 status 升 active):tool_name + timestamp 引用
- [ ] 第 5 條鐵律:快照值附 timestamp + 端點名稱

## 對位檢查(每頁變更必填)

- 憲章:`~/workspace/atlas/docs/ATLAS_METHODOLOGY.md` v1.0 對位項:
- 5 條鐵律:①②③④⑤
- 散戶語言錨:是否影響 §_consult-index §6

## 風險與回滾

<!-- 預期影響範圍、回滾方式、是否需通知 kaecer -->
